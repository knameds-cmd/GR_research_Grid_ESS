"""
BM 계통 상태: 결제구간마다 NESO가 BM 지시를 얼마나, 어떤 단가까지 냈는지와 그 지시를 부르는 계통 상태.
BM 채택 모형(gbess.model.bm_accept)의 설명변수다.

    from gbess.data.bm_state import state
    st = state(2019)          # 한 해. data/processed/bm_state/bm_state_2019.parquet에 저장해 두고 다시 쓴다

열 (UTC 30분 인덱스)
  계통 불균형·가격
    niv_mwh         순불균형량(정산가격 자료). 양수 = 계통이 모자람(offer가 필요)
    ssp, mid        정산가격, 도매 가격 MID
  연료별 발전 (FUELHH, MW)
    wind_mw, ps_mw, ic_mw(연계선 순수입), gen_mw(연계선 제외 총발전, 수요 대용)
    wind_ramp_mw    1시간 전 대비 풍력 변화, gen_ramp_mw 같은 방식의 총발전 변화
  지역별 BM 지시 (전 유닛 Tagged 물량·현금흐름, 구역은 gbess.data.units.bm_units)
    {r}_offer_mwh, {r}_bid_mwh     지역 r(ew = 잉글랜드·웨일스, sc = 스코틀랜드)에서 받아들인 offer·bid 물량 (bid는 양수)
    {r}_offer_p90                 받아들인 offer 단가의 물량 가중 90% 분위수 = "그 구간 그 지역에서 비싸도 받아 준 offer 단가"
    {r}_bid_p10                   받아들인 bid 단가의 물량 가중 10% 분위수 = "가장 불리한 조건으로 받아 준 bid 단가"
                                  (bid 단가는 유닛이 NESO에 내는 돈이다. NESO는 높은 bid부터 받으므로 낮은 쪽이 한계)
    sc_wind_bid_mwh               스코틀랜드 풍력이 받은 bid 물량 = 스코틀랜드 제약(B4·B6 등)의 대용 지표
    bat_offer_mwh, bat_bid_mwh    배터리(저장장치 등록표)가 받은 물량. 2021년 이후 늘어난 배터리와의 경쟁을 보는 변수
  분위수는 1 MWh 이상 받은 유닛만으로 계산한다(시험 지시 같은 작은 물량이 한계 단가를 정하지 않게).
  지시가 없던 구간의 분위수는 결측이다.
    {r}_offer_p90_x{S} 등           같은 분위수를 양수발전소 S(DINO, FFES, CRUA, FOYE)의 유닛을 빼고 다시 센 값
주의: 지역 물량과 분위수에는 모든 유닛이 들어 있다. 채택 모형에서 한 발전소를 설명할 때는 그 발전소 몫을 뺀 값을 쓴다
(물량은 gbess.model.bm_panel이 빼고, 분위수는 _x{S} 열로 바꾼다). 그러지 않으면 결과로 결과를 설명하게 된다.
처음 판(2026-10-25~28)은 분위수에서 자기 몫을 빼지 않았다. 받아 준 구간의 15~28%에서 Dinorwig의 90% 분위수가
Dinorwig 자신의 단가와 같았다(2026-10-29 독립 심사 지적, 확인함). 검증 A~C, 엔진 검증 3·4는 고친 뒤 다시 돌렸다.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.data.prices import _months, index, load_mid
from gbess.data.units import bm_units, storage_units

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "elexon"
CACHE = ROOT / "data" / "processed" / "bm_state"
MIN_MWH = 1.0
IC_PREFIX = "INT"


def _monthly(ds, start, end, pad=True):
    ms = _months(start, end)
    ms = [ms[0] - 1, *ms, ms[-1] + 1] if pad else list(ms)
    files = [RAW / ds / f"{ds}_{m:%Y%m}.parquet" for m in ms]
    return pd.concat([pd.read_parquet(f) for f in files if f.exists()], ignore_index=True)


PSH_SITES = ("DINO", "FFES", "CRUA", "FOYE")   # 자기 몫을 뺀 분위수를 따로 두는 발전소


def wquantile(v, w, q):
    """물량 가중 분위수."""
    o = np.argsort(v)
    v, w = v[o], w[o]
    c = np.cumsum(w)
    return v[np.searchsorted(c, q * c[-1])]


def unit_bm(start, end):
    """유닛·구간·방향별 받은 물량(MWh, bid는 양수)과 평균 단가. 채택 모형의 목표 변수도 여기서 나온다."""
    idx = index(start, end)
    v = _monthly("bm_volumes", start, end)
    v = v[v["dataType"] == "Tagged"].assign(t=lambda d: pd.to_datetime(d["startTime"], utc=True))
    v = v[(v["t"] >= idx[0]) & (v["t"] <= idx[-1])]
    v = v.groupby(["t", "bmUnit", "side"], as_index=False)["totalVolumeAccepted"].sum()
    c = _monthly("bm_cashflows", start, end).assign(t=lambda d: pd.to_datetime(d["startTime"], utc=True))
    c = c.groupby(["t", "bmUnit", "side"], as_index=False)["totalCashflow"].sum()
    m = v.merge(c, on=["t", "bmUnit", "side"], how="left")
    m["mwh"] = m["totalVolumeAccepted"].abs()
    m["price"] = m["totalCashflow"] / m["totalVolumeAccepted"]     # bid도 같은 식: 현금흐름(−) ÷ 물량(−)
    return m[["t", "bmUnit", "side", "mwh", "price"]]


def unit_maps():
    """Elexon 유닛 이름 → (스코틀랜드 여부, 연료). 등록부에 Elexon 이름이 비어 있는 유닛(86개, 대부분 신규 풍력)은
    "T_" + NESO 이름으로 본다(송전 연결 유닛의 Elexon 이름 규칙)."""
    b = bm_units()
    b["bmUnit"] = b["bmUnit"].fillna("T_" + b["nationalGridBmUnit"])
    b = b.drop_duplicates("bmUnit").set_index("bmUnit")
    return b["scotland"], b["fuelType"]


def _build(year):
    start, end = f"{year}-01-01", f"{year + 1}-01-01"
    idx = index(start, end)
    out = pd.DataFrame(index=idx)

    sp = _monthly("system_prices", start, end).assign(t=lambda d: pd.to_datetime(d["startTime"], utc=True))
    sp = sp.drop_duplicates("t").set_index("t").reindex(idx)
    out["niv_mwh"] = sp["netImbalanceVolume"].astype(float)
    out["ssp"] = sp["systemSellPrice"].astype(float)
    out["mid"], _ = load_mid(start, end)

    f = _monthly("fuelhh", start, end).assign(t=lambda d: pd.to_datetime(d["startTime"], utc=True))
    g = f.pivot_table(index="t", columns="fuelType", values="generation", aggfunc="last").reindex(idx)
    ic = [c for c in g.columns if c.startswith(IC_PREFIX)]
    out["wind_mw"] = g["WIND"]
    out["ps_mw"] = g["PS"]
    out["ic_mw"] = g[ic].sum(axis=1, min_count=1)
    out["gen_mw"] = g.drop(columns=ic).sum(axis=1, min_count=1).replace(0.0, np.nan)   # 0은 자료 빠짐
    out["wind_ramp_mw"] = out["wind_mw"].diff(2)
    out["gen_ramp_mw"] = out["gen_mw"].diff(2)

    m = unit_bm(start, end)
    sc, fuel = unit_maps()
    m["region"] = np.where(m["bmUnit"].map(sc).fillna(False).astype(bool), "sc", "ew")
    m["wind"] = m["bmUnit"].map(fuel).eq("WIND")
    m["site"] = m["bmUnit"].str.extract(r"^T_([A-Z]+)-")[0]
    for (r, side), d in m.groupby(["region", "side"]):
        out[f"{r}_{side}_mwh"] = d.groupby("t")["mwh"].sum().reindex(idx).fillna(0.0)
        d = d[(d["mwh"] >= MIN_MWH) & d["price"].notna()]
        q = 0.9 if side == "offer" else 0.1
        name = f"{r}_{side}_{'p90' if side == 'offer' else 'p10'}"

        def wq(x):
            return wquantile(x["price"].to_numpy(), x["mwh"].to_numpy(), q)
        out[name] = d.groupby("t").apply(wq).reindex(idx).astype(float)
        # 같은 분위수를 양수발전소 하나씩 빼고 다시 센다. 채택 모형이 그 발전소를 예측할 때 쓴다:
        # 자기가 받은 단가가 기준 분위수에 섞이면 "받았다"는 결과가 경쟁력 입력을 좋게 만든다 (2026-10-29 심사 지적)
        for s in PSH_SITES:
            if (d["site"] == s).any():
                out[f"{name}_x{s}"] = d[d["site"] != s].groupby("t").apply(wq).reindex(idx).astype(float)
            else:
                out[f"{name}_x{s}"] = out[name]
    w = m[m["wind"] & (m["region"] == "sc") & (m["side"] == "bid")]
    out["sc_wind_bid_mwh"] = w.groupby("t")["mwh"].sum().reindex(idx).fillna(0.0)
    su = storage_units()
    bat = m[m["bmUnit"].isin(su.loc[su["tech"] == "battery", "bmUnit"])]
    for side in ("offer", "bid"):
        out[f"bat_{side}_mwh"] = bat[bat["side"] == side].groupby("t")["mwh"].sum().reindex(idx).fillna(0.0)
    out.attrs = {"fuelhh_missing_sp": int(out["wind_mw"].isna().sum()), "niv_missing_sp": int(out["niv_mwh"].isna().sum())}
    return out


def state(year, force=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"bm_state_{year}.parquet"
    if path.exists() and not force:
        return pd.read_parquet(path)
    st = _build(year)
    st.to_parquet(path)
    return st
