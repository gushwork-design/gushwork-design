# Website performance dashboard — new elements and deviations

Built 7 Aug 2026. Files: `/Users/utsavsingh/Gushwork Design/website-performance/{_build.py,index.html}`

A Gushwork site-performance dashboard — `dashboard-build` shell, `section/header` (sticky), then
`section/card-layout` `KPI cards=2` · `section/progress-bar` · `section/Container`+`Graph
Type=Line` · `section/With Dropdown` · `section/Container`+`Graph Type=Bar` · `section/table`.
All figures are illustrative; the header carries a `Sample data` Badge.

Styling reuses `preview/_meta_ads_app.css` verbatim rather than rebuilding it. Everything below
is what sits on top of that file.

---

## Defects found in the shared reference build

Two of these were live in `preview/_meta_ads_app.css` and its sprite pattern, not introduced
here. **Both should land upstream.**

### 1. Every Phosphor icon renders BLACK instead of inheriting `currentColor`

The committed icon files carry `fill="currentColor"` on the **outer `<svg>`**:

```svg
<svg xmlns="..." viewBox="0 0 256 256" fill="currentColor"><path d="…"/></svg>
```

Building a sprite by stripping that wrapper into a `<symbol>` **drops the only `fill` in the
file** — the inner `<path>` has none, so it falls back to black. Result: the icon inside the
blue `primary-alpha-10` section tile rendered black, and the `ArrowUpRight` inside the
kpi-card's green badge rendered black instead of `green-300`.

`fill` is an inherited presentation attribute, so the fix is to re-apply it to the `<symbol>`:

```html
<symbol id="i-chart" viewBox="0 0 256 256" fill="currentColor">…</symbol>
```

`shared-components.md` already says *"Colour via `currentColor` only"* and *"an `<img src>` …
falls back to black"* — this is a third way to lose it that the guidance does not cover.
**Worth adding a line to `shared-components.md`:** when you inline a committed icon into a
sprite, carry the `fill` onto the symbol.

### 2. `.sec__caret` sizes its span but not its `<svg>` — carets render 300×150

`.sec__caret{width:12px;height:12px}` sizes the **span**; nothing sizes the `<svg>` inside it, so
the section collapse caret rendered at the SVG default **300×150 — 25× the measured 12px** —
pushing `.sec__hd` to a scrollWidth of 1184 against a 900 client box. `.sec{overflow:hidden}`
clipped it, which is why it never looked broken and survived the reference build. Every other
icon holder in that file sizes its own `svg`; this one was missed.

```css
.sec__caret svg{width:12px;height:12px;display:block}
```

### 3. `.li:hover` applies to the nav GROUP LABEL, which has no hover variant

The group label is a `list-item` too — `Property 1=Variant4, Label=yes` — so it inherits
`.li:hover{background:neutral-25}` and lights up under the cursor. The component set has four
variants, and **only the three `Label=no` ones carry hover and selected states.** There is no
hover variant for `Label=yes`, because the label is not a target: it labels the nav, it does not
navigate.

```css
.li.li--group,.li.li--group:hover{background:none;cursor:default}
```

Also worth marking up correctly: nav rows are `<button>`, group labels are `<div>`. A label that
looks pressable but is not is a worse defect than a missing hover.

---

## Ruled — toast auto-dismiss is 4s

`exports/dashboard/toast.md` closes with *"Auto-dismiss is still undefined … Do not invent
either."* That gap is now closed by decision, not by guess:

> **Toasts auto-dismiss after 4 seconds.** Ruled by Utsav, 7 Aug 2026.

Implemented here as a 4s timer that **resets** if a second toast fires and **clears** on manual
dismiss, so toasts never stack timers or ghost-hide a later message. **This belongs in
`toast.md`** — otherwise the next build re-reads "undefined" and re-decides it differently.

Two things the ruling does *not* cover, left alone rather than extended: whether the timer pauses
on hover or focus, and whether it applies to `State=Error` (an error that vanishes in 4s can be
missed). Worth a follow-up if either matters.

---

## Ruled — blue is a data colour, not a control-state colour

The calendar's selected day was built blue and corrected to **black**:

> **A selected date takes `--gw-color-black`, not `--gw-color-primary-500`.** Hover is
> `--gw-color-neutral-100`. Ruled by Utsav, 7 Aug 2026.

