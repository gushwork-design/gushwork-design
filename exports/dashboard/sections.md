# Sections — the section-level building blocks

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

### Colour — the structure blob doesn't state it; verified from the render

The annotation documents geometry only, so these were read off the component render
(`2140:16056`) rather than inferred. **This is the one Section whose fill is brand blue.**

| Part | Value |
|---|---|
| `fill` | `--gw-color-primary-500` — the brand blue |
| `track` (unfilled remainder) | `--gw-color-neutral-100` |
| percentage text, inside the fill | `--gw-color-white`, right-aligned at the fill's leading edge |
| `icon` tile | light blue tile, `--gw-color-primary-50`, with the Target glyph in `--gw-color-primary-500` |

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
| `Line` | 1028×400 | 6 labels, gap 56 | 999×400, 2 series + tooltip |
| `Grouped Bar` | 1108×456 | 182×456, 7 labels | 914×456, 7 bar groups × 3 bars |

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
