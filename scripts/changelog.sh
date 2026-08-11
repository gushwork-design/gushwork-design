#!/usr/bin/env bash
# Regenerate CHANGELOG.md from git history.
#
# The log is DERIVED, never hand-written — so it cannot drift from what actually shipped.
# The derivation lives in `scripts/_releases.sh` and is shared with `changelog-sheet.sh`,
# so the markdown and the rendered sheet can never disagree. Run both together:
#
#     bash scripts/release-log.sh
#
# WHAT CHANGED 8 Aug 2026. This script used to define a release as a commit whose SUBJECT
# started `vX.Y.Z`. That convention only began at v1.19.0, so it listed 11 of 34 releases
# and silently dropped v1.20.0 — the login screen — whose commit was titled
# "Add dashboard-login-screen — …" instead. A release is now a commit that moved the
# `version` field in `.claude-plugin/plugin.json`, which is the field `plugin update`
# actually compares. Nothing that shipped can be lost by writing a commit message the
# wrong way. Release subjects should still read `vX.Y.Z — what changed`, because the part
# after the dash is the summary in both renderings.
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
. scripts/_releases.sh

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
`preview/changelog-sheet.html` is the same data rendered as a sheet; both come from
`scripts/_releases.sh`, so they cannot disagree.

A release is **a commit that moved the `version` field in `.claude-plugin/plugin.json`** —
the field `plugin update` compares. Not a commit subject: subjects are a convention that
started at v1.19.0, and deriving from them dropped 23 releases including v1.20.0.

`Session` is the chat the change came from — a `claude://resume/<uuid>` deep link that
reopens that conversation in the Claude desktop app, recorded as a `Session:` trailer on
the release commit.

**The link only resolves on the machine holding the transcript.** It is a pointer for the
maintainer, not something a teammate can follow — for everyone else the commit link is the
one that works. Entries before the trailer convention are backfilled from first-hand
knowledge only; an em dash means nobody could vouch for it.

To check what you are running: the skill announces its own version and date at the start of
every session. Trust that line over memory — it is stamped into the file, so **a stale copy
reports its own stale date.**

HEAD

  printf '| Version | Date | What changed | Commit | Session |\n'
  printf '|---|---|---|---|---|\n'

  # `body` must be read even though the markdown table has no column for it. `read` puts
  # every leftover field in the LAST variable, so dropping it made `session` swallow the
  # whole commit body and print it inside the Session link.
  releases | while IFS=$'\x1f' read -r version sha date summary session body; do
    [ -z "${version:-}" ] && continue
    printf '| **v%s** | %s | %s | [`%s`](%s/commit/%s) | %s |\n' \
      "$version" "$date" "$summary" "${sha:0:7}" "$REPO" "$sha" "$(session_cell "$session")"
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
