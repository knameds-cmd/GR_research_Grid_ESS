# 모델링 세션 인계 메모 (2026-11-04)

> 이 파일은 "모델링 세션"의 작업을 다른 세션이 이어받기 위한 메모입니다. 새 세션은 이 파일을 먼저 읽고, 아래 "먼저 읽을 것" 순서대로 문서를 보면 됩니다.
> 기준 커밋: `5271db3` (브랜치 `claude/cool-goodall-nubbzr`, GitHub에 올라가 있음).

## 1. 연구가 무엇인가

> **2026-11-05 갱신.** 연구자가 방향을 A안으로 정했습니다. 이 메모의 1장·5장·6장을 새 방향에 맞게 고쳤습니다. 구현 작업은 루트 `CLAUDE.md` → `docs/IMPLEMENTATION_A_KO.md` 순서로 읽고 그 문서의 T 순서를 따릅니다.

- 주제: 영국(GB) 장주기 저장장치(LDES, 8시간 이상)와 Ofgem **cap-and-floor** 제도.
- **연구 질문 (A안, 2026-11-05)**: 전국 단일가격 아래에서 B6 북쪽 장주기 자산이 전국 가격에 맞춰 운전하면 송전 제약이 악화되고, NESO 재급전 비용을 소비자가 낸다. 이 왜곡은 얼마나 크고, 어떤 설계 보완이 줄이나?
- 교수님 지시(2026-10-24): 장주기 중심. 12/10 마감은 없음.
- **2026-11-05 확정 결정** (전체 기록은 `docs/12_decisions_2026-11_KO.md`)
  - 연구 성격: 시스템 설계·정책(최적화). 방법: 같은 계통 모형에서 정책 설계안 비교. 규칙별 기여 분해(Shapley)는 헤드라인에서 빼고, 실증 논문의 T1 회계 분해로만 남김.
  - 구조층: 자체 작은 LP(HiGHS), 3 또는 5구역(T3에서 승인), 1시간. PyPSA-GB는 설비·시계열 자료원으로만.
  - 시장 표현: 1단계 전국 시장 → 2단계 비용 최소 재급전 (i) 발전기만 (ii) 저장도 시간을 넘어 (iii) W1 북쪽 장주기만 고정 + 계획자 최적(S6).
  - M1 설계안: S0 현행, S6 계획자 최적, S1a 고정 입출력 한도, S1b 제약 연동 입출력 한도, S5 지역 가격(상한 비교용).
  - 주 지표: 계통 총비용 + 소비자 지급. M1 범위: 2030년, 기상연도 2013, FES Holistic Transition, Window 1 잠정 16건, 완전예측, 중심 비용.
  - go/no-go: 주 지표 D_W1, 크기 기준 M = £25m/년, go = 3M(£75m/년).
- 2026-10-24 결정 (아래 중 추정 대상·구조층 도구·기술 범위는 위 결정으로 대체됨. 자세한 것은 `docs/08_ldes_redesign_KO.md` 5장)
  - 추정 대상: (b) 접근가치 + 산업 범위. "이전에 없던 규칙(cap-and-floor)을 어떻게 비교하나"는 아직 열려 있음.
  - 방법: 장주기를 가장 설득력 있게 보여 주는 쪽.
  - 두 층 구조
    - **실증층(E)**: 2016-09~2026-09 실제 자료, 가격 수용자(price-taker). 기존 양수(Dinorwig, Ffestiniog, Cruachan, Foyers)로 검증.
    - **구조층(S)**: PyPSA-GB × FES × 기상연도. **아직 안 만듦.**
  - 위치: 구조층은 구역(zonal) 망, 실증층은 발전소 속성으로.
  - 관점: 투자자 + 소비자의 cap-and-floor 부담.
  - 기술: 기술 중립 4종(리튬 8/16시간, 양수, 압축공기/액화공기, 흐름전지).
  - 규칙 유형: F/C/P/M (08 문서).

