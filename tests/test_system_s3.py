"""M3c + S3 (gbess.system.s3, redispatch free_hours)를 손계산 예제로 시험한다."""
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from gbess.system.network import Gen, Network, Store
from gbess.system.planner import solve_planner
from gbess.system.redispatch import redispatch, redispatch_lo
from gbess.system.s3 import bind_hours, instructed_mwh, ranking, revenue_floor, summarize, year_row

TOL = 2.0


def test_bind_hours_both_directions_by_hand():
    # 한도 B4 6, B6 7. t0: 5<6, 1<7 → 아님 / t1: |−6| ≥ 6 → 제약 / t2: 아님 / t3: |−7| ≥ 7 → 제약
    flows = [[5, -6, 2, 0], [1, 1, 3, -7]]
    assert bind_hours(flows, [6, 7], [0, 1]).tolist() == [False, True, False, True]
    assert bind_hours(flows, [6, 7], [1]).tolist() == [False, False, False, True]


def test_instructed_mwh_by_hand():
    plan = SimpleNamespace(ch=np.array([[30.0, 30.0], [5.0, 0.0]]), d=np.array([[0.0, 0.0], [0.0, 4.0]]))
    final = SimpleNamespace(ch=np.array([[0.0, 30.0], [9.0, 0.0]]), d=np.array([[0.0, 0.0], [0.0, 1.0]]))
    assert instructed_mwh(plan, final, [0]) == pytest.approx(30)
    assert instructed_mwh(plan, final, [0, 1], dt=0.5) == pytest.approx((30 + 4 + 3) * 0.5)


def two_hours():
    return Network(zones=["N", "S"], demand=[[40, 40], [0, 0]], limits=[50], gens=[Gen("gas_S", 1, 10_000, 100.0)],
                   stores=[Store("ldes_N", 0, 30, 30, 100, soc0=0.0, tags=frozenset({"w1", "north"}))], terminal=None)


def test_free_hours_unties_only_marked_hours_by_hand():
    """test_system_model의 충전 정전 예를 두 시간으로. 계획: 두 시간 모두 충전 30. 북쪽 수입 한도 50.
    묶음(iii): 시간마다 수입 50 → 가스 £5,000 + 정전 20 × £17,000 = £345,000, 두 시간 £690,000.
    시간 0만 풂: 시간 0 충전 0 → 가스 40 × 100 = £4,000, 시간 1은 그대로 £345,000 → £349,000. 이탈 0 (푼 시간은 이탈이 아님).
    두 시간 다 풂 = 변형 (ii): 충전 0 → £8,000."""
    net = two_hours()
    plan = SimpleNamespace(ch=np.array([[30.0, 30.0]]), d=np.array([[0.0, 0.0]]), cost=0.0)
    tied = redispatch(plan, net, "intertemporal", ["ldes_N"], infeasible="min_deviation")
    assert tied.cost == pytest.approx(690_000, abs=TOL)
    one = redispatch(plan, net, "intertemporal", ["ldes_N"], infeasible="min_deviation", free_hours=[True, False])
    assert one.cost == pytest.approx(349_000, abs=TOL)
    assert one.ch[0].tolist() == pytest.approx([0, 30], abs=1e-5)       # 이탈량 허용 오차(DEV_TOL)만큼
    assert one.extra["fixed_deviation_mwh"] == pytest.approx(0, abs=1e-5)
    assert instructed_mwh(plan, one, [0]) == pytest.approx(30, abs=1e-5)
    both = redispatch(plan, net, "intertemporal", ["ldes_N"], infeasible="min_deviation", free_hours=[True, True])
    assert both.cost == pytest.approx(8_000, abs=TOL)
    assert redispatch(plan, net, "intertemporal", infeasible="min_deviation").cost == pytest.approx(8_000, abs=TOL)


