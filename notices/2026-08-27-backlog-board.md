# The backlog board — new elements and deviations

Built 27 Aug 2026. Files: `preview/board.html` (generated), `scripts/_board.py`,
`scripts/board.sh`, `scripts/hooks/backlog-sync.sh`, `scripts/hooks/backlog-context.sh`,
`BACKLOG.md`.

A Kanban board over `BACKLOG.md` with three views — board, sortable list, shipped timeline.
Uses `page-header`, `tab-group`, `tab-item`, `card-shell`, `table-row`, `table-cell`,
`section-header`, `badge`, `empty-state`. Every one of those measured values was asserted
against the render with `getBoundingClientRect()` and `getComputedStyle()`, not eyeballed —
numbers in the Verified section below.

## Created

### `lane` — a Kanban column
Five lanes: `Waiting on you`, `P0`, `P1`, `P2`, `Icebox`. A header row (title + count, 1px
`neutral/100` bottom rule) over a `spacing/12` stack of `card-shell Size=md` cards.

The library has no Kanban lane and nothing composes into one — `section/table` is a table,
`section/Container` is a single panel. Built from tokens only. Lane *width* is not a value at
all: five `1fr` columns in the available width, reflowing to two at 1000 and one at 640.

### The board card
`card-shell Size=md` (`radius/12`, `spacing/12`) holding a chip strip of `badge Size=Small`,
a `body-14-sem` title, one 2-line-clamped meta line, and a 2-line-clamped recommendation.

The 2-line clamp is **chosen, not measured** — no Kanban card exists to read it off. It is
there because the first build put a 400px card in a 250px lane, which is not a board.

### ADDED rule: a 2px leading edge on the decision lane
`border-left: 2px var(--gw-color-black)` on cards in `Waiting on you`. New rule, **existing
value** — the same `neutral/black` that carries interaction state on this surface. Not blue: a
card awaiting a decision is a state, not a datum.

## Modified

### `badge` light treatment — `{Colour}/500` label → `{Colour}/600`
The documented light pairing is a `/25` fill with a `/500` label. At the component's own
`body-12-med`, **all three signal colours fail WCAG AA** (4.5:1 for small text):

| Pair | Measured | AA |
|---|---|---|
| `red-25` / `red-500` | 4.28:1 | fail |
| `yellow-25` / `yellow-500` | 3.07:1 | fail |
| `green-25` / `green-500` | 3.15:1 | fail |
| `red-25` / `red-600` | 5.72:1 | pass |
| `yellow-25` / `yellow-600` | 4.84:1 | pass |
| `green-25` / `green-600` | 4.79:1 | pass |

Labels are one step darker here. **Fills are unchanged.** This is not a board problem — it is
every light badge in the system at Small.

### `table-row Type=data` — 56h → `min-height: 56px`
List rows carry the full card anatomy (surface, constraint, done, options, rec), so they grow
past 56. The measured value is still the floor. Consistent with build-rule 4, where a vertical
measured value is the ceiling of a clamp against *compression*, not a cap on content.

