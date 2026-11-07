"""M1 지표(소비자 지급, cap-and-floor 1년 근사, E_bind)와 실행 틀을 손계산 예제로 시험한다."""
import json

import numpy as np
import pytest

from gbess.system.designs import solve_s5
from gbess.system.network import Dispatch
from gbess.system.run_m1 import (e_bind, floor_cap_levels, payments_national, payments_zonal, run_m1,
                                 settle_cap_floor)
from gbess.system.stage1 import solve_stage1
from tests.test_system_model import e1, e2, random_net


def disp(p, ch, d):
    z = np.zeros((2, 2))
    return Dispatch(np.array(p, float), np.array(ch, float), np.array(d, float), z, z, 0.0, z, None, "", 0.0)


def test_cap_floor_one_year_settlement():
    lv = {"a": (100.0, 150.0), "b": (100.0, 150.0), "c": (100.0, 150.0)}
    top, claw = settle_cap_floor({"a": 60.0, "b": 200.0, "c": 120.0}, lv)
    assert top == {"a": 40.0, "b": 0.0, "c": 0.0}
    assert claw == pytest.approx({"a": 0.0, "b": 35.0, "c": 0.0})    # 0.70 × (200 − 150)


def test_payments_national_e1_variant_i():
    # E1 재급전 (i): 1단계 가스 [0, 200] → 최종 가스 [100, 200], 풍력 [300, 0] → [200, 0]. λ = [100, 100]로 둠
    net = e1()
    plan = disp([[300, 0], [0, 200]], [[50, 0]], [[0, 50]])
    final = disp([[200, 0], [100, 200]], [[50, 0]], [[0, 50]])
    pay = payments_national(net, np.array([100.0, 100.0]), plan, final, ["ldes_N"], {"ldes_N": (1_000.0, 2_000.0)})
    assert pay["wholesale"] == pytest.approx(100 * 250 * 2)              # 50,000
    assert pay["redispatch_payment"] == pytest.approx(10_000)            # 가스 +100 × £100
    assert pay["operator_revenue"]["ldes_N"] == pytest.approx(0)         # −50×100 + 50×100
    assert pay["floor_topup"] == pytest.approx(1_000)
    assert pay["consumer_payment"] == pytest.approx(61_000)


def test_payments_zonal_e2_s5():
    # 구역 가격: S [150, 50], N [0, 50]. 도매 = N 2,500 + S 82,500. 저장 수익 = 50 × 100. 혼잡 수입 = (150 − 0) × 100
    net = e2()
    s5 = solve_s5(net)
    pay = payments_zonal(net, s5, ["ldes_N"], {"ldes_N": (10_000.0, 20_000.0)})
    assert s5.prices[0].tolist() == pytest.approx([0, 50], abs=1e-6)
    assert pay["wholesale"] == pytest.approx(85_000, abs=1)
    assert pay["operator_revenue"]["ldes_N"] == pytest.approx(5_000, abs=1)
    assert pay["congestion_rent"] == pytest.approx(15_000, abs=1)
    assert pay["floor_topup"] == pytest.approx(5_000, abs=1)
    # 소비자 지급 = 발전 수입 + 저장 수입 + 혼잡 수입 (돈이 새지 않음)
    gas = 200 * 150 + 200 * 150 + 100 * 50
    assert pay["wholesale"] == pytest.approx(gas + 5_000 + 15_000, abs=1)


def test_e_bind_e2():
    net = e2()
    s0 = solve_stage1(net)
    assert e_bind(net, s0, ["ldes_N"], [0]) == pytest.approx(100 / 1e6)   # t1 조류 250 ≥ 100, 방전 100 MWh


def test_floor_levels_match_cost_table():
    lv = floor_cap_levels([("li8", "Li-ion BESS", 400, 8), ("psh", "PSH", 1440, 22.3)])
    assert lv["li8"][0] / 400 / 1e3 == pytest.approx(108, rel=0.01)     # 09 문서 4.4: 리튬 8h central floor £108k/MW
    assert lv["psh"][0] / 1440 / 1e3 == pytest.approx(186, rel=0.01)    # 양수 22h £186k/MW
    assert lv["li8"][1] > lv["li8"][0]


