"""
BM 기회 계열: 결제구간마다 기준 무리(같은 지역의 저장장치)가 실제로 받은 MW당 BM 지시 물량과 단가.

    from gbess.data.bm_opportunity import opportunity
    opp = opportunity("2025-01-01", "2026-01-01", scotland=False, exclude_sites=("DINO",))

반환(UTC 30분 인덱스):
    offer_mw_per_mw  기준 무리의 활동 출력 1 MW당 받은 offer 지시(출력 증가) 평균 MW = Tagged offer MWh ÷ 활동 MW ÷ 0.5h
    bid_mw_per_mw    같은 방식의 bid 지시(출력 감소) MW, 양수
    offer_price      offer 단가 £/MWh = offer 현금흐름 ÷ Tagged offer 물량 (pay-as-bid의 물량 가중 평균)
    bid_price        bid 단가 £/MWh = bid 현금흐름 ÷ Tagged bid 물량. 음수면 NESO가 유닛에 돈을 준다
    active_mw        그 달에 한 번이라도 BM 지시 자료(물량 또는 현금흐름)에 나온 기준 무리 유닛의 등록 출력 합.
                     구간마다 지시받은 유닛만 세면 분모가 "지시받은 유닛"이 되어 MW당 지시량이 부풀려진다
                     (2026-10-24 시험: 양수 무리 1,100 MW가 구간별로는 81~207 MW로 잡힘). 그래서 달 단위로 센다.
물량은 Tagged를 쓴다(정산 금액과 짝, gbess/fetch/elexon.py 참고). 지시가 없던 구간의 단가는 결측 → 엔진에서 상한 0이라 쓰이지 않는다.
이 계열은 "이 지역에서 비슷한 자산이 실제로 받았던 기회"이므로, 새 자산이 들어와 지시를 나눠 갖는 효과(잠식)는 담지 않는다.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.data.prices import _months, index
from gbess.data.units import storage_units

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "elexon"
DT = 0.5


def _load(kind, start, end):
    ms = _months(start, end)
    files = [RAW / f"bm_{kind}" / f"bm_{kind}_{m:%Y%m}.parquet" for m in [ms[0] - 1, *ms, ms[-1] + 1]]
    missing = [f.name for f in files[1:-1] if not f.exists()]
    if missing:
        raise FileNotFoundError(f"BM {kind} 파일 없음: {missing[:3]}… (gbess.fetch.elexon {kind})")
    return pd.concat([pd.read_parquet(f) for f in files if f.exists()], ignore_index=True)


def opportunity(start, end, scotland=None, tech=None, exclude_sites=(), units=None):
    """scotland: True/False면 그 지역만, None이면 전국. tech: "psh"/"battery"/None. exclude_sites: 뺄 발전소 접두어(예: "DINO")."""
    u = storage_units() if units is None else units
    if scotland is not None:
        u = u[u["scotland"] == scotland]
    if tech is not None:
        u = u[u["tech"] == tech]
    for s in exclude_sites:
        u = u[~u["bmUnit"].str.contains(f"_{s}-", regex=False)]
    mw = u.set_index("bmUnit")["mw"]
    idx = index(start, end)

    v = _load("volumes", start, end)
    v = v[(v["dataType"] == "Tagged") & v["bmUnit"].isin(mw.index)]
    v = v.assign(t=pd.to_datetime(v["startTime"], utc=True))
    v = v[(v["t"] >= idx[0]) & (v["t"] <= idx[-1])]
    c = _load("cashflows", start, end)
    c = c[c["bmUnit"].isin(mw.index)].assign(t=lambda d: pd.to_datetime(d["startTime"], utc=True))

    seen = pd.concat([v[["t", "bmUnit"]], c[["t", "bmUnit"]]])
    seen["month"] = seen["t"].dt.strftime("%Y-%m")
    month_mw = seen.drop_duplicates(["month", "bmUnit"]).assign(mw=lambda d: d["bmUnit"].map(mw)).groupby("month")["mw"].sum()
    active = pd.Series(idx.strftime("%Y-%m"), index=idx).map(month_mw)
    vol = v.groupby(["t", "side"])["totalVolumeAccepted"].sum().unstack().reindex(columns=["offer", "bid"])
    cash = c.groupby(["t", "side"])["totalCashflow"].sum().unstack().reindex(columns=["offer", "bid"])
    out = pd.DataFrame(index=idx)
    out["active_mw"] = active.reindex(idx).fillna(0.0)
    off_mwh = vol["offer"].reindex(idx).fillna(0.0)
    bid_mwh = -vol["bid"].reindex(idx).fillna(0.0)          # bid 물량은 음수로 기록됨 → 양수로
    denom = out["active_mw"].where(out["active_mw"] > 0)
    out["offer_mw_per_mw"] = (off_mwh / denom / DT).fillna(0.0)
    out["bid_mw_per_mw"] = (bid_mwh / denom / DT).fillna(0.0)
    out["offer_price"] = (cash["offer"].reindex(idx) / off_mwh.where(off_mwh > 1e-6))
    out["bid_price"] = (cash["bid"].reindex(idx) / -bid_mwh.where(bid_mwh > 1e-6))
    out.attrs = {"units": len(mw), "fleet_mw": float(mw.sum()), "scotland": scotland, "tech": tech,
                 "excluded": list(exclude_sites)}
    return out
