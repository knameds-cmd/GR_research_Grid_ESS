"""
1단계: 전국 시장(구리판). 송전 제약 없이 전국 하나의 수지로 비용을 최소화한다 (IMPL 2.2).

선형 모형에서 경쟁 가격 수용자의 이익 최대화 = 비용 최소화이므로 장주기 자산의 이익 최대화를 따로 풀지 않는다
(spec.yaml model.ldes_objective.m1 = stage1_cost_min). 출력의 flows는 사슬 구조로 계산한 암묵적 경계 조류 f¹,
prices는 전국 수지의 쌍대 λ[t] (spec.yaml degeneracy.national_price: 이 첫 풀이의 λ를 쓴다).

1단계 해는 하나로 정해지지 않을 수 있다(북·남 저장이 같은 가격을 봄). 그래서 stage1_extreme은 1단계 비용을
최적값 × (1 + rel_tol) 안에 묶은 채 정해진 저장들의 충전량을 최소화하거나 방전량을 최대화한 계획을 낸다
(spec.yaml degeneracy.D_hi = extreme_plans).
"""
import numpy as np

from gbess.system.network import LP, add_dispatch, read, solve_dispatch

REL_TOL = 1.0e-6                   # spec.yaml degeneracy.fix_stage1_cost_rel_tol


def solve_stage1(net, caps=None):
    return solve_dispatch(net, network=False, caps=caps)


def cost_cap_row(lp, blk, c1, rel_tol=REL_TOL):
    """1단계 비용 ≤ C1* × (1 + rel_tol)."""
    lp.le.add([c1 + rel_tol * abs(c1)], [(blk.cost_idx[None, :], blk.cost_coef[None, :])])


def stage1_extreme(net, c1, units, objective, caps=None, rel_tol=REL_TOL):
    """objective: "min_charge"(units의 연간 충전량 최소) 또는 "max_discharge"(units의 연간 방전량 최대)."""
    lp = LP()
    blk = add_dispatch(lp, net, network=False, caps=caps)
    cost_cap_row(lp, blk, c1, rel_tol)
    names = net.store_names()
    rows = [names.index(u) for u in units]
    c = np.zeros(lp.n)
    if objective == "min_charge":
        c[blk.ch[rows].ravel()] = 1.0
    elif objective == "max_discharge":
        c[blk.d[rows].ravel()] = -1.0
    else:
        raise ValueError(objective)
    out = read(net, lp.solve(c_override=c), blk, network=False)
    out.prices = None              # 이 풀이의 쌍대는 가격이 아님
    out.extra["objective"] = objective
    return out
