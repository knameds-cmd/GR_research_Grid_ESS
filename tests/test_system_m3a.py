"""M3a 요약 코드의 손계산 시험 (gbess.system.m3a)."""
import pandas as pd
import pytest

from gbess.system import m3a


def test_label_and_jobs():
    assert m3a.label(2013, 1.0, "S0") == "x1.0_S0"
    assert m3a.label(2015, 0.8, "S0") == "w2015_x0.8_S0"
    j = m3a.jobs([2015])
    # 한 해에 S0 ×0.8·×1.0·×1.2, S1a·S1b ×1.0, 순차 재급전 1개 = 6개
    assert len(j) == 6 and "--label w2015_x1.0_S1b" in j[4] and "f((1.0,), 2015)" in j[5]


def test_ranking_ties_by_hand():
    # S0 100, S1a 90, S1b 90.05: S1a와 S1b의 차이 0.05 < 0.1 → 같은 순위 0, S0은 세 번째(순위 2)
    row = {"system_cost_S0": 100.0, "system_cost_S1a": 90.0, "system_cost_S1b": 90.05}
    assert m3a.ranking(row, "system_cost") == (2, 0, 0)
    assert m3a.ranking({"system_cost_S0": 1.0}, "system_cost") is None


def _df():
    # 한도 ×1.0 한 판, £: S6 100m, S0 (i) 150m, (ii) 100m, (iii) 첫 풀이 130m, D_lo 120m, D_hi 140m, S1a D_lo 110m, S1b D_lo 125m
    r = []
    def add(d, v, p, cost, **kw):
        r.append({"design": d, "variant": v, "plan": p, "limit_mult": 1.0, "system_cost": cost * 1e6,
                  "consumer_payment": cost * 2e6, "curtailment_mwh": 1e6, "E_bind_twh": kw.get("e")})
    add("S6", "-", "-", 100); add("S5", "-", "-", 100)
    add("S0", "i", "first_solve", 150, e=0.5); add("S0", "ii", "first_solve", 100); add("S0", "iii", "first_solve", 130)
    add("S0", "iii", "D_lo", 120); add("S0", "iii", "D_hi_approx", 140)
    add("S1a", "iii", "D_lo", 110); add("S1b", "iii", "D_lo", 125)
    return pd.DataFrame(r)


def test_year_row_by_hand():
    seq = pd.DataFrame({"limit_mult": [1.0, 1.0], "fleet": ["with_W1N", "without_W1N"], "D_seq": [30.0, 12.0]})
    row = m3a.year_row(_df(), seq)
    # D_lo = 120 − 100 = 20, D_hi = 140 − 100 = 40, C(S0) − C(S1a) = 120 − 110 = 10, C(S0) − C(S1b) = −5
    assert row["D_lo_x1.0"] == pytest.approx(20) and row["D_hi_x1.0"] == pytest.approx(40)
    assert row["C_S0_minus_C_S1a"] == pytest.approx(10) and row["C_S0_minus_C_S1b"] == pytest.approx(-5)
    assert row["E_bind_twh"] == pytest.approx(0.5) and row["consumer_payment_S1b"] == pytest.approx(250)
    # D_seq 30, W1 북쪽 몫 30 − 12 = 18. 검산 위반 없음
    assert row["D_seq_x1.0"] == 30 and row["D_seq_W1N_share_x1.0"] == 18 and row["invariant_violations"] == 0


def test_summarize_by_hand():
    def r(d, s0, s1a, s1b, bad=0):
        return {"D_lo_x1.0": d, "system_cost_S0": s0, "system_cost_S1a": s1a, "system_cost_S1b": s1b,
                "consumer_payment_S0": 1.0, "consumer_payment_S1a": 1.0, "consumer_payment_S1b": 1.0, "invariant_violations": bad}
    rows = {2013: r(30, 100, 90, 95), 2014: r(10, 100, 90, 95), 2015: r(80, 100, 110, 95, bad=1)}
    df, out = m3a.summarize(rows, M=25.0)
    # D_lo 10·30·80: 중앙 30, ≥ 25는 2개, ≥ 75는 1개
    assert out["D_lo_x1.0"] == {"median": 30.0, "min": 10.0, "max": 80.0, "n": 3}
    assert out["years_D_lo_x1.0_ge_M"] == 2 and out["years_D_lo_x1.0_ge_3M"] == 1
    # 2013 순위 (S0, S1a, S1b) = (2, 0, 1). 2015는 (1, 2, 0)으로 뒤집힘. 소비자 지급은 셋 다 같아 (0, 0, 0)으로 모두 유지
    assert out["rank_system_cost"] == {"reference_2013": (2, 0, 1), "same_as_2013": 2, "n": 3, "flipped_years": [2015]}
    assert out["rank_consumer_payment"]["same_as_2013"] == 3
    assert out["invariant_broken_years"] == [2015]
