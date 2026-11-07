"""
M3c + S3 (spec scenarios_m3.m3c_s3, 연구자 승인 2026-11-07). M3a의 15개 기상연도, 한도 ×1.0.

    .venv/bin/python -m gbess.system.s3 run 2018          # S3-제약시간 판 하나 → results/system/m3c_s3/w2018_x1.0_S3/
    .venv/bin/python -m gbess.system.s3 jobs              # 15개 해 실행 명령 목록 (8개 동시에 돌림)
    .venv/bin/python -m gbess.system.s3 summary           # summary_by_year.csv, summary.json, m3c_revenue_floor.csv

S3-제약시간: 1단계(전국 시장) S0 첫 풀이에서 B4나 B6의 암묵적 조류가 어느 방향이든 한도에 닿는 시간(|f| ≥ F)에만 NESO가
W1 북쪽에 지시할 수 있다. 다른 시간에는 W1 북쪽은 시장 계획대로(재급전 변형 (iii)의 묶음). 1단계 계획은 S0과 같다(S3는
시장 단계를 바꾸지 않음). 재급전 비용은 (iii)처럼 첫 풀이 판과 D_lo(결합 LP) 판을 낸다. 지시 이탈은 비용 기준으로 정산
(payments_national 그대로). 정전 처리는 M3a와 같은 min_deviation, 정전이 남으면 min_shed 판을 함께 낸다.
M3c 주 가정 (a): floor 아래 운전 = 시장 이익 최대 운전 = M1·M3a 그대로이므로 새 계산 없이 수익 ÷ floor 분포만 낸다.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.system.m3a import DESIGNS as M3A_DESIGNS, REF_YEAR, TIE_GBP_M, collect_year, years

ROOT = Path(__file__).resolve().parents[2]
M1 = ROOT / "results" / "system" / "m1"
OUT = ROOT / "results" / "system" / "m3c_s3"
DESIGNS = M3A_DESIGNS + ("S3",)


def bind_hours(flows, limits, boundaries):
    """(B, T) 조류, (B,) 또는 (B, T) 한도 → (T,) bool. boundaries 중 하나라도 |f| ≥ F(방향 무관)인 시간."""
    flows = np.atleast_2d(np.asarray(flows, float))
    lim = np.broadcast_to(np.asarray(limits, float).reshape(len(flows), -1), flows.shape)
    b = list(boundaries)
    return (np.abs(flows[b]) >= lim[b] - 1e-9).any(axis=0)


def instructed_mwh(plan, final, idx, dt=1.0):
    """W1 북쪽(idx)의 지시량: Σ |Δch| + |Δd| (MWh). 계획 대비 최종 운전의 차이."""
    return float((np.abs(final.ch[idx] - plan.ch[idx]) + np.abs(final.d[idx] - plan.d[idx])).sum() * dt)


def run(year, mult=1.0, out_dir=None, log=print):
    """S3-제약시간 판 하나. 결과표 행은 run_m1과 같은 열(+ instructed_mwh, free_hours)."""
    from gbess.system.inputs import build_network_2030
    from gbess.system.planner import solve_planner
    from gbess.system.redispatch import redispatch, redispatch_lo
    from gbess.system.run_m1 import SPEC, _row, file_sha256, git_commit, payments_national
    from gbess.system.stage1 import solve_stage1
    t0 = time.perf_counter()
    net, meta = build_network_2030(weather_year=year)
    n = net.scaled_limits(mult)
    north, w1_all, levels = meta["w1_north"], meta["w1_all"], meta["levels"]
    idx = [n.store_names().index(u) for u in north]
    s6 = solve_planner(n)
    c6 = s6.cost
    s0 = solve_stage1(n)
    free = bind_hours(s0.flows, n.limits, meta["bind_boundaries"])
    rows = [_row("S6", "-", mult, s6, c6, n)]
    log(f"{year} ×{mult}: 제약 시간 {int(free.sum())}시간 ({time.perf_counter() - t0:.0f}s)")
    fs = redispatch(s0, n, "intertemporal", north, infeasible="min_deviation", free_hours=free)
    pay = payments_national(n, s0.prices, s0, fs, w1_all, levels)
    rows.append(_row("S3", "iii", mult, fs, c6, n, {**pay, "plan": "first_solve",
                                                     "instructed_mwh": instructed_mwh(s0, fs, idx, n.dt),
                                                     "free_hours": int(free.sum())}))
    runs = [("min_deviation", "D_lo")]
    for infeasible, plan_label in runs:
        lo = redispatch_lo(n, "intertemporal", north, c1=s0.cost, infeasible=infeasible, free_hours=free)
        plan = lo.extra["plan"]
        pay = payments_national(n, s0.prices, plan, lo, w1_all, levels)
        rows.append(_row("S3", "iii", mult, lo, c6, n, {**pay, "plan": plan_label,
                                                         "instructed_mwh": instructed_mwh(plan, lo, idx, n.dt),
                                                         "free_hours": int(free.sum())}))
        log(f"{year} ×{mult}: S3 {plan_label} D £{(lo.cost - c6) / 1e6:.1f}m, 정전 {pay['shed_mwh']:.0f} MWh "
            f"({time.perf_counter() - t0:.0f}s)")
        if plan_label == "D_lo" and pay["shed_mwh"] > 1e-3:
            runs.append(("min_shed", "D_lo_min_shed"))      # 4b.4: 정전이 남으면 '충전 정전' 판도 함께
    out = Path(out_dir) if out_dir else s3_dir(year, mult)
    out.mkdir(parents=True, exist_ok=True)
    record = {"git_commit": git_commit(), "spec_sha256": file_sha256(SPEC),
              "input_sha256": {str(p): file_sha256(p) for p in meta["inputs"]},
              "solver_status": sorted({r["status"] for r in rows}), "solve_seconds": time.perf_counter() - t0,
              "weather_year": year, "options": {"limit_mult": mult, "w1_north": list(north),
                                                "bind_boundaries": list(meta["bind_boundaries"]),
                                                "free_hours": int(free.sum())}}
    (out / "run.json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame([{k: v for k, v in r.items() if k != "operator_revenue"} for r in rows]).to_csv(out / "results.csv",
                                                                                              index=False)
    rev = [{"design": r["design"], "variant": r["variant"], "limit_mult": r["limit_mult"], "plan": r.get("plan"),
            "project": u, "revenue": x, "floor": levels.get(u, (np.nan,))[0]}
           for r in rows for u, x in (r.get("operator_revenue") or {}).items()]
    pd.DataFrame(rev).to_csv(out / "operator_revenue.csv", index=False)
    return rows


def jobs(ys=None):
    return [f".venv/bin/python -m gbess.system.s3 run {y}" for y in (ys or years())]


# ---------------------------------------------------------------------------------------------------------------
def year_row(m3a_df, s3_df, mult=1.0, rel=1e-6):
    """한 해의 보고 값(£m). m3a_df: run_m1.collect 결과, s3_df: S3 판 results.csv. 차이는 'X − S3' (양수면 S3가 쌈)."""
    c = {(r.design, r.variant, r.plan): r for r in m3a_df[m3a_df.limit_mult == mult].itertuples()}
    s = {r.plan: r for r in s3_df.itertuples() if r.design == "S3"}
    c6 = c[("S6", "-", "-")].system_cost
    lo = s["D_lo"]
    row = {"D_S3": (lo.system_cost - c6) / 1e6, "D_S3_first_solve": (s["first_solve"].system_cost - c6) / 1e6,
           "instructed_gwh_S3": lo.instructed_mwh / 1e3, "shed_mwh_S3": lo.shed_mwh,
           "fixed_deviation_mwh_S3": lo.fixed_deviation_mwh, "free_hours_S3": int(lo.free_hours),
           "system_cost_S3": lo.system_cost / 1e6, "consumer_payment_S3": lo.consumer_payment / 1e6,
           "floor_topup_S3": lo.floor_topup / 1e6}
    if "D_lo_min_shed" in s:
        row["D_S3_min_shed"] = (s["D_lo_min_shed"].system_cost - c6) / 1e6
        row["shed_mwh_S3_min_shed"] = s["D_lo_min_shed"].shed_mwh
    for d in M3A_DESIGNS:
        r = c.get((d, "iii", "D_lo"))
        if r is None:
            continue
        row[f"system_cost_{d}"] = r.system_cost / 1e6
        row[f"consumer_payment_{d}"] = r.consumer_payment / 1e6
        row[f"floor_topup_{d}"] = r.floor_topup / 1e6
        row[f"C_{d}_minus_C_S3"] = (r.system_cost - lo.system_cost) / 1e6
        row[f"P_{d}_minus_P_S3"] = (r.consumer_payment - lo.consumer_payment) / 1e6
    row["floor_topup_S3_minus_S0"] = row["floor_topup_S3"] - row.get("floor_topup_S0", np.nan)
    # 검산: C(S6) ≤ C(S3) (둘 다), 첫 풀이 C(S3) ≤ C(S0, iii) (같은 계획, 묶음이 더 적음)
    tol = rel * abs(c6)
    bad = []
    for k in ("first_solve", "D_lo"):
        if s[k].system_cost < c6 - tol:
            bad.append(f"C_S6 <= C_S3 ({k})")
    s0fs = c.get(("S0", "iii", "first_solve"))
    if s0fs is not None and s["first_solve"].system_cost > s0fs.system_cost + tol:
        bad.append("C_S3 <= C_S0_iii (first_solve)")
    row["invariant_violations_S3"] = len(bad)
    row["invariant_notes_S3"] = "; ".join(bad)
    return row


def ranking(row, metric, designs=DESIGNS, tie=TIE_GBP_M):
    """m3a.ranking과 같은 규칙(£0.1m 미만은 같은 순위)을 S3까지 넣은 설계안에 적용."""
    vals = {d: row.get(f"{metric}_{d}") for d in designs}
    if any(v is None or (isinstance(v, float) and np.isnan(v)) for v in vals.values()):
        return None
    order = sorted(designs, key=lambda d: vals[d])
    rank, out = 0, {}
    for i, d in enumerate(order):
        if i and vals[d] - vals[order[i - 1]] >= tie:
            rank = i
        out[d] = rank
    return tuple(out[d] for d in designs)


def summarize(rows, broken_m3a=()):
    """rows: {해: year_row}. broken_m3a: M3a에서 ×1.0 검산이 깨진 해(순위·분포에서 뺌, M3a와 같은 규칙)."""
    df = pd.DataFrame.from_dict(rows, orient="index").sort_index()
    ok = ~df.index.isin(list(broken_m3a)) & (df["invariant_violations_S3"] == 0)
    out = {"n_years": len(df), "not_comparable": [int(y) for y in df.index[~ok]]}

    def stats(s):
        s = s.dropna()
        return {"median": float(s.median()), "min": float(s.min()), "max": float(s.max()), "n": int(len(s))}

    for col in [c for c in df.columns if c.startswith(("D_S3", "C_", "P_", "instructed", "shed_mwh", "floor_topup_S3_"))]:
        out[col] = stats(df.loc[ok, col])
    for metric in ("system_cost", "consumer_payment"):
        ranks = {y: ranking(r, metric) for y, r in rows.items()}
        ref = ranks.get(REF_YEAR)
        ys = [y for y in df.index[ok] if ranks[y] is not None]
        out[f"rank_{metric}"] = {"designs": list(DESIGNS), "reference_2013": ref,
                                 "same_as_2013": sum(ranks[y] == ref for y in ys), "n": len(ys),
                                 "flipped_years": sorted(int(y) for y in ys if ranks[y] != ref),
                                 "S3_first_years": sorted(int(y) for y in ys if ranks[y][-1] == 0)}
    return df, out


def revenue_floor(rev):
    """M3c 보고: operator_revenue 표(해 열 포함)에서 W1 사업별 수익 ÷ floor. 1 이상이면 '무차별' 전제가 깨진 해·사업."""
    r = rev[(rev.plan == "D_lo") & (rev.variant == "iii") & (rev.limit_mult == 1.0)].copy()
    r["revenue_over_floor"] = r.revenue / r.floor
    return r[["weather_year", "design", "project", "revenue", "floor", "revenue_over_floor"]]


def s3_dir(year, mult=1.0):
    return OUT / f"w{year}_x{mult}_S3"


def main(argv):
    if argv[:1] == ["run"]:
        run(int(argv[1]), float(argv[2]) if len(argv) > 2 else 1.0, log=lambda *x: print(*x, flush=True))
    elif argv[:1] == ["jobs"]:
        print("\n".join(jobs([int(a) for a in argv[1:]] or None)))
    elif argv[:1] == ["summary"]:
        m3a = json.loads((ROOT / "results" / "system" / "m3a" / "summary.json").read_text())
        rows, revs = {}, []
        for y in years():
            df, _ = collect_year(y)
            rows[y] = year_row(df, pd.read_csv(s3_dir(y) / "results.csv"))
            for p in sorted(M1.glob(("x1.0_S*" if y == 2013 else f"w{y}_x1.0_S*") + "/operator_revenue.csv")):
                revs.append(pd.read_csv(p).assign(weather_year=y))
            revs.append(pd.read_csv(s3_dir(y) / "operator_revenue.csv").assign(weather_year=y))
        df, out = summarize(rows, m3a.get("not_comparable_x1.0", []))
        rf = revenue_floor(pd.concat(revs))
        rf = rf[rf.design.isin(DESIGNS)]
        out["m3c_revenue_over_floor"] = {d: {"median": float(g.revenue_over_floor.median()),
                                             "max": float(g.revenue_over_floor.max()),
                                             "n_at_or_above_floor": int((g.revenue_over_floor >= 1).sum()), "n": len(g)}
                                         for d, g in rf.groupby("design")}
        out["m3c_at_or_above_floor"] = rf[rf.revenue_over_floor >= 1][["weather_year", "design", "project"]].values.tolist()
        OUT.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT / "summary_by_year.csv", index_label="weather_year")
        rf.to_csv(OUT / "m3c_revenue_floor.csv", index=False)
        (OUT / "summary.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
        print(json.dumps(out, indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main(sys.argv[1:])
