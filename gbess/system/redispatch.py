"""
2단계: 비용 최소 재급전 (IMPL 2.3, spec.yaml redispatch). 1단계 계획을 받아, 경계 한도를 지키도록 비용 기준으로 조정한다.

    redispatch(plan, net, mode, fixed_units=None, infeasible="strict")
      mode="gen_only"      변형 (i)  : 저장은 모두 1단계 계획 그대로, 발전기(와 정전)만 조정
      mode="intertemporal" 변형 (ii) : 저장도 1년 전체에 걸쳐 다시 고름. fixed_units를 주면 그 저장만 1단계 계획에 묶음
                           변형 (iii): mode="intertemporal", fixed_units = W1 북쪽 사업
                           S3-제약시간: 변형 (iii)에 free_hours(제약 시간 표시)를 주면 그 시간에는 W1 북쪽도 묶지 않음
      mode="sequential"    구간별 순차 재급전 (M1 조건부 판정용, 2026-11-05 연구자 위임으로 정의): NESO는 한 시간씩, 앞을 보지
                           않고 재급전한다. 그 시간에는 발전기와 모든 저장(W1 북쪽 포함)을 조정할 수 있다. 발전기는 한계비용,
                           저장은 1단계 시장 해의 물 가치(저장 수지 쌍대)로 값을 매긴다: 시간 t 끝에 남은 에너지 1 MWh는 1단계의
                           t+1 물 가치(마지막 시간은 연말 저장량 제약의 쌍대)만큼의 값이다. 조정 뒤의 실제 저장량을 다음 시간으로
                           넘긴다. 연말 저장량이 1단계 계획과 다르면 그 차이를 연말 물 가치로 정산해 비용에 더한다.
                           (저장이 BM에 기회비용 단가를 낸다는 관행. 앞을 보지 않으므로 계획자 최적보다 비싸질 수 있다)
                           지시가 없으면 발전소는 제출한 계획(FPN = 1단계 계획)을 따르므로, 저장이 계획에서 벗어나는 양에 MWh당
                           FPN_TIE(£0.01)를 붙여 같은 비용의 해 중에서는 계획을 따르게 한다. 이 몫은 비용 집계에 넣지 않는다.
                           fixed_units를 주면 그 저장은 시간마다 1단계 계획에 묶는다(순차판 (iii)). free_hours를 주면 그 시간에는
                           묶지 않는다(순차판 S3, M3c+S3 추가 판, 연구자 승인 2026-11-07, 보고만). 묶은 저장 때문에 그 시간을 풀 수
                           없으면 min_deviation처럼 이탈량을 먼저 최소화한다(이탈량은 extra["fixed_deviation_mwh"]).

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
  "min_shed"      : '충전 정전' 판 (M3a 결과 뒤 추가, 연구자 결정 2026-11-06, 보고만). 정전 변수가 있으면 LP는 늘 풀리므로
                    min_deviation은 묶은 저장 대신 소비자 공급을 끊는다. 이 판은 "NESO는 정전을 막을 때만 묶은 저장에 지시"로 본다:
                    사전식 세 번 풀이 ① 최종 운전의 정전량 최소(묶은 저장 이탈 허용) ② 그 정전량에서 이탈량 최소 ③ 비용 최소.
                    정전이 없는 판에서는 ①이 0, ②가 0이라 min_deviation과 같다. 정전량은 extra["shed_min_mwh"]

최소 지시량 (redispatch_lo(…, min_instruction=True), M3c+S3 추가 판, 연구자 승인 2026-11-07, 보고만)
  D_lo 결합 LP는 비용만 최소화해서, 같은 비용의 해 중 묶음을 푼 저장(free_hours의 fixed_units)을 크게 다시 짜는 해를 고를
  수 있다. 이 판은 D_lo를 푼 뒤 "재급전 비용 ≤ 최솟값 + C1 × rel_tol" 안에서 그 저장의 지시량 Σ|Δch| + |Δd|(1단계 계획 대비,
  1단계 계획도 C1 × (1 + rel_tol) 안에서 함께 고름)를 최소화한다. 지시량은 extra["instructed_min_mwh"]

1단계 해가 여럿일 때 (spec.yaml degeneracy)
  redispatch_lo: "1단계 계획 + 재급전"을 한 LP로 묶어, 1단계 비용 ≤ C1* × (1 + 1e-6) 안에서 재급전 비용을 최소화 (D_lo, 정확)
  redispatch_hi: 1단계 극단 계획 두 개(extreme_units의 충전 최소 / 방전 최대)에 각각 재급전을 풀어 큰 쪽 (D_hi, 근사)
"""
import numpy as np

