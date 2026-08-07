# Section elements

Figma: group `section-elements` (`2146:17719`).

The reusable sub-components Sections are built from. The dashboard-side analog of
fold-elements: the small parts a Section assembles, rather than Sections themselves.

**Scope: dashboard / product only.**

## These are building blocks, not standalone sections

Reach for them **through the Section that contains them** — `section/card-layout`
instances `kpi-card` + `analytics-card`; `section/table` instances the `table` element,
which instances `table-row`. **Never place them loose on a dashboard page.** Compose a
Section, or use `section/Container` for custom content.

---

## `kpi-card` — the headline-metric card

`section/section-element/kpi-card` · set `2134:14581` · **6 variants** · 286×198, r:12.

| Property | Values |
|---|---|
| `Mode` | `dark`, `light`, `Mode3`, `Mode4`, `Mode5`, `Mode6` |
| `Type` | `Positive`, `Negative`, `Neutral` |

### `Mode` is not a light/dark switch — the names are misleading

Only **6 of the 18** combinations are built, and each `Mode` pairs with exactly one `Type`.
It is six fixed card styles, not a matrix:

| Variant | Node |
|---|---|
| `Mode=light, Type=Negative` | `2134:14580` |
| `Mode=dark, Type=Negative` | `2134:14579` |
| `Mode=Mode3, Type=Positive` | `2134:14989` |
| `Mode=Mode4, Type=Positive` | `2134:14980` |
| `Mode=Mode5, Type=Neutral` | `2134:15041` |
| `Mode=Mode6, Type=Neutral` | `2134:15032` |

**`Mode=light` renders a DARK card.** Measured: `2134:14580` (`light`) and `2134:14980`
(`Mode4`) both fill `--gw-color-neutral-900`, with white values and `neutral-300` labels.
The word `light` describes nothing about the result. Do not pick a Mode by its name —
pick the variant node, and check it.

### Appearance — from design context (`2134:14980`, `2134:14580`)

Identical across both measured variants except the badge:

| Part | Value |
|---|---|
| card | **286 wide, height content-driven** · `--gw-radius-12` · padding `--gw-space-20` · **gap `--gw-space-80`** |
| fill | **`--gw-color-neutral-900` on `Mode=light`/`Mode4`/`Mode6`; `--gw-color-neutral-25` on `Mode=dark`/`Mode3`/`Mode5`** — the names are inverted |
| title | `Inter Medium 10px`, **uppercase**, line-height 1.6, `--gw-color-neutral-300` |
| header icon | `Money` (`112:6455`) at 16px, top-right |
| value | **`--gw-text-h5`** — 32px Vert Grotesk Semibold, `--gw-color-white` |
| caption | `--gw-text-body-12-med` · `--gw-color-neutral-300` |

The 80px gap between header and value block is what makes the card 198 tall. It is a
spacer, not a design accident — don't collapse it.

**286 is the intrinsic width, not a fixed one.** Inside `section/card-layout` the cards
stretch to fill the 1084-wide section — 356 each at `KPI cards=3`. Treat 286 as a minimum.
The same applies to `analytics-card`: 160 intrinsic, 174 when six fill the row.

**The inline badge differs per Type, and not symmetrically:**

| Type | Badge fill | Badge text | Arrow |
|---|---|---|---|
| `Positive` | `--gw-color-green-alpha-10` | `--gw-color-green-300` | `ArrowUpRight` **Bold 12** |
| `Negative` | **`--gw-color-red-alpha-20`** | `--gw-color-red-300` | `ArrowDownRight` **Bold 12** |

**Note the alpha mismatch** — green uses the 10% step, red the 20%. Almost certainly
unintended; flagged rather than normalised.

These badge colours also **do not match the standalone Badge component's documented
mapping** (`green-100` fill / `green-500` text). The kpi-card's inline badge is its own
treatment. Don't substitute one for the other.

Placeholder copy ships as `card title` and `lorem ipsum` — replace both.

**Pick `Type` by the metric's direction:**

| Type | Badge | Arrow |
|---|---|---|
| `Positive` | Green | `ArrowUpRight` |
| `Negative` | Red | `ArrowDownRight` |
| `Neutral` | Neutral | `ArrowDownRight` |

**`Mode` sets the colour theme — match the surrounding Section.**

