"""
2단계: 비용 최소 재급전 (IMPL 2.3, spec.yaml redispatch). 1단계 계획을 받아, 경계 한도를 지키도록 비용 기준으로 조정한다.

    redispatch(plan, net, mode, fixed_units=None, infeasible="strict")
      mode="gen_only"      변형 (i)  : 저장은 모두 1단계 계획 그대로, 발전기(와 정전)만 조정
      mode="intertemporal" 변형 (ii) : 저장도 1년 전체에 걸쳐 다시 고름. fixed_units를 주면 그 저장만 1단계 계획에 묶음
                           변형 (iii): mode="intertemporal", fixed_units = W1 북쪽 사업
      M3에서 mode="sequential"(구간별 순차 재급전)을 더한다.

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

from gbess.system.network import LP, add_dispatch, read
from gbess.system.stage1 import REL_TOL, cost_cap_row, solve_stage1, stage1_extreme

MODES = ("gen_only", "intertemporal")
INFEASIBLE = ("strict", "min_deviation")
DEV_TOL = 1e-6


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
