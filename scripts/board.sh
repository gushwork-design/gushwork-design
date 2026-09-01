#!/usr/bin/env bash
# Regenerate preview/board.html — the backlog as a board plus a shipped timeline.
#
# DERIVED from BACKLOG.md, which is the one hand-written source in this repo. Rendering
# lives in `scripts/_board.py`. Edit the markdown, not the HTML; the next run overwrites it.
#
# WHY THERE IS NO BASH DERIVATION HERE. Every other generator splits the work — bash derives
# from git, python renders (see changelog-sheet.sh). A backlog has nothing to derive from:
# priorities are human input, so the source is a file and this script only pipes it through.
# The split is kept in the filenames so the pattern still reads the same from the outside.
#
# BOTH FILES ARE GITIGNORED. The repo is public; the backlog is not. This script is safe to
# commit, its input and output are not — see .gitignore and the note atop BACKLOG.md.
#
# Usage:  bash scripts/board.sh          # rewrite the board
#         bash scripts/board.sh --check  # exit 1 if it is out of date
#         bash scripts/board.sh --open   # rewrite, then open it
#         bash scripts/board.sh --waiting # print the decision queue; exit 1 if it is empty
#
# `--waiting` is what the notifiers read. Both the Stop hook and the morning digest go
# through it rather than grepping the markdown, so there is one parser and not three.
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="BACKLOG.md"
OUT="preview/board.html"

[ -f "$SRC" ] || { echo "$SRC is missing — nothing to render." >&2; exit 1; }

build() { OUT="$OUT" python3 scripts/_board.py < "$SRC"; }

case "${1:-}" in
  --waiting)
    exec python3 scripts/_board.py --waiting < "$SRC"
    ;;
  --check)
    if ! diff -q <(build 2>/dev/null) "$OUT" >/dev/null 2>&1; then
      echo "$OUT is out of date — run: bash scripts/board.sh" >&2
      exit 1
    fi
    echo "$OUT is current."
    ;;
  --open)
    build > "$OUT"
    open "$OUT"
    ;;
  *)
    build > "$OUT"   # the renderer reports the filename and counts on stderr
    ;;
esac
