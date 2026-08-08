#!/usr/bin/env bash
# Regenerate every rendering of the release history. Run this after a release, or any
# time you want to know whether the logs have drifted.
#
#   bash scripts/release-log.sh            # rewrite both
#   bash scripts/release-log.sh --check    # exit 1 if either is stale — for CI or a hook
#
# One derivation (`scripts/_releases.sh`), two renderings:
#
#   CHANGELOG.md                   markdown, for GitHub and for anyone reading the repo
#   preview/changelog-sheet.html   the sheet, for reviewing on-brand in a browser
#
# Neither is written by hand. If a row looks wrong, the commit is wrong — fix the history
# or the derivation, never the output.
set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/changelog.sh "$@"
bash scripts/changelog-sheet.sh "$@"
