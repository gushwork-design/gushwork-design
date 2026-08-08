#!/usr/bin/env bash
# Regenerate CHANGELOG.md from git history.
#
# The log is DERIVED, never hand-written — so it cannot drift from what actually shipped.
# A row appears for every commit whose subject starts `vX.Y.Z`. The subject after the dash
# is the one-line summary, so write release subjects accordingly.
#
# The "Session" column comes from a `Session:` trailer on the release commit —
# the session uuid, then the title:
#
#     git commit -m "v1.27.0 — what changed
#
#     ...body...
#
#     Session: 5a7c696b-5bbf-4aee-adf8-603e744f9018 Gushwork Design System plugin"
#
# It renders as a claude://resume/<uuid> deep link, which reopens that conversation in
# the desktop app. The link only resolves on the machine holding the transcript — it is
# a pointer for the maintainer, not something a teammate can follow.
#
# Never put chat CONTENT in here. The uuid and title are opaque and safe; the transcript
# is not, and this repo is public.
#
# Usage:  bash scripts/changelog.sh          # rewrite CHANGELOG.md
#         bash scripts/changelog.sh --check  # exit 1 if it is out of date
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="https://github.com/utsav-gushwork/gushwork-design"

# Releases that predate the Session: trailer. Attribution is first-hand only —
# transcript greps are unreliable because forked sessions duplicate each other's
# history, so a mention reads as authorship. Anything not listed stays blank.
backfill() {
  case "$1" in
    v1.21.0|v1.22.0|v1.23.0|v1.24.0|v1.24.1|v1.27.0)
      echo "5a7c696b-5bbf-4aee-adf8-603e744f9018 Gushwork Design System plugin" ;;
    v1.19.0|v1.25.0|v1.26.0)
      echo "5eeaa384-81a5-460f-8fff-20a987090035 Website performance dashboard" ;;
    *) echo "" ;;
  esac
}

# "<uuid> <title>" -> a markdown deep link. Bare titles (no uuid) render as plain text.
session_cell() {
  local raw="${1:-}"
  [ -z "$raw" ] && { printf '—'; return; }
  local uuid="${raw%% *}" title="${raw#* }"
  case "$uuid" in
    [0-9a-f]*-[0-9a-f]*-*) printf '[%s](claude://resume/%s)' "$title" "$uuid" ;;
    *) printf '%s' "$raw" ;;
  esac
}

build() {
  cat <<'HEAD'
# Changelog

Every released version, newest first. **Generated from git history** by
`scripts/changelog.sh` — do not edit by hand, the next release will overwrite it.

`Session` is the chat the change came from — a `claude://resume/<uuid>` deep link that
reopens that conversation in the Claude desktop app, recorded as a `Session:` trailer on
the release commit.

**The link only resolves on the machine holding the transcript.** It is a pointer for the
maintainer, not something a teammate can follow — for everyone else the commit link is the
one that works. Entries before the trailer convention are backfilled from first-hand
knowledge only; a blank cell means nobody could vouch for it.

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
          # Fall back to the table when the trailer is missing, or predates the
          # "<uuid> <title>" shape and so cannot render as a link.
          case "${session:-}" in
            [0-9a-f]*-[0-9a-f]*-*) ;;
            *) session="$(backfill "$version")" ;;
          esac
          printf '| **%s** | %s | %s | [`%s`](%s/commit/%s) | %s |\n' \
            "$version" "$date" "$summary" "${sha:0:7}" "$REPO" "$sha" "$(session_cell "$session")"
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
