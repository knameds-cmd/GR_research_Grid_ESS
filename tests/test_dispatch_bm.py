"""BM 층 엔진을 손계산 사례와 불변식으로 시험한다."""
import numpy as np
import pandas as pd
import pytest

from gbess.engine.asset import Asset
from gbess.engine.dispatch import solve, summarise
from gbess.engine.dispatch_bm import DT, solve_bm, summarise_bm


def series(vals):
    return pd.Series(vals, index=pd.date_range("2026-01-01", periods=len(vals), freq="30min", tz="UTC"), dtype=float)


def opp(n, offer=None, bid=None, po=None, pb=None):
    """offer/bid: 구간별 MW당 상한, po/pb: 단가. 주지 않으면 0 / 결측."""
    idx = series([0] * n).index
    z = np.zeros(n)
    return pd.DataFrame({"offer_mw_per_mw": z if offer is None else offer, "bid_mw_per_mw": z if bid is None else bid,
                         "offer_price": np.full(n, np.nan) if po is None else po,
                         "bid_price": np.full(n, np.nan) if pb is None else pb}, index=idx)


def toy(**kw):
    base = dict(name="toy", p_dis_mw=1, p_ch_mw=1, e_mwh=0.5, eta_ch=1.0, eta_dis=1.0, soc_init=0.0)
    return Asset(**{**base, **kw})


def test_no_bm_equals_wholesale_engine():
    rng = np.random.default_rng(1)
    p = series(rng.normal(60, 40, 96))
    a = toy(eta_ch=0.92, eta_dis=0.93, e_mwh=4, soc_init=0.5)
    out1, _ = solve(p, a)
    out2, _ = solve_bm(p, opp(96), a)
    assert summarise_bm(out2, a)["total_k_per_mw_yr"] == pytest.approx(summarise(out1, a)["margin_k_per_mw_yr"], rel=1e-6)


def test_offer_beats_wholesale_sale():
    # 가득 찬 0.5 MWh 저장장치. 도매로 팔면 £10, BM offer(£100)로 팔면 £50
    a = toy(soc_init=1.0)
    out, _ = solve_bm(series([10, 10]), opp(2, offer=[0, 1], po=[np.nan, 100]), a, terminal="value", water_value=0)
    assert out["offer_mw"].tolist() == pytest.approx([0, 1])
    assert out["offer_mw"].mul(out["offer_price"]).sum() * DT == pytest.approx(50)


def test_no_simultaneous_offer_and_bid():
    a = toy(e_mwh=10, soc_init=0.5)
    out, info = solve_bm(series([50]), opp(1, offer=[1], bid=[1], po=[100], pb=[10]), a, terminal="value",
                         water_value=50)
    assert info["offer_bid_binaries"] == 1
    assert summarise_bm(out, a)["simultaneous_offer_bid"] == 0


def test_retrade_buy_wholesale_sell_offer_needs_no_energy():
    # 빈 저장장치: 도매로 1 MW 사고(£5) 같은 양을 offer로 되팔면(£50) 실제 운전 없이 £45
    a = toy(soc_init=0.0)
    out, _ = solve_bm(series([10]), opp(1, offer=[1], po=[100]), a, terminal="value", water_value=0)
    r = summarise_bm(out, a)
    assert r["gen_mwh"] == pytest.approx(0) and r["pump_mwh"] == pytest.approx(0)
    assert out["fpn_mw"].iat[0] == pytest.approx(-1) and out["offer_mw"].iat[0] == pytest.approx(1)


def test_negative_bid_with_full_store_cannot_burn_energy():
    # 가득 찬 저장장치가 bid(−£50, 줄이면 돈을 받음)를 받으려면 FPN으로 먼저 팔아야 한다. 동시 충방전으로 태우면 안 됨
    a = toy(eta_ch=0.9, eta_dis=0.9, e_mwh=0.5, soc_init=1.0)
    out, info = solve_bm(series([20]), opp(1, bid=[1], pb=[-50]), a, terminal="value", water_value=0)
    r = summarise_bm(out, a)
    assert info["mode_binaries"] == 1
    assert r["simultaneous_charge_discharge"] == 0


