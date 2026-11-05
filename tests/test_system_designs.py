"""설계안 S1a, S1b, S5를 손계산 예제 E2(docs/notes/model_examples_KO.md)와 불변식으로 시험한다."""
import numpy as np
import pytest

from gbess.system.designs import s1a_caps, s1b_caps, s1b_marks, solve_s5
from gbess.system.planner import solve_planner
from gbess.system.redispatch import redispatch, redispatch_lo
from gbess.system.stage1 import solve_stage1
from tests.test_system_model import TIE, TOL, e1, e2, random_net


def test_s1a_caps_respected_and_halves_e2_distortion():
    net = e2()
    caps = s1a_caps(net, net.store_names("north"), 0.5)
    s1 = solve_stage1(net, caps=caps)
    assert s1.d.max() <= 50 + 1e-9 and s1.ch.max() <= 50 + 1e-9
    assert s1.cost == pytest.approx(32_500 + 100 * TIE, abs=TOL)
    r = redispatch(s1, net, "gen_only")
    assert r.cost - solve_planner(net).cost == pytest.approx(2_500, abs=TOL)


def test_s1b_marks_and_removes_e2_distortion():
    net = e2()
    s0 = solve_stage1(net)
    north = net.store_names("north")
    assert s1b_marks(net, s0, north[0], 1.0).tolist() == [True, False]   # t1 조류 250 ≥ 100
    caps = s1b_caps(net, s0, north, 1.0)
    s1 = solve_stage1(net, caps=caps)
    assert s1.d[0, 0] == pytest.approx(0)                 # 표시 시간에 방전 0
    assert s1.d[0, 1] == pytest.approx(100)               # 충전은 막지 않고, 방전은 t2로 옮김
    assert s1.cost == pytest.approx(37_500 + 100 * TIE, abs=TOL)
    assert s1.flows[0].tolist() == pytest.approx([150, 50])
    r = redispatch(s1, net, "gen_only")
    assert r.cost == pytest.approx(solve_planner(net).cost, abs=TOL)      # D = 0


def test_s1b_beta_threshold():
    net = e2()
    s0 = solve_stage1(net)
    u = net.store_names("north")[0]
    assert s1b_marks(net, s0, u, 2.5).tolist() == [True, False]     # 250 ≥ 2.5 × 100
    assert s1b_marks(net, s0, u, 2.51).tolist() == [False, False]


def test_s1x_cannot_fix_e1_undercharging_distortion():
    # E1의 왜곡은 북쪽 저장이 "덜 충전"해서 생김. 방전·충전 상한을 거는 S1a는 줄이지 못하고 오히려 늘 수 있음 (IMPL 2.6 연구 메모)
    net = e1()
    c6 = solve_planner(net).cost
    d0 = redispatch(solve_stage1(net), net, "gen_only").cost - c6
    caps = s1a_caps(net, net.store_names("north"), 0.5)
    d1a = redispatch(solve_stage1(net, caps=caps), net, "gen_only").cost - c6
    assert d0 == pytest.approx(5_000, abs=TOL)
    assert d1a >= d0 - TOL


def test_s5_equals_planner_and_prices_are_zonal_duals():
    net = e2()
    s5, s6 = solve_s5(net), solve_planner(net)
    assert abs(s5.cost - s6.cost) <= 1e-6 * s6.cost
    assert s5.prices.shape == (2, 2)
    assert s5.prices[1].tolist() == pytest.approx([150, 50])         # 남쪽: t1 비싼 가스, t2 싼 가스
    assert s5.prices[0, 0] == pytest.approx(0, abs=1e-6)            # 북쪽 t1: 풍력 출력제한 중 → 0
    # 쌍대 확인: 남쪽 t2 수요를 1 MWh 늘리면 비용이 남쪽 t2 가격만큼 는다
    net2 = e2()
    net2.demand[1, 1] += 1
    assert solve_planner(net2).cost - s6.cost == pytest.approx(s5.prices[1, 1], abs=1e-6)


@pytest.mark.parametrize("seed", [0, 1])
def test_design_invariants(seed):
    net = random_net(seed)
    c6 = solve_planner(net).cost
    north = net.store_names("north")
    s0 = solve_stage1(net)
    for caps in (s1a_caps(net, north, 0.5), s1b_caps(net, s0, north, 1.0)):
        r = redispatch_lo(net, "intertemporal", fixed_units=north, caps=caps)
        assert r.cost >= c6 - 1e-6 * c6                     # C(S1x) ≥ C(S6)
        plan = r.extra["plan"]
        for u, (cu, du) in caps.items():
            i = net.store_names().index(u)
            assert np.all(plan.ch[i] <= cu + 1e-6) and np.all(plan.d[i] <= du + 1e-6)
