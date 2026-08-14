# Data table — cell, row, pagination

Page `Dashboard Components` (`257:371`) in **`Q9L6q38dEj3Qu1JkjiT13y`** — the product file, not
the library. See `README.md` in this folder.

**Scope: dashboard / product.** Supersedes the `table-row` and `table` parts of
`exports/dashboard/section-elements.md`.

---

## `table-cell`

Set `271:528` · **10 variants** (5 × 2).

| Property | Values |
|---|---|
| `Type` | `header` · `label` · `metric` · `number` · `status` |
| `Theme` | `light` · `dark` |

Default width **137** — set `FILL` or a fixed width in the row.

| Type | Contents | Type style | Colour |
|---|---|---|---|
| `header` | label + 12px `ArrowsDownUp` sort affordance | `body-12-med` | `neutral/700`, icon `neutral/600` |
| `label` | 12px channel icon + label | `body-12-med` | `neutral/black` |
| `metric` | value over a `progress-bar Size=sm` (2px), gap `spacing/4` | `body-14-med` | `neutral/600` |
| `number` | value only | `body-12-med` | `neutral/600` |
| `status` | holds a `badge Size=sm` instance | — | — |

**Header labels are UPPERCASE.** The source read `channnel` — lowercase, with three n's. Typo
fixed and casing normalised to caps, ruled 13 Aug 2026.

⚠ **`header` binds `body-12-med`, and that is a fix.** In the screens the header text was Inter
12/16 Medium with **no text style attached**, even though `body-12-med` is an exact match. Same
for the stat-card label. Both are now bound.

⚠ The v1 file records cell text binding a **raw `#6a7077`**. That is `neutral/600` — bound
properly here.

**Dark — now a `Theme` variant, measured:** `header` → **`neutral/100`** (an earlier note said
`neutral/400`; that was wrong) · `label` → `neutral/white` · `metric` / `number` → `neutral/300` ·
`metric`'s bar → track `neutral/600` with the `/300` fill. **Component property:** `Value` (TEXT).

---

## `table-row`

Set `272:583` · **14 variants** (7 × 2).

| Property | Values |
|---|---|
| `Type` | `header` · `data` · `total` |
| `State` | `default` · `hover` · `selected` · `select-enabled` |
| `Theme` | `light` · `dark` |

Incomplete by design — valid combinations, each in both themes:

| Type | States |
|---|---|
| `header` | `default` · `select-enabled` |
| `data` | `default` · `hover` · `selected` · `select-enabled` |
| `total` | `default` |

**1092 wide.** Padding `px-24`, no vertical padding, gap **`spacing/32`**, `clipsContent`.

| Type | Height | Fill | Border |
|---|---|---|---|
| `header` | **44** | `neutral/25` | **bottom** 1px `neutral/100` |
| `data` | **56** | none | **bottom** 1px `neutral/25` |
| `total` | **56** | none | **top** 1px `neutral/100` |

| State | Fill |
|---|---|
| `default` | per Type above |
| `hover` | `neutral/25` |
| `selected` | **`primary/alpha-10`** |
| `select-enabled` | per Type; reveals the checkbox |

**`selected` is a ruling, not a measurement** — no selected row exists anywhere in the screens.
`primary/alpha-10` was chosen because blue is the system's signal colour and the tint already
appears in the channel-cell badge. Ruled 13 Aug 2026. ⚠ Note this **departs from v1**, where
`Selected` and `Hover` were the same `neutral/25` fill and selection was marked only by the
checkbox. If you are matching an existing table, check which behaviour it uses.

### Column structure

In order: `checkbox` (hidden unless `select-enabled`) · **`cell-channel` 120 FIXED** ·
`divider` (vertical, fills row height) · **`cells` group FILL**, gap `spacing/32`.

The `cells` group holds five `table-cell` instances, each `FILL` — so they share the remaining
width equally at 146.

⚠ **The screens are 160 / 160 / 137.3 / 137.3 / 137.3** — a mix of fixed and growing columns.
Equal `FILL` was chosen for the component because a fixed-width column set cannot adapt to a
different column count. If you need the screens' exact widths, set the first two to 160 FIXED.

⚠ **Two dead cells in the source.** Every row of both Channel Breakdown tables carries hidden
cells for `SPEND (USD $)` and `ROI` — leftovers from an earlier version. They are **not**
reproduced here. Their presence is why the header and body rows had different child order: hidden
children take no auto-layout space, so the columns did line up. Earlier reports of broken
alignment were wrong.

### The two tables in the screens

Both are this row with different column groups toggled — the toolbar checkboxes switch them:

| Table | Structure |
|---|---|
| Demos & Show-ups | channel 120 · divider · group 860 [160, 160, 137.3, 137.3, 137.3] |
| Spend & ROI | channel 120 · divider · group 556 [5 × 85.6] · divider · trailing group 240 [Spent, roi] |

The trailing group and its divider are **not** in the component. Add them as a second `cells`
group when you need the Spend & ROI shape.

**Dark — built, measured.** Every row sits on `neutral/black` inside a `neutral/900` card; borders
and the column divider are `neutral/800`. `hover` = `neutral/900` and `selected` = `neutral/black`
**plus** a `primary/alpha-10` tint layered on top are RULED — the dark screen draws neither. The
tint is layered rather than replacing the base, so the variant composites correctly in isolation.

---

## `pagination`

Set `278:598` · **2 variants** (`Theme` = `light` · `dark`).

**1094 × 52** — exactly the source. Padding `spacing/12`, `SPACE_BETWEEN`, no fill.

Left — `per-page`, gap `spacing/8`:
- `Items per page` · `button-14-med` · `neutral/600` (dark `neutral/300`)
- `control Kind=select, Style=outlined, Size=28`

Right — `pager`, gap `spacing/8`:
- `Page 1 of 4` · `button-14-med` · `neutral/600` (dark `neutral/300`)
- two `icon-button Size=28`, icons swapped to `ArrowLeft` / `ArrowRight` at 12px Weight=Regular

The dark variant now points at `icon-button Size=28, Theme=dark` for both arrows, whose border is
`neutral/700`. Swapping an icon-button resets its glyph to the default `ArrowsClockwise`, so the
ArrowLeft/ArrowRight swaps are re-applied explicitly.

⚠ **No disabled state on the arrows.** On page 1 the previous arrow should be non-interactive;
nothing in the source defines it. That is a finding, not a value to invent.
