"""구역 선택용 경계 제약 통계를 손계산 사례로 시험한다."""
import pandas as pd
import pytest

from gbess.system.zones_analysis import binding_stats, joint_stats, to_hourly


def raw(rows):
    return pd.DataFrame(rows, columns=["time", "group", "limit", "flow"])


def test_hourly_mean_drops_placeholders_and_old_definition():
    d = raw([
        ("2024-04-30T23:00:00", "A", 100, 500),   # 2024-05-01 전 → 뺌
        ("2024-05-01T00:00:00", "A", 100, 90),
        ("2024-05-01T00:30:00", "A", 100, 130),   # 1시간 평균: 한도 100, 조류 110
        ("2024-05-01T01:00:00", "A", 9999, 50),   # 자리채움 한도 → 뺌
        ("2024-05-01T01:30:00", "A", 0, 50),      # 자리채움 한도 → 뺌
    ])
    h = to_hourly(d)
    assert len(h) == 1
    assert h.iloc[0][["limit", "flow"]].tolist() == [100, 110]


def test_binding_fraction_near_and_exceedance():
    # 네 시간: 조류/한도 = 110/100(제약, 초과 10), 96/100(근처), 50/100, 300/100(제약, 초과 200)
    h = to_hourly(raw([
        ("2025-01-01T00:00:00", "A", 100, 110),
        ("2025-01-01T01:00:00", "A", 100, 96),
        ("2025-01-01T02:00:00", "A", 100, 50),
        ("2025-01-01T03:00:00", "A", 100, 300),
    ]))
    s = binding_stats(h).iloc[0]
    assert s["hours"] == 4
    assert s["bind_frac"] == pytest.approx(0.5)
    assert s["near_frac"] == pytest.approx(0.75)
    assert s["exceed_twh"] == pytest.approx(210 / 1e6)


def test_joint_b4_b6():
    # 세 시간은 둘 다 있음. B6 제약: 1, 2시. B4 제약: 1, 3시. 큰 쪽 초과량: 1시 max(5, 20) = 20, 2시 30, 3시 7.
    # 4시에는 B4만 있음(조류 140): 비율에서는 빠지고 초과량에는 40이 더해짐 → 97 MWh
    rows = []
    for hr, (f4, f6) in enumerate([(105, 120), (90, 130), (107, 80)], start=1):
        t = f"2025-02-01T{hr:02d}:00:00"
        rows += [(t, "SSE_SP2", 100, f4), (t, "SCOTEX", 100, f6)]
    rows.append(("2025-02-01T04:00:00", "SSE_SP2", 100, 140))
    j = joint_stats(to_hourly(raw(rows))).loc[2025]
    assert j["hours"] == 3
    assert j["either_frac"] == pytest.approx(1.0)
    assert j["both_frac"] == pytest.approx(1 / 3)
    assert j["a_given_b"] == pytest.approx(0.5)
    assert j["max_exceed_twh"] == pytest.approx(97 / 1e6)
