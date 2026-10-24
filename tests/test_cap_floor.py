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


def test_above_cap_70pct_returned():
    rev = np.full(25, C + 100.0)
    r = evaluate(rev, CAPEX, OPEX)
    g = 1.0447 ** np.arange(4, -1, -1)
    assert r["payback"].sum() == pytest.approx(0.7 * 100 * g.sum() * 5)
    assert r["consumer_cost_pv"] < 0   # 소비자가 돌려받음


def test_between_floor_and_cap_untouched():
    rev = np.full(25, (F + C) / 2)
    r = evaluate(rev, CAPEX, OPEX)
    assert r["topup"].sum() == 0 and r["payback"].sum() == 0


def test_five_year_netting():
    # 한 해 크게 모자라도 같은 5년 묶음의 다른 해가 메우면 보전 없음
    rev = np.full(25, F + 10.0)
    rev[4] = F - 40.0
    r = evaluate(rev, CAPEX, OPEX)
    assert r["topup"].sum() == 0
    r1 = evaluate(rev, CAPEX, OPEX, regime=Regime(assessment_years=1))
    assert r1["topup"].sum() == pytest.approx(40.0)


def test_unavailable_year_loses_floor():
    avail = np.ones(25, bool)
    avail[2] = False
    r = evaluate(np.zeros(25), CAPEX, OPEX, available=avail)
    g = 1.0447 ** np.arange(4, -1, -1)
    assert r["topup"][:5].sum() == pytest.approx(F * (g.sum() - g[2]))