This is more general than one component, and it sharpens a rule the system currently states too
narrowly. `button.md` and the surface defaults say *"never a blue button **fill**"* and *"blue
remains valid as a status/signal colour"* — which leaves **control states** unclassified. A
selected calendar cell is neither a button fill nor a status signal, so both readings were
available and the blue one was wrong.

The sharper statement: **blue carries data and status; black carries interaction state.** The
progress-bar fill and the chart series stay blue because they are data. Selection, active and
pressed states go black.

**One open item this exposes:** `controls/toggle` `State=On` is currently built blue here, and by
the rule above it is a control state and should be black. It was not flagged, so it is left as
built — but the two cannot both be right. Worth a one-line answer.

---

## Ruled — the user-card row is not a control

The whole card was given a hover, borrowed from the measured `State=Hover` variant. Corrected:

> **On this dashboard the dots button is the only interactive target in the user-card.** The row
> itself takes no hover; the dots button carries hover and the open state. Ruled by Utsav,
> 7 Aug 2026.

The measured `State=Hover` variant (`2125:198`) is presumably for products where the whole row
opens a profile. Since the export does not say what the hover is *for*, **worth one line in
`section-elements.md`** saying when the row is a target and when only the menu button is.

The menu is also anchored **right, directly above the dots button** — not left of the card.

---

## Created

Nothing below introduces a colour, size, radius, shadow or type value that is not already a
token. Where a Figma variant exists but its appearance is unmeasured, the nearest measured
neighbour is used and named.

### `.hdr__top` — title row in `section/header`
`section/header` (`2140:16372`) draws a page title and a toolbar. It has no slot for a Badge, and
the `Sample data` marker has to sit where it cannot be scrolled out of view. Flex row, gap
`--gw-space-12`; the measured 20px title→toolbar gap is untouched. **Most likely to recur** —
every sample-data dashboard needs it.

### `dropdown-options` `Style=Simple` — the open menu
`controls.md` records `State=Open`'s size but not its fill, border or shadow. Built as a white
panel at `--gw-radius-8` on `--gw-shadow-s3` with a `neutral-100` inset hairline, option rows at
the measured 8px padding, `--gw-text-body-12-med`, check glyph in `primary-500` on the selected
row. Closes on outside click and on Escape.

### `dropdown-options` `Style=Calendar` — reached from the `Custom` tab
Built to the measured geometry: 200 wide, 7 day headers + 35 day cells at 24×24 `--gw-radius-4`.
Hover `--gw-color-neutral-100`, selected `--gw-color-black` on white text (see the ruling above).
Previously `Custom` was inert.

**Single-select, not a range.** The variant is a bare 7×5 grid with **no range affordance drawn**
— no start/end cell, no in-between fill, no two-month view. A `Custom` date filter in a
`section/header` almost certainly wants a range, so this is a real gap: either the Calendar
variant needs range states drawn, or the toolbar needs a different control. Not invented here.

### `controls/toggle` `Size=Small`
`controls.md` gives the sizes (44×24, pad 4, gap 4) and the Off/On child-order swap, but **no
colours**. Track off `--gw-color-neutral-200`, on `--gw-color-primary-500`, knob white on
`--gw-shadow-s2`. Blue here is a state signal, the same use as the `progress-bar` fill — the
no-blue rule bans *button* fills only. Wired to the AI section so flipping it actually changes
the per-engine numbers rather than being decorative.

### `controls/dropdown` `Color=White, Size=Small`
Variant `2199:739` exists; only its node and 96×28 size are recorded. Built as `--gw-color-white`
with a 1px inset `--gw-color-neutral-100` ring, matching the grey variant's construction. Used
for the sort and page-size controls, which sit on `section/table`'s white panel.

### `table-row` `Type=Header` — type, colour, and a sort affordance
The export measures only `Type=Data, State=Default`. Chosen: `--gw-text-body-14-sem` /
`--gw-color-neutral-800`, matching the section title. Sort state is shown with the measured
`ArrowsDownUp` glyph at 12px, `primary-500` when active.

### `table-row` `State=Hover` and `user-card` `State=Hover` — fills
Variants `2192:540` and `2125:198` exist; neither fill is measured. Both borrow `list-item`'s
measured hover `--gw-color-neutral-25` rather than picking a new step.

