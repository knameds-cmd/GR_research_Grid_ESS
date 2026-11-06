"""
M1 실행과 지표 (IMPL 2.5·T7, spec.yaml metrics·go_no_go). 구역망(Network) 하나를 받아 설계안 × 재급전 변형 × 경계 한도 배율을
풀고, 결과표와 실행 기록(run.json: git 커밋, spec 해시, 입력 해시, 해 상태, 걸린 시간)을 남긴다.

    from gbess.system.run_m1 import run_m1
    rows = run_m1(net, w1_north=[...], w1_all=[...], levels={사업: (floor £/년, cap £/년)}, bind_boundaries=[B4 번호, B6 번호],
                  out_dir="results/system/m1/<판 이름>")

2030 입력(구역·설비·시계열)은 T4에서 만든다. 그 전까지 이 모듈은 시험용 작은 구역망으로만 돈다.

지표 정의 (spec.yaml)
  계통 총비용     최종 운전의 Σ c·p + Σ var·d + VoLL·shed (network.Dispatch.cost)
  재급전 비용     최종 비용 − 1단계 비용
  D               C(설계안, 변형) − C(S6). D_W1 = C(S0, iii) − C(S6). D_lo(결합 LP), D_hi(극단 계획, 근사)
  E_bind          S0 1단계(첫 풀이)에서 bind_boundaries 중 하나라도 암묵적 조류 ≥ 한도인 시간에, W1 북쪽 사업마다
                  max(d − ch, 0)을 더한 양 (TWh)
  출력제한        Σ (cap·avail − 최종 발전량), 풍력·태양광
  소비자 지급     도매 + 재급전 지급 + floor 보전 − cap 환수
                  도매 = Σ λ·D (S5: Σ 구역 가격 × 구역 수요). λ는 그 설계안 1단계 첫 풀이의 쌍대
                  재급전 지급 (pay_as_cost) = Σ c_g·Δp + Σ var_s·Δd (정전 비용은 지급이 아니라 빼고 따로 보고)
                  사업 수익 = Σ λ·(d¹ − ch¹) + var·Δd (1단계 거래 + 재급전 지급). 용량시장·보조서비스는 M1에서 뺌
                  floor 보전 = max(floor − 수익, 0), cap 환수 = 0.70 × max(수익 − cap, 0) (1년 근사, 가용률 충족 가정)
  S5의 혼잡 수입  Σ (구역 가격 차 × 경계 조류). spec 공식에는 없어서 소비자 지급에 넣지 않고 따로 보고
"""
import hashlib
import json
import subprocess
import time
from pathlib import Path

import numpy as np
import yaml

from gbess.finance.cap_floor import evaluate
from gbess.finance.costs import project_costs
from gbess.system.designs import s1a_caps, s1b_caps, solve_s5
from gbess.system.network import curtailment
from gbess.system.planner import solve_planner
from gbess.system.redispatch import redispatch, redispatch_hi, redispatch_lo
from gbess.system.stage1 import solve_stage1

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "gbess" / "config" / "spec.yaml"
TECH_MAP = {"Li-ion BESS": "li_ion", "PSH": "psh", "CAES": "caes", "VFB/Zn": "flow", "VFB": "flow"}


def load_spec(path=SPEC):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


# ---------------------------------------------------------------------------------------------------------------
def floor_cap_levels(projects, case="central"):
    """projects: [(이름, Ofgem 기술 이름, MW, 시간)] → {이름: (floor £/년, cap £/년)}. 사업별 실제 크기로 계산."""
    out = {}
    for name, tech, mw, h in projects:
        c = project_costs(TECH_MAP[tech], mw, h, case=case)
        r = evaluate(np.zeros(25), c.capex, c.opex, repex=c.repex, residual_value=c.residual_value)
        out[name] = (r["floor_level"], r["cap_level"])
    return out


