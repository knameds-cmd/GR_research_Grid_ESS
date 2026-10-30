"""
도매 + BM 운전 최적화 (실증층 엔진, BM 층). 09 문서 5.5: 장주기 자산의 핵심 수익 경로는 BM이다.

    결정변수 (t = 30분 구간, dt = 0.5h)
        fc[t], fd[t]  도매 위치(FPN) 충전·방전 MW. FPN 순출력 = fd − fc. 도매 가격 MID로 사고판다
        o[t]          받은 BM offer MW (FPN보다 출력 증가). 단가 offer_price로 받는다 (pay-as-bid)
        b[t]          받은 BM bid MW (FPN보다 출력 감소). 단가 bid_price를 낸다 (음수면 받는다)
        pc[t], pd[t]  실제 충전·방전 MW.  pd − pc = (fd − fc) + o − b
        s[t]          구간 끝 저장 에너지 MWh (실제 충·방전으로 움직임)
        k[t]          (양수형) 양수 유닛 수, pc = 유닛 출력 × k  → 정수
        z[t]          offer와 bid를 같은 구간에 동시에 받지 못하게 하는 이진변수
        y[t]          실제 충전·방전 동시 금지 이진변수
    목적함수
        max Σ dt·[ MID·(fd − fc) + offer_price·o − bid_price·b ] − 가변비용·Σ dt·pd  (+ reserve_price·r, 아래 예비력 보유)
    BM 물량 상한 (외생)
        o[t] ≤ κ_o × offer_mw_per_mw[t] × 출력,   b[t] ≤ κ_b × bid_mw_per_mw[t] × 출력
        offer_mw_per_mw 등은 같은 지역 저장장치 무리가 실제로 받은 MW당 지시 (gbess.data.bm_opportunity).
        κ는 그 무리에 비해 이 자산이 얼마나 자주 지시받는지의 배수. 기본 1, 검증에서는 보정 기간에 맞춘다.

막아야 하는 비현실적 해와 이진변수를 두는 곳
    1. offer와 bid 동시 수락: offer 단가 > bid 단가면 둘 다 받아 돈만 남긴다 → 두 상한이 모두 양수이고
       offer_price > bid_price인 구간에 z.
    2. 실제 충전·방전 동시: 손실로 에너지를 태워 저장고를 비우고, 그만큼 bid(음의 단가) 또는 음의 MID 충전으로
       돈을 더 받을 수 있다 → MID ≤ 0 이거나 bid 상한 > 0이고 bid_price < 0인 구간, 그리고 양수형은 모든 구간에 y.
허용하는 것: FPN으로 사고(fc) BM offer로 같은 양을 되파는 거래(실제 운전 pc = pd = 0). 실제 영국 저장장치가
    쓰는 재거래 전략이며, 그 물량은 상한(실제로 지시된 양)으로 제한된다.

fpn_fixed: 순 FPN을 고정하고 BM만 푼다(롤링의 실시간 단계).
fpn_feasible: True면 FPN만으로 운전해도(BM 지시가 하나도 없어도) 물리적으로 가능해야 한다. 그리드 코드상 PN은
    의도한 실제 출력이므로 이것이 맞는 조건이다. 롤링에서 이 조건이 있어야 실시간 단계가 늘 풀린다
    (없으면 예상 bid에 기대 짠 FPN을 실제 bid가 적게 온 날 지킬 수 없다. 2021-07 시험에서 확인).
    FPN 경로의 저장량 sf와, 양수형이면 FPN 양수 유닛 수 kf(정수)를 따로 둔다.
imbalance_penalty: 주면 실제 운전이 FPN + o − b에서 벗어나는 것(불균형)을 £/MWh 벌금으로 허용한다. 롤링 실시간 단계가
    수치 오차 등으로 풀리지 않을 때의 대비책이다. 불균형 물량은 결과의 imbalance_mw 열로 남는다.
p_dis_t, p_ch_t, pump_units_t: 구간별 가용 출력·입력·양수 가능 유닛 수(정지 반영, gbess.data.availability).
    주면 정격 대신 이 값이 상한이 되고, BM 상한도 가용 출력에 비례한다.

채택 모형 방식 (opp에 alpha_offer, alpha_bid 열이 있을 때, gbess.model.bm_accept)
    o[t] ≤ α_o[t] × (가용 출력 − FPN)        b[t] ≤ α_b[t] × (FPN + 가용 입력)
    α는 "이 자산이 자기 단가(offer_price, bid_price 열)로 여유를 내놓았을 때 받아 줄 몫의 기댓값"이다. α는 FPN과
    무관한 변수로만 만든 모형에서 나오므로 상한이 FPN에 선형이다. κ는 쓰지 않는다(모형이 이미 절대 수준을 준다).
    기댓값이므로 같은 구간에 offer와 bid가 둘 다 양수일 수 있다(실제로는 둘 중 하나가 일어나는 것을 평균한 것).
    그래서 이 방식에서는 offer·bid 동시 금지 이진변수(z)를 두지 않는다. 대신 각 상한이 기댓값이라 동시 수락으로
    얻는 차익도 기댓값 안에 머문다.

예비력 보유 (reserve_price를 주면, 09 문서 5.10)
    r[t]          비워 두는 상향 예비력 MW. 단가 reserve_price(£/MW/h)를 보유한 시간만큼 받는다
    배터리:  fd − fc + r ≤ Pt           (충전을 멈추고 바로 방전으로 바꿀 수 있다)
    양수형:  fd + (P/Pc)·fc + r ≤ Pt    (양수 중인 유닛은 예비력을 낼 수 없다. 남은 유닛이 스핀 대기로 낸다)
        양수발전의 공개되지 않는 부가서비스는 결산서에서 "스핀 대기(spin generation) 수입"이 맨 앞이다(Cruachan).
        스핀 대기는 유닛을 물 없이 돌려 두고 수십 초 안에 발전하는 운전이라, 양수 중인 유닛은 할 수 없다.
        Dinorwig는 양수 → 발전 전환에 약 7.5분이 걸린다(PSH_SOURCES 5.1). 처음에 양수 정지도 예비력으로 셌더니
        엔진이 예비력을 지키려고 양수를 늘렸다(2026-10-27 한 주 시험).
    저장량 ≥ 최소 저장량 + r × reserve_hours ÷ 방전 효율   (불려 나가면 그 시간 동안 낼 물이 있어야 한다)
    fpn_feasible이면 FPN 경로 저장량(sf)에도 같은 저장량 조건을 둔다(BM 지시가 없어도 약속을 지킬 수 있게).
    여유는 FPN 기준이다. 예비력으로 잡아 둔 여유를 NESO가 BM offer로 불러 쓰는 것이 실제 예비력 운용이므로
    r과 BM offer(o ≤ α_o × (Pt − FPN))는 같은 여유를 나눠 쓰지 않고 함께 쓴다. 불려 나가 낸 에너지는 offer 단가로 정산.
    (처음에는 실제 출력 기준 pd − pc + r ≤ Pt로 두었으나, 그러면 예비력과 BM offer가 서로 깎아 먹어
    예비력을 가진 자산이 BM 지시를 덜 받는 비현실적인 해가 나왔다. 2026-10-27 Dinorwig 한 주 시험.)
    reserve_fixed: r을 이 값으로 고정(롤링 실시간 단계. 예비력은 하루 전에 FPN과 함께 약속한다).
    공개되지 않는 스핀 대기·예비력·주파수 응답 계약을 "여유를 비우면 받는 값" 하나로 나타낸 것이다.
    reserve_up_mw(고정 여유, 대가 없음)는 검증 1용으로 그대로 둔다.

입찰 단가 띠 (opp에 alpha_offer_0, offer_price_0, alpha_offer_1, … 열이 있을 때, 09 문서 3.9)
    가상 자산은 실제 입찰 단가가 없으므로 단가를 스스로 골라야 한다. 후보 단가 K개(띠 k)마다 그 단가로 냈을 때의
    채택 비율 α_k(gbess.model.bm_accept.alpha_ladder)를 주면, 여유를 띠에 나눠 담는다.
        h[t,k] ≥ 0,  Σ_k h[t,k] ≤ 가용 출력 − FPN,   o[t,k] ≤ α_k[t] × h[t,k],   수입 Σ_k 단가_k × o[t,k]
    (bid도 같다. 여유는 FPN + 가용 입력.) 목적함수가 선형이므로 해는 구간마다 "α_k × (단가_k − 저장 에너지의 값)"이
    가장 큰 띠 하나에 여유를 모두 담는다. 즉 채택 곡선 위에서 기대이익이 가장 큰 단가를 고르는 것과 같다.
    띠마다 α_k를 따로 적용하는 것은 "NESO가 받아 주는 한계 단가가 단가 순서대로 띠를 채운다"는 문턱 해석이다.
    해가 한 띠로 모이므로 실제로는 구간마다 단가 하나를 고르는 것과 같아, 띠 사이 순서 문제는 생기지 않는다.
    띠가 하나면(또는 alpha_offer 열이면) 위의 채택 모형 방식과 똑같다. 결과의 offer_band, bid_band 열이 고른 띠
    번호(받은 물량이 없으면 −1), offer_price는 받은 물량 가중 평균 단가다.

운전량 요금 (charges를 주면, gbess.data.charges)
    charges = (export_gbp_mwh, import_gbp_mwh) 구간별 배열. 실제 방전 pd에 export, 실제 충전 pc에 import 단가를 매겨 뺀다.
    BSUoS처럼 계량된 운전량에 붙는 요금이다. 규칙이 바뀐 시점(CMP281, CMP308)마다 값이 다르다.

기동 비용 (start_cost를 주면, 양수형만, 09 문서 5.11)
    u[t]          발전 중인 유닛 수(정수). pd ≤ (P / 유닛 수) × u. 유닛은 가역식이라 u + k ≤ 쓸 수 있는 유닛 수
    sg[t], sp[t]  발전·양수 기동 횟수. sg ≥ u[t] − u[t−1], sp ≥ k[t] − k[t−1]
    목적함수에서 start_cost × (sg + sp)를 뺀다(£/기동). 마모와 기동 손실을 한 값으로 나타낸 것이다.
    units_start = (u, k): 직전 구간의 유닛 수(롤링에서 전날 마지막 값). 주지 않으면 0으로 본다.
    기동은 실제 운전(pd, pc)에서 센다. FPN 경로는 실행 가능성 점검용이라 기동 비용을 매기지 않는다.
"""
import re
import time
from dataclasses import asdict

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.optimize import Bounds, LinearConstraint, milp

