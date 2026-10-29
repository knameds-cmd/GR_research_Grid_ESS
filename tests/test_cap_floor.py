"""cap-and-floor 재무층을 손계산 사례로 시험한다."""
import numpy as np
import pytest

from gbess.finance.cap_floor import Regime, annuity, evaluate, irr

CAPEX, OPEX = 1000.0, 10.0
F = annuity(CAPEX, 0.0447, 25) + OPEX
C = annuity(CAPEX, 0.0748, 25) + OPEX


def test_annuity_recovers_capital_at_rate():
    a = annuity(1000, 0.05, 25)
    pv = sum(a / 1.05 ** t for t in range(1, 26))
    assert pv == pytest.approx(1000)


def test_irr_of_floor_equals_floor_rate():
    # 수익이 정확히 floor 수준이면 사업자 실질 IRR = floor 수익률
    r = evaluate(np.full(25, F), CAPEX, OPEX)
    assert r["irr_real"] == pytest.approx(0.0447, abs=1e-6)
    assert r["consumer_cost_pv"] == pytest.approx(0)


def test_zero_revenue_topped_up_to_floor():
    r = evaluate(np.zeros(25), CAPEX, OPEX)
    assert r["irr_real"] == pytest.approx(0.0447, abs=1e-6)
    assert r["floor_triggered_periods"] == 5
    assert r["topup"].sum() > 25 * F   # 묶음 끝에 몰아 받는 만큼 이자가 붙는다


def test_merchant_zero_revenue_loses_everything():
    r = evaluate(np.zeros(25), CAPEX, OPEX, regime=Regime(enabled=False))
    assert np.isnan(r["irr_real"])   # 현금흐름이 모두 음수
    assert r["topup"].sum() == 0


def test_above_cap_70pct_returned_next_year():
    rev = np.full(25, C + 100.0)
    r = evaluate(rev, CAPEX, OPEX)
    g = 1.0447 ** np.arange(5, 0, -1)          # 묶음 다음 해 지급 시점까지 환산
    assert r["payback"][6] == pytest.approx(0.7 * 100 * g.sum())
    assert r["payback"][:6].sum() == 0         # 묶음 안의 해에는 지급 없음
    assert r["payback"].sum() == pytest.approx(0.7 * 100 * g.sum() * 5)
    assert abs(r["trueup"]).sum() == pytest.approx(0, abs=1e-6)   # 묶음마다 같으면 최종 정산 없음
    assert r["consumer_cost_pv"] < 0   # 소비자가 돌려받음


def test_between_floor_and_cap_untouched():
    rev = np.full(25, (F + C) / 2)
    r = evaluate(rev, CAPEX, OPEX)
    assert r["topup"].sum() == 0 and r["payback"].sum() == 0 and r["trueup"].sum() == 0


def test_five_year_netting():
    # 한 해 크게 모자라도 같은 5년 묶음의 다른 해가 메우면 보전 없음
    rev = np.full(25, F + 10.0)
    rev[4] = F - 40.0
    r = evaluate(rev, CAPEX, OPEX)
    assert r["topup"].sum() == 0
    r1 = evaluate(rev, CAPEX, OPEX, regime=Regime(assessment_years=1), carry_over=False)
    assert r1["topup"][6] == pytest.approx(40.0 * 1.0447)   # 5년차 부족분, 6년차 지급


def test_carry_over_claws_back_interim_topup():
    # 1년 정산을 고른 사업자: 5년차 보전을 받지만 25년 전체로는 floor 위라 마지막에 되돌려 낸다 (NPV 중립)
    rev = np.full(25, F + 10.0)
    rev[4] = F - 40.0
    r = evaluate(rev, CAPEX, OPEX, regime=Regime(assessment_years=1))
    assert r["topup"][6] == pytest.approx(40.0 * 1.0447)
    assert r["trueup"][26] == pytest.approx(-40.0 * 1.0447 ** 21)
    pv = np.sum((r["topup"] - r["payback"] + r["trueup"]) / 1.0447 ** np.arange(27))
    assert pv == pytest.approx(0, abs=1e-6)


def test_unavailable_year_loses_floor():
    avail = np.ones(25, bool)
    avail[2] = False
    r = evaluate(np.zeros(25), CAPEX, OPEX, available=avail)
    g = 1.0447 ** np.arange(5, 0, -1)
    assert r["topup"][6] == pytest.approx(F * (g.sum() - g[2]))


def test_unavailable_year_counts_only_revenue_above_floor():
    # 미달 해에 floor보다 30 많이 벌었으면, floor 쪽 비교에는 30만 들어간다 (TDD p50–51)
    avail = np.ones(25, bool)
    avail[2] = False
    rev = np.zeros(25)
    rev[2] = F + 30.0
    r = evaluate(rev, CAPEX, OPEX, available=avail, carry_over=False)
    g = 1.0447 ** np.arange(5, 0, -1)
    assert r["topup"][6] == pytest.approx(F * (g.sum() - g[2]) - 30.0 * g[2])


def test_cycling_cost_lowers_assessed_revenue():
    rev = np.full(25, F)
    r = evaluate(rev, CAPEX, OPEX, cycling_cost=5.0)
    g = 1.0447 ** np.arange(5, 0, -1)
    assert r["topup"][6] == pytest.approx(5.0 * g.sum())


def test_irr_defined_when_cap_payback_comes_after_last_year():
    # 늘 cap 위인 수익: 마지막 묶음의 환수가 n+1년에 와서 현금흐름 부호가 두 번 바뀐다. IRR은 머천트보다 낮고 cap 수익률 근처
    R = np.full(25, 1.2e5)
    r = evaluate(R, 1e6, 2e4)
    merchant = irr(np.r_[-1e6, R - 2e4])
    assert r["investor_cf"][-1] < 0
    assert 0.0748 - 0.01 < r["irr_real"] < merchant
