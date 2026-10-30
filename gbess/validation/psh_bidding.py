"""
엔진 검증 6: 입찰 규칙. 실제 입찰 단가가 없는 가상 자산은 단가를 어떻게 정하나 (09 문서 3.9, 5.12).

    .venv/bin/python -m gbess.validation.psh_bidding                         # 전부 (72개, 병렬로 약 4~6시간 추정)
    .venv/bin/python -m gbess.validation.psh_bidding --years 2022 2024 --rules habit ladder_plan --info forecast

같은 엔진(검증 5의 주 설정: others_train 로짓, 3일 지평, 정지 반영, BSUoS, 예비력 단가 0, 기동 비용 없음)에서 BM 단가만
네 규칙으로 바꿔 Dinorwig 2017~2025년을 돌린다. 실제 Dinorwig는 실제 단가가 있으므로 규칙이 만든 수익·물량·단가를
실제와 맞대 볼 수 있다. 이 비교가 가상 장주기 자산에 어떤 규칙을 쓸지의 근거가 된다.
규칙
    actual           Dinorwig가 실제로 낸 단가(검증 3~5와 같음). 기준선
    habit            다른 양수 유닛의 2017~2020년 단가의 도매 대비 차이(중앙값)를 늘 낸다. "업계 습관" 규칙
    ladder_plan      후보 단가 띠에서 엔진이 하루 전에 기대이익이 가장 큰 단가를 고른다. 단가 선택에 그날의 실제
                     계통 상태가 들어가지 않는다(하한 쪽). 후보는 모형을 맞춘 자료의 실제 단가 범위(5~95%) 안만 둔다
                     (bm_accept.support_grid, 범위 밖은 외삽). --full-grid를 주면 OFFER_MARKUPS, BID_MARKUPS 전체
    ladder_realtime  같은 띠에서 실시간 단계가 그날 실제 α를 보고 다시 고른다(상한 쪽)
정보 수준: forecast, price_known (검증 5와 같음). 둘 × 규칙 넷 × 9년 = 72개.
기록하는 것 (results/validation/psh_bidding.csv)
    엔진 수익·물량(검증 3과 같은 열), 낸 offer 단가의 도매 대비 차이(구간 중앙값, 받은 물량 가중 평균),
    낸 단가가 실제 Dinorwig 단가 분포(그해 5~95% 구간) 안에 든 비율, 그리고 후보 범위의 끝(가장 싼·가장 비싼 띠)을 낸
    비율(offer_at_min_markup 등). 끝을 자주 내면 답이 채택 곡선이 아니라 범위 제한에서 정해진 것이라, 그 방향의 결과는
    범위에 민감하다. 2026-10-30 이틀 시험에서 bid는 92% 구간에서 가장 깊은 할인(MID − £111)을 냈다: 범위 안에서도 bid α가
    단가에 거의 반응하지 않는다(양수 bid는 단가보다 계통 필요로 받아들여진다). --full-grid로 민감도를 함께 본다.
"""
import argparse
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.validation.psh_bm import realized

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "validation"
YEARS = list(range(2017, 2026))
SITE, SETTING, KIND = "DINO", "others_train", "logit"
MW, PUMP_UNIT = 1728, 275.0
RULES = ("actual", "habit", "ladder_plan", "ladder_realtime")
INFOS = ("forecast", "price_known")


def real_markups(year):
    """실제 Dinorwig 가용 유닛의 offer − MID, MID − bid 분포(구간 중앙값의 5·50·95% 분위수)."""
    from gbess.model.bm_accept import load_panel
    P = load_panel([year])
    d = P[(P["site"] == SITE) & (P["mel_mw"] > 10)]
    g = d.groupby("t")[["offer_price", "bid_price", "mid"]].median()
    mo, mb = (g["offer_price"] - g["mid"]).dropna(), (g["mid"] - g["bid_price"]).dropna()
    q = lambda s: s.quantile([0.05, 0.5, 0.95]).to_numpy()   # noqa: E731
    (o5, o50, o95), (b5, b50, b95) = q(mo), q(mb)
    return {"real_offer_markup_p5": o5, "real_offer_markup_p50": o50, "real_offer_markup_p95": o95,
            "real_bid_markup_p5": b5, "real_bid_markup_p50": b50, "real_bid_markup_p95": b95}


def opportunity(rule, frame, models, habit, grid):
    """규칙 → 엔진 입력(α와 단가 계열)."""
    from gbess.model.bm_accept import alpha_ladder, alphas, fixed_ladder
    if rule == "actual":
        return alphas(models, frame)
    if rule == "habit":
        return fixed_ladder(frame, models, *habit)
    return alpha_ladder(models, frame, *grid)


