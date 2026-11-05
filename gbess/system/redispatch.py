"""
2단계: 비용 최소 재급전 (IMPL 2.3, spec.yaml redispatch). 1단계 계획을 받아, 경계 한도를 지키도록 비용 기준으로 조정한다.

    redispatch(plan, net, mode, fixed_units=None, infeasible="strict")
      mode="gen_only"      변형 (i)  : 저장은 모두 1단계 계획 그대로, 발전기(와 정전)만 조정
      mode="intertemporal" 변형 (ii) : 저장도 1년 전체에 걸쳐 다시 고름. fixed_units를 주면 그 저장만 1단계 계획에 묶음
                           변형 (iii): mode="intertemporal", fixed_units = W1 북쪽 사업
      mode="sequential"    구간별 순차 재급전 (M1 조건부 판정용, 2026-11-05 연구자 위임으로 정의): NESO는 한 시간씩, 앞을 보지
                           않고 재급전한다. 그 시간에는 발전기와 모든 저장(W1 북쪽 포함)을 조정할 수 있다. 발전기는 한계비용,
                           저장은 1단계 시장 해의 물 가치(저장 수지 쌍대)로 값을 매긴다: 시간 t 끝에 남은 에너지 1 MWh는 1단계의
                           t+1 물 가치(마지막 시간은 연말 저장량 제약의 쌍대)만큼의 값이다. 조정 뒤의 실제 저장량을 다음 시간으로
                           넘긴다. 연말 저장량이 1단계 계획과 다르면 그 차이를 연말 물 가치로 정산해 비용에 더한다.
                           (저장이 BM에 기회비용 단가를 낸다는 관행. 앞을 보지 않으므로 계획자 최적보다 비싸질 수 있다)
                           지시가 없으면 발전소는 제출한 계획(FPN = 1단계 계획)을 따르므로, 저장이 계획에서 벗어나는 양에 MWh당
                           FPN_TIE(£0.01)를 붙여 같은 비용의 해 중에서는 계획을 따르게 한다. 이 몫은 비용 집계에 넣지 않는다.

조정 단가는 한계비용, 상향·하향 대칭이다. 그러면 "Σ c·(u − w)를 최소화"하는 것은 "최종 운전의 비용을 최소화"하는 것과
같으므로 최종 운전을 변수로 둔다. 재급전 비용 = 최종 운전 비용 − 1단계 계획 비용 (실제 BM 단가보다 낮을 수 있어 하한).
변형 (ii)는 실행 가능 집합이 계획자 최적과 같아 최종 비용이 늘 C(S6)과 같다 (시험).

묶은 저장 때문에 풀 수 없을 때 (infeasible=)
  묶은 저장의 방전이 "그 쪽 수요 + 경계 한도"보다 크거나, 묶은 충전이 그 쪽 공급 + 경계 한도보다 크면 발전기만으로는
  수지를 맞출 수 없다. spec.yaml은 이 경우를 정하지 않았다(연구자에게 물을 사항).
  "strict"        : 그대로 실패(RuntimeError). spec 문구 그대로
  "min_deviation" : 묶은 저장이 계획에서 벗어나는 양 Σ|Δch| + Σ|Δd| (MWh)를 먼저 최소화하고, 그 양을 넘지 않는 범위에서
                    비용을 최소화한다(사전식 두 번 풀이). 벗어난 양은 extra["fixed_deviation_mwh"]에 남긴다. 저장량은
                    벗어난 운전대로 물리적으로 바뀐다. 묶을 수 있으면 벗어난 양 0이라 strict와 같다

1단계 해가 여럿일 때 (spec.yaml degeneracy)
  redispatch_lo: "1단계 계획 + 재급전"을 한 LP로 묶어, 1단계 비용 ≤ C1* × (1 + 1e-6) 안에서 재급전 비용을 최소화 (D_lo, 정확)
  redispatch_hi: 1단계 극단 계획 두 개(extreme_units의 충전 최소 / 방전 최대)에 각각 재급전을 풀어 큰 쪽 (D_hi, 근사)
"""
import numpy as np

from gbess.system.network import LP, Gen, Network, Store, add_dispatch, read
from gbess.system.network import Dispatch
from gbess.system.stage1 import REL_TOL, cost_cap_row, solve_stage1, stage1_extreme

MODES = ("gen_only", "intertemporal", "sequential")
INFEASIBLE = ("strict", "min_deviation")
DEV_TOL = 1e-6
FPN_TIE = 0.01                     # £/MWh. 순차 재급전에서 저장이 1단계 계획에서 벗어나는 양에 붙이는 동률 깨기 비용