def test_run_m1_smoke(tmp_path):
    net = random_net(0, T=24)
    north = net.store_names("north")
    rows = run_m1(net, north, net.store_names("w1"), {u: (1e5, 2e5) for u in net.store_names("w1")}, [0, 1],
                  tmp_path, limit_mults=(1.0,), log=lambda *a: None)
    rec = json.loads((tmp_path / "run.json").read_text())
    assert rec["spec_sha256"] and (tmp_path / "results.csv").exists()
    c = {(r["design"], r["variant"], r.get("plan")): r["system_cost"] for r in rows}
    c6 = c[("S6", "-", None)]
    tol = 1e-6 * c6
    assert abs(c[("S5", "-", None)] - c6) <= tol
    s0 = {v: c[("S0", v, "first_solve")] for v in ("i", "ii", "iii")}
    assert c6 - tol <= s0["ii"] <= s0["iii"] + tol <= s0["i"] + 2 * tol
    assert c[("S0", "iii", "D_lo")] <= c[("S0", "iii", "D_hi_approx")] + tol
    for d in ("S1a", "S1b"):
        assert c[(d, "iii", "D_lo")] >= c6 - tol


def test_zone_of_reference_points():
    from gbess.system.inputs import zone_of
    assert zone_of(57.48, -4.22) == "N"      # Inverness
    assert zone_of(56.46, -2.97) == "N"      # Dundee (SSEN 배전 지역)
    assert zone_of(55.95, -3.19) == "S"      # Edinburgh
    assert zone_of(55.86, -4.25) == "S"      # Glasgow
    assert zone_of(54.89, -2.93) == "EW"     # Carlisle
    assert zone_of(51.51, -0.13) == "EW"     # London
    assert zone_of(54.60, -5.93) is None     # Belfast


def test_power_curve_and_hub_height():
    from gbess.system.inputs import power_curve, wind_cf
    v = np.array([2.9, 3.0, 7.75, 12.5, 24.9, 25.0])
    p = power_curve(v, 3.0, 12.5, 25.0)
    assert p.tolist() == pytest.approx([0, 0, (7.75**3 - 27) / (12.5**3 - 27), 1, 1, 0])
    # 육상 허브 100 m: 100 m 풍속 그대로, 손실 0.90
    assert wind_cf(np.array([12.5]), np.array([0.1]), "onshore")[0] == pytest.approx(0.90)


