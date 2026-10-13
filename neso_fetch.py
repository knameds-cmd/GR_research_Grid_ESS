#!/usr/bin/env python3
"""
NESO Data Portal 다운로드 도구 (GB 계통용 배터리 연구용)

NESO 데이터 포털(https://www.neso.energy/data-portal)은 CKAN 기반이라 키 없이 API로 받을 수 있습니다.
gb_data_fetch.py(EAC 요약·유닛별 결과, EAC 이전 DC, skip rate, CM, Elexon 가격)가 받지 않는 나머지
NESO 데이터셋을 받습니다. 연구에 필요한 데이터셋 목록을 묶음(group)으로 정리해 두고, 각 데이터셋의 파일(리소스)을
data/raw/neso/<데이터셋>/ 폴더에 그대로 내려받습니다. 이미 받은 파일은 건너뛰므로 중간에 끊겨도 다시
실행하면 이어서 받습니다. 받은 내역은 data/raw/neso/MANIFEST.csv 에 남습니다(재현성).

설치:
    pip install requests pandas

자주 쓰는 명령 (저장소 루트에서):
    python3 neso_fetch.py list                      # 묶음과 데이터셋 목록
    python3 neso_fetch.py list core                 # core 묶음의 각 데이터셋 파일 목록·크기 (받기 전에 확인)
    python3 neso_fetch.py search "dynamic moderation"   # 포털에서 데이터셋 이름 찾기
    python3 neso_fetch.py get core --dry-run        # 무엇을 받을지 미리 보기
    python3 neso_fetch.py get core requirements     # 1순위 묶음 받기
    python3 neso_fetch.py get system-inertia        # 데이터셋 하나만
    python3 neso_fetch.py get system-frequency-data --match 2023 --allow-large   # 큰 파일은 골라서

옵션:
    --match REGEX    파일 이름에 REGEX가 들어간 것만 받기 (대소문자 무시). 예: --match "2024|2025"
    --max-mb N       N MB보다 큰 파일은 건너뛰기 (기본 200). --allow-large 로 해제
    --dry-run        받지 않고 목록·크기만 출력
    --force          이미 받은 파일도 다시 받기

참고:
    - 데이터셋 이름(slug)은 2026-10-06 포털 검색으로 확인한 것입니다. 이름이 바뀌어 못 찾으면
      스크립트가 비슷한 이름을 자동으로 검색해 보여 줍니다. 그 이름으로 다시 실행하세요.
    - 1초 주파수(system-frequency-data)는 한 달에 수십~수백 MB라 heavy 묶음으로 따로 뒀습니다.
    - EAC 결과, EAC 이전 DC, skip rate, MID·정산가격은 gb_data_fetch.py로 받습니다(아래 ELSEWHERE).
      두 스크립트가 같은 자료를 다른 폴더에 받지 않도록 여기서는 받지 않습니다.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

NESO_API = os.environ.get("NESO_API", "https://api.neso.energy/api/3/action")
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "raw" / "neso"
MANIFEST = OUT / "MANIFEST.csv"

# ---------------------------------------------------------------------------
# 받을 데이터셋 목록: 묶음 -> [(slug, 설명)]
# ---------------------------------------------------------------------------
GROUPS = {
    "core": [  # 지금 꼭 필요한 것 (gb_data_fetch.py 자료의 빈 곳)
        ("eac-br-auction-results", "2025.10 이전 Balancing Reserve 경매 결과 (2024.3~)"),
    ],
    "requirements": [  # 상품별 필요량 — 포화 분석, 가격 설명 변수
        ("dynamic-moderation-requirements", "DM 필요량"),
        ("dynamic-regulation-requirements", "DR 필요량"),
        ("long-term-forecasts-for-dc-dm-dr-requirements", "DC/DM/DR 필요량 장기 전망"),
        ("balancing-reserve-auction-requirement-forecast", "BR 필요량 전망"),
        ("quick-reserve-auction-requirement-forecast", "QR 필요량 전망"),
    ],
    "drivers": [  # 가격·서비스 수요를 설명하는 변수, 롤링 호라이즌 예측 입력
        ("system-inertia", "계통 관성"),
        ("1-day-ahead-demand-forecast", "하루 전 수요 예측"),
        ("day-ahead-wind-forecast", "하루 전 풍력 예측"),
        ("embedded-wind-and-solar-forecasts", "배전망 연결 풍력·태양광 예측"),
    ],
    "costs": [  # 비용 쪽 규칙(망요금) — 반사실에 넣을 경우
        ("transmission-network-use-of-system-tnuos-tariffs", "TNUoS 송전요금"),
        ("bsuos-fixed-tariffs", "BSUoS 고정요금 (2023.4~)"),
        ("daily-balancing-costs-balancing-services-use-of-system", "일별 밸런싱 비용"),
    ],
    "obp": [  # BM 밖(비BM) 배터리의 일괄발령 데이터
        ("obp-non-bm-physical-notifications", "비BM 유닛 물리적 계획"),
        ("obp-non-bm-reserve-instructions", "비BM 예비력 지시"),
        ("obp-reserve-availability-utilisation-price", "OBP 예비력 가용·이용 가격"),
    ],
    "history": [  # EFR/FFR 시절(2016~2021)까지 계보 잇기
        ("firm-frequency-response-post-tender-reports", "FFR/EFR 낙찰 보고서"),
    ],
    "heavy": [  # 매우 큼 — --match 로 기간을 골라 받기
        ("system-frequency-data", "1초 계통 주파수 (월별 파일, 파일당 수십~수백 MB)"),
    ],
}
ALL_SLUGS = {slug: desc for items in GROUPS.values() for slug, desc in items}

# gb_data_fetch.py가 받는 데이터셋 -> 그쪽 명령과 저장 폴더 (중복 다운로드 방지)
ELSEWHERE = {
    "eac-auction-results": ("--only eac,units", "data/raw/eac_results_summary.csv, data/raw/eac_units/"),
    "dynamic-containment-data": ("--only dc", "data/raw/dc_pre_eac/"),
    "skip-rates": ("--only skip", "data/raw/skip_rates/"),
}

SESSION = requests.Session()
SESSION.headers["User-Agent"] = "GR_research_Grid_ESS data fetch (academic research)"
RETRY_STATUS = {429, 500, 502, 503, 504}


class CkanError(Exception):
    pass


# ---------------------------------------------------------------------------
# HTTP / CKAN helpers
# ---------------------------------------------------------------------------
def http_get(url, params=None, stream=False, timeout=180, tries=5):
    """GET with retries on network errors and 429/5xx (2, 4, 8, 16 s backoff)."""
    for attempt in range(tries):
        try:
            r = SESSION.get(url, params=params, stream=stream, timeout=timeout)
            if r.status_code in RETRY_STATUS and attempt < tries - 1:
                wait = 2 ** (attempt + 1)
                print(f"    HTTP {r.status_code}, {wait}s 후 재시도")
                time.sleep(wait)
                continue
            return r
        except (requests.ConnectionError, requests.Timeout) as e:
            if attempt == tries - 1:
                raise
            wait = 2 ** (attempt + 1)
            print(f"    연결 오류({e.__class__.__name__}), {wait}s 후 재시도")
            time.sleep(wait)


def ckan(action, **params):
    r = http_get(f"{NESO_API}/{action}", params=params)
    try:
        j = r.json()
    except ValueError:
        r.raise_for_status()
        raise CkanError(f"{action}: JSON이 아닌 응답 (HTTP {r.status_code})")
    if not j.get("success"):
        raise CkanError(f"{action}: {j.get('error')}")
    return j["result"]


def search_datasets(query, rows=20):
    res = ckan("package_search", q=query, rows=rows)
    return [(p["name"], p.get("title", ""), len(p.get("resources", []))) for p in res.get("results", [])]


def dataset_resources(slug):
    """Return (title, resources) for a dataset, or suggest similar names if not found."""
    try:
        pkg = ckan("package_show", id=slug)
    except (CkanError, requests.HTTPError) as e:
        print(f"  [!] '{slug}' 데이터셋을 찾지 못했습니다 ({e}).")
        try:
            cands = search_datasets(slug.replace("-", " "), rows=8)
        except Exception as e2:  # noqa: BLE001
            print(f"      검색도 실패했습니다: {e2}")
            return None, []
        if cands:
            print("      비슷한 이름 (이 이름으로 다시 실행하세요):")
            for name, title, n in cands:
                print(f"        - {name}  ({title}, 파일 {n}개)")
        return None, []
    return pkg.get("title", slug), pkg.get("resources", [])


def safe_name(s):
    return re.sub(r"[^\w.\-]+", "_", s or "").strip("_")[:120] or "resource"


def resource_ext(res):
    suffix = Path(urlparse(res.get("url") or "").path).suffix.lstrip(".").lower()
    if suffix and len(suffix) <= 5:
        return suffix
    fmt = (res.get("format") or "").lower().strip(".")
    return fmt if fmt else "bin"


def resource_bytes(res):
    """Size from CKAN metadata, else HEAD Content-Length, else None."""
    size = res.get("size")
    if isinstance(size, (int, float)) and size > 0:
        return int(size)
    url = res.get("url")
    if not url:
        return None
    try:
        h = SESSION.head(url, allow_redirects=True, timeout=30)
        cl = h.headers.get("Content-Length")
        return int(cl) if cl and cl.isdigit() else None
    except requests.RequestException:
        return None


def fmt_mb(b):
    return "?" if b is None else f"{b / 1e6:,.1f}"


def fmt_size(b):
    if b is None:
        return "?"
    if b < 1e3:
        return f"{b} B"
    return f"{b / 1e3:,.0f} KB" if b < 1e6 else f"{b / 1e6:,.1f} MB"


def append_manifest(row):
    OUT.mkdir(parents=True, exist_ok=True)
    new = not MANIFEST.exists()
    with MANIFEST.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if new:
            w.writeheader()
        w.writerow(row)


def stream_to_file(url, dest):
    """Download to <dest>.part then rename; return (bytes, sha256)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    r = http_get(url, stream=True, timeout=600)
    r.raise_for_status()
    h, n = hashlib.sha256(), 0
    with tmp.open("wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            if chunk:
                f.write(chunk)
                h.update(chunk)
                n += len(chunk)
    tmp.replace(dest)
    return n, h.hexdigest()


def datastore_to_csv(resource_id, dest, filters=None, page=32000):
    """Page through datastore_search and write CSV; return number of rows."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    off, total, writer = 0, 0, None
    with tmp.open("w", newline="", encoding="utf-8") as f:
        while True:
            params = {"resource_id": resource_id, "limit": page, "offset": off}
            if filters:
                params["filters"] = json.dumps(filters)
            recs = ckan("datastore_search", **params)["records"]
            if recs and writer is None:
                fields = [k for k in recs[0].keys() if k != "_full_text"]
                writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
                writer.writeheader()
            for rec in recs:
                writer.writerow(rec)
            total += len(recs)
            off += len(recs)
            print(f"    {resource_id[:8]}… {total:,} rows")
            if len(recs) < page:
                break
            time.sleep(1.0)
    tmp.replace(dest)
    return total


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def expand(targets):
    slugs = []
    for t in targets:
        if t == "all":
            slugs += [s for g, items in GROUPS.items() if g != "heavy" for s, _ in items]
        elif t in GROUPS:
            slugs += [s for s, _ in GROUPS[t]]
        else:
            slugs.append(t)  # 목록에 없는 데이터셋 이름도 그대로 허용
    seen = set()
    return [s for s in slugs if not (s in seen or seen.add(s))]


def cmd_list(args):
    if not args.targets:
        for g, items in GROUPS.items():
            print(f"[{g}]")
            for slug, desc in items:
                print(f"  {slug:55s} {desc}")
        print("\n데이터셋별 파일 목록:  python3 neso_fetch.py list <묶음 또는 데이터셋>")
        return
    for slug in expand(args.targets):
        title, res = dataset_resources(slug)
        if title is None:
            continue
        print(f"\n== {slug} — {title} ({len(res)} files)")
        for r in res:
            size = r.get("size") if isinstance(r.get("size"), (int, float)) else None
            print(f"   {fmt_mb(size):>9s} MB  {resource_ext(r):5s}  {r.get('last_modified') or r.get('created') or '':19.19s}  {r.get('name')}")


def cmd_search(args):
    for name, title, n in search_datasets(" ".join(args.query), rows=args.rows):
        print(f"  {name:60s} {title}  (파일 {n}개)")


def cmd_get(args):
    pattern = re.compile(args.match, re.I) if args.match else None
    totals = {"ok": 0, "skip": 0, "large": 0, "fail": 0, "elsewhere": 0}
    for slug in expand(args.targets):
        if slug in ELSEWHERE:
            cmd, where = ELSEWHERE[slug]
            print(f"\n== {slug}: gb_data_fetch.py가 받는 자료입니다 -> python3 gb_data_fetch.py {cmd}  ({where})")
            totals["elsewhere"] += 1
            continue
        title, res = dataset_resources(slug)
        if title is None:
            totals["fail"] += 1
            continue
        print(f"\n== {slug} — {title}")
        used = set()
        for r in res:
            name = r.get("name") or r.get("id")
            if pattern and not pattern.search(name or ""):
                continue
            base = safe_name(name)
            if base in used:  # 이름이 같은 파일이 여러 개면 id를 붙여 구분
                base = f"{base}_{r['id'][:8]}"
            used.add(base)
            dest = OUT / slug / f"{base}.{resource_ext(r)}"
            if dest.exists() and dest.stat().st_size > 0 and not args.force:
                print(f"   skip (이미 있음)  {dest.relative_to(ROOT)}")
                totals["skip"] += 1
                continue
            size = resource_bytes(r)
            if size is not None and size > args.max_mb * 1e6 and not args.allow_large:
                print(f"   skip (큼 {fmt_mb(size)} MB > {args.max_mb} MB, --allow-large 필요)  {name}")
                totals["large"] += 1
                continue
            if args.dry_run:
                print(f"   would get {fmt_mb(size):>9s} MB  {dest.relative_to(ROOT)}")
                continue
            try:
                if r.get("url"):
                    n, sha = stream_to_file(r["url"], dest)
                    status = "file"
                elif r.get("datastore_active"):
                    dest = dest.with_suffix(".csv")
                    n, sha = datastore_to_csv(r["id"], dest), ""
                    status = "datastore"
                else:
                    print(f"   [!] 다운로드 주소가 없음: {name}")
                    totals["fail"] += 1
                    continue
            except Exception as e:  # noqa: BLE001
                print(f"   [!] 실패: {name} ({e})")
                totals["fail"] += 1
                continue
            shown = fmt_size(n) if status == "file" else f"{n:,} rows"
            print(f"   ok   {shown:>12s}  {dest.relative_to(ROOT)}")
            totals["ok"] += 1
            append_manifest({
                "downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "dataset": slug, "resource_id": r.get("id"), "resource_name": name,
                "format": r.get("format"), "url": r.get("url"), "last_modified": r.get("last_modified"),
                "mode": status, "bytes_or_rows": n, "sha256": sha, "path": str(dest.relative_to(ROOT)),
            })
            time.sleep(0.5)
    print(f"\n완료: 받음 {totals['ok']}, 이미 있음 {totals['skip']}, 큰 파일 건너뜀 {totals['large']}, 실패 {totals['fail']}"
          + (f", gb_data_fetch.py 담당 {totals['elsewhere']}" if totals["elsewhere"] else ""))
    if totals["large"]:
        print("큰 파일은 --match 로 기간을 고른 뒤 --allow-large 를 붙여 받으세요.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="NESO 데이터 포털 다운로드 도구 (자세한 사용법은 파일 맨 위 설명)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="묶음·데이터셋·파일 목록 보기")
    p.add_argument("targets", nargs="*", help="묶음 이름(core, requirements, ...) 또는 데이터셋 이름")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("search", help="포털에서 데이터셋 이름 검색")
    p.add_argument("query", nargs="+")
    p.add_argument("--rows", type=int, default=20)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("get", help="데이터셋 파일 받기")
    p.add_argument("targets", nargs="+", help="묶음 이름, 데이터셋 이름, 또는 all (heavy 제외)")
    p.add_argument("--match", help="파일 이름 정규식 필터 (대소문자 무시)")
    p.add_argument("--max-mb", type=float, default=200)
    p.add_argument("--allow-large", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_get)

    args = ap.parse_args(argv)
    try:
        args.func(args)
    except BrokenPipeError:  # e.g. output piped into `head`
        return 0
    except KeyboardInterrupt:
        print("\n중단됨. 다시 실행하면 받은 파일은 건너뛰고 이어서 받습니다.")
        return 130
    except requests.RequestException as e:
        print(f"\n[!] 네트워크 오류: {e}\n    인터넷 연결이나 회사·학교 프록시를 확인하세요.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
