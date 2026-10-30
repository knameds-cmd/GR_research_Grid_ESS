"""
기술·비용 입력 (11 문서 #6, 09 문서 4.5). 기술별 건설비·운영비·교체 투자·수명을 1차 자료 값 그대로(원래 통화·연도) 받아
2025년 실질 £(CPIH)로 바꾸고, 자산 크기(출력 MW × 지속시간 h)에서 cap-and-floor 재무층(gbess.finance.cap_floor.evaluate)에
넣을 값(capex = RAV, opex, repex 계획, 잔존가치)과 엔진에 넣을 가변비용(£/MWh)을 만든다.

    from gbess.finance.costs import project_costs
    c = project_costs("li_ion", 400, 8)              # 중앙값
    c = project_costs("psh", 1440, 22.3, case="high")

값: gbess/config/costs.yaml. 출처와 쪽 번호: literature/sources/tech/TECH_SOURCES.md.
가격 기준: 2025년 실질 £. 외화는 자료 연도의 연평균 환율(영국은행 XUAAUSS·XUAAERS)로 £로 바꾼 뒤, CPIH(ONS L522
연평균)로 2025년까지 올린다(환산 먼저, 물가 나중). 원자료: data/raw/macro/.
정의
  - 에너지 단가(£/kWh)는 정격 출력 × 지속시간(= 내보낼 수 있는 kWh) 기준이다. 엔진의 e_mwh(저장 기준, 방전 효율로 나눈 값)와
    다르다.
  - construction = 출력 단가 × kW + 에너지 단가 × kWh. devex_grid = 개발비 + 계통 접속 £/kW × kW (자료 capex에 들어 있지
    않을 때만, 예: Mott MacDonald 계열). 건설 중 이자(IDC): (construction + devex_grid)를 build_years 동안 고르게 쓰고 운전
    시작 시점까지 idc_rate로 복리 환산. capex(RAV, 운전 시작 시점) = construction + devex_grid + IDC. Ofgem RAV 구성(TDD p40–41)과 같다. 예비품·금융 비용은 뺀다.
  - opex = 고정 운영비(£/kW·년 × kW + £/kWh·년 × kWh). 통과 비용(망요금·지방세·면허료)은 제외(cap·floor 밖, TDD p41).
  - repex: replacements(정해진 해에 출력·에너지 부분의 일부를 다시 삼)와 리튬 보강(augmentation). 보강은 Ofgem 조건
    "25년 내내 정격 출력으로 8시간 이상"(TDD p19, MTD 5.6)을 지키려고 줄어든 용량을 augmentation_years마다 채운다.
    줄어드는 양 = (달력 열화 + 사이클당 열화 × 연 사이클) × kWh × 경과 연수(선형). 보강 단가는 augmentation_cost(셀·모듈
    부분만, PNNL 방식)를 그해까지 energy_cost_trend(실질 연 변화율)로 낮춘 값.
  - 엔진 가변비용(var_cost, £/MWh 방전) = 가변 운영비 + 사이클 열화의 한계 비용(사이클당 열화 × 보강 단가 × 1000).
    엔진이 이 값을 쓰면 재무층에서는 사이클 열화 보강을 다시 빼지 않도록 cycles_per_year=0으로 부른다(이중 계산 방지).
  - 잔존가치: Ofgem 편익·비용 분석의 잔여 가치 규칙(MTD 5.19)과 같이 (capex + repex) × max(0, 경제 수명 − 25) ÷ 경제 수명.
    제도 안의 잔존가치는 사업마다 다르고 공개되지 않았다(MTD 6.11). residual="none"이면 0.
  - case: "central"/"low"/"high". 값마다 low·high가 없으면 central을 쓴다. low = 싼 쪽(사업자에게 유리), high = 비싼 쪽.
status가 sourced(1차 자료에서 읽음)나 derived(1차 자료 값으로 계산)가 아닌 값이 쓰이면 결과의 placeholders에 남는다.
"""
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).resolve().parents[1] / "config" / "costs.yaml"
MACRO = ROOT / "data" / "raw" / "macro"
BASE_YEAR = 2025
CASES = ("central", "low", "high")


