"""M2 검증 코드의 손계산 시험: gbess.system.observed, backcast의 순수 함수, era5_ncar 변환."""
import numpy as np
import pandas as pd
import pytest

from gbess.system import backcast as bc
from gbess.system import era5_ncar as en
from gbess.system import observed as ob


def _frame(flow, limit, freq="h"):
    idx = pd.date_range("2025-01-01", periods=len(flow), freq=freq, tz="UTC")
    return pd.DataFrame({"flow": flow, "limit": limit}, index=idx)


def test_binding_and_exceedance_by_hand():
    # 4시간: 조류 5, 10, 12, 3 / 한도 10 → 제약 2시간(10 ≥ 10, 12 ≥ 10), 초과 0 + 0 + 2 + 0 = 2 MWh
    s = ob.binding_stats(_frame([5, 10, 12, 3], [10] * 4))
    assert s["binding"] == pytest.approx(0.5)
    assert s["exceed_mwh"] == pytest.approx(2.0)
    # 30분 자료면 초과량에 0.5시간을 곱함
    s = ob.binding_stats(_frame([12, 12], [10, 10], freq="30min"))
    assert s["exceed_mwh"] == pytest.approx(2.0)


def test_joint_exceedance_takes_hourly_max():
    h4 = _frame([12, 5, 9], [10, 10, 10])      # 초과 2, 0, 0
    h6 = _frame([11, 13, 9], [10, 10, 10])     # 초과 1, 3, 0
    j = ob.joint_exceedance(h4, h6)
    assert list(j) == [2, 3, 0]                # 시간마다 큰 값. 합 5 (연간 합끼리의 큰 값 = 4와 다름)


def test_hourly_mean_of_half_hours():
    f = _frame([10, 20, 30, 50], [15, 15, 40, 40], freq="30min")
    h = ob.hourly(f)
    assert list(h["flow"]) == [15, 40] and list(h["limit"]) == [15, 40]


def test_localize_dst_fall_back():
    # 2025-10-26 01:00, 01:30이 두 번(BST, GMT) → UTC 00:00, 00:30, 01:00, 01:30
    t = pd.Series(["2025-10-26T00:30:00", "2025-10-26T01:00:00", "2025-10-26T01:30:00", "2025-10-26T01:00:00",
                   "2025-10-26T01:30:00", "2025-10-26T02:00:00"])
    u = ob._localize(t)
    want = pd.to_datetime(["2025-10-25 23:30", "2025-10-26 00:00", "2025-10-26 00:30", "2025-10-26 01:00",
                           "2025-10-26 01:30", "2025-10-26 02:00"]).tz_localize("UTC")
    assert list(u) == list(want)


def test_bid_share_in_binding():
    idx = pd.date_range("2025-01-01", periods=4, freq="30min", tz="UTC")
    down = pd.Series([10.0, 0.0, 30.0, 60.0], index=idx)
    bind = pd.Series([1.0, 1.0, 0.0, np.nan], index=idx)        # 마지막 구간은 제약 여부 모름 → 뺌
    share, base, lift = ob.bid_share_in_binding(down, bind)
    assert share == pytest.approx(10 / 40)
    assert base == pytest.approx(2 / 3)
    assert lift == pytest.approx((10 / 40) / (2 / 3))


def test_daily_spread_top_bottom_k():
    # 현지 하루 24시간 가격 0, 1, …, 23 (겨울이라 UTC = 현지). k = 4: (20+21+22+23)/4 − (0+1+2+3)/4 = 20
    idx = pd.date_range("2025-01-15", periods=24, freq="h", tz="UTC")
    s = ob.daily_spread(pd.Series(np.arange(24.0), index=idx), 4)
    assert s.iloc[0] == pytest.approx(20.0)


def test_logit_recovers_breakeven():
    # P(순환) = σ((x − 30)/5) 에서 많이 뽑으면 손익분기 −a/b ≈ 30
    rng = np.random.default_rng(1)
    x = rng.uniform(0, 60, 20000)
    y = (rng.uniform(size=x.size) < 1 / (1 + np.exp(-(x - 30) / 5))).astype(float)
    assert ob.breakeven(x, y) == pytest.approx(30.0, abs=0.5)


