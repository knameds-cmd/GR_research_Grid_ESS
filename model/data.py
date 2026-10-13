"""
층 1 모델 입력 만들기: 30분 결제구간(SP)마다 도매가격과 EAC 상품 가격을 한 표로 맞춘다.

- 도매가격: Elexon MID 중 APX(EPEX) 가격. 거래량 0인 구간은 가격이 0으로 찍혀 있어 결측으로 보고 보간한다.
  읽는 파일: data/raw/elexon_mid/elexon_mid_YYYYMM.csv (gb_data_fetch.py --only prices)
             data/raw/elexon_mid_YYYYMM.csv (기본 샘플)
- EAC 가격: data/raw/eac_results_summary.csv. 시각은 UTC다(여름에 EFA 블록이 22시에 시작하는 것으로 확인).
  DC/DM/DR은 4시간 EFA 블록, BR/QR/SR은 30분 단위로 낙찰된다.
모든 시각은 UTC로 다룬다. 서머타임 날의 3시간·5시간 블록도 낙찰 결과의 시작·끝 시각을 그대로 써서 맞춘다.
"""
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SP_HOURS = 0.5

# EAC 상품: 방향(up = 출력을 늘림 = 방전 쪽, down = 출력을 줄임 = 충전 쪽), 에너지 지속시간(h), 낙찰 단위
# 지속시간은 literature/context/GB_market_history_EN.md 4장 상품표 기준. QR은 출처마다 13~15분이라 15분으로 둔다.
PRODUCTS = {
    "DCL": ("up", 0.25, "block"), "DCH": ("down", 0.25, "block"),
    "DML": ("up", 0.5, "block"), "DMH": ("down", 0.5, "block"),
    "DRL": ("up", 1.0, "block"), "DRH": ("down", 1.0, "block"),
    "PBR": ("up", 0.5, "sp"), "NBR": ("down", 0.5, "sp"),
    "PQR": ("up", 0.25, "sp"), "NQR": ("down", 0.25, "sp"),
    "PSR": ("up", 2.0, "sp"), "NSR": ("down", 2.0, "sp"),
}
RESPONSE = ["DCL", "DCH", "DML", "DMH", "DRL", "DRH"]
RESERVE = ["PBR", "NBR", "PQR", "NQR", "PSR", "NSR"]

# 주파수 응답 곡선: (주파수 편차 Hz, 계약 물량 대비 응답 비율). 편차가 클수록 더 많이 낸다 (GB_market_history_EN.md 4장)
RESPONSE_CURVES = {
    "DC": [(0.015, 0.0), (0.2, 0.05), (0.5, 1.0)],   # 사고 후용: ±0.2 Hz 안에서는 거의 안 움직임
    "DM": [(0.015, 0.0), (0.1, 0.05), (0.2, 1.0)],
    "DR": [(0.015, 0.0), (0.2, 1.0)],                # 평상시 조정용: 작은 편차에도 계속 움직임
}


def expected_utilisation(sigma_hz):
    """주파수 편차가 평균 0, 표준편차 sigma_hz인 정규분포라고 할 때, 계약 1 MW가 한 시간에 한쪽 방향으로
    내는 평균 에너지(MWh). 낮은 쪽(L)과 높은 쪽(H)은 대칭이라 같은 값. 1초 주파수 자료를 받으면
    실제 분포로 바꾼다 (neso_fetch.py get system-frequency-data)."""
    x = np.linspace(0.0, 1.0, 100001)
    pdf = np.exp(-0.5 * (x / sigma_hz) ** 2) / (sigma_hz * np.sqrt(2 * np.pi))
    out = {}
    for fam, pts in RESPONSE_CURVES.items():
        g = np.interp(x, [a for a, _ in pts], [b for _, b in pts], left=0.0, right=1.0)
        a = float(np.sum((g[1:] * pdf[1:] + g[:-1] * pdf[:-1]) / 2 * np.diff(x)))
        out[fam + "L"] = out[fam + "H"] = a
    return out


