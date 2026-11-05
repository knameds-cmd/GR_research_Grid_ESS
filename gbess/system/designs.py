"""
설계안 S1a, S1b, S5 (IMPL 2.6, spec.yaml designs). 1단계(전국 시장)에 넣는 충·방전 한도와, 구역 시장(S5)을 만든다.

    S1a 고정 입출력 한도   대상 장주기(북쪽 구역 W1 지원 사업)의 ch ≤ X·Pch, d ≤ X·Pdis (spec: X = 0.5)
    S1b 제약 연동 한도     (1) S0 1단계 계획의 암묵적 경계 조류로 "표시 시간"을 정한다: 그 사업의 구역에서 남쪽으로 가는
                           길의 경계 l 중 하나라도 f¹[l,t] ≥ β·F[l,t]이면 표시 (spec: β = 1.0, 민감도 0.95)
                           (2) 다시 푼 1단계에서 표시 시간에 그 사업의 d = 0 (충전은 허용)
                           (3) 그 뒤 재급전. 표시는 S0 계획으로 한 번만 하고 다시 반복하지 않는다 (spec: iterate = false)
    S5 지역 가격           1단계를 구역 시장으로 푼다 = 계획자 최적과 같은 운전(선형 경쟁 모형). 가격은 구역 수지의 쌍대

S1a·S1b는 caps(저장 이름 → (ch 상한, d 상한))를 돌려주고, gbess.system.stage1.solve_stage1(net, caps=…)과
redispatch_lo/hi(…, caps=…)에 그대로 넘긴다.
"""
import numpy as np

from gbess.system.planner import solve_planner


def _store(net, name):
    return net.stores[net.store_names().index(name)]


def s1a_caps(net, units, X):
    T = net.T
    return {u: (np.full(T, X * _store(net, u).p_ch), np.full(T, X * _store(net, u).p_dis)) for u in units}


def s1b_marks(net, plan_s0, unit, beta):
    """그 사업의 구역에서 남쪽으로 가는 길의 경계(l = 구역 번호 … Z−2) 중 하나라도 f¹ ≥ β·F인 시간 (T,) bool."""
    z = _store(net, unit).zone
    path = slice(z, net.Z - 1)
    f, F = plan_s0.flows[path], net.limits[path]
    if f.shape[0] == 0:
        return np.zeros(net.T, bool)
    return (f >= beta * F - 1e-9).any(axis=0)


def s1b_caps(net, plan_s0, units, beta):
    caps = {}
    for u in units:
        m = s1b_marks(net, plan_s0, u, beta)
        st = _store(net, u)
        caps[u] = (np.full(net.T, st.p_ch), np.where(m, 0.0, st.p_dis))
    return caps


def solve_s5(net):
    """구역 시장. 운전과 계통 비용은 계획자 최적과 같고, prices = 구역 가격 (Z, T)."""
    out = solve_planner(net)
    out.extra["design"] = "S5"
    return out