def test_fpn_fixed_is_respected():
    a = toy(e_mwh=2, soc_init=0.5)
    f = np.array([1.0, -1.0, 0.0, 0.5])
    out, _ = solve_bm(series([10, 20, 30, 40]), opp(4, offer=[1] * 4, po=[50] * 4), a, fpn_fixed=f,
                      terminal="value", water_value=0)
    assert out["fpn_mw"].to_numpy() == pytest.approx(f)


def test_energy_balance_with_bm():
    rng = np.random.default_rng(2)
    n = 96
    a = toy(eta_ch=0.92, eta_dis=0.93, e_mwh=4, soc_init=0.5, p_dis_mw=2, p_ch_mw=2)
    o = opp(n, offer=rng.uniform(0, 0.5, n), bid=rng.uniform(0, 0.5, n), po=rng.normal(120, 30, n),
            pb=rng.normal(20, 30, n))
    out, info = solve_bm(series(rng.normal(60, 30, n)), o, a)
    s_prev = np.r_[a.soc_init * a.e_mwh, out["soc_mwh"].to_numpy()[:-1]]
    rhs = s_prev + DT * (a.eta_ch * out["charge_mw"] - out["discharge_mw"] / a.eta_dis)
    assert np.allclose(out["soc_mwh"], rhs, atol=1e-6)
    assert np.allclose(out["net_mw"], out["fpn_mw"] + out["offer_mw"] - out["bid_mw"], atol=1e-6)
    assert (out["offer_mw"] <= out["offer_cap"] + 1e-6).all() and (out["bid_mw"] <= out["bid_cap"] + 1e-6).all()
    assert info["optimal"]


def test_time_varying_availability():
    a = toy(p_dis_mw=10, p_ch_mw=10, e_mwh=40, soc_init=0.5, pump_units=2)
    out, _ = solve_bm(series([10, 100, 10, 100]), opp(4, offer=[1] * 4, po=[200] * 4), a,
                      p_dis_t=[10, 3, 10, 0], p_ch_t=[10, 10, 5, 10], pump_units_t=[2, 2, 1, 2])
    assert (out["discharge_mw"].to_numpy() <= np.array([10, 3, 10, 0]) + 1e-6).all()
    assert out["charge_mw"].iat[2] <= 5 + 1e-6
    assert (out["offer_cap"].to_numpy() == pytest.approx([10, 3, 10, 0]))


def test_rolling_bm_runs_and_respects_caps():
    from gbess.engine.rolling_bm import run_bm
    rng = np.random.default_rng(3)
    n = 48 * 4
    p = series(60 + 30 * np.sin(np.arange(n) / 48 * 2 * np.pi) + rng.normal(0, 5, n))
    o = opp(n, offer=rng.uniform(0, 0.3, n), bid=rng.uniform(0, 0.3, n), po=rng.normal(150, 20, n),
            pb=rng.normal(20, 10, n))
    a = toy(eta_ch=0.9, eta_dis=0.9, e_mwh=8, soc_init=0.5, p_dis_mw=1, p_ch_mw=1)
    out, meta = run_bm(p, o, a, horizon_days=2)
    assert len(out) == n
    assert (out["offer_mw"] <= out["offer_cap"] + 1e-6).all()
    assert np.allclose(out["net_mw"], out["fpn_mw"] + out["offer_mw"] - out["bid_mw"], atol=1e-6)
    assert summarise_bm(out, a)["simultaneous_offer_bid"] == 0


def test_imbalance_fallback_when_fpn_cannot_be_met():
    # 빈 저장장치에 방전 FPN을 고정하면 원래는 풀 수 없다. 벌금을 주면 불균형으로 풀고 그 양을 남긴다
    a = toy(soc_init=0.0)
    with pytest.raises(RuntimeError):
        solve_bm(series([50]), opp(1), a, fpn_fixed=[1.0], terminal="value", water_value=0)
    out, _ = solve_bm(series([50]), opp(1), a, fpn_fixed=[1.0], terminal="value", water_value=0,
                      imbalance_penalty=1000.0)
    assert out["imbalance_mw"].iat[0] == pytest.approx(-1.0)


