"""
M3a: 2030년 모형을 기상연도 2010~2024 15개 해로 돌린다 (spec scenarios_m3.m3a, 연구자 승인 2026-11-06).
설계안·지표·규칙은 M1 그대로. 2013·2020은 M1 결과를 그대로 쓴다.

    .venv/bin/python -m gbess.system.m3a inputs          # 새 해의 입력 파일 (data/processed/system)
    .venv/bin/python -m gbess.system.m3a jobs [해 ...]   # 실행 명령 목록 (8개 동시에 돌림)
    .venv/bin/python -m gbess.system.m3a summary         # results/system/m3a/summary_by_year.csv, summary.json, fig_d_by_year.png
    .venv/bin/python -m gbess.system.m3a hours 2018      # 보고 뒤 점검: S0 (iii) D_lo 판의 시간별 값과 정전 시간 (약 20~30분)
    .venv/bin/python -m gbess.system.m3a shed_runs       # '충전 정전' 판 대상 (×1.0 (iii) D_lo 판 중 정전이 있는 것)
    .venv/bin/python -m gbess.system.m3a shed_variant 2018 S0   # '충전 정전' 판 하나 → results/system/m3a/shed_variant.csv

- 판 이름은 M1과 같은 규칙: 2013은 x{배율}_{설계안}, 다른 해는 w{해}_x{배율}_{설계안} (results/system/m1/).
- 순차 재급전은 run_sequential_w1n_increment(한도 ×1.0) → results_sequential_w1n_increment_{해}.csv.
- 순위 기준(spec에 없던 세부, 결과 전에 정함): 해마다 S0·S1a·S1b의 계통 총비용과 소비자 지급을 재급전 (iii) D_lo 판에서
  비교한다. 차이가 £0.1m 미만이면 같은 순위. "유지"는 2013년(M1 주 결과, Ofgem 기준 기상연도)의 순위와 같은 해.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
M1 = ROOT / "results" / "system" / "m1"
OUT = ROOT / "results" / "system" / "m3a"
DONE = (2013, 2020)
DESIGNS = ("S0", "S1a", "S1b")
REF_YEAR = 2013
TIE_GBP_M = 0.1


def years(spec=None):
    from gbess.system.run_m1 import load_spec
    return list((spec or load_spec())["scenarios_m3"]["m3a"]["weather_years"])


def label(year, mult, design):
    return f"x{mult}_{design}" if year == 2013 else f"w{year}_x{mult}_{design}"


def jobs(new_years):
    py = ".venv/bin/python"
    cmds = []
    for y in new_years:
        for m in (0.8, 1.0, 1.2):
            cmds.append(f"{py} -m gbess.system.run_m1 --weather-year {y} --mult {m} --designs S0 --label {label(y, m, 'S0')}")
        for d in ("S1a", "S1b"):
            cmds.append(f"{py} -m gbess.system.run_m1 --weather-year {y} --mult 1.0 --designs {d} --label {label(y, 1.0, d)}")
        cmds.append(f"{py} -c \"from gbess.system.run_m1 import run_sequential_w1n_increment as f; f((1.0,), {y})\"")
    return cmds


def wind_cf(year, zones=("N", "S", "EW")):
    """그해 2030 모형의 풍력 이용률(육상+해상, 2030 설비 가중). 입력 파일에서 계산."""
    from gbess.system.inputs import build_fleet, load_processed
    mw = build_fleet()["renewable_mw"]
    _, cf = load_processed(zones, year)
    num = sum(mw[k][z] * cf[k][i].mean() for k in ("onshore_wind", "offshore_wind") for i, z in enumerate(zones))
    den = sum(mw[k][z] for k in ("onshore_wind", "offshore_wind") for z in zones)
    return num / den


def constraint_share(flows, limits, boundary):
    """경계 boundary의 암묵적 조류가 한도 이상인 시간의 비율 (run_m1.e_bind와 같은 '제약 시간' 정의). limits: (B,) 또는 (B, T)."""
    flows = np.atleast_2d(np.asarray(flows, float))
    lim = np.asarray(limits, float).reshape(len(flows), -1)[boundary]
    return float((flows[boundary] >= lim - 1e-9).mean())


def b6_share(year, mult=1.0):
    """그해 S0 1단계 첫 풀이(전국 시장)에서 B6 암묵적 조류가 한도 이상인 시간의 비율. 초안 3.3 "B6 제약 시간 비율"."""
    from gbess.system.inputs import build_network_2030
    from gbess.system.stage1 import solve_stage1
    net, meta = build_network_2030(weather_year=year)
    n = net.scaled_limits(mult)
    return constraint_share(solve_stage1(n).flows, n.limits, meta["bind_boundaries"][1])


def year_row(df, seq=None):
    """한 해의 판 모음(run_m1.collect 결과)에서 보고 값(£m/년, TWh). seq: 순차 재급전 증분 표(한도 ×1.0 행 사용)."""
    from gbess.system.run_m1 import check_invariants, go_no_go_values
    g = go_no_go_values(df)["values"]
    c = {(r.design, r.variant, r.plan, r.limit_mult): r for r in df.itertuples()}
    row = {}
    for m, v in g.items():
        row[f"D_lo_x{m}"] = v["D_lo_gbp_m"]
        if m == 1.0:
            row["D_hi_x1.0"] = v["D_hi_approx_gbp_m"]
            row["E_bind_twh"] = v["E_bind_twh"]
            for d, x in v["C_S0_minus_C_S1x_gbp_m"].items():
                row[f"C_S0_minus_C_{d}"] = x
    for d in DESIGNS:
        r = c.get((d, "iii", "D_lo", 1.0))
        if r is not None:
            row[f"system_cost_{d}"] = r.system_cost / 1e6
            row[f"consumer_payment_{d}"] = r.consumer_payment / 1e6
            row[f"curtailment_twh_{d}"] = r.curtailment_mwh / 1e6
    if seq is not None:
        s = seq[seq["limit_mult"] == 1.0].set_index("fleet")
        row["D_seq_x1.0"] = s.loc["with_W1N", "D_seq"]
        row["D_seq_W1N_share_x1.0"] = s.loc["with_W1N", "D_seq"] - s.loc["without_W1N", "D_seq"]
    bad = check_invariants(df)
    row["invariant_violations"] = len(bad)
    for m in g:
        row[f"invariant_violations_x{m}"] = sum(b[0] == m for b in bad)
    return row


def ranking(row, metric):
    """설계안을 metric(낮을수록 좋음)으로 줄 세운 순위 튜플. £0.1m 미만 차이는 같은 순위. 값이 없으면 None."""
    vals = {d: row.get(f"{metric}_{d}") for d in DESIGNS}
    if any(v is None or (isinstance(v, float) and np.isnan(v)) for v in vals.values()):
        return None
    order = sorted(DESIGNS, key=lambda d: vals[d])
    rank, out = 0, {}
    for i, d in enumerate(order):
        if i and vals[d] - vals[order[i - 1]] >= TIE_GBP_M:
            rank = i
        out[d] = rank
    return tuple(out[d] for d in DESIGNS)


def summarize(rows, M=25.0, go_multiple=3):
    """rows: {해: year_row}. 분포, D_lo ≥ M·3M 해 수, 순위 유지 비율(2013 기준).
    검산이 깨진 판(해 × 한도 배율)은 not_comparable_x{배율}에 따로 적고, 그 배율의 분포·해 수는 뺀 값(기본 키)과
    넣은 값(*_all) 둘 다 낸다.
    순위와 C(S0) − C(S1x)는 ×1.0 판이라 ×1.0이 깨진 해만 뺀다."""
    df = pd.DataFrame.from_dict(rows, orient="index").sort_index()
    out = {"n_years": len(df), "invariant_broken_years": [int(y) for y in df.index[df["invariant_violations"] > 0]]}

    def broken(m):
        # spec m3a.rules: 검산이 깨진 판은 '비교 불가'로 따로 셈. 배율별 기록이 없으면 그해 전체 위반 수로 판단
        col = f"invariant_violations_x{m}"
        return df[col].fillna(0) > 0 if col in df else df["invariant_violations"] > 0

    for m in (0.8, 1.0, 1.2):
        if f"D_lo_x{m}" in df:
            out[f"not_comparable_x{m}"] = [int(y) for y in df.index[broken(m)]]
    def stats(s):
        s = s.dropna()
        return {"median": float(s.median()), "min": float(s.min()), "max": float(s.max()), "n": int(len(s))}

    # 초안 3.3은 "비교 불가로 표시하고 분포 계산에서 빼지 않고 따로 센다", spec rules는 "'비교 불가'로 따로 셈".
    # 두 읽기가 갈리므로 둘 다 낸다: 기본 키 = 비교 불가 판을 뺀 값, *_all = 넣은 값 (비교 불가 판이 있는 배율만)
    for col in [c for c in df.columns if c.startswith(("D_", "C_S0_minus"))]:
        m = float(col.rsplit("_x", 1)[1]) if "_x" in col else 1.0
        out[col] = stats(df.loc[~broken(m), col])
        if broken(m).any():
            out[f"{col}_all"] = stats(df[col])
    for m in (0.8, 1.0, 1.2):
        s = df.get(f"D_lo_x{m}")
        if s is not None:
            for sfx, x in (("", s[~broken(m)]), ("_all", s)):
                if sfx and not broken(m).any():
                    continue
                out[f"years_D_lo_x{m}_ge_M{sfx}"] = int((x >= M).sum())
                out[f"years_D_lo_x{m}_ge_3M{sfx}"] = int((x >= go_multiple * M).sum())
    ok_years = set(df.index[~broken(1.0)])
    for metric in ("system_cost", "consumer_payment"):
        ranks = {y: ranking(r, metric) for y, r in rows.items()}
        ref = ranks.get(REF_YEAR)
        ok = [y for y, r in ranks.items() if r is not None and y in ok_years]
        out[f"rank_{metric}"] = {"reference_2013": ref,
                                 "same_as_2013": sum(ranks[y] == ref for y in ok), "n": len(ok),
                                 "flipped_years": sorted(int(y) for y in ok if ranks[y] != ref)}
    return df, out


def figure_years(df, path, M=25.0, go_multiple=3):
    """spec m3a.report "해와 D의 관계는 그림만": 해마다 D_lo ×1.0과 M·3M 선, 풍력 이용률·B6 제약 시간 비율과 D_lo ×1.0."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from gbess.system.run_m1 import BLUE, INK, MUTED, ORANGE, _style
    plt.rcParams["font.family"] = ["AppleGothic", "DejaVu Sans"]
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(14, 3.8), gridspec_kw={"width_ratios": [1.6, 1, 1]})
    ys = df.index.astype(int)
    a.bar(ys, df["D_lo_x1.0"], color=[ORANGE if y == REF_YEAR else BLUE for y in ys], width=0.7)
    for v, t in ((M, "M £25m"), (go_multiple * M, "3M £75m")):
        a.hlines(v, ys.min() - 0.6, ys.max() + 0.4, color=MUTED, lw=0.8, ls="--")
        a.text(ys.max() + 0.5, v, t, color=MUTED, fontsize=8, va="center", ha="left")
    a.set_xticks(ys, [str(y)[2:] for y in ys])
    a.set_xlim(ys.min() - 0.6, ys.max() + 2.2)
    a.set_title("D_W1 (D_lo, 한도 ×1.0), £m/년. 주황 = 2013 (M1 주 결과)", fontsize=9, color=INK, loc="left")
    for ax, x, xl, t in ((b, "wind_cf", "풍력 이용률 (2030 설비 가중)", "풍력 이용률과 D_lo ×1.0 (회귀 없음)"),
                         (c, "b6_constraint_share", "B6 제약 시간 비율 (S0 1단계)", "B6 제약 시간과 D_lo ×1.0 (회귀 없음)")):
        if x not in df:
            ax.set_visible(False)
            continue
        ax.scatter(df[x], df["D_lo_x1.0"], s=40, color=BLUE, edgecolor="white", lw=1.5)
        for y, r in df.iterrows():
            ax.annotate(str(int(y))[2:], (r[x], r["D_lo_x1.0"]), xytext=(4, 2), textcoords="offset points", fontsize=7, color=MUTED)
        ax.set_xlabel(xl, fontsize=8, color=MUTED)
        ax.set_title(t, fontsize=9, color=INK, loc="left")
    for ax in (a, b, c):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def shed_events(shed_mw, dt=1.0, tol=1e-6):
    """(Z, T) 정전 MW → 이어진 시간 묶음 [(시작 시간, 끝 시간(포함), 구역별 MWh 튜플)]. 0보다 큰(tol 초과) 시간만."""
    shed = np.atleast_2d(np.asarray(shed_mw, float))
    on = shed.sum(0) > tol
    out, t, T = [], 0, len(on)
    while t < T:
        if on[t]:
            u = t
            while u + 1 < T and on[u + 1]:
                u += 1
            out.append((t, u, tuple(float(x) for x in shed[:, t:u + 1].sum(1) * dt)))
            t = u + 1
        else:
            t += 1
    return out


