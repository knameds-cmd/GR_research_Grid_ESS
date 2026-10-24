"""
BM 유닛의 출력 경로를 분 단위로 복원한다: PN(사업자가 낸 계획) 위에 BOALF(NESO의 BM 지시)를 덮어쓴다.

- PN과 BOALF는 모두 (timeFrom, levelFrom) → (timeTo, levelTo) 직선 구간의 모음이다. 단위는 MW(발전 +, 양수·충전 −).
- BOALF는 지시 번호(acceptanceNumber)마다 여러 구간을 가진다. 뒤에 나온 지시가 겹치는 시간의 앞선 지시를 대체하므로,
  지시 시각 순서대로 덮어쓴다. 지시가 끝난 뒤에는 그 지시에 들어 있는 복귀 구간까지만 반영되고, 그 다음은 PN으로 돌아간다.
- 이렇게 만든 "지시 반영 출력"은 실측 출력이 아니다. 지시를 따르지 못한 편차(불균형)는 실측 자료(B1610)가 있어야 보인다.
결과는 결제구간(30분)별 에너지(MWh): pn_mwh(계획), phys_mwh(지시 반영), boa_mwh = phys − pn(BM으로 바뀐 양).
"""
import numpy as np
import pandas as pd

MIN = np.timedelta64(1, "m")


def _paint(values, t0, frm, to, lfrom, lto):
    """values[분]에 직선 구간들을 순서대로 칠한다. 각 구간은 [frm, to) 분을 덮는다."""
    i0 = ((frm - t0) // MIN).astype(np.int64)
    i1 = ((to - t0) // MIN).astype(np.int64)
    n = len(values)
    for a, b, la, lb in zip(i0, i1, lfrom, lto):
        if b <= a:
            continue
        lo, hi = max(a, 0), min(b, n)
        if hi <= lo:
            continue
        k = np.arange(lo, hi)
        # 구간 시작점에서 levelFrom, 끝점에서 levelTo. 분의 중간값을 써서 에너지를 정확히 적분
        values[lo:hi] = la + (lb - la) * ((k - a) + 0.5) / (b - a)


def unit_profile(pn, boalf, start, end):
    """한 유닛의 [start, end) 분 단위 출력. pn, boalf는 그 유닛의 행만. 반환: (분 시각, pn_mw, phys_mw)."""
    t0 = np.datetime64(pd.Timestamp(start).tz_convert("UTC").tz_localize(None), "m")
    t1 = np.datetime64(pd.Timestamp(end).tz_convert("UTC").tz_localize(None), "m")
    n = int((t1 - t0) // MIN)
    pn_mw = np.full(n, np.nan)

    def times(s):
        return pd.to_datetime(s, utc=True).dt.tz_localize(None).to_numpy().astype("datetime64[m]")

    if len(pn):
        p = pn.sort_values("timeFrom")
        _paint(pn_mw, t0, times(p["timeFrom"]), times(p["timeTo"]), p["levelFrom"].to_numpy(float),
               p["levelTo"].to_numpy(float))
    phys = pn_mw.copy()
    if len(boalf):
        b = boalf.sort_values(["acceptanceTime", "acceptanceNumber", "timeFrom"])
        _paint(phys, t0, times(b["timeFrom"]), times(b["timeTo"]), b["levelFrom"].to_numpy(float),
               b["levelTo"].to_numpy(float))
    minutes = t0 + np.arange(n) * MIN
    return minutes, pn_mw, phys


def sp_energy(pn, boalf, start, end):
    """유닛별·결제구간별 에너지 표. PN이 없는 분은 0 MW로 본다(그 유닛이 계획을 내지 않음)."""
    out = []
    units = sorted(set(pn["bmUnit"]) | set(boalf["bmUnit"]))
    for u in units:
        m, p, f = unit_profile(pn[pn["bmUnit"] == u], boalf[boalf["bmUnit"] == u], start, end)
        missing = np.isnan(p)
        p = np.where(missing, 0.0, p)
        f = np.where(np.isnan(f), 0.0, f)
        sp = (m - m[0]) // np.timedelta64(30, "m")
        df = pd.DataFrame({"sp": sp, "pn": p / 60, "phys": f / 60, "pn_missing_min": missing})
        g = df.groupby("sp").sum()
        g.index = pd.DatetimeIndex(m[0] + g.index.to_numpy() * np.timedelta64(30, "m")).tz_localize("UTC")
        g.index.name = "start_utc"
        g = g.rename(columns={"pn": "pn_mwh", "phys": "phys_mwh"})
        g["boa_mwh"] = g["phys_mwh"] - g["pn_mwh"]
        g["bmUnit"] = u
        out.append(g.reset_index())
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()
