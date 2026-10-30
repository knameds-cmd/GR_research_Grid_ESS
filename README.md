# GB 계통용 배터리 수익성 × 시장설계 연구

영국(GB) 시장의 어떤 상품 규칙이 계통용 배터리를 수익 사업으로 만들었고, 각 규칙이 수익성과 입찰·운전 전략을 얼마나 바꾸는지 분석한다.

## 처음이라면 여기부터

> **2026-10-24: 연구 중심이 장주기(LDES, 8시간 이상)로 바뀌었습니다** (교수님 지침). 12/10 일정에 맞출 필요는 없어졌습니다.

0. **[`docs/10_study_path_KO.md`](docs/10_study_path_KO.md)**: 학습 경로. 지금 어디까지 왔는지, 어떤 문서를 어떤 순서로 읽고 무엇을 직접 돌려 보고 어떤 질문에 답할 수 있어야 하는지
1. **[`docs/08_ldes_redesign_KO.md`](docs/08_ldes_redesign_KO.md)**: 장주기 중심 재설계. 질문, 두 층(실증·구조) 방법, "이전에 없던 규칙"을 비교하는 법, 확정한 결정
2. **[`docs/09_model_explained_KO.md`](docs/09_model_explained_KO.md)**: 모델 해설. 손계산 예제로 실제 수익 재구성, 운전 엔진(BM 층, 채택 모형, 예비력, 망요금, 기동 비용, 가상 자산의 입찰 규칙), 기술·비용 입력과 cap-and-floor 재무층, 검증 실험 1~6, 결산서 대조를 설명
3. **[`docs/11_referee_review_KO.md`](docs/11_referee_review_KO.md)**: 독립 심사 기록(2026-10-29). 이 모델이 학술 비판을 견디는지, 영국 시장 규칙 분석에 맞는지에 대한 판정, 지적별 확인·수정·남은 일
4. [`docs/07_decisions_and_build_KO.md`](docs/07_decisions_and_build_KO.md): 확정할 것과 구현 차이, 정밀한 연구 환경, 허점 점검표
5. [`docs/05_method_assessment_KO.md`](docs/05_method_assessment_KO.md), [`docs/06_project_roadmap_KO.md`](docs/06_project_roadmap_KO.md): 단주기 기준의 이전 판단과 로드맵 (장주기 전환 전)

> **새 모델은 `gbess/`입니다.** `model/`과 `results/layer1/`은 단주기 프로토타입입니다. 다시 설계해 만들 예정이므로 결과 수치는 인용하지 마세요(05 문서 7장).

## 문서