def hours(year, mult=1.0, out_dir=None, log=print):
    """보고 뒤 점검(M3a 결과 메모 7장): S0 재급전 (iii) D_lo 판을 다시 풀어 시간별 값을 저장한다. 판정에 쓰지 않음.
    hours_{해}_x{배율}.csv: 구역별 수요·풍력 가용·정전, 경계 조류(1단계 암묵적·최종)·한도, W1 북쪽 순방전, S6 정전.
    재급전 비용이 결과 판(results.csv)과 같은지 run.json 대신 로그로 확인한다."""
    import time
    from gbess.system.inputs import build_network_2030
    from gbess.system.planner import solve_planner
    from gbess.system.redispatch import redispatch_lo
    from gbess.system.stage1 import solve_stage1
    t0 = time.perf_counter()
    net, meta = build_network_2030(weather_year=year)
    n = net.scaled_limits(mult)
    s6 = solve_planner(n)
    s0 = solve_stage1(n)
    lo = redispatch_lo(n, "intertemporal", meta["w1_north"], c1=s0.cost, infeasible="min_deviation")
    plan = lo.extra["plan"]
    log(f"{year} ×{mult}: D_lo £{(lo.cost - s6.cost) / 1e6:.1f}m, 정전 {lo.shed.sum() * n.dt / 1e3:.2f} GWh "
        f"({time.perf_counter() - t0:.0f}s)")
    T = n.demand.shape[1]
    df = pd.DataFrame({"time": pd.date_range(f"{year}-01-01", periods=T, freq="h")})
    lim = np.broadcast_to(np.asarray(n.limits, float).reshape(len(n.zones) - 1, -1), (len(n.zones) - 1, T))
    idx = [n.store_names().index(u) for u in meta["w1_north"]]
    for z, name in enumerate(n.zones):
        df[f"demand_{name}"] = n.demand[z]
        df[f"wind_avail_{name}"] = sum(np.asarray(g.avail if g.avail is not None else 1.0) * g.cap
                                       for g in n.gens if g.renewable and g.zone == z and "wind" in g.name)
        df[f"shed_{name}"] = lo.shed[z]
        df[f"shed_S6_{name}"] = s6.shed[z]
    for b in range(len(n.zones) - 1):
        nm = f"{n.zones[b]}_{n.zones[b + 1]}"
        df[f"flow_plan_{nm}"] = plan.flows[b]
        df[f"flow_final_{nm}"] = lo.flows[b]
        df[f"limit_{nm}"] = lim[b]
    df["w1n_net_discharge_plan"] = (plan.d[idx] - plan.ch[idx]).sum(0)
    df["w1n_net_discharge_final"] = (lo.d[idx] - lo.ch[idx]).sum(0)
    df["w1n_energy_plan"] = plan.e[idx].sum(0)
    out = Path(out_dir or OUT) / f"hours_{year}_x{mult}.csv"
    df.to_csv(out, index=False)
    return df, shed_events(lo.shed, n.dt), (lo.cost - s6.cost) / 1e6


