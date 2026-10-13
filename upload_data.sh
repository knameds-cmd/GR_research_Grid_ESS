#!/usr/bin/env bash
# get_data.sh로 받은 data/raw/ 를 GitHub 작업 브랜치에 올립니다. 저장소 폴더에서:
#   bash upload_data.sh
# - 20MB 넘는 CSV는 압축본(.csv.gz)을 만들어 그것을 올리고, 원본은 이 컴퓨터에만 둡니다.
# - 압축해도 90MB가 넘는 파일은 올리지 않습니다 (GitHub 한도 100MB). 이 컴퓨터의 .git/info/exclude에만 적어 둡니다.
# - 한 번에 1GB 넘게 올리려 하면 멈춥니다.
# - cm_cmu.csv에 담당자 연락처 열이 남아 있으면 멈춥니다 (공개 저장소).
set -u
cd "$(dirname "$0")" || exit 1
BRANCH=claude/cool-goodall-nubbzr
COMPRESS_MB=20
LIMIT_MB=90
MAX_TOTAL_MB=1000

CUR=$(git rev-parse --abbrev-ref HEAD) || exit 1
if [ "$CUR" != "$BRANCH" ]; then
  echo "[!] 지금 브랜치가 $CUR 입니다. 먼저 실행: git checkout $BRANCH"
  exit 1
fi
if [ -f data/raw/cm_cmu.csv ] && head -1 data/raw/cm_cmu.csv | grep -Eq 'Contact_(Telephone|Email)'; then
  echo "[!] data/raw/cm_cmu.csv에 담당자 전화번호·이메일 열이 있습니다."
  echo "    git pull origin $BRANCH 로 최신 gb_data_fetch.py를 받고 bash get_data.sh를 다시 실행하세요."
  exit 1
fi

exclude() {
  grep -qxF "/$1" .git/info/exclude 2>/dev/null || echo "/$1" >> .git/info/exclude
}
# 큰 CSV 압축 (이미 git에 올라가 있는 파일은 그대로 둠)
find data/raw -type f -name "*.csv" -size +${COMPRESS_MB}M | while IFS= read -r f; do
  git ls-files --error-unmatch "$f" >/dev/null 2>&1 && continue
  if [ ! -f "$f.gz" ] || [ "$f" -nt "$f.gz" ]; then
    echo "  압축: $f"
    gzip -c -9 "$f" > "$f.gz.part" && mv "$f.gz.part" "$f.gz" || { rm -f "$f.gz.part"; echo "[!] 압축 실패: $f"; exit 1; }
  fi
  exclude "$f"
done || exit 1
find data/raw -type f -size +${LIMIT_MB}M | while IFS= read -r f; do
  exclude "$f"
  case "$f" in *.csv) [ -f "$f.gz" ] && continue ;; esac
  echo "  올리지 않음 (${LIMIT_MB}MB 초과): $f"
done

git add data/raw || exit 1
if git diff --cached --quiet -- data/raw; then
  echo "새로 올릴 데이터가 없습니다."
  exit 0
fi
TOTAL_KB=$(git diff --cached --name-only --diff-filter=AM -z -- data/raw | xargs -0 -r du -k 2>/dev/null | awk '{s += $1} END {print s + 0}')
TOTAL_MB=$((TOTAL_KB / 1024))
echo "올릴 데이터: 약 ${TOTAL_MB} MB"
if [ "$TOTAL_MB" -gt "$MAX_TOTAL_MB" ]; then
  git reset -q -- data/raw
  echo "[!] ${MAX_TOTAL_MB} MB가 넘어 멈췄습니다. 어느 폴더가 큰지 보기: du -sh data/raw/* data/raw/neso/*"
  exit 1
fi
if ! git config user.email >/dev/null; then
  git reset -q -- data/raw
  echo "[!] git 사용자 정보가 없습니다. 아래 두 줄의 따옴표 안을 본인 정보로 바꿔 실행한 뒤 다시 하세요:"
  echo '    git config --global user.name "이름"'
  echo '    git config --global user.email "GitHub에 등록한 이메일"'
  exit 1
fi

git commit -q -m "Add raw data downloaded with get_data.sh ($(date +%Y-%m-%d))" -- data/raw || exit 1
if ! git pull -q --rebase --autostash origin "$BRANCH"; then
  echo "[!] GitHub의 새 변경과 합치지 못했습니다. 화면 내용을 Claude에게 보여 주세요."
  exit 1
fi
if git push -u origin "$BRANCH"; then
  echo "올렸습니다. Claude에게 '데이터 올렸어'라고 알려 주세요."
else
  echo "[!] push 실패. GitHub 로그인이 안 되어 있으면 아래를 실행한 뒤 bash upload_data.sh 를 다시 실행하세요:"
  echo "    brew install gh && gh auth login && gh auth setup-git"
  exit 1
fi
