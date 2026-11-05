"""구조층 2단계 모형(1단계 전국 시장, 재급전 i·ii·iii, 계획자 최적)을 손계산 예제 E1~E3와 불변식으로 시험한다.
예제 숫자와 풀이는 docs/notes/model_examples_KO.md에 있다.

동률 깨기: 효율 100%면 가스로 충전해 가스를 대신하는 것이 손익 0이다. 그래서 저장에 방전 1 MWh당 £0.01의 아주 작은
가변비용을 둔다(효율은 100% 그대로). 기대값은 그만큼(방전량 × £0.01) 더한 값으로 비교하고, 허용 오차를 £2로 둔다.
"""
import numpy as np
import pytest

from gbess.system.network import Gen, Network, Store, curtailment
from gbess.system.planner import solve_planner
from gbess.system.redispatch import redispatch, redispatch_hi, redispatch_lo
from gbess.system.stage1 import solve_stage1

TIE = 0.01
TOL = 2.0


def e1():
    """03 문서 6.3. 구역 N(0), S(1), 경계 100 MW, 두 시간."""
    return Network(
        zones=["N", "S"], demand=[[50, 50], [200, 200]], limits=[100],
        gens=[Gen("wind_N", 0, 300, 0.0, avail=[1.0, 0.0], renewable=True), Gen("gas_S", 1, 10_000, 100.0)],
        stores=[Store("ldes_N", 0, 100, 100, 100, soc0=0.0, var_cost=TIE, tags=frozenset({"w1", "north"}))],
        terminal=None)


def test_e1_stage1_national_market():
    s1 = solve_stage1(e1())
    assert s1.p[1].sum() == pytest.approx(200)            # 가스 200 MWh
    assert s1.cost == pytest.approx(20_000 + 50 * TIE, abs=TOL)
    assert s1.ch[0, 0] == pytest.approx(50)                # t1 충전 50
    assert s1.flows[0, 0] == pytest.approx(200)            # 암묵적 경계 조류 200 > 한도 100
    assert s1.prices[1] == pytest.approx(100)              # t2 전국 가격 = 가스


def test_e1_planner_optimum():
    net = e1()
    s6 = solve_planner(net)
    assert s6.cost == pytest.approx(25_000 + 100 * TIE, abs=TOL)
    assert s6.flows[0, 0] == pytest.approx(100)
    assert s6.ch[0, 0] == pytest.approx(100)
    assert curtailment(net, s6.p) == pytest.approx(50)


def test_e1_redispatch_variants():
    net = e1()
    s1 = solve_stage1(net)
    r_i = redispatch(s1, net, "gen_only")
    r_ii = redispatch(s1, net, "intertemporal")
    r_iii = redispatch(s1, net, "intertemporal", fixed_units=net.store_names("north"))
    c6 = solve_planner(net).cost
    assert r_i.extra["redispatch_cost"] == pytest.approx(10_000, abs=TOL)
    assert r_i.cost == pytest.approx(30_000, abs=TOL)       # 왜곡 £5,000
    assert r_ii.cost == pytest.approx(c6, abs=TOL)          # 왜곡 0
    assert r_ii.extra["redispatch_cost"] == pytest.approx(5_000, abs=TOL)
    assert r_ii.ch[0, 0] == pytest.approx(100)              # t1에 +50 충전
    assert r_ii.d[0, 1] == pytest.approx(100)               # t2에 +50 방전
    assert r_iii.cost == pytest.approx(r_i.cost, abs=TOL)   # 이 예의 저장은 W1 북쪽 → (i)과 같음, D_W1 = £5,000
    assert r_iii.cost - c6 == pytest.approx(5_000, abs=TOL)


def e2():
    """북쪽 저장이 1단계에서 방전해 경계 조류를 늘리는 예. 북쪽 저장은 가득 찬 채 시작."""
    return Network(
        zones=["N", "S"], demand=[[50, 50], [500, 150]], limits=[100],
        gens=[Gen("wind_N", 0, 200, 0.0, avail=[1.0, 0.0], renewable=True),
              Gen("gas_cheap_S", 1, 200, 50.0), Gen("gas_dear_S", 1, 10_000, 150.0)],
        stores=[Store("ldes_N", 0, 100, 100, 100, soc0=1.0, var_cost=TIE, tags=frozenset({"w1", "north"}))],
        terminal=None)


