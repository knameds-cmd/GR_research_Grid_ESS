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


def storage_units():
    b = pd.read_csv(RAW / "elexon_bmunits.csv")
    b["zone"] = b["gspGroupName"].replace(ZONE_ALIASES)
    known = b[b["zone"].notna() & b["transmissionLossFactor"].notna()]
    modal = known.groupby("transmissionLossFactor")["zone"].agg(lambda s: s.value_counts().index[0])
    counts = known.groupby("transmissionLossFactor").size()
    rep = modal[counts >= 3]   # 대표값: 3개 이상 유닛이 같은 TLF를 쓰는 값
    bat = _battery_names()
    u = b[(b["fuelType"] == "PS") | b["nationalGridBmUnit"].isin(bat)].copy()
    u["tech"] = np.where(u["fuelType"] == "PS", "psh", "battery")
    u["zone_method"] = np.where(u["zone"].notna(), "gsp", None)
    miss = u["zone"].isna() & u["transmissionLossFactor"].notna()
    for i in u.index[miss]:
        tlf = u.at[i, "transmissionLossFactor"]
        if tlf in modal.index:
            u.at[i, "zone"], u.at[i, "zone_method"] = modal[tlf], "tlf_exact"
        else:
            j = int(np.abs(rep.index.to_numpy() - tlf).argmin())
            u.at[i, "zone"], u.at[i, "zone_method"] = rep.iloc[j], "tlf_nearest"
    u["scotland"] = u["zone"].isin({ZONE_ALIASES.get(z, z) for z in SCOTLAND})
    u = u.rename(columns={"elexonBmUnit": "bmUnit", "generationCapacity": "mw"})
    return u[["bmUnit", "nationalGridBmUnit", "tech", "mw", "zone", "zone_method", "scotland", "leadPartyName"]] \
        .reset_index(drop=True)
