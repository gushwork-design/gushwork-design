#!/usr/bin/env bash
# Regenerate CHANGELOG.md from git history.
#
# The log is DERIVED, never hand-written — so it cannot drift from what actually shipped.
# A row appears for every commit whose subject starts `vX.Y.Z`. The subject after the dash
# is the one-line summary, so write release subjects accordingly.
#
# The "Session" column comes from a `Session:` trailer on the release commit:
#
#     git commit -m "v1.27.0 — what changed
#
#     ...body...
#
#     Session: GW Design Associate"
#
# Chat sessions are machine-local and have no shareable URL, so the trailer holds the
# session TITLE — enough for Utsav to find the right conversation, meaningless to leak.
# Never put a session id, transcript path or chat content in here: the repo is public.
#
# Usage:  bash scripts/changelog.sh          # rewrite CHANGELOG.md
#         bash scripts/changelog.sh --check  # exit 1 if it is out of date
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="https://github.com/utsav-gushwork/gushwork-design"

build() {
  cat <<'HEAD'
# Changelog

Every released version, newest first. **Generated from git history** by
`scripts/changelog.sh` — do not edit by hand, the next release will overwrite it.

`Session` is the chat the change came from. Chat sessions are machine-local and have no
shareable link, so this is the session's title, recorded as a `Session:` trailer on the
release commit. If it is blank, the release predates the convention.

To check what you are running: the skill announces its own version and date at the start of
every session. Trust that line over memory — it is stamped into the file, so **a stale copy
reports its own stale date.**

HEAD

  printf '| Version | Date | What changed | Commit | Session |\n'
  printf '|---|---|---|---|---|\n'

  # One record per line, fields split on US (0x1f). Trailers are single-line by
  # construction, so newline stays a safe record separator.
  git log --format='%H%x1f%ad%x1f%s%x1f%(trailers:key=Session,valueonly,separator=%x2c)' \
          --date=format:'%d %b %Y %H:%M' \
  | while IFS=$'\x1f' read -r sha date subject session; do
      [ -z "${sha:-}" ] && continue
      case "$subject" in
        v[0-9]*)
          version="${subject%% *}"
          summary="${subject#* — }"
          [ "$summary" = "$subject" ] && summary="${subject#"$version" }"
          printf '| **%s** | %s | %s | [`%s`](%s/commit/%s) | %s |\n' \
            "$version" "$date" "$summary" "${sha:0:7}" "$REPO" "$sha" "${session:-—}"
          ;;
      esac
    done
}

if [ "${1:-}" = "--check" ]; then
  if ! diff -q <(build) CHANGELOG.md >/dev/null 2>&1; then
    echo "CHANGELOG.md is out of date — run: bash scripts/changelog.sh" >&2
    exit 1
  fi
  echo "CHANGELOG.md is current."
else
  build > CHANGELOG.md
  echo "Wrote CHANGELOG.md — $(grep -c '^| \*\*v' CHANGELOG.md) releases."
fi
