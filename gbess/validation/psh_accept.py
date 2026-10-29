"""
엔진 검증 3: BM 채택 모형(gbess.model.bm_accept)을 넣은 엔진이 Dinorwig의 실제 운전과 수익을 설명하나.

    .venv/bin/python -m gbess.validation.psh_accept

검증 2(psh_bm)와 같은 틀(두 단계 롤링, 3일 지평, 평균 예측, MEL·MIL 가용)이고 BM 지시 상한만 바꾼다.
    검증 2: 기준 무리의 MW당 지시량 × κ (κ를 2017~2020년에 맞춤)
    검증 3: α × 여유. α = Dinorwig 자신의 입찰 단가와 그 구간 계통 상태로 채택 모형이 준 기댓값. 맞추는 값 없음
채택 모형은 Dinorwig를 뺀 양수 발전소 자료로만 맞춘다 (자기 자료로 자기를 설명하지 않게)
    others_all:   나머지 세 발전소의 2017~2026년 (채택 모형 검증 C와 같은 조건, 주 결과)
    others_train: 나머지 세 발전소의 2017~2020년만 (검증 A 조건, 가장 엄격)
입찰 단가는 Dinorwig의 실제 BOD(가용 유닛의 구간별 중앙값)를 쓴다. 가상 자산에는 따로 입찰 규칙이 필요하다.
결과: results/validation/psh_accept.csv
"""
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.validation.psh_bm import realized

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "validation"
YEARS = range(2017, 2027)
END_2026 = "2026-10-01"   # 자료 끝


def one(args):
    setting, kind, year = args
    from gbess.data.availability import site_availability
    from gbess.data.charges import bsuos_storage
    from gbess.data.prices import load_mid
    from gbess.engine.asset import load_technologies
    from gbess.engine.dispatch_bm import summarise_bm
    from gbess.engine.rolling_bm import run_bm
    from gbess.model.bm_accept import alphas, site_frame, trained
    a = load_technologies()["dinorwig"]
    s, e, w0 = f"{year}-01-01", (END_2026 if year == 2026 else f"{year + 1}-01-01"), f"{year - 1}-12-01"
    m = trained("DINO", setting, kind)
    al = alphas(m, site_frame("DINO", [year - 1, year]))
    p, rep = load_mid(s, e)
    wp, _ = load_mid(w0, s)
    o, wo = al.reindex(p.index), al.reindex(wp.index)
    av = site_availability("DINO", s, e, pump_unit_mw=275)
    ch = bsuos_storage(s, e)
    out, meta = run_bm(p, o, a, horizon_days=3, method="avg", warmup_price=wp, warmup_opp=wo, avail=av, charges=ch)
    r = summarise_bm(out, a)
    yr_frac = len(p) / (365.25 * 48)   # 2026은 아홉 달: 물량은 실제와 같은 기간 합계로 비교
    return {"setting": setting, "kind": kind, "year": year, **{f"model_{k}": v for k, v in r.items()},
            "model_gen_mwh": r["gen_mwh"], "period_years": yr_frac, "alpha_offer_mean": float(o["alpha_offer"].mean()),
            "alpha_bid_mean": float(o["alpha_bid"].mean()), "avail_mean_mw": float(av["mel_mw"].mean()),
            "mid_filled_ssp": rep["filled_ssp"], "solve_seconds": meta["solve_seconds"],
            "imbalance_fallback_days": len(meta["imbalance_fallback_days"]), "imbalance_mwh": meta["imbalance_mwh"]}


def main(argv=None):
    from gbess.model.bm_accept import trained
    for st in ("others_all", "others_train"):          # 모형을 먼저 만들어 둔다 (프로세스마다 다시 맞추지 않게)
        for k in ("logit", "gbm"):
            trained("DINO", st, k)
    jobs = [(st, k, y) for st in ("others_all", "others_train") for k in ("logit", "gbm") for y in YEARS]
    rows = []
    with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 2)) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for i, f in enumerate(as_completed(futs), 1):
            rows.append(f.result())
            print(f"[{i}/{len(jobs)}] {futs[f]} 완료", flush=True)
    m = pd.DataFrame(rows).merge(realized(), on="year")
    m["model_bm_mwh"] = m["model_offer_mwh"] + m["model_bid_mwh"]
    m["real_bm_mwh"] = m["real_offer_mwh"] + m["real_bid_mwh"]
    m["model_bm_k"] = m["model_bm_offer_k"] + m["model_bm_bid_k"]
    # summarise_bm은 연환산(£k/MW/yr), 실제 값은 그 해 합계 ÷ MW. 2026(아홉 달)은 실제 값을 연환산해 맞춘다
    for c in ("real_total_k_per_mw_yr", "real_gross_k_per_mw_yr", "real_bsuos_k", "real_bm_k"):
        m[c] = m[c] / m["period_years"].where(m["year"] == 2026, 1.0)
    OUT.mkdir(parents=True, exist_ok=True)
    m.to_csv(OUT / "psh_accept.csv", index=False)
    cols = ["year", "model_gen_mwh", "real_gen_mwh", "model_offer_mwh", "real_offer_mwh", "model_bid_mwh",
            "real_bid_mwh", "model_total_k_per_mw_yr", "real_total_k_per_mw_yr", "model_bm_k", "real_bm_k"]
    for (st, k), c in m.groupby(["setting", "kind"]):
        c = c.sort_values("year")
        print(f"\n== {st}, {k}")
        print(c[cols].round(1).to_string(index=False))
        for name, per in (("보정 기간과 겹침(2017~2020)", c["year"] <= 2020), ("검증 기간(2021~)", c["year"] >= 2021)):
            t = c[per]
            print(f"{name} 평균 절대 오차 %: 발전량",
                  round(float((t["model_gen_mwh"] / t["real_gen_mwh"] - 1).abs().mean() * 100), 1),
                  "/ BM 물량", round(float((t["model_bm_mwh"] / t["real_bm_mwh"] - 1).abs().mean() * 100), 1),
                  "/ 거래 수익", round(float((t["model_total_k_per_mw_yr"] / t["real_total_k_per_mw_yr"] - 1).abs().mean()
                                         * 100), 1),
                  "/ 불균형 대비책 쓴 날", int(t["imbalance_fallback_days"].sum()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
