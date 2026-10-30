# 물가·환율 (비용 입력을 2025년 실질 £로 바꾸는 데 씀, gbess.finance.costs)

받은 날 2026-10-30. 둘 다 공개 통계라 저장소에 그대로 둔다.

| 파일 | 무엇 | 출처 |
|---|---|---|
| ons_cpih_index_l522.csv | CPIH 지수(2015=100), 연·분기·월. 코드에서는 연평균 행만 씀 | ONS 시계열 L522 (MM23), https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/l522/mm23 (2026-10-21 발표분) |
| boe_fx_annual.csv | 연평균 환율: XUAAUSS(£1당 US$), XUAAERS(£1당 €), 2015~2025 | 영국은행 통계 데이터베이스, https://www.bankofengland.co.uk/boeapps/database/ (시리즈 코드 XUAAUSS, XUAAERS) |

Ofgem cap-and-floor는 CPIH 실질 기준이라(FACTS.md 2.1) CPIH를 쓴다.
