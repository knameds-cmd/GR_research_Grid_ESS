"""
엔진 검증 4: 예비력 보유에 값을 주면 엔진이 Dinorwig의 실제 운전(대부분 쉬며 여유를 남김)을 재현하나.

    .venv/bin/python -m gbess.validation.psh_reserve

검증 3(psh_accept, others_all, logit)과 같은 틀에 예비력 보유 r을 더한다(gbess.engine.dispatch_bm 머리말).
    단가 π ∈ {2, 4, 8, 16} £/MW/h, 지속 조건 1시간. π = 0은 검증 3 결과를 그대로 쓴다.
    1. 보정: 2017~2020 연 발전량의 로그 오차 제곱합이 가장 작은 π를 고른다 (운전으로 맞춘다).
    2. 검증: 그 π로 2021~2025 발전량, BM 물량, 거래 수익(예비력 제외)을 실제와 비교한다.
    3. 돈으로 따로 확인: 엔진이 번 예비력 수입을 결산서와 비교한다. 맞추는 데 쓰지 않은 독립 점검이다.
       - First Hydro(Dinorwig + Ffestiniog) 결산서 (매출 − 매출원가) − 공개 재구성 = 공개되지 않는 몫(선도 판매 포함, 상한 쪽)
       - Cruachan 결산서의 공개되지 않는 부가서비스 £26~56k/MW/yr (09 문서 5.9)
결과: results/validation/psh_reserve.csv
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
TRAIN = [2017, 2018, 2019, 2020]
PRICES = [2.0, 4.0, 8.0, 16.0]
RESERVE_HOURS = 1.0
SETTING, KIND = "others_all", "logit"
MW = 1728


def one(args):
    pi, year = args
    from gbess.data.availability import site_availability
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
    av = site_availability("DINO", s, e, pump_unit_mw=275)
    out, meta = run_bm(p, al.reindex(p.index), a, horizon_days=3, method="avg", warmup_price=wp,
                       warmup_opp=al.reindex(wp.index), avail=av, reserve_price=pi, reserve_hours=RESERVE_HOURS)
    r = summarise_bm(out, a)
    idle = float((out["net_mw"].abs() < 1.0).mean())
    return {"reserve_price": pi, "year": year, **{f"model_{k}": v for k, v in r.items()}, "model_idle_share": idle,
            "imbalance_fallback_days": len(meta["imbalance_fallback_days"]), "solve_seconds": meta["solve_seconds"]}


def zero_price():
    """π = 0: 검증 3의 같은 설정 결과."""
    v = pd.read_csv(OUT / "psh_accept.csv")
    v = v[(v["setting"] == SETTING) & (v["kind"] == KIND) & v["year"].isin(YEARS)]
    keep = [c for c in v.columns if c.startswith("model_")] + ["year", "imbalance_fallback_days", "solve_seconds"]
    return v[keep].assign(reserve_price=0.0, model_reserve_k=0.0, model_reserve_mw_mean=0.0)


def main(argv=None):
    from gbess.model.bm_accept import trained
    trained("DINO", SETTING, KIND)
    jobs = [(pi, y) for pi in PRICES for y in YEARS]
    rows = []
    with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 2)) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for i, f in enumerate(as_completed(futs), 1):
            rows.append(f.result())
            print(f"[{i}/{len(jobs)}] π={futs[f][0]} {futs[f][1]} 완료", flush=True)
    m = pd.concat([zero_price(), pd.DataFrame(rows)], ignore_index=True).merge(realized(), on="year")
    m["model_bm_mwh"] = m["model_offer_mwh"] + m["model_bid_mwh"]
    m["real_bm_mwh"] = m["real_offer_mwh"] + m["real_bid_mwh"]
    m["model_trading_k"] = m["model_total_k_per_mw_yr"] - m["model_reserve_k"]
    m["model_reserve_gbp_m"] = m["model_reserve_k"] * MW / 1e3
    m["log_gen_err"] = np.log(m["model_gen_mwh"] / m["real_gen_mwh"])
    sse = m[m["year"].isin(TRAIN)].groupby("reserve_price")["log_gen_err"].apply(lambda e: float((e ** 2).sum()))
    best = float(sse.idxmin())
    m["chosen"] = m["reserve_price"] == best
    acc = pd.read_csv(OUT / "accounts.csv")
    acc = acc[acc["entity"] == "FHC"].assign(fhc_unexplained_gbp_m=lambda d: d["acc_margin"] - d["pub_total"])
    m = m.merge(acc[["year", "fhc_unexplained_gbp_m"]], on="year", how="left")
    OUT.mkdir(parents=True, exist_ok=True)
    m.sort_values(["reserve_price", "year"]).to_csv(OUT / "psh_reserve.csv", index=False)

    print("보정 기간 발전량 로그 오차 제곱합:", sse.round(3).to_dict(), "→ 선택 π =", best)
    print("\nπ별 검증 기간(2021~2025) 평균 절대 오차 %와 예비력")
    for pi, c in m[m["year"] >= 2021].groupby("reserve_price"):
        err = lambda a, b: round(float((c[a] / c[b] - 1).abs().mean() * 100), 1)   # noqa: E731
        print(f"  π={pi:>4}: 발전 {err('model_gen_mwh', 'real_gen_mwh')} / BM 물량 {err('model_bm_mwh', 'real_bm_mwh')}"
              f" / 거래 수익 {err('model_trading_k', 'real_total_k_per_mw_yr')} / 평균 r {c['model_reserve_mw_mean'].mean():.0f} MW"
              f" / 예비력 £{c['model_reserve_k'].mean():.1f}k/MW/yr / 쉬는 구간 {c['model_idle_share'].mean():.0%}")
    cols = ["year", "model_gen_mwh", "real_gen_mwh", "model_bm_mwh", "real_bm_mwh", "model_trading_k",
            "real_total_k_per_mw_yr", "model_reserve_mw_mean", "model_reserve_gbp_m", "fhc_unexplained_gbp_m",
            "model_idle_share"]
    print(f"\n== 선택 π = {best} £/MW/h")
    print(m[m["chosen"]].sort_values("year")[cols].round(2).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
