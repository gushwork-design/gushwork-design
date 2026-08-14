# Sections — the section-level building blocks

> ## ⚠ PARTLY SUPERSEDED — 13 Aug 2026
>
> | Section | Status |
> |---|---|
> | `section/header` | **Superseded** by `page-header` + `section-header` — [`v2/cards-and-chrome.md`](v2/cards-and-chrome.md). One 1164×146 header becomes two: a 1120×113 page header (44px title) and a 1120×24 section header (`body-16-sem` + qualifier) |
> | `section/Container` | **Superseded** as a shell by `card-shell` (`lg`/`md`/`sm` radius tiers). Still current as a **composition slot** for custom content |
> | `section/card-layout` | **Current.** The `KPI cards` = 1/2/3 decision is unchanged — but the cards inside it are now `stat-card` / `metric-card` |
> | `section/table` | **Current** as a Section. Its rows are now `v2/data-table.md` |
> | `section/progress-bar` | **Current.** A 1084×116 card with a 32px labelled blue bar — a genuinely different component from the v2 hairline bar. Both exist |
> | `section/With Dropdown` | **Current — unchanged** |
>
> **The composition ladder is unchanged and still binding:**
> `section-elements → Sections → Dashboard Build`. v2 supplies parts, not a new ladder. Never put
> a v2 component loose in the Dashboard Build slot.

Figma: group `sections` (`2146:17154`).

Self-contained rows and panels that stack inside the Dashboard Build slot to compose a
product page. The dashboard-side analog of Folds: where Folds build the marketing
website, Sections build the app. Each composes dashboard atoms into a reusable, often
collapsible block.

**Scope: dashboard / product only.**

## Pick the Section by what it holds

| Section | Use when | Node |
|---|---|---|
| `section/Container` | A generic collapsible section with a slot for arbitrary content. **Use when nothing more specific fits.** | `2134:14477` |
| `section/card-layout` | A KPI + analytics row. | `2136:491` |
| `section/progress-bar` | A single goal/progress readout — label + count + filled track. | `2140:16056` |
| `section/With Dropdown` | A section with a dropdown filter in its header over tabular metric data. Use when the data needs filtering in place. | `2140:16131` |
| `section/table` | A sortable, paginated data table. Use for browsable product data — leads, campaigns, entries. | `2209:17021` |
| `section/header` | The page-level header. **One per page, at the top.** | `2140:16372` |
| `section/section-element/Graph` | A chart. | `2143:684` |

`section/table` is **distinct from the website's `fold/Comparison Table`** — that is a
fixed marketing feature-comparison; this is a live data grid.

---

## `section/Container`

Component set `2134:14477` · **2 variants** · slot property `Slot` (accepts any content).

| Property | Values |
|---|---|
| `State` | `Default`, `Collapsed` |

```
State=Default
COMPONENT (1084×300, r:12, VERTICAL, gap:16, pad:12)
├── FRAME "header" (HORIZONTAL, gap:8, pad:4)
│   ├── FRAME "title-container" (HORIZONTAL, gap:8)
│   │   ├── FRAME "icon-container" (20×20, r:4, pad:4)
│   │   │   └── INSTANCE "ChartLine" (Weight=Bold)
│   │   └── TEXT title (14px)
│   └── INSTANCE "CaretDown" (collapse toggle)
└── FRAME "container" (r:8, VERTICAL, gap:10, pad:16)
    └── SLOT "Slot" (r:8, VERTICAL, gap:40, pad:10)

State=Collapsed
COMPONENT (1084×52, r:12, VERTICAL, gap:16, pad:12)
├── FRAME "header" (same as Default)
└── FRAME "container" [HIDDEN]
```

**The rules call this `section/Other`. The component on canvas is named
`section/Container`.** Use `section/Container`.

---

## `section/card-layout`

Component set `2136:491` · **3 variants**.

| Property | Values |
|---|---|
| `KPI cards` | `1`, `2`, `3` |

Choose by how many headline metrics lead the row. **Always paired with 6 analytics
cards.**

