"""
도매 + BM 두 단계 롤링 운전.

하루(D)마다:
  1. 하루 전 단계 (D 00:00 UTC): 그 전까지의 도매 가격과 BM 기회(MW당 지시 물량·단가)만으로 앞으로 horizon_days일을
     예측하고(gbess.engine.rolling.forecast, 계열마다 같은 방법), 도매 + 예상 BM으로 최적화해 D의 FPN을 정한다.
  2. 실시간 단계: D의 FPN을 고정하고, D의 실제 BM 기회로 지시 수락과 실제 운전을 정한다.
     끝 저장량은 1단계와 같은 water value로 평가한다.
정보 가정 (결과에 기록): 2단계는 D 하루의 BM 기회를 미리 안다. 실제로는 지시가 실시간에 오므로 이 단계는 상한 쪽이다.
가용 출력(정지)은 운영자가 미리 아는 정보로 두고 두 단계 모두 실제 값을 쓴다.
reserve_price(£/MW/h)를 주면 1단계가 FPN과 함께 그날의 예비력 r을 정하고, 2단계는 그 r을 지킨다(gbess.engine.dispatch_bm).
2단계가 r을 지키며 풀리지 않으면 불균형 대비책에서는 r을 다시 고르게 한다(그날은 기록에 남는다).
info (09 문서 5.11)
    "forecast"     1단계는 과거 값으로 만든 예측만 쓴다(기본, 정보 수준 1).
    "price_known"  1단계가 D의 도매 가격(MID)은 실제 값을 안다. 이후 날과 BM 기회는 예측 그대로.
                   실제 운영자는 하루 전 경매 가격과 당일 시장을 보고 게이트 마감 1시간 전까지 FPN을 고치므로,
                   "forecast"와 이 값 사이에 실제 정보 수준이 있다.
charges(열 export_gbp_mwh, import_gbp_mwh; gbess.data.charges)를 주면 운전량 요금을 뺀다. 1단계는 지난 7일 평균을
    지평 전체에 쓰고(사후 재정산 값은 미리 모른다), 2단계는 실제 값을 쓴다.
start_cost(£/유닛 기동)를 주면 양수형 유닛 기동 비용을 넣고, 유닛 상태를 다음 날로 넘긴다(gbess.engine.dispatch_bm).
입찰 단가 띠 (opp에 alpha_offer_0, offer_price_0, … 열이 있을 때, 09 문서 3.9; gbess.model.bm_accept.alpha_ladder)
    1단계는 띠마다의 α와 단가를 예측해 FPN과 함께 구간마다 띠(단가)를 고른다. 2단계에서 그 단가를 어떻게 다루나:
    price_choice="plan"      1단계가 고른 띠를 그대로 낸다(기본). 2단계는 그 띠의 실제 α만 본다. 단가를 미리 정해
                             내는 것이므로 단가 선택에 미래 정보가 들어가지 않는다(하한 쪽).
    price_choice="realtime"  2단계가 그날의 실제 α를 보고 띠를 다시 고른다. 실제로는 게이트 마감(1시간 전)까지 단가를
                             고칠 수 있지만, NESO가 그 구간에 무엇을 받아 줄지는 모르므로 이것은 상한 쪽이다.
    1단계에서 고른 띠가 없는(받을 물량을 0으로 계획한) 구간은 예측 α_k × (단가_k − 지평 중앙 가격)이 가장 큰 띠를
    낸다(bid는 α_k × (중앙 가격 − 단가_k)). 결과의 offer_band, bid_band 열이 실제로 낸 띠 번호다.
"""
import re

import numpy as np
import pandas as pd

from .dispatch_bm import solve_bm
from .rolling import SP_DAY, forecast

OPP_COLS = ["offer_mw_per_mw", "bid_mw_per_mw", "offer_price", "bid_price"]
ACC_COLS = ["alpha_offer", "alpha_bid"]   # 채택 모형 방식 (gbess.engine.dispatch_bm 머리말)


def _band_cols(opp: pd.DataFrame):
    """띠 열 이름: {"offer": [(α 열, 단가 열), ...], "bid": [...]}. 띠가 없으면 빈 dict."""
    out = {}
    for side in ("offer", "bid"):
        ks = sorted(int(c.rsplit("_", 1)[1]) for c in opp.columns if re.fullmatch(f"alpha_{side}_\\d+", c))
        if ks:
            out[side] = [(f"alpha_{side}_{k}", f"{side}_price_{k}") for k in ks]
    return out