def one(args):
    rule, info, year, habit, grid = args
    from gbess.data.availability import site_availability
    from gbess.data.charges import bsuos_storage
    from gbess.data.prices import load_mid
    from gbess.engine.asset import load_technologies
    from gbess.engine.dispatch_bm import summarise_bm
    from gbess.engine.rolling_bm import run_bm
    from gbess.model.bm_accept import site_frame, trained
    a = load_technologies()["dinorwig"]
    s, e, w0 = f"{year}-01-01", f"{year + 1}-01-01", f"{year - 1}-12-01"
    models = trained(SITE, SETTING, KIND)
    op = opportunity(rule, site_frame(SITE, [year - 1, year]), models, habit, grid)
    p, _ = load_mid(s, e)
    wp, _ = load_mid(w0, s)
    av = site_availability(SITE, s, e, pump_unit_mw=PUMP_UNIT)
    out, meta = run_bm(p, op.reindex(p.index), a, horizon_days=3, method="avg", warmup_price=wp,
                       warmup_opp=op.reindex(wp.index), avail=av, charges=bsuos_storage(s, e), info=info,
                       price_choice="realtime" if rule == "ladder_realtime" else "plan")
    r = summarise_bm(out, a)
    # 낸 단가의 도매 대비 차이 (받은 물량이 없으면 낸 띠의 단가). 단가를 내지 못한 구간(정지, 자료 없음)은 뺀다
    mo = (out["offer_price"] - out["price"]).where(out["offer_cap"] > 0)
    mb = (out["price"] - out["bid_price"]).where(out["bid_cap"] > 0)
    w = out["offer_mw"]
    row = {"rule": rule, "info": info, "year": year, **{f"model_{k}": v for k, v in r.items()},
           "offer_markup_median": float(mo.median()), "bid_markup_median": float(mb.median()),
           "offer_markup_accepted": float((mo * w).sum() / w.sum()) if w.sum() > 0 else np.nan,
           "imbalance_fallback_days": len(meta["imbalance_fallback_days"]), "solve_seconds": meta["solve_seconds"]}
    if rule.startswith("ladder"):   # 띠별로 낸 구간 비율과 범위 끝을 낸 비율
        for side, g in (("offer", grid[0]), ("bid", grid[1])):
            band = out[f"{side}_band"].where(out[f"{side}_cap"] > 0)
            for k, m in enumerate(g):
                row[f"{side}_band_share_{m:g}"] = float((band == k).mean())
            n_ = band.notna().sum()   # 범위 끝: 도매 대비 차이가 가장 작은 띠(0)와 가장 큰 띠
            row[f"{side}_at_min_markup"] = float((band == 0).sum() / n_) if n_ else np.nan
            row[f"{side}_at_max_markup"] = float((band == len(g) - 1).sum() / n_) if n_ else np.nan
    row["_mo"], row["_mb"] = mo.to_numpy(), mb.to_numpy()
    return row


def main(argv=None):
    from gbess.model.bm_accept import BID_MARKUPS, OFFER_MARKUPS, habit_markups, support_grid, trained
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, nargs="*", default=YEARS)
    ap.add_argument("--rules", nargs="*", default=list(RULES), choices=RULES)
    ap.add_argument("--info", nargs="*", default=list(INFOS), choices=INFOS)
    ap.add_argument("--full-grid", action="store_true", help="후보 단가를 실제 범위로 막지 않는다(외삽 민감도)")
    a = ap.parse_args(argv)
    trained(SITE, SETTING, KIND)
    habit = habit_markups(SITE, SETTING)
    grid = (OFFER_MARKUPS, BID_MARKUPS) if a.full_grid else support_grid(SITE, SETTING)
    print(f"습관 규칙 단가: offer = MID + £{habit[0]:.1f}, bid = MID − £{habit[1]:.1f}", flush=True)
    print(f"후보 단가: offer = MID + {grid[0]}, bid = MID − {grid[1]}", flush=True)
    jobs = [(r, i, y, habit, grid) for r in a.rules for i in a.info for y in a.years]
    rows = []
    with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 2)) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for n, f in enumerate(as_completed(futs), 1):
            rows.append(f.result())
            print(f"[{n}/{len(jobs)}] {futs[f][:3]} 완료", flush=True)
    rm = {y: real_markups(y) for y in a.years}
    for r in rows:   # 낸 단가가 실제 단가 분포 안에 든 비율 (외삽 점검)
        q = rm[r["year"]]
        mo, mb = r.pop("_mo"), r.pop("_mb")
        mo, mb = mo[~np.isnan(mo)], mb[~np.isnan(mb)]
        r["offer_markup_in_real_range"] = float(np.mean((mo >= q["real_offer_markup_p5"])
                                                        & (mo <= q["real_offer_markup_p95"])))
        r["bid_markup_in_real_range"] = float(np.mean((mb >= q["real_bid_markup_p5"]) & (mb <= q["real_bid_markup_p95"])))
        r.update(q)
    m = pd.DataFrame(rows).merge(realized(), on="year")
    m["model_bm_mwh"] = m["model_offer_mwh"] + m["model_bid_mwh"]
    m["real_bm_mwh"] = m["real_offer_mwh"] + m["real_bid_mwh"]
    m["model_bm_k"] = m["model_bm_offer_k"] + m["model_bm_bid_k"]
    m["habit_offer_markup"], m["habit_bid_markup"] = habit
    OUT.mkdir(parents=True, exist_ok=True)
    m["grid"] = "full" if a.full_grid else "support"
    m.sort_values(["rule", "info", "year"]).to_csv(OUT / ("psh_bidding_fullgrid.csv" if a.full_grid else "psh_bidding.csv"),
                                                   index=False)

    pd.set_option("display.width", 250)
    v = m[m["year"] >= 2021]
    err = lambda c, r: (v[c] / v[r] - 1).abs().mul(100)   # noqa: E731
    v = v.assign(gen_err=err("model_gen_mwh", "real_gen_mwh"), bm_err=err("model_bm_mwh", "real_bm_mwh"),
                 rev_err=err("model_total_k_per_mw_yr", "real_total_k_per_mw_yr"))
    print("\n== 검증 기간(2021~) 평균: 오차 %, 수익 £k/MW/yr, 낸 offer 단가의 도매 대비 차이 £/MWh")
    print(v.groupby(["rule", "info"])[["gen_err", "bm_err", "rev_err", "model_total_k_per_mw_yr", "model_bm_k",
                                       "real_total_k_per_mw_yr", "real_bm_k", "offer_markup_median",
                                       "real_offer_markup_p50", "offer_markup_in_real_range", "offer_at_min_markup",
                                       "offer_at_max_markup", "bid_at_max_markup"]].mean().round(2)
          .to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
