"""
M2 검증의 관측 쪽 값 (spec.yaml validation V1~V4). 모형 없이 자료만으로 계산한다.

    .venv/bin/python -m gbess.system.observed            # results/system/m2/observed_*.csv와 표 출력

- V1 관측: NESO 하루 전 조류(da_constraint_flows, 30분, 현지 시각)를 UTC로 바꾸고 1시간 평균한다. 한도가 0 이하이거나 9999 이상인
  구간은 뺀다(spec data_rules). 제약 발생 = 1시간 평균 조류 ≥ 1시간 평균 한도. 초과량 = Σ max(F − L, 0) × 1시간.
  "B4·B6 중 큰 쪽"은 시간마다 두 경계 초과량 중 큰 값을 더한다(04 보고서 표 3의 7.42 TWh와 같은 정의, 시험으로 확인).
- V2b: Cruachan(T_CRUA-1~4) BOA 하향 MWh(PN 위에 BOALF를 덮은 출력 − PN, gbess.realized.physical) 중 B6(SCOTEX)가 제약된
  30분 구간의 몫. 기저 비율은 같은 해 B6 30분 제약 발생 비율.
- V3: 양수 유닛(Dinorwig·Ffestiniog·Cruachan, Foyers는 자연 유입 때문에 뺌)의 날마다 "순환 여부"를 PN으로 정하고, 그날 MID
  가격차에 로짓을 맞춰 순환 확률 50%가 되는 손익분기 가격차를 구한다. 규칙 변경 전후 12개월의 차이(전 − 후)가 지표다.
- V4 관측: MID(APXMIDP) 30분 가격을 1시간 평균하고 현지 날짜로 묶는다.

V3에서 spec에 없던 정의 (연구자 위임으로 정함, status: derived)
- 순환한 날: 그날 PN 양수와 PN 발전이 모두 유닛 정격 × 1시간 이상. 유닛 정격 = 발전소 순 출력 ÷ 유닛 수(psh.SITES).
  PN을 쓰는 이유: BSUoS는 사업자의 도매 계획에 영향을 주는 비용이고, BOA는 NESO의 지시라서.
- 가격차: 그날 1시간 MID 상위 k시간 평균 − 하위 k시간 평균. 주 결과 k = 4(양수 저수지 몇 시간 분량), 민감도 k = 8(V4와 같은 k).
- 로짓: 유닛·날을 모아(pool) P(순환) = σ(a + b·가격차), 손익분기 = −a/b. 90% 신뢰구간은 날 단위 블록 붓스트랩(유닛을 날과 함께
  뽑음) 1,000회의 백분위수. 변경일: CMP281 2021-04-01, CMP308 2023-04-01 (gbess.data.charges).
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
NESO = ROOT / "data" / "raw" / "neso_sql"
ELEXON = ROOT / "data" / "raw" / "elexon"
OUT = ROOT / "results" / "system" / "m2"
GROUPS = {"B6": ["SCOTEX"], "B4": ["SSE_SP", "SSE_SP2"]}   # spec validation.data_rules.boundary_map
SSE_SP2_FROM = pd.Timestamp("2024-04-21", tz="Europe/London")
PSH_SITES = ("DINO", "FFES", "CRUA")


def _localize(naive):
    """현지 시각(GMT/BST) 문자열 → UTC. 서머타임이 끝나는 날의 겹치는 한 시간은 _id 순서(먼저 BST)로 구분한다."""
    t = pd.to_datetime(naive)
    first = ~t.duplicated(keep="first")
    dup = t.duplicated(keep=False)
    amb = np.where(dup, first, False)
    return t.dt.tz_localize("Europe/London", ambiguous=amb, nonexistent="shift_forward").dt.tz_convert("UTC")


def da_flows(boundary, path=None):
    """경계 하나의 30분 조류·한도 (UTC 색인). B4는 2024-04-21 전 SSE_SP, 그 뒤 SSE_SP2."""
    d = pd.read_parquet(path or NESO / "da_constraint_flows.parquet")
    d = d[d["Constraint Group"].isin(GROUPS[boundary])].copy()
    d["_id"] = d["_id"].astype(int)
    d = d.sort_values("_id")
    out = []
    for g, x in d.groupby("Constraint Group"):
        x = x.assign(t=_localize(x["Date_ Time GMT_BST"]))
        out.append(x)
    d = pd.concat(out)
    if boundary == "B4":
        d = d[((d["Constraint Group"] == "SSE_SP") & (d["t"] < SSE_SP2_FROM))
              | ((d["Constraint Group"] == "SSE_SP2") & (d["t"] >= SSE_SP2_FROM))]
    f = pd.DataFrame({"flow": pd.to_numeric(d["Flow_MW"], errors="coerce").values,
                      "limit": pd.to_numeric(d["Limit_MW"], errors="coerce").values},
                     index=pd.DatetimeIndex(d["t"], name="t"))
    f = f[~f.index.duplicated(keep="first")].sort_index()
    bad = (f["limit"] <= 0) | (f["limit"] >= 9999) | f["flow"].isna() | f["limit"].isna()
    return f[~bad]


def hourly(f):
    """30분 → 1시간 평균. 두 구간 중 하나만 있는 시간도 그 값으로 둔다."""
    return f.groupby(f.index.floor("h")).mean()


def binding_stats(f):
    """{'binding': 제약 발생 비율, 'exceed_mwh': Σ max(F − L, 0)·dt}. f는 1시간(또는 30분) 표, dt는 색인 간격으로 추정."""
    dt = 0.5 if len(f) > 1 and (f.index[1] - f.index[0]) == pd.Timedelta("30min") else 1.0
    ex = (f["flow"] - f["limit"]).clip(lower=0)
    return {"binding": float((f["flow"] >= f["limit"]).mean()), "exceed_mwh": float(ex.sum() * dt), "hours": len(f)}


def joint_exceedance(h4, h6):
    """시간마다 B4·B6 초과량 중 큰 값 (MWh, 1시간 표). 한쪽 자료만 있는 시간은 그쪽 값."""
    e = pd.concat({"B4": (h4["flow"] - h4["limit"]).clip(lower=0),
                   "B6": (h6["flow"] - h6["limit"]).clip(lower=0)}, axis=1)
    return e.max(axis=1)


def _year(f, year):
    s, e = pd.Timestamp(f"{year}-01-01", tz="UTC"), pd.Timestamp(f"{year + 1}-01-01", tz="UTC")
    return f[(f.index >= s) & (f.index < e)]


def v1_observed(year=2025):
    """V1 관측 지표와 월별 B4·B6 큰 쪽 초과량(TWh)."""
    hb = {b: _year(hourly(da_flows(b)), year) for b in ("B4", "B6")}
    row = {f"{b}_{k}": v for b in hb for k, v in binding_stats(hb[b]).items()}
    j = joint_exceedance(hb["B4"], hb["B6"])
    row["exceed_max_B4_B6_twh"] = float(j.sum() / 1e6)
    either = pd.concat({b: hb[b]["flow"] >= hb[b]["limit"] for b in hb}, axis=1)
    row["either_binding"] = float(either.any(axis=1).mean())
    row["both_binding"] = float(either.all(axis=1).mean())
    monthly = (j.groupby(j.index.tz_convert(None).to_period("M")).sum() / 1e6).rename("exceed_max_B4_B6_twh")
    cost = thermal_cost(year)
    row.update(cost)
    return row, monthly


def thermal_cost(year=2025):
    """달력연도 열적 제약 비용(£m)과 bid 물량(TWh). constraint_breakdown은 회계연도 파일로 나뉘어 있다."""
    parts = [pd.read_parquet(p) for p in sorted(NESO.glob("constraint_breakdown_*.parquet"))]
    c = pd.concat(parts)
    c["Date"] = pd.to_datetime(c["Date"].str[:10])
    c = c.drop_duplicates("Date")
    c = c[c["Date"].dt.year == year]
    return {"thermal_cost_gbp_m": float(pd.to_numeric(c["Thermal constraints cost"]).sum() / 1e6),
            "thermal_volume_twh": float(-pd.to_numeric(c["Thermal constraints volume"]).sum() / 1e6),
            "cost_days": int(len(c))}


# ---------------------------------------------------------------------------------------------------- 양수 PN·BOA
def psh_sp(year_months, sites=PSH_SITES):
    """유닛별 30분 PN·지시 반영 에너지 (gbess.realized.physical.sp_energy). year_months: pd.Period 목록."""
    from gbess.realized.physical import sp_energy
    pat = "|".join(sites)
    out = []
    for m in year_months:
        pn = pd.read_parquet(ELEXON / "pn_psh" / f"pn_psh_{m:%Y%m}.parquet")
        bo = pd.read_parquet(ELEXON / "boalf_psh" / f"boalf_psh_{m:%Y%m}.parquet")
        pn, bo = pn[pn["bmUnit"].str.contains(pat)], bo[bo["bmUnit"].str.contains(pat)]
        s = m.start_time.tz_localize("UTC")
        e = (m + 1).start_time.tz_localize("UTC")
        out.append(sp_energy(pn, bo, s, e))
    return pd.concat(out, ignore_index=True)


def bid_share_in_binding(boa_down, bind):
    """boa_down: 30분 하향 MWh(양수, UTC 색인 Series). bind: 같은 색인의 제약 여부(bool, 자료 없는 구간은 NaN).
    반환: (제약 구간의 몫, 기저 제약 비율, 배수). 제약 여부를 모르는 구간은 분모·분자 모두에서 뺀다."""
    b = bind.reindex(boa_down.index)
    ok = b.notna()
    v, bb = boa_down[ok], b[ok].astype(bool)
    share = float(v[bb].sum() / v.sum()) if v.sum() > 0 else float("nan")
    base = float(bind.dropna().astype(bool).mean())
    return share, base, share / base


def cruachan_pn(year=2025):
    """Cruachan 연간 PN 발전·양수와 BOA 하향 (GWh)."""
    sp = psh_sp(pd.period_range(f"{year}-01", f"{year}-12", freq="M"), sites=("CRUA",))
    return {"pn_gen_gwh": float(sp["pn_mwh"].clip(lower=0).sum() / 1e3),
            "pn_pump_gwh": float(-sp["pn_mwh"].clip(upper=0).sum() / 1e3),
            "boa_down_gwh": float(-sp["boa_mwh"].clip(upper=0).sum() / 1e3)}


def v2b(year=2025):
    months = pd.period_range(f"{year}-01", f"{year}-12", freq="M")
    sp = psh_sp(months, sites=("CRUA",))
    down = (-sp["boa_mwh"].clip(upper=0)).groupby(sp["start_utc"]).sum()
    rows = {}
    f6 = _year(da_flows("B6"), year)
    f4 = _year(da_flows("B4"), year)
    b6 = (f6["flow"] >= f6["limit"])
    b4 = (f4["flow"] >= f4["limit"])
    either = pd.concat({"B4": b4, "B6": b6}, axis=1).any(axis=1)
    for name, bind in (("B6", b6), ("B4_or_B6", either)):
        share, base, lift = bid_share_in_binding(down, bind.astype(float))
        rows[name] = {"boa_down_gwh": float(down.sum() / 1e3), "share_in_binding": share, "base_rate": base, "lift": lift}
    return pd.DataFrame(rows).T


# ---------------------------------------------------------------------------------------------------- V3
def daily_spread(p_hourly, k):
    """현지 날짜별 상위 k시간 평균 − 하위 k시간 평균 (£/MWh). p_hourly: UTC 색인 1시간 가격."""
    loc = p_hourly.tz_convert("Europe/London")
    g = loc.groupby(loc.index.date)

    def f(x):
        v = np.sort(x.to_numpy())
        return v[-k:].mean() - v[:k].mean() if len(v) >= 2 * k else np.nan
    return g.apply(f)


def mid_hourly(start, end):
    from gbess.data.prices import load_mid
    s, _rep = load_mid(start, end)
    return s.groupby(s.index.floor("h")).mean()


def unit_cycle_days(sp):
    """유닛·현지 날짜별 순환 여부(PN 양수와 발전 모두 유닛 정격 × 1시간 이상)."""
    from gbess.realized.psh import SITES
    d = sp.assign(site=sp["bmUnit"].str[2:6], date=sp["start_utc"].dt.tz_convert("Europe/London").dt.date)
    n_units = d.groupby("site")["bmUnit"].nunique()
    unit_mw = {s: SITES[s]["mw"] / n_units[s] for s in n_units.index}
    g = d.groupby(["bmUnit", "site", "date"])["pn_mwh"]
    gen = g.apply(lambda x: x.clip(lower=0).sum())
    pump = g.apply(lambda x: -x.clip(upper=0).sum())
    t = pd.DataFrame({"gen": gen, "pump": pump}).reset_index()
    mw = t["site"].map(unit_mw)
    t["cycle"] = ((t["gen"] >= mw) & (t["pump"] >= mw)).astype(int)
    return t


def fit_logit(x, y, iters=50):
    """P(y=1) = σ(a + b x)의 최대우도 (뉴턴법). 반환 (a, b)."""
    X = np.column_stack([np.ones_like(x), x])
    w = np.zeros(2)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(X @ w)))
        H = X.T @ (X * (p * (1 - p))[:, None])
        step = np.linalg.solve(H + 1e-9 * np.eye(2), X.T @ (y - p))
        w += step
        if np.abs(step).max() < 1e-10:
            break
    return w[0], w[1]


def breakeven(x, y):
    a, b = fit_logit(np.asarray(x, float), np.asarray(y, float))
    return -a / b


def breakeven_shift(df_before, df_after, n_boot=1000, seed=0):
    """df: 열 date, spread, cycle. 반환: {before, after, shift(= 전 − 후), ci90}. 날 단위 블록 붓스트랩."""
    rng = np.random.default_rng(seed)
    pt = breakeven(df_before["spread"], df_before["cycle"]) - breakeven(df_after["spread"], df_after["cycle"])

    def boot(df):
        days = df["date"].unique()
        by = {d: i for i, d in enumerate(days)}
        idx = df["date"].map(by).to_numpy()
        order = np.argsort(idx, kind="stable")
        starts = np.searchsorted(idx[order], np.arange(len(days)))
        ends = np.searchsorted(idx[order], np.arange(len(days)), side="right")
        pick = rng.integers(0, len(days), len(days))
        rows = np.concatenate([order[starts[i]:ends[i]] for i in pick])
        return breakeven(df["spread"].to_numpy()[rows], df["cycle"].to_numpy()[rows])
    draws = np.array([boot(df_before) - boot(df_after) for _ in range(n_boot)])
    lo, hi = np.percentile(draws, [5, 95])
    return {"before": breakeven(df_before["spread"], df_before["cycle"]),
            "after": breakeven(df_after["spread"], df_after["cycle"]), "shift": pt, "ci90_lo": lo, "ci90_hi": hi,
            "n_before": len(df_before), "n_after": len(df_after),
            "cycle_rate_before": float(df_before["cycle"].mean()), "cycle_rate_after": float(df_after["cycle"].mean())}


def v3(ks=(4, 8), n_boot=1000):
    from gbess.data.charges import CMP281, CMP308
    rows = []
    for name, t in (("CMP281", CMP281), ("CMP308", CMP308)):
        t = t.tz_convert("Europe/London")
        s, e = t - pd.DateOffset(months=12), t + pd.DateOffset(months=12)
        months = pd.period_range(s.strftime("%Y-%m"), (e - pd.Timedelta(days=1)).strftime("%Y-%m"), freq="M")
        cyc = unit_cycle_days(psh_sp(months))
        price = mid_hourly(s.tz_convert("UTC"), e.tz_convert("UTC"))
        for k in ks:
            sp = daily_spread(price, k).rename("spread")
            d = cyc.merge(sp, left_on="date", right_index=True).dropna(subset=["spread"])
            before = d[pd.to_datetime(d["date"]) < t.tz_localize(None).normalize()]
            after = d[pd.to_datetime(d["date"]) >= t.tz_localize(None).normalize()]
            r = breakeven_shift(before, after, n_boot=n_boot)
            rows.append({"change": name, "k_hours": k, **r})
    return pd.DataFrame(rows)


def v3_verdict(shift, lo, hi, predicted):
    """spec V3: 판정 불가(90% 구간이 0 포함) / 통과(부호가 맞고 비율 0.5~2이거나 예측이 90% 구간 안) / 실패."""
    if lo <= 0 <= hi:
        return "inconclusive"
    ok_sign = np.sign(shift) == np.sign(predicted)
    ratio = shift / predicted
    if ok_sign and (0.5 <= ratio <= 2.0 or lo <= predicted <= hi):
        return "pass"
    return "fail"


# ---------------------------------------------------------------------------------------------------- V4
def price_metrics(p_hourly, k=8):
    """V4 지표: 하루 상위 k − 하위 k 시간 평균의 중앙값·P90, 가격 ≤ 0 시간 비율."""
    sp = daily_spread(p_hourly, k).dropna()
    return {"spread_median": float(sp.median()), "spread_p90": float(sp.quantile(0.9)),
            "nonpositive_share": float((p_hourly <= 0).mean()), "days": len(sp)}


def v4_observed(year=2025):
    s = pd.Timestamp(f"{year}-01-01", tz="UTC")
    return price_metrics(mid_hourly(s, s + pd.DateOffset(years=1)))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    row, monthly = v1_observed(2025)
    pd.Series(row).to_csv(OUT / "observed_v1_2025.csv", header=["value"])
    monthly.to_csv(OUT / "observed_v1_monthly_2025.csv")
    print("V1 관측 2025:", {k: round(v, 4) for k, v in row.items()})
    b = v2b(2025)
    b.to_csv(OUT / "observed_v2b_2025.csv")
    print(b)
    p = v4_observed(2025)
    pd.Series(p).to_csv(OUT / "observed_v4_2025.csv", header=["value"])
    print("V4 관측 2025:", p)
    r = v3()
    pred = {"CMP281": 9.2, "CMP308": 9.3}
    r["predicted"] = r["change"].map(pred)
    r["verdict"] = [v3_verdict(a, lo, hi, pr) for a, lo, hi, pr in zip(r["shift"], r["ci90_lo"], r["ci90_hi"], r["predicted"])]
    r.to_csv(OUT / "observed_v3.csv", index=False)
    print(r.round(3).to_string())


if __name__ == "__main__":
    main()
