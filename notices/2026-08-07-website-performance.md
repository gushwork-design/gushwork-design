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
Selected cells use `--gw-color-primary-500`. Previously `Custom` was inert.

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

### `table-row` `State=Hover` — fill
Variant `2192:540` exists; its fill is not measured. Borrowed `list-item`'s measured hover
`--gw-color-neutral-25` rather than picking a new step.

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

### `section/card-layout` `KPI cards=2` — side-by-side split now stacks below 1440
`preview/_meta_ads_app.css` carries `.cl--side .kpi{min-width:0}`, which lets kpi-cards fall under
their measured 286 floor when the shell narrows. **Measured 242.9px at a 1280 viewport.**
`build-rules.md` is explicit that 286 and 160 are floors and that horizontal measured values are
never clamped.

The arithmetic: the 580/496 split seats 2 KPIs at 286 and 6 analytics cards at 160 only when the
section is the full measured 1084 — and section width = viewport − 16 shell padding − 260 rail −
80 slot padding, so 1084 requires **exactly 1440**. Added `@media (max-width:1439px)` to stack the
two blocks; each then gets the whole section and both floors hold (verified: 458 and 302.7 at
1280).

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

**1. Blue is not the only missing signal — there is no focus specification at all.** The hover
gaps are recoverable by analogy (each is one step from a measured neighbour). Focus is not: no
component in the file defines one, so every keyboard user on every Gushwork dashboard currently
gets whatever the browser does. This is an accessibility gap, not a polish item, and it needs a
real decision rather than my `primary-alpha-40` guess.

**2. The 1440 floor on `card-layout` `KPI cards=2`.** The measured split and the measured card
floors are only simultaneously satisfiable at exactly 1440. Below it something must give, and the
reference CSS currently gives up the floor silently. A **Promote** candidate: either the component
gets a documented stacking behaviour below 1440, or `.cl--side .kpi{min-width:0}` comes out of the
reference stylesheet. Two files currently disagree about which rule wins.

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
- Every control exercised programmatically **after a navigate-away-and-back round trip**:
  dropdowns open/select/close, tabs switch, `Custom` opens the calendar and cells select, the
  toggle flips and changes the per-engine figures, sections collapse and expand, all four sortable
  columns produce a monotonic rendered column, page size 10/25/50 and pagination move through 40
  rows, Export raises the toast and the toast dismisses.
- Figures reconcile: the 40 table rows sum to 85,386 sessions / 404 leads / 3,338 citations, each
  at or under the site totals of 96,420 / 412 / 3,860, with the remainder in the long tail; the
  per-engine cells sum to exactly 3,860; the chart series sums to exactly 96,420.