def e_bind(net, plan_s0, units, boundaries):
    if not boundaries:
        return 0.0
    bind = (plan_s0.flows[boundaries] >= net.limits[boundaries] - 1e-9).any(axis=0)
    idx = [net.store_names().index(u) for u in units]
    net_dis = np.maximum(plan_s0.d[idx] - plan_s0.ch[idx], 0.0)
    return float(net_dis[:, bind].sum() * net.dt / 1e6)


def settle_cap_floor(revenue, levels, share_returned=0.70):
    """사업별 1년 근사: 보전 = max(floor − 수익, 0), 환수 = 0.70 × max(수익 − cap, 0)."""
    top = {u: max(levels[u][0] - r, 0.0) for u, r in revenue.items() if u in levels}
    claw = {u: share_returned * max(r - levels[u][1], 0.0) for u, r in revenue.items() if u in levels}
    return top, claw


def payments_national(net, lam, plan, final, units, levels):
    """S0·S1x: 도매(1단계 λ) + 재급전 지급(pay_as_cost) + floor 보전 − cap 환수. 사업 수익도 돌려준다."""
    dt = net.dt
    gc = net.gen_cost()
    vc = np.array([s.var_cost for s in net.stores])[:, None]
    wholesale = float((lam * net.demand.sum(axis=0)).sum() * dt)
    redis_pay = float(((final.p - plan.p) * gc).sum() * dt + ((final.d - plan.d) * vc).sum() * dt)
    names = net.store_names()
    rev = {}
    for u in units:
        i = names.index(u)
        rev[u] = float((lam * (plan.d[i] - plan.ch[i])).sum() * dt + vc[i, 0] * (final.d[i] - plan.d[i]).sum() * dt)
    top, claw = settle_cap_floor(rev, levels)
    return {"wholesale": wholesale, "redispatch_payment": redis_pay, "floor_topup": sum(top.values()),
            "cap_clawback": sum(claw.values()),
            "consumer_payment": wholesale + redis_pay + sum(top.values()) - sum(claw.values()),
            "shed_mwh": float(final.shed.sum() * dt), "operator_revenue": rev}


def payments_zonal(net, s5, units, levels):
    dt = net.dt
    pi = s5.prices
    wholesale = float((pi * net.demand).sum() * dt)
    names = net.store_names()
    rev = {}
    for u in units:
        i, z = names.index(u), net.stores[names.index(u)].zone
        rev[u] = float((pi[z] * (s5.d[i] - s5.ch[i])).sum() * dt)
    top, claw = settle_cap_floor(rev, levels)
    rent = float(((pi[1:] - pi[:-1]) * s5.flows).sum() * dt)
    return {"wholesale": wholesale, "redispatch_payment": 0.0, "floor_topup": sum(top.values()),
            "cap_clawback": sum(claw.values()),
            "consumer_payment": wholesale + sum(top.values()) - sum(claw.values()),
            "congestion_rent": rent, "shed_mwh": float(s5.shed.sum() * dt), "operator_revenue": rev}


# ---------------------------------------------------------------------------------------------------------------
def _row(design, variant, mult, r, c6, net, extra=None):
    row = {"design": design, "variant": variant, "limit_mult": mult, "system_cost": r.cost,
           "redispatch_cost": r.extra.get("redispatch_cost", 0.0), "D": r.cost - c6,
           "curtailment_mwh": curtailment(net, r.p), "status": r.status, "seconds": r.seconds,
           "fixed_deviation_mwh": r.extra.get("fixed_deviation_mwh", 0.0)}
    row.update(extra or {})
    return row