Only these 6 of the 18 possible `Mode × Type` combinations exist:

| Node | Variant |
|---|---|
| `2134:14580` | `Mode=light, Type=Negative` |
| `2134:14579` | `Mode=dark, Type=Negative` |
| `2134:14989` | `Mode=Mode3, Type=Positive` |
| `2134:14980` | `Mode=Mode4, Type=Positive` |
| `2134:15041` | `Mode=Mode5, Type=Neutral` |
| `2134:15032` | `Mode=Mode6, Type=Neutral` |

Asking for a combination outside this list resolves to nothing. `Mode3`–`Mode6` are
Figma auto-generated names and are the literal keys — `section/card-layout` references
`Mode4` directly, so they are load-bearing and must not be renamed casually.

```
COMPONENT (286×198, r:12, VERTICAL, gap:80, pad:20)
├── FRAME "header row" (HORIZONTAL, gap:34)
│   ├── TEXT card title (10px, uppercase)
│   └── INSTANCE icon (Size=32)
└── FRAME "metrics" (VERTICAL, gap:8)
    ├── FRAME "value row" (HORIZONTAL, gap:8)
    │   ├── TEXT value (32px)
    │   └── INSTANCE "badge" (trailing icon) → TEXT delta (12px) + arrow
    └── TEXT caption (12px)
```

---

## `analytics-card` — the compact metric card

Set `2134:14584` · **2 variants** · **160 wide**, r12.

| Node | Variant |
|---|---|
| `2134:14583` | `Mode=light` |
| `2134:14582` | `Mode=dark` |

### Appearance — from the set

| Part | `Mode=light` | `Mode=dark` |
|---|---|---|
| fill | `--gw-color-neutral-25` | **`--gw-color-neutral-800`** |
| title | Inter Medium 10, uppercase, lh 1 · `--gw-color-neutral-600` | · `--gw-color-neutral-400` |
| value | **Vert Grotesk Display Medium 20** · `--gw-color-black` | · `--gw-color-white` |
| caption | `--gw-text-body-12-med` · `--gw-color-neutral-600` | · `--gw-color-neutral-400` |

Padding `--gw-space-12`, gap `--gw-space-20`, inner stack gap `--gw-space-4`, `overflow: hidden`.

**The value is the display face at Medium 20 — not Inter, and not Semibold.** There is no
token for it; the heading ramp has no 20px step (h7 is 22 Medium). Tokenless, flagged.

**`Mode=dark` is `neutral-800`, not the `neutral-900` that kpi-card uses.** The two cards sit
side by side in `card-layout` and their dark treatments differ by one step.

Ships `card title` / `lorem ipsum` — replace both.

## `table` — the assembled data table

`section/section-element/table` · component `2205:15807` · **no variants** · 1084×606, r:12.

Sort toolbar + header row + 10 data rows + pagination. Use **inside `section/table`**
for browsable product data.

```
COMPONENT (1084×606, r:12, VERTICAL)
├── FRAME "table-toolbar" (HORIZONTAL, pad:16/24)
│   ├── FRAME "toolbar-left" (HORIZONTAL, gap:12)
│   │   ├── TEXT "Sort by" (14px)
│   │   ├── INSTANCE "controls/dropdown" (Size=Small, State=Closed)
│   │   └── INSTANCE "ArrowsDownUp" (Weight=Bold)
│   └── FRAME "toolbar-right" (empty)
├── FRAME "table-body" (VERTICAL)
│   ├── INSTANCE "table-row" (Type=Header, State=Default)
│   └── 10× INSTANCE "table-row" (Type=Data, State=Default)
└── FRAME "table-footer" (HORIZONTAL, pad:16/24)
    ├── FRAME "footer-left" → TEXT "Showing per page" + controls/dropdown (Small)
    └── FRAME "footer-center" (HORIZONTAL, gap:4)
        ├── INSTANCE "Button" (prev arrow, Ghost, Icon Only)
        ├── 4× page-number buttons
        ├── TEXT "..."
        ├── last-page button
        └── INSTANCE "Button" (next arrow, Ghost, Icon Only)
```

---

## `table-row`

`section/section-element/table-row` · set `2192:543` · **7 variants** · 1084×44.

