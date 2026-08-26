#!/usr/bin/env python3
"""Render BACKLOG.md as preview/board.html — the task board and shipped timeline.

Reads BACKLOG.md on stdin, writes HTML to stdout. Never run directly;
`scripts/board.sh` is the entry point and holds the usage notes.

WHY THIS ONE IS BACKWARDS FROM THE REST. Every other generator here derives from something
machine-truthful — `_releases.sh` reads the version field out of plugin.json at each commit,
so the changelog cannot lie. A backlog has no such source: priorities are human input, so
BACKLOG.md *is* the source and this script only renders it. The one-directional flow is what
keeps the file and the board from disagreeing; there is no writing back.

STATE IS THE SECTION, not a field. `## P0` / `## Waiting on you` / `## Completed` are the
states, and a card's position in the file is its priority. Nothing here reads a status key,
because a status key next to a section heading is two truths waiting to diverge.

NO STATE IS CARRIED BY COLOUR ALONE. Utsav's editor theme is dark-daltonized, so every
status that has a colour also has a word: an overdue card says "6 days", a flagged card says
"needs detail", a priority pill says "P0". Removing all colour from this page should lose
emphasis and no information. Check that before adding a swatch.

LIGHT THEME ONLY, matching preview/changelog-sheet.html by the same instruction. There is no
prefers-color-scheme block. Do not add one without asking.

Every value in the CSS is a token from foundation/tokens.css. Where a rule is new but its
values are not, it is marked ADDED — reported per foundation/new-component-notice.md.
"""

import datetime as dt
import html
import os
import re
import sys

# The board's states, in the order they appear on the page. Anything else under a `##` in
# BACKLOG.md is prose — the file explains its own format in two such sections, and the
# `- [ ]` line inside its fenced example must not be mistaken for a real card.
QUEUE = "Waiting on you"
COLUMNS = ["P0", "P1", "P2", "Icebox"]
DONE = "Completed"
SECTIONS = [QUEUE] + COLUMNS + [DONE]

# Keys a card may carry. Anything else on an indented line renders as a plain note rather
# than being dropped, so a typo is visible instead of silent.
KEYS = ["surface", "constraint", "done", "added", "since", "options", "rec", "shipped",
        "blocked", "needs"]

# A card in an open column is only pickable unattended if it says where to work and what
# finished looks like. Missing either, it is flagged and skipped rather than guessed at.
REQUIRED = ["surface", "done"]

TODAY = dt.date.today()


# ── parse ─────────────────────────────────────────────────────────────────────────────
CARD = re.compile(r"^-\s+\[[ xX?]\]\s+(.+?)\s*$")
KEYLINE = re.compile(r"^([a-z][a-z-]*):\s*(.*)$")
# `- [x] 2026-08-15 · Title` — the date leads a completed card and is what the timeline
# groups on. The separator may be ·, - or em dash; all three get typed by hand.
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})\s*[·\-—]?\s*(.*)$")


def parse(text):
    """BACKLOG.md -> {section: [card]}. Cards outside a known section are ignored."""
    out = {name: [] for name in SECTIONS}
    section, card, fenced = None, None, False

    for raw in text.split("\n"):
        line = raw.rstrip()

        # Fenced blocks hold the format example, which contains a card-shaped line.
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue

        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            name = head.group(1).strip()
            section = name if name in out else None
            card = None
            continue

        if section is None:
            continue

        m = CARD.match(line)
        if m:
            title = m.group(1).strip()
            date = ""
            d = DATED.match(title)
            if d:
                date, title = d.group(1), d.group(2).strip()
            card = dict(title=title, date=date, keys={}, notes=[])
            out[section].append(card)
            continue

        # Continuation lines are indented under their card.
        if card is not None and raw[:1] in (" ", "\t") and line.strip():
            body = line.strip()
            k = KEYLINE.match(body)
            if k and k.group(1) in KEYS:
                card["keys"][k.group(1)] = k.group(2).strip()
            else:
                card["notes"].append(body)
            continue

        if not line.strip():
            card = None

    return out


def age_days(card, *keys):
    """Whole days since the first of `keys` that holds a date. None if undated."""
    for k in keys:
        v = card["keys"].get(k) or (card["date"] if k == "date" else "")
        if not v:
            continue
        try:
            return (TODAY - dt.date.fromisoformat(v[:10])).days
        except ValueError:
            continue
    return None


def age_label(days):
    """Words first — this is the accessible half of every status on the page."""
    if days is None:
        return "undated"
    if days <= 0:
        return "today"
    if days == 1:
        return "1 day"
    return "%d days" % days