DT = 0.5


class LP:
    """변수 묶음과 제약을 이름으로 쌓아 scipy milp로 푼다 (최대화)."""

    def __init__(self):
        self.n = 0
        self.blocks = {}
        self.lb, self.ub, self.obj, self.integ = [], [], [], []
        self.rows, self.cols, self.vals, self.rlo, self.rhi = [], [], [], [], []
        self.r = 0

    def var(self, name, size, lb=0.0, ub=np.inf, obj=0.0, integer=False):
        self.blocks[name] = np.arange(self.n, self.n + size)
        self.n += size
        self.lb.append(np.broadcast_to(np.asarray(lb, float), size).copy())
        self.ub.append(np.broadcast_to(np.asarray(ub, float), size).copy())
        self.obj.append(np.broadcast_to(np.asarray(obj, float), size).copy())
        self.integ.append(np.full(size, 1 if integer else 0))
        return self.blocks[name]

    def row(self, terms, lo, hi):
        """terms: [(변수 index, 계수), ...]. lo ≤ Σ 계수·변수 ≤ hi."""
        for j, a in terms:
            self.rows.append(self.r)
            self.cols.append(int(j))
            self.vals.append(float(a))
        self.rlo.append(lo)
        self.rhi.append(hi)
        self.r += 1

    def solve(self, gap=1e-6, time_limit=600):
        c = -np.concatenate(self.obj)            # milp는 최소화
        A = sp.csr_matrix((self.vals, (self.rows, self.cols)), shape=(self.r, self.n))
        res = milp(c, constraints=LinearConstraint(A, self.rlo, self.rhi), integrality=np.concatenate(self.integ),
                   bounds=Bounds(np.concatenate(self.lb), np.concatenate(self.ub)),
                   options={"mip_rel_gap": gap, "time_limit": time_limit, "disp": False})
        return res