from gbess.system.network import LP, Gen, Network, Store, add_dispatch, read
from gbess.system.network import Dispatch
from gbess.system.stage1 import REL_TOL, cost_cap_row, solve_stage1, stage1_extreme

MODES = ("gen_only", "intertemporal", "sequential")
INFEASIBLE = ("strict", "min_deviation", "min_shed")
DEV_TOL = 1e-6
FPN_TIE = 0.01                     # £/MWh. 순차 재급전에서 저장이 1단계 계획에서 벗어나는 양에 붙이는 동률 깨기 비용
SEQ_FIXED_PENALTY = 1e6            # £/MWh. 순차판에서 묶은 저장의 이탈 비용(첫 풀이). 이탈이 남으면 사전식으로 다시 푼다


def _fixed_names(net, mode, fixed_units):
    if mode == "gen_only":
        return net.store_names()
    if mode == "intertemporal":
        return list(fixed_units or [])
    raise ValueError(f"mode는 {MODES}")


def _link(lp, net, b2, units, target, soft, free=None):
    """b2의 units 충·방전을 target에 묶는다. target = (ch 배열들, d 배열들) 상수 또는 1단계 블록(b1).
    free: (T,) bool. True인 시간에는 묶지 않는다(S3-제약시간). soft면 이탈 변수(±)를 두고 그 번호를 돌려준다."""
    names = net.store_names()
    hrs = np.arange(net.T) if free is None else np.flatnonzero(~np.asarray(free, bool))
    dev = []
    if len(hrs) == 0:
        return np.array([], int)
    for u in units:
        i = names.index(u)
        for x2, tgt in ((b2.ch, "ch"), (b2.d, "d")):
            terms = [(x2[i][hrs], 1.0)]
            if isinstance(target, dict):
                rhs = np.asarray(target[u][0 if tgt == "ch" else 1])[hrs]
            else:
                rhs = np.zeros(len(hrs))
                terms.append((getattr(target, tgt)[i][hrs], -1.0))
            if soft:
                pos, neg = lp.var((len(hrs),)), lp.var((len(hrs),))
                terms += [(pos, -1.0), (neg, 1.0)]
                dev += [pos, neg]
            lp.eq.add(rhs, terms)
    return np.concatenate(dev) if dev else np.array([], int)


def _solve(lp, c, dev, infeasible, shed=None):
    """infeasible="min_deviation"이면 먼저 이탈량 최소, 그다음 그 이탈량 안에서 c 최소.
    "min_shed"면 그 앞에 shed(최종 운전의 정전 변수 번호) 합을 먼저 최소화한다."""
    if infeasible == "strict" or len(dev) == 0:
        return lp.solve(c_override=c), 0.0
    secs = 0.0
    if infeasible == "min_shed":
        shed = np.asarray(shed).ravel()
        c_shed = np.zeros(lp.n)
        c_shed[shed] = 1.0
        rs = lp.solve(c_override=c_shed)
        secs += rs.seconds
        lp.le.add([float(rs.x[shed].sum()) * (1 + DEV_TOL) + DEV_TOL], [(shed[None, :], 1.0)])
    c_dev = np.zeros(lp.n)
    c_dev[dev] = 1.0
    r0 = lp.solve(c_override=c_dev)
    dev_min = float(r0.x[dev].sum())
    lp.le.add([dev_min * (1 + DEV_TOL) + DEV_TOL], [(dev[None, :], 1.0)])
    r = lp.solve(c_override=c)
    r.seconds += r0.seconds + secs
    return r, float(r.x[dev].sum())


