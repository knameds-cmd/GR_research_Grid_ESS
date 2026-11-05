"""
구조층 2단계 모형의 공용 부품: 구역망 자료, LP 조립, 경계 조류 (docs/IMPLEMENTATION_A_KO.md 2장).

구역망은 북→남 방사형 사슬이다. 구역 z = 0(가장 북쪽) … Z−1, 경계 l은 구역 l과 l+1 사이. 경계 조류 f[l,t]는 남쪽으로 가면 +.
사슬이므로 경계 조류는 구역 순위치로 유일하게 정해진다: f[l,t] = Σ_{z ≤ l} (발전 + 방전 − 충전 + 정전 − 수요)[z,t].

한 번의 운전 문제(1단계·2단계·계획자 최적 모두 같은 틀)
    변수   p[g,t] 발전, ch[s,t]·d[s,t] 충·방전, e[s,t] 구간 t 끝 저장량, shed[z,t] 정전, (망 제약이면) f[l,t]
    비용   Σ c_g·p + Σ var_s·d + VoLL·Σ shed   (모두 × dt)
    수지   network=False: 전국 하나 Σ_z(…) = Σ_z D       (쌍대 = 전국 가격 λ[t])
           network=True : 구역마다 (…)[z] + f[z−1] − f[z] = D[z],  −F_l ≤ f[l] ≤ F_l   (쌍대 = 구역 가격)
    저장   e[t] = e[t−1] + dt·(η_ch·ch[t] − d[t]/η_dis),  e[−1] = soc0·E,  0 ≤ e ≤ E,  terminal="geq_init"이면 e[T−1] ≥ e[−1]
    고정   fixed={저장 이름: (ch, d)}이면 그 저장의 충·방전을 그 값으로 묶음 (재급전 i·iii)
    한도   caps={저장 이름: (ch 상한, d 상한)} (설계안 S1a·S1b)
scipy.optimize.linprog(HiGHS)에 희소행렬로 넘긴다. 쌍대값은 eqlin.marginals(우변 1 단위당 목적함수 변화)다.
"""
import time
from dataclasses import dataclass, field

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog


@dataclass
class Gen:
    name: str
    zone: int
    cap: float                     # MW
    cost: float                    # £/MWh
    avail: object = None           # 길이 T 배열(가용률 0~1) 또는 None(늘 1)
    renewable: bool = False        # 출력제한 집계용


@dataclass
class Store:
    name: str
    zone: int
    p_ch: float                    # MW
    p_dis: float                   # MW
    e_mwh: float                   # 저장 용량 MWh
    eta_ch: float = 1.0
    eta_dis: float = 1.0
    soc0: float = 0.5              # 시작 저장량 ÷ 용량
    var_cost: float = 0.0          # £/MWh 방전
    tags: frozenset = frozenset()  # 예: {"w1", "north"}


@dataclass
class Network:
    zones: list                    # 북 → 남 순서의 구역 이름
    demand: np.ndarray             # (Z, T) MW
    limits: np.ndarray             # (Z−1,) 또는 (Z−1, T) MW, 경계 l = 구역 l | l+1
    gens: list
    stores: list
    voll: float = 17000.0          # £/MWh (spec.yaml model.voll_gbp_mwh)
    dt: float = 1.0                # 시간
    terminal: str = "geq_init"     # 또는 None (끝 저장량 제약 없음)

    def __post_init__(self):
        self.demand = np.atleast_2d(np.asarray(self.demand, float))
        Z, T = self.demand.shape
        if Z != len(self.zones):
            raise ValueError("demand 행 수 ≠ 구역 수")
        lim = np.asarray(self.limits, float)
        self.limits = np.broadcast_to(lim.reshape(Z - 1, -1), (Z - 1, T)).copy()

    @property
    def T(self):
        return self.demand.shape[1]

    @property
    def Z(self):
        return len(self.zones)

    def gen_ub(self):
        return np.array([g.cap * (np.ones(self.T) if g.avail is None else np.asarray(g.avail, float)) for g in self.gens])

    def store_names(self, tag=None):
        return [s.name for s in self.stores if tag is None or tag in s.tags]

    def scaled_limits(self, k):
        out = Network(self.zones, self.demand, self.limits * k, self.gens, self.stores, self.voll, self.dt, self.terminal)
        return out


@dataclass
class Dispatch:
    """한 번 푼 운전 결과. 배열은 (단위 수, T)."""
    p: np.ndarray
    ch: np.ndarray
    d: np.ndarray
    e: np.ndarray
    shed: np.ndarray               # (Z, T)
    cost: float                    # 이 운전의 계통 비용 £
    flows: np.ndarray              # (Z−1, T) 경계 조류 (망 제약 없는 1단계면 암묵적 조류)
    prices: np.ndarray             # 1단계: (T,) 전국 가격 λ / 망 제약: (Z, T) 구역 가격. 쌍대가 없으면 None
    status: str
    seconds: float
    extra: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------------------------------------------
