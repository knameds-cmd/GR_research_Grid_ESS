# M3c 준비: cap-and-floor 면허 원문이 floor 아래 운전에 대해 말하는 것

> 작성 2026-11-06. M3 사전등록 초안 4장(`m3_prereg_draft_KO.md`)의 "floor 아래 운전 가정"을 정하기 전에 Ofgem 원문을 확인했다(연구자 결정 2026-11-06 "면허 원문 먼저").
> **모두 초안 단계 문서다.** Ofgem은 면허를 "2026년 가을 cap-and-floor 지급 결정 뒤에" 확정한다고 했고, Ofgem LDES 페이지에는 2026-07-28 뒤에 나온 문서가 없다(2026-11-06 확인).
> 원문 PDF는 git에 넣지 않는다. 쪽 번호는 인쇄 쪽.

## 1. 문서

| 줄임 | 문서 | 날짜 | 주소 |
| --- | --- | --- | --- |
| FFD | Financial Framework: LDES Window 1 Cap and Floor regime (OFG1164). NERA가 "FFD"로 인용한 문서(Financial Framework Decision) | 2025-09-23 | https://www.ofgem.gov.uk/sites/default/files/2025-09/LDES%20Window%201%20Financial%20Framework%20Decision.pdf |
| CfI-3월 | LDES: Call for Input on Draft Special Licence Conditions | 2026-03-16 | https://www.ofgem.gov.uk/sites/default/files/2026-03/Long-Duration-Electricity-Storage-Call-for-Input-on-Draft-Special-Licence-Conditions.pdf |
| MtD-7월 | LDES draft special licence conditions: minded-to decisions | 2026-07-21 | https://www.ofgem.gov.uk/sites/default/files/2026-07/Long-duration-electricity-storage-draft-special-licence-conditions-minded-to-decisions.pdf |
| 면허-7월 | Draft LDES special licence conditions, "Consultation Draft July 2026" | 2026-07 | https://www.ofgem.gov.uk/sites/default/files/2026-07/LDES-special-licence-conditions-draft-july-2026.pdf |
| 지침-7월 | Draft guidance on the Special Licence Conditions | 2026-07-28 | https://www.ofgem.gov.uk/sites/default/files/2026-07/Guidance-on-the-Special-Licence-Conditions-for-LDES-cap-and-floor-projects.pdf |

## 2. 찾은 것

