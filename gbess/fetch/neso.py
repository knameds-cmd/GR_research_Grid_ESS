"""
NESO 데이터 포털(CKAN datastore)에서 SQL로 필요한 행만 받아 parquet로 저장한다.

    from gbess.fetch.neso import sql_cached
    df = sql_cached("stor_psh", 'SELECT * FROM "844a1a65-..." WHERE "Unit ID" ILIKE \'DINO%\'')

    .venv/bin/python -m gbess.fetch.neso constraints     # 송전 제약 자료 (아래 CONSTRAINTS)

결과: data/raw/neso_sql/<name>.parquet. 같은 이름이 있으면 다시 받지 않는다(force=True면 다시).
받은 기록(질의문, 행 수, sha256)은 data/raw/neso_sql/MANIFEST.csv에 남긴다.
datastore_search_sql은 한 번에 최대 32,000행을 돌려주므로 OFFSET으로 나눠 받는다.
"""
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "raw" / "neso_sql"
API = "https://api.neso.energy/api/3/action/datastore_search_sql"
PAGE = 30000


def sql(query):
    rows, offset = [], 0
    while True:
        q = f"{query} LIMIT {PAGE} OFFSET {offset}"
        r = requests.get(API, params={"sql": q}, timeout=300)
        r.raise_for_status()
        j = r.json()
        if not j.get("success"):
            raise RuntimeError(f"NESO SQL 실패: {j.get('error')}")
        recs = j["result"]["records"]
        rows += recs
        if len(recs) < PAGE:
            break
        offset += PAGE
    df = pd.DataFrame(rows)
    return df.drop(columns=[c for c in ("_full_text",) if c in df.columns])


def sql_cached(name, query, force=False):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.parquet"
    if path.exists() and not force:
        return pd.read_parquet(path)
    df = sql(query)
    df.astype(str).to_parquet(path, index=False)   # 원자료는 문자열 그대로 보관, 형 변환은 읽는 쪽에서
    man = OUT / "MANIFEST.csv"
    row = pd.DataFrame([{"downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "name": name,
                         "rows": len(df), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "query": query}])
    if man.exists():
        old = pd.read_csv(man)
        row = pd.concat([old[old["name"] != name], row], ignore_index=True)
    row.to_csv(man, index=False)
    return pd.read_parquet(path)


# 송전 제약 자료. 하루 전 경계 조류·한계는 2023-01부터만 있다(2026-10-25 확인). 그 전 기간의 위치 신호는 BM 자료에서 만든다
CONSTRAINTS = {"da_constraint_flows": "38a18ec1-9e40-465d-93fb-301e80fd1352"}
BREAKDOWN = {"2017-2018": "3651e9e3-52a8-46b6-a675-3a4c2aedc813", "2018-2019": "26af8438-1824-4436-9bbd-d397a9a517e2",
             "2019-2020": "c4d2be3a-4c05-4fac-be7e-56368ca46142", "2020-2021": "87088ac4-72d5-48ff-9ee1-f2a99e18277a",
             "2021-2022": "419337fb-f609-45e3-9097-798a41b4b3de", "2022-2023": "efb633ae-f6d7-444b-8759-449ac0539dd0",
             "2023-2024": "24d067d8-1328-452a-9720-21cb691e491e", "2024-2025": "748557ef-2bb3-41c0-8181-5f1a148c1ff4",
             "2025-2026": "6afe1c2b-6d70-4e76-8e74-0952b0a2beab", "2026-2027": "4136a8e2-07c5-4784-8096-28999447a16e"}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["constraints"])
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    for name, rid in CONSTRAINTS.items():
        df = sql_cached(name, f'SELECT * FROM "{rid}" ORDER BY "_id"', force=a.force)
        print(name, len(df))
    for fy, rid in BREAKDOWN.items():   # 일별 제약 비용·물량 (열 이름이 해마다 조금씩 다르다)
        df = sql_cached(f"constraint_breakdown_{fy.replace('-', '_')}", f'SELECT * FROM "{rid}" ORDER BY "_id"',
                        force=a.force)
        print(fy, len(df), list(df.columns)[1:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
