#!/usr/bin/env bash
# Publish the review sheets to https://gushwork-design.vercel.app
#
#   bash scripts/publish-sheets.sh            # deploy to production
#   bash scripts/publish-sheets.sh --dry-run  # assemble and print the tree, deploy nothing
#
# WHAT THIS IS FOR
# ----------------
# The sheets are the one part of the system that only works if you clone the repo. Hosting
# them turns `preview/` into a URL anyone at Gushwork can open, which is the distribution
# half of the mandate. It is for READING and REVIEWING — the plugin is still how you build.
#
# THE PAGES ARE NEVER EDITED. This assembles a copy in a temp directory and deploys that,
# preserving the repo's own layout, so the deployed URLs are /preview/<sheet>.html and not
# one line of any sheet has to change. `scripts/publish-index.html` is the entry point —
# a deploy needs one or the root 404s — and is the only page that exists solely to be
# hosted.
#
# WHY THE VERCEL MCP CANNOT DO THIS. `deploy_to_vercel` takes files inline in the tool
# call. This tree is 2.4 MB — three font TTFs plus a 490 KB review sheet — so the CLI is
# the only path. If `vercel whoami` fails, run `vercel login`; never pass a token on the
# command line.
set -euo pipefail
cd "$(dirname "$0")/.."

DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

# The sheets that go up. Add a line to publish another; keep the repo-relative path.
SHEETS=(
  preview/review-sheet.html
  preview/catalogue.html
  preview/changelog-sheet.html
  preview/install.html
)

# Social card images. A page's og:image must be an absolute URL for crawlers to
# resolve it, so it never matches the ../assets/ grep further down. List it here
# or the card 404s and the link unfurls blank.
SOCIAL=(
  assets/og/install.png
)

# The changelog sheet is generated, so a publish must not ship a stale one.
bash scripts/release-log.sh --check

command -v vercel >/dev/null || { echo "vercel CLI not installed — brew install vercel" >&2; exit 1; }
if [ "$DRY" = 0 ] && ! vercel whoami >/dev/null 2>&1; then
  echo "Vercel CLI is not authenticated. Run:  vercel login" >&2
  exit 1
fi

# The directory name becomes the project name on first deploy, and the project name becomes
# the URL. It must be `gushwork-design`.
STAGE="$(mktemp -d)/gushwork-design"
trap 'rm -rf "$(dirname "$STAGE")"' EXIT
mkdir -p "$STAGE/preview" "$STAGE/foundation" "$STAGE/fonts"

cp scripts/publish-index.html "$STAGE/index.html"
for s in "${SHEETS[@]}"; do cp "$s" "$STAGE/preview/"; done

# The component registry goes up too, and it is the ONE file here that is not for reading.
# Every dashboard the skill builds fetches it on load to see whether the components it was built
# from have moved on, and shows its owner a notice if they have. That check has to keep working
# after the repo goes private, which is exactly why it points at this public deploy and not at
# raw.githubusercontent.com. Deploying without it does not break a dashboard — the fetch fails
# silently — it just means nobody is ever told.
mkdir -p "$STAGE/exports/dashboard"
cp exports/dashboard/component-registry.json "$STAGE/exports/dashboard/"
python3 -c "import json,sys; json.load(open('exports/dashboard/component-registry.json'))" \
  || { echo "  component-registry.json is not valid JSON — fix it before publishing" >&2; exit 1; }
cp foundation/tokens.css "$STAGE/foundation/"
cp fonts/*.ttf "$STAGE/fonts/"
for a in "${SOCIAL[@]}"; do
  [ -f "$a" ] || { echo "  MISSING social image: $a" >&2; exit 1; }
  mkdir -p "$STAGE/$(dirname "$a")" && cp "$a" "$STAGE/$a"
done

# Any page that links tokens.css needs the real fonts; review-sheet and catalogue inline
# their own. Copy whatever else the sheets reference, so a new sheet with assets just works.
for s in "${SHEETS[@]}"; do
  grep -oE '(href|src)="\.\./assets/[^"]+"' "$s" 2>/dev/null | sed 's/.*="\.\.\///;s/"$//' || true
done | sort -u | while read -r a; do
  [ -f "$a" ] || { echo "  MISSING asset referenced by a sheet: $a" >&2; continue; }
  mkdir -p "$STAGE/$(dirname "$a")" && cp "$a" "$STAGE/$a"
done

echo "Staged $(find "$STAGE" -type f | wc -l | tr -d ' ') files · $(du -sh "$STAGE" | cut -f1)"
find "$STAGE" -type f | sed "s|$STAGE/||" | sort | sed 's/^/  /'

if [ "$DRY" = 1 ]; then
  echo
  echo "Dry run — nothing deployed."
  exit 0
fi

echo
cd "$STAGE" && vercel deploy --prod --yes
