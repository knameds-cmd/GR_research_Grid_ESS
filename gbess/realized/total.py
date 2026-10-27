"""
양수발전 총수익(공개 자료로 잡히는 부분) = 거래(도매 PN + BM) + 용량시장 + FFR + 확정 Fast Reserve + STOR(상한) + 무효전력.

    .venv/bin/python -m gbess.realized.total

먼저 gbess.realized.psh와 gbess.realized.ancillary를 돌려 둔다.
빠진 것: 의무 주파수 응답(MFR), 옵션 Fast Reserve(2020~), 스핀 대기, 블랙스타트 등 양자계약, Fast Reserve 지명 요금(fr_pos_upper, 합계 밖), 불균형 정산, 망요금(TNUoS·BSUoS) 같은 비용.
결과: results/realized/psh_total_annual.csv (£k/MW/yr, 거래 수익은 MID와 정산가격 두 가지)
"""
from pathlib import Path

import pandas as pd

from gbess.realized.psh import SITES

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "realized"


def build():
    t = pd.read_csv(OUT / "psh_monthly.csv")
    a = pd.read_csv(OUT / "psh_ancillary_monthly.csv")
    df = t.merge(a, on=["month", "site"], how="left").fillna({c: 0.0 for c in a.columns if c.endswith("_gbp")
                                                              or c.endswith("_upper")})
    df["year"] = df["month"].str[:4]
    g = df.groupby(["year", "site"]).agg(
        months=("month", "count"), trading_mid=("trading_mid_gbp", "sum"), trading_ssp=("trading_ssp_gbp", "sum"),
        cm=("cm_gbp", "sum"), ffr=("ffr_gbp", "sum"), fr=("fr_gbp", "sum"), fr_pos_upper=("fr_pos_gbp_upper", "sum"),
        stor_upper=("stor_gbp_upper", "sum"), orps=("orps_gbp", "sum"))
    g = g.reset_index()
    g["mw"] = g["site"].map(lambda s: SITES[s]["mw"])
    scale = 12 / g["months"] / g["mw"] / 1e3
    for c in ("trading_mid", "trading_ssp", "cm", "ffr", "fr", "fr_pos_upper", "stor_upper", "orps"):
        g[c + "_k"] = g[c] * scale
    other = g["cm_k"] + g["ffr_k"] + g["fr_k"] + g["stor_upper_k"] + g["orps_k"]
    g["total_mid_k"] = g["trading_mid_k"] + other
    g["total_ssp_k"] = g["trading_ssp_k"] + other
    g["total_mid_gbp_m"] = (g["trading_mid"] + g["cm"] + g["ffr"] + g["fr"] + g["stor_upper"] + g["orps"]) / 1e6
    return g


def main():
    g = build()
    g.to_csv(OUT / "psh_total_annual.csv", index=False)
    cols = ["year", "site", "months", "trading_mid_k", "cm_k", "orps_k", "ffr_k", "fr_k", "stor_upper_k", "total_mid_k",
            "total_ssp_k", "total_mid_gbp_m"]
    print(g[cols].round(1).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
