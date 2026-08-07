# Website performance dashboard — new elements and deviations

Built 7 Aug 2026. Files: `/Users/utsavsingh/Gushwork Design/website-performance/{_build.py,index.html}`

A single-page Gushwork site-performance dashboard — `dashboard-build` shell, `section/header`
(sticky), then `section/card-layout` `KPI cards=2` · `section/progress-bar` ·
`section/Container`+`Graph Type=Line` · `section/With Dropdown` · `section/Container`+`Graph
Type=Bar` · `section/table`. All figures are illustrative; the header carries a `Sample data`
Badge.

Styling reuses `preview/_meta_ads_app.css` verbatim rather than rebuilding it. Everything below
is what sits on top of that file.

---

## Created

### `.hdr__top` — title row in `section/header`
`section/header` (`2140:16372`) draws a page title and a toolbar. It has no slot for a Badge,
and the `Sample data` marker has to sit where it cannot be scrolled out of view — a screenshot
of a scrolled-past marker is exactly the failure the marker exists to prevent. A flex row
holding the `h5` title and the Badge, gap `--gw-space-12`. The measured 20px title→toolbar gap
is untouched. **This is the element most likely to recur** — every sample-data dashboard needs it.

### `.dd--w` — `controls/dropdown` `Color=White, Size=Small`
The variant exists (`2199:739`) but `exports/dashboard/controls.md` records only its node and
its 96×28 size, not its fill or border. Used for the sort and page-size controls, which sit on
`section/table`'s white panel rather than the grey canvas. Built as `--gw-color-white` with a
1px inset `--gw-color-neutral-100` ring, matching the grey variant's construction.

### `table-row` `Type=Header` — type and colour
`exports/dashboard/section-elements.md` measures only `Type=Data, State=Default`. The header
variant (`2192:538`) has no recorded appearance. Chosen: `--gw-text-body-14-sem` /
`--gw-color-neutral-800`, matching the section-title treatment so the two read as one level.

### `table-row` `State=Hover` — fill
Variant `2192:540` exists; its fill is not measured. Borrowed `list-item`'s measured hover fill
`--gw-color-neutral-25` rather than picking a new step.

### `.ddbody` / `.sec__body--nb`
`section/With Dropdown` stacks its sub-sections at gap 12, and its data containers are white
with **no** border — unlike `section/Container`'s bordered inner card. The shared `.sec__body`
carries that border, so it is cleared here rather than inherited.

### `Export` button in the table toolbar
`toolbar-right` is drawn empty in `section/section-element/table` (`2205:15807`). Filled with a
dashboard `Button` `Style=Outline, Size=Small`. Using the drawn slot, not a new one.

---

## Modified

### `preview/_meta_ads_app.css` `.sec__caret` — 12px → rendered 300×150. **This is a defect, not a deviation.**
`.sec__caret` sizes the *span* to 12×12 but nothing sizes the `<svg>` inside it, so the section
collapse caret rendered at the SVG default **300×150 — 25× the measured 12px**. It pushed
`.sec__hd` to a scrollWidth of 1184 against a 900 client box. `.sec{overflow:hidden}` clipped
the overflow, which is why it never looked obviously broken and survived the reference build.
Every other icon holder in that file sizes its own `svg`; this one was missed. Fixed here with
`.sec__caret svg{width:12px;height:12px;display:block}`. **The same one-line fix should land in
`preview/_meta_ads_app.css`.**

### `section/card-layout` `KPI cards=2` — side-by-side split now stacks below 1440
`preview/_meta_ads_app.css` carries `.cl--side .kpi{min-width:0}`, which lets kpi-cards fall
under their measured 286 floor when the shell narrows. **Measured 242.9px at a 1280 viewport.**
`build-rules.md` is explicit that 286 and 160 are floors and that horizontal measured values are
never clamped.

The arithmetic: the 580/496 split seats 2 KPIs at 286 and 6 analytics cards at 160 only when the
section is the full measured 1084 — and section width = viewport − 16 shell padding − 260 rail −
80 slot padding, so 1084 requires **exactly 1440**. Added `@media (max-width:1439px)` to stack
the two blocks; each then gets the whole section and both floors hold (verified: 458 and 302.7 at
1280).

