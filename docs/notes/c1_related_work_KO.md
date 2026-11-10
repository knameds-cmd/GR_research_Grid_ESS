# C1: A안과 같은 질문을 다룬 연구가 있나 (2026-11-08)

> `review_2026-11-04/03_진행_방법_KO.md` 1.2절의 C1 확인입니다. 연구자 지시(2026-11-08): **"같은 연구가 있어도 원래 계획대로 간다. 찾는 정도만."** 그래서 이 메모는 연구 계획을 바꾸자는 제안이 아니라, 논문에서 인용하고 차이를 밝혀야 할 자료의 목록입니다.
> 찾은 방법: 웹 검색(학술·업계·정부 문서), PDF는 받아서 글자를 뽑아 직접 읽었습니다. 쪽 번호는 PDF 쪽입니다. 직접 읽지 못하고 검색 요약만 본 것은 **(요약만)**으로 표시했습니다.

---

## 1. 한 줄 결론

- **"B6 북쪽 장주기 저장장치가 전국 가격에 맞춰 운전하면 재급전 비용이 늘어난다"는 현상 자체는 이미 정부 연구에 나와 있습니다.** DESNZ가 맡긴 LCP Delta·Regen 보고서(2024-01)가 같은 2단계 구조(전국 시장 → 구역 재급전)로 이 방향과 메커니즘을 보였습니다.
- **그러나 A안의 핵심 세 가지를 한 연구는 찾지 못했습니다.**
  1. **왜곡의 크기**: 같은 자산을 전국 가격대로 돌릴 때와 계통에 가장 좋게 돌릴 때의 차이(D). 기존 연구는 "장주기가 있을 때와 없을 때"의 차이만 봅니다.
  2. **설계 보완 비교**: 입출력 한도(S1a·S1b), 제약 시간 운전 의무(S3), 지역 가격(S5).
  3. **실제 Window 1 사업과 cap-and-floor의 결합**: 실제 선정 사업 위치, floor 아래 운전 유인, 15개 기상연도.
- 정부·Ofgem의 공식 평가는 오히려 "제약 지역에 있는 장주기는 제약 비용을 줄일 수 있다"는 쪽으로 서술합니다. 늘릴 수 있다는 위험은 숫자로 다루지 않았습니다.
- 실제 운전 자료에서는 북쪽 저장장치가 제약을 키우는 증거가 나와 있습니다(FTI 2024, NESO 2026). A안의 동기를 뒷받침하는 자료로 쓸 수 있습니다.

---

## 2. 가장 가까운 연구: DESNZ·LCP Delta (2024-01)