## 2. 먼저 읽을 것 (순서)

0. **(2026-11-05 추가)** 루트 `CLAUDE.md`, `docs/IMPLEMENTATION_A_KO.md`, `docs/12_decisions_2026-11_KO.md`, `review_2026-11-04/`의 네 문서. 아래 1~5는 실증층과 배경을 볼 때
1. `docs/10_study_path_KO.md`: 현재 상태표, 문서 지도, 코드 흐름
2. `docs/09_model_explained_KO.md`: 모델 해설의 최신판 (숫자·해석은 여기가 기준)
3. `docs/11_referee_review_KO.md`: 독립 심사 기록, 남은 일, **5장 다음 작업 순서**
4. `docs/08_ldes_redesign_KO.md`: 장주기 재설계와 확정한 결정
5. 출처: `literature/sources/ldes/FACTS.md`(Ofgem 제도), `literature/sources/psh/PSH_SOURCES.md`(양수 수입원), `literature/sources/tech/TECH_SOURCES.md`(기술·비용)

## 3. 지금까지 한 것 (커밋 순)

| 커밋 | 내용 |
| --- | --- |
| 720912b | 장주기 재설계, `gbess/` 패키지 시작 |
| 1f6fa3e | 양수 거래 밖 수입, 엔진 검증 1 |
| 7ef3ec1 | 엔진에 BM 층, Dinorwig 대조 |
| 792a2a6 | BM 채택 모형(α)과 엔진 검증 |
| aec7a50 | 결산서 대조, Fast Reserve 계약, 배터리 유닛 자료 |
| f33c68c | 엔진에 예비력 보유, 학습 경로 문서(10) |
| e384241 | 검증 4: 단일 예비력 단가로는 "쉬는 운전"을 재현 못 함 |
| 713e3e2 | 독립 심사 반영: 채택 모형 누수 수정, 망요금(BSUoS·TNUoS)·기동 비용, cap-and-floor 정산 규칙 재작성, 검증 5 |
| bb1232d | 입찰 규칙 엔진(가상 자산의 단가 띠 선택), 검증 6 설계 (**실행 안 함**) |
| 5271db3 | 기술·비용 입력 표: Window 1 대표 자산, 세 경우 비용, repex·잔존가치를 cap-and-floor에 연결 |

시험: `.venv/bin/python -m pytest -q tests` → 100개 통과(2026-11-05 기준, 구조층 38개 포함).

## 4. 코드 지도 (`gbess/`)

| 폴더/파일 | 역할 |
| --- | --- |
| `fetch/` | Elexon·NESO 자료 받기 |
| `data/` | 가격, 유닛, 계통 상태(`bm_state.py`, 자기 발전소를 뺀 분위수 `_x{발전소}` 열) |
| `realized/` | 실제 수익 재구성 (도매, BM, BSUoS, `tnuos.py`) |
| `model/` | BM 채택 모형 |
| `engine/` | 2단계 롤링 운전 엔진(계획/실시간 가격 사다리, α 채택 상한, 예비력, 기동 비용, 입찰 규칙). `asset.py`가 `config/technologies.yaml`을 읽음 |
| `validation/` | 검증 1~6 (`psh_*.py`, `accounts.py`). 결과는 `results/validation/` |
| `finance/cap_floor.py` | Ofgem 정산 규칙: 5년 평가·다음 해 지급, 이월·최종 정산, MAT 규칙, cap 초과 70% 환수, repex·잔존가치, IRR(격자 탐색, 가장 큰 근) |
| `finance/costs.py` | 기술·비용 입력 → capex(RAV)·opex·repex·잔존가치·엔진 가변비용 (2025년 실질 £). `python -m gbess.finance.costs`로 표 출력 |
| `config/costs.yaml` | 기술별 low/central/high 값, 출처·쪽(행)·status |
| `config/technologies.yaml` | 대표 자산 크기·효율 (Window 1 Table 6) |