### `Graph Type=Line` — 2 series → 1
The measured component (`2143:682`) draws two series. The system has no second-series colour and
no categorical chart palette — `sections.md` already records this against `Type=Grouped Bar`.
Rather than invent a hue or eyedrop one, this chart ships a single series in
`--gw-color-primary-500` with the documented area gradient. See "Worth a decision".

### Vertical rhythm — measured maxima not reached at the drawn height
Inherited from the reference CSS, recorded because it surprised me. The clamps
(`--v-hdr: clamp(16px,3.2vh,40px)`, `--v-kpi: clamp(140px,21vh,198px)`) only reach their measured
ceilings above roughly 1250px of viewport height. At the drawn 1440×**888**, header padding
measures 28.6 rather than 40 and kpi-card height 186.5 rather than 198 — about 7% under.
`build-rules.md` says a tall viewport should render the component exactly as drawn; at the height
it *was* drawn, it does not. Left alone rather than diverging from the verified stylesheet.

---

## Worth a decision

**1. The 1440 floor on `card-layout` `KPI cards=2`.** The measured split and the measured card
floors are only simultaneously satisfiable at exactly 1440. Below it, something must give — and
the reference CSS currently gives up the floor silently. This is a **Promote** candidate: either
the component gets a documented stacking behaviour below 1440, or `.cl--side .kpi{min-width:0}`
comes out of the reference stylesheet. Right now two files disagree about which rule wins, and a
future build will resolve it the other way.

**2. The missing chart palette, hit for the second time.** `Grouped Bar`'s three untokenised
hexes were already logged. This build hit the same wall on `Type=Line`, whose second series has
no colour at all. Every multi-series chart in the system is currently blocked on this. A
categorical palette is a small addition and it keeps coming up — worth deciding whether to add
one or to spec `Line` as single-series.

---

## Tokens

**No new colour, type, radius, shadow or spacing value was introduced.** Every rule added here
resolves to a `foundation/tokens.css` custom property. Verified in the browser by reading
`getComputedStyle` back against the token values, not by eye:

| Checked | Result |
|---|---|
| shell / container / kpi / analytics / section fills | `neutral-100` · `white` · `neutral-900` · `neutral-25` · `neutral-25` — all exact |
| progress fill, chart bars | `--gw-color-primary-500` `#0070ff` — exact |
| nav row type | Inter 500 / 14 / lh 1 = `--gw-text-button-14`; colour `neutral-900`, icon same |
| nav group label | Inter 600 / 10 = `--gw-text-body-10-sem`; `neutral-400` |
| page title | 32 / 600 = `--gw-text-h5` |
| table data cells | `neutral-600` on every column; bottom border `neutral-200` |
| section icon tiles | `--gw-color-primary-alpha-10` |
| blue button fills | **0** |

Values in use with **no token**, all pre-existing gaps rather than inventions:

- Line-chart area gradient stops `#e4efff` / `#eff6ff` / `#f9fbff` — sampled values documented in
  `sections.md`, used verbatim.
- `analytics-card` value at display Medium 20 and `With Dropdown` cell value at display Medium 18
  — both already flagged tokenless in `section-elements.md`.
- Any chart series colour beyond the first — see "Worth a decision".

### Also verified

- Shell geometry at 1440×888: rail **260×880 at x=8**, container **1164 at x=268** (flush, no
  gap), every section **1084**, KPI split **580/496**, kpi-card **286**, analytics-card **160**.
- `html, body { overflow: hidden }`; the slot is the only scrolling region; the rail does not
  scroll; all six slot children compute `flex: 0 0 auto`.
- Bar chart label-to-bar drift: **0px on all 7 rows** (the export warns of ~2px per row
  accumulating to 14px when the two columns are independent).
- Bar height 10 with radius on the trailing end only; every value label inside its track.
- Collapse carets all `scaleY(-1)` — pointing up while expanded.
- Both brand faces render, proved by comparing measured text width against a forced fallback,
  not `document.fonts.check()`.
- No clipped text and no horizontal overflow at 1280, 1440 or 1920.
