#!/usr/bin/env bash
#
# One command for a release. Stamps, commits, regenerates, verifies — in the order the
# ritual has always required, so it cannot be half-done.
#
#   bash scripts/release.sh 1.44.0 "what changed"
#   bash scripts/release.sh 1.44.0 "what changed" --session "<uuid> <chat title>"
#   bash scripts/release.sh 1.44.0 "what changed" --session "..." --publish
#
# WHY THIS EXISTS
# ---------------
# The steps were correct and written down, and they were still got wrong. v1.40.0 moved
# plugin.json and both announce lines but not marketplace.json — stamp-release.sh writes all
# of them, so it had simply not been run — and the marketplace served 1.39.0 while the plugin
# called itself 1.40.0 for ten days. Nothing failed. Nothing said anything. The gap was only
# found because someone went looking.
#
# A sequence a human drives is a sequence with a step missing sooner or later. This drives it,
# and refuses to continue at the first disagreement.
#
# WHAT IT WILL NOT DO
# -------------------
# It does not push. scripts/hooks/pre-push exists precisely so a push to main is a deliberate
# act rather than an incidental one, and a release script that pushed would route around the
# guard the repo installed on purpose.
#
# THE TWO COMMITS ARE NOT NEGOTIABLE
# ----------------------------------
# A release is a commit that MOVES THE VERSION FIELD — that is the definition scripts/
# _releases.sh derives the changelog from. The log regeneration is a SECOND commit, never an
# amend, because amending rewrites the sha that the newest changelog row just recorded.

set -euo pipefail
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"

VERSION="" SUMMARY="" SESSION="" PUBLISH=0
while [ $# -gt 0 ]; do
  case "$1" in
    --session) SESSION="${2:-}"; shift 2 ;;
    --publish) PUBLISH=1; shift ;;
    -*) echo "unknown flag: $1" >&2; exit 1 ;;
    *) if [ -z "$VERSION" ]; then VERSION="$1"; elif [ -z "$SUMMARY" ]; then SUMMARY="$1";
       else echo "unexpected argument: $1" >&2; exit 1; fi; shift ;;
  esac
done

[ -n "$VERSION" ] && [ -n "$SUMMARY" ] || {
  echo 'usage: bash scripts/release.sh <version> "<summary>" [--session "<uuid> <title>"] [--publish]' >&2
  exit 1; }
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "version must look like 1.2.0" >&2; exit 1; }

CURRENT="$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['version'])")"
python3 - "$CURRENT" "$VERSION" <<'PY' || exit 1
import sys
def v(s): return tuple(int(x) for x in s.split("."))
cur, new = sys.argv[1], sys.argv[2]
if v(new) <= v(cur):
    sys.exit(f"  {new} is not ahead of the current {cur} — nothing to release")
PY

# ── preflight ──────────────────────────────────────────────────────────────────────────────
# A dirty tree is disqualifying, not inconvenient: this script commits, so anything already
# modified would be swept into a release commit under a subject that does not describe it.
[ -z "$(git status --porcelain --untracked-files=no)" ] || {
  echo "Working tree is dirty — commit or stash first. A release commit must contain only" >&2
  echo "the stamp:" >&2
  git status --porcelain --untracked-files=no | sed 's/^/  /' >&2
  exit 1; }

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[ "$BRANCH" = main ] || echo "  note: releasing from '$BRANCH', not main."

if [ -z "$SESSION" ]; then
  echo "  note: no --session, so this release's Session column will be blank."
  echo "        uuid = the transcript filename in ~/.claude/projects/<project>/"
fi

echo "Releasing v$VERSION (from v$CURRENT)"
echo

# ── 1 · stamp ──────────────────────────────────────────────────────────────────────────────
bash scripts/stamp-release.sh "$VERSION" | sed 's/^/  /'

# ── 2 · the release commit ─────────────────────────────────────────────────────────────────
# The subject IS the changelog row, in both renderings.
#
# The trailer must sit in the LAST PARAGRAPH. Git only parses trailers there, so a Session:
# line separated from whatever follows it by a blank line is silently not a trailer at all —
# and the Session column comes out blank with nothing to say why. Built as one block here,
# and verified below rather than assumed.
MSG="v$VERSION — $SUMMARY"
[ -n "$SESSION" ] && MSG="$MSG

Session: $SESSION"

# -u, not -A: the preflight above only refuses on modified TRACKED files, so an untracked
# scratch file sitting in the tree would sail past it and land in the release commit. Everything
# a release legitimately touches — the manifests, the announce lines, the derived logs — is
# already tracked.
git add -u
git commit -q -m "$MSG"

if [ -n "$SESSION" ]; then
  PARSED="$(git log -1 --format='%(trailers:key=Session,valueonly)' | tr -d '\n')"
  [ -n "$PARSED" ] || {
    echo "  ✘ the Session: trailer did not parse — the changelog row would be blank." >&2
    echo "    Fix the commit message and re-run; do not push this." >&2
    exit 1; }
  echo "  Session trailer parses -> $PARSED"
fi
echo "  release commit         -> $(git log -1 --format=%h)"

# ── 3 · the logs, as a SECOND commit ───────────────────────────────────────────────────────
echo
bash scripts/release-log.sh | sed 's/^/  /'
git add -u
git commit -q -m "Regenerate the release logs after v$VERSION"
echo "  log commit             -> $(git log -1 --format=%h)"

# ── 4 · prove it ───────────────────────────────────────────────────────────────────────────
# Everything above can succeed individually and still leave the release inconsistent. These
# are the three things that were actually wrong at one time or another.
echo
echo "Verifying:"
bash scripts/version-json.sh --check | sed 's/^/  /'
bash scripts/release-log.sh --check >/dev/null 2>&1 \
  && echo "  ✔ derived logs agree with their generator" \
  || { echo "  ✘ derived logs disagree with their generator" >&2; exit 1; }
grep -q "v$VERSION" CHANGELOG.md \
  && echo "  ✔ v$VERSION is a row in CHANGELOG.md" \
  || { echo "  ✘ v$VERSION did not become a changelog row — the version field did not move" >&2; exit 1; }

# ── 5 · publish, only if asked ─────────────────────────────────────────────────────────────
if [ "$PUBLISH" = 1 ]; then
  echo
  bash scripts/publish-sheets.sh
fi

echo
echo "Done. Two commits, nothing pushed:"
git log --oneline -2 | sed 's/^/  /'
echo
echo "  GW_PUSH=1 git push origin $BRANCH"
[ "$PUBLISH" = 1 ] || echo "  bash scripts/publish-sheets.sh      # when you want it live"