def acc(n, ao=None, ab=None, po=None, pb=None):
    """채택 모형 방식 입력: α와 자기 단가."""
    idx = series([0] * n).index
    z = np.zeros(n)
    return pd.DataFrame({"alpha_offer": z if ao is None else ao, "alpha_bid": z if ab is None else ab,
                         "offer_price": np.full(n, np.nan) if po is None else po,
                         "bid_price": np.full(n, np.nan) if pb is None else pb}, index=idx)


def test_accept_offer_cap_is_alpha_times_headroom():
    a = toy(e_mwh=10, soc_init=0.5, p_dis_mw=2, p_ch_mw=2)
    o = acc(3, ao=[0.5] * 3, po=[200] * 3)
    out, info = solve_bm(series([10, 10, 10]), o, a, fpn_fixed=[0.0, 2.0, -2.0], terminal="value", water_value=0)
    # 여유 = 가용 출력 − FPN: 2, 0, 4 → offer 상한 1, 0, 2
    assert out["offer_mw"].to_numpy() == pytest.approx([1.0, 0.0, 2.0])
    assert info["bm_mode"] == "accept" and info["offer_bid_binaries"] == 0


def test_accept_bid_cap_is_alpha_times_headroom():
    a = toy(e_mwh=10, soc_init=0.5, p_dis_mw=2, p_ch_mw=2)
    o = acc(3, ab=[0.25] * 3, pb=[-50] * 3)    # 음의 bid: 받으면 돈을 받으므로 상한까지 받는다
    out, _ = solve_bm(series([10, 10, 10]), o, a, fpn_fixed=[2.0, 0.0, -2.0], terminal="value", water_value=0)
    # 여유 = FPN + 가용 입력: 4, 2, 0 → bid 상한 1, 0.5, 0
    assert out["bid_mw"].to_numpy() == pytest.approx([1.0, 0.5, 0.0])


def test_accept_alpha_ignored_without_own_price():
    a = toy(e_mwh=10, soc_init=0.5)
    out, _ = solve_bm(series([10]), acc(1, ao=[1.0], ab=[1.0]), a, terminal="value", water_value=0)
    assert out["offer_mw"].iat[0] == pytest.approx(0) and out["bid_mw"].iat[0] == pytest.approx(0)


def test_accept_free_fpn_trades_off_wholesale_and_headroom():
    # 도매 £50, offer £100에 α = 0.5. 꽉 찬 1 MWh 저장장치(2구간 × 1 MW)를 한 구간에 쓴다면:
    # FPN 1 MW로 팔면 £25, FPN 0으로 두고 offer 0.5 MW를 받으면 £25 + 남은 에너지. 둘 다 같은 기댓값 근처에서
    # 해가 정해지는지보다, 어떤 해든 상한(α × 여유)을 지키는지를 본다
    a = toy(e_mwh=1, soc_init=1.0, p_dis_mw=1, p_ch_mw=1)
    out, _ = solve_bm(series([50, 50]), acc(2, ao=[0.5, 0.5], po=[100, 100]), a, terminal="value", water_value=0)
    head = 1 - out["fpn_mw"]
    assert (out["offer_mw"] <= 0.5 * head + 1e-6).all()


# ---------------------------------------------------------------- 예비력 보유 (reserve_price)
def test_reserve_limited_by_stored_energy():
    # 0.5 MWh가 차 있는 1 MW 자산, 도매 가격 0, 예비력 £10/MW/h, 1시간 지속 조건.
    # 출력 여유는 1 MW지만 1시간 낼 물이 0.5 MWh뿐이라 r = 0.5. 수입 = 10 × 0.5 MW × 0.5h × 4구간 = £10
    a = toy(soc_init=1.0)
    out, _ = solve_bm(series([0, 0, 0, 0]), opp(4), a, reserve_price=10.0, reserve_hours=1.0)
    assert out["reserve_mw"].to_numpy() == pytest.approx([0.5] * 4)
    assert float((out["reserve_price"] * out["reserve_mw"]).sum() * DT) == pytest.approx(10.0)


