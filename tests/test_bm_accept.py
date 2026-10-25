"""BM 채택 모형의 부품을 시험한다: 가중 분위수, 분수 로짓이 알려진 관계를 되찾는지, 방향별 설계 행렬의 부호."""
import numpy as np
import pandas as pd
import pytest

from gbess.data.bm_state import wquantile
from gbess.model.bm_accept import FracLogit, design


def test_weighted_quantile():
    v = np.array([10.0, 20.0, 30.0])
    assert wquantile(v, np.array([1.0, 1.0, 8.0]), 0.9) == 30.0
    assert wquantile(v, np.array([8.0, 1.0, 1.0]), 0.5) == 10.0


def test_frac_logit_recovers_known_relation():
    rng = np.random.default_rng(0)
    n = 20000
    x = rng.normal(size=n)
    p = 1 / (1 + np.exp(-(-2.0 + 1.5 * x)))
    y = rng.binomial(20, p) / 20                    # 분수 결과 (0~1)
    m = FracLogit(C=1e6).fit(pd.DataFrame({"x": x}), y, np.ones(n))
    assert m.coefs()["x"] == pytest.approx(1.5, abs=0.05)


def _panel_row(**kw):
    base = dict(t=pd.Timestamp("2024-01-01 12:00", tz="UTC"), head_up_mw=100.0, head_dn_mw=100.0,
                offer_price=80.0, bid_price=20.0, mid=50.0, niv_mwh=100.0, wind_mw=5000.0, wind_ramp_mw=0.0,
                gen_ramp_mw=0.0, ew_offer_p90=100.0, ew_bid_p10=10.0, sc_bid_p10=np.nan, ew_offer_mwh=500.0,
                sc_offer_mwh=0.0, ew_bid_mwh=300.0, sc_bid_mwh=0.0, sc_wind_bid_mwh=0.0, scotland=False,
                offer_mwh=10.0, bid_mwh=0.0, unit_mw=100.0, fpn_mw=0.0)
    return pd.DataFrame([{**base, **kw}])


def test_design_signs_and_target():
    X, y, w, ok = design(_panel_row(), "offer")
    assert X["comp"].iat[0] == pytest.approx(-0.2)       # 자기 단가 80 − 한계 100 = −£20 → /100
    assert X["markup"].iat[0] == pytest.approx(0.3)
    assert y[0] == pytest.approx(10 / (100 * 0.5)) and w[0] == 100
    X, y, w, ok = design(_panel_row(), "bid")
    assert X["comp"].iat[0] == pytest.approx(0.1)        # bid 20 − 한계 10: NESO에 더 유리 → 양수
    assert X["niv"].iat[0] == pytest.approx(-0.1)        # 계통이 모자람(NIV +) → bid 쪽 신호는 음수
    assert X["comp_sc"].iat[0] == 0                       # 스코틀랜드가 아니면 스코틀랜드 항은 0


def test_design_drops_small_headroom():
    X, y, w, ok = design(_panel_row(head_up_mw=2.0), "offer")
    assert len(X) == 0 and not ok.iat[0]