def ladder(opp: pd.DataFrame, side: str):
    """opp의 side("offer"·"bid") 띠 → (α T×K, 단가 T×K). 띠 열이 없으면 alpha_{side}·{side}_price를 K=1로 돌려준다.
    채택 모형 열이 아예 없으면 None."""
    ks = sorted(int(c.rsplit("_", 1)[1]) for c in opp.columns if re.fullmatch(f"alpha_{side}_\\d+", c))
    if ks:
        A = opp[[f"alpha_{side}_{k}" for k in ks]].to_numpy(float)
        Pr = opp[[f"{side}_price_{k}" for k in ks]].to_numpy(float)
        return A, Pr
    if f"alpha_{side}" in opp.columns:
        return opp[[f"alpha_{side}"]].to_numpy(float), opp[[f"{side}_price"]].to_numpy(float)
    return None


def solve_bm(price: pd.Series, opp: pd.DataFrame, asset, kappa_offer=1.0, kappa_bid=1.0, fpn_fixed=None,
             terminal="geq_init", water_value=None, s_start=None, reserve_up_mw=0.0, reserve_hours=1.0,
             gap=1e-6, time_limit=600, p_dis_t=None, p_ch_t=None, pump_units_t=None, fpn_feasible=True,
             imbalance_penalty=None, reserve_price=None, reserve_fixed=None, start_cost=None, units_start=None, charges=None):
    p = price.to_numpy(float)
    if np.isnan(p).any():
        raise ValueError("도매 가격 결측")
    opp = opp.reindex(price.index)
    T = len(p)
    P, Pc, E = asset.p_dis_mw, asset.p_ch_mw, asset.e_mwh
    Pt = np.full(T, P) if p_dis_t is None else np.minimum(np.asarray(p_dis_t, float), P)
    Pct = np.full(T, Pc) if p_ch_t is None else np.minimum(np.asarray(p_ch_t, float), Pc)
    lo_, lb_ = ladder(opp, "offer"), ladder(opp, "bid")
    accept = lo_ is not None
    if accept:   # 채택 모형 방식. 띠가 하나면 K = 1
        (Ao, Po), (Ab, Pb) = lo_, lb_
        Ao, Ab = np.clip(np.nan_to_num(Ao), 0, 1), np.clip(np.nan_to_num(Ab), 0, 1)
        Ao[np.isnan(Po)], Ab[np.isnan(Pb)] = 0.0, 0.0
        O_cap, B_cap = Ao * (Pt + Pct)[:, None], Ab * (Pt + Pct)[:, None]   # 변수 상한. 실제 상한은 아래 FPN 선형 제약
    else:
        O_cap = np.nan_to_num(kappa_offer * opp["offer_mw_per_mw"].to_numpy(float) * Pt)[:, None]
        B_cap = np.nan_to_num(kappa_bid * opp["bid_mw_per_mw"].to_numpy(float) * Pt)[:, None]
        Po, Pb = opp[["offer_price"]].to_numpy(float), opp[["bid_price"]].to_numpy(float)
        O_cap[np.isnan(Po)], B_cap[np.isnan(Pb)] = 0.0, 0.0
    Po, Pb = np.nan_to_num(Po), np.nan_to_num(Pb)
    Ko, Kb = Po.shape[1], Pb.shape[1]
    o_cap, b_cap = O_cap.max(axis=1), B_cap.max(axis=1)
    po, pb = Po[:, 0], Pb[:, 0]   # 띠가 하나일 때의 단가 (상대 거래 방식의 z 이진변수에 쓴다)
    integer_pump = asset.pump_units is not None
    s0 = asset.soc_init * E if s_start is None else float(s_start)

    lp = LP()
    if fpn_fixed is None:
        fc = lp.var("fc", T, 0, Pct, obj=-p * DT)
        fd = lp.var("fd", T, 0, Pt, obj=p * DT)
    else:
        f = np.asarray(fpn_fixed, float)
        fc = lp.var("fc", T, np.maximum(-f, 0), np.maximum(-f, 0), obj=-p * DT)
        fd = lp.var("fd", T, np.maximum(f, 0), np.maximum(f, 0), obj=p * DT)
    O = lp.var("o", T * Ko, 0, O_cap.ravel(), obj=(Po * DT).ravel()).reshape(T, Ko)   # O[t, k]: 띠 k에서 받은 offer
    B = lp.var("b", T * Kb, 0, B_cap.ravel(), obj=(-Pb * DT).ravel()).reshape(T, Kb)
    o, b = O[:, 0], B[:, 0]
    if charges is None:
        ch_e, ch_i = np.zeros(T), np.zeros(T)
    else:
        ch_e, ch_i = (np.nan_to_num(np.broadcast_to(np.asarray(c, float), T)) for c in charges)
    pc = lp.var("pc", T, 0, Pct, obj=-ch_i * DT)
    pd_ = lp.var("pd", T, 0, np.maximum(Pt - reserve_up_mw, 0), obj=-(asset.var_cost + ch_e) * DT)
    s_lb = asset.soc_min * E + reserve_up_mw * reserve_hours / asset.eta_dis
    s_lb_arr = np.full(T, s_lb)
    if terminal == "geq_init":
        s_lb_arr[-1] = max(s_lb, s0)
    s_obj = np.zeros(T)
    if terminal == "value":
        s_obj[-1] = float(water_value)
    elif terminal != "geq_init":
        raise ValueError(terminal)
    s = lp.var("s", T, s_lb_arr, asset.soc_max * E, obj=s_obj)
    keep = 1 - asset.self_discharge_per_h * DT
    if imbalance_penalty is not None:
        iu = lp.var("iu", T, 0, P + Pc, obj=-imbalance_penalty * DT)    # FPN+BM보다 더 낸 양
        idn = lp.var("idn", T, 0, P + Pc, obj=-imbalance_penalty * DT)  # 덜 낸 양
    hold = reserve_price is not None or reserve_fixed is not None
    rp = np.zeros(T) if reserve_price is None else np.broadcast_to(np.asarray(reserve_price, float), T).copy()
    if hold:
        if reserve_fixed is None:
            r = lp.var("r", T, 0, Pt, obj=rp * DT)
        else:
            rf = np.minimum(np.asarray(reserve_fixed, float), Pt)
            if fpn_fixed is not None:   # FPN 반올림(펌프 단위)으로 여유가 조금 줄었으면 그만큼만 지킨다
                f = np.asarray(fpn_fixed, float)
                used = np.where(f > 0, f, -f * (P / Pc if asset.pump_units is not None else -1.0))
                rf = np.clip(np.minimum(rf, Pt - used), 0, None)
            r = lp.var("r", T, rf, rf, obj=rp * DT)
        r_e = reserve_hours / asset.eta_dis
        fc_coef = P / Pc if integer_pump else -1.0
        for t in range(T):
            lp.row([(fd[t], 1), (fc[t], fc_coef), (r[t], 1)], -np.inf, Pt[t])
            lp.row([(s[t], 1), (r[t], -r_e)], asset.soc_min * E, np.inf)

    for t in range(T):
        # 에너지 수지
        terms = [(s[t], 1.0), (pc[t], -DT * asset.eta_ch), (pd_[t], DT / asset.eta_dis)]
        if t > 0:
            terms.append((s[t - 1], -keep))
            lp.row(terms, 0.0, 0.0)
        else:
            lp.row(terms, keep * s0, keep * s0)
        # 실제 출력 = FPN + offer − bid (+ 불균형)
        terms = [(pd_[t], 1), (pc[t], -1), (fd[t], -1), (fc[t], 1)] + [(j, -1) for j in O[t]] + [(j, 1) for j in B[t]]
        if imbalance_penalty is not None:
            terms += [(iu[t], -1), (idn[t], 1)]
        lp.row(terms, 0.0, 0.0)

    if fpn_feasible and fpn_fixed is None:
        sf = lp.var("sf", T, s_lb, asset.soc_max * E)
        for t in range(T):
            terms = [(sf[t], 1.0), (fc[t], -DT * asset.eta_ch), (fd[t], DT / asset.eta_dis)]
            if t > 0:
                terms.append((sf[t - 1], -keep))
                lp.row(terms, 0.0, 0.0)
            else:
                lp.row(terms, keep * s0, keep * s0)
        if integer_pump:
            kf_ub = asset.pump_units if pump_units_t is None else np.minimum(np.asarray(pump_units_t, float),
                                                                             asset.pump_units)
            kf = lp.var("kf", T, 0, kf_ub, integer=True)
            for t in range(T):
                lp.row([(fc[t], 1), (kf[t], -Pc / asset.pump_units)], 0.0, 0.0)
        if hold:   # 약속한 예비력은 FPN만으로 운전해도 지킬 수 있어야 한다
            for t in range(T):
                lp.row([(sf[t], 1), (r[t], -r_e)], asset.soc_min * E, np.inf)
        # FPN 방전은 예비력 여유를 뺀 출력까지만
        for t in range(T):
            lp.row([(fd[t], 1.0)], -np.inf, max(Pt[t] - reserve_up_mw, 0.0))
        # FPN 충전과 방전을 같은 구간에 함께 잡지 못하게 한다. 함께 잡으면 순 FPN이 펌프 단위로 나누어떨어지지 않거나
        # FPN 경로의 손실 계산이 실제와 달라져, BM 지시가 없을 때 FPN을 지킬 수 없다 (2017-01 시험에서 확인)
        wf = lp.var("wf", T, 0, 1, integer=True)
        for t in range(T):
            lp.row([(fc[t], 1), (wf[t], -Pc)], -np.inf, 0.0)
            lp.row([(fd[t], 1), (wf[t], P)], -np.inf, P)

    if accept:
        if Ko == 1:
            a_o = Ao[:, 0]
            for t in range(T):
                if a_o[t] > 0:   # o ≤ α_o (Pt − fd + fc)
                    lp.row([(o[t], 1), (fd[t], a_o[t]), (fc[t], -a_o[t])], -np.inf, a_o[t] * Pt[t])
        else:            # 여유를 띠에 나눠 담는다: o_k ≤ α_k h_k, Σ h_k ≤ Pt − fd + fc
            ho = lp.var("ho", T * Ko, 0, (Pt + Pct).repeat(Ko)).reshape(T, Ko)
            for t in range(T):
                for k_ in range(Ko):
                    lp.row([(O[t, k_], 1), (ho[t, k_], -Ao[t, k_])], -np.inf, 0.0)
                lp.row([(j, 1) for j in ho[t]] + [(fd[t], 1), (fc[t], -1)], -np.inf, Pt[t])
        if Kb == 1:
            a_b = Ab[:, 0]
            for t in range(T):
                if a_b[t] > 0:   # b ≤ α_b (fd − fc + Pct)
                    lp.row([(b[t], 1), (fd[t], -a_b[t]), (fc[t], a_b[t])], -np.inf, a_b[t] * Pct[t])
        else:
            hb = lp.var("hb", T * Kb, 0, (Pt + Pct).repeat(Kb)).reshape(T, Kb)
            for t in range(T):
                for k_ in range(Kb):
                    lp.row([(B[t, k_], 1), (hb[t, k_], -Ab[t, k_])], -np.inf, 0.0)
                lp.row([(j, 1) for j in hb[t]] + [(fd[t], -1), (fc[t], 1)], -np.inf, Pct[t])
    both = np.array([], int) if accept else np.flatnonzero((o_cap > 0) & (b_cap > 0) & (po > pb))
    if len(both):
        z = lp.var("z", len(both), 0, 1, integer=True)
        for j, t in enumerate(both):
            lp.row([(o[t], 1), (z[j], -o_cap[t])], -np.inf, 0.0)          # o ≤ cap·z
            lp.row([(b[t], 1), (z[j], b_cap[t])], -np.inf, b_cap[t])       # b ≤ cap·(1 − z)
    mode_t = np.arange(T) if integer_pump else np.flatnonzero((p <= 0) | ((B_cap > 0) & (Pb < 0)).any(axis=1))
    if len(mode_t):
        y = lp.var("y", len(mode_t), 0, 1, integer=True)
        for j, t in enumerate(mode_t):
            lp.row([(pc[t], 1), (y[j], -Pc)], -np.inf, 0.0)
            lp.row([(pd_[t], 1), (y[j], P)], -np.inf, P)
    if integer_pump:
        k_ub = asset.pump_units if pump_units_t is None else np.minimum(np.asarray(pump_units_t, float),
                                                                        asset.pump_units)
        k = lp.var("k", T, 0, k_ub, integer=True)
        unit = Pc / asset.pump_units
        for t in range(T):
            lp.row([(pc[t], 1), (k[t], -unit)], 0.0, 0.0)
    commit = start_cost is not None and integer_pump
    if commit:
        G = asset.pump_units
        g_unit = P / G
        u_ub = np.minimum(np.ceil(Pt / g_unit - 1e-9), G)
        n_ub = np.maximum(u_ub, k_ub)          # 발전이나 양수에 쓸 수 있는 유닛 수
        u = lp.var("u", T, 0, u_ub, integer=True)
        sg = lp.var("sg", T, 0, G, obj=-float(start_cost))
        spp = lp.var("sp", T, 0, G, obj=-float(start_cost))
        u0, k0 = (0.0, 0.0) if units_start is None else units_start
        for t in range(T):
            lp.row([(pd_[t], 1), (u[t], -g_unit)], -np.inf, 0.0)
            lp.row([(u[t], 1), (k[t], 1)], -np.inf, float(np.broadcast_to(n_ub, T)[t]))
            if t == 0:
                lp.row([(sg[t], 1), (u[t], -1)], -u0, np.inf)
                lp.row([(spp[t], 1), (k[t], -1)], -k0, np.inf)
            else:
                lp.row([(sg[t], 1), (u[t], -1), (u[t - 1], 1)], 0.0, np.inf)
                lp.row([(spp[t], 1), (k[t], -1), (k[t - 1], 1)], 0.0, np.inf)

    t0 = time.time()
    res = lp.solve(gap=gap, time_limit=time_limit)
    if res.x is None:
        raise RuntimeError(f"해를 찾지 못함: {res.message}")
    x = res.x
    g = lambda blk: x[blk]   # noqa: E731
    Ov, Bv = x[O], x[B]                       # T × K 띠별 받은 물량
    ov, bv = Ov.sum(axis=1), Bv.sum(axis=1)

    def eff(V, Pr):   # 받은 물량 가중 평균 단가. 받은 것이 없으면 첫 띠 단가 (수입 계산에는 영향 없음)
        tot = V.sum(axis=1)
        return np.where(tot > 1e-9, (V * Pr).sum(axis=1) / np.where(tot > 1e-9, tot, 1.0), Pr[:, 0])

    out = pd.DataFrame({"price": p, "fpn_mw": g(fd) - g(fc), "offer_mw": ov, "bid_mw": bv,
                        "charge_mw": g(pc), "discharge_mw": g(pd_), "soc_mwh": g(s),
                        "offer_price": eff(Ov, Po), "bid_price": eff(Bv, Pb), "offer_cap": o_cap, "bid_cap": b_cap},
                       index=price.index)
    out["offer_band"] = np.where(ov > 1e-9, Ov.argmax(axis=1), -1)
    out["bid_band"] = np.where(bv > 1e-9, Bv.argmax(axis=1), -1)
    out["net_mw"] = out["discharge_mw"] - out["charge_mw"]
    out["imbalance_mw"] = (g(iu) - g(idn)) if imbalance_penalty is not None else 0.0
    out["reserve_mw"] = g(r) if hold else 0.0
    out["reserve_price"] = rp
    if integer_pump:
        unit_p = P / asset.pump_units
        out["gen_units"] = np.round(g(u)) if commit else np.ceil(np.round(g(pd_), 6) / unit_p - 1e-6)
        out["pump_units"] = np.round(g(k))
        if commit:   # 켜진 유닛 수의 증가분 (기동 비용이 0이면 sg·sp 값이 정해지지 않으므로 유닛 수에서 센다)
            u_prev = np.r_[u0, out["gen_units"].to_numpy()[:-1]]
            k_prev = np.r_[k0, out["pump_units"].to_numpy()[:-1]]
            out["starts"] = (np.clip(out["gen_units"] - u_prev, 0, None) + np.clip(out["pump_units"] - k_prev, 0, None))
        else:
            out["starts"] = np.nan
    out["start_cost"] = float(start_cost) if commit else 0.0
    out["charge_export"], out["charge_import"] = ch_e, ch_i
    info = {"status": res.message, "optimal": bool(res.success), "mip_gap": getattr(res, "mip_gap", None),
            "seconds": round(time.time() - t0, 2), "periods": T, "offer_bid_binaries": int(len(both)),
            "mode_binaries": int(len(mode_t)), "placeholders": asset.placeholders(), "bands": (Ko, Kb),
            "offer_mw_bands": Ov, "bid_mw_bands": Bv,
            "kappa": None if accept else (kappa_offer, kappa_bid), "bm_mode": "accept" if accept else "fleet",
            "asset": {k_: v for k_, v in asdict(asset).items()
                                                         if k_ not in ("status", "source")}}
    return out, info