def test_v3_verdict_rules():
    assert ob.v3_verdict(5.0, -1.0, 9.0, 9.2) == "inconclusive"   # 90% 구간이 0을 포함
    assert ob.v3_verdict(8.0, 3.0, 13.0, 9.2) == "pass"           # 비율 0.87
    assert ob.v3_verdict(30.0, 25.0, 35.0, 9.2) == "fail"         # 비율 3.3, 예측이 구간 밖
    assert ob.v3_verdict(-8.0, -12.0, -3.0, 9.2) == "fail"        # 부호 틀림


def test_price_metrics_by_hand():
    # 이틀: 첫날 상위8 − 하위8 = 16 (0..23), 둘째 날 모두 −1 → 0. 중앙값 8, 가격 ≤ 0 시간 = (1 + 24)/48
    idx = pd.date_range("2025-01-15", periods=48, freq="h", tz="UTC")
    p = pd.Series(np.r_[np.arange(24.0), -np.ones(24)], index=idx)
    m = ob.price_metrics(p, k=8)
    assert m["spread_median"] == pytest.approx(8.0)
    assert m["nonpositive_share"] == pytest.approx(25 / 48)


def test_sp_to_utc_bst():
    # 여름(BST): 정산일 2025-07-01 구간 1 = 현지 00:00 = UTC 전날 23:00. 구간 3 = UTC 00:00
    u = bc.sp_to_utc(pd.Series(["2025-07-01", "2025-07-01"]), [1, 3])
    assert list(u) == list(pd.to_datetime(["2025-06-30 23:00", "2025-07-01 00:00"]).tz_localize("UTC"))


def test_zone_demand_and_interconnectors():
    h = pd.DataFrame({"ND": [100.0], "ENGLAND_WALES_DEMAND": [90.0], "EMBEDDED_WIND_GENERATION": [6.0],
                      "EMBEDDED_SOLAR_GENERATION": [4.0], **{c: [0.0] for c in bc.IC_COLUMNS}})
    h["MOYLE_FLOW"] = -3.0
    h["IFA_FLOW"] = 7.0
    d = bc.zone_demand_2025(h, ["N", "S", "EW"], {"N": 0.25, "S": 0.75})
    # 실제 소비 110, 스코틀랜드 몫 0.1 → 11 (N 2.75, S 8.25), EW 99
    assert d[:, 0] == pytest.approx([2.75, 8.25, 99.0])
    inj = bc.interconnector_injection(h, ["N", "S", "EW"])
    assert inj[:, 0] == pytest.approx([0.0, -3.0, 7.0])


def test_era5_convert_and_indices():
    v = en.convert(np.array([3.0]), np.array([4.0]), np.array([0.1]))
    assert v["wnd100m"][0] == pytest.approx(5.0) and v["roughness"][0] == pytest.approx(0.1)
    lon = np.arange(0, 360, 0.25)
    lo = en.lon_index(lon)
    assert lon[lo[0]] == pytest.approx(346.5) and lon[lo[-1]] == pytest.approx(1.75) and len(lo) == 62
    lat = np.arange(90, -90.001, -0.25)
    li = en.lat_index(lat)
    assert lat[li[0]] == pytest.approx(60.75) and lat[li[-1]] == pytest.approx(50.0) and len(li) == 44


def test_embedded_split_by_hand():
    # ND 100, E&W 90 → 스코틀랜드 송전 수요 10. 배전망 풍력 20, 태양광 10. 몫 0.5, 0.1 → 스코틀랜드 10 + 10 + 1 = 21
    # 실제 소비 130 → EW 109. N:S = 1:3 → N 5.25, S 15.75
    h = pd.DataFrame({"ND": [100.0], "ENGLAND_WALES_DEMAND": [90.0], "EMBEDDED_WIND_GENERATION": [20.0],
                      "EMBEDDED_SOLAR_GENERATION": [10.0]})
    d = bc.zone_demand_embedded_split(h, ["N", "S", "EW"], {"N": 0.25, "S": 0.75}, 0.5, 0.1)
    assert d[:, 0] == pytest.approx([5.25, 15.75, 109.0])
    assert d[:, 0].sum() == pytest.approx(130.0)


# --- V5 보류 표본 (gbess.system.holdout) ---
from gbess.system import holdout as ho