**Scenario Deployment Analysis for Long-Duration Electricity Storage**. DESNZ Research Paper 2023/047. LCP Delta와 Regen 작성. [원문](https://assets.publishing.service.gov.uk/media/659be546c23a1000128d0c51/long-duration-electricity-storage-scenario-deployment-analysis.pdf). status: sourced.

| 항목 | 내용 | 쪽 |
| --- | --- | --- |
| 모형 | LCP Locational Dispatch Model. 경계 제약 없이 전국 단일가격으로 운전을 정한 뒤, 경계 제약을 넣어 재급전(BM)합니다. 둘의 차이가 "locational balancing" 비용입니다 | p104 |
| 구역 | 5구역: 북스코틀랜드, 남스코틀랜드, 북잉글랜드·웨일스, 남잉글랜드·웨일스, 동잉글랜드. 경계는 B2, B6, B8, EC5/SCD1 | p105 |
| 장주기 운전 | 4일 앞을 6시간 단위로 보는 "사전 최적화"로 하루 끝 충전량을 정하고, 하루 안에서는 시간 단위로 운전합니다. 시장 이익 운전입니다 | p104~105 |
| 비교 대상 | 장주기 10 GW를 **넣었을 때와 안 넣었을 때**의 locational balancing 비용. NPV 2030~2050, £(real 2022) | p108~109 |
| 결과 (유형별) | 양수형 Medium(90%가 스코틀랜드) +£0.5bn(+6%), 양수형 Long +£0.6bn(+7%). 스코틀랜드에 없는 압축공기형은 −£0.7bn | p109 |
| 결과 (위치별) | 10 GW 모두 잉글랜드: 최대 −£1.7bn. 모두 스코틀랜드: 최대 +£0.7bn | p9, p111 |
| 메커니즘 | 전국 가격이 높은 때(잉글랜드 수요가 큼)와 스코틀랜드 재생에너지 수출이 많아 B2·B6가 막히는 때가 겹칩니다. 그때 스코틀랜드 장주기가 방전해 다시 내려야 하고, 잉글랜드에서 올려야 합니다. 2035년 Even Mix에서 상향 조정량 19 TWh(스코틀랜드) vs 17 TWh(잉글랜드) | p9, p111 |
| 해석 | "그렇다고 스코틀랜드 장주기를 막아야 한다는 뜻은 아니다. 다른 계통 이익(10 GW에서 최대 £14bn)이 훨씬 크다" | p9 |

**A안과의 차이**
- **비교 기준이 다릅니다.** LCP는 "장주기가 있을 때 − 없을 때"입니다. A안의 D는 "같은 장주기를 시장대로 돌릴 때 − 계획자 최적으로 돌릴 때"입니다. 그래서 A안은 같은 자산의 운전 방식에서 생기는 낭비만 따로 잽니다.
- **설계 보완을 시험하지 않습니다.** 운전 의무, 입출력 한도, 위치 신호의 효과가 없습니다.
- 가상 10 GW 배치(유형별 위치 가정)입니다. 실제 Window 1 16건이 아니고, cap-and-floor도 없습니다.
- 몇 개 기상연도를 썼는지는 이 장에서 확인하지 못했습니다.

**논문에서 쓸 법**: "LCP Delta(2024)는 북쪽 장주기의 존재가 재급전 비용을 키울 수 있음을 보였다. 이 연구는 (i) 그 원인을 운전 방식의 왜곡으로 분리해 재고, (ii) 그것을 줄이는 설계안을 비교하며, (iii) 실제 Window 1 사업과 cap-and-floor 아래 운전 유인을 반영한다."

---

## 3. 공식 평가 문서 (NESO·Ofgem)

### 3.1 NESO, Window 1 평가 방법 (2025-09)

**LDES Window 1: Assessment Methodology for System and Welfare Impacts**. [원문](https://www.ofgem.gov.uk/sites/default/files/2025-09/LDES%20Window%201%20Assessment%20Methodology%20for%20System%20and%20Welfare%20Impacts%20(NESO).pdf). status: sourced.

- PLEXOS로 두 단계를 차례로 풉니다. 먼저 제약 없는 도매시장(전국 가격)을 풀고, 그 결과에 경계 제약을 넣어 재급전 비용 최소로 다시 풉니다(p13, 3.5절). **A안과 같은 2단계 구조입니다.**
- 사업마다 "넣었을 때 − 뺐을 때"(Marginal Addition)로 BM 비용 변화를 소비자 후생에 넣습니다(p17, p46).
- 기본은 2013 기상연도이고, 1985·2010을 민감도로 둡니다(p28). 전국 가격이 기본이고, 지역 가격 민감도는 뺐습니다(p9~10, p13).
- **(요약만)** Ofgem의 minded-to 문서에 따르면, NESO의 BM 모형에 "남은 최적화 퇴화(residual optimisation degeneracy)" 문제가 있었습니다. 그래서 사업 순위를 매길 때 BM 결과를 쓰지 않았고, Ofgem도 "위치 효과가 순위에 다 반영되지 않았을 수 있다"고 인정했습니다. [minded-to 답변 부록](https://consult.ofgem.gov.uk/energy-generation/ldes-window-1-minded-to-decision/supporting_documents/appendix-responses-to-questions-from-respondents-260731pdf). 원문 쪽 번호는 아직 확인하지 않았습니다.

**A안과의 차이**: 사업 선정용이라 "있음 − 없음"만 봅니다. 왜곡(시장 운전 − 최적 운전)과 설계 보완은 보지 않습니다. 사업별 BM 결과도 공개되지 않았습니다(위 요약이 맞다면 순위에서도 빠졌습니다). → **A안이 이 빈칸을 채웁니다.**

### 3.2 Ofgem, 포트폴리오 영향 평가 (2026-06)

**Assessment of impacts of the proposed LDES portfolio** (Window 1 minded-to). [원문](https://consult.ofgem.gov.uk/energy-generation/ldes-window-1-minded-to-decision/supporting_documents/assessment-of-ldes-impactspdf). status: sourced.

- 선정 사업 표에 북스코틀랜드 사업 7건이 있습니다(Loch Kemp, Coire Glas, Earba, Field 4건)(p10 표 1).
- 제약 효과는 숫자 없이 "제약 지역에 있으면 제약 비용을 줄일 수 있다"고만 씁니다(p20 5.6, p22 5.17).
- 운전 조건이나 면허 조건이 장주기 사용을 지나치게 제한하면 투자가 약해진다고 적었습니다(p19~20). S1·S3 같은 운전 제한형 설계를 논할 때 함께 인용할 문장입니다.

### 3.3 NESO, DESNZ 요청에 대한 답변 (2024 말 추정, Window 1 기술 결정 전)

**Long Duration Electricity Storage: Response to DESNZ Request Q1 and Q2**. [원문](https://www.neso.energy/document/356906/download). status: sourced. 날짜는 본문에 "TDD가 2025-03 발표 예정"이라고 적혀 있어 2024년 말로 봤습니다(derived).

- 500 MW 장주기를 북스코틀랜드(Zone 8)와 콘월·데번(Zone F)에 각각 넣고 길이를 2~24시간으로 바꿨습니다. **두 곳 모두** 재급전 비용(NPV 2030~2050)이 줄었고, 20시간이 넘으면 더 줄지 않았습니다(p17~18). BM 참여를 가정했습니다(p26).
- B6 위에서 **제약만 돕도록 운전하는** 저장장치의 이용률: 2030년 6시간 26%, 8시간 30%, 20시간 43%. 2035년 14%, 16%, 28%(p18~19).
- 2035년 B6 제약은 횟수는 줄지만 길어집니다. 1/3은 하루 넘게 이어집니다(p18).
- "잘못 배치하면 제약을 악화시킬 수 있다"는 문장이 있지만 숫자는 없습니다(p27).

**A안과의 차이**: 북쪽 장주기가 계통을 돕는 쪽으로 운전한다고 가정합니다. A안의 질문(전국 가격대로 운전하면?)과 정반대의 가정이라, 대조용으로 인용할 수 있습니다.

---

## 4. 실제 운전 증거 (A안의 동기)

### 4.1 FTI Consulting (2024-12): 배터리의 "flip-flopping"

**The Curious Case of Batteries Flip-Flopping: How the Current GB Wholesale Market Design Fails to Make Best Use of Flexible Assets**. [원문](https://www.fticonsulting.com/-/media/files/insights/reports/2024/dec/how-current-gb-wholesale-market-design-fails-make-best-use-flexible.pdf). status: sourced.

- 자료: 2024-04~09, Elexon BM 지시를 분 단위로. 북스코틀랜드 배터리 4기 107 MW, 런던·남동부 6기 256 MW(p6).
- 북쪽 배터리의 BM 지시 중 NESO가 제약 해소용으로 표시한(flagged) 것이 57.5%(bid는 70.4%). 남쪽은 3.2%(p6 표 1).
- 그런 지시의 59%는 **배터리가 도매시장에서 정한 자기 운전을 되돌리는 것**이었습니다(p1).
- 처방은 지역(zonal) 도매가격입니다. 그대로 두면 운전을 제한하는 규제가 생길 수 있다고 경고합니다(p1).
- 단주기 배터리 자료지만 메커니즘은 A안과 같습니다.

### 4.2 NESO, 개혁된 전국 가격: 균형·정산·급전 의견 요청 (2026-02)

**Reformed National Pricing: Balancing, Settlement and Dispatch, Call for Input**. [원문](https://www.neso.energy/document/376966/download). status: sourced.

- 전국 단일가격은 유연 자원(저장장치, 인터커넥터, 수요)이 언제 충전·방전할지 "틀린" 신호를 줄 수 있다고 씁니다. 위 FTI 결과를 인용합니다(p32).
- 제약 뒤에서 system flag bid를 받은 뒤 운전 계획(PN)을 더 낸 행동의 소비자 비용은 £136.3m입니다(2024-11~2025-10, 도매 £59.5m + 균형 £76.8m). **균형 비용의 81.7%가 저장장치(배터리와 양수) 때문**이었습니다(p33).
- 2032-04-28 모형 예시: 스코틀랜드 바람이 강할 때 풍력 약 11 GW를 내리고 인터커넥터 offer 약 14 GW를 올립니다. **저장장치도 북쪽은 bid, 남쪽은 offer로 모두 10 GW를 조정**합니다(p33~34).
- 저장장치를 재급전하면 충전량이 바뀌어 다음 시간에도 같은 양을 다시 사야 하는 "반복 재거래(repetitive re-trading)"가 생긴다고 씁니다(p32). A안의 순차판에서 W1 북쪽을 계획에 묶을 때 생긴 현상(정전, 이탈)과 같은 종류의 문제입니다.
- 급전 개혁 항목에 "저장장치 운영"이 따로 있습니다(p100). 아직 구체안이나 숫자는 없습니다.

---

## 5. 그 밖에 관련 있는 것

| 자료 | 무엇을 했나 | A안과의 관계 | status |
| --- | --- | --- | --- |
| AFRY, *Benefits of Long Duration Electricity Storage*, BEIS Research Paper 2022/019 (2022-07). [원문](https://assets.publishing.service.gov.uk/media/62e9794de90e07142da017ec/benefits-long-duration-electricity-storage.pdf) | 비용 최소 계획 모형. 저장장치가 **제약을 고려해 제자리에 짓도록 하는 위치 신호가 있다고 가정**(p51). 2050년 B6 10 GW에서 한 주 동안 스코틀랜드 잉여 4.4 TWh 예시(p93) | 계획자 최적 쪽만 봄. 왜곡 없음 | sourced |
| Franken, Lyden, Friedrich, *Risk and Reward of Transitioning from a National to a Zonal Electricity Market in Great Britain*, arXiv 2506.04107 (2025-06). [원문](https://arxiv.org/abs/2506.04107) | 2022~2024년, 6구역(B6 포함), 도매 → 재급전 2단계. 지역 가격이면 소비자 약 £9.4/MWh 절약. 저장장치 이익은 지역 가격에서 약 10% 높음 | 전국 vs 지역 가격 비교. 장주기를 따로 보지 않고, 저장장치별 왜곡이나 설계 보완은 없음 | 하위 에이전트가 읽음(일부는 요약), 미확인 |
| Nosratabadi 외, *The Impact of Grid Storage on Balancing Costs and Carbon Emissions in Great Britain*, arXiv 2410.07740 (2024-10). [원문](https://arxiv.org/abs/2410.07740) | 여러 위치·기술 저장장치의 BM 운전이 탄소배출에 주는 영향 | 비용보다 배출. 본문 확인 안 함 | 요약만 |
| Baringa, *Long-duration energy storage: what are the consequences of deploying 7.6 GW through Window 1?* (2026-10-27). [웹 글](https://www.baringa.com/en/insights/low-carbon-futures/long-duration-energy-storage/) | 7.6 GW vs 4.4 GW: 순후생 약 −£1.3bn, 소비자 후생 약 −£1.6bn(2030~2055), floor 지급 연 약 £110m 증가 | cap-and-floor 소비자 부담. 웹 글에는 위치·제약 분석 없음(보고서 본문 미확인) | 웹 글만 |
| Neon(Hirth 등), 독일 대형 배터리의 계통 기여 (*Netzdienlichkeit von Großbatterien*) | 독일 단일 가격구역에서 배터리가 재급전 비용을 조금 줄였지만 "우연"이었다. 시간·위치별 망요금을 권고 | 다른 나라의 같은 구조(단일가격 + 재급전). S2(위치 신호)의 참고 | 요약만 |

---

## 6. 정리: A안이 새로 더하는 것

| 질문 | 기존 자료 | A안 |
| --- | --- | --- |
| 북쪽 장주기가 전국 가격대로 운전하면 재급전 비용이 늘 수 있나? | **있음.** LCP Delta 2024(모형), FTI 2024·NESO 2026(실제 단주기 배터리·양수) | 같은 결론을 2030 Window 1 실제 사업으로 다시 확인 |
| 그중 운전 방식 때문에 생긴 몫(왜곡 D)은 얼마인가? | 찾지 못함. 기존 연구는 모두 "있음 − 없음" | D = 시장 운전 − 계획자 최적 운전, 15개 기상연도 분포 |
| 어떤 설계 보완이 얼마나 줄이나? | 찾지 못함. NESO 2026은 문제 제기와 방향만, FTI·Neon은 지역 가격·망요금을 말로만 권고 | S1a·S1b·S3·S5를 같은 모형에서 비교. S2는 다음 단계 |
| cap-and-floor가 운전 유인에 어떻게 작용하나? | Baringa는 소비자 부담 총액만. 왜곡과의 연결 없음 | floor 아래 운전(M3c), S3에서 floor 보전과 소비자 지급 |
| 공식 평가는 이 위험을 다뤘나? | NESO 평가는 같은 2단계 구조지만 "있음 − 없음"뿐이고, BM 결과는 순위에서 빠짐(요약만). Ofgem 영향 평가는 제약 효과를 이익 쪽으로만 서술 | 공식 평가의 빈칸을 채움 |

**주의**: 위 "찾지 못함"은 이번 검색 범위(웹 검색 십여 번, PDF 8개 읽음)에서의 결과입니다. 학술 데이터베이스(Scopus, Web of Science)를 체계적으로 뒤진 것은 아닙니다. 논문 투고 전에 한 번 더 확인합니다.

## 7. 다음에 할 수 있는 것 (지금은 하지 않음)

- LCP Delta 2024 보고서의 기상연도 수와 연도별 결과를 확인해, A안의 2030 D와 자릿수를 비교합니다. LCP 값은 20년 NPV이고 A안은 한 해 값이라 바로 비교할 수 없습니다.
- Ofgem minded-to 답변 부록에서 "degeneracy" 문장의 원문과 쪽 번호를 확인합니다.
- `literature/papers/`에 LCP Delta 2024, FTI 2024, NESO 2026 카드를 만듭니다.