def flags(card, section):
    """Non-colour status words attached to a card."""
    out = []
    if section in COLUMNS and section != "Icebox":
        missing = [k for k in REQUIRED if not card["keys"].get(k)]
        if missing:
            out.append("needs detail")
    if card["keys"].get("blocked"):
        out.append("blocked")
    return out


# ── page ────────────────────────────────────────────────────────────────────────────────
# Two thresholds, both stated on the page rather than implied by a shade. Three working days
# is where a decision stops being "recent" and starts being the reason nothing shipped; a
# week is where it needs saying out loud.
STALE, OVERDUE = 3, 7

# The Kanban columns, left to right. `Waiting on you` leads because it is the queue that
# blocks every other column — a decision nobody makes is the most expensive card on the board.
LANES = [QUEUE] + COLUMNS

BUILD_COMPONENTS = ["badge", "card-shell", "empty-state", "page-header", "section-header",
                    "tab-group", "tab-item", "table-cell", "table-row"]

CSS = """
  /* LIGHT THEME ONLY, matching preview/changelog-sheet.html by the same instruction. There is
     no prefers-color-scheme block. table-row, tab-group and input have no dark variants yet
     (a known gap in v2), so a dark board would need values that do not exist. Do not add one
     without asking.

     Every value is a token. Rules marked ADDED are new rules, not new values.

     NO STATE IS CARRIED BY COLOUR ALONE. Utsav's editor theme is dark-daltonized, so every
     status that has a colour also has a word — an overdue card says "12 days", a flagged card
     says "needs detail". Strip every colour from this page and it loses emphasis, not
     information. Check that before adding a swatch. */
  *,*::before,*::after{box-sizing:border-box}
  body{margin:0;background:var(--gw-color-neutral-25);
       font:var(--gw-text-body-14-reg);letter-spacing:var(--gw-text-body-14-reg-tracking);
       color:var(--gw-color-neutral-900);-webkit-font-smoothing:antialiased}
  code{font-family:var(--gw-font-body);font-weight:500;color:var(--gw-color-neutral-900);
       background:var(--gw-color-neutral-35);border-radius:var(--gw-radius-4);
       padding:0 var(--gw-space-4)}
  [hidden]{display:none !important}
  :focus-visible{outline:var(--gw-focus-ring);outline-offset:var(--gw-focus-offset)}

  /* The gray canvas is the dashboard default. CHOSEN, not measured: the 32px gutter.

     TWO COLUMN WIDTHS, deliberately. 1120 is the v2 content column — page-header, card-shell,
     section-header and table-row are all measured against it, so the header, the list and the
     timeline sit at 1120. The BOARD does not: five lanes inside 1120 come out at 198px each,
     which is too narrow to read a card in. No Kanban lane exists in the system to measure, so
     the board gets the full gutter-to-gutter width and the lanes land near 260. Stated here
     because it is a deviation from the measured column, not a value from Figma. */
  .wrap{max-width:1376px;margin:0 auto;padding:var(--gw-space-32) var(--gw-space-32)
        var(--gw-space-80)}
  .ph,[data-panel="list"],[data-panel="shipped"]{max-width:1120px}

  /* ── page-header (278:567) — 1120 x 113, vertical, gap spacing/24, no fill ── */
  .ph{display:flex;flex-direction:column;gap:var(--gw-space-24)}
  /* Dashboard/display-44-sem. ⚠ NO TOKEN — the five Dashboard/display-* styles match no
     --gw-text-* property (44 is Semibold where h3 is Bold). Literal spec per R15; never
     substitute h3. */
  .ph__t{margin:0;font:600 44px/1.2 var(--gw-font-display);letter-spacing:0;
         color:var(--gw-color-black)}
  .ph__row{display:flex;align-items:center;justify-content:space-between;
           gap:var(--gw-space-16);flex-wrap:wrap}
  .ph__l{display:flex;align-items:center;gap:var(--gw-space-16);flex-wrap:wrap}
  /* period-meta: button-10-med on neutral/600 */
  .meta{font:var(--gw-text-body-10-med);letter-spacing:var(--gw-text-body-10-med-tracking);
        color:var(--gw-color-neutral-600);font-variant-numeric:tabular-nums}

  /* ── tab-group (356:913) — 36h, radius/12, padding spacing/4, gap spacing/4,
     fill neutral/50, 1px neutral/100. Gap is 4, NOT 8 — the v1 controls/tab used 8 and the
     screens won. ── */
  .tabs{display:inline-flex;align-items:center;height:36px;padding:var(--gw-space-4);
        gap:var(--gw-space-4);border-radius:var(--gw-radius-12);
        background:var(--gw-color-neutral-50);
        border:1px solid var(--gw-color-neutral-100)}
  /* tab-item (268:408) — 28h, radius/8, py-8 px-12, button-12-med.
     Inactive labels are NOT greyed — they are neutral/900, both themes. Active is a
     neutral/black fill with a white label (black carries interaction state; blue would be
     wrong here — blue is data and status on this surface). */
  .tab{display:inline-flex;align-items:center;gap:var(--gw-space-4);height:28px;
       padding:0 var(--gw-space-12);border:0;border-radius:var(--gw-radius-8);
       background:none;color:var(--gw-color-neutral-900);
       font:var(--gw-text-button-12);cursor:pointer;white-space:nowrap}
  .tab[aria-selected="true"]{background:var(--gw-color-black);color:var(--gw-color-white)}
  .tab__n{font-variant-numeric:tabular-nums;opacity:.6}
  .tab[aria-selected="true"] .tab__n{opacity:.7}

  /* ── section-header (276:560) — 1120 x 24, px-8, SPACE_BETWEEN, gap spacing/8.
     The qualifier is part of the pattern, not decoration: it states what the section covers. ── */
  .sh{display:flex;align-items:baseline;justify-content:space-between;gap:var(--gw-space-8);
      padding:0 var(--gw-space-8);margin:var(--gw-space-32) 0 var(--gw-space-16)}
  .sh__g{display:flex;align-items:baseline;gap:var(--gw-space-8);flex-wrap:wrap}
  .sh__t{font:var(--gw-text-body-16-sem);letter-spacing:var(--gw-text-body-16-sem-tracking);
         color:var(--gw-color-black)}
  .sh__q{font:var(--gw-text-body-16-reg);letter-spacing:var(--gw-text-body-16-reg-tracking);
         color:var(--gw-color-neutral-500)}

  /* ── badge (1582:628) Size=Small — 24h, px-8, radius/8, body-12-med. ONE size is used
     here. There is no smaller step in the component (Small / Medium / Large only) and a 20h
     chip was NOT invented for the dense rows — interpolating a variant is how a build drifts.

     Blue is UNDEFINED in the badge rule, so it is deliberately unused rather than pressed
     into meaning "info". Colour is never decorative: Red = needs attention now, Yellow = the
     card is not ready, Green = shipped, Black = higher-emphasis neutral (P0), Neutral = a
     plain label.

     ⚠ DEVIATION, and a finding. The documented light treatment is a {Colour}/25 fill with a
     {Colour}/500 label. At the component's own body-12-med that FAILS WCAG AA on all three
     signal colours — measured red 4.28:1, yellow 3.07:1, green 3.15:1, against the 4.5:1
     small-text threshold. The /600 steps pass (red 5.72, yellow 4.84, green 4.79) so the
     labels are one step darker here. The fill is unchanged. This affects every badge in the
     system, not just this board — reported, see notices/. ── */
  .bdg{display:inline-flex;align-items:center;height:24px;padding:0 var(--gw-space-8);
       border-radius:var(--gw-radius-8);font:var(--gw-text-body-12-med);
       letter-spacing:var(--gw-text-body-12-med-tracking);white-space:nowrap;
       background:var(--gw-color-neutral-50);color:var(--gw-color-neutral-700)}
  .bdg--black{background:var(--gw-color-neutral-900);color:var(--gw-color-white)}
  .bdg--red{background:var(--gw-color-red-25);color:var(--gw-color-red-600)}
  .bdg--yellow{background:var(--gw-color-yellow-25);color:var(--gw-color-yellow-600)}
  .bdg--green{background:var(--gw-color-green-25);color:var(--gw-color-green-600)}

  /* ── board ── five equal lanes, no floor: a floor plus five lanes would overflow the
     column and put a horizontal scrollbar on the default view. They reflow to two and then
     one instead, per R17's narrowing. CHOSEN, both the count and the breakpoints. */
  .board{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:var(--gw-space-16);
         align-items:start}
  .lane{min-width:0;display:flex;flex-direction:column;gap:var(--gw-space-12)}
  .lane__hd{display:flex;align-items:center;justify-content:space-between;
            gap:var(--gw-space-8);padding:0 var(--gw-space-4) var(--gw-space-8);
            border-bottom:1px solid var(--gw-color-neutral-100)}
  .lane__t{font:var(--gw-text-body-12-sem);letter-spacing:var(--gw-text-body-12-sem-tracking);
           color:var(--gw-color-neutral-900)}
  .lane__n{font:var(--gw-text-body-12-med);color:var(--gw-color-neutral-400);
           font-variant-numeric:tabular-nums}
  .lane__list{display:flex;flex-direction:column;gap:var(--gw-space-12)}

  /* card-shell (276:521) Size=md — radius/12, padding spacing/12, white + 1px neutral/100.
     Nested cards are 12; outer containers are 16 and inner surfaces 8. Two tiers, deliberate. */
  .card{padding:var(--gw-space-12);border-radius:var(--gw-radius-12);
        background:var(--gw-color-white);border:1px solid var(--gw-color-neutral-100)}
  /* ADDED: a 2px leading edge marking the decision lane. New rule, existing value — the same
     neutral/black that carries interaction state elsewhere on this surface. Not blue: a card
     waiting on a decision is a state, not a datum. */
  .lane--q .card{border-left:2px solid var(--gw-color-black)}
  .card__chips{display:flex;flex-wrap:wrap;gap:var(--gw-space-4);
               margin-bottom:var(--gw-space-8)}
  .card__t{margin:0;font:var(--gw-text-body-14-sem);
           letter-spacing:var(--gw-text-body-14-sem-tracking);
           color:var(--gw-color-neutral-900)}
  /* One clamped meta line, and a clamped recommendation. Anything longer is the List
     view's job — a board card answers "what is where, and how urgent", nothing more.
     CHOSEN: the 2-line clamp. No measured Kanban card exists in the system to read it off. */
  .card__m{margin:var(--gw-space-8) 0 0;font:var(--gw-text-body-12-med);
           letter-spacing:var(--gw-text-body-12-med-tracking);
           color:var(--gw-color-neutral-600);overflow-wrap:anywhere;
           display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
           overflow:hidden}
  .card__rec{margin:var(--gw-space-8) 0 0;padding-top:var(--gw-space-8);
             border-top:1px solid var(--gw-color-neutral-50);
             font:var(--gw-text-body-12-med);
             letter-spacing:var(--gw-text-body-12-med-tracking);
             color:var(--gw-color-neutral-800);
             display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
             overflow:hidden}
  .card__rec b{font-weight:600;color:var(--gw-color-black)}

  /* ── list view ── table-row (272:583) in a card-shell Size=sm wrapper (radius/8, the inner
     surface tier). Row geometry: header 44h on neutral/25 with a bottom 1px neutral/100;
     data 56h, no fill, bottom 1px neutral/25; hover neutral/25. Padding px-24, gap spacing/32.
     The 1092 measured width is what the row happens to be inside the 1120 container — the
     row FILLS its slot here rather than being pinned to it. */
  .grid{border-radius:var(--gw-radius-8);overflow:hidden;
        border:1px solid var(--gw-color-neutral-100);background:var(--gw-color-white)}
  table{width:100%;border-collapse:collapse}
  thead tr{height:44px;background:var(--gw-color-neutral-25)}
  thead th{text-align:left;padding:0 var(--gw-space-12);
           border-bottom:1px solid var(--gw-color-neutral-100)}
  thead th:first-child{padding-left:var(--gw-space-24)}
  thead th:last-child{padding-right:var(--gw-space-24)}
  /* table-cell Type=header — body-12-med on neutral/700, labels UPPERCASE, with a 12px
     ArrowsDownUp sort affordance. The affordance is drawn ONLY because sorting is wired —
     see the sort handler in the script block. A drawn control with no function is the trap. */
  .th{display:inline-flex;align-items:center;gap:var(--gw-space-4);background:none;border:0;
      padding:0;cursor:pointer;font:var(--gw-text-body-12-med);
      letter-spacing:var(--gw-text-body-12-med-tracking);
      text-transform:uppercase;color:var(--gw-color-neutral-700);border-radius:var(--gw-radius-4)}
  .th svg{width:12px;height:12px;flex:none;color:var(--gw-color-neutral-600)}
  .th[aria-sort="ascending"] svg,.th[aria-sort="descending"] svg{color:var(--gw-color-black)}
  /* table-row Type=data is measured at 56h. These rows carry the full card anatomy, so
     56 is the MINIMUM and the row grows past it — a vertical measured value is the ceiling of
     a clamp for compression, not a cap on content. Stated because it is a deviation. */
  tbody tr{min-height:56px;border-bottom:1px solid var(--gw-color-neutral-25)}
  tbody tr:hover{background:var(--gw-color-neutral-25)}
  tbody tr:last-child{border-bottom:0}
  tbody td{padding:var(--gw-space-8) var(--gw-space-12);vertical-align:middle}
  tbody td:first-child{padding-left:var(--gw-space-24)}
  tbody td:last-child{padding-right:var(--gw-space-24)}
  /* Type=label — body-12-med on neutral/black. Type=number — body-12-med on neutral/600. */
  .td-label{font:var(--gw-text-body-12-med);
            letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--gw-color-black)}
  .td-num{font:var(--gw-text-body-12-med);color:var(--gw-color-neutral-600);
          font-variant-numeric:tabular-nums;white-space:nowrap}
  .td-sub{display:block;margin-top:var(--gw-space-4);font:var(--gw-text-body-10-med);
          letter-spacing:var(--gw-text-body-10-med-tracking);
          color:var(--gw-color-neutral-500);overflow-wrap:anywhere}

  /* ── shipped timeline ── the 152px rail matches the release rail on
     preview/changelog-sheet.html, so the two pages read as one system. */
  .tl__m{margin-top:var(--gw-space-24)}
  .tl__mt{margin:0 0 var(--gw-space-8);padding:0 var(--gw-space-8);
          font:var(--gw-text-body-10-med);
          letter-spacing:var(--gw-text-body-10-med-tracking);
          text-transform:uppercase;color:var(--gw-color-neutral-400)}
  .tl__r{display:grid;grid-template-columns:152px minmax(0,1fr);gap:var(--gw-space-24);
         padding:var(--gw-space-12) var(--gw-space-8)}
  .tl__r + .tl__r{border-top:1px solid var(--gw-color-neutral-50)}
  .tl__d{font:var(--gw-text-body-12-med);color:var(--gw-color-neutral-500);
         font-variant-numeric:tabular-nums}
  .tl__t{margin:0;font:var(--gw-text-body-14-med);
         letter-spacing:var(--gw-text-body-14-med-tracking);color:var(--gw-color-neutral-900)}

  /* ── empty-state (283:889) — 480 wide, padding spacing/40, gap spacing/16, centred.
     icon-circle 40x40 radius/full on neutral/50 holding a 16px glyph on neutral/400;
     title body-16-sem on neutral/black, body body-12-med on neutral/500.
     The action is optional and omitted — there is nothing to click when a queue is empty. */
  .empty{max-width:480px;margin:0 auto;padding:var(--gw-space-40);display:flex;
         flex-direction:column;align-items:center;gap:var(--gw-space-16);text-align:center}
  .empty__c{width:40px;height:40px;border-radius:var(--gw-radius-full);
            background:var(--gw-color-neutral-50);display:flex;align-items:center;
            justify-content:center;flex:none}
  .empty__c svg{width:16px;height:16px;color:var(--gw-color-neutral-400)}
  .empty__cp{display:flex;flex-direction:column;gap:var(--gw-space-8)}
  .empty__t{font:var(--gw-text-body-16-sem);
            letter-spacing:var(--gw-text-body-16-sem-tracking);color:var(--gw-color-black)}
  .empty__b{font:var(--gw-text-body-12-med);
            letter-spacing:var(--gw-text-body-12-med-tracking);color:var(--gw-color-neutral-500)}
  /* A lane with no cards gets a line, not the 480px component — an empty-state per column
     would be five of them on an idle board. */
  .lane__none{padding:var(--gw-space-12) var(--gw-space-4);font:var(--gw-text-body-12-med);
              color:var(--gw-color-neutral-300)}

  /* 1440 is the minimum dashboard width and below it the shell scales rather than reflowing —
     but that rule governs the 260-rail app shell. This is a single 1120 surface with no rail,
     so it reflows instead, per R17's narrowing. CHOSEN breakpoints. */
  @media (max-width:1000px){
    .board{grid-template-columns:repeat(2,minmax(0,1fr))}
  }
  @media (max-width:640px){
    .wrap{padding:var(--gw-space-20) var(--gw-space-16) var(--gw-space-56)}
    .board{grid-template-columns:minmax(0,1fr)}
    .ph__t{font-size:32px}
    .tl__r{grid-template-columns:minmax(0,1fr);gap:var(--gw-space-4)}
    .grid{overflow-x:auto}
  }
"""

