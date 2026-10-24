"""
양수발전의 거래 외 수입: 용량시장(CM), FFR 월간 입찰, STOR 일일 경매, 무효전력(ORPS).

    .venv/bin/python -m gbess.realized.ancillary

2026-10-24 확인: 양수발전은 EAC(DC/DM/DR·BR·QR·SR), BR 2023-24, 정적 FFR 경매에 한 번도 낙찰되지 않았고,
STOR은 Cruachan 7일(2023), Ffestiniog 4일(2022)뿐이다. 그래서 공개 자료로 잡히지 않는 수입이 남는다:
의무 주파수 응답(MFR), Fast Reserve(2024-12 QR로 대체), 블랙스타트 등 양자계약. 이 몫은 회사 결산서로 위에서 맞춘다.

계산 방법과 단순화 (결과에 그대로 남김)
- CM: 낙찰된 CMU의 디레이팅 용량(MW) × 1,000 × 그 경매 낙찰가(£/kW/yr). 낙찰가 = 경매 총비용 ÷ 낙찰 용량
  (cm_auction_capacity_cost.csv, 알려진 낙찰가와 일치 확인). 인도연도는 10월~다음 해 9월.
  실제 지급은 월별 수요 가중이지만 여기서는 12개월에 고르게 나눈다. 2018-11~2019-10 CM 중단기의 지급은 나중에 소급 지급되어 발생 기준으로 둔다.
- FFR: 낙찰 건마다 가용 요금(£/h) × (평일·토·일 창 길이) × 해당 날짜 수. 공휴일은 평일로 센다. 지명 요금(nomination fee)은 넣지 않음.
- STOR: 낙찰 건 Contracted MW × 시장 낙찰가(£/MW/h) × 24h. 실제로는 STOR 창 시간만 지급되므로 **상한**.
- ORPS: 월별 사용량(MVArh, TOTAL) × 그 달 기본 지급 단가(“X = 1” 열, £/MVArh).
"""
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from gbess.fetch.neso import sql_cached

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results" / "realized"
SITE_NAMES = {"DINO": "Dinorwig", "FFES": "Ffestiniog", "CRUA": "Cruachan", "FOYE": "Foyers"}
UNIT_RE = r"^(DINO|FFES|CRUA|FOYE)"


# ---------------------------------------------------------------- 용량시장
def cm_prices():
    k = pd.read_csv(RAW / "cm_auction_capacity_cost.csv")
    k["price_kw_yr"] = k["Forecast Cost_GBP"] / (k["Capacity Awarded"] * 1000)
    return k.groupby("Auction Name")["price_kw_yr"].first()


def capacity_market():
    c = pd.read_csv(RAW / "cm_cmu.csv", low_memory=False)
    c["site"] = None
    for k, v in SITE_NAMES.items():
        c.loc[c["CM Unit Name"].astype(str).str.contains(v, case=False), "site"] = k
    c = c[c["site"].notna() & (c["Capacity Agreement Awarded"] == "Yes")].copy()
    price = cm_prices()
    c["price_kw_yr"] = c["Auction Name"].map(price)
    if c["price_kw_yr"].isna().any():
        raise ValueError(f"낙찰가가 없는 경매: {c.loc[c['price_kw_yr'].isna(), 'Auction Name'].unique()}")
    c["dy_start"] = c["Auction Name"].str[:4].astype(int)     # "2017-18 (T-1) ..." → 2017년 10월 시작
    c["gbp_yr"] = c["De Rated Capacity"].astype(float) * 1000 * c["price_kw_yr"]
    rows = []
    for _, r in c.iterrows():
        for m in pd.period_range(f"{r.dy_start}-10", f"{r.dy_start + 1}-09", freq="M"):
            rows.append({"month": str(m), "site": r.site, "cm_gbp": r.gbp_yr / 12})
    return pd.DataFrame(rows).groupby(["month", "site"], as_index=False).sum()