| 항목 | 원문 (짧게) | 위치 | 뜻 |
| --- | --- | --- | --- |
| 평가 수익 | "ARₜ = GRₜ − MRCₜ − NCCₜ − IATₜ" | 지침-7월 p24, 5.47 | floor·cap과 비교하는 수익은 총수익에서 시장 관련 비용 등을 뺀 값 |
| 총수익에 드는 것 | 도매(선도·하루 전·당일), 밸런싱 메커니즘(BM)·불균형, 보조서비스, 용량시장 수익 | 지침-7월 p25, 5.51 | 재급전(BM) 수익도 들어감 |
| 빼는 비용 | 시장 관련 비용(MRC)은 "charging energy costs, … Marginal Cycling Costs"를 포함 | 지침-7월 p26, 5.55 | **충전 전기값과 한계 순환 비용(MWh당 마모)을 수익에서 뺌** |
| Ofgem이 본 위험 | "Even when system value is low, a Project might still cycle because its costs could be reimbursed under the C&F regime" | FFD p39, 5.27 | floor 아래에서는 운전 비용을 소비자가 돌려줌 → 가치가 낮아도 돌릴 수 있음 |
| 시장 참여 의무 | "Participate in all eligible electricity markets … including markets for energy, balancing, ancillary services and capacity" | 면허-7월 SpC18 Part A 4(a), p151 | |
| 보류 금지 | "Not unreasonably withhold the Relevant LDES Facility from participation … where this would forego achievable External Revenue" | 면허-7월 SpC18 4(b), p151 | |
| 일부러 보류 금지 | "Deliberately withhold capacity, delay dispatch, or submit inflated offer prices … where the main purpose is to reduce External Revenue so as to increase Floor Level support" | 면허-7월 SpC18 Part D 16(a), p153 | floor 지원을 늘리려고 쉬는 운전은 금지 |
| 위반 시 | Ofgem이 "a prudent and efficient operator" 기준의 가상 값으로 바꿔 넣을 수 있음 | 면허-7월 SpC18 18, pp153–154 | |
| 최소 가용률(MAT) | 배터리 90%, 양수·LAES·CAES 95% → 양수는 92.5%로 낮출 예정 | CfI-3월 p20 §3.6; MtD-7월 p19, 2.51 | |
| 가용률 계산 | NESO에 낸 최대 송전·수전 수준(MEL·MIL)으로 계산. 실제 운전량이 아님 | CfI-3월 p20; MtD-7월 p19, 2.54 | 신고만 하고 쉬어도 가용률은 채움. 막는 것은 보류 금지 조항 |
| cap 위 | 보유율 10% → 30%로 올림 "to strengthen operational incentives" | FFD p29, 4.6 | |
| 송전 제약 | 제약 때문에 생기는 반복 재거래가 "can lead to inefficient dispatch"라고 인정하면서도 "not introducing LDES-specific requirements at this stage" | MtD-7월 p43, 2.197·2.199 | **위치·B6 관련 규칙은 없음.** NESO의 개혁된 전국 가격 작업으로 넘김 |
| 짧게 돌리기 | 장주기 능력과 "materially inconsistent"하게 상시 운전하면 안 됨 | 지침-7월 p55, 5.277–5.278 | |

찾지 못한 것: 면허·Window 1 지급의 최종 결정, 사업별 최종 MAT 값, 한계 순환 비용 계산 방법, 가용률을 실제 운전과 묶는 규칙, Ofgem의 운전 변화 정량 추정, 위치·구역 가격에 대한 운전 규칙.

## 3. M3c에 주는 뜻 (해석, 판정 아님)

1. **초안 4장의 선택지 (b) "floor 아래에서는 거의 쉰다"는 원문과 맞지 않는다.** 충전 전기값과 순환 비용을 수익에서 빼므로, floor 아래 사업자는 운전해도 비용을 잃지 않는다. 그리고 보류 금지 조항이 floor를 노린 휴지를 막는다. 그래서 floor 아래 사업자의 한계 이익은 0이고(무차별), 면허는 시장에서 "신중하고 효율적인 사업자"처럼 운전하라고 요구한다.
2. 그러면 법이 요구하는 운전에 가장 가까운 것은 **(a) 시장 이익 최대 운전(= M1)**이다. M1의 주 가정이 원문으로 뒷받침된다.
3. 원문이 연 새 위험은 반대 방향이다. Ofgem 스스로 "가치가 낮아도 돌릴 수 있다"(FFD 5.27)고 했다. 이것을 모형에 넣는다면 "floor 아래 사업자는 시장 비용을 무시하고 운전한다(충전 전기값 0으로 봄)"는 범위 판이 된다. 이 판은 B6 북쪽에서 충전·방전을 더 많이 해 D를 키우는 쪽이다.
4. **A안의 왜곡(전국 가격에 맞춘 운전이 B6 제약을 악화)은 면허 초안이 다루지 않는다.** Ofgem은 제약 문제를 인정하면서도 LDES 전용 규칙을 넣지 않았다(MtD-7월 2.199). 설계안 S1·S3의 정책 근거로 쓸 수 있다.

## 4. 연구자에게 물을 것 (M3c 사전등록 때)

- 주 결과를 (a) 그대로 두고, 범위 판으로 위 3번("floor 아래에서 충전 비용을 무시")을 넣을지, 아니면 (a)만 두고 3번은 말로만 적을지.
- 면허가 확정되면(2026년 가을 이후) 이 메모를 다시 확인한다.