def test_reserve_competes_with_discharge():
    # 가득 찬 4 MWh, 1 MW 자산. 구간 0 가격 £100, 예비력 £30/MW/h (지속 조건 0.5h).
    # 구간 0에 1 MW 방전하면 £50, 예비력으로 비워 두면 £15 → 방전. 나머지 구간은 가격 0이라 예비력 1 MW
    a = toy(e_mwh=4, soc_init=1.0)
    out, _ = solve_bm(series([100, 0, 0]), opp(3), a, reserve_price=30.0, reserve_hours=0.5)
    assert out["discharge_mw"].iat[0] == pytest.approx(1.0)
    assert out["reserve_mw"].to_numpy() == pytest.approx([0.0, 1.0, 1.0])
    assert (out["net_mw"] + out["reserve_mw"] <= 1.0 + 1e-6).all()


def test_reserve_fixed_is_held_and_paid():
    a = toy(e_mwh=4, soc_init=1.0)
    out, _ = solve_bm(series([100, 0, 0]), opp(3), a, reserve_price=30.0, reserve_hours=0.5,
                      reserve_fixed=[0.6, 0.6, 0.6])
    assert out["reserve_mw"].to_numpy() == pytest.approx([0.6] * 3)
    assert out["net_mw"].iat[0] == pytest.approx(0.4)                # 1 MW − 약속한 0.6 MW
    r = summarise_bm(out, a)
    assert r["reserve_k"] > 0 and r["reserve_mw_mean"] == pytest.approx(0.6)


def test_rolling_reserve_commits_day_ahead():
    from gbess.engine.rolling_bm import run_bm
    rng = np.random.default_rng(3)
    p = series(rng.normal(60, 30, 96))
    a = toy(e_mwh=4, soc_init=0.5, eta_ch=0.9, eta_dis=0.9)
    out, meta = run_bm(p, opp(96), a, horizon_days=1, reserve_price=5.0, reserve_hours=1.0)
    assert (out["net_mw"] + out["reserve_mw"] <= 1.0 + 1e-6).all()
    assert (out["soc_mwh"] + 1e-6 >= out["reserve_mw"] * 1.0 / 0.9).all()
    assert meta["reserve_price"] == 5.0 and out["reserve_mw"].mean() > 0


def test_psh_pumping_units_cannot_hold_reserve():
    # 양수형 2유닛(각 1 MW 발전, 1 MW 양수). 구간 0 가격이 아주 낮아 한 유닛 양수가 이득.
    # 양수 중인 유닛은 스핀 대기를 못 하므로 그 구간 예비력은 남은 한 유닛분(1 MW)까지만
    a = toy(p_dis_mw=2, p_ch_mw=2, e_mwh=8, soc_init=0.5, pump_units=2)
    out, _ = solve_bm(series([-50, 0, 0, 0]), opp(4), a, reserve_price=1.0, reserve_hours=0.5)
    assert out["charge_mw"].iat[0] > 0
    pumping_units = out["charge_mw"] / 1.0
    assert (out["reserve_mw"] <= 2 - pumping_units - out["discharge_mw"] + 1e-6).all()


def test_start_cost_counts_and_prices_unit_starts():
    # 양수형 2유닛. 가격이 낮음-높음-낮음-높음으로 두 번 오르내린다. 기동 비용이 없으면 두 번 다 양수·발전하고,
    # 기동 비용이 차익보다 크면 아예 돌리지 않는다. 기동 횟수 = 발전·양수 유닛이 0에서 켜진 횟수
    a = toy(p_dis_mw=2, p_ch_mw=2, e_mwh=8, soc_init=0.5, pump_units=2, eta_ch=0.9, eta_dis=0.9)
    p = series([0, 100, 0, 100])
    free, _ = solve_bm(p, opp(4), a, start_cost=0.0)
    s = summarise_bm(free, a)
    assert free["starts"].sum() == pytest.approx(free["gen_units"].clip(lower=0).diff().clip(lower=0).fillna(
        free["gen_units"].iat[0]).sum() + free["pump_units"].diff().clip(lower=0).fillna(free["pump_units"].iat[0]).sum())
    assert s["start_cost_k"] == 0 and free["gen_units"].max() > 0
    dear, _ = solve_bm(p, opp(4), a, start_cost=1e4)
    assert dear["starts"].sum() == 0 and summarise_bm(dear, a)["total_k_per_mw_yr"] >= -1e-9
    assert (dear["gen_units"] + dear["pump_units"] <= 2).all()


