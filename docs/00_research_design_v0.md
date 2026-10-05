# 영국 계통용 배터리 수익성 연구 설계

Oct 5, 2026 · @Dongseok

## 1. 회의 요약

교수님 결론: 기존 주제(imbalance 정산·시장 구조 전반 + AI)는 박사논문 규모라서 접고, \*\*"계통용 배터리가 어떤 시장 메커니즘 덕분에 수익을 내게 되었나"\*\*를 국가별 사례로 좁혀 논문 한 편 단위로 만들라는 것.

- **사례 구도**: 호주(최초로 수익화) → 영국(작년부터 수익화, 지금 붐) → 북유럽(이제 막 수익화 진입) → 한국(아직 수익성 없음). 한 명은 북유럽, 본인은 영국을 맡음. 방법론은 공유하고 결과는 각자 다른 논문.
- **교수님이 직접 던진 질문 4개** (연구 질문의 뼈대로 그대로 쓰면 됨):
  1. 계통용 배터리는 어떤 가치(benefit/value)를 제공하는가?
  2. 어떤 시장 메커니즘에 참여할 수 있는가? (보조서비스, 용량시장, 유연성 서비스)
  3. 어떤 규제 변화가 필요했는가?
  4. 영국/북유럽에서는 각각 실제로 어떻게 작동하는가?
- **방법 지시**: ① 필요한 데이터 입력이 뭔지 정리 → ② 데이터 포털에서 직접 다운로드(AI 접근은 막혀 있어도 사람은 무료로 받을 수 있음) → ③ 받은 엑셀/CSV로 모델링.
- **입찰 전략의 위치**: "입찰이어야 하냐"는 질문에 교수님은 "Bidding is gonna be a part of this" — 입찰은 주제의 한 층(layer)으로 들어가고, 주제 자체는 **market design**.
- **최종 메시지**: 한국 정책입안자·투자자가 "영국은 이런 시장 규칙을 만들었고, 그래서 배터리가 사업이 됐다"를 보고 그대로 이식할 수 있는 근거.

## 2. 연구 질문과 범위

한 줄 주제: **"영국 시장의 어떤 상품 규칙이 배터리를 수익 사업으로 만들었고, 각 규칙은 수익성과 입찰 전략을 얼마나 바꾸는가"**. 영국은 2020년 DC 도입 → 2022년 호황 → 2023년 수익 67% 붕괴 → 도매·BM 중심 재편이라는 뚜렷한 국면이 있어서, 규칙과 수익의 관계를 보기에 좋은 자연실험입니다.

| RQ | 질문 | 교수님 질문과의 대응 | 방법 |
| --- | --- | --- | --- |
| RQ1 | GB 배터리 수익 구성은 2020–2026년 어떻게 변했고, 각 국면을 만든 제도 변화는 무엇인가? | ① 가치, ② 참여 메커니즘 | 공개 데이터로 revenue stack 분해 + 제도 연표 |
| RQ2 | 개별 규칙(DC 도입, EAC 공동최적화, SoE 의무화, BM 30분 규칙·skip rate, CM 디레이팅)은 대표 배터리의 NPV/IRR에 각각 얼마나 기여했나? | ③ 규제 변화 | 규칙 on/off 반사실(counterfactual) 시뮬레이션 |
| RQ3 | 규칙이 바뀌면 최적 입찰·운전 전략(서비스 배분, 사이클, SoC)은 어떻게 바뀌는가? | "Bidding is a part" | 완전예측 MILP(상한) vs 롤링 호라이즌 MILP(예측 기반) |
| RQ4 | 한국에 이식한다면 어떤 규칙이 우선이고, 어떤 함정(포화, 디레이팅)을 피해야 하나? | 한국 시사점 | RQ2 결과를 한국 제도에 매핑 |

**범위**

- 자산: 대표 배터리 50 MW, **1시간·2시간** 두 종류 (영국 신규 설치의 주류가 2시간).
- 기간: 추세 분석은 2020–2026, 상세 시뮬레이션은 EAC 공동최적화 경매가 시작된 **2023년 11월 이후**(데이터 포맷이 일관됨).
- 빼는 것: LDES(8시간+ cap-and-floor), 안정도(stability) 시장, 계통 접속 비용 상세 — 한 줄 언급만.
- 북유럽 파트와의 공유: 배터리 스펙·비용 가정·열화 모델·재무 지표를 하나의 템플릿으로 맞추고, 시장 규칙 부분만 국가별로 바꿈. 앞서 정한 "하나의 시뮬레이터 + 시장 규칙 스위치" 설계와 그대로 맞물립니다.

## 3. 영국 배터리 수익원과 시장 규칙

영국 배터리 수익은 초기엔 주파수 응답(2020–22년 수익의 87%)이었지만, 지금은 \*\*도매+BM이 약 60%, 보조서비스 약 33%, 용량시장 약 10%\*\*입니다(2시간 배터리, 2026년 4월까지 12개월, Modo). 아래 표가 모델에 넣어야 할 "규칙 스위치" 목록이기도 합니다.

