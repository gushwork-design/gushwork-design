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

`section/section-element/analytics-card` · set `2134:14584` · **2 variants** · 160×94, r:12.

| Property | Values |
|---|---|
| `Mode` | `light` (`2134:14583`), `dark` (`2134:14582`) |

Use for secondary metrics beside a KPI. `Mode` matches the Section. No icon, no badge —
a simplified kpi-card.

```
COMPONENT (160×94, r:12, VERTICAL, gap:20, pad:12)
├── TEXT card title (10px, uppercase)
└── FRAME "metrics" (VERTICAL, gap:4)
    ├── TEXT value (20px)
    └── TEXT caption (12px)
```

---

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

## `list-item` — a nav/menu row

Set `2102:13507` · **4 variants** · 228 wide · instance-swap prop `icon` (default `CirclesFour`).

| Property | Values |
|---|---|
| `Property 1` | `default`, `hover`, `selected`, `Variant4` |
| `Label` | `no`, `yes` |

| Node | Variant | Size |
|---|---|---|
| `2102:13505` | `Property 1=default, Label=no` | 228×32 |
| `2102:13506` | `Property 1=hover, Label=no` | 228×32 |
| `2102:13504` | `Property 1=selected, Label=no` | 228×32 |
| `2102:13521` | `Property 1=Variant4, Label=yes` | 228×23 |

`default` / `hover` / `selected` are **interaction states, not a choice** — icon (16px)
+ text (14px), r:8, gap:8, pad:8.

**Use `Property 1=Variant4, Label=yes` for an uppercase group-header row** within a
list — text only, 10px uppercase, pad:4/8.

Both the property name (`Property 1`) and the value `Variant4` are Figma
auto-generated and are the literal keys. They are what `dashboard-build` references, so
they are load-bearing.

---

## `user-card` — the user identity row

Set `2125:200` · **3 variants** · 228×48, r:12 · boolean prop `Show Menu` (default true).

| Property | Values |
|---|---|
| `State` | `Default` (`2125:197`), `Hover` (`2125:198`), `Clicked` (`2125:199`) |

```
State=Default / Hover
COMPONENT (228×48, r:12, HORIZONTAL, gap:12, pad:8/4)
├── FRAME "user info" (HORIZONTAL, gap:8)
│   ├── INSTANCE "Avatar" (Style=1, Color=Blue, Admin=true)
│   └── FRAME "name block" (VERTICAL, gap:4)
│       ├── TEXT name (12px)
│       └── TEXT designation (10px)
└── FRAME "menu button" (20×20, r:4) → INSTANCE "DotsThreeOutlineVertical"

State=Clicked — same + INSTANCE "dropdown-options" (Style=Icon)
                       ├── "Sign out" + INSTANCE "SignOut"
                       └── "Refresh"  + INSTANCE "ArrowCounterClockwise"
```

`Show Menu` toggles the three-dots action. `Clicked` opens the `Icon` dropdown.

The avatar follows the Avatar rule — **Admin avatar for owner/admin only**. See
`avatar.md`.

---

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