### Toast copy is written to a 292px column
The toast's 360 width is measured, so it is **not widened to fit copy.** After 16px padding, the
20px icon, the 16px close and 16px of gaps, the message column is exactly **292px** — verified in
the browser. `Export ready — 40 pages, last 28 days` needed ~307px and wrapped to two lines; the
copy was shortened rather than the component stretched. Worth stating in `toast.md`, since the
component gives a fixed width and no guidance on message length.

### `user-card` `State=Clicked` → `dropdown-options` `Style=Icon`
The set documents `State=Clicked` as opening "the Icon dropdown" and `dropdown-options`
`Style=Icon` (`2124:182`) as 140×102, r8, pad 4, gap 4, with three text props and a trailing
action icon — but the menu's own contents are nowhere specified. Built with the three actions a
signed-in user needs: **Account settings · Notifications · Sign out**, each with a trailing
Phosphor glyph.

Two things worth recording:

- **It opens upward.** The card sits at the foot of the rail and `build-rules.md` requires the
  rail to be `overflow: hidden`, so a downward menu is clipped and invisible. Any future
  implementation of this component has the same constraint.
- **It is 112 tall, not the measured 102.** Rows reuse the `.ddopt` treatment (8px padding) so
  every menu in the product matches. Hitting 102 needs a 28.7px row, which needs 6.3px vertical
  padding, and **there is no 6px spacing token** — the scale jumps 4 → 8. Matching sibling menus
  was worth 10px; inventing a spacing value was not.
- **Sign out has no destructive treatment**, because the system defines none — no destructive
  Button style, no red menu row. Left neutral rather than reaching for `red-500`. Flagging it
  rather than inventing it.

### Empty state
`output-targets.md` requires an empty state per Section and records that the library ships none
(`Skeleton` and `Spinner` are named but never drawn). Composed from `section/Container` + tokens,
used for the seven nav destinations this sample does not build.

### Focus ring
**Figma has no focus specification at all** — not on Button, controls, `list-item`, or
`table-row`. A keyboard user currently has nothing. Built as a 2px `--gw-color-primary-alpha-40`
outline at 2px offset — an existing token used as a signal ring, not a fill. **This is a real gap
in the system, not just in this build.**

### Hover states
`controls/tab Show=Hover`, `controls/dropdown`, `Button State=Hover` and `table-row State=Hover`
all exist as Figma variants; **none of their fills is measured in `exports/`.** Each is derived
from the nearest measured neighbour rather than a new value:

| Control | Hover | Why that value |
|---|---|---|
| `controls/tab` | `--gw-color-neutral-alpha-50-white` | moves *toward* the white `Selected` state instead of darkening away from it |
| `controls/dropdown` (Grey) | `--gw-color-neutral-100` | one step up from its `neutral-50` trigger |
| `Button` `Outline` / `Ghost` | `--gw-color-neutral-25` | the measured `list-item` hover |
| `Button` `Primary` | `--gw-color-neutral-900` | the lightest near-black in the ramp |

