"""
엔진 검증 2: 도매 + BM 층 엔진이 Dinorwig의 실제 운전과 수익을 설명하나.

    .venv/bin/python -m gbess.validation.psh_bm

검증 1(psh_headroom)에서 도매만 쓰는 엔진은 실제 Dinorwig를 설명하지 못했다(09 문서 5.4). 실제 수익 경로는 BM이고(5.5),
결산서상 가용률은 2016년 99.5% → 2025년 31.5%로 떨어졌다. 그래서 이번에는
  - BM 층(gbess.engine.dispatch_bm)과 두 단계 롤링(gbess.engine.rolling_bm)
  - 유닛 정지(MEL·MIL, gbess.data.availability)
를 넣고 다시 맞춘다.

BM 기회의 기준 무리 (Dinorwig 자신은 늘 뺀다. 넣으면 순환 논리)
  A. ffes:     Ffestiniog 단독. 같은 구역·같은 사업자의 양수발전. 2024년부터 정지라 2017~2023만
  B. national: 전국 저장장치(양수 + 배터리). 2023년 전에는 배터리가 적어 사실상 양수 무리
보정·검증 (07 문서 T13): κ ∈ KAPPAS를 2017~2020년 BM 지시 물량(offer + bid)의 로그 오차 제곱합으로 고르고,
  2021년 이후로 검증한다. 롤링은 3일 지평, 평균 예측.
결과: results/validation/psh_bm.csv
"""
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "validation"
KAPPAS = [0.25, 0.5, 1.0, 2.0]
TRAIN = [2017, 2018, 2019, 2020]
FLEETS = {"ffes": {"kw": {"tech": "psh", "scotland": False}, "years": range(2017, 2024)},
          "national": {"kw": {}, "years": range(2017, 2026)}}


def one(args):
    fleet, year, kappa = args
    from gbess.data.availability import site_availability
    from gbess.data.bm_opportunity import opportunity
    from gbess.data.prices import load_mid
    from gbess.engine.asset import load_technologies
    from gbess.engine.dispatch_bm import summarise_bm
    from gbess.engine.rolling_bm import run_bm
    a = load_technologies()["dinorwig"]
    s, e, w0 = f"{year}-01-01", f"{year + 1}-01-01", f"{year - 1}-12-01"
    kw = FLEETS[fleet]["kw"]
    p, rep = load_mid(s, e)
    wp, _ = load_mid(w0, s)
    o = opportunity(s, e, exclude_sites=("DINO",), **kw)
    wo = opportunity(w0, s, exclude_sites=("DINO",), **kw)
    av = site_availability("DINO", s, e, pump_unit_mw=275)
    out, meta = run_bm(p, o, a, horizon_days=3, method="avg", warmup_price=wp, warmup_opp=wo, avail=av,
                       kappa_offer=kappa, kappa_bid=kappa)
    r = summarise_bm(out, a)
    return {"fleet": fleet, "year": year, "kappa": kappa, **{f"model_{k}": v for k, v in r.items()},
            "avail_mean_mw": float(av["mel_mw"].mean()), "fleet_active_mw": float(o["active_mw"].mean()),
            "mid_filled_ssp": rep["filled_ssp"], "solve_seconds": meta["solve_seconds"],
            "imbalance_fallback_days": len(meta["imbalance_fallback_days"]), "imbalance_mwh": meta["imbalance_mwh"]}


def realized():
    m = pd.read_csv(ROOT / "results" / "realized" / "psh_monthly.csv")
    m = m[m["site"] == "DINO"].assign(year=lambda d: d["month"].str[:4].astype(int))
    g = m.groupby("year").agg(real_gen_mwh=("phys_gen_mwh", "sum"), real_offer_mwh=("boa_up_mwh", "sum"),
                              real_bid_mwh=("boa_down_mwh", "sum"), real_wholesale=("wholesale_mid_gbp", "sum"),
                              real_offer=("bm_offer_gbp", "sum"), real_bid=("bm_bid_gbp", "sum"),
                              real_bsuos=("bsuos_gbp", "sum"))
    k = 1728 * 1e3   # £ → £k/MW/yr (연 단위라 연환산 불필요)
    g["real_gross_k_per_mw_yr"] = (g["real_wholesale"] + g["real_offer"] + g["real_bid"]) / k
    g["real_bsuos_k"] = g["real_bsuos"] / k
    # 엔진도 BSUoS를 빼므로(2026-10-29부터) 비교 기준은 BSUoS를 뺀 순액이다
    g["real_total_k_per_mw_yr"] = g["real_gross_k_per_mw_yr"] - g["real_bsuos_k"]
    g["real_bm_k"] = (g["real_offer"] + g["real_bid"]) / k
    return g.reset_index()


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-year", type=int, default=2025, help="이 해까지만 (자료가 다 받아지지 않았을 때)")
    a = ap.parse_args(argv)
    jobs = [(f, y, k) for f, spec in FLEETS.items() for y in spec["years"] if y <= a.max_year for k in KAPPAS]
    from concurrent.futures import as_completed
    rows = []
    with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 2)) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for i, f in enumerate(as_completed(futs), 1):   # 하나 끝날 때마다 진행 상황을 찍는다
            rows.append(f.result())
            print(f"[{i}/{len(jobs)}] {futs[f]} 완료", flush=True)
    m = pd.DataFrame(rows).merge(realized(), on="year")
    m["model_bm_mwh"] = m["model_offer_mwh"] + m["model_bid_mwh"]
    m["real_bm_mwh"] = m["real_offer_mwh"] + m["real_bid_mwh"]
    m["model_bm_k"] = m["model_bm_offer_k"] + m["model_bm_bid_k"]
    m["log_bm_err"] = np.log(m["model_bm_mwh"].clip(lower=1) / m["real_bm_mwh"])
    m["period"] = np.where(m["year"].isin(TRAIN), "train", "test")
    best = (m[m["period"] == "train"].groupby(["fleet", "kappa"])["log_bm_err"].apply(lambda e: float((e ** 2).sum()))
            .groupby(level=0).idxmin().map(lambda t: t[1]))
    m["chosen"] = m.apply(lambda r: r["kappa"] == best[r["fleet"]], axis=1)
    OUT.mkdir(parents=True, exist_ok=True)
    m.to_csv(OUT / "psh_bm.csv", index=False)
    cols = ["year", "period", "model_gen_mwh", "real_gen_mwh", "model_bm_mwh", "real_bm_mwh",
            "model_total_k_per_mw_yr", "real_total_k_per_mw_yr", "model_bm_k", "real_bm_k", "avail_mean_mw"]
    for f in FLEETS:
        c = m[(m["fleet"] == f) & m["chosen"]].sort_values("year")
        print(f"\n== 기준 무리 {f}, 선택 κ = {best[f]}")
        print(c[cols].round(1).to_string(index=False))
        t = c[c["period"] == "test"]
        print("검증 기간 평균 절대 오차 %: 발전량",
              round(float((t["model_gen_mwh"] / t["real_gen_mwh"] - 1).abs().mean() * 100), 1),
              "/ BM 물량", round(float((t["model_bm_mwh"] / t["real_bm_mwh"] - 1).abs().mean() * 100), 1),
              "/ 거래 수익", round(float((t["model_total_k_per_mw_yr"] / t["real_total_k_per_mw_yr"] - 1).abs().mean() * 100), 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