| 파일 | 내용 |
| --- | --- |
| [`docs/10_study_path_KO.md`](docs/10_study_path_KO.md) | **학습 경로**: 현재 상태표, 문서 지도(유효/지난 문서), 4단계 학습과 자가 점검 질문, 코드 흐름, 자주 묻는 질문(장주기 자산 현황, 예비력과 모델) |
| [`docs/08_ldes_redesign_KO.md`](docs/08_ldes_redesign_KO.md) | **장주기 재설계**: 영국 LDES 제도 사실, 규칙 4유형(F·C·P·M)과 비교 방법, 실증층 2016-09~2026-09 + 구조층 미래 × 기상연도, 바뀌는 구현, 확정한 결정 |
| [`docs/09_model_explained_KO.md`](docs/09_model_explained_KO.md) | **모델 해설**: 실제 수익 재구성(PN·BM 지시·현금흐름), 운전 엔진과 정보 수준, BM 층·채택 모형·예비력 보유·망요금(BSUoS·TNUoS)·기동 비용·입찰 규칙(단가 띠), 기술·비용 입력(Window 1 대표 자산, 세 경우), cap-and-floor 재무층(Ofgem 정산 규칙), 검증 실험 1~6, 결산서 대조, 손계산 예제 |
| [`docs/11_referee_review_KO.md`](docs/11_referee_review_KO.md) | **독립 심사 기록**: 판정(학술 비판, 규칙 분석 적합성), 주요 지적 9개와 우려 9개의 확인·수정·남은 일, 말할 수 있는 것과 못 하는 것, 다음 작업 순서 |
| [`literature/sources/psh/PSH_SOURCES.md`](literature/sources/psh/PSH_SOURCES.md) | 양수발전 수입원과 출처: MFR, Fast Reserve 계약 전체, 무효전력, 결산서(First Hydro, Cruachan 단독), 물리 매개변수 |
| [`docs/07_decisions_and_build_KO.md`](docs/07_decisions_and_build_KO.md) | 확정할 것과 결정별 구현 차이, 오늘 확인한 데이터 사실 F1~F7, 정밀 환경 E1~E7, 허점 점검표 H1~H13 |
| [`literature/sources/ldes/FACTS.md`](literature/sources/ldes/FACTS.md) | Ofgem LDES cap-and-floor 제도 사실 정리 (기술결정문, Window 1 잠정결정, NERA 비평, 쪽 번호 포함) |
| [`docs/06_project_roadmap_KO.md`](docs/06_project_roadmap_KO.md) | **로드맵**: 결정 D1~D7, 학습할 개념, 재확인할 사실, 있는/없는 데이터, 단계별 할 일과 완료 기준, 위험, 축소안 |
| [`docs/05_method_assessment_KO.md`](docs/05_method_assessment_KO.md) | **방법론 판단**: 수익성의 네 단계, 규칙 스위치와 국면 분할의 유효 조건, 장주기 ESS, 선로·위치 모델링, 규칙·상황 귀속과 오류 |
| [`docs/00_research_design_v0.md`](docs/00_research_design_v0.md) | 연구 설계 초안 원본 (2026-10-05 회의 정리) |
| [`docs/01_next_actions.md`](docs/01_next_actions.md) | 설계 검토, 경쟁 논문 확인 결과, 연구 방향 옵션, 업로드 점검표, 수정 일정 |
| [`docs/03_competitor_analysis_KO.md`](docs/03_competitor_analysis_KO.md) | **경쟁·선행 논문 3편 전문 분석**(Gale 2026, Landy 2026, Martins & Miles 2021): 그들이 한 것 / 안 한 것 / 우리가 다른 점, 설계에 반영할 것 |
| [`docs/meeting/2026-10-13_research_meeting_EN.pptx`](docs/meeting/2026-10-13_research_meeting_EN.pptx) | 연구 미팅용 영어 슬라이드 3장: 연구 주제와 목표, GB 시장 국면(Phase), 모델링 선택과 근거 |
| [`docs/meeting/2026-10-13_professor_meeting_brief_KO.pdf`](docs/meeting/2026-10-13_professor_meeting_brief_KO.pdf) | 교수님 미팅용 연구 진행 보고 (9쪽): 연구 질문과 방향, 영국 시장과 배터리, 모델링과 근거, 첫 결과, 선행 연구 비교, 일정, 예상 쟁점 |
| [`docs/04_layer1_model_KO.md`](docs/04_layer1_model_KO.md) | **층 1 모델 해설**: 배터리 입장에서 본 영국 시장 구조와 각 규칙의 이유, 변수·제약 하나씩, 2026년 9월 첫 결과, 규칙 스위치와 Shapley 예시 |
| [`docs/02_study_guide_KO.md`](docs/02_study_guide_KO.md) | **연구자 학습 가이드**: 영국 시장 핵심 개념 11개, 논문 아카이브 읽는 법과 필독 16편, 주제 연결 지도(다리 16개), 연습·자가 점검 질문, 용어집 |
| [`data/README.md`](data/README.md) | 받은 데이터 12개 파일 해설: 구조·기간·품질·연결 키, 첫 계산 결과, 할 수 있는 분석 |
| [`data/recommendations.md`](data/recommendations.md) | 추가로 받을 데이터와 참고 데이터 (존재 확인한 데이터셋 이름·엔드포인트 포함) |
| [`literature/INDEX.md`](literature/INDEX.md) | 논문 아카이브 색인 (114편, 8개 갈래, 분위 판정 규칙) |
| [`literature/LINEAGE.md`](literature/LINEAGE.md) | 계보 지도: 이 연구의 위치, 유사 연구의 모델링 방식 비교, 가능한 연구 방향 |
| [`literature/WATCHLIST.md`](literature/WATCHLIST.md) | 경쟁 논문·프리프린트 추적 (Q1 규칙 적용 안 함) |
| [`literature/DOWNLOAD_LIST.md`](literature/DOWNLOAD_LIST.md) | 내려받을 영국 핵심 논문 25편 (우선순위·DOI·오픈액세스 여부) |
| [`literature/context/GB_market_history_KO.md`](literature/context/GB_market_history_KO.md) | 영국 전력시장 구조 변천사와 배터리 (2010 → 2026.10), 한글 해설 |
| [`literature/context/GB_market_history_EN.md`](literature/context/GB_market_history_EN.md) | 같은 내용의 상세판 (사건 70여 개 표, 상품 사양, 용량시장, 출처·신뢰도) |

## 폴더