def _fixed_names(net, mode, fixed_units):
    if mode == "gen_only":
        return net.store_names()
    if mode == "intertemporal":
        return list(fixed_units or [])
    raise ValueError(f"mode는 {MODES}")


def _link(lp, net, b2, units, target, soft):
    """b2의 units 충·방전을 target에 묶는다. target = (ch 배열들, d 배열들) 상수 또는 1단계 블록(b1).
    soft면 이탈 변수(±)를 두고 그 번호를 돌려준다."""
    names = net.store_names()
    dev = []
    for u in units:
        i = names.index(u)
        for x2, tgt in ((b2.ch, "ch"), (b2.d, "d")):
            terms = [(x2[i], 1.0)]
            if isinstance(target, dict):
                rhs = target[u][0 if tgt == "ch" else 1]
            else:
                rhs = np.zeros(net.T)
                terms.append((getattr(target, tgt)[i], -1.0))
            if soft:
                pos, neg = lp.var((net.T,)), lp.var((net.T,))
                terms += [(pos, -1.0), (neg, 1.0)]
                dev += [pos, neg]
            lp.eq.add(rhs, terms)
    return np.concatenate(dev) if dev else np.array([], int)


def _solve(lp, c, dev, infeasible):
    """infeasible="min_deviation"이면 먼저 이탈량 최소, 그다음 그 이탈량 안에서 c 최소."""
    if infeasible == "strict" or len(dev) == 0:
        return lp.solve(c_override=c), 0.0
    c_dev = np.zeros(lp.n)
    c_dev[dev] = 1.0
    r0 = lp.solve(c_override=c_dev)
    dev_min = float(r0.x[dev].sum())
    lp.le.add([dev_min * (1 + DEV_TOL) + DEV_TOL], [(dev[None, :], 1.0)])
    r = lp.solve(c_override=c)
    r.seconds += r0.seconds
    return r, float(r.x[dev].sum())


def redispatch(plan, net, mode, fixed_units=None, infeasible="strict"):
    if mode == "sequential":
        if fixed_units:
            raise ValueError("sequential은 모든 저장을 조정한다 (fixed_units 없음)")
        return redispatch_sequential(plan, net)
    if infeasible not in INFEASIBLE:
        raise ValueError(f"infeasible는 {INFEASIBLE}")
    names = net.store_names()
    units = _fixed_names(net, mode, fixed_units)
    lp = LP()
    b2 = add_dispatch(lp, net, network=True)
    target = {u: (plan.ch[names.index(u)], plan.d[names.index(u)]) for u in units}
    dev = _link(lp, net, b2, units, target, soft=infeasible == "min_deviation")
    res, dev_mwh = _solve(lp, lp.cost_vector(), dev, infeasible)
    out = read(net, res, b2, network=True)
    if dev_mwh > 0:
        out.prices = None          # 이탈량 제약이 걸린 풀이의 쌍대는 구역 가격이 아님
    out.extra.update(redispatch_cost=out.cost - plan.cost, stage1_cost=plan.cost, mode=mode,
                     fixed_units=sorted(units), infeasible=infeasible, fixed_deviation_mwh=dev_mwh * net.dt)
    return out


def redispatch_lo(net, mode, fixed_units=None, c1=None, caps=None, rel_tol=REL_TOL, infeasible="strict"):
    """재급전 비용을 최소로 만드는 1단계 최적 계획과 그 재급전. extra['plan']에 그 1단계 계획."""
    if c1 is None:
        c1 = solve_stage1(net, caps=caps).cost
    units = _fixed_names(net, mode, fixed_units)
    lp = LP()
    b1 = add_dispatch(lp, net, network=False, caps=caps)
    cost_cap_row(lp, b1, c1, rel_tol)
    b2 = add_dispatch(lp, net, network=True)
    dev = _link(lp, net, b2, units, b1, soft=infeasible == "min_deviation")
    c = np.zeros(lp.n)
    np.add.at(c, b2.cost_idx, b2.cost_coef)
    np.add.at(c, b1.cost_idx, -b1.cost_coef)
    res, dev_mwh = _solve(lp, c, dev, infeasible)
    plan = read(net, res, b1, network=False)
    final = read(net, res, b2, network=True)
    plan.prices = final.prices = None   # 이 결합 LP의 쌍대는 시장 가격이 아님
    final.extra.update(redispatch_cost=final.cost - plan.cost, stage1_cost=plan.cost, mode=mode,
                       fixed_units=sorted(units), plan=plan, infeasible=infeasible,
                       fixed_deviation_mwh=dev_mwh * net.dt)
    return final


