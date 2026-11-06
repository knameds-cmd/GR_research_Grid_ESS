"""
M3a: 2030년 모형을 기상연도 2010~2024 15개 해로 돌린다 (spec scenarios_m3.m3a, 연구자 승인 2026-11-06).
설계안·지표·규칙은 M1 그대로. 2013·2020은 M1 결과를 그대로 쓴다.

    .venv/bin/python -m gbess.system.m3a inputs          # 새 해의 입력 파일 (data/processed/system)
    .venv/bin/python -m gbess.system.m3a jobs [해 ...]   # 실행 명령 목록 (8개 동시에 돌림)
    .venv/bin/python -m gbess.system.m3a summary         # results/system/m3a/summary_by_year.csv, summary.json, fig_d_by_year.png

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
    검산이 깨진 판(해 × 한도 배율)은 그 배율의 분포·해 수에서 빼고 not_comparable_x{배율}에 따로 적는다.
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
    for col in [c for c in df.columns if c.startswith(("D_", "C_S0_minus"))]:
        m = float(col.rsplit("_x", 1)[1]) if "_x" in col else 1.0
        s = df.loc[~broken(m), col].dropna()
        out[col] = {"median": float(s.median()), "min": float(s.min()), "max": float(s.max()), "n": int(len(s))}
    for m in (0.8, 1.0, 1.2):
        s = df.get(f"D_lo_x{m}")
        if s is not None:
            s = s[~broken(m)]
            out[f"years_D_lo_x{m}_ge_M"] = int((s >= M).sum())
            out[f"years_D_lo_x{m}_ge_3M"] = int((s >= go_multiple * M).sum())
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
    """spec m3a.report "해와 D의 관계는 그림만": (왼쪽) 해마다 D_lo ×1.0과 M·3M 선, (오른쪽) 풍력 이용률과 D_lo ×1.0."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from gbess.system.run_m1 import BLUE, INK, MUTED, ORANGE, _style
    plt.rcParams["font.family"] = ["AppleGothic", "DejaVu Sans"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1.6, 1]})
    ys = df.index.astype(int)
    a.bar(ys, df["D_lo_x1.0"], color=[ORANGE if y == REF_YEAR else BLUE for y in ys], width=0.7)
    for v, t in ((M, "M £25m"), (go_multiple * M, "3M £75m")):
        a.hlines(v, ys.min() - 0.6, ys.max() + 0.4, color=MUTED, lw=0.8, ls="--")
        a.text(ys.max() + 0.5, v, t, color=MUTED, fontsize=8, va="center", ha="left")
    a.set_xticks(ys, [str(y)[2:] for y in ys])
    a.set_xlim(ys.min() - 0.6, ys.max() + 2.2)
    a.set_title("D_W1 (D_lo, 한도 ×1.0), £m/년. 주황 = 2013 (M1 주 결과)", fontsize=9, color=INK, loc="left")
    b.scatter(df["wind_cf"], df["D_lo_x1.0"], s=40, color=BLUE, edgecolor="white", lw=1.5)
    for y, r in df.iterrows():
        b.annotate(str(int(y))[2:], (r["wind_cf"], r["D_lo_x1.0"]), xytext=(4, 2), textcoords="offset points", fontsize=7, color=MUTED)
    b.set_xlabel("풍력 이용률 (2030 설비 가중)", fontsize=8, color=MUTED)
    b.set_title("풍력 이용률과 D_lo ×1.0 (회귀 없음)", fontsize=9, color=INK, loc="left")
    for ax in (a, b):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


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
    elif argv[:1] == ["summary"]:
        rows = {}
        for y in ys:
            df, seq = collect_year(y)
            rows[y] = {**year_row(df, seq), "wind_cf": wind_cf(y)}
        df, out = summarize(rows)
        OUT.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT / "summary_by_year.csv", index_label="weather_year")
        figure_years(df, OUT / "fig_d_by_year.png")
        (OUT / "summary.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
        print(json.dumps(out, indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main(sys.argv[1:])