| 폴더 | 용도 |
| --- | --- |
| `docs/` | 설계·계획·메모 |
| `literature/` | 논문 아카이브(.md). `papers/`에 논문 1편당 파일 1개(가정·제약·모델·데이터 가공·정당화), `streams/`에 갈래별 종합, `GROUPS.md` 연구 그룹·사제 계보, `CANON.md` 교과서·랜드마크 리뷰 |
| `data/raw/` | 원자료 CSV (NESO EAC 경매, 용량시장 등록부, Elexon 2026-09 샘플). 약 33MB |
| `data/processed/` | 가공본 (git 제외) |
| `gbess/` | **새 모델 패키지**: 데이터 받기(`fetch/`), 가격·유닛·계통 상태(`data/`), 실제 수익 재구성(`realized/`), BM 채택 모형(`model/`), 운전 엔진(`engine/`), 검증(`validation/`), 재무층(`finance/`), 기술·비용 매개변수(`config/`, 출처는 `literature/sources/tech/TECH_SOURCES.md`). 해설은 `docs/09`, 읽는 순서는 `docs/10` |
| `tests/` | `gbess` 시험 62개 (손계산 예제, 불변식). `.venv/bin/python -m pytest -q tests` |
| `results/realized/` | 양수발전 실제 수익 패널 (도매, BM, BSUoS, TNUoS 추정, 거래 밖 수입) |
| `results/validation/` | 엔진 검증 1~5, 채택 모형 검증, 결산서 대조 (검증 6은 스크립트만, 아직 돌리지 않음) |
| `model/` | **(단주기 프로토타입)** 층 1 완전예측 MILP (`data.py` 입력, `layer1.py` 모델). 실행은 루트의 `run_layer1.py`. 재구축 예정 |
| `results/layer1/` | **(프로토타입)** 모델 결과: 시나리오별 수익 `summary.csv`, 30분 운전 계획 `*_dispatch.csv` |

## 데이터 받기

**가장 쉬운 방법 (Mac 터미널에 그대로 붙여넣기).** 홈 폴더에 저장소를 받고(이미 있으면 최신으로 바꾸고) 필요한 데이터를 모두 받습니다. 30분~1시간 걸리니 전원을 연결해 두세요. 진행 기록은 `get_data.log`에 남습니다.

```bash
cd ~ &&
{ [ -d GR_research_Grid_ESS ] || git clone https://github.com/knameds-cmd/GR_research_Grid_ESS.git; } &&
cd GR_research_Grid_ESS &&
git fetch -q origin claude/cool-goodall-nubbzr &&
git checkout -q claude/cool-goodall-nubbzr &&
git pull -q --ff-only origin claude/cool-goodall-nubbzr &&
bash get_data.sh
```

다 받은 뒤 GitHub에 올리기 (20MB 넘는 CSV는 .csv.gz로 압축해 올리고, 압축해도 90MB가 넘는 파일은 뺍니다):

```bash
cd ~/GR_research_Grid_ESS && bash upload_data.sh
```

`get_data.sh`는 아래 두 스크립트를 차례로 실행합니다. 따로 실행할 때는 아래 명령을 쓰세요. 두 스크립트가 받는 자료는 겹치지 않고, 둘 다 저장소 루트에서 실행합니다.

**`gb_data_fetch.py`**: EAC 요약·유닛별 결과, EAC 이전 DC, skip rate, 용량시장 등록부, Elexon MID·정산가격과 2026-09 샘플(Lakeside 배터리). 결과는 `data/raw/`. 묶음과 기간 옵션은 `data/README.md` 6장.

```bash
pip install requests pandas
python3 gb_data_fetch.py                                          # EAC 요약 + 용량시장 + Elexon 2026-09 샘플
python3 gb_data_fetch.py --only units,dc,prices,skip --start 2021-09-01   # 유닛별 EAC, EAC 이전 DC, 가격 장기 시계열, skip rate
```

**`neso_fetch.py`**: 위 스크립트에 없는 나머지 NESO 데이터 포털 자료를 묶음으로 정리해 두었습니다. 받은 파일은 `data/raw/neso/<데이터셋>/`, 받은 내역은 `data/raw/neso/MANIFEST.csv`에 남습니다.

```bash
python3 neso_fetch.py list                       # 묶음·데이터셋 목록
python3 neso_fetch.py list core requirements     # 각 데이터셋의 파일·크기 확인
python3 neso_fetch.py get core requirements --dry-run   # 받을 것 미리 보기
python3 neso_fetch.py get core requirements      # 1순위: 2025.10 이전 BR, 상품별 필요량
python3 neso_fetch.py get drivers costs obp history     # 설명변수(관성·수요·풍력), 망요금, OBP, FFR/EFR 보고서
python3 neso_fetch.py get system-frequency-data --match 2023 --allow-large   # 1초 주파수 (큼, 기간 골라서)
python3 neso_fetch.py search "dynamic moderation"       # 포털에서 다른 데이터셋 찾기 → get <이름>
```

데이터셋 이름을 못 찾으면 비슷한 이름을 보여 줍니다. 200 MB보다 큰 파일은 `--allow-large`를 붙여야 받습니다. 두 스크립트 모두 이미 받은 파일은 건너뛰므로 끊겨도 다시 실행하면 이어서 받습니다. 1초 주파수 폴더와 `.part` 파일은 git에서 제외되며, 100 MB가 넘는 파일은 GitHub에 올라가지 않으니 커밋하지 마세요.

NESO와 Elexon API는 키 없이 무료입니다. 클라우드 세션에서는 네트워크 정책 때문에 접근이 막힐 수 있으니 본인 컴퓨터에서 실행하세요.
