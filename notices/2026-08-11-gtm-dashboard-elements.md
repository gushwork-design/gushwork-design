# GTM Command Center — 21 new elements for the dashboard surface

Built **11 Aug 2026**. Files: `preview/dashboard-new-elements.html`,
`preview/dashboard-audit-sheet.html`

Three exported pages of the GTM Command Center (`overview`, `meta-ads`, `admin/targets`) were
inventoried against `exports/dashboard/` — 62 components, 205 distinct `tag + class` pairs. Of
those, **8 can be instanced today, 31 need a variant on a component that exists, 2 are settled
by decision, and 21 had nothing at all.** This is the 21.

All of them are **RULED, not measured** — nothing here exists in Figma yet. Of the six rulings
checked in the August measurement passes, one held. Treat every value below accordingly.

## Created

Prefix `gwd-`, light surface only. Dark treatments follow the per-component `Mode` convention
and are a second pass — the source dashboard's global `.dark` class swap has no equivalent in
the library, and inventing one is a bigger decision than these elements.

### `gwd-figure` — the tabular numeral run
Four sizes (`sz-value` `--gw-text-h5`, `sz-rate` `body-20-sem`, `sz-cell` `body-14-med`) and
four tones. Every figure in the dashboard is a number in a column, and a column of numbers must
not shift width as it updates. **The library had no numeral treatment at all** — `kpi-card` and
`analytics-card` both set their value in the display face with no tabular figures.

### `gwd-pace` — the pace badge
The three-state pill that says whether a metric will *land*, as against `kpi-card`'s inline
delta badge, which says which way it *moved*. Different question, so a different element rather
than a restyle. Colours are **Badge's own documented Green mapping** (`green-100` fill /
`green-500` text) extended to Yellow and Red at the same steps. A fourth `st-info` state on
`primary-50` / `primary-600` carries data labels like "Rescheduled", which are not signals.

### `gwd-meter` — the in-card progress bar
`section/progress-bar` is a 1084×116 panel with a 32px blue track, an icon tile and an inset
percentage. This is the bar alone, for use inside a card: `--gw-space-8` tall,
`--gw-radius-full`, fill carries the pace colour. `sz-inline` is the `--gw-space-40` form that
sits in a table cell beside a value/target pair.

### `gwd-info-dot`, `gwd-today-tag`, `gwd-section-label`, `gwd-cell-hint`
Four marks with no equivalent. The info dot is `--gw-space-16` square on a `neutral-200`
hairline and is the **only** tooltip trigger — in the source it marked one card while the
tooltip fired from anywhere on that card. `gwd-cell-hint` is the dotted-underline cell that
signals a hover explanation.

### `gwd-kv` — the key-value row
Label left, tabular value right. Appears in three different cards in the source with three
different gaps (6, 10 and 6px at a 14px font). One element, one gap: `--gw-space-8`. Marks up
as a `<dl>` so the pairing is real rather than visual.

### `gwd-range` + `gwd-range-meta` — the date-range switch
A radio group: it selects a value, it does not navigate. **No base existed** —
`controls/toggle` is a switch and `controls/tab` is navigation. The last segment opens
`dropdown-options Style=Calendar`, which is itself still RULED and has no range selection, so
that remains open. `gwd-range-meta` is the "Day 10 of 31" label beside it.

### `gwd-pace-card` — the missing `kpi-card` mode
Label (+ optional info dot) / pace badge / value / `of N` + % / meter. Same `--gw-radius-12`
and `--gw-space-20` padding as the measured `kpi-card` so the two tile together, but no 80px
spacer — the meter occupies that space. **Emphasis is elevation only** (`--gw-shadow-s3` + a
`primary-alpha-40` hairline); the value never changes size.

### `gwd-stat-card` — two modes `analytics-card` has no form of
A figure with a key-value block beneath it, and a block with no figure at all (the source's
"Unit Economics" card). Both reuse `gwd-kv`.

### `gwd-rate` + `gwd-rate-panel` — actual against required
Rate per day with the required rate under it. The figure takes the pace colour; **the "need"
line never does** — it is a reference, not a signal. `gwd-rate-panel` is the card of four.

### `gwd-notice` + `gwd-notice-stack` — the persistent inline alert
**A new placement for `toast`, not a new component.** Toast already ships
`Mode` [Light, Dark] × `State` [Error, Warning, Success, Info]. What it does not do is persist:
it is 360 wide, one line, and auto-dismisses at `--gw-toast-dismiss` (4s). This is the same
four states, full width, stacked, dismissed by hand, scoped to a source channel. Each state is
its own ramp's 25 / 100 / 700 steps with a 500 mark. **Info is a state the source dashboard
never had**, and it arrives free.

### `gwd-card-head` + `gwd-card-foot` + `gwd-btn` + `gwd-btn-quiet` + `gwd-field`
A card header that carries controls, which `section/header` does not, and a footer bar, which
nothing does. `gwd-btn` is the page action — **black on white** — and `gwd-field` is
`input/text-field`'s geometry at `--gw-radius-8`.

### `gwd-page-title` — the page title row
Title left at `--gw-text-h7`, range controls right. `h7` (22 Medium display) is the ramp's
smallest display step; the source used 20px, which the display ramp does not have.

### Table parts — grouped header, inline-bar cell, actions cell, pinned column
Three additions to `table`, assembled as `gwd-daily-table`. The grouped header uses real
`colspan`/`rowspan` with `scope` on **both** rows — the source shipped two different
implementations of the same header, one of which had no `scope` at all. Hover stays
`neutral-25` as measured; the today row is `primary-alpha-10`.

## Modified