@lru_cache(maxsize=None)
def _macro():
    c = pd.read_csv(MACRO / "ons_cpih_index_l522.csv", header=None, names=["k", "v"])
    c = c[c["k"].astype(str).str.fullmatch(r"\d{4}")]
    cpih = {int(k): float(v) for k, v in zip(c["k"], c["v"])}
    fx = pd.read_csv(MACRO / "boe_fx_annual.csv")
    fx["year"] = pd.to_datetime(fx["DATE"], format="%d %b %Y").dt.year
    usd = dict(zip(fx["year"], fx["XUAAUSS"]))   # US$ per £
    eur = dict(zip(fx["year"], fx["XUAAERS"]))   # € per £
    return cpih, {"USD": usd, "EUR": eur}


def to_base(value, currency, year, base_year=BASE_YEAR):
    """원래 통화·연도의 금액 → base_year 실질 £."""
    cpih, fx = _macro()
    if currency == "GBP":
        gbp = value
    elif currency in fx:
        gbp = value / fx[currency][year]
    else:
        raise ValueError(f"통화 {currency}")
    return gbp * cpih[base_year] / cpih[year]


def load_costs(path=CONFIG):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["technologies"]


def load_assets(path=CONFIG):
    """대표 자산 {이름: (기술, MW, h)}. Window 1 신청 사업 범위에서 정한다(costs.yaml의 assets)."""
    a = yaml.safe_load(Path(path).read_text(encoding="utf-8"))["assets"]
    return {k: (x["tech"], x["p_mw"], x["duration_h"]) for k, x in a.items()}


@dataclass(frozen=True)
class ProjectCost:
    tech: str
    case: str
    p_mw: float
    duration_h: float
    capex: float                 # RAV, 운전 시작 시점, 2025년 실질 £
    opex: float                  # £/년
    repex: np.ndarray            # 운전 연도 1..n의 교체 투자 £
    residual_value: float        # 시점 n의 잔존가치 £
    var_cost: float              # 엔진 가변비용 £/MWh 방전
    life_years: float
    breakdown: dict = field(default_factory=dict)
    placeholders: tuple = ()
    sources: dict = field(default_factory=dict)

    def per_kw(self):
        """비교용 요약 (£/kW, £/kWh)."""
        kw, kwh = self.p_mw * 1e3, self.p_mw * 1e3 * self.duration_h
        return {"capex_per_kw": self.capex / kw, "capex_per_kwh": self.capex / kwh, "opex_per_kw_yr": self.opex / kw,
                "repex_per_kw": float(self.repex.sum()) / kw, "residual_per_kw": self.residual_value / kw}


