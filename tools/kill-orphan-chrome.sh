#!/bin/sh
# 띄운 쪽이 죽어 주인 없이 남은 헤드리스 Chrome(뷰어 테스트 · 스크린샷 스크립트가 남긴 것)을 끈다.
# 남은 헤드리스가 사용자 Chrome 과 Chrome Services 를 같이 써서, 사용자 Chrome 이 느려지거나 헤드리스만 앞으로 불렀다.
#
#   tools/kill-orphan-chrome.sh             끈다
#   tools/kill-orphan-chrome.sh --dry-run   끌 것만 찍는다
#
# 끄는 것은 셋을 모두 만족하는 Chrome 본체(--type= 이 없는 프로세스)뿐이다 — 이름이나 포트만으로는 끄지 않는다.
#   ① 명령줄에 --headless  ② --user-data-dir 가 $TMPDIR 아래  ③ 부모가 launchd(PPID 1) — 띄운 스크립트가 이미 죽었다
# 그래서 창이 있는 사용자 Chrome, 사용자 프로필, 부모가 살아 있는 다른 세션의 테스트 Chrome 은 남는다.
# 끈 줄마다 `PID 프로필` 한 줄을 찍는다. 도우미 프로세스는 본체를 따라 내려간다.
set -eu

DRY=0
case "${1:-}" in
  "") ;;
  --dry-run) DRY=1 ;;
  *) echo "사용: $0 [--dry-run]" >&2; exit 2 ;;
esac

TMP="${TMPDIR:-/tmp}"
TMP="${TMP%/}"
[ -d "$TMP" ] || { echo "TMPDIR 이 없다: $TMP" >&2; exit 2; }
# macOS 의 /var 는 /private/var 의 링크라 명령줄에는 어느 쪽으로도 적힐 수 있다.
REAL="$(cd "$TMP" && pwd -P)"

# 조건 셋을 만족하는 줄만 `PID 프로필` 로 찍는다.
orphans() {
  ps -axww -o pid= -o ppid= -o command= | awk -v tmp="$TMP/" -v real="$REAL/" '
    $2 != 1 { next }
    {
      cmd = $0
      sub(/^[ \t]*[0-9]+[ \t]+[0-9]+[ \t]+/, "", cmd)
      if (cmd ~ / --type=/) next
      if (cmd !~ / --headless(=| |$)/) next
      if (!match(cmd, / --user-data-dir=[^ ]+/)) next
      dir = substr(cmd, RSTART + 17, RLENGTH - 17)
      if (index(dir, tmp) != 1 && index(dir, real) != 1) next
      print $1, dir
    }' | while read -r PID DIR; do
    # 실행 파일로 가린다 — 명령줄은 Chrome 을 띄운 셸(`sh -c "…/Google Chrome" --headless …`)에도 같은 글자가 있다.
    case "$(ps -o comm= -p "$PID" 2>/dev/null)" in
      # macOS 는 전체 경로, Linux 는 이름만 찍는다.
      */"Google Chrome"|*/"Google Chrome for Testing"|*/Chromium|*/chromium|*/chrome|*/headless_shell|chrome|chromium|headless_shell) echo "$PID $DIR" ;;
    esac
  done
}

LIST="$(orphans)"
[ -n "$LIST" ] || exit 0

echo "$LIST" | while read -r PID DIR; do
  if [ "$DRY" = 1 ]; then echo "끌 것 $PID $DIR"; continue; fi
  kill -TERM "$PID" 2>/dev/null || continue
  # TERM 에 3초 안에 내려가지 않으면 KILL — 도우미가 붙잡고 있으면 가끔 남는다.
  n=0
  while kill -0 "$PID" 2>/dev/null && [ "$n" -lt 30 ]; do sleep 0.1; n=$((n + 1)); done
  kill -0 "$PID" 2>/dev/null && kill -KILL "$PID" 2>/dev/null
  echo "끔 $PID $DIR"
done