Nothing measured was overridden. Two off-ramp values in the source were swapped for the nearest
existing step, and both are visible changes rather than rounding:

### meter height — `6px` → `--gw-space-8`
6 is not a spacing step. At 8px the bar reads slightly heavier under a 32px figure than the
source's did. The alternative is adding a 6px step that no other component needs.

### control radius — `6px` → `--gw-radius-8`
6 is not a radius step. Applies to the range switch's segments, the field and the buttons. The
range switch's outer shell steps to `--gw-radius-10` to keep the 2px inset reading correctly.

Two further values had no token and were reported rather than invented — see **Tokens**.

## Worth a decision

**1. The status green and red both shift.** `--on-track #0d9463` is an emerald and
`--critical #dc2626` is Tailwind's red; **neither exists anywhere in the Gushwork ramps, in
either theme.** Gushwork's green ramp is a true green and its red ramp is rose. There was no
token-safe way to keep the source colours, so these use `green-500` and `red-500` on the 100
steps, following Badge. The alternative is adding both hexes as ramp steps — a palette change,
and it would leave the system with two greens that differ by a step. **The yellows needed no
decision: `--warning`, `--warning-bg` and `--warning-border` were already byte-identical to
`yellow-600 / 25 / 100`, and dark-mode `--warning` to `yellow-300`.** Whoever built the source
took the amber scale from the system and then hand-picked green and red out of Tailwind.

**2. Emphasis is elevation only.** The source promoted its hero card by ringing it, adding an
indigo glow (`rgba(67,56,202,.06)` — the pre-`#0070FF` brand) and bumping the value from 30 to
36px. Which card gets promoted was undefined across the pages: Overview promotes one, Meta Ads
promotes two, and the spend total uses a third treatment. Here the value stays at
`--gw-text-h5` in both modes and emphasis is `shadow-s3` plus a hairline. The alternative is a
size step, and the display ramp jumps 32 → 38, which is large for a card that tiles with its
siblings.

**3. The pinned column is not darkened.** `table-row` rules explicitly against darkening the
first column to emphasise the row's identifier — "it fights the component's deliberate
quietness". All three of the source's tables darken it, weight it and stick it. I kept the
ruling: the pinned column is distinguished by position and stickiness alone. Either the ruling
holds and the source is wrong, or the deviation is right across three tables and should be
**promoted** into `table-row`.

## Tokens

**86 distinct `--gw-*` tokens referenced. Every one resolves against
`foundation/tokens.css` — verified, not asserted.** The element block contains no raw hex, no
`rgba()`, and no font-size, radius, shadow or duration literal. **No colour, type step, radius,
shadow or spacing value was introduced.**

The only lengths written directly are `1px` hairlines — per `DECISIONS.md` → **R5**, sub-pixel
and hairline borders build as 1px — and two letter-spacing values, both listed below.

Swaps from source to token:

| Role | Source | Token used |
|---|---|---|
| on-track | `#0d9463` / `#ecfdf5` / `#bbf7d0` | `green-500` on `green-100` |
| warning | `#b45309` / `#fffbeb` / `#fde68a` | `yellow-600` on `yellow-100` |
| critical | `#dc2626` / `#fef2f2` / `#fecaca` | `red-500` on `red-100` |
| info | *no such state* | `primary-600` on `primary-50` |
| brand accent | `#0070FF` | `primary-500` — already exact |
| primary control | blue fill | `--gw-color-black` |
| surface / hairlines | `#fff` / `#e2e4ed` / `#eff0f6` | `white` / `neutral-200` / `neutral-100` |
| page ground | `#f8f9fc` | `neutral-25` |
| label / quiet text | `#4B5563` / `#9CA3AF` | `neutral-800` / `neutral-500` |
| card value | 30–36px Inter 700 | `--gw-text-h5` |
| page title | 20px 600 | `--gw-text-h7` |
| label / caption sizes | 13px, 11px | `body-12-*`, `body-10-*` |
| card radius / shadow | 12 / `0 1px 2px rgba(0,0,0,.04)` | `--gw-radius-12` / `--gw-shadow-s2` |
| emphasis | indigo `rgba(67,56,202,.06)` | `--gw-shadow-s3` + `primary-alpha-40` |
| motion | 150 / 200 / 500ms | `--gw-motion-fast` |
| focus | `2px solid` brand-500 | `--gw-focus-ring` / `--gw-focus-offset` |

### Values in use with no token — gaps to report, not inventions

**1. Tabular numerals.** Every figure in a data column needs Inter with
`font-variant-numeric: tabular-nums`, and no `--gw-text-*` token carries it. The ramp sets card
values in the display face, so there is nowhere for this to bind. `gwd-figure` declares it
directly. **This is the one real hole in the type ramp for dashboard work** — it affects every
table cell and every KPI value in the system, not just these elements.

**2. Uppercase tracking.** `gwd-section-label` needs `.1em` and `gwd-today-tag` `.06em` on a
10px uppercase run. `--gw-text-body-10-sem-tracking` is `0`, and an uppercase run at 10px needs
letter-spacing to stay legible. Both values are set in the element.

### Not created, deliberately

The **shell and the tab bar**. `dashboard-build` assumes a left rail at a 1440 minimum that
scales below it; the GTM dashboard has a 56px top header and a scrolling 9-item tab bar. That
build stands by decision, so the rail-versus-top-header question is closed and needs no
component. The six rail components it displaces — `side-panel`, `list-item`, `user-card`,
`avatar`, and both dropdown controls — stay in the library for dashboards that do use a rail.

The **31 Extend items** are also not here. They are variants on components that already exist
and belong in those components' own specs, not in a new-elements pass.
