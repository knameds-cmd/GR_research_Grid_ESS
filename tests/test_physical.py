"""손으로 답을 계산할 수 있는 사례로 출력 복원을 시험한다."""
import pandas as pd
import pytest

from gbess.realized.physical import sp_energy

START, END = pd.Timestamp("2026-01-01T00:00Z"), pd.Timestamp("2026-01-01T02:00Z")


def seg(t0, t1, l0, l1, **kw):
    return {"bmUnit": "U", "timeFrom": t0, "timeTo": t1, "levelFrom": l0, "levelTo": l1, **kw}


def test_flat_pn_only():
    pn = pd.DataFrame([seg("2026-01-01T00:00Z", "2026-01-01T02:00Z", 100, 100)])
    e = sp_energy(pn, pd.DataFrame(columns=["bmUnit"]), START, END)
    assert len(e) == 4
    assert e["pn_mwh"].tolist() == pytest.approx([50, 50, 50, 50])
    assert e["boa_mwh"].abs().sum() == pytest.approx(0)


def test_ramp_energy_is_trapezoid():
    # 0 → 60 MW를 30분에 걸쳐 올리면 에너지는 (0+60)/2 × 0.5h = 15 MWh
    pn = pd.DataFrame([seg("2026-01-01T00:00Z", "2026-01-01T00:30Z", 0, 60)])
    e = sp_energy(pn, pd.DataFrame(columns=["bmUnit"]), START, END)
    assert e["pn_mwh"].iat[0] == pytest.approx(15)


def test_later_acceptance_overrides_earlier():
    pn = pd.DataFrame([seg("2026-01-01T00:00Z", "2026-01-01T02:00Z", 0, 0)])
    boalf = pd.DataFrame([
        # 지시 1: 00:00~01:00 200 MW 발전
        seg("2026-01-01T00:00Z", "2026-01-01T01:00Z", 200, 200, acceptanceNumber=1, acceptanceTime="2025-12-31T23:50Z"),
        # 지시 2(나중): 00:30~01:00을 -100 MW 양수로 바꿈
        seg("2026-01-01T00:30Z", "2026-01-01T01:00Z", -100, -100, acceptanceNumber=2, acceptanceTime="2026-01-01T00:20Z"),
    ])
    e = sp_energy(pn, boalf, START, END)
    assert e["phys_mwh"].tolist() == pytest.approx([100, -50, 0, 0])
    assert e["boa_mwh"].tolist() == pytest.approx([100, -50, 0, 0])


def test_missing_pn_counted():
    pn = pd.DataFrame([seg("2026-01-01T00:00Z", "2026-01-01T01:00Z", 10, 10)])
    e = sp_energy(pn, pd.DataFrame(columns=["bmUnit"]), START, END)
    assert e["pn_missing_min"].tolist() == [0, 0, 30, 30]