| Property | Values |
|---|---|
| `Type` | `Header`, `Data` |
| `State` | `Default`, `Hover`, `Select enabled`, `Selected` |

| Node | Variant |
|---|---|
| `2192:538` | `Type=Header, State=Default` |
| `2177:12472` | `Type=Header, State=Select enabled` |
| `2177:12488` | `Type=Header, State=Selected` |
| `2192:539` | `Type=Data, State=Default` |
| `2192:540` | `Type=Data, State=Hover` |
| `2192:541` | `Type=Data, State=Select enabled` |
| `2192:542` | `Type=Data, State=Selected` |

`Type=Header, State=Hover` does not exist.

**`Type`** is Header or Data (content style). **`State` controls selection:**

- `Default` / `Hover` — checkbox hidden. **Use for read-only tables.**
- `Select enabled` — empty checkbox visible. Padding shifts to `12/24/12/52`.
- `Selected` — checkbox filled with a `Check` icon (12×12).

**Turn selection on only when the table supports row actions** (bulk-select).

Six columns, gap 40, padding 12/24. Widths: `col-price` 200, `col-sales` /
`col-revenue` / `col-stock` / `col-status` / `col-rating` 120 each, all ×20. Each row
ends with a `DotsThree` overflow menu.

---

### `table-row` appearance — from the set (`2192:539`, `Type=Data, State=Default`)

| Part | Value |
|---|---|
| row | **1084 wide** · fill `--gw-color-white` · **1px bottom border `--gw-color-neutral-200`** |
| padding | `12px 24px` · gap `--gw-space-12` |
| columns | inner group gap **40** · `col-price` 200 wide, the other five **120** each |
| cell text | **`--gw-text-body-14-med`** · **`--gw-color-neutral-600`** |
| rating cell | 16px star + value, gap `--gw-space-4` |
| overflow | `DotsThree` (`112:10164`) at **16px**, outside the column group |

**Data cells are `neutral-600`, not near-black.** The row reads quieter than a typical table.

**The bottom border is `neutral-200`** — a step darker than the `neutral-100` used for
hairlines elsewhere in the dashboard.

The star glyph resolves to `112:17221`, one of the three sets still named
`component_set-element` in Figma, so it cannot be found by icon name.

## `dropdown` — the in-section filter

`section/section-element/dropdown` · set `2142:584` · **2 variants** · 466 wide.

| Property | Values |
|---|---|
| `State` | `Open` (`2142:582`, 466×226), `Closed` (`2142:583`, 466×40) |

**Closed by default.** Opens to a `Detailed` options list. Use when a Section's data
needs filtering in place.

```
State=Closed
COMPONENT (466×40, VERTICAL, gap:4)
├── FRAME "trigger" (r:8, HORIZONTAL, gap:8, pad:8)
│   ├── FRAME "content" (HORIZONTAL, gap:4)
│   │   ├── INSTANCE "CalendarBlank" [HIDDEN]
│   │   └── FRAME "label row" (HORIZONTAL, gap:8)
│   │       ├── TEXT selected label (14px)
│   │       └── 2× badge (Neutral, Green)
│   └── INSTANCE "CaretDown" (Fill, Size=32)
└── FRAME "dropdown-options" [HIDDEN]

State=Open — same trigger + INSTANCE "dropdown-options" (Style=Detailed, r:8)
```

The trigger row carries **inline badges** next to the selected label.

---

## `dropdown-options` — the menu list

Set `2124:199` · **4 variants** · text props `Option 1`, `Option 2`, `Option 3`.

| Property | Values | Size |
|---|---|---|
| `Style` | `Simple` (`2124:192`) | 140×102 — text only |
| | `Icon` (`2124:182`) | 140×102 — text + action icon |
| | `Detailed` (`2137:587`) | 400×182 — text + status badges |
| | `Calendar` (`2138:579`) | 200×172 — date picker grid |

All r:8, pad:4, gap:4.

**Style by need.** Rarely placed directly — it is what dropdowns and user-cards open
into.

`Detailed` rows are 390×40 and carry two badges each (a `Neutral` label badge and a
status badge — `Green`/`Active` or `Red`/`Deactive`). `Calendar` is a GRID of 7 day
headers + 35 day cells, each 24×24, r:4.

---

## `list-item`