| Variant | Layout | Size |
|---|---|---|
| `KPI cards=1` | 1 large KPI left (400×198) + 6 analytics right (676×196 grid) | 1084×198 |
| `KPI cards=2` | 2 KPIs left (580×198) + 6 analytics right (496×196 grid) | 1084×198 |
| `KPI cards=3` | 3 KPIs stacked on top + 6 analytics below | 1084×300 |

Gap 8 throughout. The reference variants use kpi-card modes `Mode4/Positive`,
`Mode6/Neutral`, `light/Negative` — match the Mode to the surrounding section, and pick
`Type` by the metric's direction.

---

## `section/progress-bar`

Component `2140:16056` · **no variants**.

```
COMPONENT (1084×116, r:16, VERTICAL, gap:16, pad:20)
├── FRAME "header" (HORIZONTAL, gap:8, pad:4)
│   ├── FRAME "label" (HORIZONTAL, gap:8)
│   │   ├── FRAME "icon" (20×20, r:4, pad:4) → INSTANCE "Target" (Weight=Bold)
│   │   └── TEXT label (14px)
│   └── TEXT count (14px)
└── FRAME "track" (1044×32, r:8)
    └── FRAME "fill" (r:8) → TEXT percentage (14px)
```

Placeholder count text reads `"97/ 120 calls"` — a stray space after the slash. Write
`97/120 calls`.

### Appearance — from design context (`2140:16056`), not the annotation

The structure blob documents geometry only. Every value below is the component's real
bound value. **This is the one Section whose fill is brand blue.**

| Part | Value |
|---|---|
| container | `--gw-color-neutral-25` · `--gw-radius-16` · padding `--gw-space-20` · gap `--gw-space-16` · w 1084 |
| `header` | padding `--gw-space-4` · `justify-content: space-between` · full width · gap `--gw-space-8` |
| `icon` tile | `--gw-color-primary-alpha-10` · `--gw-radius-4` · padding `--gw-space-4` |
| Target glyph | **12px**, not 20 — the 20px tile is 12px glyph + 4px padding |
| label | `--gw-text-body-14-sem` · `--gw-color-neutral-800` · tracking `-0.2px` |
| count | `--gw-text-body-14-med` · `--gw-color-neutral-500` · tracking `-0.2px` |
| `track` | `--gw-color-neutral-100` · h 32 · `--gw-radius-8` · full width |
| `fill` | `--gw-color-primary-500` · h 32 · `--gw-radius-8` |
| percentage | `--gw-text-body-14-med` · `--gw-color-white`, inset from the fill's leading edge |

Icon: `Target` — Figma node `112:13686`, committed at `assets/icons/target.svg`.

**The label is `neutral-800` semibold, not black**, and the icon tile is the 10%-alpha blue,
not `primary-50`. Both are easy to get wrong by eye.

**This is not a blue button fill and does not violate the no-blue-fill rule** — that ban
covers button fills only. Blue stays valid as a data and signal colour, which is what this
track is.

---

## `section/With Dropdown`

Component `2140:16131` · **no variants**.

```
COMPONENT (1084×296, r:12, VERTICAL, gap:16, pad:12)
├── FRAME "header" (HORIZONTAL, gap:8, pad:4)
│   ├── INSTANCE "section/section-element/dropdown" (State=Closed)
│   └── INSTANCE "CaretDown" (section collapse toggle)
└── FRAME "body" (VERTICAL, gap:12)
    ├── FRAME "sub-section 1" → "data container" (r:8, pad:16)
    │   └── FRAME "data row" (HORIZONTAL, gap:8)
    │       ├── 6× FRAME "data cell" (100×50, VERTICAL, gap:4, pad:4/8)
    │       │   ├── TEXT label (10px, uppercase)
    │       │   └── TEXT value (20px)
    │       ├── LINE separators between cells
    │       └── 2× FRAME "data cell" (100×42, compact)
    └── FRAME "sub-section 2" (VERTICAL, gap:8)
        ├── FRAME "sub-section header" (HORIZONTAL, pad:4)
        │   ├── TEXT sub-section title (10px, uppercase)
        │   └── FRAME badge [HIDDEN]
        └── FRAME "data container" (same structure, 9 cells)
```

The sub-section title placeholder reads `"SUB-SECtion title"` — broken casing in the
source. Write proper text.

