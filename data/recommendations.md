# 추가로 필요한 데이터와 참고할 데이터 (2026-10-06)

아래 NESO 데이터셋은 NESO 포털 API(`package_search`)로, Elexon 엔드포인트는 실제 호출로 2026-10-06에 존재를 확인했습니다. 따로 적지 않은 것은 무료입니다.

- NESO 포털: https://www.neso.energy/data-portal/<데이터셋 이름> (API: `https://api.neso.energy/api/3/action/package_show?id=<이름>`)
- Elexon: `https://data.elexon.co.uk/bmrs/api/v1<경로>`

## 1. 지금 꼭 필요한 것 (현재 데이터의 빈 곳)

| 데이터 | 어디서 | 왜 필요한가 |
|---|---|---|
| 배터리 유닛별 EAC 결과 | `python3 gb_data_fetch.py --units` | 실제 배터리 230개가 서비스를 어떻게 나눠 쓰는지 볼 수 있음. 제도 변화 전후 비교의 핵심 |
| EAC 이전 DC/DM/DR 결과 (2020.9–2023.10) | NESO `dynamic-containment-data` | 2022년 호황과 2023년 붕괴 구간이 지금 데이터에 없음 |
| 2025년 10월 이전 BR 결과 | NESO `eac-br-auction-results` | BR 출시(2024.3)부터의 가격 |
| MID 가격·정산가격 장기 시계열 | Elexon `/datasets/MID/stream`, `/balancing/settlement/system-prices/{date}` | 지금은 2026년 9월 한 달뿐이라 최적화 모델을 1년 이상 돌릴 수 없음 |
| BM 유닛별 입찰가 (BOD) | Elexon `/datasets/BOD/stream?bmUnit=` | 배터리가 BM에 어떤 가격으로 입찰했는지. 실제 행동을 최적 입찰과 비교할 수 있음 |
| BM 유닛별 발령 물량 | Elexon `/balancing/settlement/acceptance/volumes/all/{bid\|offer}/{date}/{period}?bmUnit=` | BOALF의 출력 수준을 가공할 필요 없이 확정 물량을 바로 줌 |
| Skip rate (발령에서 배터리를 건너뛴 비율) | NESO `skip-rates` (2024.12~) | BM 수익의 "발령 확률"을 데이터로 보정 |
| 계통 주파수 1초 | NESO `system-frequency-data` | DC/DM/DR 제공 시 SoC 변화, 규칙 준수 시뮬레이션 |

## 2. 모델 품질을 높이는 것

| 데이터 | 어디서 | 쓰임 |
|---|---|---|
| 수요·풍력 예측 | NESO `1-day-ahead-demand-forecast`, `day-ahead-wind-forecast`, `embedded-wind-and-solar-forecasts` / Elexon `/datasets/NDF` | 롤링 호라이즌 모델에서 가격 예측의 입력. 그 시점에 실제로 알 수 있던 정보만 쓰게 됨 |
| 연료별 발전량 (30분) | Elexon `/datasets/FUELHH` | 가격 설명 변수, 재생에너지 비중과 스프레드의 관계 |
| 보조서비스 소요량과 전망 | NESO `dynamic-regulation-requirements`, `dynamic-moderation-requirements`, `long-term-forecasts-for-dc-dm-dr-requirements`, `balancing-reserve-auction-requirement-forecast`, `quick-reserve-auction-requirement-forecast` | 물량 한도(예: DRL 480 MW)라는 규칙 자체를 시계열로 확보. 규칙 스위치의 근거 |
| 정산가격 조정 내역 | Elexon `/datasets/DISBSAD`, `/datasets/NETBSAD` | 정산가격이 어떻게 결정됐는지 분해 |
| 최소 수입량 (MIL) | Elexon `/datasets/MILS/stream` (이미 받은 MELS와 짝) | 충방전 출력 한계, 2024년 30분 규칙의 효과 |
| 비BM 유닛의 OBP 데이터 | NESO `obp-non-bm-physical-notifications`, `obp-non-bm-reserve-instructions`, `obp-reserve-availability-utilisation-price` | BM에 등록되지 않은 배터리 약 46개의 운영 |
| 송전요금·BSUoS | NESO `transmission-network-use-of-system-tnuos-tariffs`, `bsuos-fixed-tariffs`, `daily-balancing-costs-balancing-services-use-of-system` | 비용 항목. 계통요금 규칙이 수익에 미치는 효과 |
| 계통 관성 | NESO `system-inertia` | 주파수 서비스 수요가 왜 바뀌는지 설명하는 변수 |
| 과거 FFR/EFR 낙찰 | NESO `firm-frequency-response-post-tender-reports` | 2016–2021 EFR/FFR 시절까지 계보를 잇기 위해 |

## 3. 비용·열화 (데이터 포털이 아닌 공개 자료)

- **NREL Annual Technology Baseline (ATB)**: 배터리 CAPEX·O&M의 연도별 전망. 아카이브의 Schmidt 2019 LCOS(`literature/papers/schmidt2019_lcos.md`)와 함께 비용 가정의 근거로.
- **Battery Archive (batteryarchive.org)**: 셀 열화 실험 데이터. 열화 모델 파라미터를 직접 맞출 때.
- **Lazard LCOS 보고서**: 업계 기준치 비교용. 학술 근거로는 보조적.

## 4. 비교와 확장용

- **ENTSO-E Transparency**: 벨기에·북유럽 하루 전 가격과 보조서비스. 영국은 2021년부터 빠져 있음. 같은 모델에 다른 시장 규칙을 넣어 비교할 때.
- **Fingrid Open Data**: FCR-N/FCR-D/FFR 가격·입찰. 무료 API 키 필요.
- **AEMO NEMWEB**: 호주 5분 FCAS 가격. 선행연구가 가장 많은 시장이라 벤치마크로 좋음.
- **Elexon `/datasets/BOALF` (유닛 미지정)**: 전 유닛 발령을 한 번에(2시간에 3,273건). 배터리와 가스 발전기의 발령 비교.

## 5. 유료라서 대체가 필요한 것

- **실제 하루 전 경매가 (N2EX/EPEX)**: Nord Pool에 학생·학술용 조건이 있다고 함. 그 전까지는 MID로 대체.
- **가스·탄소 가격 (NBP, UK ETS)**: 가격의 근본 동인이지만 원자료는 대부분 유료. 무료 대체 출처는 아직 확인하지 못함.
- **Modo Energy 지수·데이터북**: 업계 수익 벤치마크. 무료 계정으로는 월별 요약 기사만.

## 6. 확인 결과 공지와 다른 점

- Grid Code GC0166(2026년 7월 도입)의 새 BM 파라미터(최대 인도량·기간, Elexon `MDV`/`MDP`)는 아직 빈 값으로 나옴. 배터리 MWh를 이걸로 바로 얻기는 어려움.
- Elexon `FPN` 엔드포인트는 404. 이미 받은 PN이 같은 역할.

## 우선순위

1번 표의 앞 네 줄(유닛별 EAC, EAC 이전 DC, 이전 BR, 가격 장기 시계열)부터 받으면 됩니다.