def redispatch_hi(net, mode, extreme_units, fixed_units=None, c1=None, caps=None, rel_tol=REL_TOL, infeasible="strict"):
    """극단 계획 두 개(extreme_units의 충전 최소 / 방전 최대) 각각의 재급전 중 재급전 비용이 큰 쪽. 정확한 최대의 하한."""
    if c1 is None:
        c1 = solve_stage1(net, caps=caps).cost
    runs = []
    for obj in ("min_charge", "max_discharge"):
        plan = stage1_extreme(net, c1, extreme_units, obj, caps=caps, rel_tol=rel_tol)
        r = redispatch(plan, net, mode, fixed_units, infeasible=infeasible)
        r.extra.update(plan=plan, extreme=obj)
        runs.append(r)
    best = max(runs, key=lambda r: r.extra["redispatch_cost"])
    best.extra["candidates"] = {r.extra["extreme"]: r.extra["redispatch_cost"] for r in runs}
    return best


def redispatch_sequential(plan, net, log_every=None):
    """구간별 순차 재급전 (모듈 머리말). plan은 쌍대(water_value)가 있는 1단계 첫 풀이여야 한다."""
    if "water_value" not in plan.extra:
        raise ValueError("1단계 계획에 물 가치(water_value)가 없음: solve_stage1의 첫 풀이를 넘길 것")
    import time
    t0 = time.perf_counter()
    wv, wv_end = plan.extra["water_value"], plan.extra["water_value_end"]
    G, S, Z, T, dt = len(net.gens), len(net.stores), net.Z, net.T, net.dt
    ub = net.gen_ub()
    E = np.array([s.e_mwh for s in net.stores])
    e_prev = np.array([s.soc0 * s.e_mwh for s in net.stores])
    p, ch, d, e = np.zeros((G, T)), np.zeros((S, T)), np.zeros((S, T)), np.zeros((S, T))
    shed, flows = np.zeros((Z, T)), np.zeros((Z - 1, T))
    for t in range(T):
        gens = [Gen(g.name, g.zone, 1.0, g.cost, [ub[i, t]], g.renewable) for i, g in enumerate(net.gens)]
        stores = [Store(s.name, s.zone, s.p_ch, s.p_dis, s.e_mwh, s.eta_ch, s.eta_dis,
                        float(e_prev[k] / E[k]) if E[k] > 0 else 0.0, s.var_cost, s.tags) for k, s in enumerate(net.stores)]
        sub = Network(net.zones, net.demand[:, t:t + 1], net.limits[:, t:t + 1], gens, stores, net.voll, dt, terminal=None)
        lp = LP()
        b = add_dispatch(lp, sub, network=True)
        names = sub.store_names()
        dev = _link(lp, sub, b, names, {u: (plan.ch[k, t:t + 1], plan.d[k, t:t + 1]) for k, u in enumerate(names)}, True)
        c = lp.cost_vector()
        value = wv[:, t + 1] if t + 1 < T else wv_end
        c[b.e[:, 0]] -= value
        c[dev] = FPN_TIE * dt
        x = lp.solve(c_override=c).x
        p[:, t], ch[:, t], d[:, t], e[:, t] = x[b.p[:, 0]], x[b.ch[:, 0]], x[b.d[:, 0]], x[b.e[:, 0]]
        shed[:, t], flows[:, t] = x[b.shed[:, 0]], x[b.f[:, 0]]
        e_prev = e[:, t]
        if log_every and (t + 1) % log_every == 0:
            print(f"    순차 재급전 {t + 1}/{T}시간", flush=True)
    gc = np.array([g.cost for g in net.gens])[:, None]
    vc = np.array([s.var_cost for s in net.stores])[:, None]
    run_cost = float((gc * p).sum() * dt + (vc * d).sum() * dt + net.voll * shed.sum() * dt)
    terminal_adj = float(-(wv_end * (e[:, -1] - plan.e[:, -1])).sum())
    out = Dispatch(p, ch, d, e, shed, run_cost + terminal_adj, flows, None, "sequential", time.perf_counter() - t0)
    out.extra.update(redispatch_cost=out.cost - plan.cost, stage1_cost=plan.cost, mode="sequential", fixed_units=[],
                     terminal_adjustment=terminal_adj, running_cost=run_cost, fixed_deviation_mwh=0.0)
    return out
