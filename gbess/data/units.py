"""
저장장치 BM 유닛 등록표: 유닛, 기술(psh / battery), 등록 출력, 구역, 스코틀랜드 여부(= B6 북쪽).

    from gbess.data.units import storage_units
    u = storage_units()

- 양수발전: Elexon 등록부 fuelType == "PS".
- 배터리: NESO skip rate 자료에서 fuel == "BATTERY"로 표시된 유닛 (2024-12 이후 활동한 유닛). 그 전에 퇴출된 배터리는 빠진다.
- 구역: 배전망 연결 유닛은 등록부의 GSP 그룹. 송전망 직접 연결(T형)은 GSP 그룹이 비어 있어서,
  송전손실계수(TLF)가 같은 구역 안에서는 같은 값이라는 점을 이용해 GSP 그룹이 있는 유닛의 TLF와 맞춘다.
  같은 값이 없으면 가장 가까운 대표값의 구역을 쓰고 zone_method에 "tlf_nearest"로 남긴다.
  검산(2026-10-24): Dinorwig·Ffestiniog → Merseyside North Wales, Cruachan → South Scotland, Foyers → North Scotland,
  Lakeside·Pillswood → Yorkshire로 실제 위치와 일치.
- 등록 출력과 TLF는 등록부의 현재 값(스냅숏)이다. 과거에 바뀐 값은 반영하지 못한다.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
SCOTLAND = {"North Scotland", "South Scotland", "NORTH of SCOTLAND GSP", "SOUTH of SCOTLAND GSP"}
ZONE_ALIASES = {"NORTH of SCOTLAND GSP": "North Scotland", "SOUTH of SCOTLAND GSP": "South Scotland",
                "Yorkshire Electricity": "Yorkshire", "_F - Northern": "Northern"}


def _battery_names():
    f = RAW / "skip_rates" / "skip_rate_in_merit_all_balancing_mechanism_september_2026.csv"
    s = pd.read_csv(f, usecols=["bm_unit", "fuel"])
    return set(s.loc[s["fuel"] == "BATTERY", "bm_unit"])


def bm_units():
    """등록부의 모든 BM 유닛과 구역. 구역 규칙은 이 파일 머리말과 같다."""
    b = pd.read_csv(RAW / "elexon_bmunits.csv")
    b["zone"] = b["gspGroupName"].replace(ZONE_ALIASES)
    known = b[b["zone"].notna() & b["transmissionLossFactor"].notna()]
    modal = known.groupby("transmissionLossFactor")["zone"].agg(lambda s: s.value_counts().index[0])
    counts = known.groupby("transmissionLossFactor").size()
    rep = modal[counts >= 3]   # 대표값: 3개 이상 유닛이 같은 TLF를 쓰는 값
    b["zone_method"] = np.where(b["zone"].notna(), "gsp", None)
    miss = b["zone"].isna() & b["transmissionLossFactor"].notna()
    tlf = b.loc[miss, "transmissionLossFactor"]
    exact = tlf.map(modal)
    near = tlf.map(lambda v: rep.iloc[int(np.abs(rep.index.to_numpy() - v).argmin())])
    b.loc[miss, "zone"] = exact.fillna(near)
    b.loc[miss, "zone_method"] = np.where(exact.notna(), "tlf_exact", "tlf_nearest")
    b["scotland"] = b["zone"].isin({ZONE_ALIASES.get(z, z) for z in SCOTLAND})
    return b.rename(columns={"elexonBmUnit": "bmUnit", "generationCapacity": "mw"})


def storage_units():
    u = bm_units()
    bat = _battery_names()
    u = u[(u["fuelType"] == "PS") | u["nationalGridBmUnit"].isin(bat)].copy()
    u["tech"] = np.where(u["fuelType"] == "PS", "psh", "battery")
    return u[["bmUnit", "nationalGridBmUnit", "tech", "mw", "zone", "zone_method", "scotland", "leadPartyName"]] \
        .reset_index(drop=True)
