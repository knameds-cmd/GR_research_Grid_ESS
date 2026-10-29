"""
엔진 검증 5: 실제 Dinorwig는 왜 대부분 쉬는가. 세 가설을 시험한다 (09 문서 5.11).

    .venv/bin/python -m gbess.validation.psh_idle

1. 분해 (엔진을 돌리지 않음): 실제 FPN을 엔진과 같은 잣대(도매 = FPN × MID, BM = 채택 모형 α × 여유 × 자기 단가)로
   값을 매긴다. 엔진이 고른 FPN보다 실제 FPN이 이 잣대에서 더 벌면, 실제 운영자는 "손해 보며 쉬는" 것이 아니라
   엔진이 모르는 것을 알고 더 잘 고르는 것이다. → psh_idle.csv의 real_*·realfpn_* 열
2. 정보 가설: 1단계(FPN 결정)가 D의 도매 가격을 안다(info="price_known", gbess.engine.rolling_bm).
3. 기동 비용 가설: 유닛 기동마다 START_COST £를 뺀다(gbess.engine.dispatch_bm). 값은 문헌 확인 전 임시값이다.
   운전 지표: 유닛 단위 쉬는 비율과 기동 횟수. 실제 값은 PN에서 같은 정의로 센다(FPN 기준, 유닛 단위).
설정: others_train 로짓, 3일 지평, 정지 반영, 예비력 단가 0, BSUoS 반영.
결과: results/validation/psh_idle.csv
"""
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.validation.psh_bm import realized

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "validation"
YEARS = range(2017, 2026)
SETTING, KIND = "others_train", "logit"   # 2026-10-29: 검증 기간과 겹치지 않는 모형 (독립 심사 지적)
MW, UNITS, GEN_UNIT, PUMP_UNIT = 1728, 6, 288.0, 275.0
START_COST = 3000.0
CASES = [("forecast", None), ("price_known", None), ("forecast", START_COST), ("price_known", START_COST)]


def fpn_units(fpn):
    """사이트 FPN(MW) → 유닛 단위 발전·양수 유닛 수. 실제와 엔진에 같은 정의를 쓴다."""
    f = np.asarray(fpn, float)
    gen = np.ceil(np.clip(f, 0, None) / GEN_UNIT - 1e-6)
    pump = np.round(np.clip(-f, 0, None) / PUMP_UNIT)
    return gen, pump


def real_operation(year):
    """실제 PN에서 유닛 단위 쉬는 비율과 유닛당 연 기동 횟수(FPN 기준)."""
    from gbess.model.bm_accept import load_panel
    P = load_panel([year])
    d = P[P["site"] == "DINO"].sort_values(["bmUnit", "t"])
    on = d["fpn_mw"].abs() >= 1
    starts = (on & ~on.groupby(d["bmUnit"]).shift(1, fill_value=False)).groupby(d["bmUnit"]).sum()
    return {"real_unit_idle": float((~on).mean()), "real_starts_per_unit": float(starts.mean())}


def decompose(year):
    """실제 FPN을 엔진 잣대로 값 매기기 (£k/MW/yr)."""
    from gbess.data.availability import site_availability
    from gbess.data.charges import bsuos_storage
    from gbess.model.bm_accept import alphas, load_panel, site_frame, trained
    al = alphas(trained("DINO", SETTING, KIND), site_frame("DINO", [year]))
    P = load_panel([year])
    f = P[P["site"] == "DINO"].groupby("t")["fpn_mw"].sum()
    av = site_availability("DINO", f"{year}-01-01", f"{year + 1}-01-01", pump_unit_mw=PUMP_UNIT)
    d = al.join(f.rename("fpn")).join(av[["mel_mw", "mil_mw"]]).dropna(subset=["fpn"])
    pt, pct = d["mel_mw"].clip(upper=MW), d["mil_mw"].abs().clip(upper=1650)
    o = d["alpha_offer"] * (pt - d["fpn"]).clip(lower=0)
    b = d["alpha_bid"] * (d["fpn"] + pct).clip(lower=0)
    k = MW * 1e3
    return {"realfpn_alpha_bm_k": float(((o * d["offer_price"].fillna(0)).sum() - (b * d["bid_price"].fillna(0)).sum())
                                        * 0.5 / k),
            "realfpn_alpha_bm_mwh": float((o.sum() + b.sum()) * 0.5)}


