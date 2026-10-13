"""
층 1: 완전예측·가격 수용자 MILP. 배터리 하나가 도매(MID)와 EAC 상품(DC/DM/DR, BR/QR/SR)에서
얻을 수 있는 최대 수익과 그때의 운전 계획을 구한다. 해설은 docs/04_layer1_model_KO.md.

변수 (t = 30분 구간)
    c[t], d[t]   충전·방전 전력 MW (도매에서 사고파는 물량. 계통 기준 순출력 = d - c)
    u[t]         1이면 충전 모드, 0이면 방전 모드 (동시 충방전 금지용 이진 변수)
    soc[k]       k번째 구간 시작 시점의 저장 에너지 MWh (k = 0..n)
    r[p, w]      상품 p를 낙찰 구간 w(EFA 블록 또는 30분)에 판 물량 MW. 한 구간 안에서는 같은 값
목적함수
    도매 수익 Σ 가격·(d - c)·0.5h  +  가용 수익 Σ 낙찰가·r·0.5h  -  처리량 비용 Σ κ·(c + d)·0.5h
제약 (규칙 스위치 Rules로 켜고 끔)
    에너지 수지      soc[t+1] = soc[t] + 0.5·(ηc·c[t] - d[t]/ηd) + 주파수 응답으로 평균적으로 드나드는 에너지
    출력 여유        위쪽: (d - c) + Σ up 상품 ≤ P,  아래쪽: (c - d) + Σ down 상품 ≤ P
    SoE 규칙         구간 시작·끝 에너지가 위쪽 상품을 지속시간 동안 낼 만큼 남고, 아래쪽 상품을 받을 만큼 비어 있어야 함
    도매 겹치기 금지  (wholesale_stacking=False) 상품을 든 구간에는 도매 거래 0
    상품 쪼개기 금지  (splitting=False) 한 구간·한 방향에 상품 하나만
    물량 상한        (cap_by_cleared_volume) 그 구간 시장 전체 낙찰량보다 많이 팔 수 없음
"""
import time
from dataclasses import asdict, dataclass, field
from typing import Optional

import pandas as pd
import pulp

from .data import PRODUCTS, RESERVE, RESPONSE, SP_HOURS, expected_utilisation


@dataclass
class Battery:
    power_mw: float = 50.0
    duration_h: float = 2.0
    eta_charge: float = 0.95        # 충전 효율. 왕복효율 = 0.95 × 0.95 = 90.25% (Gale et al. 2026과 같음)
    eta_discharge: float = 0.95
    soc_min: float = 0.0            # 저장 에너지 하한·상한 (용량 대비 비율)
    soc_max: float = 1.0
    soc_init: float = 0.5           # 시작 에너지. 끝에도 이만큼은 남겨야 함 (기간 끝에 다 팔아 버리는 것 방지)
    throughput_cost: float = 0.5    # £/MWh, 충전·방전 각각. 열화 대리 비용 (Gale et al. 2026과 같음)
    max_cycles_per_day: Optional[float] = None  # 하루 방전량 ≤ N × 용량. None이면 제한 없음

    @property
    def energy_mwh(self):
        return self.power_mw * self.duration_h


@dataclass
class Rules:
    services: tuple = tuple(RESPONSE + RESERVE)  # 참여할 수 있는 상품
    soe_rule: bool = True               # 2024년 SoE 규칙: 낙찰 물량만큼 에너지를 확보
    wholesale_stacking: bool = True     # 상품을 든 구간에도 도매 거래 허용 (2021년 DC+BM 겹치기 허용 이후)
    splitting: bool = True              # 한 구간에 같은 방향 상품 여러 개로 쪼개 팔기 허용 (EAC 공동최적화)
    cap_by_cleared_volume: bool = True  # 시장 전체 낙찰량을 넘게 팔지 못함 (가격 수용자 가정의 보완)


@dataclass
class Built:
    model: pulp.LpProblem
    c: dict
    d: dict
    u: dict
    soc: dict
    rt: dict                       # rt[p][t] = 구간 t에서 상품 p 물량 변수 (낙찰 구간 w의 변수를 공유)
    terms: dict = field(default_factory=dict)