def run_one_limit(net, mult, w1_north, w1_all, levels, bind_boundaries, X=0.5, beta=1.0, infeasible="strict",
                  log=print, lo_variants=("i", "iii"), designs=("S0", "S1a", "S1b"), sequential=False):
    n = net.scaled_limits(mult)
    rows = []
    t0 = time.perf_counter()
    s6 = solve_planner(n)
    c6 = s6.cost
    rows.append(_row("S6", "-", mult, s6, c6, n))
    s5 = solve_s5(n)
    rows.append(_row("S5", "-", mult, s5, c6, n, payments_zonal(n, s5, w1_all, levels)))
    log(f"  ×{mult}: S6·S5 {time.perf_counter() - t0:.0f}s")

    s0 = solve_stage1(n)
    design_caps = {"S0": None, "S1a": s1a_caps(n, w1_north, X), "S1b": s1b_caps(n, s0, w1_north, beta)}
    variants = {"i": ("gen_only", None), "ii": ("intertemporal", None), "iii": ("intertemporal", w1_north)}
    for dname, caps in design_caps.items():
        if dname not in designs:
            continue
        plan = s0 if caps is None else solve_stage1(n, caps=caps)
        eb = e_bind(n, plan, w1_north, bind_boundaries) if dname == "S0" else None
        for v, (mode, fu) in variants.items():
            r = redispatch(plan, n, mode, fu, infeasible=infeasible)
            pay = payments_national(n, plan.prices, plan, r, w1_all, levels)
            rows.append(_row(dname, v, mult, r, c6, n, {**pay, "plan": "first_solve", "E_bind_twh": eb}))
        for v in lo_variants:
            mode, fu = variants[v]
            lo = redispatch_lo(n, mode, fu, c1=plan.cost, caps=caps, infeasible=infeasible)
            pay = payments_national(n, plan.prices, lo.extra["plan"], lo, w1_all, levels)
            rows.append(_row(dname, v, mult, lo, c6, n, {**pay, "plan": "D_lo"}))
        if dname == "S0" and sequential:
            sq = redispatch(plan, n, "sequential")
            pay = payments_national(n, plan.prices, plan, sq, w1_all, levels)
            rows.append(_row(dname, "seq", mult, sq, c6, n, {**pay, "plan": "first_solve",
                                                               "terminal_adjustment": sq.extra["terminal_adjustment"]}))
        if dname == "S0":
            hi = redispatch_hi(n, "intertemporal", w1_north, w1_north, c1=plan.cost, infeasible=infeasible)
            rows.append(_row(dname, "iii", mult, hi, c6, n, {"plan": "D_hi_approx", "extreme": hi.extra["extreme"]}))
        log(f"  ×{mult}: {dname} 끝 {time.perf_counter() - t0:.0f}s")
    return rows