def project_costs(tech, p_mw, duration_h, case="central", cycles_per_year=None, regime_years=25,
                  residual="economic_life", costs=None):
    """cycles_per_year: 리튬 사이클 열화 보강을 계산할 연 등가 완전 사이클 수. None이면 표의 ref_cycles_per_year,
    0이면 사이클 열화 보강을 넣지 않는다(엔진 var_cost가 그 비용을 이미 낸 경우)."""
    if case not in CASES:
        raise ValueError(f"case {case}")
    spec = (costs or load_costs())[tech]
    used, ph, src = {}, set(), {}

    def v(key, default=None):
        """경우(case)의 값을 2025년 실질 £로. 경우 값이 dict면 그 안의 통화·연도·출처가 매개변수 공통값보다 앞선다."""
        p = spec.get(key)
        if p is None:
            if default is None:
                raise KeyError(f"{tech}: {key} 없음")
            return default
        if not isinstance(p, dict):
            return p
        x = p.get(case, p["central"])
        meta = {k: p.get(k) for k in ("currency", "year", "status", "source")}
        if isinstance(x, dict):
            meta.update({k: x[k] for k in ("currency", "year", "status", "source") if k in x})
            x = x["value"]
        if (meta["status"] or "placeholder") not in ("sourced", "derived"):
            ph.add(key)
        src[key] = meta["source"] or ""
        if meta["currency"]:
            x = to_base(x, meta["currency"], meta["year"])
        used[key] = x
        return x

    kw, kwh = p_mw * 1e3, p_mw * 1e3 * duration_h
    n = regime_years
    c_pow, c_en = v("capex_power"), v("capex_energy")
    construction = c_pow * kw + c_en * kwh
    devex_grid = v("devex_grid", 0.0) * kw
    build, r_idc = int(v("build_years", 1)), v("idc_rate", 0.0)
    idc_factor = float(np.mean([(1 + r_idc) ** (k + 0.5) for k in range(build)]))
    idc = (construction + devex_grid) * (idc_factor - 1)
    capex = construction + devex_grid + idc
    opex = v("fixed_om_power", 0.0) * kw + v("fixed_om_energy", 0.0) * kwh

    repex = np.zeros(n)
    for i, ev in enumerate(spec.get("replacements", [])):
        y = int(ev["year"])
        if 1 <= y <= n:
            if "cost_per_kw" in ev:   # 원래 통화의 절대 단가 (예: 흐름전지 스택 교체 $/kW)
                c = ev["cost_per_kw"]
                repex[y - 1] += to_base(c.get(case, c["central"]), c["currency"], c["year"]) * kw
            else:
                part = c_pow * kw if ev["part"] == "power" else c_en * kwh
                repex[y - 1] += ev["share"] * part
            src[f"replacement_{i}"] = ev.get("source", "")
            if ev.get("status", "placeholder") != "sourced":
                ph.add("replacements")
    if "augmentation_years" in spec:
        k = int(v("augmentation_years"))
        cyc = v("ref_cycles_per_year", 0.0) if cycles_per_year is None else cycles_per_year
        fade = v("fade_calendar", 0.0) + v("fade_per_cycle", 0.0) * cyc
        trend, c_aug = v("energy_cost_trend", 0.0), v("augmentation_cost")
        for y in range(k, n, k):   # 마지막 해(n)에는 보강하지 않는다
            repex[y - 1] += fade * k * kwh * c_aug * (1 + trend) ** y

    life = v("life_years")
    rv = 0.0
    if residual == "economic_life":
        rv = (capex + repex.sum()) * max(0.0, life - n) / life
    elif residual != "none":
        raise ValueError(f"residual {residual}")
    c_aug = v("augmentation_cost") if "augmentation_cost" in spec else 0.0
    var_cost = v("var_om", 0.0) + v("fade_per_cycle", 0.0) * c_aug * 1e3
    bd = {"construction": construction, "devex_grid": devex_grid, "idc": idc, **{f"unit_{k_}": x for k_, x in used.items()}}
    return ProjectCost(tech=tech, case=case, p_mw=p_mw, duration_h=duration_h, capex=capex, opex=opex, repex=repex,
                       residual_value=rv, var_cost=var_cost, life_years=life, breakdown=bd,
                       placeholders=tuple(sorted(ph)), sources=src)


def table(assets=None, cases=CASES):
    """대표 자산별 비용 요약 표 (2025년 실질 £). assets: {이름: (기술, MW, h)}."""
    costs = load_costs()
    assets = assets or load_assets()
    rows = []
    for name, (tech, p, d) in assets.items():
        for cs in cases:
            c = project_costs(tech, p, d, case=cs, costs=costs)
            rows.append({"asset": name, "case": cs, "p_mw": p, "duration_h": d, "capex_m": c.capex / 1e6,
                         "opex_m_yr": c.opex / 1e6, "repex_m": c.repex.sum() / 1e6,
                         "residual_m": c.residual_value / 1e6, "var_cost": c.var_cost, "life": c.life_years,
                         **c.per_kw(), "placeholders": ",".join(c.placeholders)})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    print(table().round(1).to_string(index=False))
