"""
단일 저장장치의 가격 수용자 운전 최적화 (실증층 엔진).

    결정변수 (t = 30분 구간, dt = 0.5h)
        c[t]  충전(양수) MW,  d[t]  방전(발전) MW,  s[t]  구간 t 끝의 저장 에너지 MWh
        k[t]  (양수형만) 양수 중인 유닛 수. c[t] = k[t] × 유닛당 양수 출력  → 정수
        y[t]  1이면 충전 모드. 동시 충방전 금지용 이진변수. 연속형 자산은 가격 ≤ 0인 구간에만,
              양수형은 모든 구간에 둔다 (펌프가 유닛 단위 고정 출력이면 일부 유닛 양수 + 일부 발전으로
              순출력을 맞추는 해가 가격 > 0에서도 나온다. 2025년 시험에서 4구간 확인)
    목적함수
        max Σ price[t]·(d[t] − c[t])·dt − var_cost·Σ d[t]·dt
    제약
        s[t] = s[t−1]·(1 − σ·dt) + dt·(eta_ch·c[t] − d[t]/eta_dis)
        soc_min·E ≤ s[t] ≤ soc_max·E,  s[−1] = soc_init·E,  s[T−1] ≥ soc_init·E (기간 끝에 다 팔아 버리지 않게)
        연속형 자산은 가격 > 0이면 동시 충방전이 손실만 내므로 최적해에 나오지 않는다.

scipy.optimize.milp(HiGHS)에 희소행렬로 바로 넘긴다. 1년(17,520구간) 연속 문제가 수 초 안에 풀린다.
"""
import time
from dataclasses import asdict

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.optimize import Bounds, LinearConstraint, milp

DT = 0.5


def solve(price: pd.Series, asset, gap=1e-6, time_limit=600, terminal="geq_init", s_start=None, water_value=None):
    """terminal: "geq_init"(기간 끝 저장량 ≥ 시작 저장량) 또는 "value"(끝 저장량 1 MWh당 water_value £를 목적함수에 더함).
    s_start: 시작 저장량 MWh (None이면 soc_init × 용량). 롤링에서 전날 끝 저장량을 넘길 때 쓴다."""
    p = price.to_numpy(float)
    if np.isnan(p).any():
        raise ValueError(f"가격에 결측 {int(np.isnan(p).sum())}구간. 먼저 채우거나 기간을 줄이세요.")
    T = len(p)
    E = asset.e_mwh
    integer_pump = asset.pump_units is not None
    neg = np.arange(T) if integer_pump else np.flatnonzero(p <= 0)
    nb = len(neg)

    # 변수 순서: c[0:T], d[T:2T], s[2T:3T], (k[3T:4T]), y[...nb]
    ic, id_, is_ = 0, T, 2 * T
    ik = 3 * T
    iy = ik + (T if integer_pump else 0)
    n = iy + nb

    cost = np.zeros(n)
    cost[ic:ic + T] = p * DT                       # milp는 최소화: −(수익)
    cost[id_:id_ + T] = -p * DT + asset.var_cost * DT

    lb = np.zeros(n)
    ub = np.full(n, np.inf)
    ub[ic:ic + T] = asset.p_ch_mw
    ub[id_:id_ + T] = asset.p_dis_mw
    lb[is_:is_ + T] = asset.soc_min * E
    ub[is_:is_ + T] = asset.soc_max * E
    if integer_pump:
        ub[ik:ik + T] = asset.pump_units
    ub[iy:iy + nb] = 1
    integrality = np.zeros(n)
    if integer_pump:
        integrality[ik:ik + T] = 1
    integrality[iy:iy + nb] = 1

    rows, cols, vals, lo, hi = [], [], [], [], []
    r = 0
    keep = 1 - asset.self_discharge_per_h * DT
    s0 = asset.soc_init * E if s_start is None else float(s_start)
    # 에너지 수지: s[t] − keep·s[t−1] − dt·eta_ch·c[t] + dt/eta_dis·d[t] = 0   (t=0이면 우변 keep·s0)
    for t in range(T):
        rows += [r, r, r]
        cols += [is_ + t, ic + t, id_ + t]
        vals += [1.0, -DT * asset.eta_ch, DT / asset.eta_dis]
        if t > 0:
            rows.append(r); cols.append(is_ + t - 1); vals.append(-keep)
            lo.append(0.0); hi.append(0.0)
        else:
            lo.append(keep * s0); hi.append(keep * s0)
        r += 1
    if integer_pump:
        unit = asset.p_ch_mw / asset.pump_units
        for t in range(T):   # c[t] − unit·k[t] = 0
            rows += [r, r]; cols += [ic + t, ik + t]; vals += [1.0, -unit]
            lo.append(0.0); hi.append(0.0); r += 1
    for j, t in enumerate(neg):   # c ≤ Pc·y,  d ≤ Pd·(1 − y)
        rows += [r, r]; cols += [ic + t, iy + j]; vals += [1.0, -asset.p_ch_mw]
        lo.append(-np.inf); hi.append(0.0); r += 1
        rows += [r, r]; cols += [id_ + t, iy + j]; vals += [1.0, asset.p_dis_mw]
        lo.append(-np.inf); hi.append(asset.p_dis_mw); r += 1
    if terminal == "geq_init":
        lb[is_ + T - 1] = max(lb[is_ + T - 1], s0)
    elif terminal == "value":
        cost[is_ + T - 1] -= float(water_value)
    else:
        raise ValueError(f"terminal은 geq_init 또는 value: {terminal}")

    A = sp.csr_matrix((vals, (rows, cols)), shape=(r, n))
    t0 = time.time()
    res = milp(cost, constraints=LinearConstraint(A, lo, hi), integrality=integrality,
               bounds=Bounds(lb, ub), options={"mip_rel_gap": gap, "time_limit": time_limit, "disp": False})
    secs = time.time() - t0
    if res.x is None:
        raise RuntimeError(f"해를 찾지 못함: {res.message}")
    x = res.x
    out = pd.DataFrame({"price": p, "charge_mw": x[ic:ic + T], "discharge_mw": x[id_:id_ + T],
                        "soc_mwh": x[is_:is_ + T]}, index=price.index)
    out["net_mw"] = out["discharge_mw"] - out["charge_mw"]
    info = {
        "status": res.message, "optimal": bool(res.success), "mip_gap": getattr(res, "mip_gap", None),
        "seconds": round(secs, 2), "periods": T, "binary_periods": nb, "integer_pump": integer_pump,
        "placeholders": asset.placeholders(), "asset": {k: v for k, v in asdict(asset).items()
                                                         if k not in ("status", "source")},
    }
    return out, info


def summarise(out, asset):
    hours = len(out) * DT
    rev = float((out["price"] * out["net_mw"]).sum() * DT)
    var = float(asset.var_cost * out["discharge_mw"].sum() * DT)
    dis = float(out["discharge_mw"].sum() * DT)
    yr = 8760 / hours
    return {
        "margin_gbp": rev - var,
        "margin_k_per_mw_yr": (rev - var) / asset.p_dis_mw * yr / 1e3,
        "margin_per_mwh_cap_yr": (rev - var) / (asset.duration_h * asset.p_dis_mw) * yr,
        "discharged_mwh": dis,
        "full_cycles_per_yr": dis / (asset.duration_h * asset.p_dis_mw) * yr,
        "simultaneous_periods": int(((out["charge_mw"] > 1e-6) & (out["discharge_mw"] > 1e-6)).sum()),
    }