### Appearance — MEASURED 8 Aug 2026, and the tree above is wrong in four places

Read off `2140:16131`. The shell matches `section/Container` exactly — `--gw-color-neutral-25`,
`p-12`, `--gw-radius-12`, `gap-16`, `overflow: clip`, 1084 wide. Below that it diverges:

| | Transcribed above | **Measured** |
|---|---|---|
| Metric value | `20px` | **Vert Grotesk Display Medium 18**/1.2 on `--gw-color-neutral-900` |
| First card | `6× cell` + `2× compact` | **10 cells**, all the same |
| Second card | `9 cells` | **6 cells** |
| Data card border | not stated | **none** — see below |

| Part | Measured |
|---|---|
| Data card | `--gw-color-neutral-white` · `p-16` · `--gw-radius-8` · **no border** · `overflow: clip` |
| Metric cell | `px-8 py-4` · `gap-4` · **`min-width: 100`** |
| Metric label | Inter Medium **10**, line-height **1.6**, **UPPERCASE**, `--gw-color-neutral-600` |
| Metric value | **Vert Grotesk Display Medium 18**/1.2, `--gw-color-neutral-900` |
| Separator | a 1px vertical rule between every pair of cells, `self-stretch` |
| Sub-section title | Inter Medium 10/1.6 UPPERCASE on **`--gw-color-neutral-500`**, `p-4` |

**The data card has no border, and `section/Container`'s inner card does** (1px
`--gw-color-neutral-50`). Two sections that look like siblings are built differently. Don't copy
one's card into the other.

**Three text tiers, all 10px uppercase, separated only by colour**: metric label `neutral/600`,
sub-section title `neutral/500`. Getting these the same way round matters more than it looks —
the quieter colour is the *heading*, which is backwards from every other hierarchy in the system.

**✗ The data row overflows its card.** The row is drawn **1036 wide** inside a card whose content
box is 1028 (`1084 − 12·2 shell − 16·2 card`). `overflow: clip` hides the last 8px. Build the row
`width: 100%` and let the cells flex; do not reproduce 1036.

### The header dropdown is its own component

`section/section-element/dropdown` `2142:583` · **466 wide** · 2 variants — **not**
`controls/dropdown`.

| Part | Measured |
|---|---|
| Trigger | `--gw-color-neutral-white` · `p-8` · `--gw-radius-8` · `min-w-140` · `justify-between` |
| Label | **Inter Semi Bold 14**, `--gw-color-neutral-800`, tracking `-0.2px`, line-height 1 |
| Badge 1 | `--gw-color-neutral-100` · `px-8 py-4` · `--gw-radius-4` · `--gw-text-body-12-med` on `--gw-color-neutral-600` |
| Badge 2 | **`--gw-color-green-alpha-10`** · same geometry · text **`--gw-color-green-500`** |
| Caret | `CaretDown` 12px |

**It carries two badges, and the second is a status.** "Active" in green is part of the drawn
component, not example content — this dropdown names a *thing with a state*, e.g. a campaign.
These are hand-built badge frames, **not** instances of the `badge` set in
`foundation/shared-components.md`, so they inherit nothing from it.

---

## `section/table`

Component `2209:17021` · **no variants**.

```
COMPONENT (1084×674, r:12, VERTICAL, gap:16, pad:12)
├── FRAME "header" (HORIZONTAL, gap:8, pad:4)
│   ├── FRAME "title-container" → icon tile (20×20, r:4) + TEXT title (14px)
│   └── INSTANCE "CaretDown" (collapse toggle)
└── FRAME "container" (r:12)
    └── INSTANCE "section/section-element/table"
        ├── FRAME "table-toolbar" (HORIZONTAL, pad:16/24)
        │   └── TEXT "Sort by" + controls/dropdown (Small) + INSTANCE "ArrowsDownUp" (Bold)
        ├── FRAME "table-body"
        │   ├── INSTANCE "table-row" (Type=Header, State=Default)
        │   └── 10× INSTANCE "table-row" (Type=Data, State=Default)
        └── FRAME "table-footer" (HORIZONTAL, pad:16/24)
            ├── TEXT "Showing per page" + controls/dropdown (Small)
            └── pagination: Button (Ghost, Icon Only) + page numbers + "..." + Button
```

