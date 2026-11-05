"""
구역 선택 메모(T3)를 위한 경계 제약 통계. NESO 하루 전 경계 조류·한도(Day-Ahead Constraint Flows and Limits)에서
제약 그룹별로 "얼마나 자주, 얼마나 크게 묶이나"를 연도별로 센다. 메모: docs/notes/zones_choice_KO.md.

    .venv/bin/python -m gbess.system.zones_analysis            # 표를 출력하고 results/system/zones/에 csv 저장

자료 규칙 (gbess/config/spec.yaml validation.data_rules, 사전등록)
  - 2024-05-01 이후만 쓴다. 2024-04-22에 정의가 바뀌었고, 그 전에는 조류가 한도에서 잘려 있다.
  - 한도 ≤ 0 또는 ≥ 9999인 구간은 자리채움 값이라 뺀다.
  - 30분 값을 1시간 평균으로 묶는다(한도와 조류 각각 평균). 한 시간에 유효한 30분 값이 하나뿐이면 그 값을 쓴다.
  - 제약 = 1시간 조류 ≥ 1시간 한도. 0.95 × 한도는 "한도 근처"로 따로 센다(민감도).
  - 초과량 = Σ max(조류 − 한도, 0) × 1시간 (MWh). "조치 전 예상 조류" 기준이라 실제로 넘친 양이 아니다.
  - 사본은 data/raw/neso_sql/da_constraint_flows.parquet (2026-10-24까지). 이 모듈은 새로 받지 않는다.
시각 열은 GMT/BST 현지 시각 문자열이다. 시간 묶기는 문자열의 날짜·시(앞 13자)로 한다. 서머타임이 끝나는 날의 겹치는 한 시간은
네 구간이 한 시간으로 묶이지만 연간 통계에는 영향이 무시할 만하다.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "raw" / "neso_sql" / "da_constraint_flows.parquet"
OUT = ROOT / "results" / "system" / "zones"
START = "2024-05-01"
SNAPSHOT_END = "2026-10-24"
NEAR = 0.95
B4, B6 = "SSE_SP2", "SCOTEX"


def load_hourly(path=SRC, start=START):
    """30분 자료 → 그룹 × 1시간 평균 (columns: group, hour, limit, flow)."""
    d = pd.read_parquet(path)
    d = pd.DataFrame({
        "time": d["Date_ Time GMT_BST"].astype(str),
        "group": d["Constraint Group"].astype(str),
        "limit": pd.to_numeric(d["Limit_MW"], errors="coerce"),
        "flow": pd.to_numeric(d["Flow_MW"], errors="coerce"),
    })
    return to_hourly(d, start)


def to_hourly(d, start=START):
    d = d[d["time"] >= start]
    d = d[(d["limit"] > 0) & (d["limit"] < 9999)].dropna(subset=["limit", "flow"])
    d = d.assign(hour=d["time"].str.slice(0, 13))
    h = d.groupby(["group", "hour"], as_index=False)[["limit", "flow"]].mean()
    h["year"] = h["hour"].str.slice(0, 4).astype(int)
    return h


def binding_stats(h):
    """그룹 × 연도: 유효 시간 수, 제약 비율(조류 ≥ 한도), 한도 근처 비율(≥ 0.95 × 한도), 초과량 TWh, 한도 중앙값·P10."""
    x = h.assign(bind=h["flow"] >= h["limit"], near=h["flow"] >= NEAR * h["limit"],
                 exceed=np.maximum(h["flow"] - h["limit"], 0.0))
    g = x.groupby(["group", "year"])
    return pd.DataFrame({
        "hours": g.size(),
        "bind_frac": g["bind"].mean(),
        "near_frac": g["near"].mean(),
        "exceed_twh": g["exceed"].sum() / 1e6,
        "limit_median": g["limit"].median(),
        "limit_p10": g["limit"].quantile(0.10),
    }).reset_index()


def joint_stats(h, a=B4, b=B6):
    """연도별 두 경계 a, b.
    비율(a 또는 b 제약, 둘 다, b일 때 a도 제약)은 두 경계가 함께 있는 시간(hours)만으로 센다.
    큰 쪽 초과량(max_exceed_twh)은 하나라도 있는 시간을 모두 세고, 없는 쪽은 0으로 둔다(R04의 7.42 TWh와 같은 방식)."""
    x = h[h["group"].isin([a, b])].assign(ex=lambda x: np.maximum(x["flow"] - x["limit"], 0.0),
                                          bind=lambda x: x["flow"] >= x["limit"])
    ex = x.pivot_table(index=["year", "hour"], columns="group", values="ex")
    bind = x.pivot_table(index=["year", "hour"], columns="group", values="bind").dropna().astype(bool)
    both = bind[a] & bind[b]
    g = bind.groupby(level="year")
    return pd.DataFrame({
        "hours": g.size(),
        "either_frac": (bind[a] | bind[b]).groupby(level="year").mean(),
        "both_frac": both.groupby(level="year").mean(),
        "a_given_b": both.groupby(level="year").sum() / bind[b].groupby(level="year").sum(),
        "max_exceed_twh": ex.max(axis=1).groupby(level="year").sum() / 1e6,
    })


def main():
    h = load_hourly()
    s = binding_stats(h)
    j = joint_stats(h)
    OUT.mkdir(parents=True, exist_ok=True)
    s.to_csv(OUT / "binding_by_group_year.csv", index=False)
    j.to_csv(OUT / "b4_b6_joint_by_year.csv")
    pd.set_option("display.width", 200)
    print(f"자료: {SRC.relative_to(ROOT)} ({START} ~ {SNAPSHOT_END}), 1시간 평균")
    print(s.round(3).to_string(index=False))
    print(f"\nB4({B4})·B6({B6}) 함께")
    print(j.round(3).to_string())


if __name__ == "__main__":
    main()
