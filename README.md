# GB 계통용 배터리 수익성 × 시장설계 연구

영국(GB) 시장의 어떤 상품 규칙이 계통용 배터리를 수익 사업으로 만들었고, 각 규칙이 수익성과 입찰·운전 전략을 얼마나 바꾸는지 분석한다.

## 문서

| 파일 | 내용 |
| --- | --- |
| [`docs/00_research_design_v0.md`](docs/00_research_design_v0.md) | 연구 설계 초안 원본 (2026-10-05 회의 정리) |
| [`docs/01_next_actions.md`](docs/01_next_actions.md) | 설계 검토, 경쟁 논문 확인 결과, 연구 방향 옵션, 업로드 점검표, 수정 일정 |
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

## 데이터 다시 받기

```bash
pip install requests pandas
python3 gb_data_fetch.py          # EAC 요약 + 용량시장 + Elexon 2026-09 샘플 → data/raw/
python3 gb_data_fetch.py --units  # 배터리 유닛별 EAC 결과까지 (수십만 행)
```

NESO와 Elexon API는 키 없이 무료다. 일부 클라우드 환경은 네트워크 정책 때문에 이 API에 접근하지 못할 수 있다.
