# 구역 선택 메모 (T3, M1-0): 3구역을 고른다

> 작성 2026-11-05. 지시서 [`../IMPLEMENTATION_A_KO.md`](../IMPLEMENTATION_A_KO.md) T3. 분석 코드: `gbess/system/zones_analysis.py` (시험 `tests/test_system_zones_analysis.py`), 결과 `results/system/zones/`.
> **결정 경위**: 지시서는 이 제안을 연구자가 승인하도록 했다. 연구자는 2026-11-05에 "확정해야 하는 값들은 근거가 확실하고 문제 없는 선에서 Claude가 추천하는 것으로 그대로 하라"고 위임했다. 그래서 아래 추천을 적용했고, spec.yaml `changelog`와 [`../12_decisions_2026-11_KO.md`](../12_decisions_2026-11_KO.md)에 기록했다.
> 출처 확인은 웹 조사 에이전트 세 개가 했다. 출처는 각 줄에 링크로 단다. NESO 웹사이트는 자동 접근을 막아서, 일부 문서는 Wayback Machine 사본으로 읽었다.

## 결론

- **3구역**, 북→남 사슬 구조: **N = B4 북쪽(SSEN 송전망)**, **S = B4~B6(SP 송전망)**, **EW = 잉글랜드·웨일스(NGET)**.
- 경계는 B4(N|S)와 B6(S|EW) 두 개다.
- 2030년 한도는 ETYS 2024의 2030 용량 × 관측 감산 계수로 정했다. **B4 3,940 MW, B6 5,740 MW**이고, 근거는 4장에 있다.
- 5구역(잉글랜드를 B7a·B8에서 나눔)은 M3의 견고성 축(D17 "구역 수")으로 미룬다.

## 1. 제약 그룹 ↔ ETYS 경계 대응

| NESO 그룹 | 경계 | 근거 | 확신 |
| --- | --- | --- | --- |
| SCOTEX | **B6** (스코틀랜드→잉글랜드) | NESO Year-Ahead Constraint Limits 열 이름 "B6 - SCOTEX". NESO Dispatch Transparency webinar(2025-08-07) p.13 "SCOTEX B6 Constraint – Anglo-Scottish Border" | 높음 |
| SSE_SP2 (2024-04 전 SSE_SP) | **B4** (SSEN→SPT) | 같은 페이지 "B4 - SSE-SP2". OTF 혼잡 자료의 "Min of B4 B5"와 값이 일치 | 높음 |
| SSEN_S | B2 | "B2 - SSEN-S" | 높음 |
| NKILGRMO, SSE_GRMO | B5 | "B5 - NKILGRMO", "B5 - SSE+GRM" | 중간~높음 |
| HARSPNBLY | B6a (잉글랜드 북동부, B6 바로 남쪽) | OTF 자료 "B6a"와 24개월 앞 한도가 26주 중 9주 일치. 문서로 명시된 곳은 찾지 못함 | 중간~높음 (숫자로만 확인) |
| SSHARN3 | **B7** | "B7 - SSHARN3" | 높음 |
| FLOWSTH | B9 (미들랜즈→남부) | OTF "B9"와 7주 일치 | 중간~높음 (숫자로만 확인) |
| SEIMPPR23 | LE1 (런던 유입) | "LE1 - SEIMPPR2" | 높음 |
| ESTEX | B15 (템스 하구) | "B15 - ESTEX" | 높음 |
| GM_SNOW5A, DRESHEX1, 2026-05-31의 켄트 그룹들 | ETYS 번호 없음 (북서부, 험버, 켄트의 국지 제약) | NESO 하루 전 자료의 망 지도 설명 | 낮음~중간 |