def test_units_cannot_generate_and_pump_beyond_unit_count():
    a = toy(p_dis_mw=2, p_ch_mw=2, e_mwh=8, soc_init=0.5, pump_units=2)
    out, _ = solve_bm(series([-50, 80, -50, 80]), opp(4), a, start_cost=0.0)
    assert (out["gen_units"] + out["pump_units"] <= 2).all()
    assert np.all(out["discharge_mw"] <= out["gen_units"] * 1.0 + 1e-6)


def test_rolling_price_known_uses_actual_day_prices():
    from gbess.engine.rolling_bm import run_bm
    rng = np.random.default_rng(5)
    p = series(rng.normal(60, 40, 96))
    a = toy(e_mwh=4, soc_init=0.5, eta_ch=0.9, eta_dis=0.9)
    f, _ = run_bm(p, opp(96), a, horizon_days=1)
    k, meta = run_bm(p, opp(96), a, horizon_days=1, info="price_known")
    assert meta["info"] == "price_known"
    assert np.allclose(k["fpn_forecast_price"], p.to_numpy())
    assert summarise_bm(k, a)["total_k_per_mw_yr"] >= summarise_bm(f, a)["total_k_per_mw_yr"] - 1e-6


def test_charges_reduce_arbitrage_and_are_reported():
    # 가격 0 → 10. 왕복 손실 없음. 방전에 £6/MWh, 충전에 £6/MWh를 매기면 차익 10 < 12라 돌리지 않는다
    a = toy(e_mwh=1, soc_init=0.0)
    p = series([0, 10])
    free, _ = solve_bm(p, opp(2), a, terminal="value", water_value=0.0)
    assert free["discharge_mw"].iat[1] > 0
    dear, _ = solve_bm(p, opp(2), a, terminal="value", water_value=0.0, charges=(np.full(2, 6.0), np.full(2, 6.0)))
    assert dear["discharge_mw"].sum() == pytest.approx(0)
    half, _ = solve_bm(p, opp(2), a, terminal="value", water_value=0.0, charges=(np.full(2, 6.0), np.zeros(2)))
    s = summarise_bm(half, a)
    assert half["discharge_mw"].iat[1] > 0
    assert s["charges_k"] == pytest.approx(-6.0 * half["discharge_mw"].sum() * DT / 1 * 8760 / (2 * DT) / 1e3)


# ---------------------------------------------------------------- 입찰 단가 띠 (가상 자산의 입찰 규칙)
def ladder_opp(n, offer_bands, bid_bands=((0.0, 0.0),)):
    """offer_bands, bid_bands: [(α, 단가), ...]. 모든 구간에 같은 띠."""
    idx = series([0] * n).index
    d = {}
    for side, bands in (("offer", offer_bands), ("bid", bid_bands)):
        for k, (al, pr) in enumerate(bands):
            d[f"alpha_{side}_{k}"], d[f"{side}_price_{k}"] = np.full(n, al), np.full(n, pr)
    return pd.DataFrame(d, index=idx)


