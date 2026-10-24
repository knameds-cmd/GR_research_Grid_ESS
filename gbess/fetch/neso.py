"""
NESO 데이터 포털(CKAN datastore)에서 SQL로 필요한 행만 받아 parquet로 저장한다.

    from gbess.fetch.neso import sql_cached
    df = sql_cached("stor_psh", 'SELECT * FROM "844a1a65-..." WHERE "Unit ID" ILIKE \'DINO%\'')

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