| 상품 | 조달 방식 | 배터리에 중요한 규칙 | 현재 상태 |
| --- | --- | --- | --- |
| **Dynamic Containment (DC)** L/H | NESO EAC, D-1 14:00, pay-as-clear, 4시간 EFA 블록 | 0.5초 개시/1초 완전응답, 데드밴드 ±0.015 Hz, 최소 에너지 15분 | 2020.9 출시. 2022 호황의 주역, 2023 공급과잉으로 가격 붕괴 |
| **Dynamic Moderation (DM)** | 동일 | 0.5/1초, ±0.1 Hz, 에너지 30분 | 2022.5 출시 |
| **Dynamic Regulation (DR)** | 동일 | 2/10초, 데드밴드 없음, 에너지 60분 | 2022.4 출시 |
| 공통 규칙 (DC/DM/DR) | — | SoE: 결제구간마다 요구 에너지의 20% 회복 여유(2024 의무화). 가용률 99.9% 미만이면 해당 구간 지급 0. K-factor 패널티. 서비스 간 stacking·splitting 허용 | 2026.7.31부터 FPN 없으면 참여 불가 |
| **Balancing Reserve (BR)** | EAC, 결제구간(30분) 단위 가용성 요금 | BM 유닛만. 10분 내 도달, 30분 유지 → 1시간 배터리는 SoC 50% 이상 필요 | 2024.3 출시 |
| **Quick Reserve (QR)** | EAC | 1분 내 완전응답 | 2024.12 출시(Fast Reserve 대체), 2025.10 비BM 개방 |
| **Slow Reserve (SR)** | EAC | 15분 내 응답 | 2026.3.31 출시(STOR 대체), 첫날 가스가 \~75% |
| **Balancing Mechanism (BM)** | NESO 발령, pay-as-bid, Elexon 정산 | 2024.3 MEL/MIL은 30분 유지 가능 출력으로. skip rate(싸는데도 건너뜀) 49%→38%(2025H1→2026H1). 2026.7 GC0166(MDO/MDB) | OBP 일괄발령으로 배터리 발령 증가, 2025.10 월 기록 |
| **도매 (DA/ID)** | EPEX·N2EX DA 경매, 일중 연속거래 | 단일 정산가격(imbalance), VoLL £6,000/MWh | DA 매도 후 BM에서 되사는 "비물리적 재거래"가 핵심 수익원으로 부상 |
| **Capacity Market (CM)** | T-4/T-1 경매, £/kW/yr | 디레이팅: 1시간 10.47%, 2시간 20.94%(T-4 2028/29). 2017년 0.5시간 저장장치 96%→21%로 삭감 | 2026.3 T-4 £27.10(-55%), T-1 £5로 폭락 |

**국면별 수치** (Modo, 연간환산 £k/MW/yr. 지수가 여러 번 개편돼 엄밀한 비교는 불가)

| 연도 | 설치용량 | 수익 | 무슨 일이 있었나 |
| --- | --- | --- | --- |
| 2025 | 6.8 GW / 11 GWh | 월별 47–77 | BM 발령 급증, QR 비BM 개방 |
| 2024 | 4.7 GW | 48.7 | BR·QR 출시, 신규 67%가 2시간 |
| 2023 | 3.5 GW / 4.5 GWh | 51 (-67%) | DC/DR 공급과잉, EAC 도입·가격하한 폐지 |
| 2022 | 약 2.1 GW | **156 (정점)** | DC 63% + FFR 25% |