### Motion
**There are no motion tokens anywhere in the file** (documented gap #10). Every transition here is
therefore a component-level choice, held to a single 120ms ease in one custom property so it can
be swapped for a token the day one exists. `prefers-reduced-motion` disables all of it.

---

## Modified

### `section/card-layout` — the section holds its measured 1084 floor at every width

**Corrected after review.** An earlier pass here stacked the two blocks below 1440 (2 KPIs
full-width above 6 analytics). That was wrong, and worth recording because it is an easy mistake:
it produces a layout matching **none of the three variants** — it reads as a malformed
`KPI cards=3`, which is 3 KPIs above **six-across** analytics, not two above a 3×2 grid.

`KPI cards=2` **is** "2 KPIs left + 6 analytics right". That is the variant's definition, not a
wide-screen arrangement, so it must not be rearranged responsively.

The variant's numbers are mutually dependent and hold only at 1084:

| | |
|---|---|
| split | 580 / 496 |
| 2 KPIs in 580 | (580 − 8) / 2 = **286**, exactly the intrinsic floor |
| 6 analytics in 496, 3 columns | (496 − 16) / 3 = **160**, exactly the intrinsic floor |
| height | 2 analytics rows (2×94 + 8 = 196) ≈ 1 KPI (198) |

Section width = viewport − 16 shell padding − 260 rail − 80 slot padding, so 1084 needs **exactly
1440**.

**Resolution, after two wrong attempts — the 1440 canvas is scaled to fit the window.** Both
earlier answers failed in review and are recorded because the failure modes are instructive:

| Attempt | Why it failed |
|---|---|
| Stack the blocks below 1440 | Produces a layout matching none of the three variants — reads as a malformed `KPI cards=3` |
| Hold 1084 and scroll the slot horizontally | Sections get visibly clipped, and the header toolbar wraps the refresh control onto a second line |

The shell now keeps its **full 1440 layout width at every viewport** and is scaled with
`zoom: min(1, 100vw/1440)`, with width and height divided by the same factor so the scaled box
fills the window exactly. Every measured value survives — verified at 1024, 1230 and 1440 that
the rail is **260**, container **1164**, section **1084**, split **580/496**, kpi-card **286**,
analytics-card **160**, with **nothing clipped** and the toolbar on **one line**. It never scales
above 1, because past 1440 the container is genuinely fluid.

**The trade-off, stated plainly:** below 1440 type paints smaller than the ramp — 14px renders
~12px at a 1230 viewport, ~10px at 1024. That is the price of a fixed-width canvas with no
responsive specification, and it is the only option that deforms nothing. If sub-1440 is a
supported width for real users rather than reviewers, the variants need narrow behaviour drawn.

`preview/_meta_ads_app.css` carries `.cl--side .kpi{min-width:0}`, which is what let the cards
fall under their floor in the first place (**measured 242.9px at 1280**). With the section floor
in place that override no longer bites, but **it should still come out** — it silently defeats the
rule `build-rules.md` states.

### `.kpi` takes a fixed height while the analytics grid sizes to content — the columns drift

Also in `preview/_meta_ads_app.css`. `.kpi{height:var(--v-kpi)}` is a **fixed** clamped height,
while `.cl__agrid` sizes to its content at a flat 196. Below roughly 1250px of viewport height the
two diverge: **measured 189 against 196 at 900 tall**, so the dark cards end 7px above the light
ones — a visible misalignment along the section's whole width. In Figma both are ~196–198 and read
as flush.

```css
.cl--side .kpi{height:auto;min-height:var(--v-kpi)}
```

Stretching the KPI to the row locks the columns together at every height and still honours 198 as
the ceiling — verified flush at 196/196 on a 853-tall viewport and at 198.4/198.4 on a 1300-tall
one.

### `Graph Type=Line` — 2 series → 1
The measured component (`2143:682`) draws two series. The system has no second-series colour and
no categorical chart palette — `sections.md` already records this against `Type=Grouped Bar`.
Rather than invent a hue or eyedrop one, this chart ships a single series in
`--gw-color-primary-500` with the documented area gradient.

### Vertical rhythm — measured maxima not reached at the drawn height
Inherited from the reference CSS, recorded because it surprised me. The clamps
(`--v-hdr: clamp(16px,3.2vh,40px)`, `--v-kpi: clamp(140px,21vh,198px)`) only reach their measured
ceilings above roughly 1250px of viewport height. At the drawn 1440×**888**, header padding
measures 28.6 rather than 40 and kpi-card height 186.5 rather than 198 — about 7% under.
`build-rules.md` says a tall viewport should render the component exactly as drawn; at the height
it *was* drawn, it does not. Left alone rather than diverging from the verified stylesheet.

### Multi-page rail — handlers must rebind per page
`build-rules.md` already establishes that the rail persists while header and slot swap. Worth
adding one line to it: **every control inside the header or the slot has to be bound after each
swap.** Binding once at load leaves dead controls the moment you navigate away and back — it
looks fine and silently does nothing, which is the worst failure shape.

---

## Worth a decision

**0. Blue: data or control state?** Ruled for the calendar (black), but `controls/toggle`
`State=On` is still blue in this build, and the same argument applies to it. One line settles both
and stops the next build re-deciding. See the ruling section above.

**1. Blue is not the only missing signal — there is no focus specification at all.** The hover
gaps are recoverable by analogy (each is one step from a measured neighbour). Focus is not: no
component in the file defines one, so every keyboard user on every Gushwork dashboard currently
gets whatever the browser does. This is an accessibility gap, not a polish item, and it needs a
real decision rather than my `primary-alpha-40` guess.

**2. The dashboard surface has no defined behaviour below 1440, and every guess was wrong.**
This is the single biggest gap found. The split, both card floors and the
two-analytics-rows-equals-one-KPI height relationship are only simultaneously satisfiable at
exactly 1084 / 1440 — there is no slack anywhere in the variant. Two attempts failed in review
before landing on scale-to-fit (see `card-layout` above). Every future Gushwork dashboard hits
this on the first narrow window.

**The ruling needed, one line in `build-rules.md`:** is 1440 the **minimum supported width** for
the dashboard surface?

- **If yes** — scale-to-fit is the right answer and should be written down as the standard
  treatment, so nobody re-derives it.
- **If no** — the three `card-layout` variants need narrow behaviour drawn in Figma, because the
  intuitive guess (stack the blocks) collides with what `KPI cards=3` already means.

Either way, **remove `.cl--side .kpi{min-width:0}`** from the reference stylesheet — it silently
defeats the floor rule `build-rules.md` states.

**3. The missing chart palette, hit for the second time.** `Grouped Bar`'s three untokenised hexes
were already logged. This build hit the same wall on `Type=Line`, whose second series has no
colour at all. Every multi-series chart is blocked on this — worth deciding whether to add a
categorical palette or to spec `Line` as single-series.

---

## Tokens

**No new colour, type, radius, shadow or spacing value was introduced.** Verified in the browser
by reading `getComputedStyle` back against the token values, not by eye:

| Checked | Result |
|---|---|
| shell / container / kpi / analytics / section fills | `neutral-100` · `white` · `neutral-900` · `neutral-25` · `neutral-25` — exact |
| progress fill, chart bars, toggle On | `--gw-color-primary-500` `#0070ff` — exact |
| **icon colours, all 17 containers** | `sec__ico` + `pb__ico` `#0070ff` · kpi badge `#4ade80` (green-300) · kpi header `#bbbec4` (neutral-300) · nav `#262a2e` · toast `#16a34a` — **zero black** |
| nav row type | Inter 500 / 14 / lh 1 = `--gw-text-button-14`; `neutral-900`, icon same colour |
| nav group label | Inter 600 / 10 = `--gw-text-body-10-sem`; `neutral-400` |
| page title | 32 / 600 = `--gw-text-h5` |
| table data cells | `neutral-600` on every column; bottom border `neutral-200` |
| blue button fills | **0** |

Values in use with **no token**, all pre-existing gaps rather than inventions:

- Line-chart area gradient stops `#e4efff` / `#eff6ff` / `#f9fbff` — sampled values documented in
  `sections.md`, used verbatim.
- `analytics-card` value at display Medium 20 and `With Dropdown` cell value at display Medium 18
  — both already flagged tokenless in `section-elements.md`.
- Any chart series colour beyond the first, any focus ring, any motion duration — see above.

### Also verified

- Geometry at 1440: rail **260 at x=8**, container **1164 at x=268** (flush), sections **1084**,
  split **580/496**, kpi-card **286**, analytics-card **160** — every one exact.
- `html, body { overflow: hidden }`; the slot is the only scrolling region; the rail does not
  scroll; all slot children compute `flex: 0 0 auto`. No clipped text or horizontal overflow at
  1280, 1440 or 1920.
- Bar chart label-to-bar drift **0px on all 7 rows**; bar height 10 with radius on the trailing
  end only; every value label inside its track.
- Collapse carets `scaleY(-1)` while expanded, and now **12×12**.
- Both brand faces render, proved by comparing measured text width against a forced fallback, not
  `document.fonts.check()`.
- Toast: width **360** (measured), message column **292**, message height 24 against a 24px
  line-height — **one line, no wrap**. Auto-dismiss measured at 4.4s elapsed: still visible at
  3.5s, gone by 4.4s. Re-firing resets the timer instead of stacking; manual dismiss clears it.
- Nav group label: `cursor: default`, background stays transparent, and the override outranks
  `.li:hover` on both specificity and order.
- User-card menu: **140 wide**, opens upward, and its box sits entirely inside the rail's
  bounds — so the rail's required `overflow: hidden` cannot clip it.
- Every control exercised programmatically **after a navigate-away-and-back round trip**:
  dropdowns open/select/close, tabs switch, `Custom` opens the calendar and cells select, the
  toggle flips and changes the per-engine figures, sections collapse and expand, all four sortable
  columns produce a monotonic rendered column, page size 10/25/50 and pagination move through 40
  rows, Export raises the toast and the toast dismisses.
- Figures reconcile: the 40 table rows sum to 85,386 sessions / 404 leads / 3,338 citations, each
  at or under the site totals of 96,420 / 412 / 3,860, with the remainder in the long tail; the
  per-engine cells sum to exactly 3,860; the chart series sums to exactly 96,420.
