"""
인터커넥터 가격 수용 민감도 (spec model.interconnectors: "가격 수용 판은 M2 민감도"). 연구자 결정 2026-11-06: 선택지 A.
주 결과는 인터커넥터를 뺀다. 이 판은 2030년 링크를 해외 시간별 가격에 사고파는 발전원 하나로 넣는다(수입 +, 수출 −,
비용 = 해외 가격 × 출력). 1단계·재급전·계획자 모두에서 다른 발전원처럼 조정할 수 있다(그래야 C(S0, ii) = C(S6) 검산이 성립).

    .venv/bin/python -m gbess.system.interconnectors extract <Ember 시간별 zip>   # data/raw/system/ember_prices_2020_hourly.csv
    .venv/bin/python -m gbess.system.run_m1 --weather-year 2020 --interconnectors price_taking --designs S0 --label sens_ic_w2020_x1.0_S0

- 해외 가격: Ember "European wholesale electricity price data" 시간별 하루 전 가격(EUR/MWh, ENTSO-E·EMR·SEMOpx), CC-BY-4.0.
  기상연도와 같은 해(2020)만 쓴다. Ember 시간별 자료는 2015년부터라 기상연도 2013 판은 만들 수 없다.
  노르웨이·덴마크는 Ember의 나라 평균값(연결 지점 NO2·DK1과 다를 수 있음).
- 2030년 수준으로 올리기(연료비 지수, placeholder): 해외 가격 × k, k = 2030 CCGT 연료+탄소 비용(£) ÷ 2020 CCGT 연료+탄소 비용(€).
  같은 효율(0.53)·배출계수(0.203 t/MWh LHV)를 쓴다(fleet_2030.yaml). 모든 시간·나라에 같은 k라 가스가 가격을 정하지 않는
  나라·시간(노르웨이 수력, 프랑스 원자력)도 같은 비율로 오른다는 단순화다.
- 2030년 링크 용량: FES 2025 BB Gen_BB022 HT 2030 = 11,700 MW (NGET 11,200 + SPTL 500). 2025년 운전 링크 9,800 MW(NGET)
  + Moyle 500(SPTL)에, 2030년 증가분 1,400 MW를 NeuConnect(독일, 1.4 GW, 건설 중)로 둔다(BB에는 사업 이름이 없어 추정, derived).
- 시간: 2020년 UTC 첫 8,760시간(윤년 12월 31일 뺌, 수요·이용률과 같음).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "system"
PRICES = RAW / "ember_prices_{year}_hourly.csv"
COUNTRIES = {"FR": "France", "BE": "Belgium", "NL": "Netherlands", "NO": "Norway", "DK": "Denmark", "IE": "Ireland",
             "DE": "Germany", "GB": "United Kingdom"}           # GB는 참고용(모형에 쓰지 않음)

# (이름, 나라, 구역, MW). 정격은 각 사업 공개 정격(NESO·Ofgem 인터커넥터 목록). 합 = FES BB Gen_BB022 HT 2030 11,700 MW
LINKS_2030 = [("IFA", "FR", "EW", 2000), ("IFA2", "FR", "EW", 1000), ("ElecLink", "FR", "EW", 1000),
              ("BritNed", "NL", "EW", 1000), ("Nemo", "BE", "EW", 1000), ("NSL", "NO", "EW", 1400),
              ("Viking", "DK", "EW", 1400), ("EastWest", "IE", "EW", 500), ("Greenlink", "IE", "EW", 500),
              ("NeuConnect", "DE", "EW", 1400), ("Moyle", "IE", "S", 500)]

# 연료비 지수 (k)
EFF_CCGT, EF_GAS = 0.53, 0.203                  # fleet_2030.yaml ccgt efficiency, ef_gas_t_mwh (LHV)
GAS_2030_GBP, CARBON_2030_GBP = 26.02, 92.15    # FES 2025 Economics CP.01 행 19·57, 2030 (2025년 실질 £)
GAS_2020_USD_MMBTU = 3.178229816083333          # IMF "Global price of Natural gas, EU" 2020 연평균 (FRED PNGASEUUSDA)
USD_PER_EUR_2020 = 1.1410                       # Federal Reserve 2020 연평균 (FRED AEXUSEU)
MWH_PER_MMBTU = 0.293071
NCV_GCV = 0.90                                  # 가스 진발열량/총발열량 (fleet_2030.yaml ccgt 효율 교차 확인과 같은 값)
CARBON_2020_EUR = 24.61                         # UBA "Jahresbericht zu deutschen Versteigerungen im EU-Emissionshandel"
                                                # (2021-03-30): 2020 독일 경매 "Durchschnittserlös pro Berechtigung 24,61 Euro" (EUA+EUAA)


def srmc(gas_per_mwh_lhv, carbon_per_t, eff=EFF_CCGT, ef=EF_GAS):
    """CCGT 연료 + 탄소 비용 (전기 1 MWh당). 가변 운영비는 넣지 않음."""
    return gas_per_mwh_lhv / eff + carbon_per_t * ef / eff


def gas_2020_eur_mwh_lhv():
    return GAS_2020_USD_MMBTU / USD_PER_EUR_2020 / MWH_PER_MMBTU / NCV_GCV


def price_index():
    """k (£2025 per €2020): 해외 가격 €/MWh × k = 2030년 £/MWh."""
    return srmc(GAS_2030_GBP, CARBON_2030_GBP) / srmc(gas_2020_eur_mwh_lhv(), CARBON_2020_EUR)


def extract_ember(zip_path, year=2020, out=None):
    """Ember 시간별 zip에서 그해 나라별 가격(EUR/MWh, UTC)만 뽑아 한 파일로."""
    import zipfile
    cols = {}
    with zipfile.ZipFile(zip_path) as z:
        for code, name in COUNTRIES.items():
            d = pd.read_csv(z.open(f"{name}.csv"))
            t = pd.to_datetime(d["Datetime (UTC)"])
            s = pd.Series(d["Price (EUR/MWhe)"].to_numpy(float), index=t)
            cols[code] = s[s.index.year == year]
    df = pd.DataFrame(cols)
    df.index.name = "utc"
    out = Path(out or str(PRICES).format(year=year))
    df.to_csv(out)
    return out, df


def foreign_prices_gbp(year, T=8760, path=None):
    """{나라: 길이 T £/MWh(2030년 수준)}."""
    df = pd.read_csv(path or str(PRICES).format(year=year), index_col=0, parse_dates=True)
    if df.isna().any().any() or len(df) < T:
        raise ValueError(f"해외 가격 결측 또는 시간 부족: {len(df)}")
    k = price_index()
    return {c: df[c].to_numpy(float)[:T] * k for c in df.columns}


def link_gens(zones, prices, links=LINKS_2030):
    """링크마다 Gen 하나: 용량 ±MW, 비용 = 그 나라 시간별 가격."""
    from gbess.system.network import Gen
    return [Gen(f"ic_{name}", zones.index(zone), float(mw), prices[c], None, False, -float(mw))
            for name, c, zone, mw in links]


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "extract":
        p, df = extract_ember(sys.argv[2])
        print(p, df.shape, df.mean().round(2).to_dict())
    print("k =", round(price_index(), 4), "gas 2020 €/MWh LHV =", round(gas_2020_eur_mwh_lhv(), 3))