def _fc_opp(hist_opp: pd.DataFrame, hist_price: np.ndarray, H, method):
    """BM 기회 예측. 단가 결측(지시 없던 구간)은 같은 구간 도매 가격으로 채운 뒤 예측한다 (상한도 0이라 영향 없음).
    띠가 있으면 띠마다의 α와 단가를 같은 방법으로 예측한다."""
    out = {}
    bands = _band_cols(hist_opp)
    if bands:
        qty = [a for side in bands.values() for a, _ in side]
        prices = [pr for side in bands.values() for _, pr in side]
    else:
        qty = ACC_COLS if "alpha_offer" in hist_opp.columns else ["offer_mw_per_mw", "bid_mw_per_mw"]
        prices = ["offer_price", "bid_price"]
    for c in qty:
        out[c] = forecast(np.nan_to_num(hist_opp[c].to_numpy(float)), H, method)
    for c in prices:
        v = hist_opp[c].to_numpy(float)
        v = np.where(np.isnan(v), hist_price[-len(v):], v)
        out[c] = forecast(v, H, method)
    return out


def _chosen_bands(plan: pd.DataFrame, fo: dict, bands: dict, ref_price: float, n: int):
    """1단계 해에서 처음 n구간에 낼 띠 번호. 받을 물량을 계획하지 않은 구간은 예측 기대이익이 가장 큰 띠."""
    out = {}
    for side, sign in (("offer", 1.0), ("bid", -1.0)):
        A = np.column_stack([fo[a][:n] for a, _ in bands[side]])
        Pr = np.column_stack([fo[pr][:n] for _, pr in bands[side]])
        score = A * sign * (Pr - ref_price)
        pick = plan[f"{side}_band"].to_numpy()[:n].copy()
        none = pick < 0
        pick[none] = score[none].argmax(axis=1)
        out[side] = pick.astype(int)
    return out


def _fix_bands(opp_day: pd.DataFrame, bands: dict, pick: dict):
    """그날 실제 띠 열에서 고른 띠 하나만 남긴 채택 모형 입력(alpha_offer, offer_price, …)."""
    out = pd.DataFrame(index=opp_day.index)
    rows = np.arange(len(opp_day))
    for side in ("offer", "bid"):
        A = opp_day[[a for a, _ in bands[side]]].to_numpy(float)
        Pr = opp_day[[pr for _, pr in bands[side]]].to_numpy(float)
        out[f"alpha_{side}"] = A[rows, pick[side]]
        out[f"{side}_price"] = Pr[rows, pick[side]]
    return out