def shed_runs(rows_by_year=None, mult=1.0):
    """'충전 정전' 판의 대상(spec changelog 2026-11-06 (3)): 한도 ×1.0 S0·S1a·S1b (iii) D_lo 판 중 정전이 있는 (해, 설계안)."""
    out = []
    for y in years():
        df, _ = collect_year(y)
        for d in DESIGNS:
            r = df[(df.design == d) & (df.variant == "iii") & (df.plan == "D_lo") & (df.limit_mult == mult)]
            if len(r) and r.shed_mwh.iloc[0] > 1e-3:
                out.append((y, d))
    return out


def shed_variant(year, design, mult=1.0, X=0.5, beta=1.0, log=print):
    """'충전 정전' 판 하나: 재급전 (iii) D_lo를 infeasible="min_shed"로 다시 푼다(보고만). 값은 £m."""
    import time
    from gbess.system.designs import s1a_caps, s1b_caps
    from gbess.system.inputs import build_network_2030
    from gbess.system.planner import solve_planner
    from gbess.system.redispatch import redispatch_lo
    from gbess.system.stage1 import solve_stage1
    t0 = time.perf_counter()
    net, meta = build_network_2030(weather_year=year)
    n = net.scaled_limits(mult)
    north = meta["w1_north"]
    c6 = solve_planner(n).cost
    s0 = solve_stage1(n)
    caps = {"S0": None, "S1a": s1a_caps(n, north, X), "S1b": s1b_caps(n, s0, north, beta)}[design]
    c1 = s0.cost if caps is None else solve_stage1(n, caps=caps).cost
    lo = redispatch_lo(n, "intertemporal", north, c1=c1, caps=caps, infeasible="min_shed")
    row = {"weather_year": year, "design": design, "limit_mult": mult, "system_cost": lo.cost / 1e6, "C_S6": c6 / 1e6,
           "D": (lo.cost - c6) / 1e6, "shed_mwh": float(lo.shed.sum() * n.dt),
           "fixed_deviation_mwh": lo.extra["fixed_deviation_mwh"], "seconds": time.perf_counter() - t0}
    log(f"{year} {design} ×{mult}: 충전 정전 판 D £{row['D']:.1f}m, 정전 {row['shed_mwh']:.0f} MWh, "
        f"이탈 {row['fixed_deviation_mwh']:.0f} MWh ({row['seconds']:.0f}s)")
    return row


