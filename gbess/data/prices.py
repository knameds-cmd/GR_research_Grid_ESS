"""
도매(MID)·정산가격을 UTC 30분 인덱스로 읽는다. 원자료는 gbess.fetch.elexon prices로 받은 월별 parquet.

- MID: Elexon Market Index Data 중 APX(EPEX) 단기시장 가격. 거래량 0인 구간은 가격이 0으로 찍혀 있어 결측으로 본다.
  결측은 선형 보간하고, 보간한 구간 수와 가장 긴 연속 결측을 report에 남긴다.
- 정산가격(SSP): 2015-11 이후 단일 가격이라 SSP = SBP. 불균형 노출 평가와 도매 평가의 상한·하한 비교에 쓴다.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "elexon"


def _months(start, end):
    return pd.period_range(_utc(start).strftime("%Y-%m"), (_utc(end) - pd.Timedelta(minutes=1)).strftime("%Y-%m"),
                           freq="M")


def _utc(t):
    t = pd.Timestamp(t)
    return t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")


def index(start, end):
    return pd.date_range(_utc(start), _utc(end), freq="30min", inclusive="left")


def load_mid(start, end, max_gap_sp=6, long_gap="ssp"):
    """max_gap_sp 이하의 결측은 선형 보간. 더 긴 결측은 long_gap="ssp"면 같은 구간의 정산가격으로 채우고,
    "raise"면 멈춘다. 2017~2021년에는 2~4일(96~192구간) 연속 결측이 있다 (2026-10-24 확인).
    장주기 자산은 여러 날의 가격 차로 돈을 벌기 때문에 며칠을 직선으로 메우면 결과가 왜곡된다."""
    idx = index(start, end)
    files = [RAW / "mid" / f"mid_{m:%Y%m}.parquet" for m in _months(start, end)]
    # 월 경계의 구간은 이웃 달 파일에 있을 수 있으므로 앞뒤 달도 읽는다
    m0, m1 = _months(start, end)[0] - 1, _months(start, end)[-1] + 1
    files = [RAW / "mid" / f"mid_{m0:%Y%m}.parquet"] + files + [RAW / "mid" / f"mid_{m1:%Y%m}.parquet"]
    df = pd.concat([pd.read_parquet(f) for f in files if f.exists()])
    df = df[(df["dataProvider"] == "APXMIDP") & (df["volume"] > 0)]
    s = df.assign(t=pd.to_datetime(df["startTime"], utc=True)).drop_duplicates("t").set_index("t")["price"]
    s = s.reindex(idx).astype(float)
    miss = s.isna()
    run_id = miss.ne(miss.shift()).cumsum()
    run_len = miss.groupby(run_id).transform("sum").where(miss, 0)
    longest = int(run_len.max())
    long_mask = run_len > max_gap_sp
    report = {"periods": len(idx), "missing": int(miss.sum()), "longest_gap_sp": longest,
              "filled_interp": int((miss & ~long_mask).sum()), "filled_ssp": 0}
    if long_mask.any():
        if long_gap != "ssp":
            raise ValueError(f"MID 연속 결측 {longest}구간 > {max_gap_sp}: {report}")
        ssp = load_ssp(start, end)
        s = s.where(~long_mask, ssp)
        report["filled_ssp"] = int((long_mask & s.notna()).sum())
        report["both_missing_interp"] = int((long_mask & s.isna()).sum())  # MID·SSP 둘 다 없는 구간 (2019-08에 1구간)
    return s.interpolate(limit_direction="both"), report


def load_ssp(start, end):
    idx = index(start, end)
    ms = _months(start, end)
    files = [RAW / "system_prices" / f"system_prices_{m:%Y%m}.parquet" for m in [ms[0] - 1, *ms, ms[-1] + 1]]
    df = pd.concat([pd.read_parquet(f) for f in files if f.exists()])
    s = df.assign(t=pd.to_datetime(df["startTime"], utc=True)).drop_duplicates("t").set_index("t")["systemSellPrice"]
    return s.reindex(idx).astype(float)