# ---------------------------------------------------------------- FFR 월간 입찰
def _ffr_file(path):
    df = pd.read_excel(path, header=None)
    hdr = df.index[df.iloc[:, 0].fillna("").astype(str).str.strip() == "Tender Ref"]
    if len(hdr) == 0:
        return None
    h = hdr[0]
    # pandas 3의 astype(str)은 결측을 그대로 두므로 빈 문자열로 먼저 바꾼다
    top, mid, low = (df.iloc[h + k].map(lambda v: "" if pd.isna(v) else str(v)) for k in range(3))

    def col(row, text):
        hit = [i for i, v in enumerate(row) if text.lower() in v.lower()]
        return hit

    # 상태 열 제목이 빈 보고서가 있다(TR124). 그때는 다른 보고서와 같은 위치(둘째 열)를 쓴다
    c_status = (col(top, "Status") or [1])[0]
    c_unit = col(top, "Tendered Unit")[0]
    c_start, c_end = col(top, "Start Date")[0], col(top, "End Date")[0]
    c_fee = col(mid, "Availability Fee")[0]
    durs = col(low, "Duration")[:3]
    body = df.iloc[h + 3:]
    body = body[body.iloc[:, c_status].fillna("").astype(str).str.strip().str.lower() == "accepted"]
    body = body[body.iloc[:, c_unit].fillna("").astype(str).str.strip().str.upper().str.match(UNIT_RE)]
    out = []
    for _, r in body.iterrows():
        start, end = pd.to_datetime(r.iloc[c_start], errors="coerce"), pd.to_datetime(r.iloc[c_end], errors="coerce")
        fee = pd.to_numeric(r.iloc[c_fee], errors="coerce")
        d = [pd.to_numeric(r.iloc[i], errors="coerce") for i in durs]
        if pd.isna(start) or pd.isna(end) or pd.isna(fee):
            continue
        out.append({"file": path.name, "unit": str(r.iloc[c_unit]).strip(), "start": start, "end": end,
                    "fee_gbp_h": float(fee), "wd_h": d[0], "sat_h": d[1], "sun_h": d[2]})
    return pd.DataFrame(out)


def ffr():
    files = sorted((RAW / "neso" / "firm-frequency-response-post-tender-reports").glob("*.xls*"))
    parts, failed = [], []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for f in files:
            try:
                p = _ffr_file(f)
            except (IndexError, ValueError) as e:
                # 머리글 형식이 다른 보고서(TR135, TR140). 양수발전 행이 없으면 빠진 수입이 없으므로 실패로 치지 않는다
                cells = pd.read_excel(f, header=None).fillna("").astype(str)
                if cells.apply(lambda c: c.str.strip().str.upper().str.match(UNIT_RE)).to_numpy().any():
                    failed.append(f"{f.name}: {e}")
                continue
            if p is None:
                failed.append(f"{f.name}: 머리글 없음")
            elif len(p):
                parts.append(p)
    t = pd.concat(parts, ignore_index=True)
    t.attrs["failed"] = failed
    rows = []
    for _, r in t.iterrows():
        for day in pd.date_range(r.start, r.end, freq="D"):
            h = r.sat_h if day.dayofweek == 5 else r.sun_h if day.dayofweek == 6 else r.wd_h
            h = 0.0 if pd.isna(h) else float(h)
            rows.append({"month": day.strftime("%Y-%m"), "site": r.unit[:4], "ffr_gbp": r.fee_gbp_h * h})
    tenders = t.assign(n_files=len(files))
    tenders.attrs["failed"] = failed
    return pd.DataFrame(rows).groupby(["month", "site"], as_index=False).sum(), tenders


# ---------------------------------------------------------------- STOR
def stor():
    q = ('SELECT * FROM "844a1a65-0a3c-4704-b327-d1685d0c397b" WHERE "Status" = \'Accepted\' AND '
         '("Unit ID" ILIKE \'DINO%\' OR "Unit ID" ILIKE \'FFES%\' OR "Unit ID" ILIKE \'CRUA%\' OR "Unit ID" ILIKE \'FOYE%\')')
    s = sql_cached("stor_psh_accepted", q)
    if s.empty:
        return pd.DataFrame(columns=["month", "site", "stor_gbp_upper"])
    s["gbp"] = s["Contracted MW"].astype(float) * s["Market Clearing Price"].astype(float) * 24
    s["month"] = pd.to_datetime(s["Service Delivery From"]).dt.strftime("%Y-%m")
    s["site"] = s["Unit ID"].str[:4]
    return s.groupby(["month", "site"], as_index=False)["gbp"].sum().rename(columns={"gbp": "stor_gbp_upper"})


