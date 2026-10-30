"""기술·비용 입력(gbess.finance.costs)을 손계산 사례로 시험한다."""
import numpy as np
import pytest

from gbess.finance.cap_floor import evaluate
from gbess.finance.costs import CASES, load_assets, project_costs, table, to_base

TOY = {"toy": {
    "capex_power": {"central": 100.0, "currency": "GBP", "year": 2025, "status": "sourced", "source": "t"},
    "capex_energy": {"central": 50.0, "currency": "GBP", "year": 2025, "status": "sourced", "source": "t",
                     "high": {"value": 80.0, "currency": "GBP", "year": 2025, "status": "sourced", "source": "h"}},
    "devex_grid": {"central": 10.0, "currency": "GBP", "year": 2025, "status": "sourced", "source": "t"},
    "fixed_om_power": {"central": 2.0, "currency": "GBP", "year": 2025, "status": "sourced", "source": "t"},
    "fixed_om_energy": {"central": 0.5, "currency": "GBP", "year": 2025, "status": "sourced", "source": "t"},
    "var_om": {"central": 1.0, "currency": "GBP", "year": 2025, "status": "sourced", "source": "t"},
    "life_years": {"central": 40, "status": "sourced", "source": "t"},
    "build_years": {"central": 1, "status": "sourced", "source": "t"},
    "idc_rate": {"central": 0.0, "status": "placeholder", "source": "t"},
    "augmentation_years": {"central": 5, "status": "sourced", "source": "t"},
    "augmentation_cost": {"central": 20.0, "currency": "GBP", "year": 2025, "status": "sourced", "source": "t"},
    "fade_per_cycle": {"central": 1e-4, "status": "sourced", "source": "t"},
    "fade_calendar": {"central": 0.01, "status": "sourced", "source": "t"},
    "ref_cycles_per_year": {"central": 100, "status": "sourced", "source": "t"},
    "energy_cost_trend": {"central": 0.0, "status": "sourced", "source": "t"},
    "replacements": [{"year": 10, "part": "power", "share": 0.3, "status": "sourced", "source": "t"}],
}}


def test_to_base_converts_fx_then_cpih():
    assert to_base(100, "GBP", 2025) == pytest.approx(100)
    assert to_base(100, "GBP", 2019) == pytest.approx(100 * 138.0 / 107.8)
    assert to_base(124.34, "USD", 2023) == pytest.approx(100 * 138.0 / 128.6)   # £1 = $1.2434 (2023 연평균)


def test_toy_project_by_hand():
    c = project_costs("toy", 10, 4, costs=TOY)   # 10 MW = 10,000 kW, 40,000 kWh
    kw, kwh = 1e4, 4e4
    assert c.capex == pytest.approx(100 * kw + 50 * kwh + 10 * kw)   # 이자율 0이면 IDC 없음
    assert c.opex == pytest.approx(2 * kw + 0.5 * kwh)
    fade5 = (0.01 + 1e-4 * 100) * 5 * kwh * 20   # 5년마다 줄어든 kWh × 보강 단가
    expect = np.zeros(25)
    expect[[4, 9, 14, 19]] = fade5
    expect[9] += 0.3 * 100 * kw                  # 10년째 출력 부분 30% 교체
    assert np.allclose(c.repex, expect)
    assert c.residual_value == pytest.approx((c.capex + expect.sum()) * 15 / 40)
    assert c.var_cost == pytest.approx(1.0 + 1e-4 * 20 * 1e3)
    assert c.placeholders == ("idc_rate",)


def test_case_override_and_cycle_switch():
    hi = project_costs("toy", 10, 4, case="high", costs=TOY)
    assert hi.capex == pytest.approx(100 * 1e4 + 80 * 4e4 + 10 * 1e4)
    no_cyc = project_costs("toy", 10, 4, cycles_per_year=0, costs=TOY)   # 엔진 var_cost가 사이클 열화를 낸 경우
    assert no_cyc.repex[4] == pytest.approx(0.01 * 5 * 4e4 * 20)


def test_idc_compounds_over_build_years():
    spec = {"toy": {**TOY["toy"], "build_years": {"central": 2, "status": "sourced"},
                    "idc_rate": {"central": 0.05, "status": "sourced"}}}
    c = project_costs("toy", 10, 4, costs=spec)
    base = 100 * 1e4 + 50 * 4e4 + 10 * 1e4
    assert c.capex == pytest.approx(base * (1.05 ** 0.5 + 1.05 ** 1.5) / 2)


def test_every_representative_asset_has_sources_and_ordered_cases():
    t = table()
    assert set(t["asset"]) == set(load_assets())
    for a, g in t.groupby("asset"):
        cap = g.set_index("case")["capex_per_kw"]
        assert cap["low"] <= cap["central"] <= cap["high"], a
    for name, (tech, p, d) in load_assets().items():
        for cs in CASES:
            c = project_costs(tech, p, d, case=cs)
            assert all(c.sources.values()), (name, cs)   # 쓴 값마다 출처가 있다


def test_costs_feed_cap_floor():
    c = project_costs("psh", 1440, 22.3)
    f = evaluate(np.zeros(25), c.capex, c.opex, repex=c.repex, residual_value=c.residual_value)["floor_level"]
    r = evaluate(np.full(25, f), c.capex, c.opex, repex=c.repex, residual_value=c.residual_value)
    assert r["irr_real"] == pytest.approx(0.0447, abs=1e-6)
