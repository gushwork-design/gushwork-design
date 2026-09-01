#!/usr/bin/env bash
# Stamp the site's "Last updated" line from the release history.
#
#   bash scripts/stamp-site.sh            # rewrite the pages
#   bash scripts/stamp-site.sh --check    # exit 1 if stale — for CI or a hook
#
# WHY THIS EXISTS
# ---------------
# The Overview hero and the Style Guide header both carry a "Last updated" date.
# They were typed by hand from the Figma ("14th Aug, 2026") and had already gone
# stale by the time the site was built — a date that lies is worse than no date,
# because people trust it to decide whether they are looking at current guidance.
#
# The date is now DERIVED, from the same place CHANGELOG.md and the changelog
# sheet come from: `scripts/_releases.sh`, where a release is a commit that moved
# the `version` field in `.claude-plugin/plugin.json`. That is the repo's
# definition of "the design system changed" — so the three renderings cannot
# disagree, which is the whole point of having one derivation.
#
# It is deliberately NOT `date` / "today". Stamping today's date would mean the
# line moves whenever someone happens to run a script, and --check could never
# tell stale from fresh because the expected value would change every midnight.
#
# Called by scripts/release-log.sh, so a release updates it along with the
# other two renderings, and `--check` there gates every publish.
set -euo pipefail
cd "$(dirname "$0")/.."

CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

. scripts/_releases.sh

# Newest release. Fields are split on US (0x1f); the date field is "15 Aug 2026 19:29".
IFS=$'\x1f' read -r VERSION _SHA DATETIME _REST < <(releases)
[ -n "${VERSION:-}" ] || { echo "stamp-site: no releases found — is this a git checkout?" >&2; exit 1; }

DAY="$(echo "$DATETIME"  | awk '{print $1}')"
MON="$(echo "$DATETIME"  | awk '{print $2}')"
YEAR="$(echo "$DATETIME" | awk '{print $3}')"

# "15" -> "15th". 11/12/13 are the exceptions that break the last-digit rule.
case "$DAY" in
  11|12|13) SUFFIX=th ;;
  *1) SUFFIX=st ;;
  *2) SUFFIX=nd ;;
  *3) SUFFIX=rd ;;
  *)  SUFFIX=th ;;
esac
STAMP="${DAY}${SUFFIX} ${MON}, ${YEAR}"

# file|regex — the class is part of the pattern so this can only ever rewrite the
# one element, never a "Last updated" that appears in body copy.
TARGETS=(
  'web/index.html|(<p class="gw-hero__meta">Last updated )[^<]+'
  'web/style-guide.html|(<p class="sg__meta">Last updated )[^<]+'
)

STAMP="$STAMP" VERSION="$VERSION" CHECK="$CHECK" \
TARGETS="$(printf '%s\n' "${TARGETS[@]}")" python3 - <<'PY'
import os, re, sys

stamp = os.environ["STAMP"]
version = os.environ["VERSION"]
check = os.environ["CHECK"] == "1"
stale = []

for line in os.environ["TARGETS"].strip().split("\n"):
    path, pattern = line.split("|", 1)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    rx = re.compile(pattern)
    found = rx.search(text)
    if not found:
        # Loud, like stamp-release.sh — a silently skipped file is how the date
        # went stale in the first place.
        sys.exit(f"stamp-site: no 'Last updated' line found in {path} — "
                 f"did its markup change?")

    current = found.group(0)[len(found.group(1)):]
    if current == stamp:
        print(f"  {path:<24} already {stamp}")
        continue

    if check:
        stale.append(f"  {path}: says {current!r}, should be {stamp!r}")
        continue

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(rx.sub(lambda m: m.group(1) + stamp, text, count=1))
    print(f"  {path:<24} {current} -> {stamp}")

if stale:
    print(f"\nThe site's 'Last updated' is stale (newest release is v{version}, {stamp}):",
          file=sys.stderr)
    print("\n".join(stale), file=sys.stderr)
    print("\n  run: bash scripts/stamp-site.sh", file=sys.stderr)
    sys.exit(1)
PY

[ "$CHECK" = 1 ] && echo "Site date is current: $STAMP (v$VERSION)" || echo "Stamped the site: $STAMP (v$VERSION)"
