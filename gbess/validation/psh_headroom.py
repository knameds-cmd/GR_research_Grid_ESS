"""
엔진 검증 1: 예비력 여유 하나로 Dinorwig의 실제 운전을 설명할 수 있나.

    .venv/bin/python -m gbess.validation.psh_headroom

가설: 실제 Dinorwig가 엔진보다 2~3배 적게 발전하는 것(09 문서 5.2)은 응답·예비력 계약 때문에 출력 여유를 늘 비워 두기 때문이다.
방법 (07 문서 T13, 보정·검증 분리):
  1. 예비력 여유 R ∈ {0, 320, 640, 960, 1280} MW (유닛 0~4기 몫)로 2017~2025년을 롤링(3일, 평균 예측) 운전.
  2. 보정 기간 2017~2020에서 연 발전량의 로그 오차 제곱합이 가장 작은 R을 고른다.
  3. 그 R로 검증 기간 2021~2025의 발전량과 거래 수익을 실제와 비교한다.
비교 대상: 실제 발전량 = PN + BM 지시 반영 출력(gbess.realized.physical), 실제 거래 수익 = 도매(PN × MID) + BM 순수익.
주의: 엔진은 MID 가격 하나로 도매만 한다. 실제는 도매 + BM 두 경로로 번다. 그래서 수익 비교는 "같은 크기인가"를 보는 1차 점검이다.
결과: results/validation/psh_headroom.csv
"""
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "validation"
YEARS = list(range(2017, 2026))
RESERVES = [0, 320, 640, 960, 1280]
TRAIN = [2017, 2018, 2019, 2020]


def one(args):
    year, r = args
    from gbess.data.prices import load_mid
    from gbess.engine.asset import load_technologies
    from gbess.engine.dispatch import summarise
    from gbess.engine.rolling import run
    a = load_technologies()["dinorwig"]
    p, rep = load_mid(f"{year}-01-01", f"{year + 1}-01-01")
    w, _ = load_mid(f"{year - 1}-12-01", f"{year}-01-01")
    out, meta = run(p, a, horizon_days=3, method="avg", warmup=w, reserve_up_mw=r, reserve_hours=1.0)
    s = summarise(out, a)
    return {"year": year, "reserve_mw": r, "model_gen_gwh": s["discharged_mwh"] / 1e3,
            "model_margin_k_per_mw_yr": s["margin_k_per_mw_yr"], "mid_filled_ssp": rep["filled_ssp"],
            "solve_seconds": meta["solve_seconds"]}


def main():
    jobs = [(y, r) for y in YEARS for r in RESERVES]
    with ProcessPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) - 1)) as ex:
        rows = list(ex.map(one, jobs))
    m = pd.DataFrame(rows)
    real = pd.read_csv(ROOT / "results" / "realized" / "psh_annual.csv")
    real = real[real["site"] == "DINO"][["year", "gen", "trading_mid_k_per_mw_yr"]]
    real = real.rename(columns={"gen": "real_gen_mwh", "trading_mid_k_per_mw_yr": "real_trading_k"})
    real["year"] = real["year"].astype(int)
    m = m.merge(real, on="year")
    m["real_gen_gwh"] = m["real_gen_mwh"] / 1e3
    m["log_gen_err"] = np.log(m["model_gen_gwh"] / m["real_gen_gwh"])
    train = m[m["year"].isin(TRAIN)].groupby("reserve_mw")["log_gen_err"].apply(lambda e: float((e ** 2).sum()))
    best = int(train.idxmin())
    m["chosen"] = m["reserve_mw"] == best
    m["period"] = np.where(m["year"].isin(TRAIN), "train", "test")
    OUT.mkdir(parents=True, exist_ok=True)
    m.to_csv(OUT / "psh_headroom.csv", index=False)
    print("보정 기간 로그 오차 제곱합:", train.round(3).to_dict(), "→ 선택 R =", best, "MW")
    cols = ["year", "period", "model_gen_gwh", "real_gen_gwh", "model_margin_k_per_mw_yr", "real_trading_k"]
    print(m[m["chosen"]][cols].round(1).to_string(index=False))
    t = m[m["chosen"] & (m["period"] == "test")]
    print("검증 기간 발전량 평균 절대 오차 %:", round(float((np.exp(t["log_gen_err"].abs()) - 1).mean() * 100), 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