def test_redispatch_lo_free_hours_limits():
    """D_lo 결합 LP: 모두 풀면 = 계획자 최적(변형 ii와 같음), 아무것도 안 풀면 = free_hours 없음."""
    from tests.test_system_model import e1
    net = e1()
    all_free = redispatch_lo(net, "intertemporal", ["ldes_N"], free_hours=[True, True])
    assert all_free.cost == pytest.approx(solve_planner(net).cost, abs=TOL)
    none = redispatch_lo(net, "intertemporal", ["ldes_N"], free_hours=[False, False])
    assert none.cost == pytest.approx(redispatch_lo(net, "intertemporal", ["ldes_N"]).cost, abs=1e-6)


def test_year_row_ranking_summary_by_hand():
    """£ 값(원 단위)을 손으로 만든 한 해. C(S6)=100m, S0 130m, S1a 125m, S1b 140m, S3 D_lo 110m (첫 풀이 115m)."""
    m = 1e6
    m3a = pd.DataFrame([
        dict(design="S6", variant="-", plan="-", limit_mult=1.0, system_cost=100 * m),
        dict(design="S0", variant="iii", plan="first_solve", limit_mult=1.0, system_cost=131 * m),
        *[dict(design=d, variant="iii", plan="D_lo", limit_mult=1.0, system_cost=c * m, consumer_payment=p * m,
               floor_topup=f * m) for d, c, p, f in (("S0", 130, 500, 50), ("S1a", 125, 520, 70), ("S1b", 140, 505, 55))],
    ])
    s3 = pd.DataFrame([dict(design="S3", variant="iii", plan=k, limit_mult=1.0, system_cost=c * m, consumer_payment=p * m,
                            floor_topup=60 * m, instructed_mwh=2_000, shed_mwh=0.0, fixed_deviation_mwh=0.0,
                            free_hours=300) for k, c, p in (("first_solve", 115, 510), ("D_lo", 110, 508))])
    row = year_row(m3a, s3)
    assert row["D_S3"] == pytest.approx(10) and row["D_S3_first_solve"] == pytest.approx(15)
    assert row["C_S0_minus_C_S3"] == pytest.approx(20) and row["C_S1a_minus_C_S3"] == pytest.approx(15)
    assert row["P_S0_minus_P_S3"] == pytest.approx(-8)
    assert row["floor_topup_S3_minus_S0"] == pytest.approx(10)
    assert row["instructed_gwh_S3"] == pytest.approx(2) and row["invariant_violations_S3"] == 0
    # 순위(S0, S1a, S1b, S3): 비용 110 < 125 < 130 < 140 → (2, 1, 3, 0); 지급 500 < 505 < 508 < 520 → (0, 3, 1, 2)
    assert ranking(row, "system_cost") == (2, 1, 3, 0)
    assert ranking(row, "consumer_payment") == (0, 3, 1, 2)
    # 첫 풀이 S3(115)가 S0 첫 풀이(131)보다 비싸면 검산 위반
    bad = s3.assign(system_cost=[135 * m, 110 * m])
    assert year_row(m3a, bad)["invariant_violations_S3"] == 1
    _, out = summarize({2013: row, 2014: {**row, "system_cost_S3": 126.0}}, broken_m3a=[])
    assert out["rank_system_cost"]["same_as_2013"] == 1 and out["rank_system_cost"]["flipped_years"] == [2014]
    assert out["rank_system_cost"]["S3_first_years"] == [2013]
    _, out = summarize({2013: row, 2014: row}, broken_m3a=[2014])
    assert out["not_comparable"] == [2014] and out["D_S3"]["n"] == 1


def test_revenue_floor_by_hand():
    rev = pd.DataFrame([dict(weather_year=2013, design="S0", variant="iii", limit_mult=1.0, plan="D_lo", project="A",
                             revenue=30.0, floor=100.0),
                        dict(weather_year=2013, design="S0", variant="iii", limit_mult=1.0, plan="first_solve",
                             project="A", revenue=99.0, floor=100.0),
                        dict(weather_year=2013, design="S0", variant="i", limit_mult=1.0, plan="D_lo", project="A",
                             revenue=99.0, floor=100.0)])
    r = revenue_floor(rev)
    assert len(r) == 1 and r.revenue_over_floor.iloc[0] == pytest.approx(0.3)
