"""엔진을 손계산 사례와 불변식으로 시험한다."""
import numpy as np
import pandas as pd
import pytest

from gbess.engine.asset import Asset, load_technologies
from gbess.engine.dispatch import DT, solve, summarise


def prices(vals):
    return pd.Series(vals, index=pd.date_range("2026-01-01", periods=len(vals), freq="30min", tz="UTC"),
                     dtype=float)


def toy(**kw):
    base = dict(name="toy", p_dis_mw=1, p_ch_mw=1, e_mwh=0.5, eta_ch=1.0, eta_dis=1.0, soc_init=0.0)
    return Asset(**{**base, **kw})


def test_buy_low_sell_high():
    out, info = solve(prices([10, 100]), toy())
    assert out["charge_mw"].tolist() == pytest.approx([1, 0])
    assert out["discharge_mw"].tolist() == pytest.approx([0, 1])
    assert summarise(out, toy())["margin_gbp"] == pytest.approx((100 - 10) * 0.5)


def test_losses_kill_small_spread():
    # 왕복효율 81%: 12 × 0.81 = 9.72 < 10 이므로 거래하지 않는다
    a = toy(eta_ch=0.9, eta_dis=0.9)
    out, _ = solve(prices([10, 12]), a)
    assert out["net_mw"].abs().sum() == pytest.approx(0, abs=1e-9)


def test_negative_price_no_simultaneous():
    a = toy(eta_ch=0.9, eta_dis=0.9, e_mwh=10)
    out, info = solve(prices([-50] * 4 + [20] * 4), a)
    assert info["binary_periods"] == 4
    assert summarise(out, a)["simultaneous_periods"] == 0


def test_integer_pumping_units():
    a = toy(p_ch_mw=2, p_dis_mw=2, e_mwh=10, pump_units=2)
    out, _ = solve(prices([5, 30, 6, 80, 7, 90]), a)
    assert set(np.round(out["charge_mw"], 6)) <= {0.0, 1.0, 2.0}


def test_energy_balance_invariant():
    rng = np.random.default_rng(0)
    a = toy(eta_ch=0.92, eta_dis=0.93, e_mwh=4, soc_init=0.5, self_discharge_per_h=0.001)
    p = prices(rng.normal(60, 40, 48 * 7))
    out, info = solve(p, a)
    s_prev = np.r_[a.soc_init * a.e_mwh, out["soc_mwh"].to_numpy()[:-1]]
    rhs = s_prev * (1 - a.self_discharge_per_h * DT) + DT * (a.eta_ch * out["charge_mw"] - out["discharge_mw"] / a.eta_dis)
    assert np.allclose(out["soc_mwh"], rhs, atol=1e-6)
    assert out["soc_mwh"].iat[-1] >= a.soc_init * a.e_mwh - 1e-6
    assert info["optimal"]


def test_placeholders_reported():
    tech = load_technologies()
    out, info = solve(prices([10, 100]), tech["li_ion"])
    assert "eta_ch" in info["placeholders"]
    assert set(tech) >= {"li_ion", "psh", "caes_laes", "flow"}


def test_reserve_headroom_caps_discharge_and_keeps_energy():
    a = toy(p_dis_mw=10, p_ch_mw=10, e_mwh=20, soc_init=0.5)
    out, _ = solve(prices([10, 200, 10, 200]), a, reserve_up_mw=4, reserve_hours=1.0)
    assert out["discharge_mw"].max() <= 6 + 1e-9
    assert out["soc_mwh"].min() >= 4 - 1e-9
