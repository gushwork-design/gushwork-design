#!/usr/bin/env bash
#
# Stamps a version and today's date everywhere they appear, so the two can
# never disagree.
#
#   bash scripts/stamp-release.sh 1.2.0
#
# Touches four places:
#   .claude-plugin/plugin.json       version   <- what `claude plugin list` shows
#   .claude-plugin/marketplace.json  version   <- the marketplace entry
#   skills/gushwork-web/SKILL.md     announce line
#   skills/gushwork-dashboard/SKILL.md
#
# The announce line matters most: a teammate on a stale copy sees that copy's
# own stale date, which is how drift becomes visible without anyone checking.
# Run this before you push anything people should notice.

set -euo pipefail

[ $# -eq 1 ] || { echo "usage: bash scripts/stamp-release.sh <version>   e.g. 1.2.0" >&2; exit 1; }
VERSION="$1"
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "version must look like 1.2.0" >&2; exit 1; }

ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
DATE="$(date +"%-d %b %Y")"

VERSION="$VERSION" DATE="$DATE" ROOT="$ROOT" python3 - <<'PY'
import json, os, re, pathlib

v, d, root = os.environ["VERSION"], os.environ["DATE"], pathlib.Path(os.environ["ROOT"])

p = root / ".claude-plugin" / "plugin.json"
m = json.loads(p.read_text()); m["version"] = v
p.write_text(json.dumps(m, indent=2) + "\n")
print(f"  plugin.json          -> {v}")

p = root / ".claude-plugin" / "marketplace.json"
m = json.loads(p.read_text())
m.setdefault("metadata", {})["version"] = v
for entry in m.get("plugins", []):
    entry["version"] = v
p.write_text(json.dumps(m, indent=2) + "\n")
print(f"  marketplace.json     -> {v}")

pat = re.compile(r'(Using the Gushwork \w+ skill — v)[0-9.]+(, updated )[^."]+')
for name in ("gushwork-web", "gushwork-dashboard"):
    p = root / "skills" / name / "SKILL.md"
    t = p.read_text()
    t2, n = pat.subn(lambda x: f"{x.group(1)}{v}{x.group(2)}{d}", t)
    if n == 0:
        raise SystemExit(f"no announce line found in {p} — did its wording change?")
    p.write_text(t2)
    print(f"  {name:<20} -> v{v}, {d}")
PY

echo
echo "Stamped v$VERSION · $DATE"
echo
echo "The commit subject becomes the CHANGELOG row, so write it as the one-line"
echo "summary — 'v$VERSION — what changed' — and name the chat in a trailer:"
echo
echo "    Session: <this chat's title>"
echo
echo "Then regenerate the log as a SEPARATE commit — never an amend, because"
echo "amending rewrites the sha the newest row just recorded:"
echo
echo "    bash scripts/changelog.sh"
echo "    git add CHANGELOG.md && git commit -m \"Regenerate CHANGELOG after v$VERSION\""
echo "    git push"
