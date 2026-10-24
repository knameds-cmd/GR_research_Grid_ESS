"""
Elexon Insights에서 BM 현금흐름·PN·BOALF·가격을 월 단위 parquet로 받는다.

    .venv/bin/python -m gbess.fetch.elexon cashflows --start 2016-01 --end 2026-10
    .venv/bin/python -m gbess.fetch.elexon pn --units psh --start 2016-01 --end 2026-10
    .venv/bin/python -m gbess.fetch.elexon boalf --units psh --start 2016-01 --end 2026-10
    .venv/bin/python -m gbess.fetch.elexon prices --start 2018-01 --end 2021-09

- cashflows: 날짜·방향(bid/offer)마다 한 번 호출하면 그날 BM에 참여한 모든 유닛의 결제구간별 현금흐름이 나온다.
  유닛별 쌍(pair) 내역은 버리고 결제구간 합계(totalCashflow)만 남긴다.
- pn, boalf: --units로 고른 유닛만. 한 호출에 여러 유닛을 넣고, 하루씩 끊어 받는다.
- prices: MID(APX만)와 정산가격. 기존 gb_data_fetch.py의 CSV와 같은 열을 parquet로 저장.
결과: data/raw/elexon/<dataset>/<dataset>_YYYYMM.parquet. 받은 달마다 MANIFEST.csv에 행 수·sha256을 남긴다.
이미 있는 달은 건너뛴다(--force면 다시). 끝나지 않은 달(이번 달)은 받지만 MANIFEST에 partial로 표시한다.
"""
import argparse
import hashlib
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "raw" / "elexon"
API = "https://data.elexon.co.uk/bmrs/api/v1"
RETRY = {429, 500, 502, 503, 504, 520, 521, 522, 523, 524}
SESSION = requests.Session()

# 유닛 묶음. 양수발전은 Elexon 등록부의 fuelType PS (2026-10 기준 16개)
UNIT_SETS = {
    "psh": [f"T_DINO-{i}" for i in range(1, 7)] + [f"T_FFES-{i}" for i in range(1, 5)]
           + [f"T_CRUA-{i}" for i in range(1, 5)] + ["T_FOYE-1", "T_FOYE-2"],
}


def get(path, params=None, tries=6):
    params = {**(params or {}), "format": "json"}
    for k in range(tries):
        try:
            r = SESSION.get(API + path, params=params, timeout=120)
            if r.status_code in RETRY:
                raise requests.HTTPError(f"{r.status_code}")
            r.raise_for_status()
            j = r.json()
            return j["data"] if isinstance(j, dict) and "data" in j else j
        except (requests.RequestException, ValueError) as e:
            if k == tries - 1:
                raise
            wait = 5 * 2 ** k
            print(f"    재시도 {k + 1}/{tries - 1} ({e}), {wait}초 대기", flush=True)
            time.sleep(wait)


def months(start, end):
    """'2016-01' ~ '2026-10'(포함 안 함)의 각 달 첫날."""
    m = date.fromisoformat(start + "-01")
    stop = date.fromisoformat(end + "-01")
    while m < stop:
        yield m
        m = (m.replace(day=28) + timedelta(days=4)).replace(day=1)


def days_of(m):
    d = m
    nxt = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
    while d < nxt:
        yield d
        d += timedelta(days=1)


def fetch_cashflows(m):
    rows = []
    for d in days_of(m):
        for side in ("bid", "offer"):
            for x in get(f"/balancing/settlement/indicative/cashflows/all/{side}/{d}"):
                x.pop("bidOfferPairCashflows", None)
                x["side"] = side
                rows.append(x)
    return pd.DataFrame(rows)


def fetch_unit_stream(dataset, units, m):
    rows = []
    for d in days_of(m):
        rows += get(f"/datasets/{dataset}/stream",
                    {"from": f"{d}T00:00Z", "to": f"{d + timedelta(days=1)}T00:00Z", "bmUnit": units})
    # 하루씩 끊어 받으면 자정에 걸친 구간이 양쪽 날에 다 나온다 (2026-01 PN 시험에서 960행 중복 확인)
    return pd.DataFrame(rows).drop_duplicates()


def fetch_prices(m):
    nxt = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
    mid = []
    for d in days_of(m):
        mid += get("/datasets/MID/stream", {"from": f"{d}T00:00Z", "to": f"{d + timedelta(days=1)}T00:00Z"})
    sp = []
    for d in days_of(m):
        sp += get(f"/balancing/settlement/system-prices/{d}")
    mid = pd.DataFrame(mid)
    if not mid.empty:
        mid = mid[mid["dataProvider"] == "APXMIDP"].drop_duplicates(["startTime"])
    return {"mid": mid, "system_prices": pd.DataFrame(sp)}, nxt


def write(dataset, m, df, partial):
    folder = OUT / dataset
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{dataset}_{m:%Y%m}.parquet"
    df.to_parquet(path, index=False)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    man = OUT / "MANIFEST.csv"
    row = pd.DataFrame([{"downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "dataset": dataset, "month": f"{m:%Y-%m}", "rows": len(df),
                         "partial": partial, "sha256": sha, "path": str(path.relative_to(ROOT))}])
    if man.exists():
        old = pd.read_csv(man)
        row = pd.concat([old[old["path"] != row["path"].iat[0]], row], ignore_index=True)
    row.to_csv(man, index=False)
    print(f"  {path.relative_to(ROOT)}: {len(df):,}행{' (진행 중인 달)' if partial else ''}", flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=["cashflows", "pn", "boalf", "prices"])
    ap.add_argument("--start", required=True, help="YYYY-MM")
    ap.add_argument("--end", required=True, help="YYYY-MM (포함 안 함)")
    ap.add_argument("--units", help=f"유닛 묶음({', '.join(UNIT_SETS)}) 또는 쉼표로 구분한 Elexon 유닛 이름")
    ap.add_argument("--tag", help="pn/boalf 저장 이름 꼬리표 (기본: --units 값)")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)

    today = date.today()
    for m in months(a.start, a.end):
        partial = m.year == today.year and m.month == today.month
        if a.what == "cashflows":
            names = ["bm_cashflows"]
        elif a.what == "prices":
            names = ["mid", "system_prices"]
        else:
            if not a.units:
                sys.exit("--units가 필요합니다")
            names = [f"{a.what}_{a.tag or a.units}"]
        if not a.force and not partial and all((OUT / n / f"{n}_{m:%Y%m}.parquet").exists() for n in names):
            continue
        print(f"{a.what} {m:%Y-%m}", flush=True)
        if a.what == "cashflows":
            write(names[0], m, fetch_cashflows(m), partial)
        elif a.what == "prices":
            dfs, _ = fetch_prices(m)
            for n in names:
                write(n, m, dfs[n], partial)
        else:
            units = UNIT_SETS.get(a.units) or a.units.split(",")
            write(names[0], m, fetch_unit_stream(a.what.upper(), units, m), partial)
    return 0


if __name__ == "__main__":
    sys.exit(main())
