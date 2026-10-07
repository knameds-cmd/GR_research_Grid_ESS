import os,re,sys,collections,datetime
# Regenerate literature/INDEX.md from papers/*.md metadata.
# Usage (from repo root): python3 literature/tools/gen_index.py literature
root=sys.argv[1]; d=os.path.join(root,'papers')
names={'S1_foundations_value':'S1 저장장치 가치·경제성 기초','S2_stacking_cooptimization':'S2 다중서비스 공동최적화(수익 스택)',
'S3_bidding_uncertainty':'S3 불확실성 하 입찰(SP/RO/SDP/가격결정자)','S4_degradation_operation':'S4 열화·물리 모델링',
'S5_rl_learning':'S5 강화학습·학습 기반 입찰','S6_ancillary_products':'S6 보조서비스 상품 설계와 배터리',
'S7_market_design':'S7 저장장치 시장설계·규제','S8_empirical_econ':'S8 실증·계량경제'}
rows=[]
for fn in sorted(os.listdir(d)):
    s=open(os.path.join(d,fn),encoding='utf-8').read()
    g=lambda k: (re.search(r'^'+k+r':\s*(.*)$',s,re.M) or [None,''])[1].strip().strip('"')
    st=re.findall(r'S\d_[a-z_]+',g('streams'))
    qb=g('quartile_basis'); basis=qb.split(';')[0].strip(); m=re.search(r'rule=(\w+)',qb); rule=m.group(1) if m else 'unchecked'
    if rule=='FAIL': Q='Q2!'
    elif rule=='unchecked': Q='Q1?'
    elif basis=='pub-year': Q='Q1'
    else: Q='Q1~'
    ev=g('evidence_read').lower()
    E='full' if ev.startswith('full') else ('partial' if ev.startswith('partial') else 'abstract')
    rows.append(dict(id=fn[:-3],y=int(g('year')),j=g('journal'),Q=Q,m=g('method_class')[:40],c=g('market_context')[:50],E=E,st=st,comp=bool(g('competitor'))))
n=len(rows); ec=collections.Counter(r['E'] for r in rows); qc=collections.Counter(r['Q'] for r in rows)
out=[]
out.append('# 논문 아카이브 인덱스\n')
today=datetime.date.today().isoformat()
out.append(f'총 {n}편 ({today} 생성). 한 논문이 여러 갈래에 걸치면 각 갈래 표에 모두 나옵니다. 이 파일은 `tools/gen_index.py`가 `papers/*.md` 메타데이터에서 생성하므로 직접 고치지 말고 논문 파일을 고친 뒤 다시 생성하세요.\n')
out.append('- 각 논문 파일: `papers/<id>.md` (YAML 메타데이터 + 11개 섹션: 질문, 가정, 제약, 모델, 데이터·가공, 정당화, 결과, 한계, 관련성, 계보, 검증기록)')
out.append('- 갈래별 종합: `streams/S*.md` (개관, 계보, 그룹, 요약표, 공백)')
out.append('- 연구 그룹·사제 계보: `GROUPS.md` / 교과서·랜드마크 리뷰: `CANON.md` / 내 연구의 위치: `LINEAGE.md`')
out.append('- **경쟁·프리프린트 추적**: `WATCHLIST.md` (Q1 규칙 적용 안 함) / **내려받을 영국 핵심 논문**: `DOWNLOAD_LIST.md` / **영국 시장 변천사**: `context/`\n')
out.append('## 분위 판정 규칙 (2026-10-07 통일)\n')
out.append('**SJR(Scimago) 기준, 발행연도(권호 연도)의 분위. 발행연도 SJR이 아직 없거나(2026년 논문) 저널 창간 직후라 순위가 없으면 가장 가까운 연도를 쓴다. 발행연도 값을 확인하지 못했더라도 바로 앞뒤 해(±1년)가 모두 Q1로 확인되면 통과로 본다(bracketed). 저널이 여러 분야에 걸치면 가장 높은 분야의 분위를 쓴다.** 각 파일의 `quartile_basis` 필드에 판정 근거가 있습니다.\n')
out.append('| 표기 | 뜻 | 편수 |\n|---|---|---|')
out.append(f"| `Q1` | 발행연도 Q1 확인 (해당 파일 또는 같은 저널·같은 연도를 확인한 다른 아카이브 파일) | {qc['Q1']} |")
out.append(f"| `Q1~` | 가장 가까운 연도(발행연도 순위 없음) 또는 앞뒤 해(±1년) 모두 Q1로 확인 | {qc['Q1~']} |")
out.append(f"| `Q1?` | **발행연도(또는 가장 가까운 연도) 미확인** — 이후 연도만 확인했거나 전혀 확인 못 함 (SJR 사이트가 세션에서 막혀 재확인 못 함) | {qc['Q1?']} |")
out.append(f"| `Q2!` | **규칙 미달**: 발행연도(또는 가장 가까운 연도) Q2 (`provisional` 표시는 분야별 확인이 덜 된 경우) | {qc['Q2!']} |\n")
out.append('2026-10-06 독립 검증에서 표본 24편 서지·12개 저널 등급을 재확인했습니다. 이전 표기 `Q1*`(2026-10-06)는 위 4단계로 대체했습니다. `근거`: full = 전문(프리프린트·저자본 포함), partial = 일부 전문, abstract = 초록·메타데이터만(심층 필드는 "(from abstract)" 표시).\n')
out.append(f"근거 수준 분포: full {ec['full']}편, partial {ec['partial']}편, abstract {ec['abstract']}편\n")
fails=[r for r in rows if r['Q']=='Q2!']; unch=[r for r in rows if r['Q']=='Q1?']
out.append('### 규칙 미달 `Q2!` — 남길지 결정 필요\n')
for r in fails: out.append(f"- [{r['id']}](papers/{r['id']}.md) ({r['y']}, {r['j']})")
out.append('\n### 발행연도 미확인 `Q1?` — SJR 접근 가능할 때 재확인\n')
out.append(', '.join(f"[{r['id']}](papers/{r['id']}.md)" for r in unch)+'\n')
for key,title in names.items():
    rs=sorted([r for r in rows if key in r['st']],key=lambda r:(r['y'],r['id']))
    out.append(f'## {title} ({len(rs)}편)\n')
    out.append('| id | 연도 | 저널 | Q | 방법 | 맥락 | 근거 |\n|---|---|---|---|---|---|---|')
    for r in rs:
        star=' ★경쟁' if r['comp'] else ''
        out.append(f"| [{r['id']}](papers/{r['id']}.md){star} | {r['y']} | {r['j']} | {r['Q']} | {r['m'].replace('|','/')} | {r['c'].replace('|','/')} | {r['E']} |")
    out.append('')
open(os.path.join(root,'INDEX.md'),'w',encoding='utf-8').write('\n'.join(out))
print(n,ec,qc)
