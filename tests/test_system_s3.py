"""M3c + S3 (gbess.system.s3, redispatch free_hours)를 손계산 예제로 시험한다."""
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from gbess.system.network import Gen, Network, Store
from gbess.system.planner import solve_planner
from gbess.system.redispatch import redispatch, redispatch_lo
from gbess.system.s3 import bind_hours, extra_year_row, instructed_mwh, ranking, revenue_floor, summarize, year_row

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


def seq_plan(ch, d, e):
    """순차 재급전용 손 계획(물 가치 0: 남은 에너지에 값이 없음)."""
    ch, d, e = (np.atleast_2d(np.asarray(x, float)) for x in (ch, d, e))
    return SimpleNamespace(ch=ch, d=d, e=e, cost=0.0,
                           extra={"water_value": np.zeros_like(ch), "water_value_end": np.zeros(len(ch))})


def test_sequential_fixed_and_free_hours_by_hand():
    """두 시간 예(위)를 순차판으로. 계획: 두 시간 모두 충전 30, 물 가치 0.
    묶음(순차판 iii): 시간마다 가스 50 × £100 + 정전 20 × £17,000 = £345,000 → £690,000 (묶음 이탈 0, 정전을 고름).
    S3 순차판(시간 0만 풂): 시간 0 충전 0 → 가스 40 × 100 = £4,000, 시간 1 £345,000 → £349,000.
    모두 풂(기존 순차 재급전): 충전 0 → £8,000. 연말 저장량 차이는 물 가치 0이라 정산 0."""
    net = two_hours()
    plan = seq_plan([30, 30], [0, 0], [30, 60])
    tied = redispatch(plan, net, "sequential", ["ldes_N"])
    assert tied.cost == pytest.approx(690_000, abs=TOL)
    assert tied.extra["fixed_deviation_mwh"] == pytest.approx(0, abs=1e-6)
    one = redispatch(plan, net, "sequential", ["ldes_N"], free_hours=[True, False])
    assert one.cost == pytest.approx(349_000, abs=TOL)
    assert one.ch[0].tolist() == pytest.approx([0, 30], abs=1e-6)
    assert redispatch(plan, net, "sequential").cost == pytest.approx(8_000, abs=TOL)


def test_sequential_fixed_needs_deviation_by_hand():
    """한 시간. 북쪽 수요 10, 수출 한도 50, 묶은 방전 계획 80 → 북쪽에서 쓸 수 있는 건 60뿐이라 이탈 20이 꼭 필요.
    이탈량 최소(20) 뒤 비용 최소: 방전 60, 남쪽 가스 100 − 50 = 50 → £5,000."""
    net = Network(zones=["N", "S"], demand=[[10], [100]], limits=[50], gens=[Gen("gas_S", 1, 10_000, 100.0)],
                  stores=[Store("ldes_N", 0, 100, 100, 100, soc0=1.0)], terminal=None)
    r = redispatch(seq_plan([0], [80], [20]), net, "sequential", ["ldes_N"])
    assert r.extra["fixed_deviation_mwh"] == pytest.approx(20, abs=1e-4)
    assert r.d[0, 0] == pytest.approx(60, abs=1e-4)
    assert r.cost == pytest.approx(5_000, abs=TOL)


def test_min_instruction_by_hand():
    """E1 (test_system_model). 1단계 계획: t1 충전 50, t2 방전 50 (하나뿐). 계획자 최적: t1 충전 100, t2 방전 100.
    두 시간 다 풂: 계획이 하나라면 최소 지시량 = |100 − 50| + |100 − 50| = 100 MWh. 다만 1단계 계획은 C1 × (1 + 1e-6)
    (C1 ≈ £20,000 → 여유 £0.02) 안에서 함께 고르므로, t1 가스로 2 MWh 더 충전하고 t2에 2 MWh 더 방전하는 계획(추가 비용
    2 × TIE £0.01 = £0.02)도 된다 → 지시량 |100 − 52| × 2 = 96 MWh. 비용 = 계획자 최적.
    t1만 풂(t2는 방전 50에 묶임): t1 충전 50~100 모두 같은 비용(남는 에너지는 쓸 데 없음) → 최소 지시량 0."""
    from tests.test_system_model import e1
    net = e1()
    both = redispatch_lo(net, "intertemporal", ["ldes_N"], free_hours=[True, True], min_instruction=True)
    assert both.extra["instructed_min_mwh"] == pytest.approx(96, abs=1e-3)
    assert instructed_mwh(both.extra["plan"], both, [0]) == pytest.approx(96, abs=1e-3)
    assert both.cost == pytest.approx(solve_planner(net).cost, abs=TOL)
    one = redispatch_lo(net, "intertemporal", ["ldes_N"], free_hours=[True, False], min_instruction=True)
    assert one.extra["instructed_min_mwh"] == pytest.approx(0, abs=1e-3)
    assert instructed_mwh(one.extra["plan"], one, [0]) == pytest.approx(0, abs=1e-3)
    ref = redispatch_lo(net, "intertemporal", ["ldes_N"], free_hours=[True, False])
    assert one.cost == pytest.approx(ref.cost, abs=TOL)


def test_extra_year_row_by_hand():
    """D(S0) 40, D(S3) 15 → 완전예측 효과 25. 순차판 iii 300, S3 240 → 순차판 효과 60, 늘 풂(기존 D_seq) 230 → S3 − 늘 풂 10.
    지시량: D_lo 판 8 TWh(= 8,000 GWh), 최소 6 TWh → 비율 0.75."""
    s3_row = {"D_S0": 40.0, "D_S3": 15.0, "instructed_gwh_S3": 8_000.0}
    seq = pd.DataFrame([dict(case="seq_iii", D=300.0, shed_mwh=5.0, fixed_deviation_mwh=1.0, instructed_mwh=1e5),
                        dict(case="seq_S3", D=240.0, shed_mwh=0.0, fixed_deviation_mwh=2e6, instructed_mwh=9e6)])
    mn = pd.DataFrame([dict(case="D_lo_min_instruction", D=15.0, instructed_mwh=6e6)])
    r = extra_year_row(s3_row, seq, mn, 230.0)
    assert r["foresight_gain_S3"] == pytest.approx(25) and r["seq_gain_S3"] == pytest.approx(60)
    assert r["seq_S3_minus_all_free"] == pytest.approx(10) and r["instructed_twh_seq_S3"] == pytest.approx(9)
    assert r["instructed_min_twh_S3"] == pytest.approx(6) and r["instructed_min_share"] == pytest.approx(0.75)
    assert "D_seq_iii" not in extra_year_row(s3_row, None, None, 230.0)


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
