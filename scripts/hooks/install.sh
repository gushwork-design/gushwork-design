#!/usr/bin/env bash
#
# Installs the repo's git hooks into this clone. Hooks live in .git/hooks, which git does not
# track, so a fresh clone has none until this runs.
#
#   bash scripts/hooks/install.sh
#
set -euo pipefail
ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
SRC="$ROOT/scripts/hooks"
DST="$(git -C "$ROOT" rev-parse --git-path hooks)"

mkdir -p "$DST"
for hook in pre-push; do
  [ -f "$SRC/$hook" ] || continue
  cp "$SRC/$hook" "$DST/$hook"
  chmod +x "$DST/$hook"
  echo "✔ installed $hook"
done

echo
echo "main now refuses a plain push. Authorise one with:"
echo "    GW_PUSH=1 git push origin main"
