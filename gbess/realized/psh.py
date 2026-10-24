"""
기존 양수발전소의 실제 수익을 공개 자료로 재구성한다 (실증층 검증 기준).

    .venv/bin/python -m gbess.realized.psh --start 2016-09 --end 2026-10

발전소·월별로 다음을 계산한다. 단위: 에너지 MWh, 돈 £.
- 도매: PN(사업자 계획 위치) × 가격. 실제 거래 가격은 모르므로 MID와 정산가격(SSP) 두 가지로 평가해 범위로 낸다 (07 문서 H1).
- BM: Elexon 정산 현금흐름(indicative cashflows). offer(출력 증가 지시)는 +, bid(출력 감소 지시)는 −로 이미 부호가 붙어 있다.
- 지시 반영 에너지: PN 위에 BOALF를 덮어쓴 출력 (gbess.realized.physical). 발전/양수 비율로 자료를 검증한다.
아직 넣지 않은 것: 불균형 정산(실측 출력 B1610 필요), 보조서비스 계약(응답·예비력), 용량시장, 망요금. 결과표에 열로 표시만 해 둔다.
Foyers는 자연 유입이 큰 수력 겸용이라 순수 저장장치 비교에서는 뺀다(is_pure_storage = False).
"""
import argparse
from pathlib import Path

import pandas as pd

from gbess.data.prices import load_mid, load_ssp
from gbess.realized.physical import sp_energy

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "elexon"
OUT = ROOT / "results" / "realized"

SITES = {  # 등록부 출력 합(MW), 지역, 순수 저장장치 여부
    "DINO": {"name": "Dinorwig", "mw": 1920, "region": "North Wales", "b6_north": False, "pure": True},
    "FFES": {"name": "Ffestiniog", "mw": 364, "region": "North Wales", "b6_north": False, "pure": True},
    "CRUA": {"name": "Cruachan", "mw": 453, "region": "Argyll, Scotland", "b6_north": True, "pure": True},
    "FOYE": {"name": "Foyers", "mw": 320, "region": "Highland, Scotland", "b6_north": True, "pure": False},
}


def month_panel(m):
    s = m.start_time.tz_localize("UTC")
    e = (m + 1).start_time.tz_localize("UTC")
    pn = pd.read_parquet(RAW / "pn_psh" / f"pn_psh_{m:%Y%m}.parquet")
    bo = pd.read_parquet(RAW / "boalf_psh" / f"boalf_psh_{m:%Y%m}.parquet")
    cf_path = RAW / "bm_cashflows" / f"bm_cashflows_{m:%Y%m}.parquet"
    if pn.empty or not cf_path.exists():
        return None
    cf = pd.read_parquet(cf_path)
    en = sp_energy(pn, bo, s, e)
    mid, rep = load_mid(s, e)
    ssp = load_ssp(s, e)
    en["p_mid"] = en["start_utc"].map(mid)
    en["p_ssp"] = en["start_utc"].map(ssp)
    en["site"] = en["bmUnit"].str[2:6]
    cf = cf[cf["bmUnit"].str.match(r"T_(DINO|FFES|CRUA|FOYE)-")].assign(site=lambda d: d["bmUnit"].str[2:6])
    rows = []
    for site, g in en.groupby("site"):
        c = cf[cf["site"] == site].groupby("side")["totalCashflow"].sum()
        boa = g["boa_mwh"]
        rows.append({
            "month": f"{m:%Y-%m}", "site": site,
            "pn_gen_mwh": g["pn_mwh"].clip(lower=0).sum(), "pn_pump_mwh": -g["pn_mwh"].clip(upper=0).sum(),
            "phys_gen_mwh": g["phys_mwh"].clip(lower=0).sum(), "phys_pump_mwh": -g["phys_mwh"].clip(upper=0).sum(),
            "boa_up_mwh": boa.clip(lower=0).sum(), "boa_down_mwh": -boa.clip(upper=0).sum(),
            "wholesale_mid_gbp": (g["pn_mwh"] * g["p_mid"]).sum(),
            "wholesale_ssp_gbp": (g["pn_mwh"] * g["p_ssp"]).sum(),
            "bm_offer_gbp": float(c.get("offer", 0.0)), "bm_bid_gbp": float(c.get("bid", 0.0)),
            "mid_filled_ssp_sp": rep["filled_ssp"], "pn_missing_min": int(g["pn_missing_min"].sum()),
        })
    return pd.DataFrame(rows)


def build(start, end):
    months = pd.period_range(start, pd.Period(end, freq="M") - 1, freq="M")
    parts = [month_panel(m) for m in months]
    df = pd.concat([p for p in parts if p is not None], ignore_index=True)
    df["bm_net_gbp"] = df["bm_offer_gbp"] + df["bm_bid_gbp"]
    df["trading_mid_gbp"] = df["wholesale_mid_gbp"] + df["bm_net_gbp"]
    df["trading_ssp_gbp"] = df["wholesale_ssp_gbp"] + df["bm_net_gbp"]
    df["mw"] = df["site"].map(lambda s: SITES[s]["mw"])
    df["pure_storage"] = df["site"].map(lambda s: SITES[s]["pure"])
    df["b6_north"] = df["site"].map(lambda s: SITES[s]["b6_north"])
    return df


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2016-09")
    ap.add_argument("--end", default="2026-10")
    a = ap.parse_args(argv)
    df = build(a.start, a.end)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "psh_monthly.csv", index=False)
    yr = df.assign(year=df["month"].str[:4]).groupby(["year", "site"]).agg(
        months=("month", "count"), mw=("mw", "first"), wholesale_mid=("wholesale_mid_gbp", "sum"),
        wholesale_ssp=("wholesale_ssp_gbp", "sum"), bm_net=("bm_net_gbp", "sum"),
        gen=("phys_gen_mwh", "sum"), pump=("phys_pump_mwh", "sum")).reset_index()
    ann = 12 / yr["months"]
    for k in ("wholesale_mid", "wholesale_ssp", "bm_net"):
        yr[f"{k}_k_per_mw_yr"] = yr[k] * ann / yr["mw"] / 1e3
    yr["trading_mid_k_per_mw_yr"] = yr["wholesale_mid_k_per_mw_yr"] + yr["bm_net_k_per_mw_yr"]
    yr["trading_ssp_k_per_mw_yr"] = yr["wholesale_ssp_k_per_mw_yr"] + yr["bm_net_k_per_mw_yr"]
    yr["gen_over_pump"] = yr["gen"] / yr["pump"]
    yr.to_csv(OUT / "psh_annual.csv", index=False)
    print(yr[["year", "site", "months", "wholesale_mid_k_per_mw_yr", "bm_net_k_per_mw_yr",
              "trading_mid_k_per_mw_yr", "trading_ssp_k_per_mw_yr", "gen_over_pump"]].round(2).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