def test_e2_north_discharge_raises_flow():
    net = e2()
    s1 = solve_stage1(net)
    assert s1.d[0, 0] == pytest.approx(100)                # 전국 가격이 높은 t1에 다 방전
    assert s1.cost == pytest.approx(27_500 + 100 * TIE, abs=TOL)
    assert s1.flows[0, 0] == pytest.approx(250)            # 200 + 100 − 50
    s6 = solve_planner(net)
    assert s6.cost == pytest.approx(45_000 + 100 * TIE, abs=TOL)
    assert s6.d[0, 1] == pytest.approx(100)                # 계획자는 t2에 방전
    r_i = redispatch(s1, net, "gen_only")
    assert r_i.cost == pytest.approx(50_000 + 100 * TIE, abs=TOL)   # 왜곡 £5,000
    assert r_i.extra["redispatch_cost"] == pytest.approx(22_500, abs=TOL)
    r_ii = redispatch(s1, net, "intertemporal")
    assert r_ii.cost == pytest.approx(s6.cost, abs=TOL)


def e3():
    """1단계 해가 여럿인 예: 같은 저장이 북·남에 하나씩. 한 시간."""
    return Network(
        zones=["N", "S"], demand=[[50], [200]], limits=[100],
        gens=[Gen("wind_N", 0, 200, 0.0, renewable=True), Gen("gas_S", 1, 10_000, 100.0)],
        stores=[Store("st_N", 0, 50, 50, 50, soc0=1.0, var_cost=TIE, tags=frozenset({"w1", "north"})),
                Store("st_S", 1, 50, 50, 50, soc0=1.0, var_cost=TIE)],
        terminal=None)


def test_e3_degenerate_stage1_gives_range():
    net = e3()
    lo = redispatch_lo(net, "gen_only")
    hi = redispatch_hi(net, "gen_only", extreme_units=net.store_names("north"))
    c6 = solve_planner(net).cost
    assert lo.extra["plan"].d[1, 0] == pytest.approx(50)   # D_lo 계획: 남쪽 저장이 방전
    assert lo.cost - c6 == pytest.approx(0, abs=TOL)
    assert hi.extra["plan"].d[0, 0] == pytest.approx(50)   # D_hi 계획: 북쪽 저장이 방전
    assert hi.cost - c6 == pytest.approx(5_000, abs=TOL)
    assert lo.cost - c6 < hi.cost - c6