def build(inp, bat: Battery, rules: Rules, relax=False, freq_sigma_hz=0.06, binary_periods=None):
    """freq_sigma_hz: 주파수 편차 표준편차(Hz). DC/DM/DR을 들고 있으면 평균적으로 이만큼 에너지가 드나든다.
    0.06은 1초 주파수 자료로 보정하기 전의 임시값. None이면 이 에너지를 무시한다 (상한 계산용).
    binary_periods: 충전/방전 모드를 이진 변수로 둘 구간. None이면 도매가격 ≤ 0인 구간
    (그 밖의 구간에서 동시 충방전이 생기면 solve_exact가 그 구간을 더해 다시 푼다)."""
    n, dt = len(inp.index), SP_HOURS
    T = range(n)
    P, E = bat.power_mw, bat.energy_mwh
    alpha = expected_utilisation(freq_sigma_hz) if freq_sigma_hz else {}
    m = pulp.LpProblem("layer1", pulp.LpMaximize)

    c = pulp.LpVariable.dicts("charge", T, 0, P)
    d = pulp.LpVariable.dicts("discharge", T, 0, P)
    soc = pulp.LpVariable.dicts("soc", range(n + 1), bat.soc_min * E, bat.soc_max * E)
    if binary_periods is None:
        binary_periods = {t for t in T if inp.wholesale.iat[t] <= 0}
    u = {t: pulp.LpVariable(f"is_charging_{t}", 0, 1,
                            "Binary" if (t in binary_periods and not relax) else "Continuous") for t in T}

    # 상품 물량 변수: 낙찰 구간(EFA 블록 또는 30분)마다 하나. 같은 블록의 8개 구간이 같은 변수를 쓴다
    r, rt = {}, {}
    for p in rules.services:
        if p not in inp.price:
            continue
        rt[p] = {}
        for t in T:
            w, price = inp.window[p].iat[t], inp.price[p].iat[t]
            if pd.isna(w) or pd.isna(price):
                continue
            if (p, w) not in r:
                ub = P
                if rules.cap_by_cleared_volume:
                    ub = min(P, max(0.0, float(inp.cleared[p].iat[t])))
                r[(p, w)] = pulp.LpVariable(f"r_{p}_{len(r)}", 0, ub)
            rt[p][t] = r[(p, w)]

    def side(t, direction):
        return [(p, rt[p][t]) for p in rt if PRODUCTS[p][0] == direction and t in rt[p]]

    # 목적함수
    wholesale = pulp.lpSum(float(inp.wholesale.iat[t]) * (d[t] - c[t]) * dt for t in T)
    services = {p: pulp.lpSum(float(inp.price[p].iat[t]) * v * dt for t, v in rt[p].items()) for p in rt}
    cost = pulp.lpSum(bat.throughput_cost * (c[t] + d[t]) * dt for t in T)
    m += wholesale + pulp.lpSum(services.values()) - cost

    # 시작·끝 에너지
    m += soc[0] == bat.soc_init * E, "soc_start"
    m += soc[n] >= bat.soc_init * E, "soc_end"

    for t in T:
        up, down = side(t, "up"), side(t, "down")
        # 주파수 응답으로 평균적으로 나가는(L) 에너지와 들어오는(H) 에너지. 이 에너지는 따로 돈을 받지 않으므로
        # (불균형 정산에서 중립 처리) 빠진 만큼 도매에서 다시 사 와야 한다
        fr_out = pulp.lpSum(alpha.get(p, 0.0) * v for p, v in up)
        fr_in = pulp.lpSum(alpha.get(p, 0.0) * v for p, v in down)
        # 에너지 수지: 충전은 손실만큼 덜 쌓이고, 방전은 손실만큼 더 빠진다
        m += soc[t + 1] == soc[t] + dt * (bat.eta_charge * (c[t] + fr_in) - (d[t] + fr_out) / bat.eta_discharge), \
            f"energy_{t}"
        # 동시 충방전 금지 (음의 가격에서 손실로 에너지를 태워 돈을 받는 비현실적 해 방지)
        m += c[t] <= P * u[t], f"mode_c_{t}"
        m += d[t] <= P * (1 - u[t]), f"mode_d_{t}"

        # 출력 여유: 기준 출력(d - c)에서 위로 올릴 수 있는 폭과 아래로 내릴 수 있는 폭
        m += d[t] - c[t] + pulp.lpSum(v for _, v in up) <= P, f"headroom_up_{t}"
        m += c[t] - d[t] + pulp.lpSum(v for _, v in down) <= P, f"headroom_down_{t}"

        if rules.soe_rule and (up or down):
            need_up = pulp.lpSum(v * PRODUCTS[p][1] for p, v in up) / bat.eta_discharge
            need_down = pulp.lpSum(v * PRODUCTS[p][1] for p, v in down) * bat.eta_charge
            for k in (t, t + 1):  # 구간 시작과 끝 모두 (구간 안에서 에너지는 직선으로 변함)
                m += soc[k] >= bat.soc_min * E + need_up, f"soe_up_{t}_{k - t}"
                m += soc[k] <= bat.soc_max * E - need_down, f"soe_down_{t}_{k - t}"


    if not rules.wholesale_stacking:
        # 상품을 든 구간에는 도매 거래 금지. 상품을 든다는 결정은 낙찰 구간(EFA 블록 또는 30분)마다 하나
        y = {}
        for (p, w), v in r.items():
            key = ("block", w) if p in RESPONSE else ("sp", w)
            if key not in y:
                y[key] = pulp.LpVariable(f"holds_{key[0]}_{len(y)}", cat="Binary")
            m += v <= P * y[key], f"stack_{v.name}"
        for t in T:
            keys = {("block", inp.window[p].iat[t]) if p in RESPONSE else ("sp", inp.window[p].iat[t])
                    for p, _ in side(t, "up") + side(t, "down")}
            for i, key in enumerate(sorted(keys, key=str)):
                m += c[t] + d[t] <= P * (1 - y[key]), f"no_trade_{t}_{i}"

    if not rules.splitting:
        # EAC 이전처럼 DC/DM/DR 중 한 블록·한 방향에 상품 하나만 (예비력 BR/QR/SR은 30분 단위라 따로 둔다)
        z = {key: pulp.LpVariable(f"pick_{i}", cat="Binary") for i, key in enumerate(r) if key[0] in RESPONSE}
        for key, zv in z.items():
            m += r[key] <= P * zv, f"split_{zv.name}"
        done = set()
        for t in T:
            for direction in ("up", "down"):
                keys = tuple(sorted((p, inp.window[p].iat[t]) for p, _ in side(t, direction) if p in RESPONSE))
                if len(keys) > 1 and keys not in done:
                    done.add(keys)
                    m += pulp.lpSum(z[k] for k in keys) <= 1, f"one_product_{direction}_{t}"

    if bat.max_cycles_per_day:
        days = pd.Series(range(n), index=inp.index).groupby(inp.index.date)
        for day, ts in days:
            m += pulp.lpSum(d[t] * dt for t in ts) <= bat.max_cycles_per_day * E, f"cycles_{day}"

    return Built(m, c, d, u, soc, rt, {"wholesale": wholesale, "services": services, "cost": cost,
                                        "binary_periods": set(binary_periods)})


