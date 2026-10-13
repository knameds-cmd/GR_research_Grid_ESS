# GB 계통용 배터리 수익성 × 시장설계 연구

영국(GB) 시장의 어떤 상품 규칙이 계통용 배터리를 수익 사업으로 만들었고, 각 규칙이 수익성과 입찰·운전 전략을 얼마나 바꾸는지 분석한다.

## 문서

| 파일 | 내용 |
| --- | --- |
| [`docs/00_research_design_v0.md`](docs/00_research_design_v0.md) | 연구 설계 초안 원본 (2026-10-05 회의 정리) |
| [`docs/01_next_actions.md`](docs/01_next_actions.md) | 설계 검토, 경쟁 논문 확인 결과, 연구 방향 옵션, 업로드 점검표, 수정 일정 |
| [`docs/03_competitor_analysis_KO.md`](docs/03_competitor_analysis_KO.md) | **경쟁·선행 논문 3편 전문 분석**(Gale 2026, Landy 2026, Martins & Miles 2021): 그들이 한 것 / 안 한 것 / 우리가 다른 점, 설계에 반영할 것 |
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

다 받은 뒤 GitHub에 올리기 (50MB 넘는 파일은 빼고 올립니다):

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