## 5. 주요 결과 (인용 가능한 것만)

- 실증층: 공개 자료로 기존 양수의 도매·BM 수익을 재구성. BM은 Cruachan 결산서와 5% 안팎(09 5.9).
- 정보 시험: 계획 단계가 그날 가격을 알면 2021~2025 거래 수익 오차 49% → 7% (09 5.11). 엔진 값은 "공개 가격 + 단순 예측" 자산의 **하한**이지 "접근가치"가 아님(심사 #2).
- 비용 표 (2025년 £, central): floor는 MW당 연간 리튬 8h £108k, 리튬 16h £192k, 양수 22h £186k, 압축공기 30h £150k, 흐름전지 8h £237k.
- **기존 양수와 비교할 때는 범위를 맞춤** (2026-11-05 고침, 09 4.4). Dinorwig의 2021~2025 도매+BM 거래 수익 £24~70k/MW·년에는 용량시장·비공개 계약이 빠져 있고, Dinorwig는 5시간 설비라 floor와 바로 비교하면 안 됨. 결산서 총이익 기준 Cruachan은 2022~2025년 £182~401k/MW로 양수 floor 이상인 해가 있고, First Hydro는 2017~2025년 £72~137k. 그래서 "시장 수익만으로는 floor에 못 미친다"는 확정할 수 없음.

## 6. 다음 작업 (2026-11-05 교체)

`docs/IMPLEMENTATION_A_KO.md`의 T 순서를 따릅니다. 각 작업의 "멈추고 물어볼 지점"에서는 연구자에게 묻고 기다립니다.

0. **2026-11-05 현황**: T0~T7·T9 1차 완료 (결과 `docs/notes/m1_results_KO.md`, 규칙 결과 "조건부" `docs/notes/m1_go_no_go_KO.md`, 판정은 연구자). T8(2025 기본 점검)은 2025년 기상 자료가 없어 남음. 연구자가 조건부 절차(A)를 골라 순차 재급전과 2020년을 더했다(`docs/notes/m1_conditional_KO.md`). 연구자 판정: **M2로 진행**(2026-11-05). M2 검증과 T8 1차 계산 끝(`docs/notes/m2_validation_KO.md`): V1 떨어짐(보정 여부 연구자 판단 대기), V2c·V6 통과, V2a·V4 떨어짐, V2b·V3는 해석을 연구자에게 물음. V1 원인 점검(메모 7장): 배전망 풍력 지역 분배 + 스코틀랜드 풍력 이용률이 주원인, 바로잡아도 2030 D_lo는 거의 그대로. `backcast.diagnose`, `diagnose_combined`, `m1_input_sensitivity`. 2025 재현: `.venv/bin/python -m gbess.system.backcast`, ERA5 2025: `gbess.system.era5_ncar`. **2026-11-06**: 연구자 결정 ②로 두 입력 수정(스코틀랜드 몫 0.445·0.045, 스코틀랜드 육상 × 0.895)을 주 모형에 넣고 2025 재현(V1 표본 안 통과)과 M1 19개 판을 다시 계산(메모 8장). 2013 규칙 결과 "조건부" 그대로, 2020년만의 규칙 결과는 "no-go"로 바뀜. 연구자 판정: **M2 계속 진행**(2020은 한계로 보고). 수정 전 2025 재현은 `backcast raw`. M1 다시 돌리기: 판마다 20~55분, 8개 동시에 약 2시간. V5: 절차를 관측 전에 정함(spec changelog 2026-11-06), `gbess.system.holdout` (`dry` 연습 판 통과, `v5`는 2027-05-06 이후에만). 인터커넥터 가격 수용 민감도(2020, 연구자 결정 A): `run_m1 --weather-year 2020 --interconnectors price_taking`, 결과 메모 `m1_results_KO.md` 6.1. 연구자 판정(2026-11-06): V2b 주 기준으로 떨어짐(변형 (ii)는 범위 끝값으로만), V3 실패 그대로(S1a·S1b 행동 반응은 검증 안 된 가정), 얼린 모형 태그 `prereg-v5`. M3 사전등록: 단계로 나눠 **M3a만 승인**(2026-11-06, `docs/notes/m3_prereg_draft_KO.md`, spec `scenarios_m3.m3a`). 실행: `python -m gbess.system.m3a inputs` → `jobs`(8개 동시) → `summary`. M3c는 면허 원문 확인 먼저
1. T0 환경 점검 (2026-11-05 완료), T1 문서 정리
2. T2 사전등록 `gbess/config/spec.yaml`. **승인 전에는 T5 이후 모형을 돌리지 않음.** 승인 전에는 2026-10-25 이후 NESO 하루 전 조류 자료를 받거나 보지 않음
3. T3 구역 선택 메모 (3구역 또는 5구역, 연구자 승인)
4. T4 2030 입력 (구역·경계 한도, 설비, 시계열, 인터커넥터)
5. T5 2단계 모형과 계획자 최적, T6 설계안 S1a·S1b·S5
6. T7 M1 결과표, T8 2025년 기본 점검, T9 go/no-go 계산 (판정은 연구자)
7. 그 뒤 M2~M5 (지시서 4장). 이전 목록의 검증 6 실행은 M4 실증 논문으로 옮김. 실행 명령(약 5~8시간, **연구자가 괜찮다고 할 때만**): `.venv/bin/python -m gbess.validation.psh_bidding`, 짧은 판(약 1시간): `--years 2022 2024 --info forecast`
8. 이전 목록의 나머지가 어디로 갔는지는 `docs/11_referee_review_KO.md` 5장 표에 있음

## 7. 반드시 지킬 것

**대화**
- 사용자에게는 **쉬운 한국어**로 답하고 전문 용어는 풀어 설명. 커밋 메시지는 영어.
- 커밋은 **사용자가 요청할 때만**. 메시지 끝: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

**git**
- 브랜치는 `claude/cool-goodall-nubbzr` 하나. 원격: https://github.com/knameds-cmd/GR_research_Grid_ESS.git
- **다른 세션(데이터 세션)의 파일은 절대 커밋하지 않음**:
  - 수정됨: `data/raw/cm_cmu.csv`, `cm_components.csv`, `eac_monthly_by_product.csv`, `eac_results_summary.csv`, `gb_data_fetch.py`
  - 추적 안 됨: `data/raw/dc_pre_eac/`, `eac_units/`, `elexon_mid/`, `elexon_system_prices/`, `neso/`, `skip_rates/`
  - `gbess/realized/tnuos.py`가 `data/raw/neso/`를 읽음. 읽기만 하고 커밋은 안 함.
  - 그래서 `git add -A` 금지. 파일을 하나씩 지정해서 add.
- PDF·txt·xlsx 원문(출판사·Ofgem·회사 자료)과 parquet은 git 제외(저작권·크기). .md/.csv 요약만 커밋.
- **푸시는 사용자가 직접**: `cd ~/GR_research_Grid_ESS && git push origin claude/cool-goodall-nubbzr`
- 사용자가 이전에 채팅에 GitHub 토큰을 붙여 넣은 적이 있음. 토큰은 어디에도 저장·재사용하지 않음(파일, git 설정, 원격 URL, 키체인 모두).

**연구**
- `model/`, `results/layer1/`, `docs/04`는 단주기 **프로토타입**. 결과 수치를 인용하지 않음.
- 숫자를 바꾸면 09 문서(해설), 10 문서(상태표·시험 개수), 11 문서(남은 일), README(시험 개수)를 같이 고침.
- 값마다 출처와 쪽(행) 번호, status(sourced/derived/placeholder)를 남김.