def summarise_bm(out, asset):
    hours = len(out) * DT
    yr = 8760 / hours
    wholesale = float((out["price"] * out["fpn_mw"]).sum() * DT)
    offer = float((out["offer_price"] * out["offer_mw"]).sum() * DT)
    bid = float(-(out["bid_price"] * out["bid_mw"]).sum() * DT)
    var = float(asset.var_cost * out["discharge_mw"].sum() * DT)
    reserve = float((out["reserve_price"] * out["reserve_mw"]).sum() * DT) if "reserve_mw" in out else 0.0
    starts = float(out["starts"].sum()) if "starts" in out and out["starts"].notna().any() else 0.0
    start = float(out["start_cost"].iat[0]) * starts if "start_cost" in out and len(out) else 0.0
    chg = float((out["charge_export"] * out["discharge_mw"] + out["charge_import"] * out["charge_mw"]).sum() * DT) \
        if "charge_export" in out else 0.0
    total = wholesale + offer + bid - var + reserve - start - chg
    k = lambda v: v / asset.p_dis_mw * yr / 1e3   # noqa: E731
    return {"wholesale_k": k(wholesale), "bm_offer_k": k(offer), "bm_bid_k": k(bid), "var_cost_k": -k(var),
            "reserve_k": k(reserve), "charges_k": -k(chg), "start_cost_k": -k(start), "starts": starts * yr, "reserve_mw_mean": float(out["reserve_mw"].mean()) if "reserve_mw" in out else 0.0,
            "total_k_per_mw_yr": k(total), "gen_mwh": float(out["discharge_mw"].sum() * DT),
            "pump_mwh": float(out["charge_mw"].sum() * DT), "offer_mwh": float(out["offer_mw"].sum() * DT),
            "bid_mwh": float(out["bid_mw"].sum() * DT),
            "simultaneous_offer_bid": int(((out["offer_mw"] > 1e-6) & (out["bid_mw"] > 1e-6)).sum()),
            "simultaneous_charge_discharge": int(((out["charge_mw"] > 1e-6) & (out["discharge_mw"] > 1e-6)).sum())}