출처: [NESO Year-Ahead Constraint Limits (Wayback 2025-08-21)](https://web.archive.org/web/20250821052649/https://www.neso.energy/data-portal/year-ahead-constraint-limits/year_ahead_constraint_limits), [Dispatch Transparency webinar](https://web.archive.org/web/20251211032933/https://www.neso.energy/document/366426/download), [Day-Ahead Constraint Flows 망 지도 (잉글랜드·웨일스)](https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/bb6d6ec6-16d9-4be5-b32c-1a70c09fd871/download/ew-network-diagram-da-limit-boundaries-oct2026.pdf).

## 2. 어느 경계가 얼마나 자주, 얼마나 크게 묶이나 (2024-05-01 ~ 2026-10-24)

1시간 평균, 조류 ≥ 한도를 "제약"으로 셌다. 2024년은 5~12월, 2026년은 1월~10월 24일이다.

| 그룹 (경계) | 2024 | 2025 | 2026 | 2025 초과량 |
| --- | --- | --- | --- | --- |
| SSEN_S (B2) | 38.9% | 42.0% | 49.3% | 4.5 TWh |
| SSE_SP2 (B4) | 47.3% | 40.2% | 51.4% | 5.3 TWh |
| NKILGRMO (B5) | 40.5% | 40.1% | 54.9% | 5.2 TWh |
| SCOTEX (B6) | 32.3% | 32.5% | 40.3% | 5.6 TWh |
| HARSPNBLY (B6a) | 35.9% | 34.4% | 37.9% | 5.8 TWh |
| SSHARN3 (B7) | 36.4% | 28.4% | 43.2% | 5.3 TWh |
| FLOWSTH (B9) | 5.4% | 4.8% | 12.5% | 0.3 TWh |
| SEIMPPR23 (LE1) | 1.7% | 2.9% | 2.2% | 0.2 TWh |

- **B4 또는 B6** 제약: 2024년 48.8%, 2025년 44.3%, 2026년 54.8%. 둘 다 제약: 30.7%, 28.1%, 36.2%.
- **B6가 묶일 때 B4도 묶인 비율**: 2024년 96%, 2025년 86%, 2026년 90%. 지시서와 04 보고서는 2025년을 "90%"로 적었지만, 원자료로 다시 계산하면 86%다(30분 기준 86.3%).
- **두 경계 중 큰 쪽 초과량** (하나라도 값이 있는 시간): 2025년 7.36 TWh(1시간). 30분 기준으로는 7.42 TWh로 04 보고서와 같다.
- **스코틀랜드 안의 경계(B2·B4·B5)는 거의 함께 움직인다.** 하나가 묶이면 다른 것도 85~93% 함께 묶인다(2025년, 두 그룹씩 짝지어 계산). 그래서 북스코틀랜드를 더 나눠도 얻는 정보가 적다.
- **잉글랜드 북부(B6a·B7)는 B6만큼 자주 묶이지만, 대부분 B4·B6와 같은 시간이다.** 2025년에 잉글랜드 북부만 묶이고 B4·B6는 묶이지 않은 시간은 4.6%다. B6와 조류 상관은 0.90~0.93이다. 스코틀랜드에서 내려오는 같은 흐름이 이어서 걸리는 모양이다.
- **비용**: 열적 제약 비용 중 B4·B6의 몫은 FY24/25 79%, FY25/26 81%다. B7은 12~13%, B15(ESTEX)는 1~8%다. 이 값은 NESO Thermal Constraint Costs 그룹별 자료로 계산한 몫이다. 이 자료는 전체 열적 비용의 일부만 담고 있어서 몫으로만 쓴다. NESO 연간 균형 비용 보고서(2025-06) p.12도 "the cause of cost is concentrated in Scotland"라고 쓴다.

## 3. Window 1 잠정 16건과 기존 양수의 위치

| 사업 | 연결 변전소 (TEC 등록부 2026-11-03) | 구역 | 확신 |
| --- | --- | --- | --- |
| Coire Glas (양수 1,440 MW) | Coire Glas GSP → Fort Augustus, SHET | N (B4 북쪽) | 높음 |
| Earba (양수 1,800 MW) | Earba 발전소 → 새 Coire Mashie 400 kV (Beauly–Denny 선) | N | 높음 |
| Loch Kemp (양수 660 MW) | Loch Kemp 275 kV → Foyers | N | 높음 |
| Field Fyrish / Netherton / New Deer / Rigifa (리튬 4건) | Fyrish 132 kV / Longside 400 kV / New Deer 2 400 kV / Gills Bay 132 kV, 모두 SHET | N | 높음 |
| 잉글랜드 리튬 7건, TeesCAES, Frontier Legacy | NGET 지역 (East Claydon, Sundon, Navenby, Drakelow, Ocker Hill 등) | EW | 높음. 단 Thornton BESS 2, Frontier Legacy, TeesCAES는 변전소가 확인되지 않음. 지역(잉글랜드·웨일스)은 확실 |
| Cruachan (기존 양수 440 MW) | Cruachan 275 kV, SPT (Dalmally) | **S** (B4 남쪽, B6 북쪽) | 높음 |
| Foyers (기존 300 MW) | Foyers 275 kV, SHET | N | 높음 |
| Dinorwig, Ffestiniog | 웨일스 | EW | 높음 |

- **W1 북쪽 = N 구역의 7건, 5,100 MW.** 지시서와 spec의 "W1 북쪽"과 같다.
- 출처: [NESO TEC 등록부 2026-11-03](https://api.neso.energy/dataset/cbd45e54-e6e2-4a38-99f1-8de6fd96d7c1/resource/17becbab-e3e8-473f-b303-3806f43a6a10/download/tec-register-03-november-2026.csv), [SSEN Coire Glas 연결](https://www.ssen-transmission.co.uk/projects/project-map/coire-glas-connection-project), [SSEN Coire Mashie](https://www.ssen-transmission.co.uk/globalassets/projects/new-coire-mashie-400kv-substation-and-earba-psh-connection-downloads/new-corie-mashie-400kv-substation-project-overview-information-may-2025.pdf), [SSEN Loch Kemp 연결](https://www.ssen-transmission.co.uk/projects/project-map/loch-kemp-hydro-scheme-connection/).
- 경계의 어느 쪽인지는 NESO ETYS 경계 지도(2025-03 shapefile)로 기하학적으로 판정했다.
- **잉글랜드 내부 경계와의 관계**: 잉글랜드 W1 리튬은 B8~B9 사이(Springwell, Drakelow, Ocker Hill)나 B9 남쪽(East Claydon, Sundon)에 있고, Long Stratton은 동앵글리아(EC5 안쪽)에 있다. 북쪽 경계(B6a·B7)와는 관계가 없다.
- TEC와 Ofgem의 MW가 다른 사업이 있다(Coire Glas 1,296 대 1,440, Netherton 200 대 400 등). **모형은 Ofgem 값(`window1_projects.csv`)을 쓴다.**

## 4. 2030년 경계 한도

| 경계 | ETYS 2024 기준 용량 (지금) | ETYS 2024의 2030 용량 (HT) | 관측 한도 ÷ 기준 용량 (2024-05~2026-10 평균) | **M1 한도 2030** |
| --- | --- | --- | --- | --- |
| B4 | 4,000 MW ("limited to 4 GW … Tealing - Westfield", p.28) | 7,300 MW | 0.539 (중앙값 0.50, P10 0.40, P90 0.71) | **3,940 MW** |
| B6 | 6,700 MW ("limited to 6.7 GW … Harker-Moffat", p.30) | 10,200 MW | 0.563 (중앙값 0.52, P10 0.35, P90 0.84) | **5,740 MW** |

- 출처: [ETYS 2024 (Wayback)](https://web.archive.org/web/20250311115820/https://www.neso.energy/document/352001/download) p.28, p.30. 2030 값은 ETYS 2024 대화형 그래프(문서 351896 B4, 351906 B6)에서 읽었다. 이 용량은 "Beyond 2030" 최적 경로의 보강을 전제로 한다.
- 2030 용량에는 EGL1(Torness–Hawthorn Pit, 2030)과 EGL2(Peterhead–Drax, 2029) HVDC가 들어 있다(CP2030 Annex 2 Table 2 p.9). 사슬 모형에서 HVDC는 경계 용량 안에 있는 것으로 본다(ETYS의 경계 용량 정의와 같음).
- **감산 계수를 쓴 이유**: 실제 운전 한도는 정비·보강 공사 때문에 회선이 정지되고, 안정도·전압 제약도 걸려서 ETYS 기준 용량보다 훨씬 낮다. 2025년 B6 관측 중앙값 3,800 MW는 기준 용량의 약 57%다(04 보고서 6장 3번과 같음). 2030년에도 Beyond 2030 보강 공사가 이어지므로, 지금의 비율을 그대로 쓴다.
- **후보와 영향**

  | 후보 | B4 / B6 | 왜곡 D에 주는 영향 |
  | --- | --- | --- |
  | (a) 감산 없음 (ETYS 명목 2030) | 7,300 / 10,200 | 제약이 적어 D가 가장 작음 |
  | **(b) 관측 평균 비율 (채택)** | 3,940 / 5,740 | 중간 |
  | (c) 관측 중앙값 비율 | 3,650 / 5,320 | D가 더 큼 |

- spec의 민감도 ×0.8·×1.2는 (b)에 곱한다: B6 4,590~6,890 MW. (a)는 이 범위 밖이라, **보고만 하는 추가 민감도**로 따로 돌린다(판정에는 쓰지 않음).
- 이것이 결과를 가장 크게 좌우하는 선택이다. 결과 해석에서 늘 함께 밝힌다.

## 5. 2030년 잉글랜드 내부 경계가 묶일 가능성

- ETYS 2024: B7a는 "expected power flows are already beyond the present boundary capability"(p.33). B8·B9도 2030년 이후 예상 조류가 용량을 넘는다(p.34, p.37).
- CP2030 Annex 2 p.8: Norwich–Tilbury가 2031년으로 늦어지면 2030년 제약 비용이 +£2.8bn 늘어난다(동앵글리아 EC5, 주로 해상풍력·인터커넥터 때문).
- 그러나 지금 비용은 스코틀랜드(B4·B6)가 약 80%이고, 잉글랜드 북부 제약은 대부분 B6와 같은 시간에 걸린다(2장). 또 W1 북쪽 장주기가 영향을 주는 경계는 B4·B6다.

## 6. 자료 확보 가능성

- **3구역은 공개 자료에서 바로 나온다.** FES 2025 Building Blocks(GSP 단위, NESO Open Data Licence)의 배전 사업자 구역과 송전 직접 연결 행(Direct(SHETL)/Direct(SPTL)/Direct(NGET))이 그대로 N/S/EW가 된다(B4 = SHETL|SPTL, B6 = SPTL|NGET).
- **5구역은 잉글랜드의 송전 연결 설비를 우리가 직접 나눠야 한다.** 해상풍력 약 35 GW, CCGT 20 GW, 송전 연결 태양광 10.7 GW 등이고, FES는 이 설비를 "Direct(NGET)" 한 덩어리로만 준다. TEC 등록부로 나눌 수는 있지만 그 값은 "derived"가 된다. 또 B7a·B8의 2030 용량은 그래프를 눈으로 읽은 근사값뿐이다.

## 7. 계산량과 검증 부담

- 3구역 1년(8,760시간) 가상 구역망 시험 풀이 시간: 1단계 12초, 계획자 최적 10초, 재급전 16~24초, **D_lo 결합 LP 10.6분**. 5구역이면 변수가 늘어 결합 LP가 더 오래 걸린다.
- 검증 V1은 B4·B6만 맞추면 된다. 5구역이면 B6a·B7도 맞춰야 하는데, 이 둘은 그룹 대응의 확신이 낮다.

## 8. 3구역 대 5구역 비교

| 기준 | 3구역 | 5구역 |
| --- | --- | --- |
| A안 메커니즘(B4·B6, W1 북쪽) | 담음 | 담음 |
| 잉글랜드 북부 제약 | 빠짐. 대부분 B6와 같은 시간이라 영향이 작을 것 | 담음 |
| 입력 status | 대부분 sourced | 잉글랜드 송전 설비 배분이 derived |
| 2030 한도 | ETYS 수치 | B7a·B8은 그래프 근사 |
| 계산 | 결합 LP 약 10분 | 더 오래 걸림 |
| 검증 | B4·B6 (대응 확신 높음) | + B6a·B7 (확신 중간) |

**추천: 3구역.** 5구역은 M3의 구역 수 견고성 축으로 둔다.