Set `2102:13507` · **4 variants**. Two shapes from one component: the uppercase group
label, and the nav row in three states.

| Node | Variant | Fill | Padding | Size |
|---|---|---|---|---|
| `2102:13505` | `Property 1=default, Label=no` | none | `8px` | 228 × 32 |
| `2102:13506` | `Property 1=hover, Label=no` | `--gw-color-neutral-25` | `8px` | 228 × 32 |
| `2102:13504` | `Property 1=selected, Label=no` | `--gw-color-neutral-50` | `8px` | 228 × 32 |
| `2102:13521` | `Property 1=Variant4, Label=yes` | none | `4px 8px` | 228 × **23** |

All four are `--gw-radius-8`, width 228, gap `--gw-space-8`.

### Type — read this off the component set, not off an instance

| | Token | Resolves to | Colour |
|---|---|---|---|
| nav row | **`--gw-text-button-14`** | Inter **Medium 500**, 14px, line-height 1 | `--gw-color-neutral-900` |
| group label | **`--gw-text-body-10-sem`** | Inter **Semi Bold 600**, 10px, line-height 15 | `--gw-color-neutral-400` |

Icon is `CirclesFour` (`112:13335`) at **`Weight=Regular, Size=16`**, coloured
`--gw-color-neutral-900` — the same as the label, so the row reads as one solid weight.
Greying it is wrong.

### Source conflict — the instance and the component set disagree on weight

Pulling design context on the **instance inside `dashboard-build`** (`2102:14027`) reports
`Inter:Bold` / `font-bold` for both the nav row and the group label. Pulling the
**component set** (`2102:13507`) reports `Inter:Medium` for the nav row and
`Inter:Semi_Bold` for the label — and names the underlying style `Button/button-14-med`.

**The component set wins.** It is the definition; the instance read is either an override
or an artefact of how the instance was resolved. An earlier pass here trusted the instance
and shipped the whole rail at Bold 700, which is visibly too heavy.

**When an instance and its component set disagree, measure the set.**

## `user-card`

Set `2125:200` · **3 variants** · 228 × 48.

| Node | Variant |
|---|---|
| `2125:197` | `State=Default` |
| `2125:198` | `State=Hover` |
| `2125:199` | `State=Clicked` |

Boolean prop `Show Menu` — default `true`. `Clicked` opens the Icon dropdown.

### Appearance — from the component set (`2125:197`)

| Part | Value |
|---|---|
| row | 228 × 48 · `--gw-radius-12` · padding `8px 4px` · space-between |
| avatar | **42.667 × 32** · radius **53.333** (`--gw-radius-80`) · `--gw-color-neutral-50` fill · **0.333px** `--gw-color-neutral-100` border |
| name | **`--gw-text-button-12`** — Inter Medium 12 · `--gw-color-black` |
| designation | **`--gw-text-button-10`** — Inter Medium 10 · `--gw-color-neutral-400` |
| name stack gap | `--gw-space-4` |
| menu | padding `--gw-space-4` · `--gw-radius-4` · `DotsThreeOutlineVertical` at **12px** |

**The avatar is a landscape pill, not a circle** — 42.667 × 32 at radius 53.333 clamps to a
stadium. Same proportion as the web `client/avatar`. Two components now, both pills.

**Name and designation are Medium, not Bold.** See the source-conflict note under
`list-item` — an instance read reports Bold; the set reports Medium.

## `gushwork-logo-(internal-use)`

Component `2102:13508` · **no variants** · 32×32, r:8, pad:8.

Wraps `gushwork-logo (Size=16 px, Type=White, Only Symbol=yes)`. The symbol-only tile
for product chrome. **Not for marketing** — use the main Gushwork Logo there. Full
rules in `foundation/shared-components.md`.

---

## Semantics inherited — don't redefine

| Element | Inherits |
|---|---|
| `kpi-card` badge colours | the Badge rule — green positive, red negative, neutral |
| `user-card` avatar | the Avatar rule — admin avatar for owner/admin |
| `table` pagination and sort buttons | the dashboard button rule — black / outline / ghost, **never blue** |

## Source notes

The rules text (`2168:17887`) opens with the meta-line *"Rules of Usage Updated Section
Elements block (rules only, table-row + table added):"* and then restates the
description already present in the description frame. Ignore the preamble.