6 columns, 10 data rows, per-row `DotsThree` overflow menu, pagination footer with
page-size control.

### Geometry — MEASURED 8 Aug 2026

Read off `2209:17021`. **1084 × 674**, and it tiles exactly:
`12 + 28 + 16 + 606 + 12 = 674`. ✓

| Part | Position | Size |
|---|---|---|
| `header` | 12, 12 | **1060 × 28** |
| `title-container` | 4, 4 *(within header)* | 145 × 20 |
| `icon-container` | 0, 0 | **20 × 20** — `p-4` around a 12px `ChartLine` |
| `title` | **28**, 3 | 117 × 14 — so `gap-8` after the 20px tile |
| `CaretDown` | 1044, **20** | 12 × 12 |
| `container` | 12, **56** | **1060 × 606** |

The container holds one instance — `section/section-element/table` at the full 1060 × 606. The
section is a shell; **all the table's own structure belongs to that element**, not here.

**✗ The collapse caret is not vertically centred.** The title block spans y 4–24 (centre **14**);
the caret spans y 20–32 (centre **26**). They are **12px apart**, and the caret's bottom edge
overflows the 28-tall header by 4. `section/Container` centres the two correctly, so this is
`section/table` alone.

**Build it centred.** Two sections whose headers are meant to read identically should not differ
by 12px, and nothing about the table makes its caret a special case. Report the drift.

---

## `section/header`

Component `2140:16372` · **no variants** · one per page.

```
COMPONENT (1164×146, VERTICAL, gap:20, pad:40/40/20/40)
├── TEXT page title (32px)
└── FRAME "toolbar" (HORIZONTAL)
    ├── FRAME "controls" (HORIZONTAL, gap:12)
    │   ├── INSTANCE "controls/tab" (Size=Medium, Show=Selected) → 5 tabs
    │   └── 3× FRAME "dropdown" (r:8, HORIZONTAL, gap:8, pad:8) → label (12px) + CaretDown
    └── FRAME "refresh" (HORIZONTAL, gap:8)
        ├── TEXT "Updated 4s ago" (10px)
        └── FRAME "refresh button" (28×28, r:8) → INSTANCE "ArrowClockwise"
```

The structure annotation states `1164×164`; the actual symbol is **1164×146**. Use 146.

---

## `section/section-element/Graph`

Component set `2143:684` · **3 variants**.

| Property | Values |
|---|---|
| `Type` | `Bar`, `Line`, `Grouped Bar` |

**Pick by data shape:**

| Data | Type |
|---|---|
| Comparison across items | `Bar` — horizontal bars |
| Change over time | `Line` — time-series with tooltip |
| Several measures per item | `Grouped Bar` |

All three share one pattern: `y-axis labels │ chart area with grid lines + data │ x-axis`.

| Variant | Size | y-axis | Chart area |
|---|---|---|---|
| `Bar` | 1060×280 | 182×280, 7 labels, gap 20 | 866×280, grid gap 60 |
| `Line` | 1028×400 | 6 labels, gap 56 | 999×400, **1 series + gradient fill** + tooltip |
| `Grouped Bar` | 1108×456 | 182×456, 7 labels | 914×456, 7 bar groups × 3 bars |

**The three sizes are not interchangeable** — 280, 400 and 456 tall. A slot sized for `Bar` will
not hold `Grouped Bar`. Pick the chart before you size the section.

## Graph appearance — MEASURED 8 Aug 2026

Read off `2143:681`, `2143:682` and `2143:683`, plus the four SVG assets `Line` renders its data
as.

### Shared across all three

| Part | Measured |
|---|---|
| Canvas | `--gw-color-neutral-white`, `overflow: clip` |
| Grid lines | **6**, horizontal, `--gw-color-neutral-100` `#e7e8e9`, 1px solid, in a `py-16` band |
| Axis labels | Inter Medium **12**, line-height 1, tracking `-0.2px`, `--gw-color-neutral-600` |
| x-axis | `justify-between`, each tick **32 wide** (36 on `Line`) |

The chart area is authored **rotated −90°** inside a `containerType: size` wrapper, so every bar
is drawn horizontal and turned. That is a Figma drawing technique, not a spec — build it however
your chart library wants.

