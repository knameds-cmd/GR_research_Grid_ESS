"""
cap-and-floor 재무층 (08 문서 2장의 F형 규칙). 연 수익 경로가 주어지면 사업자 현금흐름과 소비자 부담을 계산한다.
제도 사실은 literature/sources/ldes/FACTS.md 2장 (Ofgem TDD 2025-03, Window 1 MTD 2026-06, NERA 2026).

모든 금액은 CPIH 실질 £. 정해진 대로 넣은 것과 단순화한 것:
  - floor·cap 수준 = RAV(100%)를 각 수익률로 regime_years 동안 연금화한 값 + 통제 가능 운영비. 잔존가치 0.  [TDD p56–61, MTD p37]
  - 정산은 assessment_years(기본 5년) 묶음마다: 묶음 수익 합 < floor 합이면 부족분 전액 보전,
    > cap 합이면 초과분의 share_returned(기본 70%)를 소비자에게 돌려줌.  [TDD p35, p44; NERA p7 인용 FFD]
  - 가용률 조건을 못 채운 해: 그해 floor는 0으로 본다(그해 수익은 cap 비교에는 모두 들어감).  [TDD p50–51]
  - 묶음 안의 수익·floor·cap은 npv_rate로 묶음 끝 해까지 복리 환산해 비교한다("NPV 중립", TDD p44). 할인율은 문서에
    없으므로(TDD p55 "to be defined") 기본값을 floor 수익률로 둔다. 이렇게 해야 수익 0인 사업자의 IRR이 floor 수익률과 같아진다.
  단순화(결과에 함께 기록): 묶음 사이 이월과 25년 최종 정산은 넣지 않았다.
  세금·통과비용(망요금 등)은 넣지 않았다. "수익"은 에너지 구입비를 뺀 거래 마진으로 본다(Ofgem은 시장 관련 비용을
  정해진 방법으로 통과시킨다고 함, NERA p7). 이 정의는 확인 필요.
"""
from dataclasses import dataclass

import numpy as np


def annuity(pv, rate, years):
    if rate == 0:
        return pv / years
    return pv * rate / (1 - (1 + rate) ** -years)


@dataclass(frozen=True)
class Regime:
    floor_rate: float = 0.0447
    cap_rate: float = 0.0748
    regime_years: int = 25
    assessment_years: int = 5
    share_returned: float = 0.70
    npv_rate: float = None          # 묶음 안 NPV 중립 환산율. None이면 floor_rate
    enabled: bool = True


def irr(cashflows, lo=-0.99, hi=1.0, tol=1e-9):
    """이분법 IRR. 부호가 한 번만 바뀌는 현금흐름을 가정. 해가 없으면 nan."""
    cf = np.asarray(cashflows, float)
    t = np.arange(len(cf))

    def npv(r):
        return float(np.sum(cf / (1 + r) ** t))

    f_lo, f_hi = npv(lo), npv(hi)
    if np.sign(f_lo) == np.sign(f_hi):
        return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2
        f = npv(mid)
        if abs(f) < tol:
            break
        if np.sign(f) == np.sign(f_lo):
            lo, f_lo = mid, f
        else:
            hi = mid
    return mid


def evaluate(revenue, capex, opex, regime=Regime(), available=None, social_rate=0.035):
    """revenue: 연 거래 마진 길이 regime_years 배열(실질 £). capex: 운전 시작 시점 RAV. opex: 연 통제 가능 운영비.
    반환: 사업자 현금흐름, 연도별 floor 보전·cap 환수, IRR, 소비자 부담(사회 할인율 현재가치)."""
    R = np.asarray(revenue, float)
    n = regime.regime_years
    if len(R) != n:
        raise ValueError(f"수익 경로 길이 {len(R)} ≠ regime_years {n}")
    avail = np.ones(n, bool) if available is None else np.asarray(available, bool)
    F = annuity(capex, regime.floor_rate, n) + opex
    C = annuity(capex, regime.cap_rate, n) + opex
    topup = np.zeros(n)
    payback = np.zeros(n)
    if regime.enabled:
        r = regime.floor_rate if regime.npv_rate is None else regime.npv_rate
        for a in range(0, n, regime.assessment_years):
            b = min(a + regime.assessment_years, n)
            last = b - 1   # 정산은 묶음 끝 해에 반영 (실제로는 다음 해 지급)
            g = (1 + r) ** (last - np.arange(a, b))   # 묶음 끝 해 기준으로 환산
            rev = float(np.sum(R[a:b] * g))
            floor_sum = float(np.sum(F * avail[a:b] * g))
            cap_sum = float(np.sum(C * g))
            if rev < floor_sum:
                topup[last] = floor_sum - rev
            elif rev > cap_sum:
                payback[last] = regime.share_returned * (rev - cap_sum)
    investor = np.r_[-capex, R - opex + topup - payback]
    consumer = topup - payback
    disc = (1 + social_rate) ** -np.arange(1, n + 1)
    return {
        "floor_level": F, "cap_level": C,
        "investor_cf": investor, "topup": topup, "payback": payback,
        "irr_real": irr(investor),
        "consumer_cost_pv": float(np.sum(consumer * disc)),
        "floor_triggered_periods": int((topup > 0).sum()),
        "cap_triggered_periods": int((payback > 0).sum()),
    }
