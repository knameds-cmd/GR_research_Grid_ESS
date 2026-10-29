"""
저장장치가 운전량(MWh)에 비례해 내는 망·계통 요금. 규칙이 바뀐 시점마다 다르다(08 문서의 C형 규칙: 운전을 바꾼다).

    from gbess.data.charges import bsuos_storage
    c = bsuos_storage("2019-01-01", "2020-01-01")   # 열 export_gbp_mwh, import_gbp_mwh (UTC 30분)

BSUoS (계통 운영 비용을 나눠 내는 요금, 결제구간마다 £/MWh)
  ~2021-03   발전(내보냄)과 수요(받아들임) 모두 같은 단가로 낸다. 저장장치는 양쪽에서 두 번 낸다.
  2021-04~2023-03   CMP281: 신고한 저장장치는 받아들이는 쪽이 면제. 내보내는 쪽은 그대로 낸다.
  2023-04~   CMP308: 발전은 면제, 최종 수요만 낸다. 저장장치는 최종 수요가 아니라 받아들이는 쪽도 면제 → 0.
  출처: Ofgem CMP308 결정, NESO "TNUoS and BSUoS CVA Facility Declarations"(CMP281 신고), Modo(2022-03) 정리.
  단가: NESO Historic RF BSUoS Data(2016-04~2023-03, gbess.fetch.neso bsuos). 2016-04 이전은 자료가 없어 결측이다.
  실제로 낸 값(재정산 RF)이다. 운영자는 미리 몰랐으므로 롤링 엔진의 계획 단계에는 지난 7일 평균을 쓴다.
TNUoS(송전망 이용 요금)의 발전 쪽은 연간 £/kW(용량)라 운전량에 비례하지 않는다. 운전을 바꾸지 않으므로 여기 두지 않고
실제 수익의 순액 계산에서 뺀다(gbess.realized.tnuos).
"""
from pathlib import Path

import pandas as pd

from gbess.data.prices import index

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "neso_sql" / "bsuos_rf_hist.parquet"
CMP281 = pd.Timestamp("2021-04-01", tz="Europe/London").tz_convert("UTC")
CMP308 = pd.Timestamp("2023-04-01", tz="Europe/London").tz_convert("UTC")


def bsuos_price():
    """결제구간 BSUoS 단가(£/MWh), UTC 시작 시각 인덱스."""
    d = pd.read_parquet(RAW)
    day = pd.to_datetime(d["Settlement Day"].str[:10]).dt.tz_localize("Europe/London")
    t = (day + pd.to_timedelta((d["Settlement Period"].astype(int) - 1) * 30, unit="min")).dt.tz_convert("UTC")
    s = pd.Series(d["BSUoS Price GBP per MWh"].astype(float).to_numpy(), index=t).sort_index()
    return s[~s.index.duplicated(keep="last")]


def bsuos_storage(start, end):
    idx = index(start, end)
    p = bsuos_price().reindex(idx)
    p[idx >= CMP308] = 0.0
    exp = p.copy()
    imp = p.where(idx < CMP281, 0.0)
    return pd.DataFrame({"export_gbp_mwh": exp, "import_gbp_mwh": imp}, index=idx)