def one(args):
    info, sc, year = args
    from gbess.data.availability import site_availability
    from gbess.data.charges import bsuos_storage
    from gbess.data.prices import load_mid
    from gbess.engine.asset import load_technologies
    from gbess.engine.dispatch_bm import summarise_bm
    from gbess.engine.rolling_bm import run_bm
    from gbess.model.bm_accept import alphas, site_frame, trained
    a = load_technologies()["dinorwig"]
    s, e, w0 = f"{year}-01-01", f"{year + 1}-01-01", f"{year - 1}-12-01"
    al = alphas(trained("DINO", SETTING, KIND), site_frame("DINO", [year - 1, year]))
    p, _ = load_mid(s, e)
    wp, _ = load_mid(w0, s)
    av = site_availability("DINO", s, e, pump_unit_mw=PUMP_UNIT)
    ch = bsuos_storage(s, e)
    out, meta = run_bm(p, al.reindex(p.index), a, horizon_days=3, method="avg", warmup_price=wp,
                       warmup_opp=al.reindex(wp.index), avail=av, charges=ch, info=info, start_cost=sc)
    r = summarise_bm(out, a)
    g, k = fpn_units(out["fpn_mw"])
    on = (g + k) > 0
    return {"info": info, "start_cost": 0.0 if sc is None else sc, "year": year,
            **{f"model_{k_}": v for k_, v in r.items()},
            "model_unit_idle": float(1 - ((g + k) / UNITS).mean()),
            "model_unit_idle_actual": float(1 - ((out["gen_units"] + out["pump_units"]) / UNITS).mean()),
            "model_site_idle": float((~on).mean()),
            "model_starts_per_unit": float((np.clip(np.diff(np.r_[0, g]), 0, None).sum()
                                            + np.clip(np.diff(np.r_[0, k]), 0, None).sum()) / UNITS),
            "imbalance_fallback_days": len(meta["imbalance_fallback_days"]), "solve_seconds": meta["solve_seconds"]}


def main(argv=None):
    from gbess.model.bm_accept import trained
    trained("DINO", SETTING, KIND)
    R = realized()
    dec = pd.DataFrame([{"year": y, **decompose(y), **real_operation(y)} for y in YEARS]).merge(R, on="year")
    dec["real_wholesale_k"] = dec["real_wholesale"] / (MW * 1e3)
    dec["realfpn_alpha_total_k"] = dec["real_wholesale_k"] + dec["realfpn_alpha_bm_k"] - dec["real_bsuos_k"]
    jobs = [(i, c, y) for i, c in CASES for y in YEARS]
    rows = []
    with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 2)) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for n, f in enumerate(as_completed(futs), 1):
            rows.append(f.result())
            print(f"[{n}/{len(jobs)}] {futs[f]} 완료", flush=True)
    m = pd.DataFrame(rows).merge(dec, on="year")
    m["model_trading_k"] = m["model_total_k_per_mw_yr"] - m["model_start_cost_k"]
    OUT.mkdir(parents=True, exist_ok=True)
    m.sort_values(["info", "start_cost", "year"]).to_csv(OUT / "psh_idle.csv", index=False)

    pd.set_option("display.width", 250)
    print("\n== 1. 실제 FPN을 엔진 잣대로 (£k/MW/yr)")
    base = m[(m["info"] == "forecast") & (m["start_cost"] == 0)].sort_values("year")
    print(pd.DataFrame({"year": base["year"], "real_total": base["real_total_k_per_mw_yr"],
                        "realFPN_under_alpha": base["realfpn_alpha_total_k"],
                        "engine": base["model_total_k_per_mw_yr"]}).round(1).to_string(index=False))
    print("\n== 2·3. 경우별 평균 (2017~2025)")
    cols = ["model_gen_mwh", "real_gen_mwh", "model_trading_k", "real_total_k_per_mw_yr", "model_unit_idle",
            "real_unit_idle", "model_starts_per_unit", "real_starts_per_unit", "model_site_idle"]
    print(m.groupby(["info", "start_cost"])[cols].mean().round(2).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