### `Bar` — single series

Bars are **`--gw-color-primary-500`**, **10 tall**, radius **2 on the right corners only**
(`rounded-br-2 rounded-tr-2`). Value labels sit just past the bar end, Inter Medium **10**.

**✗ The value labels disagree with each other.** The first is `--gw-color-neutral-black`; the
other two are `--gw-color-neutral-900`. Same role, two colours. Build **`neutral/900`** — it is
the majority, and it is closest to `Grouped Bar`, which uses `neutral/800` throughout and never
black. Report the drift.

### `Line` — one series, not two

**The data is four SVG assets, not styled elements**, which is why an earlier pass recorded "2
series" and "the second series has no colour". There is no second series:

| Asset | Measured |
|---|---|
| The line | `stroke: #0070FF` = `--gw-color-primary-500`, **`stroke-width: 2`** |
| The area beneath it | a vertical linear gradient, `#0070FF` **30% → 0%** |
| Grid lines | `stroke: #E7E8E9` = `--gw-color-neutral-100` |
| Crosshair | `#0070FF`, **`stroke-dasharray: 2 2`** |

So `Line` is **single-series by design** and needs no categorical palette. Only `Grouped Bar`
does.

#### The tooltip — a component nothing else documents

`Line` carries a hover tooltip that appears in no other export:

| Part | Measured |
|---|---|
| Surface | `--gw-color-neutral-25` · **0.5px `--gw-color-neutral-100`** · `--gw-radius-4` · `p-8` · `gap-8` · **`--gw-shadow-s2`** |
| Header | 12px `Clock` + `gap-2` + `--gw-text-body-10-med` on `--gw-color-neutral-500` |
| Headline | `--gw-text-body-10-med` on `--gw-color-neutral-900`, with an 8px flipped `CaretDown` pushed right |
| Breakdown | **0.7px dashed left border `--gw-color-neutral-500`**, `pl-8 py-4`; rows of **8px** Inter Medium, `gap-12` across, `gap-4` down |
| Breakdown row | label `--gw-color-neutral-600` · value `--gw-color-neutral-700` |

Figma's Tailwind output reports the shadow as `drop-shadow(0 2px 2px …)` while the style
annotation names `Shadows/S2` — *offset (0,2), radius 4*. **The annotation is the token.** Same
flattening as the login button's S3.

**0.7px and 0.5px are sub-pixel** — build 1px per `DECISIONS.md` → **R5**, and report them.

### `Grouped Bar` — three series, none of them a token

7 category groups × 3 bars, **`gap-px` between bars within a group**. Bars are 10 tall with the
same right-only radius 2. Value labels are Inter Medium 10 on `--gw-color-neutral-800` —
consistent here, unlike `Bar`.

| Series | Measured | Nearest token | Δ |
|---|---|---|---|
| 1 | `#a1cdfe` | `--gw-color-primary-200` `#99c6ff` | ~11/765 — imperceptible |
| 2 | `#9784ff` | **none — the system has no purple ramp** | — |
| 3 | `#fed14a` | `--gw-color-yellow-200` `#fcd34d` | ~4/765 — imperceptible |

**Two of the three are almost certainly meant to be those tokens and are simply unbound.** The
third has nowhere to go. `DECISIONS.md` → **R11**.

The left label column is `pb-40` with `gap-32` and 32-tall labels. **✗ One category label is
`--gw-color-neutral-black` where the other six are `--gw-color-neutral-600`** — the same
one-off-in-a-set drift as `Bar`'s value labels. Build all seven `neutral/600`.

---

## Collapse behaviour

`section/Container`, `section/With Dropdown`, and `section/table` are collapsible.

**Default to expanded.** The caret collapses to header-only. Use collapse to let users
manage a dense dashboard — **not to hide primary content by default.**

## Composition — reuse, don't rebuild

Sections compose section-elements, and each inherits its own rules. Don't restyle them
inside a Section.

| Section | Instances |
|---|---|
| `section/card-layout` | `kpi-card` + `analytics-card` |
| `section/table` | the `table` element (which instances `table-row`), `controls/dropdown`, `Button` (Ghost / Icon Only for pagination) |
| `section/With Dropdown` | `section/section-element/dropdown` |
| `section/header` | `controls/tab` |