class _Rows:
    def __init__(self):
        self.r, self.c, self.v, self.rhs, self.m = [], [], [], [], 0

    def add(self, rhs, terms):
        """terms = [(열 번호 배열 (R,) 또는 (R,k), 계수 스칼라·(R,)·(R,k))]. 새 행 번호를 돌려준다."""
        rhs = np.asarray(rhs, float).ravel()
        R = len(rhs)
        rows = np.arange(self.m, self.m + R)
        for cols, coef in terms:
            cols = np.asarray(cols).reshape(R, -1)
            coef = np.asarray(coef, float)
            if coef.ndim == 1 and coef.size == R and cols.shape[1] != R:
                coef = coef.reshape(R, 1)
            coef = np.broadcast_to(coef, cols.shape)
            self.r.append(np.repeat(rows, cols.shape[1]))
            self.c.append(cols.ravel())
            self.v.append(coef.ravel())
        self.rhs.append(rhs)
        self.m += R
        return rows

    def matrix(self, n):
        if self.m == 0:
            return None, None
        A = sp.csr_matrix((np.concatenate(self.v), (np.concatenate(self.r), np.concatenate(self.c))), shape=(self.m, n))
        return A, np.concatenate(self.rhs)


class LP:
    """변수 묶음과 제약 행을 쌓아 linprog(HiGHS)로 최소화한다."""

    def __init__(self):
        self.n = 0
        self._c, self._lb, self._ub = [], [], []
        self.eq, self.le = _Rows(), _Rows()

    def var(self, shape, lb=0.0, ub=np.inf, cost=0.0):
        k = int(np.prod(shape))
        idx = np.arange(self.n, self.n + k).reshape(shape)
        self.n += k
        self._c.append(np.broadcast_to(np.asarray(cost, float), shape).ravel().copy())
        self._lb.append(np.broadcast_to(np.asarray(lb, float), shape).ravel().copy())
        self._ub.append(np.broadcast_to(np.asarray(ub, float), shape).ravel().copy())
        return idx

    def solve(self, c_override=None):
        c = np.concatenate(self._c) if c_override is None else c_override
        lb, ub = np.concatenate(self._lb), np.concatenate(self._ub)
        A_eq, b_eq = self.eq.matrix(self.n)
        A_ub, b_ub = self.le.matrix(self.n)
        t0 = time.perf_counter()
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=np.column_stack([lb, ub]), method="highs")
        res.seconds = time.perf_counter() - t0
        if res.status != 0:
            raise RuntimeError(f"LP 풀이 실패: {res.message}")
        return res

    def cost_vector(self):
        return np.concatenate(self._c)

    def set_bounds(self, idx, lb=None, ub=None):
        lbv, ubv = np.concatenate(self._lb), np.concatenate(self._ub)
        if lb is not None:
            lbv[np.ravel(idx)] = np.ravel(lb)
        if ub is not None:
            ubv[np.ravel(idx)] = np.ravel(ub)
        self._lb, self._ub = [lbv], [ubv]


@dataclass
class Block:
    """LP 안에 만든 운전 문제 한 벌의 변수 번호와 비용 항."""
    p: np.ndarray
    ch: np.ndarray
    d: np.ndarray
    e: np.ndarray
    shed: np.ndarray
    f: object                      # (Z−1, T) 또는 None
    balance_rows: np.ndarray       # 쌍대를 읽을 등식 행 번호. 1단계: (T,), 망: (Z, T)
    cost_idx: np.ndarray
    cost_coef: np.ndarray
    store_rows: object = None      # (S, T) 저장 수지 등식 행 번호. 쌍대의 부호를 바꾸면 그 구간에 쓸 수 있는 에너지 1 MWh의 값(물 가치)
    terminal_rows: object = None   # (S,) 끝 저장량 제약(≤) 행 번호