def run_bm(price: pd.Series, opp: pd.DataFrame, asset, horizon_days=3, method="avg", warmup_price: pd.Series = None,
           warmup_opp: pd.DataFrame = None, avail: pd.DataFrame = None, kappa_offer=1.0, kappa_bid=1.0, gap=1e-4,
           reserve_price=None, reserve_hours=1.0, info="forecast", start_cost=None, charges=None, price_choice="plan"):
    if len(price) % SP_DAY:
        raise ValueError("기간은 하루(48구간) 단위여야 합니다")
    opp = opp.reindex(price.index)
    hp = warmup_price.to_numpy(float) if warmup_price is not None else np.array([])
    ho = warmup_opp.reindex(warmup_price.index) if warmup_opp is not None else opp.iloc[:0]
    actual = price.to_numpy(float)
    H = horizon_days * SP_DAY
    s = asset.soc_init * asset.e_mwh
    days, seconds, fallback_days = [], 0.0, []
    if info not in ("forecast", "price_known"):
        raise ValueError(info)
    if price_choice not in ("plan", "realtime"):
        raise ValueError(price_choice)
    bands = _band_cols(opp)
    if bands and set(bands) != {"offer", "bid"}:
        raise ValueError("입찰 단가 띠는 offer와 bid 모두 있어야 합니다")
    units = None

    def avail_slice(a, b):
        if avail is None:
            return {}
        x = avail.reindex(price.index).iloc[a:b]
        return {"p_dis_t": x["mel_mw"].to_numpy(), "p_ch_t": x["mil_mw"].to_numpy(),
                "pump_units_t": x["units_pump"].to_numpy() if asset.pump_units else None}

    for k in range(len(actual) // SP_DAY):
        a, b = k * SP_DAY, (k + 1) * SP_DAY
        past_p = np.r_[hp, actual[:a]]
        past_o = pd.concat([ho, opp.iloc[:a]])
        if len(past_p) < SP_DAY:
            past_p, past_o = actual[:SP_DAY], opp.iloc[:SP_DAY]   # 과거가 없으면 첫날만 그날 값으로 (첫날 한정)
        fp = forecast(past_p, H, method)
        if info == "price_known":
            fp[:SP_DAY] = actual[a:b]
        fo = _fc_opp(past_o, past_p, H, method)
        idx = pd.date_range(price.index[a], periods=H, freq="30min")
        wv = float(np.median(fp)) * asset.eta_dis
        av = avail_slice(a, a + H)
        if av and len(av["p_dis_t"]) < H:   # 기간 끝: 마지막 가용값을 늘려 붙인다
            av = {key: (None if v is None else np.resize(v, H) if len(v) == 0 else np.r_[v, np.full(H - len(v), v[-1])])
                  for key, v in av.items()}
        rk = dict(reserve_price=reserve_price, reserve_hours=reserve_hours, start_cost=start_cost, units_start=units)
        ch_plan = ch_real = None
        if charges is not None:
            c = charges.reindex(price.index)
            past = c.iloc[max(0, a - 7 * SP_DAY):a] if a > 0 else c.iloc[:SP_DAY]
            ch_plan = tuple(np.full(H, np.nan_to_num(past[k_].mean())) for k_ in ("export_gbp_mwh", "import_gbp_mwh"))
            ch_real = tuple(c[k_].to_numpy()[a:b] for k_ in ("export_gbp_mwh", "import_gbp_mwh"))
        plan, i1 = solve_bm(pd.Series(fp, index=idx), pd.DataFrame(fo, index=idx), asset, kappa_offer, kappa_bid,
                            terminal="value", water_value=wv, s_start=s, gap=gap, charges=ch_plan, **rk, **av)
        fpn = plan["fpn_mw"].to_numpy()[:SP_DAY].copy()
        fpn[np.abs(fpn) < 1e-6] = 0.0
        if asset.pump_units:   # FPN 양수는 펌프 단위의 배수여야 한다. 미세한 수치 오차를 맞춘다
            unit = asset.p_ch_mw / asset.pump_units
            neg = fpn < 0
            fpn[neg] = -np.round(-fpn[neg] / unit) * unit
        kw2 = dict(fpn_fixed=fpn, terminal="value", water_value=wv, s_start=s, gap=gap, charges=ch_real, **rk,
                   **avail_slice(a, b))
        r_plan = plan["reserve_mw"].to_numpy()[:SP_DAY] if reserve_price is not None else None
        opp_day = opp.iloc[a:b]
        if bands and price_choice == "plan":   # 1단계가 고른 단가를 낸다
            pick = _chosen_bands(plan, fo, bands, float(np.median(fp)), SP_DAY)
            opp_day = _fix_bands(opp_day, bands, pick)
        try:
            real, i2 = solve_bm(price.iloc[a:b], opp_day, asset, kappa_offer, kappa_bid, reserve_fixed=r_plan, **kw2)
        except RuntimeError:
            # 그래도 풀리지 않으면 불균형을 벌금(£1,000/MWh)으로 허용해 다시 푼다. 횟수와 물량을 기록한다
            real, i2 = solve_bm(price.iloc[a:b], opp_day, asset, kappa_offer, kappa_bid,
                                imbalance_penalty=1000.0, **kw2)
            fallback_days.append(str(price.index[a].date()))
        if bands and price_choice == "plan":   # 받은 물량이 없어도 낸 띠를 기록한다
            real["offer_band"], real["bid_band"] = pick["offer"], pick["bid"]
        s = float(real["soc_mwh"].iat[-1])
        if start_cost is not None and "gen_units" in real:
            units = (float(real["gen_units"].iat[-1]), float(real["pump_units"].iat[-1]))
        real["fpn_forecast_price"] = fp[:SP_DAY]
        days.append(real)
        seconds += i1["seconds"] + i2["seconds"]
    out = pd.concat(days)
    meta = {"horizon_days": horizon_days, "method": method, "kappa": (kappa_offer, kappa_bid),
            "reserve_price": reserve_price, "reserve_hours": reserve_hours, "info": info, "start_cost": start_cost,
            "charges": charges is not None, "price_choice": price_choice if bands else None,
            "bands": {k_: len(v) for k_, v in bands.items()},
            "solve_seconds": round(seconds, 1), "end_soc_mwh": s, "imbalance_fallback_days": fallback_days,
            "imbalance_mwh": float(out["imbalance_mw"].abs().sum() * 0.5) if "imbalance_mw" in out else 0.0,
            "information": ("FPN은 D 00:00에 예측으로 정함. 실시간 단계는 D의 실제 계통 상태로 계산한 채택 기댓값(α)을 씀"
                            if "alpha_offer" in opp.columns else
                            "FPN은 D 00:00에 예측으로 정함. BM 수락은 D의 실제 BM 기회를 미리 안다고 가정(상한 쪽)")}
    return out, meta