def test_window_hours_and_shift():
    h = ho.window_hours("2025-11-06", "2025-11-08")
    assert len(h) == 48 and h[0] == pd.Timestamp("2025-11-06", tz="UTC")
    assert ho.shift_year("2026-11-06", "2027-05-06") == ("2025-11-06", "2026-05-06")


def test_guard_blocks_window_before_it_ends():
    with pytest.raises(RuntimeError):
        ho.guard("2026-11-06", "2027-05-06", today="2026-11-06")
    ho.guard("2026-11-06", "2027-05-06", today="2027-05-06")        # 창이 끝난 뒤에는 읽음
    ho.guard("2025-11-06", "2026-05-06", today="2026-11-06")        # no-peek 날짜 전 자료는 언제나 읽음


def test_v5_metrics_and_table_by_hand():
    # B4: 조류 5, 12 / 한도 10 → 제약 1/2, 초과 0, 2. B6: 조류 11, 9 / 한도 10 → 제약 1/2, 초과 1, 0
    # 큰 쪽 초과량: max(0,1) + max(2,0) = 3 MWh
    m = ho.metrics({"B4": _frame([5, 12], [10, 10]), "B6": _frame([11, 9], [10, 10])})
    assert m == pytest.approx({"B4_binding": 0.5, "B6_binding": 0.5, "exceed_twh": 3e-6})
    spec = {"binding_tol_abs": 0.10, "exceedance_ratio_band": [0.65, 1.35]}
    t = ho.v5_table({"B6_binding": 0.30, "B4_binding": 0.50, "exceed_twh": 4.0},
                    {"B6_binding": 0.35, "B4_binding": 0.38, "exceed_twh": 3.0},
                    {"B6_binding": 0.40, "B4_binding": 0.40, "exceed_twh": 3.3}, spec).set_index("metric")
    assert bool(t.loc["V5 B6 제약 발생 비율", "pass"])                    # |0.30 − 0.35| = 0.05 ≤ 0.10
    assert not bool(t.loc["V5 B4 제약 발생 비율", "pass"])                # 0.12 > 0.10
    assert t.loc["V5 B4·B6 큰 쪽 초과량 TWh", "ratio"] == pytest.approx(4 / 3)
    assert bool(t.loc["V5 B4·B6 큰 쪽 초과량 TWh", "pass"])               # 1.33 ≤ 1.35
    assert t.loc["V5 B4·B6 큰 쪽 초과량 TWh", "persistence_abs_err"] == pytest.approx(0.3)


# --- 인터커넥터 가격 수용 민감도 (gbess.system.interconnectors) ---
from gbess.system import interconnectors as icx


def test_fuel_index_by_hand():
    assert icx.srmc(5.3, 0.0) == pytest.approx(10.0)                         # 5.3 ÷ 0.53
    assert icx.srmc(0.0, 100.0, eff=0.5, ef=0.2) == pytest.approx(40.0)      # 100 × 0.2 ÷ 0.5
    # $3.178/MMBtu ÷ 1.141 $/€ ÷ 0.293071 MWh/MMBtu ÷ 0.90 = €10.56/MWh LHV
    assert icx.gas_2020_eur_mwh_lhv() == pytest.approx(10.56, abs=0.01)
    assert sum(mw for *_, mw in icx.LINKS_2030) == 11700                    # FES BB Gen_BB022 HT 2030


def test_price_taking_link_imports_cheap_exports_dear():
    from gbess.system.network import Gen, Network
    from gbess.system.stage1 import solve_stage1
    # 남쪽 수요 10, 발전기 £50·20 MW, 링크 ±5 MW (해외 £30, £80)
    # 1시간: 수입 5 @30 + 발전 5 @50 = 400.  2시간: 발전 15 @50 − 수출 5 @80 = 350.  합 750
    gens = [Gen("g", 1, 20.0, 50.0), Gen("ic", 1, 5.0, np.array([30.0, 80.0]), None, False, -5.0)]
    net = Network(["N", "S"], [[0.0, 0.0], [10.0, 10.0]], [100.0], gens, [])
    r = solve_stage1(net)
    assert r.cost == pytest.approx(750.0)
    assert r.p[1] == pytest.approx([5.0, -5.0]) and r.p[0] == pytest.approx([5.0, 15.0])