def redispatch(plan, net, mode, fixed_units=None, infeasible="strict", free_hours=None):
    if mode == "sequential":
        return redispatch_sequential(plan, net, fixed_units=fixed_units, free_hours=free_hours)
    if infeasible not in INFEASIBLE:
        raise ValueError(f"infeasible는 {INFEASIBLE}")
    names = net.store_names()
    units = _fixed_names(net, mode, fixed_units)
    lp = LP()
    b2 = add_dispatch(lp, net, network=True)
    target = {u: (plan.ch[names.index(u)], plan.d[names.index(u)]) for u in units}
    dev = _link(lp, net, b2, units, target, soft=infeasible != "strict", free=free_hours)
    res, dev_mwh = _solve(lp, lp.cost_vector(), dev, infeasible, b2.shed)
    out = read(net, res, b2, network=True)
    if dev_mwh > 0:
        out.prices = None          # 이탈량 제약이 걸린 풀이의 쌍대는 구역 가격이 아님
    out.extra.update(redispatch_cost=out.cost - plan.cost, stage1_cost=plan.cost, mode=mode,
                     fixed_units=sorted(units), infeasible=infeasible, fixed_deviation_mwh=dev_mwh * net.dt)
    return out


def redispatch_lo(net, mode, fixed_units=None, c1=None, caps=None, rel_tol=REL_TOL, infeasible="strict",
                  free_hours=None, min_instruction=False):
    """재급전 비용을 최소로 만드는 1단계 최적 계획과 그 재급전. extra['plan']에 그 1단계 계획.
    min_instruction: 그 비용 안에서 free_hours의 fixed_units 지시량을 최소화한 해를 돌려준다(모듈 머리말)."""
    if c1 is None:
        c1 = solve_stage1(net, caps=caps).cost
    units = _fixed_names(net, mode, fixed_units)
    lp = LP()
    b1 = add_dispatch(lp, net, network=False, caps=caps)
    cost_cap_row(lp, b1, c1, rel_tol)
    b2 = add_dispatch(lp, net, network=True)
    dev = _link(lp, net, b2, units, b1, soft=infeasible != "strict", free=free_hours)
    ins = np.array([], int)
    if min_instruction:
        if free_hours is None:
            raise ValueError("min_instruction에는 free_hours가 필요")
        ins = _link(lp, net, b2, units, b1, soft=True, free=~np.asarray(free_hours, bool))   # 푼 시간의 |Δ| (비용 0)
    c = np.zeros(lp.n)
    np.add.at(c, b2.cost_idx, b2.cost_coef)
    np.add.at(c, b1.cost_idx, -b1.cost_coef)
    res, dev_mwh = _solve(lp, c, dev, infeasible, b2.shed)
    r_min = float(c @ res.x)
    if min_instruction:
        nz = np.flatnonzero(c)
        lp.le.add([r_min + abs(c1) * rel_tol], [(nz[None, :], c[nz])])
        c_ins = np.zeros(lp.n)
        c_ins[ins] = 1.0
        if len(dev):
            c_ins[dev] = 1.0
        r2 = lp.solve(c_override=c_ins)
        r2.seconds += res.seconds
        res = r2
    plan = read(net, res, b1, network=False)
    final = read(net, res, b2, network=True)
    plan.prices = final.prices = None   # 이 결합 LP의 쌍대는 시장 가격이 아님
    final.extra.update(redispatch_cost=final.cost - plan.cost, stage1_cost=plan.cost, mode=mode,
                       fixed_units=sorted(units), plan=plan, infeasible=infeasible,
                       fixed_deviation_mwh=dev_mwh * net.dt)
    if min_instruction:
        final.extra.update(redispatch_cost_min=r_min, instructed_min_mwh=float(res.x[np.concatenate([ins, dev])].sum()) * net.dt)
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


