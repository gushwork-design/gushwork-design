#!/usr/bin/env bash
#
# Keeps preview/board.html current and says out loud when the backlog changed.
#
# Wired as a Claude Code **Stop** hook, so it runs once when a turn finishes rather than on
# every tool call. That matters: a PostToolUse hook on Write/Edit fires many times per turn
# and would notify per keystroke-ish edit. Once per turn is one notification per real change.
#
# What it does, in order:
#   1. exits silently if BACKLOG.md is absent or unchanged — the common case, so it is cheap
#   2. regenerates preview/board.html, so the board is never stale
#   3. diffs the card list against the previous turn and notifies about what actually changed
#
# Two directions, and only one of them can be solved here. When CLAUDE adds a card, this
# fires and you hear about it. When YOU add a card with no session running, nothing can wake
# Claude up — that one is picked up at the next session start or by the morning digest.
#
# State lives in .git/, which is untracked by definition — it can never be committed and
# never shows up in `git status`.
#
# Install:  bash scripts/hooks/install.sh   (or see the settings.json snippet it prints)
# Test:     bash scripts/hooks/backlog-sync.sh --test

set -uo pipefail

ROOT="${GW_BACKLOG_ROOT:-$HOME/Downloads/gushwork-design}"
SRC="$ROOT/BACKLOG.md"
STATE="$ROOT/.git/gw-backlog-state"

# Absent backlog is not an error — this hook is installed user-wide and most sessions are
# nowhere near this repo.
[ -f "$SRC" ] || exit 0

cd "$ROOT" || exit 0

now="$(python3 scripts/_board.py --titles < "$SRC" 2>/dev/null)" || exit 0
prev=""
[ -f "$STATE" ] && prev="$(cat "$STATE")"

# Unchanged: the overwhelmingly common case. Nothing to render, nothing to say.
if [ "$now" = "$prev" ]; then
  exit 0
fi

# Always rebuild before notifying, so opening the board from the notification shows the
# state being described rather than the previous one.
bash scripts/board.sh >/dev/null 2>&1 || true
printf '%s' "$now" > "$STATE"

# First run has no baseline — record it and stay quiet rather than announcing every
# existing card as new.
if [ -z "$prev" ]; then
  exit 0
fi

# Join lines with " · ". See the note on `paste -d` above the fix in git history:
# `paste -sd' · '` cycles the three characters one per join instead of using all three.
added="$(comm -13 <(printf '%s\n' "$prev" | sort) <(printf '%s\n' "$now" | sort))"
[ -z "$added" ] && exit 0

n="$(printf '%s\n' "$added" | grep -c . || true)"
newly_waiting="$(printf '%s\n' "$added" | grep -c '^Waiting on you' || true)"
newly_done="$(printf '%s\n' "$added" | grep -c '^Completed' || true)"

# Lead with the thing to act on. A card landing in the decision queue outranks a card
# landing in the backlog, which outranks something being marked shipped.
if [ "$newly_waiting" -gt 0 ]; then
  title="Waiting on you"
  body="$(printf '%s\n' "$added" | grep '^Waiting on you' | cut -f2 | awk '{printf "%s%s", sep, $0; sep=" · "}')"
elif [ "$n" -gt "$newly_done" ]; then
  title="Backlog — $((n - newly_done)) new"
  body="$(printf '%s\n' "$added" | grep -v '^Completed' | cut -f2 | awk '{printf "%s%s", sep, $0; sep=" · "}')"
else
  title="Shipped"
  body="$(printf '%s\n' "$added" | grep '^Completed' | cut -f2 | awk '{printf "%s%s", sep, $0; sep=" · "}')"
fi

# Trim: the notification centre truncates hard, and a truncated list reads as broken.
[ "${#body}" -gt 180 ] && body="${body:0:177}..."

if [ "${1:-}" = "--test" ]; then
  printf 'would notify:\n  title: %s\n  body:  %s\n' "$title" "$body"
  exit 0
fi

osascript -e "display notification \"${body//\"/\\\"}\" with title \"Gushwork · ${title//\"/\\\"}\"" \
  >/dev/null 2>&1 || true

exit 0
