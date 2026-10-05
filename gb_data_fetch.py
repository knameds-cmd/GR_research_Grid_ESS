"""
GB 배터리 연구용 공개 데이터 다운로드 스크립트
- NESO EAC 경매 결과 (DC/DM/DR/BR/QR/SR): 요약 + 배터리 유닛별 결과
- NESO Capacity Market Register: 구성요소(저장장치 지속시간), CMU(계약기간), 디레이팅 계수
- Elexon Insights: BM 유닛 목록, MID 가격, 정산가격, 특정 배터리의 PN / BOALF / BM 현금흐름

실행 (본인 Mac 터미널에서):
    pip install requests pandas
    python3 gb_data_fetch.py              # 기본: EAC 요약 + CM + Elexon 2026-09 샘플
    python3 gb_data_fetch.py --units      # 배터리 유닛별 EAC 결과까지 (수십만 행, 몇 분 소요)

결과는 ./data/raw/ 폴더에 CSV로 저장됩니다. 키 없이 무료로 접근 가능합니다.
"""
import argparse
import json
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

OUT = Path(__file__).resolve().parent / "data" / "raw"
OUT.mkdir(exist_ok=True)

NESO = "https://api.neso.energy/api/3/action"
ELEXON = "https://data.elexon.co.uk/bmrs/api/v1"

# --- NESO 데이터셋 resource id (2026-10-05 확인) ---
EAC_SUMMARY = {  # 서비스별 낙찰가·낙찰량 (EFA 4시간 블록 / 30분 결제구간)
    "FY2023": "be5c6b0d-a335-4859-93f2-389585b4e9a1",  # 2023-11 ~ 2024-03
    "FY2024": "ab130833-3ce4-4361-90fb-69fa3cf30f15",
    "FY2025": "be55ee51-b79e-47da-b71e-a0f8865d9d66",
    "current": "596f29ac-0387-4ba4-a6d3-95c243140707",  # 2026-04 ~
}
EAC_UNIT = {  # 유닛별 낙찰 결과 (technologyType 필드로 배터리 구분)
    "FY2023": "7505ec16-e1e7-432e-8abd-a554e03e4f02",
    "FY2024": "2fc9dd7e-5274-40e3-abf4-6d31b30f21c6",
    "FY2025": "c312358e-87da-480e-88cc-d45c1dce1b41",
    "current": "a63ab354-7e68-44c2-ad96-c6f920c30e85",
}
CM = {
    "cm_components": "790f5fa0-f8eb-4d82-b98d-0d34d3e404e8",   # 'Generating Technology Class' = Storage (Duration Xh)
    "cm_cmu": "25a5fa2e-873d-41c5-8aaf-fbc2b06d79e6",          # 계약 기간(1/3/15년), 디레이팅 용량
    "cm_derating_factors": "d94ff98d-39ba-40d6-9672-7433de0631ac",
    "cm_auction_capacity_cost": "b1b58919-eaa4-40ea-80df-3d3e526f8223",
}


def neso_all(resource_id, filters=None):
    """CKAN datastore_search를 페이지 단위로 전부 받기 (요청 간 1.2초 대기)."""
    rows, off = [], 0
    while True:
        params = {"resource_id": resource_id, "limit": 32000, "offset": off}
        if filters:
            params["filters"] = json.dumps(filters)
        r = requests.get(f"{NESO}/datastore_search", params=params, timeout=180)
        r.raise_for_status()
        recs = r.json()["result"]["records"]
        rows += recs
        off += len(recs)
        print(f"  {resource_id[:8]}... {off} rows")
        if len(recs) < 32000:
            break
        time.sleep(1.2)
    return pd.DataFrame(rows)


def elexon(path, params=None):
    r = requests.get(f"{ELEXON}{path}", params=params, timeout=120)
    r.raise_for_status()
    j = r.json()
    return pd.DataFrame(j if isinstance(j, list) else j.get("data", []))


def days(start, end):
    d = start
    while d < end:
        yield d
        d += timedelta(days=1)


def fetch_eac_summary():
    print("EAC summary")
    df = pd.concat([neso_all(rid).assign(source=k) for k, rid in EAC_SUMMARY.items()], ignore_index=True)
    df.to_csv(OUT / "eac_results_summary.csv", index=False)
    # 월별·상품별 요약 (시간가중 평균가 GBP/MW/h, 평균 낙찰량 MW)
    df["deliveryStart"] = pd.to_datetime(df["deliveryStart"])
    df["deliveryEnd"] = pd.to_datetime(df["deliveryEnd"])
    df["hours"] = (df["deliveryEnd"] - df["deliveryStart"]).dt.total_seconds() / 3600
    df["month"] = df["deliveryStart"].dt.to_period("M").astype(str)
    df["p_h"] = df["clearingPrice"] * df["hours"]
    m = df.groupby(["month", "auctionProduct", "serviceType"]).agg(
        blocks=("clearingPrice", "size"), p_h=("p_h", "sum"), hours=("hours", "sum"),
        avg_cleared_mw=("clearedVolume", "mean")).reset_index()
    m["timeavg_price_gbp_per_mw_h"] = m["p_h"] / m["hours"]
    m.drop(columns=["p_h"]).to_csv(OUT / "eac_monthly_by_product.csv", index=False)


def fetch_eac_units():
    print("EAC battery unit results (large)")
    for k, rid in EAC_UNIT.items():
        df = neso_all(rid, filters={"technologyType": "Batteries"})
        df.to_csv(OUT / f"eac_unit_results_batteries_{k}.csv", index=False)


def fetch_cm():
    print("Capacity Market register")
    for name, rid in CM.items():
        neso_all(rid).to_csv(OUT / f"{name}.csv", index=False)


def fetch_elexon_sample(bm_unit="T_LKSDB-1", start=date(2026, 9, 1), end=date(2026, 10, 1)):
    print("Elexon reference + prices + one battery")
    elexon("/reference/bmunits/all").to_csv(OUT / "elexon_bmunits.csv", index=False)
    f, t = f"{start}T00:00Z", f"{end}T00:00Z"
    elexon("/datasets/MID/stream", {"from": f, "to": t}).to_csv(OUT / f"elexon_mid_{start:%Y%m}.csv", index=False)
    elexon("/datasets/PN/stream", {"from": f, "to": t, "bmUnit": bm_unit}).to_csv(
        OUT / f"elexon_pn_{bm_unit}_{start:%Y%m}.csv", index=False)
    elexon("/datasets/BOALF/stream", {"from": f, "to": t, "bmUnit": bm_unit}).to_csv(
        OUT / f"elexon_boalf_{bm_unit}_{start:%Y%m}.csv", index=False)
    sp, cf = [], []
    for d in days(start, end):
        sp.append(elexon(f"/balancing/settlement/system-prices/{d}"))
        for bo in ("bid", "offer"):
            x = elexon(f"/balancing/settlement/indicative/cashflows/all/{bo}/{d}", {"bmUnit": bm_unit})
            cf.append(x.assign(side=bo))
        time.sleep(0.2)
    pd.concat(sp).to_csv(OUT / f"elexon_system_prices_{start:%Y%m}.csv", index=False)
    pd.concat(cf).to_csv(OUT / f"elexon_bm_cashflows_{bm_unit}_{start:%Y%m}.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", action="store_true", help="배터리 유닛별 EAC 결과도 받기")
    a = ap.parse_args()
    fetch_eac_summary()
    fetch_cm()
    fetch_elexon_sample()
    if a.units:
        fetch_eac_units()
    print("done ->", OUT)
