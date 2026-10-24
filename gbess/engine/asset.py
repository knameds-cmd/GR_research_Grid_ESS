"""
저장장치 자산 매개변수. 기술 중립 4종(리튬, 양수, CAES/LAES, 흐름전지)을 같은 틀로 표현한다.

값마다 출처(source)와 상태(status)를 둔다. status가 "placeholder"인 값으로 낸 결과에는 엔진이 경고를 붙인다.
값은 gbess/config/technologies.yaml에서 읽는다.
"""
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Optional

import yaml

CONFIG = Path(__file__).resolve().parents[1] / "config" / "technologies.yaml"


@dataclass(frozen=True)
class Asset:
    name: str
    p_dis_mw: float                  # 최대 방전(발전) 출력
    p_ch_mw: float                   # 최대 충전(양수) 입력
    e_mwh: float                     # 저장 용량 (방전 쪽 에너지가 아니라 저장된 에너지 기준)
    eta_ch: float                    # 충전 효율
    eta_dis: float                   # 방전 효율. 왕복효율 = eta_ch × eta_dis
    soc_min: float = 0.0             # 용량 대비 하한·상한
    soc_max: float = 1.0
    soc_init: float = 0.5
    var_cost: float = 0.0            # 방전 MWh당 가변비용(열화·가변 O&M), £/MWh
    self_discharge_per_h: float = 0.0
    pump_units: Optional[int] = None  # 양수처럼 충전이 유닛 단위 고정 출력이면 유닛 수. None이면 연속
    status: dict = field(default_factory=dict)   # 항목별 "sourced" / "placeholder"
    source: dict = field(default_factory=dict)

    @property
    def rte(self):
        return self.eta_ch * self.eta_dis

    @property
    def duration_h(self):
        """정격 출력으로 저장 에너지를 다 내는 시간 (방전 효율 반영)."""
        return self.e_mwh * self.eta_dis / self.p_dis_mw

    def placeholders(self):
        return sorted(k for k, v in self.status.items() if v != "sourced")

    def scaled(self, p_mw, duration_h):
        """같은 기술로 출력·지속시간만 바꾼 자산."""
        e = duration_h * p_mw / self.eta_dis
        units = self.pump_units
        return replace(self, name=f"{self.name}_{p_mw:g}MW_{duration_h:g}h", p_dis_mw=p_mw,
                       p_ch_mw=p_mw * self.p_ch_mw / self.p_dis_mw, e_mwh=e, pump_units=units)


def load_technologies(path=CONFIG):
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    out = {}
    for key, spec in raw["technologies"].items():
        vals = {k: v["value"] for k, v in spec["params"].items()}
        status = {k: v.get("status", "placeholder") for k, v in spec["params"].items()}
        source = {k: v.get("source", "") for k, v in spec["params"].items()}
        out[key] = Asset(name=key, status=status, source=source, **vals)
    return out