# Phosphor, Regular weight. ArrowsDownUp for the sort affordance, MagnifyingGlass for the
# empty state — both are what the components specify, not stand-ins.
ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-sort" viewBox="0 0 256 256"><path fill="none" stroke="currentColor"
 stroke-width="20" stroke-linecap="round" stroke-linejoin="round"
 d="M80 224V32M32 176l48 48 48-48M176 32v192M128 80l48-48 48 48"/></symbol>
<symbol id="i-search" viewBox="0 0 256 256"><path fill="none" stroke="currentColor"
 stroke-width="20" stroke-linecap="round" stroke-linejoin="round"
 d="M112 176a64 64 0 1 0 0-128 64 64 0 0 0 0 128ZM160 160l48 48"/></symbol>
</svg>"""


def esc(s):
    return html.escape(s or "")


def badge(text, tone=""):
    """The badge component at Size=Small — the only size this page uses."""
    cls = "bdg" + (" bdg--" + tone if tone else "")
    return '<span class="%s">%s</span>' % (cls, esc(text))


def age_tone(days):
    """Red past a week, yellow past three days. The word is always shown alongside."""
    if days is None:
        return ""
    if days >= OVERDUE:
        return "red"
    if days >= STALE:
        return "yellow"
    return ""


def card_chips(card, lane):
    out = []
    if lane == QUEUE:
        d = age_days(card, "since", "added", "date")
        out.append(badge("waiting " + age_label(d), age_tone(d)))
        if d is not None and d >= OVERDUE:
            out.append(badge("blocking", "red"))
    else:
        out.append(badge(lane, "black" if lane == "P0" else ""))
        d = age_days(card, "added", "date")
        if d is not None and d >= OVERDUE:
            out.append(badge(age_label(d) + " old", age_tone(d)))
    for f in flags(card, lane):
        out.append(badge(f, "yellow" if f == "needs detail" else "red"))
    return '<div class="card__chips">%s</div>' % "".join(out)


def render_card(card, lane):
    """One board card: chips, title, one meta line, and the recommendation if there is one."""
    # `surface` is the most useful single line on a board — it says where the work is. Falling
    # back to `blocked` then `needs` means a card that cannot say where always says why.
    meta = (card["keys"].get("surface") or card["keys"].get("blocked")
            or card["keys"].get("needs") or "")
    rec = card["keys"].get("rec")
    return ('<article class="card">%s<h3 class="card__t">%s</h3>%s%s</article>'
            % (card_chips(card, lane), esc(card["title"]),
               ('<p class="card__m">%s</p>' % esc(meta)) if meta else "",
               ('<p class="card__rec"><b>Rec:</b> %s</p>' % esc(rec)) if rec else ""))


def render_kanban(sections):
    lanes = []
    for name in LANES:
        cards = sections[name]
        body = "".join(render_card(c, name) for c in cards) or \
            '<p class="lane__none">Empty</p>'
        lanes.append(
            '<div class="lane%s"><div class="lane__hd"><span class="lane__t">%s</span>'
            '<span class="lane__n">%d</span></div><div class="lane__list">%s</div></div>'
            % (" lane--q" if name == QUEUE else "", esc(name), len(cards), body))
    return '<div class="board">%s</div>' % "".join(lanes)


def empty(title, body):
    return ('<div class="empty"><div class="empty__c">'
            '<svg aria-hidden="true"><use href="#i-search"/></svg></div>'
            '<div class="empty__cp"><span class="empty__t">%s</span>'
            '<span class="empty__b">%s</span></div></div>' % (esc(title), esc(body)))


LIST_COLS = [("task", "Task"), ("state", "State"), ("age", "Age"), ("status", "Status")]

# Keys shown under a list row, in reading order: where, the rule, and what done means.
ROW_DETAIL = ["surface", "constraint", "done", "options", "rec", "blocked", "needs"]


def render_list(sections):
    rows = []
    for name in LANES:
        for c in sections[name]:
            d = (age_days(c, "since", "added", "date") if name == QUEUE
                 else age_days(c, "added", "date"))
            fl = flags(c, name)
            status = "".join(badge(f, "yellow" if f == "needs detail" else "red")
                             for f in fl)
            if name == QUEUE:
                status = badge("awaiting decision",
                               age_tone(d) or "") + status
            detail = "".join(
                '<span class="td-sub"><b>%s</b> %s</span>' % (esc(k), esc(c["keys"][k]))
                for k in ROW_DETAIL if c["keys"].get(k))
            rows.append(
                '<tr data-age="%d" data-lane="%d">'
                '<td><span class="td-label">%s</span>%s</td>'
                '<td>%s</td>'
                '<td><span class="td-num">%s</span></td>'
                '<td>%s</td></tr>'
                % (-1 if d is None else d, LANES.index(name), esc(c["title"]), detail,
                   badge(name, "black" if name == "P0" else ""),
                   esc(age_label(d)), status or '<span class="td-num">—</span>'))
    if not rows:
        return empty("Nothing open", "Every card is either shipped or iced. "
                                     "Add one to BACKLOG.md and rerun scripts/board.sh.")
    head = "".join(
        '<th><button class="th" type="button" data-sort="%s" aria-sort="none">%s'
        '<svg aria-hidden="true"><use href="#i-sort"/></svg></button></th>' % (k, esc(l))
        for k, l in LIST_COLS)
    return ('<div class="grid"><table><thead><tr>%s</tr></thead>'
            '<tbody data-rows>%s</tbody></table></div>' % (head, "".join(rows)))


def render_shipped(cards):
    if not cards:
        return empty("Nothing shipped yet",
                     "Move a card to Completed with a date and it appears here.")
    dated = sorted([c for c in cards if c["date"]], key=lambda c: c["date"], reverse=True)
    undated = [c for c in cards if not c["date"]]

    months, order = {}, []
    for c in dated:
        key = c["date"][:7]
        if key not in months:
            months[key] = []
            order.append(key)
        months[key].append(c)

    out = []
    for key in order:
        label = dt.date.fromisoformat(key + "-01").strftime("%B %Y")
        rows = []
        for c in months[key]:
            when = dt.date.fromisoformat(c["date"]).strftime("%-d %b")
            shipped = c["keys"].get("shipped")
            rows.append(
                '<div class="tl__r"><div><span class="tl__d">%s</span></div>'
                '<div><p class="tl__t">%s</p>%s</div></div>'
                % (esc(when), esc(c["title"]),
                   ('<div style="margin-top:var(--gw-space-4)">%s</div>'
                    % badge(shipped, "green")) if shipped else ""))
        out.append('<div class="tl__m"><p class="tl__mt">%s</p>%s</div>'
                   % (esc(label), "".join(rows)))
    if undated:
        rows = "".join(
            '<div class="tl__r"><div><span class="tl__d">no date</span></div>'
            '<div><p class="tl__t">%s</p></div></div>' % esc(c["title"]) for c in undated)
        out.append('<div class="tl__m"><p class="tl__mt">No date recorded</p>%s</div>' % rows)
    return "".join(out)


# The view switcher and the column sort. Both are real: every data-* hook below is bound here,
# and every <button> the markup draws is reachable by one of these selectors. A component's
# anatomy is not a checklist — an affordance that does nothing is the trap this guards.
SCRIPT = r"""
(function () {
  var tabs = [].slice.call(document.querySelectorAll('[data-view]'));
  var panels = {};
  [].forEach.call(document.querySelectorAll('[data-panel]'), function (p) {
    panels[p.getAttribute('data-panel')] = p;
  });

  function show(name) {
    tabs.forEach(function (t) {
      t.setAttribute('aria-selected', String(t.getAttribute('data-view') === name));
    });
    Object.keys(panels).forEach(function (k) { panels[k].hidden = k !== name; });
    try { localStorage.setItem('gw-board-view', name); } catch (e) {}
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () { show(t.getAttribute('data-view')); });
  });

  /* Remember the last view, so reopening the board does not always dump you on Kanban.
     Wrapped: localStorage throws outright in some privacy modes. */
  var saved = null;
  try { saved = localStorage.getItem('gw-board-view'); } catch (e) {}
  show(saved && panels[saved] ? saved : 'kanban');

  /* Sort — the ArrowsDownUp affordance on each header is drawn only because this exists.
     Lane and age sort numerically off data-* attributes; task and status sort on text. */
  var body = document.querySelector('[data-rows]');
  if (!body) return;
  var dir = {};
  [].forEach.call(document.querySelectorAll('[data-sort]'), function (btn) {
    btn.addEventListener('click', function () {
      var key = btn.getAttribute('data-sort');
      dir[key] = dir[key] === 'asc' ? 'desc' : 'asc';
      var sign = dir[key] === 'asc' ? 1 : -1;
      [].forEach.call(document.querySelectorAll('[data-sort]'), function (o) {
        o.setAttribute('aria-sort', o === btn
          ? (dir[key] === 'asc' ? 'ascending' : 'descending') : 'none');
      });
      var rows = [].slice.call(body.querySelectorAll('tr'));
      rows.sort(function (a, b) {
        var x, y;
        if (key === 'age') { x = +a.dataset.age; y = +b.dataset.age; }
        else if (key === 'state') { x = +a.dataset.lane; y = +b.dataset.lane; }
        else {
          var i = key === 'task' ? 0 : 3;
          x = (a.cells[i].textContent || '').trim().toLowerCase();
          y = (b.cells[i].textContent || '').trim().toLowerCase();
        }
        return x < y ? -sign : x > y ? sign : 0;
      });
      rows.forEach(function (r) { body.appendChild(r); });
    });
  });
})();
"""


def waiting_text(sections):
    """The queue as plain text, for the Stop hook and the morning digest.

    Prints nothing when the queue is empty — a notifier that says "nothing to report" every
    morning is a notifier people turn off.
    """
    cards = sections[QUEUE]
    if not cards:
        return ""
    lines = []
    for c in cards:
        days = age_days(c, "since", "added", "date")
        mark = " (OVERDUE)" if days is not None and days >= OVERDUE else ""
        lines.append("%s — waiting %s%s" % (c["title"], age_label(days), mark))
    return "\n".join(lines)


def main():
    sections = parse(sys.stdin.read())

    if "--titles" in sys.argv:
        # `section<TAB>title` per card. The Stop hook diffs two of these to work out what
        # actually changed, so it can say "new in P1: …" rather than "the file changed".
        for name in SECTIONS:
            for c in sections[name]:
                sys.stdout.write("%s\t%s\n" % (name, c["title"]))
        return 0

    if "--waiting" in sys.argv:
        out = waiting_text(sections)
        if out:
            sys.stdout.write(out + "\n")
        return 0 if out else 1

    favicon = ""
    here = os.path.dirname(os.path.abspath(__file__))
    fav = os.path.join(here, "_favicon.txt")
    if os.path.exists(fav):
        with open(fav) as fh:
            favicon = fh.read().strip()

    version = "unknown"
    pj = os.path.join(here, "..", ".claude-plugin", "plugin.json")
    if os.path.exists(pj):
        import json as _json
        with open(pj) as fh:
            version = _json.load(fh).get("version", "unknown")

    waiting = sections[QUEUE]
    open_cards = sum(len(sections[c]) for c in COLUMNS if c != "Icebox")
    shipped = len(sections[DONE])
    oldest = max((age_days(c, "since", "added", "date") or 0)
                 for c in waiting) if waiting else None

    stamp = ('{"pluginVersion":"%s","createdBy":"Utsav Singh","createdAt":"%s",'
             '"registry":"https://gushwork-design.vercel.app/exports/dashboard/'
             'component-registry.json",'
             '"changelog":"https://gushwork-design.vercel.app/preview/changelog-sheet.html",'
             '"components":[%s]}'
             % (version, TODAY.strftime("%-d %b %Y"),
                ",".join('"%s"' % c for c in BUILD_COMPONENTS)))

    meta_bits = ["Generated %s" % TODAY.strftime("%-d %b %Y")]
    if waiting:
        meta_bits.append("oldest decision waiting %s" % age_label(oldest))

    tabs = [("kanban", "Board", len(waiting) + open_cards + len(sections["Icebox"])),
            ("list", "List", len(waiting) + open_cards + len(sections["Icebox"])),
            ("shipped", "Shipped", shipped)]

    print("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Backlog — Gushwork Design System</title>
<link rel="icon" type="image/svg+xml" href="%(favicon)s">
<link rel="stylesheet" href="../foundation/tokens.css">
<style>%(css)s</style>
</head>
<body>
<!-- gushwork-build:%(stamp)s -->
%(icons)s
<div class="wrap">

  <header class="ph">
    <h1 class="ph__t">Backlog</h1>
    <div class="ph__row">
      <div class="ph__l">
        <div class="tabs" role="tablist" aria-label="Board view">%(tabs)s</div>
        <span class="meta">%(meta)s</span>
      </div>
      <span class="meta">Source BACKLOG.md · rebuild with scripts/board.sh</span>
    </div>
  </header>

  <div data-panel="kanban" role="tabpanel">
    %(kanban)s
  </div>

  <div data-panel="list" role="tabpanel" hidden>
    <div class="sh"><div class="sh__g"><span class="sh__t">All open work</span>
      <span class="sh__q">every lane, sortable</span></div></div>
    %(list)s
  </div>

  <div data-panel="shipped" role="tabpanel" hidden>
    <div class="sh"><div class="sh__g"><span class="sh__t">Shipped</span>
      <span class="sh__q">newest first, by month</span></div></div>
    %(shipped)s
  </div>

</div>
<script>%(script)s</script>
</body>
</html>""" % dict(
        favicon=favicon,
        css=CSS,
        stamp=stamp,
        icons=ICONS,
        tabs="".join(
            '<button class="tab" type="button" role="tab" data-view="%s" '
            'aria-selected="%s">%s<span class="tab__n">%d</span></button>'
            % (k, "true" if k == "kanban" else "false", esc(label), n)
            for k, label, n in tabs),
        meta=esc(" · ".join(meta_bits)),
        kanban=render_kanban(sections),
        list=render_list(sections),
        shipped=render_shipped(sections[DONE]),
        script=SCRIPT,
    ))

    flagged = sum(1 for c in COLUMNS for card in sections[c] if flags(card, c))
    sys.stderr.write(
        "Wrote %s — %d waiting, %d open, %d shipped%s\n"
        % (os.environ.get("OUT", "the board"), len(waiting), open_cards, shipped,
           (", %d needing detail" % flagged) if flagged else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