`kpi-card` and the section dropdown use **Badge** — colour signals per
`foundation/shared-components.md`. Pagination and sort buttons follow the dashboard
button rule (black / outline / ghost, never blue).


## `section/Container` — appearance from the set (`2134:14477`)

| Node | Variant |
|---|---|
| `2134:14476` | `State=Default` |
| `2134:14475` | `State=Collapsed` |

| Part | Value |
|---|---|
| shell | **1084 wide** · `--gw-radius-12` · padding `--gw-space-12` · gap `--gw-space-16` · fill **`--gw-color-neutral-25`** |
| header | padding `--gw-space-4` · space-between · full width |
| icon tile | `--gw-color-primary-alpha-10` · `--gw-radius-4` · padding `--gw-space-4` · `ChartLine` at **12px** |
| title | **Inter Semi Bold 14**, `--gw-color-neutral-800`, tracking `-0.2px`, line-height 1 |
| caret | `CaretDown` at **12px** |
| body (Default only) | **`--gw-color-white`** · **1px border `--gw-color-neutral-50`** · `--gw-radius-8` · padding `--gw-space-16` |
| Slot | `--gw-radius-8` · padding 10 · gap `--gw-space-40` |

**The caret flips, it does not rotate 180°.** `State=Default` renders `CaretDown` with a
vertical flip (`scaleY(-1)`) so it points **up**; `State=Collapsed` renders it unflipped,
pointing down. Drawing both pointing down — as an earlier pass did — inverts the affordance.

**The inner container is a white card with a `neutral-50` hairline**, sitting on the
`neutral-25` shell. Two greys, one inside the other.

The title's line-height is 1, so `--gw-text-body-14-sem` (which is 14/21) is close but not
exact. Use the token and accept the 21px leading, or set `line-height: 1` explicitly and say
you did.

## `section/section-element/Graph` — `Type=Bar` measured (`2143:681`)

| Part | Value |
|---|---|
| frame | **1060 × 280** · fill `--gw-color-white` · `overflow: hidden` |
| y-axis labels | Inter Medium 12 · `--gw-color-neutral-600` · tracking `-0.2px` · gap `--gw-space-20` |
| chart area | gap `--gw-space-16` · 6 horizontal grid lines · padding-block 16 |
| bar | **height 10** · fill `--gw-color-primary-500` · **radius 2 on the trailing end only** |
| bar value | Inter Medium 10 · `--gw-color-black` or `neutral-900` · sits just past the bar's end |
| x-axis | Inter Medium 12 · `--gw-color-neutral-600` · space-between · each label 32 wide |

Bars are brand blue — a data fill, not a button fill, so the no-blue rule does not apply.

### `Type=Line` — `2143:682` · 1028 × 400

| Part | Value |
|---|---|
| stroke | `--gw-color-primary-500`, ~2px |
| area under the line | a **vertical gradient**, sampled `#e4efff` at the line → `#eff6ff` mid → `#f9fbff` at the baseline |
| y-axis | `1.0 · 0.8 · 0.6 · 0.4 · 0.2 · 0` |
| x-axis | hourly — `12 AM` … `7 AM` |
| grid | vertical rules, `--gw-color-white` on the plot |
| tooltip | white card + shadow, a dashed vertical leader down to the point |

The tooltip carries a clock glyph, a headline (`7 leads at $63 each`) and a breakdown list
of campaign rows. **It is the only charted component with a hover affordance drawn in.**

### `Type=Grouped Bar` — `2143:683` · 1108 × 456

Seven groups of three bars, each bar labelled with its percentage. x-axis `0%` … `50%`.

**The three-series palette is not in the token system.** Sampled from the render:

| Series | Value | Nearest token | Match? |
|---|---|---|---|
| 1 | `#fed14a` | `--gw-color-yellow-200` `#fcd34d` | no |
| 2 | **`#9784ff`** | — | **no purple exists in the system** |
| 3 | `#a1cdfe` | `--gw-color-primary-200` `#99c6ff` | no |

