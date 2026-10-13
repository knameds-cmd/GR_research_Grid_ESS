"""
GB 배터리 연구용 공개 데이터 다운로드 스크립트
- NESO EAC 경매 결과 (DC/DM/DR/BR/QR/SR): 요약 + 유닛별 결과
- NESO EAC 이전 DC 결과(dynamic-containment-data), BM skip rate(skip-rates)
- NESO Capacity Market Register: 구성요소(저장장치 지속시간), CMU(계약기간), 디레이팅 계수
- Elexon Insights: BM 유닛 목록, MID 가격·정산가격(기간 지정), 특정 배터리의 PN / BOALF / BM 현금흐름

실행 (본인 Mac 터미널에서):
    pip install requests pandas
    python3 gb_data_fetch.py              # 기본: EAC 요약 + CM + Elexon 2026-09 샘플
    python3 gb_data_fetch.py --units      # 배터리 유닛별 EAC 결과까지 (수십만 행, 몇 분 소요)

    # 받을 묶음과 기간 지정 (--only는 쉼표 구분, --end 날짜는 포함하지 않음, 기본 오늘)
    python3 gb_data_fetch.py --only units,dc,prices,skip --start 2021-09-01
    python3 gb_data_fetch.py --only prices --start 2023-01-01 --end 2024-01-01

    묶음: eac     EAC 요약(전체 기간)
          cm      용량시장 등록부
          sample  Elexon 2026-09 샘플(Lakeside 한 유닛)
          units   EAC 유닛별 결과. 기본은 배터리만, --all-tech면 전체 기술
          dc      EAC 이전 DC 결과(NESO 데이터셋 전체)
          prices  MID·정산가격. 기본 시작 2021-09-01, 월별 파일
          skip    BM skip rate(NESO 데이터셋 전체)
    --start/--end는 prices(달 단위로 받음)와 units(회계연도 단위로 고름)에 적용된다.
    이미 받은 파일은 건너뛰므로 중간에 끊겨도 다시 실행하면 이어 받는다(--force면 전부 다시).

결과는 ./data/raw/ 폴더에 CSV로 저장됩니다. 키 없이 무료로 접근 가능합니다.
"""
import argparse
import json
import re
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

OUT = Path(__file__).resolve().parent / "data" / "raw"
OUT.mkdir(exist_ok=True)

NESO = "https://api.neso.energy/api/3/action"
ELEXON = "https://data.elexon.co.uk/bmrs/api/v1"
SESSION = requests.Session()
RETRY = {429, 500, 502, 503, 504}

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
EAC_UNIT_FROM = {  # 각 resource가 덮는 기간의 시작(회계연도 4월 시작). 다음 항목의 시작이 끝
    "FY2023": date(2023, 11, 1),
    "FY2024": date(2024, 4, 1),
    "FY2025": date(2025, 4, 1),
    "current": date(2026, 4, 1),
}
CM = {
    "cm_components": "790f5fa0-f8eb-4d82-b98d-0d34d3e404e8",   # 'Generating Technology Class' = Storage (Duration Xh)
    "cm_cmu": "25a5fa2e-873d-41c5-8aaf-fbc2b06d79e6",          # 계약 기간(1/3/15년), 디레이팅 용량
    "cm_derating_factors": "d94ff98d-39ba-40d6-9672-7433de0631ac",
    "cm_auction_capacity_cost": "b1b58919-eaa4-40ea-80df-3d3e526f8223",
}
# --- NESO 데이터셋(패키지) 이름 → data/raw 아래 폴더 (2026-10-06 package_search로 존재 확인) ---
NESO_PACKAGES = {
    "dc": ("dynamic-containment-data", "dc_pre_eac"),  # EAC 이전 DC 결과
    "skip": ("skip-rates", "skip_rates"),              # BM skip rate (2024.12~)
}
FILE_FORMATS = {"csv", "xlsx", "xls", "json", "zip"}  # datastore에 없는 자료 중 받을 형식
PRICES_START = date(2021, 9, 1)  # 설계 M1 국면 (a) 진입기·호황기 분석 시작점

JOBS = ["eac", "cm", "sample", "units", "dc", "prices", "skip"]


def get(url, params=None, timeout=180, tries=5):
    """GET. 일시 오류(429·5xx·연결 끊김)는 2·4·8·16초 간격으로 재시도. 4xx와 프록시 차단은 바로 실패."""
    for i in range(tries):
        try:
            r = SESSION.get(url, params=params, timeout=timeout)
            if r.status_code not in RETRY:
                r.raise_for_status()
                return r
            err = f"HTTP {r.status_code}"
        except requests.exceptions.ProxyError:
            raise
        except (requests.ConnectionError, requests.Timeout) as e:
            err = type(e).__name__
        if i == tries - 1:
            raise RuntimeError(f"{url} 실패: {err}")
        print(f"  재시도 {i + 1}/{tries - 1} ({err})")
        time.sleep(2 ** (i + 1))