역사적 출발점은 **2016년 8월 EFR 입찰**(약 200 MW, 낙찰 대부분 배터리, 4년 계약)입니다. 출처: [NESO EAC](https://www.neso.energy/industry-information/balancing-services/enduring-auction-capability-eac), [Dynamic Response Guidance](https://www.neso.energy/document/276606/download), [Modo 2022 리뷰](https://modoenergy.com/research/en/7326), [Modo 2023 리뷰](https://modoenergy.com/research/modo-battery-energy-storage-year-review-2023-capacity-revenues-frequency-response), [Modo 2024 리뷰](https://modoenergy.com/research/en/gb-battery-energy-storage-markets-2024-year-in-review-great-britain-wholesale-balancing-mechanism-frequency-response-reserve), [Modo CM T-4 2029/30](https://modoenergy.com/research/en/gb-capacity-market-t4-2029-30-battery-energy-storage-march-2026), [ESS News skip rate](https://www.ess-news.com/2026/07/14/lower-skip-rates-for-uk-battery-storage-but-neso-plans-further-reform/).

## 4. 데이터: 무엇부터 볼지

첫 주에는 **① EAC 경매 결과 + ② Elexon 시장가격(MID)·정산가격** 세 가지만 받으면 됩니다. 이것만으로 "보조서비스 vs 도매" 수익 비교의 첫 그림이 나오고, 모델의 최소 입력이 다 갖춰집니다. 모두 무료입니다.

| 순서 | 데이터 | 어디서 | 모델에서 쓰임 |
| --- | --- | --- | --- |
| 1 | **EAC auction results** — DC/DM/DR/BR/QR/SR 낙찰가·물량, 유닛별 결과 (2023.11\~, UTC) | [NESO Data Portal](https://www.neso.energy/data-portal/eac-auction-results) (CKAN API, 키 불필요) | 보조서비스 가용성 수입 (£/MW/h) |
| 2 | **Market Index Data (MID)** — 거래소 30분 가격 | [Elexon Insights](https://bmrs.elexon.co.uk) (`data.elexon.co.uk/bmrs/api/v1`) | 도매 차익거래. DA 가격은 유료(N2EX/EPEX)라 MID를 대용 |
| 3 | **System/imbalance price** (DISEBSP) | Elexon Insights | 정산가격 노출, BM 가치의 근사 |
| 4 | **BOD/BOALF** — 배터리 BM 유닛의 입찰·발령 기록 + NESO **skip rate** 데이터(2024.12\~) | Elexon Insights, [NESO skip rates](https://www.neso.energy/industry-information/balancing-services/skip-rates) | BM 수익과 "발령 확률" 모델링 |
| 5 | **System Frequency** — 1초 해상도 (2020\~) | [NESO Data Portal](https://www.neso.energy/data-portal/system-frequency-data) | DC/DM/DR 응답 시 SoC 변화·열화 시뮬레이션 |
| 6 | **Capacity Market** — 등록부, 경매 결과, 디레이팅 계수 | [EMR Delivery Body](https://www.emrdeliverybody.com/CM/Auction-Results.aspx) | 고정 용량 수입 (£/kW/yr × 디레이팅) |
| 7 | EAC 이전 DC/DM/DR 결과 (2020–23, EPEX 운영 시절) | NESO Data Portal에서 "Dynamic Containment" 검색 | RQ1 2022 호황기 분석 |
| 8 | 사업 파이프라인·벤치마크 | [REPD](https://www.gov.uk/government/publications/renewable-energy-planning-database-quarterly-extract), Modo 무료 계정 | 설치용량 추이, 모델 검증용 비교치 |

**주의할 점**

- 영국은 브렉시트 이후 2021년 6월부터 ENTSO-E Transparency에 데이터가 없습니다. 북유럽은 ENTSO-E에서 DA 가격을 무료로 받을 수 있어 양쪽 데이터 출처가 다릅니다.
- 시간 단위가 제각각입니다: EFA 4시간 블록(DC/DM/DR), 30분 결제구간(BR, 도매, BM), 1초(주파수). 모델 기본 해상도는 **30분**으로 두고 나머지를 맞추는 것을 권합니다. EAC는 UTC, Elexon은 영국 현지시간 기준 결제구간이라 서머타임 처리도 필요합니다.
- 비용 가정(CAPEX, O&M, 열화)은 데이터 포털이 아니라 문헌에서 가져옵니다 (Schmidt et al. 2019; Xu et al. 2018, 6장 참고).
- 북유럽 파트 참고: Fingrid Open Data(FCR-N/FCR-D/FFR, API 키 필요), 호주 비교용 AEMO NEMWEB(5분 FCAS 가격, 무료).

## 5. 모델 설계

핵심은 **하나의 수익 스택 최적화 모델 위에 "시장 규칙"을 스위치로 올려놓고, 규칙을 하나씩 끄고 켜면서 수익성(NPV/IRR) 변화를 재는 것**입니다. 입찰 전략은 그 모델을 "얼마나 알고 운영하느냐"의 층으로 들어갑니다.

&#91;embedded content: 모델 구조 · 4개 층\]

엔진은 하나이고 규칙만 바뀝니다. 북유럽 파트도 같은 엔진에 자기 규칙 세트를 넣으면 비교가 됩니다.

**층 1 — 수익 스택 최적화 (MILP, 하루 단위 롤링)**

- 결정변수: EFA 블록별 서비스 제공량 rₛ,b (DC-L/H, DM-L/H, DR-L/H, BR, QR), 30분 단위 도매 충방전 pₜ, BM 제안량.
- 가격 수용자(price-taker) 가정: 50 MW는 시장 대비 작음. 포화 효과는 과거 낙찰가에 이미 반영되어 있음.
- 영국 규칙을 제약으로: 출력 여유, 서비스별 최소 에너지(DC 15분/DM 30분/DR 60분), SoE 20% 회복 규칙, BR의 30분 지속, 효율, 열화 비용.

```latex
\max \sum_{b,s} \pi^{av}_{s,b} r_{s,b} + \sum_t \lambda_t p_t \Delta t + \sum_t (1-\rho^{skip}) \pi^{BM}_t q_t \Delta t - c^{deg}\sum_t (p^{ch}_t+p^{dis}_t)\Delta t
```

```latex
\text{s.t. } p_t + \sum_{s\in L} r_{s,b(t)} \le P,\quad -p_t + \sum_{s\in H} r_{s,b(t)} \le P,\quad \sum_{s\in L} r_{s,b(t)}\tau_s \le SoC_t \le E - \sum_{s\in H} r_{s,b(t)}\tau_s
```

τₛ는 서비스별 요구 에너지 시간(DC 0.25h, DM 0.5h, DR 1h), ρ^skip은 BM skip rate. 첫 버전은 BM을 "발령 확률 × 정산가격"으로 단순화하고, 이후 BOD/BOALF로 정교화합니다.

**층 2 — 정보 수준 (= 입찰 전략)**

1. 완전예측(perfect foresight): 수익의 상한. 규칙 효과를 깨끗하게 보는 기준선.
2. 롤링 호라이즌 + 예측: D-1 14:00에 EAC 입찰을 확정하고 남은 용량으로 도매·BM 운영. 실제 운영자와 같은 정보 구조.
3. (선택) 2단계 확률계획: 가격 시나리오로 D-1 입찰을 정함(Krishnamurthy et al. 2018 방식). 롤링 결과의 강건성 점검용.

1과 2의 차이가 "정보의 가치"입니다. 세 방식 모두 같은 입력에 같은 답이 나오므로, 수익 차이를 규칙 효과로 깔끔하게 귀속할 수 있습니다. RL은 학습 seed·하이퍼파라미터에 따라 결과가 흔들려 규칙 효과와 섞이므로 이 논문에서는 쓰지 않습니다. 교수님 말처럼 입찰은 주제의 한 층이고, 논문의 주인공은 규칙입니다.

**층 3 — 규칙 스위치와 기여도 분해**

| 스위치 | 끄면(반사실) | 물어보는 것 |
| --- | --- | --- |
| DC/DM/DR 존재 | 도매+BM만 | 빠른 주파수 상품이 얼마나 결정적이었나 |
| EAC 공동최적화·splitting | 서비스 간 배타적 선택 | stacking 허용의 가치 |
| SoE 20% 규칙 | 규칙 없음 | 에너지 관리 규제의 비용 |
| BM 접근 (skip rate) | skip 0% / 49% / 38% | 발령 관행이 수익에 주는 영향 |
| CM 디레이팅 | 2017 이전(96%) vs 현재 | 용량시장 설계의 영향 |
| 자산 지속시간 | 1h vs 2h | 규칙이 어떤 자산을 선호하나 |

규칙끼리 상호작용이 있으므로(예: SoE 규칙은 DC가 있을 때만 의미) 하나씩 끄는 것보다 **Shapley 분해**로 각 규칙의 기여도를 배분하면 방법론적 기여가 됩니다(규칙 6개면 2⁶=64회 시뮬레이션, MILP이면 충분히 가능).

**층 4 — 재무 모델**

CAPEX(£/kW, £/kWh), O&M, 열화(사이클 기반, Xu et al. 2018), 수명 15년, WACC로 NPV·IRR·회수기간 계산. 민감도: 가격 변동성, 가용성 패널티, 열화 비용, CM 가격 폭락(2026).

**검증**: 완전예측·롤링 결과를 Modo 월별 지수(£k/MW/yr)와 비교. 롤링 결과가 지수 근처, 완전예측이 그 위에 있으면 모델이 현실적이라는 근거가 됩니다.

## 6. 선행연구 계보

이 연구는 일곱 갈래 문헌(A–G)이 만나는 지점에 있고, 중심 흐름은 다섯 단계입니다: **저장장치 가치 평가 → 수익 스택 → 영국 주파수 상품 연구 → 저장장치용 시장설계 → 입찰 최적화/RL**. 아래 논문은 모두 출판사·DOI로 서지사항을 확인했고, MDPI·학회발표는 뾈습니다. 전체 서지와 DOI는 9장에 있습니다.

&#91;embedded content: 선행연구 계보 · 6개 흐름 → 이 연구 → 한국\]

각 흐름이 남긴 공백(오른쪽 화살표 문장)을 모으면 "규칙을 변수로 두고 수익을 분해한다"는 이 연구의 자리가 됩니다.

| 갈래 | 대표 논문 | 이 흐름이 밝힌 것 | 남은 공백 |
| --- | --- | --- | --- |
| **A. 저장장치 가치·경제성** | Walawalkar et al. 2007 (*Energy Policy*); Sioshansi et al. 2009 (*Energy Economics*); Staffell & Rustomji 2016 (*J. Energy Storage*); Braff et al. 2016 (*Nature Climate Change*); Schmidt et al. 2019 (*Joule*); Mallapragada et al. 2020 (*Applied Energy*) | 차익거래만으로는 수지가 안 맞고, 주파수 조정이 돈이 된다(2007). 가치는 운영 전략에 크게 좌우된다(GB 데이터, 2016). 보급이 늘면 가치가 떨어진다(2020) | "어떤 시장 규칙이" 가치를 만드는지는 가정으로 둠 |
| **B. 수익 스택·보조서비스** | He et al. 2011 (*Energy Policy*); Stephan et al. 2016 (*Nature Energy*); Kazemi et al. 2017 (*IEEE TSTE*); Englberger et al. 2020 (*Cell Rep. Phys. Sci.*); Biggins et al. 2022 (*J. Energy Storage*) | 여러 서비스를 겹치면 경제성이 생기고, 고정 배분보다 동적 배분이 낫다 | stacking을 "허용하는 규칙" 자체는 고정된 입력 |
| **C. 영국 특화** | Greenwood et al. 2017 (*Applied Energy*); Gundogdu et al. 2018 (*IEEE TIE*); Lee et al. 2019 (*Applied Energy*); Martins & Miles 2021 (*Energy Policy*); Cao X. et al. 2024 (*IJEPES*); Fan et al. 2025 (*CSEE JPES*); Grubb & Newbery 2018 (*Energy Journal*); Newbery 2018 (*Energy Policy*); Williams & Green 2022 (*Energy Policy*) | 상품 사양(EFR→DC)이 배터리 적합성·SoC·열화를 바꾼다. 영국 배터리 사업모델의 회수기간. EMR(CfD·CM) 평가 | 대부분 EAC(2023.11) 이전 데이터. BR·QR·SR·skip rate·CM 폭락을 다룬 통합 분석 없음 |
| **D. 비교 시장** | Csereklyei et al. 2021 (*Utilities Policy*, 호주); Rangarajan et al. 2023 (*Energy Economics*, 호주); Thien et al. 2017 (*J. Energy Storage*, 독일); Nitsch et al. 2021 (*Applied Energy*, 독일); Mirzaei Alavijeh et al. 2025 (*Applied Energy*, 스웨덴); Lieskoski et al. 2024 (*J. Energy Storage*, 핀란드) | 호주에서 배터리 진입이 FCAS 비용을 낮췄다. 유럽 각국 FCR/aFRR 규칙이 운영을 좌우 | 국가별 단일 사례. 같은 모델로 규칙만 바꿔 비교한 연구 드묾 |
| **E. 저장장치 시장설계** | Sioshansi 2017 (*IEEE TPWRS*); Sakti et al. 2018 (*Energy Policy*); Parra & Mauger 2022 (*Energy Policy*); Sioshansi et al. 2022 (*IEEE TPWRS*, 리뷰) | 참여 모델·비용회수 메커니즘·EU 법제를 정리 | 대부분 정성적. 규칙별 수익 기여를 정량화하지 않음 |
| **F. 입찰·최적화·RL** | Mohsenian-Rad 2016; Krishnamurthy et al. 2018; Xu et al. 2018 (이상 *IEEE TPWRS*); Cao J. et al. 2020; Kwon & Zhu 2022 (이상 *IEEE TSG*); Li et al. 2024 (*IEEE TEMPR*); Cardo-Miota et al. 2025 (*Applied Energy*) | 불확실성·열화를 반영한 입찰. DRL 차익거래(GB 가격), 에너지+예비력 다중시장 DRL(호주 NEM, 아일랜드) | 시장 규칙을 고정된 환경으로 둠. 규칙이 바뀌면 전략이 어떻게 바뀌는지는 미해결 |
| **G. 한국** | Shcherbakova et al. 2014 (*Applied Energy*); Im & Chung 2023 (*J. Energy Storage*) | 한국 비용기반 풀에서 차익거래는 비경제적. 2017–19 ESS 화재가 보조금 설계와 연결 | 해외 시장설계 이식 관점의 정량 연구는 거의 없음 (주요 저널 기준) |

**먼저 읽을 6편** (이 순서로)

1. Staffell & Rustomji 2016 — GB 데이터로 본 저장장치 가치의 원형.
2. Greenwood et al. 2017 — "상품 사양이 배터리 수익을 좌우한다"는 이 연구 가설의 직계 조상.
3. Martins & Miles 2021 — 영국 배터리 사업모델 재무분석. 업데이트할 대상.
4. Biggins et al. 2022 — GB 차익거래+주파수 공동최적화. 층 1 MILP의 출발점.
5. Stephan et al. 2016 — 수익 스택의 정책적 의미(공공비용).
6. Krishnamurthy et al. 2018 — DA·RT 가격 불확실성 아래 확률적 차익거래. 층 2 롤링·확률계획의 기준.

**별도 확인 필요** (2026년 신규, 서지 일부만 확인): *J. Energy Storage* (2026) "Balancing with batteries: The impact of revenue stacking and skip rates on battery energy storage profitability in Great Britain" — 주제가 가장 가까운 경쟁 논문일 가능성이 큽니다. 저자·DOI를 직접 확인하고 차별점을 정리해야 합니다. *Energy & Environmental Science* 19(13) (2026) "Maximising the economic value of renewable and battery storage hybrids with revenue stacking"도 함께 확인.

## 7. 이 연구의 위치와 기여

한 문장으로: **입찰 문헌(F)은 시장 규칙을 고정된 환경으로, 시장설계 문헌(E)는 수익을 정성적으로 다뤘다. 이 연구는 규칙을 변수로 둬 배터리 수익성을 규칙별로 분해하는, 두 문헌 사이의 다리입니다.**

**공백 (선행연구가 안 한 것)**

- 영국 문헌(C)은 대부분 EFR/FFR 시절이거나 DC 하나만 봅니다. EAC 공동최적화(2023.11) 이후 BR·QR·SR, BM skip rate, 2026 CM 폭락까지 묶은 수익 구조 분석은 학술지에 없습니다(업계 보고서는 Modo 등 유료 자료뿐).
- "어느 규칙이 수익을 얼마나 만들었나"를 반사실로 분해한 연구가 없습니다. 비교 문헌(D)도 나라별 단일 사례라 규칙 효과와 가격 환경 효과가 섞여 있습니다.
- 입찰 최적화 문헌(RL 포함)은 규칙이 바뀌면 최적 전략이 어떻게 바뀌는지 묻지 않습니다.

**기여**

1. **실증**: EAC 이후(2023.11–2026) 영국 배터리 수익 스택을 공개 데이터만으로 재구성 — 재현 가능한 데이터 부록 포함.
2. **방법론**: 규칙 스위치 반사실 + Shapley 분해로 수익성을 개별 규칙에 귀속.
3. **전략**: 규칙 체제마다 완전예측과 롤링 호라이즌의 격차를 비교 → "규칙의 가치"와 "정보의 가치"를 분리.
4. **정책**: 한국에 이식할 규칙의 우선순위와 피해야 할 함정.

**한국 이식 프레임** (RQ4의 틀. 한국 쪽 현황은 별도 확인 필요)

| 영국에서 배울 것 | 한국에 던질 질문 |
| --- | --- |
| 빠른 주파수 상품을 따로 만들고 일일 경매로 조달(DC) | 한국 보조서비스는 어떤 방식으로 조달·보상되나? 배터리가 경쟁 입찰로 들어갈 문이 있나? |
| 포화의 교훈: 소규모 주파수 시장은 배터리 몇 GW에 금방 차고 가격이 붕괴(2023) | 한국 주파수 예비력 수요 규모 대비 배터리 보급 계획은? |
| 도매·BM 재거래가 장기 수익의 바탕 | 비용기반 풀에서 가격 신호가 배터리에 전달되나? (Shcherbakova et al. 2014) |
| 용량 디레이팅은 지속시간별로 차등 | 한국 용량요금은 저장장치를 어떻게 평가하나? |
| 보조금이 아닌 시장 수입(merchant)으로 성장 | 한국 2017–19 보조금 기반 성장과 화재 이후 정체의 교훈 (Im & Chung 2023) |

## 8. 다음 단계

파견 종료(12월 10일)까지 초안과 핵심 결과 1개(규칙별 수익 기여도)를 만드는 것을 목표로 잡았습니다.

**10/6–10/13 — 데이터 첫 접촉**

- [ ] 6장 "먼저 읽을 6편" 읽기
- [ ] EAC 경매 결과, Elexon MID·정산가격을 한 달치(예: 2025년 10월) 내려받기
- [ ] 첫 그림: 서비스별 낙찰가(£/MW/h) vs 도매 일일 스프레드
- [ ] "Balancing with batteries"(J. Energy Storage 2026) 저자·내용 확인 → 차별점 메모

**10/14–10/21 — 출장 주간: 문헌 정리 위주**

- [ ] 6장 A–G 나머지 논문 초록·관련 연구 절 초안

**10/22–11/8 — 층 1 모델**

- [ ] 북유럽 파트와 공통 템플릿 합의(배터리 스펙, 비용, 열화, 재무 지표)
- [ ] 완전예측 MILP 구현(Python + Pyomo 또는 CVXPY), 2시간 배터리 1년치
- [ ] Modo 월별 지수와 비교 검증
- [ ] 교수님께 중간 보고: RQ와 첫 결과

**11/9–11/22 — 규칙 스위치**

- [ ] 규칙 6개 스위치 구현 + Shapley 분해
- [ ] 롤링 호라이즌(D-1 입찰 확정) 버전
- [ ] 재무 모델(NPV/IRR)과 민감도

**11/23–12/10 — 종합과 초안**

- [ ] (선택) 2단계 확률계획으로 롤링 결과 강건성 점검
- [ ] 한국 이식 프레임에 결과 매핑, 북유럽 파트와 비교 메모
- [ ] 논문 초안 + 데이터 부록(출처·다운로드 절차)

투고처 후보: 정책·시장설계 비중이 크면 *Energy Policy* / *Utilities Policy*, 모델 비중이 크면 *Applied Energy* / *Journal of Energy Storage*. 교수님과 상의해 정하면 됩니다.

## 9. 참고문헌

모두 DOI 또는 출판사/기관 저장소 페이지에서 서지를 확인했습니다(2026-10-05).

**A. 저장장치 가치·경제성**

- Walawalkar R, Apt J, Mancini R (2007). Economics of electric energy storage for energy arbitrage and regulation in New York. *Energy Policy* 35(4):2558–2568. [doi:10.1016/j.enpol.2006.09.005](https://doi.org/10.1016/j.enpol.2006.09.005)
- Sioshansi R, Denholm P, Jenkin T, Weiss J (2009). Estimating the value of electricity storage in PJM: Arbitrage and some welfare effects. *Energy Economics* 31(2):269–277. [doi:10.1016/j.eneco.2008.10.005](https://doi.org/10.1016/j.eneco.2008.10.005)
- Staffell I, Rustomji M (2016). Maximising the value of electricity storage. *Journal of Energy Storage* 8:212–225. [doi:10.1016/j.est.2016.08.010](https://doi.org/10.1016/j.est.2016.08.010)
- Braff WA, Mueller JM, Trancik JE (2016). Value of storage technologies for wind and solar energy. *Nature Climate Change* 6(10):964–969. [doi:10.1038/nclimate3045](https://doi.org/10.1038/nclimate3045)
- Zafirakis D, Chalvatzis KJ, Baiocchi G, Daskalakis G (2016). The value of arbitrage for energy storage: Evidence from European electricity markets. *Applied Energy* 184:971–986. [doi:10.1016/j.apenergy.2016.05.047](https://doi.org/10.1016/j.apenergy.2016.05.047)
- Schmidt O, Hawkes A, Gambhir A, Staffell I (2017). The future cost of electrical energy storage based on experience rates. *Nature Energy* 2:17110. [doi:10.1038/nenergy.2017.110](https://doi.org/10.1038/nenergy.2017.110)
- Schmidt O, Melchior S, Hawkes A, Staffell I (2019). Projecting the future levelized cost of electricity storage technologies. *Joule* 3(1):81–100. [doi:10.1016/j.joule.2018.12.008](https://doi.org/10.1016/j.joule.2018.12.008)
- Mallapragada DS, Sepulveda NA, Jenkins JD (2020). Long-run system value of battery energy storage in future grids with increasing wind and solar generation. *Applied Energy* 275:115390. [doi:10.1016/j.apenergy.2020.115390](https://doi.org/10.1016/j.apenergy.2020.115390)
- Lamp S, Samano M (2022). Large-scale battery storage, short-term market outcomes, and arbitrage. *Energy Economics* 107:105786. [doi:10.1016/j.eneco.2021.105786](https://doi.org/10.1016/j.eneco.2021.105786)

**B. 수익 스택·보조서비스**

- He X, Delarue E, D'haeseleer W, Glachant J-M (2011). A novel business model for aggregating the values of electricity storage. *Energy Policy* 39(3):1575–1585. [doi:10.1016/j.enpol.2010.12.033](https://doi.org/10.1016/j.enpol.2010.12.033)
- Stephan A, Battke B, Beuse MD, Clausdeinken JH, Schmidt TS (2016). Limiting the public cost of stationary battery deployment by combining applications. *Nature Energy* 1:16079. [doi:10.1038/nenergy.2016.79](https://doi.org/10.1038/nenergy.2016.79)
- Kazemi M, Zareipour H, Amjady N, Rosehart WD, Ehsan M (2017). Operation scheduling of battery storage systems in joint energy and ancillary services markets. *IEEE Trans. Sustainable Energy* 8(4):1726–1735. [doi:10.1109/TSTE.2017.2706563](https://doi.org/10.1109/TSTE.2017.2706563)
- Englberger S, Jossen A, Hesse H (2020). Unlocking the potential of battery storage with the dynamic stacking of multiple applications. *Cell Reports Physical Science* 1(11):100238. [doi:10.1016/j.xcrp.2020.100238](https://doi.org/10.1016/j.xcrp.2020.100238)
- Biggins F, Homan S, Ejeh JO, Brown S (2022). To trade or not to trade: Simultaneously optimising battery storage for arbitrage and ancillary services. *Journal of Energy Storage* 50:104234. [doi:10.1016/j.est.2022.104234](https://doi.org/10.1016/j.est.2022.104234)

**C. 영국 특화**

- Greenwood D, Lim KY, Patsios C, Lyons PF, Lim YS, Taylor PC (2017). Frequency response services designed for energy storage. *Applied Energy* 203:115–127. [doi:10.1016/j.apenergy.2017.06.046](https://doi.org/10.1016/j.apenergy.2017.06.046)
- Gundogdu BM, Nejad S, Gladwin DT, Foster MP, Stone DA (2018). A battery energy management strategy for UK enhanced frequency response and triad avoidance. *IEEE Trans. Industrial Electronics* 65(12):9509–9517. [doi:10.1109/TIE.2018.2818642](https://doi.org/10.1109/TIE.2018.2818642)
- Grubb M, Newbery D (2018). UK electricity market reform and the energy transition: Emerging lessons. *The Energy Journal* 39(6):1–26. [doi:10.5547/01956574.39.6.mgru](https://doi.org/10.5547/01956574.39.6.mgru)
- Newbery D (2018). Shifting demand and supply over time and space to manage intermittent generation: The economics of electrical storage. *Energy Policy* 113:711–720. [doi:10.1016/j.enpol.2017.11.044](https://doi.org/10.1016/j.enpol.2017.11.044)
- Lee R, Homan S, Mac Dowell N, Brown S (2019). A closed-loop analysis of grid scale battery systems providing frequency response and reserve services in a variable inertia grid. *Applied Energy* 236:961–972. [doi:10.1016/j.apenergy.2018.12.044](https://doi.org/10.1016/j.apenergy.2018.12.044)
- Homan S, Mac Dowell N, Brown S (2021). Grid frequency volatility in future low inertia scenarios: Challenges and mitigation options. *Applied Energy* 290:116723. [doi:10.1016/j.apenergy.2021.116723](https://doi.org/10.1016/j.apenergy.2021.116723)
- Martins J, Miles J (2021). A techno-economic assessment of battery business models in the UK electricity market. *Energy Policy* 148:111938. [doi:10.1016/j.enpol.2020.111938](https://doi.org/10.1016/j.enpol.2020.111938)
- Williams O, Green R (2022). Electricity storage and market power. *Energy Policy* 164:112872. [doi:10.1016/j.enpol.2022.112872](https://doi.org/10.1016/j.enpol.2022.112872)
- Cao X, Engelhardt J, Ziras C, Marinelli M, Zhao N (2024). Battery energy storage systems providing dynamic containment frequency response service. *Int. J. Electrical Power & Energy Systems* 162:110288. [doi:10.1016/j.ijepes.2024.110288](https://doi.org/10.1016/j.ijepes.2024.110288)
- Fan F, Nwobu J, Campos-Gaona D (2025). Co-located battery energy storage optimisation for Dynamic Containment under the UK frequency response market reforms. *CSEE J. Power and Energy Systems* 11(1):340–351. [doi:10.17775/CSEEJPES.2023.01210](https://doi.org/10.17775/CSEEJPES.2023.01210)

**D. 비교 시장 (호주·유럽·북유럽)**

- Thien T, Schweer D, vom Stein D, Moser A, Sauer DU (2017). Real-world operating strategy and sensitivity analysis of frequency containment reserve provision with battery energy storage systems in the German market. *Journal of Energy Storage* 13:143–163. [doi:10.1016/j.est.2017.06.012](https://doi.org/10.1016/j.est.2017.06.012)
- Csereklyei Z, Kallies A, Diaz Valdivia A (2021). The status of and opportunities for utility-scale battery storage in Australia: A regulatory and market perspective. *Utilities Policy* 73:101313. [doi:10.1016/j.jup.2021.101313](https://doi.org/10.1016/j.jup.2021.101313)
- Nitsch F, Deissenroth-Uhrig M, Schimeczek C, Bertsch V (2021). Economic evaluation of battery storage systems bidding on day-ahead and automatic frequency restoration reserves markets. *Applied Energy* 298:117267. [doi:10.1016/j.apenergy.2021.117267](https://doi.org/10.1016/j.apenergy.2021.117267)
- Rangarajan A, Foley S, Trück S (2023). Assessing the impact of battery storage on Australian electricity markets. *Energy Economics* 120:106601. [doi:10.1016/j.eneco.2023.106601](https://doi.org/10.1016/j.eneco.2023.106601)
- Lieskoski S, Koskinen O, Tuuf J, Björklund-Sänkiaho M (2024). A review of the current status of energy storage in Finland and future development prospects. *Journal of Energy Storage* 93:112327. [doi:10.1016/j.est.2024.112327](https://doi.org/10.1016/j.est.2024.112327)
- Mirzaei Alavijeh N, Khezri R, Mazidi M, Steen D, Le AT (2025). Profit benchmarking and degradation analysis for revenue stacking of batteries in Sweden's day-ahead electricity and frequency containment reserve markets. *Applied Energy* 381:125151. [doi:10.1016/j.apenergy.2024.125151](https://doi.org/10.1016/j.apenergy.2024.125151)

**E. 저장장치 시장설계**

- Sioshansi R (2017). Using storage-capacity rights to overcome the cost-recovery hurdle for energy storage. *IEEE Trans. Power Systems* 32(3):2028–2040. [doi:10.1109/TPWRS.2016.2607153](https://doi.org/10.1109/TPWRS.2016.2607153)
- Sakti A, Botterud A, O'Sullivan F (2018). Review of wholesale markets and regulations for advanced energy storage services in the United States: Current status and path forward. *Energy Policy* 120:569–579. [doi:10.1016/j.enpol.2018.06.001](https://doi.org/10.1016/j.enpol.2018.06.001)
- Parra D, Mauger R (2022). A new dawn for energy storage: An interdisciplinary legal and techno-economic analysis of the new EU legal framework. *Energy Policy* 171:113262. [doi:10.1016/j.enpol.2022.113262](https://doi.org/10.1016/j.enpol.2022.113262)
- Sioshansi R, Denholm P, Arteaga J, et al. (2022). Energy-storage modeling: State-of-the-art and future research directions. *IEEE Trans. Power Systems* 37(2):860–875. [doi:10.1109/TPWRS.2021.3104768](https://doi.org/10.1109/TPWRS.2021.3104768)

**F. 입찰·최적화·RL**

- Mohsenian-Rad H (2016). Optimal bidding, scheduling, and deployment of battery systems in California day-ahead energy market. *IEEE Trans. Power Systems* 31(1):442–453. [doi:10.1109/TPWRS.2015.2394355](https://doi.org/10.1109/TPWRS.2015.2394355)
- Krishnamurthy D, Uckun C, Zhou Z, Thimmapuram PR, Botterud A (2018). Energy storage arbitrage under day-ahead and real-time price uncertainty. *IEEE Trans. Power Systems* 33(1):84–93. [doi:10.1109/TPWRS.2017.2685347](https://doi.org/10.1109/TPWRS.2017.2685347)
- Xu B, Zhao J, Zheng T, Litvinov E, Kirschen DS (2018). Factoring the cycle aging cost of batteries participating in electricity markets. *IEEE Trans. Power Systems* 33(2):2248–2259. [doi:10.1109/TPWRS.2017.2733339](https://doi.org/10.1109/TPWRS.2017.2733339)
- Cao J, Harrold D, Fan Z, Morstyn T, Healey D, Li K (2020). Deep reinforcement learning-based energy storage arbitrage with accurate lithium-ion battery degradation model. *IEEE Trans. Smart Grid* 11(5):4513–4521. [doi:10.1109/TSG.2020.2986333](https://doi.org/10.1109/TSG.2020.2986333)
- Kwon K-b, Zhu H (2022). Reinforcement learning-based optimal battery control under cycle-based degradation cost. *IEEE Trans. Smart Grid* 13(6):4909–4917. [doi:10.1109/TSG.2022.3180674](https://doi.org/10.1109/TSG.2022.3180674)
- Li J, Wang C, Zhang Y, Wang H (2024). Temporal-aware deep reinforcement learning for energy storage bidding in energy and contingency reserve markets. *IEEE Trans. Energy Markets, Policy and Regulation* 2(3):392–406. [doi:10.1109/TEMPR.2024.3372656](https://doi.org/10.1109/TEMPR.2024.3372656)
- Cardo-Miota J, Beltran H, Pérez E, Khadem S, Bahloul M (2025). Deep reinforcement learning-based strategy for maximizing returns from renewable energy and energy storage systems in multi-electricity markets. *Applied Energy* 388:125561. [doi:10.1016/j.apenergy.2025.125561](https://doi.org/10.1016/j.apenergy.2025.125561)

**G. 한국**

- Shcherbakova A, Kleit A, Cho J (2014). The value of energy storage in South Korea's electricity market: A Hotelling approach. *Applied Energy* 125:93–102. [doi:10.1016/j.apenergy.2014.03.046](https://doi.org/10.1016/j.apenergy.2014.03.046)
- Im D-H, Chung J-B (2023). Social construction of fire accidents in battery energy storage systems in Korea. *Journal of Energy Storage* 71:108192. [doi:10.1016/j.est.2023.108192](https://doi.org/10.1016/j.est.2023.108192)

**시장·데이터 출처 (grey literature)**: [NESO EAC](https://www.neso.energy/industry-information/balancing-services/enduring-auction-capability-eac) · [NESO Data Portal](https://www.neso.energy/data-portal) · [Elexon Insights](https://bmrs.elexon.co.uk) · [EMR Delivery Body](https://www.emrdeliverybody.com/CM/Auction-Results.aspx) · [Modo Energy research](https://modoenergy.com/research) · [Ofgem DC/DM/DR 규칙 변경 결정(2026.6)](https://www.ofgem.gov.uk/sites/default/files/2026-06/Decision-to-approve-Dynamic-Response-Services%20proposed-amendments-to-the-Terms-and-Conditions-related-to-Balancing-Effective-by-31-July-26.pdf)