def add_dispatch(lp, net, network, fixed=None, caps=None):
    """LP에 운전 문제 한 벌을 더한다. 목적함수 계수는 그 벌의 계통 비용으로 들어간다."""
    Z, T, dt = net.Z, net.T, net.dt
    G, S = len(net.gens), len(net.stores)
    gc = np.array([g.cost for g in net.gens]).reshape(G, 1)
    p = lp.var((G, T), 0.0, net.gen_ub(), gc * dt)
    pch = np.array([s.p_ch for s in net.stores]).reshape(S, 1)
    pdis = np.array([s.p_dis for s in net.stores]).reshape(S, 1)
    vc = np.array([s.var_cost for s in net.stores]).reshape(S, 1)
    E = np.array([s.e_mwh for s in net.stores]).reshape(S, 1)
    ch = lp.var((S, T), 0.0, np.broadcast_to(pch, (S, T)))
    d = lp.var((S, T), 0.0, np.broadcast_to(pdis, (S, T)), vc * dt)
    e = lp.var((S, T), 0.0, np.broadcast_to(E, (S, T)))
    shed = lp.var((Z, T), 0.0, net.demand, net.voll * dt)
    names = [s.name for s in net.stores]
    for name, (cu, du) in (caps or {}).items():
        i = names.index(name)
        lp.set_bounds(ch[i], ub=np.minimum(np.broadcast_to(cu, T), net.stores[i].p_ch))
        lp.set_bounds(d[i], ub=np.minimum(np.broadcast_to(du, T), net.stores[i].p_dis))
    for name, (cf, df) in (fixed or {}).items():
        i = names.index(name)
        lp.set_bounds(ch[i], lb=cf, ub=cf)
        lp.set_bounds(d[i], lb=df, ub=df)

    # 저장 수지
    store_rows = terminal_rows = None
    if S:
        eta_c = np.array([s.eta_ch for s in net.stores]).reshape(S, 1)
        eta_d = np.array([s.eta_dis for s in net.stores]).reshape(S, 1)
        e0 = np.array([s.soc0 * s.e_mwh for s in net.stores])
        r0 = lp.eq.add(e0, [(e[:, 0], 1.0), (ch[:, 0], -dt * eta_c[:, 0]), (d[:, 0], dt / eta_d[:, 0])])
        store_rows = np.zeros((S, T), int)
        store_rows[:, 0] = r0
        if T > 1:
            R = S * (T - 1)
            rows_t = lp.eq.add(np.zeros(R), [(e[:, 1:].ravel(), 1.0), (e[:, :-1].ravel(), -1.0),
                                    (ch[:, 1:].ravel(), np.broadcast_to(-dt * eta_c, (S, T - 1)).ravel()),
                                    (d[:, 1:].ravel(), np.broadcast_to(dt / eta_d, (S, T - 1)).ravel())])
            store_rows[:, 1:] = rows_t.reshape(S, T - 1)
        if net.terminal == "geq_init":
            terminal_rows = lp.le.add(-e0, [(e[:, -1], -1.0)])

    # 수지
    gz = np.array([g.zone for g in net.gens], int)
    sz = np.array([s.zone for s in net.stores], int)
    f = None
    if network:
        f = lp.var((Z - 1, T), -net.limits, net.limits)
        rows = np.zeros((Z, T), int)
        for z in range(Z):
            terms = [(p[gz == z].T, 1.0), (d[sz == z].T, 1.0), (ch[sz == z].T, -1.0), (shed[z][:, None], 1.0)]
            if z > 0:
                terms.append((f[z - 1][:, None], 1.0))
            if z < Z - 1:
                terms.append((f[z][:, None], -1.0))
            terms = [(cols, coef) for cols, coef in terms if cols.shape[1] > 0]
            rows[z] = lp.eq.add(net.demand[z], terms)
    else:
        rows = lp.eq.add(net.demand.sum(axis=0), [(p.T, 1.0), (d.T, 1.0), (ch.T, -1.0), (shed.T, 1.0)])

    cost_idx = np.concatenate([p.ravel(), d.ravel(), shed.ravel()])
    cost_coef = np.concatenate([np.broadcast_to(gc * dt, (G, T)).ravel(), np.broadcast_to(vc * dt, (S, T)).ravel(),
                                np.full(Z * T, net.voll * dt)])
    return Block(p, ch, d, e, shed, f, rows, cost_idx, cost_coef, store_rows if S else None,
                 terminal_rows if S and net.terminal == "geq_init" else None)


def implicit_flows(net, p, ch, d, shed):
    """사슬 구조의 경계 조류: f[l] = Σ_{z ≤ l} 순공급[z]."""
    Z, T = net.Z, net.T
    inj = np.zeros((Z, T)) - net.demand + shed
    for i, g in enumerate(net.gens):
        inj[g.zone] += p[i]
    for i, s in enumerate(net.stores):
        inj[s.zone] += d[i] - ch[i]
    return np.cumsum(inj, axis=0)[:-1]


def read(net, lp_res, blk, network):
    x = lp_res.x
    p, ch, d, e, shed = (x[blk.p], x[blk.ch], x[blk.d], x[blk.e], x[blk.shed])
    cost = float(blk.cost_coef @ x[blk.cost_idx])
    flows = x[blk.f] if network else implicit_flows(net, p, ch, d, shed)
    prices = None
    if lp_res.eqlin is not None and lp_res.eqlin.marginals is not None and len(lp_res.eqlin.marginals):
        prices = lp_res.eqlin.marginals[blk.balance_rows] / net.dt
    out = Dispatch(p, ch, d, e, shed, cost, flows, prices, lp_res.message, lp_res.seconds)
    if prices is not None and blk.store_rows is not None:
        # 저장 수지 행 t의 우변은 구간 t 끝 저장량에 넣는 에너지라, 쌍대의 부호를 바꾸면 그 1 MWh의 값이다 (£/MWh)
        out.extra["water_value"] = -lp_res.eqlin.marginals[blk.store_rows]
        wv_end = np.zeros(len(net.stores))
        if blk.terminal_rows is not None:
            wv_end = -lp_res.ineqlin.marginals[blk.terminal_rows]   # 연말 저장량 1 MWh의 값
        out.extra["water_value_end"] = wv_end
    return out


def solve_dispatch(net, network, fixed=None, caps=None):
    lp = LP()
    blk = add_dispatch(lp, net, network, fixed, caps)
    return read(net, lp.solve(), blk, network)


def curtailment(net, p):
    ub = net.gen_ub()
    ren = np.array([g.renewable for g in net.gens], bool)
    return float((ub[ren] - p[ren]).sum() * net.dt)