`get_variable_defs` on the node returns **only neutrals** — `Neutral/600`, `black`, `200`,
`100`, `800`, `white`. The three series colours are **raw hex painted on the bars**, bound
to nothing.

This is a real gap, not a transcription slip:

- There is **no categorical chart palette** in the variable collections. Any second chart
  built in this system has nothing to reach for.
- The purple `#9784ff` appears nowhere else. The file's only other purple is
  `_Helper/Purple` `#8427DE`, which is explicitly marked internal-use and must never render.
- Two of the three are *near* an existing token but not equal to it, which suggests they
  were eyedropped rather than chosen.

**Do not invent a palette to fill this.** If a chart needs more than one series, report the
gap. If you must ship the Grouped Bar as drawn, use the three hexes above verbatim and say
they are untokenised.

One y-axis label renders bold (`FLI Retargeting Core Sched`) while the other six are
`--gw-color-neutral-600` regular. Nothing distinguishes that row — it looks like a stray
override.

## `section/With Dropdown` — appearance from the component (`2140:16131`)

| Part | Value |
|---|---|
| shell | **1084 wide** · `--gw-radius-12` · pad `--gw-space-12` · gap `--gw-space-16` · fill `--gw-color-neutral-25` |
| header | pad `--gw-space-4` · space-between · holds the section dropdown + a collapse caret |
| collapse caret | `CaretDown` **12px, flipped `scaleY(-1)`** — points up when expanded |
| body | gap `--gw-space-12` |
| data container | **`--gw-color-white`** · `--gw-radius-8` · pad 16 · inner row 1036 wide, gap `--gw-space-8` |
| data cell | min-width 100 · pad `4px 8px` · gap `--gw-space-4` |
| cell label | Inter Medium 10, uppercase, line-height 1.6 · `--gw-color-neutral-600` |
| cell value | **Vert Grotesk Display Medium 18**, line-height 1.2 · `--gw-color-neutral-900` |
| separators | 1px vertical rules **between** cells, full cell height |
| sub-section title | Inter Medium 10, uppercase, lh 1.6 · `--gw-color-neutral-500` · pad `--gw-space-4` |

### The section dropdown inside the header (`2142:583`)

466 wide. Trigger is `--gw-color-white`, `--gw-radius-8`, pad `--gw-space-8`, min-width 140,
space-between, with `CaretDown` at 12px.

| Part | Value |
|---|---|
| option label | **Inter Semi Bold 14** · `--gw-color-neutral-800` · tracking `-0.2px` |
| neutral badge | `--gw-color-neutral-100` fill · `--gw-color-neutral-600` text · `--gw-radius-4` · pad `4px 8px` |
| status badge | `--gw-color-green-alpha-10` fill · **`--gw-color-green-500`** text |

**The dropdown carries two badges inline in its trigger** — a neutral one for the option's
own label and a green status one. The green badge here uses `green-500` text, where
`kpi-card`'s inline badge uses `green-300`. Three different green-badge treatments now exist
across the system: this one, kpi-card's, and the standalone Badge's `green-100`/`green-500`.

**Cell values are the display face at Medium 18** — a fourth display size in use (18, 20, 32
and the rail's 18), none of which has a token. The heading ramp starts at 22.

---

## `section/header` — `2140:16372`, measured 7 Aug 2026

Single component, no variants. **1164 × 146** — the rules text says 164; the component is 146.

| Part | Measured |
|---|---|
| Shell | white · **1px `--gw-color-neutral-50` bottom border** · `pt-40 pb-20 px-40` · `gap-20` |
| Title | Vert Grotesk **Semibold 32**/1.2 on **`--gw-color-neutral-900`** — not `neutral-black` |
| Row | `justify-content: space-between`, full width |
| Left | `gap-12` — one `controls/tab` (`Size=Small`) then **three** `controls/dropdown` at `Size=Small, Color=Grey`, 120 wide each |
| Right | `gap-4` — "Updated 4s ago" in **Inter Medium 10** on `--gw-color-neutral-700`, then a **28 × 28** refresh button: **2px `--gw-color-neutral-100`** border, `--gw-radius-8`, 16px `ArrowClockwise` |

The header is the only place a **2px-bordered 28px icon button** appears — it is an `Outline`
button at a size the `Button` set does not offer.
