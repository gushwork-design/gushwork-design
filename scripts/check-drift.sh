#!/usr/bin/env bash
#
# Tells the owner of a dashboard which of THEIR components have changed since they built it.
#
#   bash scripts/check-drift.sh path/to/dashboard.html
#   bash scripts/check-drift.sh path/to/project/           # scans for stamped files
#
# There is no server and no registry of who built what, so nothing can be *pushed* to a person.
# What this does instead: every build the skill produces carries a stamp listing the components it
# used and the plugin version it used them at. This reads that stamp, diffs it against
# exports/dashboard/component-registry.json, and reports only the intersection — the components
# that build actually uses AND that have changed since.
#
# The skill runs this automatically whenever a stamped file is in play, so the notice arrives the
# next time anyone opens the dashboard with Claude. That is the closest thing to a notification
# that a plugin distributed as a git clone can honestly offer.

set -uo pipefail

TARGET="${1:-.}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$ROOT/exports/dashboard/component-registry.json"

[ -f "$REGISTRY" ] || { echo "✘ no component registry at $REGISTRY" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "✘ python3 is required" >&2; exit 1; }

python3 - "$TARGET" "$REGISTRY" <<'PY'
import json, os, re, sys

target, registry_path = sys.argv[1], sys.argv[2]
reg = json.load(open(registry_path))
comps = reg["components"]

STAMP = re.compile(r"gushwork-build:(\{.*?\})", re.S)

def stamped_files(path):
    if os.path.isfile(path):
        return [path]
    out = []
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "dist", "build", "__pycache__")]
        for f in filenames:
            if f.endswith((".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte")):
                out.append(os.path.join(dirpath, f))
    return out

def ver(v):
    return tuple(int(x) for x in v.split("."))

found = 0
drifted_any = False
for f in stamped_files(target):
    try:
        text = open(f, encoding="utf-8", errors="ignore").read()
    except OSError:
        continue
    m = STAMP.search(text)
    if not m:
        continue
    found += 1
    try:
        stamp = json.loads(m.group(1))
    except json.JSONDecodeError:
        print(f"⚠ {f}: stamp present but unreadable"); continue

    built_at = stamp.get("pluginVersion", "0.0.0")
    used = stamp.get("components", [])
    must, may, gone = [], [], []
    for name in used:
        c = comps.get(name)
        if c is None:
            gone.append(name); continue
        if ver(c["version"]) > ver(built_at):
            (must if c.get("breaking") else may).append((name, c))

    rel = os.path.relpath(f)
    if not (must or may or gone):
        print(f"✔ {rel} — built at v{built_at}, all {len(used)} components current")
        continue

    drifted_any = True
    print(f"\n▸ {rel}")
    print(f"  built with plugin v{built_at} by {stamp.get('createdBy','(unknown)')}"
          f" on {stamp.get('createdAt','(undated)')}")
    if must:
        print(f"\n  MUST UPDATE — {len(must)} component(s) render incorrectly until you do:")
        for name, c in must:
            print(f"    • {name}  v{built_at} → v{c['version']}  ({c['doc']})")
            if c.get("note"):
                print(f"      {c['note']}")
    if may:
        print(f"\n  Worth updating — {len(may)} component(s) improved:")
        for name, c in may:
            print(f"    • {name}  → v{c['version']}  ({c['doc']})"
                  + (f"  — {c['note']}" if c.get("note") else ""))
    if gone:
        print(f"\n  No longer in the registry — check by hand: {', '.join(gone)}")

if not found:
    print("No stamped Gushwork builds found under " + target)
    print("A build carries its stamp as a `gushwork-build:{...}` comment. Older builds predate")
    print("stamping and cannot be checked automatically — compare them against")
    print("exports/dashboard/component-registry.json by hand.")
    sys.exit(0)

print()
if drifted_any:
    print("To update: re-open the dashboard with Claude and ask it to bring the drifted")
    print("components up to date. It reads the same registry and the docs each entry points at.")
    sys.exit(2)
print(f"✔ {found} stamped build(s), all current.")
PY