def test_ladder_with_one_band_equals_single_alpha():
    a = toy(e_mwh=10, soc_init=0.5, p_dis_mw=2, p_ch_mw=2)
    p = series([10, 10, 10])
    one, _ = solve_bm(p, acc(3, ao=[0.5] * 3, po=[200] * 3, ab=[0.25] * 3, pb=[-50] * 3), a,
                      fpn_fixed=[0.0, 2.0, -2.0], terminal="value", water_value=0)
    lad, info = solve_bm(p, ladder_opp(3, [(0.5, 200)], [(0.25, -50)]), a, fpn_fixed=[0.0, 2.0, -2.0],
                         terminal="value", water_value=0)
    assert info["bands"] == (1, 1)
    assert lad["offer_mw"].to_numpy() == pytest.approx(one["offer_mw"].to_numpy())
    assert lad["bid_mw"].to_numpy() == pytest.approx(one["bid_mw"].to_numpy())


def test_ladder_picks_band_with_highest_expected_margin():
    # 가득 찬 저장장치, 남은 저장 에너지의 값 £50/MWh, 도매 £40(팔지 않음). 1 MW 여유를 어느 단가로 내나?
    #   띠 0: α 0.5, £60 → 0.5 × (60 − 50) = 5        띠 1: α 0.1, £200 → 0.1 × (200 − 50) = 15  → 띠 1
    # 띠 0의 단가를 £100으로 올리면 0.5 × 50 = 25 > 15 → 띠 0
    a = toy(e_mwh=10, soc_init=1.0)
    kw = dict(terminal="value", water_value=50.0)
    out, _ = solve_bm(series([40]), ladder_opp(1, [(0.5, 60), (0.1, 200)]), a, **kw)
    assert out["offer_band"].iat[0] == 1 and out["offer_mw"].iat[0] == pytest.approx(0.1)
    assert out["offer_price"].iat[0] == pytest.approx(200)
    out, _ = solve_bm(series([40]), ladder_opp(1, [(0.5, 100), (0.1, 200)]), a, **kw)
    assert out["offer_band"].iat[0] == 0 and out["offer_mw"].iat[0] == pytest.approx(0.5)
    assert summarise_bm(out, a)["bm_offer_k"] > 0


def test_ladder_headroom_is_shared_by_bands():
    # 두 띠가 같은 여유 1 MW를 나눠 쓴다: 둘 다 α = 1이면 받는 물량 합은 1 MW를 넘지 않는다
    a = toy(e_mwh=10, soc_init=1.0)
    out, info = solve_bm(series([0]), ladder_opp(1, [(1.0, 100), (1.0, 120)]), a, terminal="value", water_value=0)
    assert info["offer_mw_bands"].sum() == pytest.approx(1.0)
    assert out["offer_band"].iat[0] == 1


def test_rolling_plan_price_choice_cannot_use_realised_acceptance():
    # 과거(1~2일째)에는 띠 0(£60, α 0.5)이 낫고, 3일째에만 띠 1(£300)의 α가 0.5로 뛴다.
    # price_choice="plan"은 하루 전에 띠 0을 낸다. "realtime"은 그날 실제 α를 보고 띠 1로 바꾼다(상한)
    from gbess.engine.rolling_bm import run_bm
    n = 48 * 3
    o = ladder_opp(n, [(0.5, 60), (0.05, 300)])
    o.loc[o.index[96:], "alpha_offer_1"] = 0.5
    a = toy(e_mwh=1000, soc_init=0.5, p_dis_mw=1, p_ch_mw=1)
    p = series([20.0] * n)
    wp = pd.Series(20.0, index=pd.date_range(p.index[0] - pd.Timedelta(days=2), periods=96, freq="30min"))
    wo = ladder_opp(96, [(0.5, 60), (0.05, 300)])
    wo.index = wp.index
    plan, meta = run_bm(p, o, a, horizon_days=1, warmup_price=wp, warmup_opp=wo, price_choice="plan")
    real, _ = run_bm(p, o, a, horizon_days=1, warmup_price=wp, warmup_opp=wo, price_choice="realtime")
    assert meta["price_choice"] == "plan" and meta["bands"] == {"offer": 2, "bid": 1}
    assert (plan["offer_band"].iloc[96:] == 0).all()
    assert (real["offer_band"].iloc[96:] == 1).all()
    assert summarise_bm(real, a)["bm_offer_k"] > summarise_bm(plan, a)["bm_offer_k"]