def collect_year(year):
    from gbess.system.run_m1 import collect
    df = collect(M1, "x*_S*" if year == 2013 else f"w{year}_x*_S*")
    p = M1 / f"results_sequential_w1n_increment_{year}.csv"
    return df, (pd.read_csv(p) if p.exists() else None)


def main(argv):
    ys = years()
    new = [y for y in ys if y not in DONE]
    if argv[:1] == ["inputs"]:
        from gbess.system.inputs import write_processed
        for y in (argv[1:] and [int(a) for a in argv[1:]]) or new:
            _, _, diag = write_processed(year=y)
            print(y, "입력 만듦", {k: diag[k] for k in diag if k in ("solar_performance_ratio", "scot_onshore_cf_scale")}, flush=True)
    elif argv[:1] == ["jobs"]:
        print("\n".join(jobs((argv[1:] and [int(a) for a in argv[1:]]) or new)))
    elif argv[:1] == ["hours"]:
        y = int(argv[1])
        mult = float(argv[2]) if len(argv) > 2 else 1.0
        df, ev, d = hours(y, mult)
        for a, b, mwh in ev:
            print(df["time"][a], "~", df["time"][b], f"{b - a + 1}시간", {z: round(x) for z, x in zip(("N", "S", "EW"), mwh)},
                  flush=True)
    elif argv[:1] == ["shed_runs"]:
        print("\n".join(f"{y} {d}" for y, d in shed_runs()))
    elif argv[:1] == ["shed_variant"]:
        y, d = int(argv[1]), argv[2]
        row = shed_variant(y, d)
        p = OUT / "shed_variant.csv"
        old = pd.read_csv(p) if p.exists() else pd.DataFrame()
        if len(old):
            old = old[~((old.weather_year == y) & (old.design == d) & (old.limit_mult == row["limit_mult"]))]
        pd.concat([old, pd.DataFrame([row])]).sort_values(["weather_year", "design"]).to_csv(p, index=False)
    elif argv[:1] == ["summary"]:
        rows = {}
        for y in ys:
            df, seq = collect_year(y)
            rows[y] = {**year_row(df, seq), "wind_cf": wind_cf(y), "b6_constraint_share": b6_share(y)}
        df, out = summarize(rows)
        OUT.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT / "summary_by_year.csv", index_label="weather_year")
        figure_years(df, OUT / "fig_d_by_year.png")
        (OUT / "summary.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
        print(json.dumps(out, indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main(sys.argv[1:])