def redispatch_sequential(plan, net, log_every=None, fixed_units=None, free_hours=None):
    """구간별 순차 재급전 (모듈 머리말). plan은 쌍대(water_value)가 있는 1단계 첫 풀이여야 한다.
    fixed_units: 시간마다 계획에 묶을 저장. free_hours: (T,) bool, True인 시간에는 묶지 않음."""
    if "water_value" not in plan.extra:
        raise ValueError("1단계 계획에 물 가치(water_value)가 없음: solve_stage1의 첫 풀이를 넘길 것")
    import time
    t0 = time.perf_counter()
    wv, wv_end = plan.extra["water_value"], plan.extra["water_value_end"]
    G, S, Z, T, dt = len(net.gens), len(net.stores), net.Z, net.T, net.dt
    ub, lb, gcost = net.gen_ub(), net.gen_lb(), net.gen_cost()
    E = np.array([s.e_mwh for s in net.stores])
    e_prev = np.array([s.soc0 * s.e_mwh for s in net.stores])
    p, ch, d, e = np.zeros((G, T)), np.zeros((S, T)), np.zeros((S, T)), np.zeros((S, T))
    shed, flows = np.zeros((Z, T)), np.zeros((Z - 1, T))
    fixed = [k for k, s in enumerate(net.stores) if s.name in set(fixed_units or [])]
    free = np.zeros(T, bool) if free_hours is None else np.asarray(free_hours, bool)
    fixed_dev = 0.0
    for t in range(T):
        gens = [Gen(g.name, g.zone, 1.0, gcost[i, t], [ub[i, t]], g.renewable, lb[i, t]) for i, g in enumerate(net.gens)]
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
        tied = np.array([] if free[t] else [dev[4 * k + j] for k in fixed for j in range(4)], int)   # 저장마다 ch±, d±
        c[tied] = SEQ_FIXED_PENALTY * dt
        x = lp.solve(c_override=c).x
        if len(tied) and x[tied].sum() > DEV_TOL:          # 묶은 채로는 풀 수 없는 시간: 이탈량 최소 → 비용 최소
            c0 = np.zeros(lp.n)
            c0[tied] = 1.0
            m = float(lp.solve(c_override=c0).x[tied].sum())
            lp.le.add([m * (1 + DEV_TOL) + DEV_TOL], [(tied[None, :], 1.0)])
            c[tied] = FPN_TIE * dt
            x = lp.solve(c_override=c).x
        fixed_dev += float(x[tied].sum()) * dt
        p[:, t], ch[:, t], d[:, t], e[:, t] = x[b.p[:, 0]], x[b.ch[:, 0]], x[b.d[:, 0]], x[b.e[:, 0]]
        shed[:, t], flows[:, t] = x[b.shed[:, 0]], x[b.f[:, 0]]
        e_prev = e[:, t]
        if log_every and (t + 1) % log_every == 0:
            print(f"    순차 재급전 {t + 1}/{T}시간", flush=True)
    gc = gcost
    vc = np.array([s.var_cost for s in net.stores])[:, None]
    run_cost = float((gc * p).sum() * dt + (vc * d).sum() * dt + net.voll * shed.sum() * dt)
    terminal_adj = float(-(wv_end * (e[:, -1] - plan.e[:, -1])).sum())
    out = Dispatch(p, ch, d, e, shed, run_cost + terminal_adj, flows, None, "sequential", time.perf_counter() - t0)
    out.extra.update(redispatch_cost=out.cost - plan.cost, stage1_cost=plan.cost, mode="sequential",
                     fixed_units=sorted(net.stores[k].name for k in fixed), free_hours=int(free.sum()),
                     terminal_adjustment=terminal_adj, running_cost=run_cost, fixed_deviation_mwh=fixed_dev)
    return out