### The board scrolls sideways, and holds a 288px lane floor
Five fitted lanes inside the measured 1120 came out at **198px**, which is not a card. Lanes
are now a fixed 288 and the board scrolls horizontally, as the reference does. This is a
second scroll region on the other axis from the page — build-rule 1 ("exactly one region
scrolls") governs the 260-rail app shell, and this is a single surface with no rail. Stated,
not assumed.

### Content column — measured 1120 → 1376 for the board only
`page-header`, `section-header`, `card-shell` and `table-row` are all measured against 1120,
and the header, list and timeline all sit at 1120. The board does not: five lanes inside 1120
come out at **198px**, too narrow to read a card in. The board alone runs gutter-to-gutter and
the lanes land at **250px**. Horizontal measured values are never clamped — this widens a
column rather than shrinking a component.

## Not created, deliberately

A 20px `badge`. The first build invented one for the dense rows; the component ships
`Small`/`Medium`/`Large` only and `Small` is 24h / `body-12-med`. Interpolating a variant is
how a build drifts, so it was removed and `Small` is used throughout.

A dark theme. `table-row`, `tab-group` and `input` have **no dark variants** in v2 — a dark
board would need values that do not exist. Light only, matching `changelog-sheet.html`.

A blue badge. `Blue` is undefined in the badge rule, so it is unused rather than pressed into
meaning "info".

## Redesigned the same day, from a supplied reference

Utsav supplied a Taskk screenshot and asked for layout reference, clarifying it is **not a
dashboard — "you can take some reference"**. Taken as loose inspiration, not a spec:

**Taken (structure and content):** breadcrumb over title over toolbar; tabs, a rule, then
actions; columns as tinted *surfaces* carrying an accent bar, a count pill and a per-column
add; a four-tier card — grouping meta, title, chips, stat footer; columns scrolling sideways
with the last one visibly cut off, which is the affordance.

**Not taken (visual treatment):** every colour, type style, radius, shadow and spacing is a
Gushwork token, and the parts are the measured v2 components. Its side panel was excluded on
instruction.

**Not taken (dead controls).** The reference draws `Import`, `+ New Board` and a per-column
`⋮`. A static file generated from a markdown source cannot create a board or import anything,
so none of them is drawn. They are replaced by controls that work: a filter over title and
surface, a `Copy rebuild command` button, and `+ Add new` per lane which copies a card
template pre-headed with that lane's section. Clipboard uses the three tiers from
`new-component-notice.md` — this file is opened from `file://` every time someone
double-clicks it, so `navigator.clipboard` fails in the common case.

**Its card slots, filled with derived data rather than invented data.** The reference's
`Client: Stellar` becomes `Area`, the top-level directory of every path in `surface:`. Its
category tag pills are dropped. Its assignee row is dropped: there is no assignee in this
system and an avatar would be fake data. Its three footer stats become the count of files the
card touches, how many of its required keys are filled, and its age.

`surface:` is free prose with paths in it, not a list — real values include *"scripts/_board.py,
copy the DRIFT_JS block from preview/_build_x.py"*. Splitting on commas produced areas called
"patterned on preview". Paths are extracted by regex and only the top-level segment is kept.

**No lane badge on a board card.** The column already states the state, and a `P2` chip on
every card in the P2 column made all of them look flagged — which is exactly when a real flag
stops being visible. The List view keeps its lane badge; there is no column there to imply it.

## Worth a decision

1. **The badge AA failure is a system finding, not a board one.** Every light badge at
   `Small` fails contrast on red, yellow and green as documented. Either the `/600` label
   becomes the spec (Promote) or the fills move darker in Figma. Until one of those lands,
   every build that reads the rule literally ships failing contrast.

2. **Two content widths on one page.** The board breaks the measured 1120 because the
   measurement was never taken for a lane. If 1120 should hold everywhere, the board needs
   three lanes rather than five, or a horizontal scroller.

## Verified, not eyeballed

`tab-group` 36h · `radius/12` · pad 4 · **gap 4** (not the v1's 8) · fill `#f1f2f3`
`neutral/50` · border 1px `#e7e8e9` `neutral/100`. `tab-item` 28h · `radius/8` · active fill
`#0d0d0d` `neutral/black` with a white label · inactive `#262a2e` `neutral/900`, **not greyed**.
`card-shell md` `radius/12` pad 12. Canvas `#f7f8f9` `neutral/25`. Header column 1120.
Title `600 44px/1.2 Vert Grotesk Display`. No horizontal document scroll at 1440, 1000 or 600.

## Tokens

54 custom properties referenced, all resolving in `foundation/tokens.css`. **No new colour,
type, radius, shadow or spacing value was introduced.**

One gap to report, not an invention: the five `Dashboard/display-*` styles still have no
tokens (R15). The page title uses the literal `600 44px/1.2` spec with a comment saying so.

## Known incomplete

The `gushwork-build:` stamp is present, so `scripts/check-drift.sh` works. The **in-page**
drift notice is not wired — it is a P2 card on the board itself. Same for a
`_verify_board.py`; the measurements above were taken by hand this once.