def test_zone_demand_scales_to_annual_totals(tmp_path):
    from gbess.system.inputs import zone_demand
    import pandas as pd
    n = 8760 * 2
    # 스코틀랜드 몫 0.2(앞 절반)·0.1(뒤 절반): 정상 범위 안이라 오류 칸 정제(clean_ew)에 걸리지 않음
    pd.DataFrame({"ND": np.full(n, 30.0), "ENGLAND_WALES_DEMAND": np.r_[np.full(n // 2, 24.0), np.full(n // 2, 27.0)],
                  "EMBEDDED_WIND_GENERATION": np.zeros(n), "EMBEDDED_SOLAR_GENERATION": np.zeros(n)}
                 ).to_csv(tmp_path / "d.csv", index=False)
    d = zone_demand({"N": 7.0, "S": 17.0, "EW": 235.0}, ["N", "S", "EW"], tmp_path / "d.csv")
    assert d.sum(axis=1).tolist() == pytest.approx([7e3, 17e3, 235e3])
    assert d[2, 0] < d[2, -1]                # EW 모양 그대로 (뒤 절반이 큼)
    assert d[0, 0] > d[0, -1]                # 스코틀랜드 = ND − EW (앞 절반이 큼)


def test_demand_shapes_regional_split_by_hand(tmp_path):
    from gbess.system.inputs import EMB_SCOT_SOLAR_SHARE, EMB_SCOT_WIND_SHARE, demand_shapes
    import pandas as pd
    # 30분 두 구간이 같은 값: ND 100, E&W 90, 배전망 풍력 20, 태양광 10
    # 스코틀랜드 = 10 + 0.445 × 20 + 0.045 × 10 = 19.35, EW = 130 − 19.35 = 110.65
    n = 8760 * 2
    pd.DataFrame({"ND": np.full(n, 100.0), "ENGLAND_WALES_DEMAND": np.full(n, 90.0),
                  "EMBEDDED_WIND_GENERATION": np.full(n, 20.0), "EMBEDDED_SOLAR_GENERATION": np.full(n, 10.0)}
                 ).to_csv(tmp_path / "d.csv", index=False)
    ew, sc = demand_shapes(tmp_path / "d.csv")
    assert EMB_SCOT_WIND_SHARE == 0.445 and EMB_SCOT_SOLAR_SHARE == 0.045
    assert sc[0] == pytest.approx(19.35) and ew[0] == pytest.approx(110.65)
    ew0, sc0 = demand_shapes(tmp_path / "d.csv", underlying=False)       # 이전 2013 판: ND 그대로
    assert (ew0[0], sc0[0]) == (90.0, 10.0)


def test_scale_scot_onshore():
    from gbess.system.inputs import scale_scot_onshore
    cf = {"onshore_wind": np.array([[0.4, 1.0], [0.3, 0.2], [0.5, 0.5]])}
    scale_scot_onshore(cf, ["N", "S", "EW"], k=0.5)
    assert cf["onshore_wind"].tolist() == [[0.2, 0.5], [0.15, 0.1], [0.5, 0.5]]   # N·S만 바뀜


def test_marginal_cost_hand_calc():
    from gbess.system.fleet import load_cfg, marginal_cost
    fc, _ = load_cfg()
    # CCGT: 26.02/0.53 + 92.15 × 0.203/0.53 + 2.372
    assert marginal_cost(fc["thermal"]["ccgt"], fc["fuel"]) == pytest.approx(26.02 / 0.53 + 92.15 * 0.203 / 0.53 + 2.372)
    assert marginal_cost(fc["thermal"]["nuclear"], fc["fuel"]) == pytest.approx(6.768)


def _fake_rows(m, c6, d_lo, d_s1a, e_bind=0.1):
    """한도 배율 m에서 C(S6) = c6, C(S0,iii,D_lo) = c6 + d_lo, C(S1a,iii,D_lo) = c6 + d_s1a (£)."""
    import pandas as pd
    r = [("S6", "-", "-", c6), ("S5", "-", "-", c6), ("S0", "i", "first_solve", c6 + 2 * d_lo),
         ("S0", "ii", "first_solve", c6), ("S0", "iii", "first_solve", c6 + d_lo), ("S0", "iii", "D_lo", c6 + d_lo),
         ("S0", "iii", "D_hi_approx", c6 + d_lo), ("S1a", "iii", "D_lo", c6 + d_s1a)]
    return pd.DataFrame([{"design": a, "variant": b, "plan": p, "system_cost": c, "limit_mult": m,
                          "E_bind_twh": e_bind if (a, b, p) == ("S0", "i", "first_solve") else None} for a, b, p, c in r])


def test_go_no_go_rule_cases():
    import pandas as pd
    from gbess.system.run_m1 import check_invariants, go_no_go_values
    M = 25e6
    go = pd.concat([_fake_rows(0.8, 1e9, 100e6, 60e6), _fake_rows(1.0, 1e9, 80e6, 50e6), _fake_rows(1.2, 1e9, 30e6, 20e6)])
    assert check_invariants(go) == []
    assert go_no_go_values(go)["rule_result"] == "go"            # D_lo(×1.0) 80 ≥ 75, D_lo(×1.2) 30 ≥ 25, S1a가 줄임
    nogo = pd.concat([_fake_rows(0.8, 1e9, 20e6, 10e6), _fake_rows(1.0, 1e9, 10e6, 5e6), _fake_rows(1.2, 1e9, 5e6, 2e6)])
    assert go_no_go_values(nogo)["rule_result"] == "no_go"
    cond = pd.concat([_fake_rows(0.8, 1e9, 60e6, 30e6), _fake_rows(1.0, 1e9, 50e6, 30e6), _fake_rows(1.2, 1e9, 30e6, 20e6)])
    assert go_no_go_values(cond)["rule_result"] == "conditional"   # 25 ≤ 50 < 75
    assert go_no_go_values(cond)["M_gbp_m"] == M / 1e6
    assert "계산 불가" in go_no_go_values(_fake_rows(1.0, 1e9, 80e6, 50e6))["rule_result"]


def test_invariant_violation_detected():
    from gbess.system.run_m1 import check_invariants
    bad = _fake_rows(1.0, 1e9, 80e6, -5e6)                          # C(S1a) < C(S6) → 버그
    assert any("C_S1a >= C_S6" in str(b) for b in check_invariants(bad))


def test_invariants_with_negative_system_cost():
    # 인터커넥터 판: 수출 수입으로 C(S6) = −£4bn. 관계가 모두 맞으면 위반 없음(허용오차는 |C(S6)| 기준)
    from gbess.system.run_m1 import check_invariants
    assert check_invariants(_fake_rows(1.0, -4e9, 70e6, 40e6)) == []
    assert any("C_S1a >= C_S6" in str(b) for b in check_invariants(_fake_rows(1.0, -4e9, 70e6, -5e6)))


def test_collect_split_runs(tmp_path):
    from gbess.system.run_m1 import check_invariants, collect
    net = random_net(1, T=24)
    north, w1 = net.store_names("north"), net.store_names("w1")
    for d in ("S0", "S1a"):
        run_m1(net, north, w1, {u: (1e5, 2e5) for u in w1}, [0, 1], tmp_path / f"x1.0_{d}", limit_mults=(1.0,),
               log=lambda *a: None, lo_variants=("iii",), designs=(d,))
    df = collect(tmp_path)
    assert (df["design"] == "S6").sum() == 1 and set(df["design"]) == {"S6", "S5", "S0", "S1a"}
    assert check_invariants(df) == []


def test_underlying_demand_shape(tmp_path):
    from gbess.system.inputs import demand_shapes
    import pandas as pd
    n = 8760 * 2
    pd.DataFrame({"ND": np.full(n, 100.0), "ENGLAND_WALES_DEMAND": np.full(n, 90.0),
                  "EMBEDDED_WIND_GENERATION": np.full(n, 5.0), "EMBEDDED_SOLAR_GENERATION": np.full(n, 15.0)}
                 ).to_csv(tmp_path / "d.csv", index=False)
    ew, sc = demand_shapes(tmp_path / "d.csv", underlying=False)
    assert ew[0] == pytest.approx(90) and sc[0] == pytest.approx(10)
    ew, sc = demand_shapes(tmp_path / "d.csv", underlying=True)     # GB 120을 EW/ND = 0.9로 나눔
    assert ew[0] == pytest.approx(108) and sc[0] == pytest.approx(12)


def test_clean_ew_by_hand():
    from gbess.system.inputs import clean_ew
    # ND 100씩, EW 90·0·88·90 → 스코틀랜드 몫 0.10·1.0·0.12·0.10. 둘째 칸(EW = 0)은 오류 → 몫을 0.10과 0.12 사이로 이어 0.11, EW 89
    ew, bad = clean_ew([100, 100, 100, 100], [90, 0, 88, 90])
    assert bad.tolist() == [False, True, False, False] and ew.tolist() == pytest.approx([90, 89, 88, 90])
    # EW > ND(몫 −0.05)와 몫 0.30(> 0.25)도 오류. 끝 칸은 가장 가까운 정상 칸 몫(0.10)으로
    ew, bad = clean_ew([100, 100, 100], [105, 90, 70])
    assert bad.tolist() == [True, False, True] and ew.tolist() == pytest.approx([90, 90, 90])
    # 오류가 없으면 그대로
    ew, bad = clean_ew([100, 200], [90, 180])
    assert not bad.any() and ew.tolist() == [90, 180]