def neso_all(resource_id, filters=None):
    """CKAN datastore_search를 페이지 단위로 전부 받기 (요청 간 1.2초 대기)."""
    rows, off = [], 0
    while True:
        params = {"resource_id": resource_id, "limit": 32000, "offset": off}
        if filters:
            params["filters"] = json.dumps(filters)
        recs = get(f"{NESO}/datastore_search", params).json()["result"]["records"]
        rows += recs
        off += len(recs)
        print(f"  {resource_id[:8]}... {off} rows")
        if len(recs) < 32000:
            break
        time.sleep(1.2)
    return pd.DataFrame(rows)


def elexon(path, params=None):
    j = get(f"{ELEXON}{path}", params, timeout=120).json()
    return pd.DataFrame(j if isinstance(j, list) else j.get("data", []))


def days(start, end):
    d = start
    while d < end:
        yield d
        d += timedelta(days=1)


def months(start, end):
    """[start, end)를 덮는 달마다 (그달 1일, 다음 달 1일)."""
    d = start.replace(day=1)
    while d < end:
        nxt = (d + timedelta(days=32)).replace(day=1)
        yield d, nxt
        d = nxt


def covers(path, last_day):
    """월별 파일이 last_day(settlementDate)까지 들어 있으면 True."""
    if not path.exists():
        return False
    try:
        s = pd.read_csv(path, usecols=["settlementDate"])["settlementDate"]
    except (ValueError, pd.errors.EmptyDataError):
        return False
    return not s.empty and s.max() >= str(last_day)


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


def fetch_eac_units(start=None, end=None, all_tech=False, force=False):
    """[start, end)와 겹치는 회계연도 resource를 통째로 받는다. 지난 회계연도는 이미 있으면 건너뜀."""
    print("EAC unit results (large)")
    d = OUT / "eac_units"
    d.mkdir(exist_ok=True)
    keys = list(EAC_UNIT)
    tag = "all" if all_tech else "batteries"
    for i, k in enumerate(keys):
        lo = EAC_UNIT_FROM[k]
        hi = EAC_UNIT_FROM[keys[i + 1]] if i + 1 < len(keys) else None
        if (end and lo >= end) or (start and hi and hi <= start):
            continue
        path = d / f"eac_unit_results_{tag}_{k}.csv.gz"  # 회계연도 하나가 수십 MB라 gzip
        if path.exists() and hi and not force:
            print(f"  {path.name} 있음, 건너뜀")
            continue
        df = neso_all(EAC_UNIT[k], filters=None if all_tech else {"technologyType": "Batteries"})
        df.to_csv(path, index=False)


def fetch_prices(start, end, force=False):
    """MID(APX·N2EX)와 정산가격을 settlementDate 기준 월별 CSV로 받는다. 시작 달은 1일부터 받는다."""
    print(f"Elexon MID + system prices {start:%Y-%m} ~ {end - timedelta(days=1)}")
    d_mid, d_sp = OUT / "elexon_mid", OUT / "elexon_system_prices"
    d_mid.mkdir(exist_ok=True)
    d_sp.mkdir(exist_ok=True)
    for m0, m1 in months(start, end):
        b = min(m1, end)
        last = b - timedelta(days=1)
        f_mid = d_mid / f"elexon_mid_{m0:%Y%m}.csv"
        if force or not covers(f_mid, last):
            # settlementDate는 영국 현지 날짜라 UTC 창을 앞뒤로 넓혀 받고 날짜로 자른다
            df = elexon("/datasets/MID/stream", {"from": f"{m0 - timedelta(days=1)}T22:00Z", "to": f"{b}T01:00Z"})
            if not df.empty:
                df = df[(df["settlementDate"] >= str(m0)) & (df["settlementDate"] < str(b))]
            df.to_csv(f_mid, index=False)
        f_sp = d_sp / f"elexon_system_prices_{m0:%Y%m}.csv"
        if force or not covers(f_sp, last):
            sp = []
            for d in days(m0, b):
                sp.append(elexon(f"/balancing/settlement/system-prices/{d}"))
                time.sleep(0.2)
            pd.concat(sp).to_csv(f_sp, index=False)
        print(f"  {m0:%Y-%m} ok")


