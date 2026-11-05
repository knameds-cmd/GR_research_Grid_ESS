"""
계획자 최적(S6): 구역 수지와 경계 한도를 처음부터 넣고 1년을 한 번에 푼다 (IMPL 2.4). 비교 기준.
prices는 구역 수지의 쌍대(구역 가격, (Z, T)). 선형 경쟁 모형에서는 구역 시장(S5)의 운전이 이것과 같다.
"""
from gbess.system.network import solve_dispatch


def solve_planner(net):
    return solve_dispatch(net, network=True)