# ---------------------------------------------------------------- 무효전력 (ORPS)
ORPS_LONG = "528b03d2-4008-4b65-a732-a001cd835a3b"      # 2020-04 ~
ORPS_HIST = "3ee65326-3729-421d-b667-b2164501e4a5"      # 2013-10 ~ 2020-03 (가로형)
ORPS_RATE = "b00df5b1-4179-44e3-b556-28a836ad619f"
_WHERE = '"Unit" ILIKE \'DINO%\' OR "Unit" ILIKE \'FFES%\' OR "Unit" ILIKE \'CRUA%\' OR "Unit" ILIKE \'FOYE%\''


def _num(x):
    return pd.to_numeric(pd.Series(x).astype(str).str.replace(",", ""), errors="coerce")


def orps():
    long = sql_cached("orps_psh_long", f'SELECT * FROM "{ORPS_LONG}" WHERE {_WHERE}')
    long["month"] = pd.to_datetime(long["Month-Year"], format="%b-%y").dt.strftime("%Y-%m")
    long["mvarh"] = _num(long["TOTAL"]).to_numpy()
    hist = sql_cached("orps_psh_hist", f'SELECT * FROM "{ORPS_HIST}" WHERE {_WHERE}')
    rows = []
    for c in hist.columns:
        m = re.match(r"^\s*([A-Za-z]{3})\w*\s*-?\s*(\d{2})\s*-?\s*(TOTAL|Total)\s*$", c) or \
            re.match(r"^\s*([A-Za-z]{3})\s*-(\d{2})\s*(TOTAL)\s*$", c)
        if not m:
            continue
        month = pd.to_datetime(f"{m.group(1)} 20{m.group(2)}", format="%b %Y").strftime("%Y-%m")
        rows.append(pd.DataFrame({"Unit": hist["Unit"], "month": month, "mvarh": _num(hist[c]).to_numpy()}))
    hist_l = pd.concat(rows)
    allm = pd.concat([hist_l, long[["Unit", "month", "mvarh"]]])
    allm = allm.drop_duplicates(["Unit", "month"], keep="last")
    rate = sql_cached("orps_rate", f'SELECT * FROM "{ORPS_RATE}"')
    rate["month"] = pd.to_datetime(rate["Year"].astype(str) + "-" + rate["Month"].astype(str).str.zfill(2)).dt.strftime("%Y-%m")
    rate = rate.set_index("month")["X = 1"].astype(float)
    allm["rate"] = allm["month"].map(rate)
    allm["site"] = allm["Unit"].str[:4]
    allm["orps_gbp"] = allm["mvarh"].fillna(0) * allm["rate"]
    missing_rate = allm.loc[allm["rate"].isna() & (allm["mvarh"] > 0), "month"].unique()
    return allm.groupby(["month", "site"], as_index=False)[["mvarh", "orps_gbp"]].sum(), sorted(missing_rate)


def build():
    cm = capacity_market()
    f, tenders = ffr()
    st = stor()
    o, missing_rate = orps()
    df = cm.merge(f, on=["month", "site"], how="outer").merge(st, on=["month", "site"], how="outer") \
        .merge(o, on=["month", "site"], how="outer").fillna(0.0)
    return df, tenders, missing_rate


def main():
    df, tenders, missing_rate = build()
    OUT.mkdir(parents=True, exist_ok=True)
    df.sort_values(["month", "site"]).to_csv(OUT / "psh_ancillary_monthly.csv", index=False)
    tenders.to_csv(OUT / "psh_ffr_tenders.csv", index=False)
    y = df.assign(year=df["month"].str[:4]).groupby(["year", "site"])[["cm_gbp", "ffr_gbp", "stor_gbp_upper", "orps_gbp"]].sum()
    print((y / 1e6).round(2).to_string())
    print(f"FFR 낙찰 건수 {len(tenders)} (보고서 {tenders['n_files'].iat[0] if len(tenders) else 0}개)")
    for x in tenders.attrs.get("failed", []):
        print("  FFR 읽기 실패:", x)
    if missing_rate:
        print("ORPS 단가 없는 달:", missing_rate[:12], "...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
