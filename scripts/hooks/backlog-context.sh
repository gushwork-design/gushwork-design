#!/usr/bin/env bash
#
# Puts the decision queue into context at the start of every session.
#
# Wired as a Claude Code **SessionStart** hook. This is the difference between a backlog and
# a backlog that gets used: without it, every session starts by re-establishing what matters,
# and cards rot in a file nobody opens.
#
# It emits the queue as `additionalContext` rather than as a CLAUDE.md line, because a
# CLAUDE.md line is a static instruction ("go read BACKLOG.md") that Claude may or may not
# act on. This puts the actual current queue in front of it, already read.
#
# Stays silent when the queue is empty — an empty queue is the good state and there is
# nothing for a session to know about it.
#
# Install:  bash scripts/hooks/install.sh
# Test:     bash scripts/hooks/backlog-context.sh

set -uo pipefail

ROOT="${GW_BACKLOG_ROOT:-$HOME/Downloads/gushwork-design}"
SRC="$ROOT/BACKLOG.md"

[ -f "$SRC" ] || exit 0
cd "$ROOT" || exit 0

waiting="$(bash scripts/board.sh --waiting 2>/dev/null)" || exit 0
[ -z "$waiting" ] && exit 0

top="$(python3 scripts/_board.py --titles < "$SRC" 2>/dev/null | awk -F'\t' '$1=="P0"{print "  - "$2}' | head -3)"

# jq builds the JSON so a card title containing a quote, backslash or newline cannot break
# the payload — these are hand-typed strings and will eventually contain all three.
{
  printf 'Gushwork backlog — read from %s at session start.\n\n' "$SRC"
  printf 'WAITING ON A DECISION FROM UTSAV (nothing downstream moves until these are answered):\n'
  printf '%s\n' "$waiting" | sed 's/^/  - /'
  if [ -n "$top" ]; then
    printf '\nTOP OF P0:\n%s\n' "$top"
  fi
  printf '\nMention the waiting queue once, briefly, if it is relevant to what Utsav asks for.\n'
  printf 'Do not start working a card unprompted. The board is at preview/board.html;\n'
  printf 'regenerate it with `bash scripts/board.sh` after any edit to BACKLOG.md.\n'
} | jq -Rs '{
      hookSpecificOutput: {
        hookEventName: "SessionStart",
        additionalContext: .
      }
    }'

exit 0