# ---------------------------------------------------------------------------------------------------------------
def random_net(seed=0, T=48, Z=3):
    rng = np.random.default_rng(seed)
    wind = np.clip(rng.normal(0.5, 0.3, (Z, T)), 0, 1)
    gens = [Gen(f"wind_{z}", z, [3000, 1500, 2000][z], 0.0, avail=wind[z], renewable=True) for z in range(Z)]
    gens += [Gen("gas_S", Z - 1, 20_000, 80.0), Gen("peak_S", Z - 1, 20_000, 200.0), Gen("gas_M", 1, 800, 90.0)]
    stores = [Store("ldes_N", 0, 500, 500, 8000, 0.9, 0.9, tags=frozenset({"w1", "north"})),
              Store("bess_M", 1, 300, 300, 600, 0.95, 0.95),
              Store("ldes_S", Z - 1, 400, 400, 6000, 0.88, 0.88, tags=frozenset({"w1"}))]
    demand = np.vstack([500 + 100 * rng.random(T), 1500 + 300 * rng.random(T), 5000 + 1500 * rng.random(T)])
    return Network([f"z{z}" for z in range(Z)], demand, [1200, 2500], gens, stores)


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_invariants(seed):
    net = random_net(seed)
    s1 = solve_stage1(net)
    s6 = solve_planner(net)
    north = net.store_names("north")
    r_i = redispatch(s1, net, "gen_only")
    r_ii = redispatch(s1, net, "intertemporal")
    r_iii = redispatch(s1, net, "intertemporal", fixed_units=north)
    tol = 1e-6 * s6.cost
    # 비용 순서와 (ii) = S6
    assert s6.cost <= r_ii.cost + tol <= r_iii.cost + 2 * tol <= r_i.cost + 3 * tol
    assert abs(r_ii.cost - s6.cost) <= tol
    assert s1.cost <= s6.cost + tol
    for r in (s6, r_i, r_ii, r_iii):
        # 경계 조류 ≤ 한도, 사슬 조류 = 구역 순공급 누적
        assert np.all(np.abs(r.flows) <= net.limits + 1e-6)
        from gbess.system.network import implicit_flows
        assert np.allclose(implicit_flows(net, r.p, r.ch, r.d, r.shed), r.flows, atol=1e-5)
        # 저장량 범위, 동시 충방전 없음
        E = np.array([s.e_mwh for s in net.stores])[:, None]
        assert np.all(r.e >= -1e-6) and np.all(r.e <= E + 1e-6)
        assert np.minimum(r.ch, r.d).max() < 1e-4
    # 전국 수지 (1단계)
    supply = s1.p.sum(0) + s1.d.sum(0) - s1.ch.sum(0) + s1.shed.sum(0)
    assert np.allclose(supply, net.demand.sum(0), atol=1e-6)
    # 재급전 (i)은 저장을 1단계 그대로, (iii)은 W1 북쪽만 그대로
    assert np.allclose(r_i.ch, s1.ch) and np.allclose(r_i.d, s1.d)
    i = net.store_names().index(north[0])
    assert np.allclose(r_iii.d[i], s1.d[i]) and np.allclose(r_iii.ch[i], s1.ch[i])
    # D_lo ≤ 기본 계획의 D ≤ ... 그리고 D_lo ≤ D_hi
    lo = redispatch_lo(net, "intertemporal", fixed_units=north, c1=s1.cost)
    hi = redispatch_hi(net, "intertemporal", extreme_units=north, fixed_units=north, c1=s1.cost)
    assert lo.cost <= r_iii.cost + tol
    assert lo.cost <= hi.cost + tol
    assert lo.extra["stage1_cost"] <= s1.cost * (1 + 1e-6) + 1e-6


def e4():
    """묶은 저장 때문에 발전기만으로는 풀 수 없는 예. 한 시간. 북쪽에 수요·발전 없이 저장 150 MW만 있음."""
    return Network(
        zones=["N", "S"], demand=[[0], [300]], limits=[100],
        gens=[Gen("gas_S", 1, 10_000, 100.0)],
        stores=[Store("ldes_N", 0, 150, 150, 150, soc0=1.0, var_cost=TIE, tags=frozenset({"w1", "north"}))],
        terminal=None)


def test_e4_fixed_storage_infeasible_unless_deviation_allowed():
    net = e4()
    s1 = solve_stage1(net)
    assert s1.d[0, 0] == pytest.approx(150) and s1.flows[0, 0] == pytest.approx(150)
    with pytest.raises(RuntimeError):
        redispatch(s1, net, "gen_only")                     # spec 문구 그대로(strict)면 풀 수 없음
    r = redispatch(s1, net, "gen_only", infeasible="min_deviation")
    assert r.extra["fixed_deviation_mwh"] == pytest.approx(50)   # 방전을 100으로 줄이는 것이 최소 이탈
    assert r.d[0, 0] == pytest.approx(100)
    assert r.extra["redispatch_cost"] == pytest.approx(5_000, abs=TOL)
    # 묶을 수 있는 예에서는 min_deviation = strict
    n1 = e1()
    p1 = solve_stage1(n1)
    a, b = redispatch(p1, n1, "gen_only"), redispatch(p1, n1, "gen_only", infeasible="min_deviation")
    assert b.extra["fixed_deviation_mwh"] == pytest.approx(0, abs=1e-6)
    assert a.cost == pytest.approx(b.cost, abs=1e-3)
    lo = redispatch_lo(net, "gen_only", infeasible="min_deviation")
    assert lo.extra["fixed_deviation_mwh"] == pytest.approx(50, abs=1e-3)   # 1단계 비용 허용 오차 안에서 조금 움직임