def solve(b: Built, time_limit=900, gap=1e-4, msg=False):
    solver = pulp.HiGHS(msg=msg, timeLimit=time_limit, gapRel=gap)
    if not solver.available():
        solver = pulp.PULP_CBC_CMD(msg=msg, timeLimit=time_limit, gapRel=gap)
    t0 = time.time()
    b.model.solve(solver)
    info = {"status": pulp.LpStatus[b.model.status], "solution": pulp.LpSolution.get(b.model.sol_status, "?"),
            "solver": solver.name, "seconds": round(time.time() - t0, 1), "mip_gap": None}
    try:  # HiGHS: 시간 제한에 걸리면 status는 Optimal로 나오지만 solution이 'Integer Feasible'이고 gap이 남는다
        info["mip_gap"] = float(b.model.solverModel.getInfo().mip_gap)
    except Exception:  # noqa: BLE001
        pass
    return info


def simultaneous(b: Built, tol=1e-4):
    """충전과 방전이 동시에 0보다 큰 구간."""
    return {t for t in b.c if (pulp.value(b.c[t]) or 0) > tol and (pulp.value(b.d[t]) or 0) > tol}


def solve_exact(inp, bat, rules, freq_sigma_hz=0.06, max_rounds=5, **kw):
    """이진 변수를 꼭 필요한 구간에만 두고 풀고, 동시 충방전이 나온 구간을 이진으로 바꿔 다시 푼다."""
    periods, total = None, 0.0
    for _ in range(max_rounds):
        b = build(inp, bat, rules, freq_sigma_hz=freq_sigma_hz, binary_periods=periods)
        info = solve(b, **kw)
        total += info["seconds"]
        bad = simultaneous(b) if info["status"] == "Optimal" else set()
        if not bad:
            break
        periods = b.terms["binary_periods"] | bad
    info.update(seconds=round(total, 1), binary_periods=len(b.terms["binary_periods"]), simultaneous=len(bad))
    return b, info


def results(inp, bat: Battery, b: Built):
    """운전 계획 표와 수익 요약."""
    T = range(len(inp.index))
    v = pulp.value
    df = pd.DataFrame(index=inp.index)
    df.index.name = "start_utc"
    df["wholesale_price"] = inp.wholesale
    df["charge_mw"] = [v(b.c[t]) for t in T]
    df["discharge_mw"] = [v(b.d[t]) for t in T]
    df["net_export_mw"] = df["discharge_mw"] - df["charge_mw"]
    df["soc_mwh"] = [v(b.soc[t]) for t in T]
    for p in b.rt:
        df[f"{p}_mw"] = [v(b.rt[p][t]) if t in b.rt[p] else 0.0 for t in T]
        df[f"{p}_price"] = inp.price[p]
    df = df.round(4)

    hours = len(inp.index) * SP_HOURS
    rev = {"wholesale": v(b.terms["wholesale"]) or 0.0}
    rev.update({p: v(e) or 0.0 for p, e in b.terms["services"].items()})
    rev["throughput_cost"] = -(v(b.terms["cost"]) or 0.0)
    total = sum(rev.values())
    per_mw_yr = {k: x / bat.power_mw * 8760 / hours for k, x in rev.items()}
    summary = {
        "hours": hours,
        "total_gbp": round(total, 0),
        "total_gbp_per_mw_yr": round(total / bat.power_mw * 8760 / hours, 0),
        "revenue_gbp_per_mw_yr": {k: round(x, 0) for k, x in per_mw_yr.items()},
        "discharged_mwh": round(df["discharge_mw"].sum() * SP_HOURS, 1),
        "cycles_per_day": round(df["discharge_mw"].sum() * SP_HOURS / bat.energy_mwh / (hours / 24), 2),
        "battery": asdict(bat),
    }
    return df, summary
