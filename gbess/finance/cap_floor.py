"""
cap-and-floor 재무층 (08 문서 2장의 F형 규칙). 연 수익 경로가 주어지면 사업자 현금흐름과 소비자 부담을 계산한다.
제도 사실은 literature/sources/ldes/FACTS.md 2장 (Ofgem TDD 2025-03, FFD 2025-09, Window 1 MTD 2026-06, NERA 2026).

모든 금액은 CPIH 실질 £. 정해진 대로 넣은 것:
  - floor·cap 수준 = RAV(100%)를 각 수익률로 regime_years 동안 연금화한 값 + 통제 가능 운영비. 잔존가치 0.  [TDD p56–61, MTD p37]
  - 정산 묶음 assessment_years(5년, 사업자가 1년을 고를 수 있음). 묶음 안의 값은 npv_rate로 지급 시점까지 복리 환산해
    비교한다("NPV 중립"). 할인율은 문서에 없으므로(TDD p55) 기본값을 floor 수익률로 둔다.  [TDD p44, p55]
  - 묶음 수익 < floor 합이면 부족분 보전, > cap 합이면 초과분의 share_returned(70%)를 돌려줌.  [FFD 4.19, NERA p7]
  - 지급은 묶음이 끝난 다음 해.  [TDD p44, p55]
  - 묶음 사이 이월과 최종 정산(carry_over=True): 묶음별 중간 지급을 하고, 25년 전체를 한 묶음으로 본 값과의 차이를
    마지막 해 다음 해에 정산한다("final assessment based on full regime duration … interim payments trued up").  [TDD p44, p55]
  - 가용률 조건(MAT)을 못 채운 해: 그해 floor는 0이고, floor 쪽 비교에는 그해 수익 중 floor 수준을 넘는 몫만 들어간다.
    cap 쪽 비교에는 그해 수익이 모두 들어간다.  [TDD p50–51, p62]. MAT 기준은 사업별로 정한다(FFD 3.23). 여기서는 해마다
    충족 여부(available)를 입력으로 받는다.
  - 한계 순환 비용(marginal cycling costs): Ofgem은 총수익에서 빼서 "평가 수익"을 만들 수 있다고 했다(FFD 5.25–5.27,
    면허에서 확정). cycling_cost로 해마다 뺄 값을 줄 수 있다. 기본 0.
  - 소비자 부담은 NESO가 공급사에 매기는 BSUoS로 회수된다(FFD 8.1–8.4). 여기서는 금액만 계산하고 누가 내는지는 나누지 않는다.
  - 교체 투자(repex)와 잔존가치(residual value): repex는 RAV에 들어가는 capex다(TDD p40–41). 사전에 정한 repex 계획을
    받아, floor·cap 수준을 RAV = capex + repex 현재가치 − 잔존가치 현재가치(각 수익률로 할인)의 연금으로 계산하고, 사업자는
    repex를 그해에 쓴다. 잔존가치는 Window 1에서 45건 중 41건이 0이 아닌 값을 인정받았다(MTD 6.11). 잔존가치만큼 floor·cap이
    낮아지고, 사업자는 제도가 끝나는 해(시점 n)에 그 값을 가진다. 둘 다 기본 0이라 예전 결과와 같다. 비용 입력은
    gbess.finance.costs.
단순화(결과에 함께 기록):
  - 제도 종료 뒤 floor 보전금 회수(TDD p37, p40; FFD 9.6 "time bound", 방식 미정)는 넣지 않았다. 그래서 floor 보전이
    큰 경로의 소비자 부담은 상한 쪽이다.
  - 세금·통과비용(망요금 등)은 넣지 않았다. "수익"은 에너지 구입비를 뺀 거래 마진으로 본다(Ofgem은 시장 관련 비용을
    정해진 방법으로 통과시킨다고 함, NERA p7).
  - 처음 판(2026-10-24~28)은 묶음을 따로따로 정산했고(이월 없음), 가용률 미달 해의 수익을 floor 쪽에 모두 넣었으며,
    같은 해에 지급했다. 2026-10-29 독립 심사 지적으로 고쳤다.
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


def irr(cashflows, lo=-0.9, hi=1.0, tol=1e-9):
    """IRR. [lo, hi]를 촘촘히 훑어 NPV 부호가 바뀌는 곳 중 가장 높은 수익률을 이분법으로 찾는다. 해가 없으면 nan.
    cap 환수가 마지막 정산(n+1)에 오면 현금흐름 부호가 두 번 바뀐다(−투자, +운전, −환수). 낮은 쪽 근은 마지막 음수
    항이 (1+r)^−(n+1)로 부풀어 생기는 가짜 근이라, 높은 쪽 근(보통 사업의 IRR)을 고른다."""
    cf = np.asarray(cashflows, float)
    t = np.arange(len(cf))

    def npv(r):
        return float(np.sum(cf / (1 + r) ** t))

    grid = np.linspace(lo, hi, 381)
    f = np.array([npv(r) for r in grid])
    ch = np.nonzero(np.sign(f[:-1]) * np.sign(f[1:]) < 0)[0]
    if len(ch) == 0:
        return float("nan")
    lo, hi = grid[ch[-1]], grid[ch[-1] + 1]
    f_lo = npv(lo)
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = npv(mid)
        if abs(fm) < tol:
            break
        if np.sign(fm) == np.sign(f_lo):
            lo, f_lo = mid, fm
        else:
            hi = mid
    return mid


def evaluate(revenue, capex, opex, regime=Regime(), available=None, social_rate=0.035, cycling_cost=None,
             carry_over=True, repex=None, residual_value=0.0):
    """revenue: 연 총수익(거래 마진) 길이 regime_years 배열(실질 £). capex: 운전 시작 시점 RAV. opex: 연 통제 가능 운영비.
    cycling_cost: 평가 수익에서 뺄 연 한계 순환 비용(스칼라나 배열). 사업자 현금흐름에서는 빼지 않는다(실제 비용은 이미
    수익 경로에 들어 있다고 본다).
    repex: 운전 연도 1..n에 쓸 교체 투자(스칼라나 길이 n 배열, 실질 £). residual_value: 시점 n의 잔존가치(실질 £).
    시점: 0 = 투자, 1..n = 운전 연도, n+1 = 마지막 묶음 지급과 최종 정산.
    반환: 사업자 현금흐름(길이 n+2), 시점별 floor 보전·cap 환수·최종 정산, IRR, 소비자 부담(사회 할인율 현재가치)."""
    R = np.asarray(revenue, float)
    n = regime.regime_years
    if len(R) != n:
        raise ValueError(f"수익 경로 길이 {len(R)} ≠ regime_years {n}")
    avail = np.ones(n, bool) if available is None else np.asarray(available, bool)
    A = R - (0.0 if cycling_cost is None else np.broadcast_to(np.asarray(cycling_cost, float), n))
    rep = np.zeros(n) if repex is None else np.broadcast_to(np.asarray(repex, float), n)
    t_op = np.arange(1, n + 1)

    def level(rate):   # RAV = capex + repex 현재가치 − 잔존가치 현재가치
        rav = capex + float(np.sum(rep / (1 + rate) ** t_op)) - residual_value / (1 + rate) ** n
        return annuity(rav, rate, n) + opex

    F, C = level(regime.floor_rate), level(regime.cap_rate)
    A_floor = np.where(avail, A, np.maximum(A - F, 0.0))   # 가용률 미달 해는 floor를 넘는 몫만
    F_t = F * avail
    topup = np.zeros(n + 2)       # 시점 0..n+1
    payback = np.zeros(n + 2)
    trueup = np.zeros(n + 2)
    year = np.arange(1, n + 1)    # 운전 연도의 시점

    def settle(sl, pay_at, r):
        g = (1 + r) ** (pay_at - year[sl])
        rev_f, rev_c = float(np.sum(A_floor[sl] * g)), float(np.sum(A[sl] * g))
        floor_sum, cap_sum = float(np.sum(F_t[sl] * g)), float(np.sum(C * g))
        if rev_f < floor_sum:
            return floor_sum - rev_f, 0.0
        if rev_c > cap_sum:
            return 0.0, regime.share_returned * (rev_c - cap_sum)
        return 0.0, 0.0

    if regime.enabled:
        r = regime.floor_rate if regime.npv_rate is None else regime.npv_rate
        for a in range(0, n, regime.assessment_years):
            b = min(a + regime.assessment_years, n)
            pay_at = b + 1                 # 묶음 끝(시점 b) 다음 해
            topup[pay_at], payback[pay_at] = settle(slice(a, b), pay_at, r)
        if carry_over:
            full_t, full_p = settle(slice(0, n), n + 1, r)
            paid = float(np.sum((topup - payback) * (1 + r) ** (n + 1 - np.arange(n + 2))))
            trueup[n + 1] = (full_t - full_p) - paid
    consumer = topup - payback + trueup
    investor = np.r_[-capex, R - opex - rep, 0.0] + consumer
    investor[n] += residual_value
    disc = (1 + social_rate) ** -np.arange(n + 2)
    return {
        "floor_level": F, "cap_level": C,
        "investor_cf": investor, "topup": topup, "payback": payback, "trueup": trueup,
        "irr_real": irr(investor),
        "consumer_cost_pv": float(np.sum(consumer * disc)),
        "floor_triggered_periods": int((topup > 0).sum()),
        "cap_triggered_periods": int((payback > 0).sum()),
    }
