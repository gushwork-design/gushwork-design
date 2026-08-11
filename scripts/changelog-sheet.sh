#!/usr/bin/env bash
# Regenerate preview/changelog-sheet.html — the changelog as a rendered sheet.
#
# DERIVED, never hand-written, from the same source as every other release view:
# `scripts/_releases.sh`, which reads the version field out of `.claude-plugin/plugin.json`
# at every commit that moved it. Rendering lives in `scripts/_changelog_sheet.py` — bash
# derives, python renders. Edit those, not the HTML; the next run overwrites it.
#
# The sheet was a table until 11 Aug 2026 and is now a reading page — see the layout note
# at the top of the python file. Light theme only, by instruction.
#
# Usage:  bash scripts/changelog-sheet.sh          # rewrite the sheet
#         bash scripts/changelog-sheet.sh --check  # exit 1 if it is out of date
set -euo pipefail
cd "$(dirname "$0")/.."
. scripts/_releases.sh

OUT="preview/changelog-sheet.html"

build() {
  # How far behind the subject-derived markdown log is. Counted, not asserted, so the note
  # cannot go stale if changelog.sh is ever changed.
  local md_rows
  md_rows="$(grep -c '^| \*\*v' CHANGELOG.md 2>/dev/null || echo 0)"
  releases | REPO="$REPO" MD_ROWS="$md_rows" python3 scripts/_changelog_sheet.py
}

if [ "${1:-}" = "--check" ]; then
  if ! diff -q <(build) "$OUT" >/dev/null 2>&1; then
    echo "$OUT is out of date — run: bash scripts/changelog-sheet.sh" >&2
    exit 1
  fi
  echo "$OUT is current."
else
  build > "$OUT"
  echo "Wrote $OUT — $(grep -c '<article class="rel"' "$OUT") releases."
fi
