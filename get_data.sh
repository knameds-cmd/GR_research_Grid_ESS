#!/usr/bin/env bash
# 연구용 공개 데이터(NESO 데이터 포털 + Elexon)를 한 번에 받습니다. 저장소 폴더에서:
#   bash get_data.sh               기본 묶음 (30분~1시간)
#   bash get_data.sh --obp         OBP(비BM 일괄발령) 자료도 받기
#   bash get_data.sh --frequency   1초 주파수 2023년 파일도 받기 (수 GB, GitHub에는 안 올라감)
# 이미 받은 파일은 건너뛰므로 끊기면 같은 명령을 다시 실행하면 이어서 받습니다.
# 진행 기록은 get_data.log에 남습니다 (문제가 생기면 이 파일 내용을 Claude에게 보여 주세요).
# 받은 뒤 GitHub에 올리기: bash upload_data.sh
set -u

# Mac이 잠자기에 들어가지 않게 (전원은 연결해 두세요)
if [ -z "${GET_DATA_AWAKE:-}" ] && command -v caffeinate >/dev/null 2>&1; then
  export GET_DATA_AWAKE=1
  exec caffeinate -i bash "$0" "$@"
fi
cd "$(dirname "$0")" || exit 1

WITH_OBP=0
WITH_FREQ=0
for a in "$@"; do
  case "$a" in
    --obp) WITH_OBP=1 ;;
    --frequency) WITH_FREQ=1 ;;
    *) echo "모르는 옵션: $a (쓸 수 있는 것: --obp --frequency)"; exit 2 ;;
  esac
done

exec > >(tee -a get_data.log) 2>&1
echo "===== $(date '+%Y-%m-%d %H:%M:%S') bash get_data.sh $* ====="

if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] python3가 없습니다. https://www.python.org/downloads/ 에서 설치한 뒤 다시 실행하세요."
  exit 1
fi
if python3 -c "import requests, pandas" >/dev/null 2>&1; then
  PY=python3
else
  echo "requests·pandas 설치 (.venv 폴더, 처음 한 번만 몇 분 걸림)"
  [ -x .venv/bin/python ] || python3 -m venv .venv || { echo "[!] 가상환경(.venv)을 만들지 못했습니다."; exit 1; }
  if ! .venv/bin/python -c "import requests, pandas" >/dev/null 2>&1; then
    .venv/bin/python -m pip install -q requests pandas || { echo "[!] 설치 실패. 인터넷 연결을 확인하세요."; exit 1; }
  fi
  PY=.venv/bin/python
fi
echo "Python: $("$PY" --version 2>&1)"
export PYTHONUNBUFFERED=1  # 진행 상황을 바로 화면에 보여 주기

FAILED=""
run() {
  echo
  echo ">>> $*"
  if ! "$PY" "$@"; then
    FAILED="$FAILED
  - $*"
  fi
}

# 작업마다 따로 실행해서 하나가 실패해도 나머지는 계속 받는다
run gb_data_fetch.py --only eac,cm                       # EAC 요약, 용량시장 등록부
run gb_data_fetch.py --only units                        # 배터리 유닛별 EAC 결과 (수십만 행)
run gb_data_fetch.py --only dc                           # EAC 이전 DC 결과 (호황기)
run gb_data_fetch.py --only skip                         # BM skip rate
run gb_data_fetch.py --only prices --start 2021-09-01    # MID·정산가격 월별 (가장 오래 걸림)
run neso_fetch.py get core requirements drivers costs history
if [ "$WITH_OBP" = 1 ]; then
  run neso_fetch.py get obp
fi
if [ "$WITH_FREQ" = 1 ]; then
  run neso_fetch.py get system-frequency-data --match 2023 --allow-large
fi

echo
echo "===== 끝 $(date '+%Y-%m-%d %H:%M:%S') ====="
du -sh data/raw 2>/dev/null
BIG=$(find data/raw -type f -size +90M ! -name "*.csv" 2>/dev/null)
if [ -n "$BIG" ]; then
  echo "90MB가 넘는 CSV 아닌 파일 (upload_data.sh가 GitHub에는 올리지 않습니다):"
  echo "$BIG" | sed 's/^/  /'
fi
echo "20MB가 넘는 CSV는 upload_data.sh가 압축(.csv.gz)해서 올립니다."
if [ -n "$FAILED" ]; then
  echo "[!] 실패한 작업:$FAILED"
  echo "같은 명령(bash get_data.sh)을 다시 실행하면 받은 것은 건너뛰고 나머지만 받습니다."
  echo "계속 실패하면 get_data.log 내용을 Claude에게 보여 주세요."
  exit 1
fi
echo "모두 받았습니다. GitHub에 올리려면: bash upload_data.sh"