def fetch_neso_package(name, sub, force=False):
    """NESO 데이터셋의 자료를 모두 받는다. datastore 자료는 CSV로, 나머지 파일은 원본 형식 그대로.
    자료 목록과 수정 시각은 _resources.json에 남기고, 수정 시각이 같은 자료는 다시 받지 않는다.
    자료 하나가 실패해도 나머지는 계속 받고, 받은 것은 그때그때 목록에 적는다(다시 실행하면 실패한 것만 받음)."""
    print(f"NESO package {name}")
    pkg = get(f"{NESO}/package_show", {"id": name}).json()["result"]
    d = OUT / sub
    d.mkdir(exist_ok=True)
    mpath = d / "_resources.json"
    old = {r["id"]: r for r in json.loads(mpath.read_text())} if mpath.exists() else {}
    manifest, used, failed = [], set(), []
    for res in pkg["resources"]:
        base = re.sub(r"[^0-9a-z]+", "_", (res.get("name") or "").lower()).strip("_")[:80] or res["id"]
        if base in used:
            base += "_" + res["id"][:8]
        used.add(base)
        fmt = (res.get("format") or "").lower()
        if res.get("datastore_active"):
            path = d / f"{base}.csv"
        elif fmt in FILE_FORMATS:
            path = d / f"{base}.{fmt}"
        else:
            path = None  # 웹 페이지·PDF 등은 목록에만 남긴다
        stamp = res.get("last_modified") or res.get("metadata_modified")
        entry = {"id": res["id"], "name": res.get("name"), "format": res.get("format"),
                 "last_modified": stamp, "url": res.get("url"), "file": path.name if path else None}
        # 목록에 기록이 없는데 파일이 있으면(지난 실행이 중간에 끊긴 경우) 받은 것으로 본다. 새로 받으려면 --force
        stale = res["id"] in old and old[res["id"]].get("last_modified") != stamp
        if path and (force or not path.exists() or stale):
            try:
                if res.get("datastore_active"):
                    neso_all(res["id"]).to_csv(path, index=False)
                else:
                    path.write_bytes(get(res["url"], timeout=600).content)
            except Exception as e:  # noqa: BLE001
                print(f"  [!] {res.get('name')} 실패: {e}")
                failed.append(res.get("name") or res["id"])
                entry["last_modified"] = None  # 다음 실행 때 다시 받도록
            time.sleep(1.2)
        manifest.append(entry)
        mpath.write_text(json.dumps(manifest + [r for i, r in old.items() if i not in {m["id"] for m in manifest}],
                                    indent=1, ensure_ascii=False))
    mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    if failed:
        raise RuntimeError(f"{name}: {len(failed)}개 자료 실패 ({', '.join(failed[:5])}). 다시 실행하면 이것만 받습니다.")


def fetch_cm():
    print("Capacity Market register")
    for name, rid in CM.items():
        df = neso_all(rid)
        # 공개 저장소라 담당자 전화번호·이메일 열은 저장하지 않는다
        df = df.drop(columns=[c for c in df.columns if re.search(r"Contact_(Telephone|Email)", c)])
        df.to_csv(OUT / f"{name}.csv", index=False)


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
    ap.add_argument("--only", help=f"받을 묶음, 쉼표 구분: {','.join(JOBS)} (기본 eac,cm,sample)")
    ap.add_argument("--units", action="store_true", help="기본 묶음에 배터리 유닛별 EAC 결과 추가")
    ap.add_argument("--start", type=date.fromisoformat, help="시작 날짜 YYYY-MM-DD (prices 기본 2021-09-01)")
    ap.add_argument("--end", type=date.fromisoformat, default=date.today(), help="끝 날짜(포함 안 함), 기본 오늘")
    ap.add_argument("--all-tech", action="store_true", help="units에서 배터리 외 기술도 받기")
    ap.add_argument("--force", action="store_true", help="이미 받은 파일도 다시 받기")
    a = ap.parse_args()
    jobs = a.only.split(",") if a.only else ["eac", "cm", "sample"] + (["units"] if a.units else [])
    if set(jobs) - set(JOBS):
        ap.error(f"모르는 묶음: {','.join(sorted(set(jobs) - set(JOBS)))}")
    if a.start and a.start >= a.end:
        ap.error("--start는 --end보다 앞이어야 합니다")
    for job in JOBS:
        if job not in jobs:
            continue
        if job == "eac":
            fetch_eac_summary()
        elif job == "cm":
            fetch_cm()
        elif job == "sample":
            fetch_elexon_sample()
        elif job == "units":
            fetch_eac_units(a.start, a.end, a.all_tech, a.force)
        elif job == "prices":
            fetch_prices(a.start or PRICES_START, a.end, a.force)
        else:
            fetch_neso_package(*NESO_PACKAGES[job], force=a.force)
    print("done ->", OUT)
