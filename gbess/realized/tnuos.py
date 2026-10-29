"""
양수발전소가 낸 TNUoS(송전망 이용 요금, 발전 쪽) 추정. 위치마다 크게 다른 비용이라, 발전소끼리 MW당 수익을 비교할 때 빼야 한다.

    .venv/bin/python -m gbess.realized.tnuos

TNUoS 발전 요금은 연간 £/kW(송전 접속 용량 TEC 기준)라 운전량에 비례하지 않는다. 그래서 엔진 운전은 바꾸지 않고
수익 순액과 위치 비교에만 들어간다(08 문서의 F형). 운전량에 붙는 BSUoS는 gbess.data.charges.
식 (CUSC 14.15, 2016 CMP268 이후 "conventional low carbon" 발전: 양수발전을 여기로 본다)
    wider £/kW = 계통 첨두(SystemPeak) + 연중 공유(SharedYearRound) × ALF + 연중 비공유(NotSharedYearRound) + 잔여(Residual)
    + 지역 회선(local circuit, 발전소별) 요금
  ALF(연간 부하율): 원래는 지난 5년 중 3년의 계량 출력 ÷ TEC. 여기서는 그해 지시 반영 발전량 ÷ (출력 × 8760)으로 대신한다.
  TEC: 엔진과 같은 순 출력(gbess.realized.psh.SITES)으로 둔다. 실제 TEC는 다를 수 있다.
요금표: NESO "Transmission Network Use of System (TNUoS) Tariffs" 데이터셋의 Final 값(Onshore_Generator_Tariffs,
  Onshore_Local_Circuit_Tariffs). Year_FY는 회계연도 끝 해다(2027 = 2026-04~2027-03). 달력연도 Y = FY(Y)×3/12 + FY(Y+1)×9/12.
  자료가 FY 2021부터라 2021~2026년만 계산한다. 원자료는 data/raw/neso/(다른 작업이 받은 파일, MANIFEST 있음)에서 읽는다.
확인되지 않은 것 (결과에 범위로 남긴다)
  - 발전 구역 배정: NESO 요금 보고서의 구역 지도를 아직 확인하지 못했다. 주 배정과 이웃 후보 구역을 함께 계산해 범위로 낸다.
  - 양수발전의 등급(conventional low carbon)과 첨두 요금 적용 여부.
"""
from pathlib import Path

import pandas as pd

from gbess.realized.psh import SITES

ROOT = Path(__file__).resolve().parents[2]
TARIFF = ROOT / "data" / "raw" / "neso" / "transmission-network-use-of-system-tnuos-tariffs"
OUT = ROOT / "results" / "realized"
ZONES = {  # 주 배정, 후보 (발전 구역 번호, 27구역 체계)
    "DINO": (19, [19, 16]),   # Anglesey and Snowdon / North Midlands and North Wales
    "FFES": (19, [19, 16]),
    "CRUA": (7, [7, 8]),      # Argyll / The Trossachs
    "FOYE": (3, [3, 1, 6]),   # Western Highlands / North Scotland / Central Grampian
}
LOCAL = {"DINO": "Dinorwig", "FFES": "Ffestiniog", "CRUA": "Cruachan", "FOYE": "Foyers"}
YEARS = range(2021, 2027)   # 2026은 9개월 자료, 요금은 연 전체 기준


def tariffs():
    g = pd.read_csv(TARIFF / "Onshore_Generator_Tariffs.csv", encoding="utf-8-sig")
    g = g[g["Publication"] == "Final"].set_index(["Year_FY", "Zone_No"])
    lc = pd.read_csv(TARIFF / "Onshore_Local_Circuit_Tariffs.csv", encoding="utf-8-sig")
    lc = lc[lc["Publication"] == "Final"].set_index(["Year_FY", "Substation_Name"])["Tariff_£/kW"]
    return g, lc


def per_kw(g, lc, fy, zone, site, alf):
    z = g.loc[(fy, zone)]
    wider = z["SystemPeak_£/kW"] + z["SharedYearRound_£/kW"] * alf + z["NotSharedYearRound_£/kW"] + z["Residual_£/kW"]
    local = float(lc.get((fy, LOCAL[site]), 0.0))
    return float(wider), local


def build():
    g, lc = tariffs()
    yr = pd.read_csv(OUT / "psh_annual.csv")
    rows = []
    for _, r in yr[yr["year"].isin(YEARS)].iterrows():
        site, y = r["site"], int(r["year"])
        mw = SITES[site]["mw"]
        alf = float(r["gen"]) / (mw * 8760 * r["months"] / 12)
        main, cands = ZONES[site]
        vals = {}
        for z in cands:
            w0, l0 = per_kw(g, lc, y, z, site, alf)
            w1, l1 = per_kw(g, lc, y + 1, z, site, alf)
            vals[z] = (0.25 * w0 + 0.75 * w1, 0.25 * l0 + 0.75 * l1)
        tot = {z: w + lo for z, (w, lo) in vals.items()}
        rows.append({"year": y, "site": site, "alf": alf, "zone": main, "wider_k": vals[main][0],
                     "local_k": vals[main][1], "tnuos_k": tot[main], "tnuos_k_min": min(tot.values()),
                     "tnuos_k_max": max(tot.values())})   # £/kW = £k/MW
    return pd.DataFrame(rows)


def main():
    d = build()
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "psh_tnuos_annual.csv", index=False)
    yr = pd.read_csv(OUT / "psh_annual.csv")
    m = d.merge(yr[["year", "site", "trading_mid_k_per_mw_yr", "bsuos_k_per_mw_yr"]], on=["year", "site"])
    m["net_k"] = m["trading_mid_k_per_mw_yr"] - m["bsuos_k_per_mw_yr"] - m["tnuos_k"]
    print(m[["year", "site", "alf", "trading_mid_k_per_mw_yr", "bsuos_k_per_mw_yr", "tnuos_k", "tnuos_k_min",
             "tnuos_k_max", "net_k"]].round(2).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
