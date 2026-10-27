"""
결산서 대조: 공개 자료로 다시 만든 양수발전 수익이 회사 결산서의 몇 %를 잡는가, 못 잡는 몫은 어느 항목인가.

    .venv/bin/python -m gbess.validation.accounts

결산서 숫자: literature/sources/psh/accounts.csv (출처 쪽수 포함)
  - Cruachan: Drax Pumped Storage Ltd(06657336). 2021-07부터 Cruachan 하나만 가진 회사라 발전소 단위로 맞춰 볼 수 있고,
    수입이 전력 판매 / BM / 부가서비스·기타로 나뉜다. 부가서비스 = 스핀 대기, 예비력, 주파수 응답, 블랙스타트, 제약 계약, 무효전력.
  - Dinorwig + Ffestiniog: First Hydro Company(02444277). 시장별 구분 없음. 총이익에서 미실현 공정가치 변동을 뺀 값(매출 − 매출원가)과 비교.
공개 재구성: results/realized/psh_monthly.csv(도매 PN × MID, BM 순수익), psh_ancillary_monthly.csv(CM, FFR, Fast Reserve, STOR 상한, ORPS).
먼저 gbess.realized.psh와 gbess.realized.ancillary를 돌려 둔다.

해석할 때 주의
  - 결산서 매출원가에는 양수 전력 외에 망요금·BSUoS 같은 비용도 있을 수 있다. 그래서 "전력 판매 − 매출원가"는 도매 순수익의 하한 쪽이다.
  - 결산서 전력 판매에는 선도 판매(헤지) 손익이 들어 있다. 공개 재구성은 당일 MID로만 값을 매기므로, 그 차이가 선도 판매 몫이다.
  - CM은 Cruachan 결산서에서 "기타"에 들어 있다고 보고 부가서비스·기타와 비교한다(결산서에 명시 없음).
결과: results/validation/accounts.csv
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REAL = ROOT / "results" / "realized"
OUT = ROOT / "results" / "validation"
ACC = ROOT / "literature" / "sources" / "psh" / "accounts.csv"
ENTITY_SITES = {"DPSL": ["CRUA"], "FHC": ["DINO", "FFES"]}
ANC = ["cm_gbp", "ffr_gbp", "fr_gbp", "stor_gbp_upper", "orps_gbp"]


def public(sites, year, months):
    """그 해 마지막 months개월(Cruachan 2021은 7~12월)의 공개 재구성 합계, £m."""
    t = pd.read_csv(REAL / "psh_monthly.csv")
    a = pd.read_csv(REAL / "psh_ancillary_monthly.csv")
    want = pd.period_range(f"{year}-{13 - months:02d}", f"{year}-12", freq="M").astype(str)
    t = t[t["site"].isin(sites) & t["month"].isin(want)]
    a = a[a["site"].isin(sites) & a["month"].isin(want)]
    return {"pub_wholesale": t["wholesale_mid_gbp"].sum() / 1e6, "pub_bm": t["bm_net_gbp"].sum() / 1e6,
            "pub_ancillary": a[ANC].sum().sum() / 1e6, "pub_months": t["month"].nunique()}


def build():
    acc = pd.read_csv(ACC)
    rows = []
    for _, r in acc.iterrows():
        p = public(ENTITY_SITES[r.entity], int(r.year), int(r.months))
        if p["pub_months"] < r.months:
            continue
        row = {"entity": r.entity, "site": r.site, "year": r.year, "months": r.months, **p}
        row["pub_total"] = p["pub_wholesale"] + p["pub_bm"] + p["pub_ancillary"]
        row["acc_margin"] = r.revenue - r.cost_of_sales            # 미실현 공정가치 변동 제외
        row["share"] = row["pub_total"] / row["acc_margin"]
        if r.entity == "DPSL":
            row["acc_wholesale"] = r.electricity_sales - r.cost_of_sales
            row["acc_bm"] = r.bm
            row["acc_ancillary"] = r.ancillary_other
            row["gap_wholesale"] = row["acc_wholesale"] - p["pub_wholesale"]   # 선도 판매·형상 최적화 몫(하한)
            row["gap_ancillary"] = row["acc_ancillary"] - p["pub_ancillary"]   # 공개되지 않는 부가서비스 계약
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    d = build()
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "accounts.csv", index=False)
    c = d[d["entity"] == "DPSL"]
    print("Cruachan (£m): 결산서 vs 공개 재구성")
    print(c[["year", "months", "acc_wholesale", "pub_wholesale", "acc_bm", "pub_bm", "acc_ancillary", "pub_ancillary",
             "gap_ancillary", "acc_margin", "pub_total", "share"]].round(2).to_string(index=False))
    f = d[d["entity"] == "FHC"]
    print("\nDinorwig + Ffestiniog (£m): 결산서 매출 − 매출원가 vs 공개 재구성")
    print(f[["year", "acc_margin", "pub_wholesale", "pub_bm", "pub_ancillary", "pub_total", "share"]].round(2)
          .to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