def run_m1(net, w1_north, w1_all, levels, bind_boundaries, out_dir, inputs=(), limit_mults=(0.8, 1.0, 1.2),
           X=0.5, beta=1.0, infeasible="strict", log=print, lo_variants=("i", "iii"), label=None,
           designs=("S0", "S1a", "S1b"), sequential=False, weather_year=2013):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    rows = []
    for m in limit_mults:
        rows += run_one_limit(net, m, w1_north, w1_all, levels, bind_boundaries, X, beta, infeasible, log, lo_variants,
                              designs, sequential)
    record = {
        "git_commit": git_commit(), "spec_sha256": file_sha256(SPEC),
        "input_sha256": {str(p): file_sha256(p) for p in inputs},
        "solver_status": sorted({r["status"] for r in rows}), "solve_seconds": time.perf_counter() - t0,
        "label": label, "weather_year": weather_year,
        "options": {"limit_mults": list(limit_mults), "X": X, "beta": beta, "infeasible": infeasible,
                    "lo_variants": list(lo_variants), "designs": list(designs), "sequential": sequential,
                    "w1_north": list(w1_north), "bind_boundaries": list(bind_boundaries)},
    }
    (out_dir / "run.json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    flat = [{k: v for k, v in r.items() if k != "operator_revenue"} for r in rows]
    import pandas as pd
    pd.DataFrame(flat).to_csv(out_dir / "results.csv", index=False)
    rev = [{"design": r["design"], "variant": r["variant"], "limit_mult": r["limit_mult"], "plan": r.get("plan"),
            "project": u, "revenue": x, "floor": levels.get(u, (np.nan,))[0]}
           for r in rows for u, x in (r.get("operator_revenue") or {}).items()]
    pd.DataFrame(rev).to_csv(out_dir / "operator_revenue.csv", index=False)
    return rows


def main():
    import argparse
    from gbess.system.inputs import build_network_2030
    ap = argparse.ArgumentParser(description="M1 실행 (2030년, 기상연도 2013, 3구역)")
    ap.add_argument("--mult", type=float, nargs="+", default=[1.0], help="경계 한도 배율 (spec: 0.8 1.0 1.2)")
    ap.add_argument("--exclude-post-2030", action="store_true", help="첫 운전 2033 사업 제외 (민감도)")
    ap.add_argument("--nominal-limits", action="store_true", help="감산 없는 ETYS 2030 명목 한도 (보고만 하는 민감도)")
    ap.add_argument("--lo", nargs="+", default=["iii"], help="D_lo를 계산할 재급전 변형 (판정은 iii)")
    ap.add_argument("--beta", type=float, default=1.0)
    ap.add_argument("--label", default="main")
    ap.add_argument("--designs", nargs="+", default=["S0", "S1a", "S1b"], help="S6·S5는 늘 함께 계산")
    ap.add_argument("--weather-year", type=int, default=2013)
    ap.add_argument("--sequential", action="store_true", help="S0에 구간별 순차 재급전 판 추가")
    ap.add_argument("--interconnectors", default=None, choices=["price_taking"],
                    help="인터커넥터 가격 수용 민감도 (gbess.system.interconnectors, 기상연도 2020만)")
    a = ap.parse_args()
    net, meta = build_network_2030(include_post_2030=not a.exclude_post_2030, nominal_limits=a.nominal_limits,
                                   weather_year=a.weather_year, interconnectors=a.interconnectors)
    out = ROOT / "results" / "system" / "m1" / a.label
    print(f"판 {a.label}: 구역 {net.zones}, 한도 {net.limits[:, 0].tolist()} MW × {a.mult}, W1 북쪽 {len(meta['w1_north'])}건")
    run_m1(net, meta["w1_north"], meta["w1_all"], meta["levels"], meta["bind_boundaries"], out, inputs=meta["inputs"],
           limit_mults=a.mult, beta=a.beta, infeasible="min_deviation", lo_variants=a.lo, label=a.label, designs=a.designs,
           sequential=a.sequential, weather_year=a.weather_year,
           log=lambda *x: print(*x, flush=True))
    print(f"결과: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------------------------------------------
def collect(base=None, pattern="x*_S*"):
    """설계안별로 나눠 돌린 판(results/system/m1/<라벨>/results.csv)을 하나로 합친다. S6·S5는 같은 값이 여러 번 나오므로 하나만.
    한 번에 한 시나리오(같은 입력)만 모은다. 민감도 판은 한도 배율이 겹치므로 pattern으로 따로 모은다."""
    import pandas as pd
    base = Path(base or ROOT / "results" / "system" / "m1")
    frames = [pd.read_csv(p).assign(label=p.parent.name) for p in sorted(base.glob(f"{pattern}/results.csv"))]
    df = pd.concat(frames, ignore_index=True)
    df["plan"] = df["plan"].fillna("-")
    return df.drop_duplicates(subset=["design", "variant", "plan", "limit_mult"], keep="first")


def check_invariants(df, rel=1e-6):
    """spec go_no_go.invariants. 한도 배율마다 위반 목록을 돌려준다(비어 있으면 통과)."""
    bad = []
    for m, g in df.groupby("limit_mult"):
        c = {(r.design, r.variant, r.plan): r.system_cost for r in g.itertuples()}
        c6 = c[("S6", "-", "-")]
        tol = rel * abs(c6)                 # 인터커넥터 판은 수출 수입 때문에 C(S6) < 0일 수 있음
        s0 = {v: c.get(("S0", v, "first_solve")) for v in ("i", "ii", "iii")}
        if not (c6 - tol <= s0["ii"] <= s0["iii"] + tol and s0["iii"] <= s0["i"] + tol):
            bad.append((m, "C_S6 <= C_S0_ii <= C_S0_iii <= C_S0_i", s0))
        if abs(s0["ii"] - c6) > tol:
            bad.append((m, "C_S0_ii = C_S6", s0["ii"] - c6))
        if abs(c[("S5", "-", "-")] - c6) > tol:
            bad.append((m, "C_S5 = C_S6", c[("S5", "-", "-")] - c6))
        for d in ("S1a", "S1b"):
            for k, val in c.items():
                if k[0] == d and val < c6 - tol:
                    bad.append((m, f"C_{d} >= C_S6", k, val - c6))
        lo, hi = c.get(("S0", "iii", "D_lo")), c.get(("S0", "iii", "D_hi_approx"))
        if lo is not None and hi is not None and lo > hi + tol:
            bad.append((m, "D_lo <= D_hi", lo - hi))
    return bad


def go_no_go_values(df, spec=None):
    """spec go_no_go 규칙에 들어가는 값(£m/년)과 규칙대로 계산한 결과. 판정은 연구자가 내린다."""
    spec = spec or load_spec()
    g = spec["go_no_go"]
    M = g["materiality_M_gbp_m"]
    val = {}
    for m, x in df.groupby("limit_mult"):
        c = {(r.design, r.variant, r.plan): r for r in x.itertuples()}
        c6 = c[("S6", "-", "-")].system_cost
        lo = c[("S0", "iii", "D_lo")].system_cost - c6
        hi = c.get(("S0", "iii", "D_hi_approx"))
        s1x = {d: c[("S0", "iii", "D_lo")].system_cost - c[(d, "iii", "D_lo")].system_cost
               for d in ("S1a", "S1b") if (d, "iii", "D_lo") in c}
        val[m] = {"D_lo_gbp_m": lo / 1e6, "D_hi_approx_gbp_m": None if hi is None else (hi.system_cost - c6) / 1e6,
                  "E_bind_twh": c[("S0", "i", "first_solve")].E_bind_twh,
                  "C_S0_minus_C_S1x_gbp_m": {d: v / 1e6 for d, v in s1x.items()}}
    out = {"M_gbp_m": M, "go_threshold_gbp_m": g["go_multiple"] * M, "values": val}
    if {0.8, 1.0, 1.2} <= set(val):
        v8, v1, v12 = val[0.8], val[1.0], val[1.2]
        no_go = v1["D_lo_gbp_m"] < M and v8["D_lo_gbp_m"] < M
        go = (v1["D_lo_gbp_m"] >= g["go_multiple"] * M and v12["D_lo_gbp_m"] >= M and v1["E_bind_twh"] > 0
              and max(v1["C_S0_minus_C_S1x_gbp_m"].values(), default=-1) > 0)
        out["rule_result"] = "no_go" if no_go else ("go" if go else "conditional")
    else:
        out["rule_result"] = f"계산 불가: 한도 배율 {sorted(val)}만 있음 (0.8, 1.0, 1.2 필요)"
    return out


# ---------------------------------------------------------------------------------------------------------------
BLUE, ORANGE, AQUA, YELLOW, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#1a1a19", "#6b6a63", "#e4e3dd"


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def figure_weeks(out_dir, limit_mult=1.0):
    """그림 (a): 바람 많은 주와 바람 없는 주에 W1 북쪽 장주기의 순방전(1단계 전국 시장 vs S6 계획자 최적)과 B4·B6 암묵적 조류(1단계).
    재급전 (iii)은 W1 북쪽을 1단계 계획에 묶으므로 그 순방전은 1단계와 같다(그래서 따로 그리지 않음)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from gbess.system.inputs import build_network_2030
    net, meta = build_network_2030(limit_mult=limit_mult)
    north = meta["w1_north"]
    s1 = solve_stage1(net)
    s6 = solve_planner(net)
    idx = [net.store_names().index(u) for u in north]
    nd1 = (s1.d[idx] - s1.ch[idx]).sum(0) / 1e3
    nd6 = (s6.d[idx] - s6.ch[idx]).sum(0) / 1e3
    wind_n = sum(np.asarray(g.avail) * g.cap for g in net.gens if g.renewable and g.zone == 0 and "wind" in g.name)
    weekly = wind_n[: 52 * 168].reshape(52, 168).mean(1)
    weeks = {"바람 많은 주": int(weekly.argmax()), "바람 없는 주": int(weekly.argmin())}
    plt.rcParams["font.family"] = ["AppleGothic", "DejaVu Sans"]
    fig, axes = plt.subplots(2, 2, figsize=(11, 6), sharex="col")
    for j, (name, w) in enumerate(weeks.items()):
        sl = slice(w * 168, (w + 1) * 168)
        h = np.arange(168) / 24
        ax = axes[0, j]
        ax.plot(h, nd1[sl], color=BLUE, lw=2, label="W1 북쪽 순방전: 1단계 전국 시장 (= S0 운전)")
        ax.plot(h, nd6[sl], color=ORANGE, lw=2, label="W1 북쪽 순방전: S6 계획자 최적")
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_title(f"{name} (제{w + 1}주): W1 북쪽 장주기 순방전 (GW, +는 방전)", fontsize=9, color=INK, loc="left")
        _style(ax)
        ax = axes[1, j]
        for k, (lab, col) in enumerate((("B4", YELLOW), ("B6", AQUA))):
            ax.plot(h, s1.flows[k, sl] / 1e3, color=col, lw=2, label=f"{lab} 암묵적 조류 (1단계)")
            ax.plot(h, net.limits[k, sl] / 1e3, color=col, lw=1, ls="--", label=f"{lab} 한도")
        ax.set_title("경계 조류 (GW, 남행 +)", fontsize=9, color=INK, loc="left")
        ax.set_xlabel("일", fontsize=8, color=MUTED)
        _style(ax)
    h1, l1 = axes[0, 0].get_legend_handles_labels()
    h2, l2 = axes[1, 0].get_legend_handles_labels()
    fig.legend(h1 + h2, l1 + l2, loc="lower center", ncol=3, fontsize=8, frameon=False)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    p = Path(out_dir) / "fig_a_weeks.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p, weeks


def figure_bars(df, out_dir, limit_mult=1.0):
    """그림 (b): 판별 계통 총비용과 소비자 지급 (£bn/년). 두 지표는 축을 따로 둔 두 패널."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    x = df[df["limit_mult"] == limit_mult]
    keys = [("S6", "-", "-", "S6 계획자"), ("S5", "-", "-", "S5 지역 가격"), ("S0", "iii", "D_lo", "S0 (iii) D_lo"),
            ("S0", "i", "first_solve", "S0 (i) 첫 풀이"), ("S1a", "iii", "D_lo", "S1a (iii) D_lo"), ("S1b", "iii", "D_lo", "S1b (iii) D_lo")]
    rows = []
    for d, v, p, lab in keys:
        m = x[(x.design == d) & (x.variant == v) & (x.plan == p)]
        if len(m):
            rows.append((lab, m.system_cost.iloc[0] / 1e9, m.consumer_payment.iloc[0] / 1e9))
    plt.rcParams["font.family"] = ["AppleGothic", "DejaVu Sans"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    for ax, k, title in ((axes[0], 1, "계통 총비용 (£bn/년)"), (axes[1], 2, "소비자 지급 (£bn/년)")):
        vals = [r[k] for r in rows]
        bars = ax.bar([r[0] for r in rows], vals, color=BLUE, width=0.6)
        for b, val in zip(bars, vals):
            if np.isfinite(val):
                ax.text(b.get_x() + b.get_width() / 2, val, f"{val:.2f}", ha="center", va="bottom", fontsize=8, color=INK)
        ax.set_title(f"{title}, 한도 ×{limit_mult}", fontsize=9, color=INK, loc="left")
        ax.tick_params(axis="x", labelrotation=20)
        _style(ax)
    fig.tight_layout()
    p = Path(out_dir) / "fig_b_costs.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def run_sequential_only(limit_mults=(0.8, 1.0, 1.2), weather_year=2013, out=None, log=print):
    """이미 돌린 판에 S0 순차 재급전 행만 더한다(1단계 첫 풀이 + 순차 재급전, 판마다 수십 초). results_sequential.csv"""
    import pandas as pd
    from gbess.system.inputs import build_network_2030
    rows = []
    for m in limit_mults:
        net, meta = build_network_2030(limit_mult=m, weather_year=weather_year)
        c6 = solve_planner(net).cost
        s0 = solve_stage1(net)
        sq = redispatch(s0, net, "sequential")
        pay = payments_national(net, s0.prices, s0, sq, meta["w1_all"], meta["levels"])
        row = _row("S0", "seq", m, sq, c6, net, {**pay, "plan": "first_solve", "weather_year": weather_year,
                                                 "terminal_adjustment": sq.extra["terminal_adjustment"]})
        row.pop("operator_revenue", None)
        rows.append(row)
        log(f"  ×{m}: D_seq £{row['D'] / 1e6:.1f}m ({sq.seconds:.0f}s)")
    df = pd.DataFrame(rows)
    out = Path(out or ROOT / "results" / "system" / "m1" / f"results_sequential_{weather_year}.csv")
    df.to_csv(out, index=False)
    return df


def run_sequential_w1n_increment(limit_mults=(0.8, 1.0, 1.2), weather_year=2013, out=None, log=print, interconnectors=None):
    """W1 북쪽이 늘린 D_seq (보고만, docs/notes/m1_conditional_KO.md 2장): 같은 구역망에서 W1 북쪽 저장을 뺀 판과의 차이.
    열: limit_mult, fleet(with_W1N / without_W1N), C_S6, D_seq, D_i (£m). D_i = C(S0, 재급전 i) − C(S6)."""
    import pandas as pd
    from gbess.system.inputs import build_network_2030
    from gbess.system.network import Network
    rows = []
    for m in limit_mults:
        net, meta = build_network_2030(limit_mult=m, weather_year=weather_year, interconnectors=interconnectors)
        wo = Network(net.zones, net.demand, net.limits, net.gens,
                     [s for s in net.stores if s.name not in meta["w1_north"]], net.voll, net.dt, net.terminal)
        for fleet, n in (("with_W1N", net), ("without_W1N", wo)):
            c6 = solve_planner(n).cost
            s0 = solve_stage1(n)
            sq = redispatch(s0, n, "sequential")
            ri = redispatch(s0, n, "gen_only", infeasible="min_deviation")
            rows.append({"limit_mult": m, "fleet": fleet, "C_S6": c6 / 1e6, "D_seq": (sq.cost - c6) / 1e6,
                         "D_i": (ri.cost - c6) / 1e6})
            log(f"  ×{m} {fleet}: D_seq £{rows[-1]['D_seq']:.1f}m")
    df = pd.DataFrame(rows)
    sfx = "" if interconnectors is None else f"_ic_{interconnectors}"
    out = Path(out or ROOT / "results" / "system" / "m1" / f"results_sequential_w1n_increment_{weather_year}{sfx}.csv")
    df.to_csv(out, index=False)
    return df