@dataclass
class Inputs:
    index: pd.DatetimeIndex     # SP 시작 시각 (UTC), 30분 간격
    wholesale: pd.Series        # £/MWh
    price: pd.DataFrame         # 상품별 낙찰가 £/MW/h (그 SP가 속한 낙찰 구간의 값), 열 = 상품
    cleared: pd.DataFrame       # 상품별 시장 전체 낙찰량 MW (가격 수용자 물량 상한)
    window: pd.DataFrame        # 상품별 낙찰 구간 id (EFA 블록 시작 시각 또는 SP 시작 시각)
    notes: list


def sp_index(start, end):
    return pd.date_range(pd.Timestamp(start, tz="UTC"), pd.Timestamp(end, tz="UTC"), freq="30min", inclusive="left")


def load_wholesale(idx):
    files = sorted(RAW.glob("elexon_mid_*.csv")) + sorted((RAW / "elexon_mid").glob("elexon_mid_*.csv"))
    if not files:
        raise FileNotFoundError("MID 파일이 없습니다. 먼저 python3 gb_data_fetch.py --only prices 로 받으세요.")
    df = pd.concat([pd.read_csv(f, usecols=["startTime", "dataProvider", "price", "volume"]) for f in files])
    df = df[df["dataProvider"] == "APXMIDP"].copy()
    df["t"] = pd.to_datetime(df["startTime"], utc=True)
    df = df.drop_duplicates("t").set_index("t").sort_index()
    s = df["price"].where(df["volume"] > 0).reindex(idx)
    n_missing = int(s.isna().sum())
    if n_missing > len(idx) * 0.05:
        raise ValueError(f"MID가 {len(idx)}구간 중 {n_missing}구간 비어 있습니다. 기간을 확인하거나 가격을 더 받으세요.")
    return s.interpolate(limit_direction="both"), n_missing


def load_eac(idx):
    df = pd.read_csv(RAW / "eac_results_summary.csv",
                     usecols=["auctionProduct", "deliveryStart", "deliveryEnd", "clearedVolume", "clearingPrice"])
    df["deliveryStart"] = pd.to_datetime(df["deliveryStart"], utc=True)
    df["deliveryEnd"] = pd.to_datetime(df["deliveryEnd"], utc=True)
    price, cleared, window = {}, {}, {}
    t = pd.DataFrame({"t": idx})
    for p in PRODUCTS:
        d = df[df["auctionProduct"] == p].sort_values("deliveryStart")
        if d.empty:
            continue
        # 각 SP 시작 시각이 들어가는 낙찰 구간 찾기 (deliveryStart <= t < deliveryEnd)
        m = pd.merge_asof(t, d, left_on="t", right_on="deliveryStart", direction="backward")
        ok = m["t"] < m["deliveryEnd"]
        price[p] = m["clearingPrice"].where(ok).to_numpy()
        cleared[p] = m["clearedVolume"].where(ok).to_numpy()
        window[p] = m["deliveryStart"].where(ok).to_numpy()
    return (pd.DataFrame(price, index=idx), pd.DataFrame(cleared, index=idx),
            pd.DataFrame(window, index=idx))


def build_inputs(start, end):
    idx = sp_index(start, end)
    wholesale, n_missing = load_wholesale(idx)
    price, cleared, window = load_eac(idx)
    notes = [f"MID 결측(거래량 0 또는 없음) {n_missing}구간은 선형 보간"]
    for p in PRODUCTS:
        if p not in price or price[p].isna().all():
            notes.append(f"{p}: 이 기간에 낙찰 결과 없음 (상품이 없던 시기이거나 자료 없음)")
        elif price[p].isna().any():
            notes.append(f"{p}: {int(price[p].isna().sum())}구간 낙찰 결과 없음 → 그 구간은 참여 불가")
    return Inputs(idx, wholesale, price, cleared, window, notes)
