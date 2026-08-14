# Cards and chrome — stat, metric, shell, topbar, sidebar, headers

Page `Dashboard Components` (`257:371`) in **`Q9L6q38dEj3Qu1JkjiT13y`** — the product file, not
the library. See `README.md` in this folder.

**Scope: dashboard / product.**

---

## `stat-card`

Set `275:533` · **2 variants** (`Theme` = `light` · `dark`). **218 × 132** (source 217.6).

`radius/12`, padding `spacing/12`, gap `spacing/16`. Inner `body` frame padding `spacing/4`, gap
`spacing/16`.

Structure:
- `label-row` — gap `spacing/8`, label **grows**, then a `status-dot` 8px
- `value-block` — gap `spacing/8`
  - `value-row` — `SPACE_BETWEEN`, cross-align **MAX** (baselines sit on the bottom)
    - `value` column, gap `spacing/4`: the number, then a `of N` sub-line
    - the percentage, right-aligned
  - `progress-bar Size=md` (4px), **FILL**

| Part | Type | Light | Dark |
|---|---|---|---|
| Surface | — | `neutral/white` + 1px `neutral/100` | `neutral/900` + 1px `neutral/800` |
| Label | `body-12-med` | `neutral/700` | **`neutral/400`** |
| Value | `Dashboard/display-28-med` ⚠ no token | `neutral/black` | `neutral/white` |
| Sub-line | `body-12-med` | `neutral/500` | `neutral/500` — **unchanged** |
| Percentage | `body-12-med` | `neutral/500` | `neutral/500` — **unchanged** |
| Progress track | — | `neutral/200` | `neutral/600` |
| Progress fill | — | `green/400` | `green/300` |
| Status dot | — | `green/400` | `green/400` — **unchanged** |

Every dark value measured off the dark screen. **The sub-line and percentage do not change** — a
sensible guess steps them down and is wrong.

**Component properties:** `Label` · `Value` · `Sub` · `Percent` (TEXT).

⚠ Supersedes `kpi-card` and `analytics-card` in `section-elements.md`, whose `Mode` names are
**inverted** (`Mode=light` renders a dark card). This component has no such defect — `Theme=light`
is light.

---

## `metric-card`

Set `275:546` · **2 variants** (`Theme`). **274 × 124** — the run-rate card.

`radius/12`, padding **`spacing/16`** — *not* `spacing/12` like `stat-card` — gap `spacing/16`,
`SPACE_BETWEEN` horizontal.

`body` column, gap `spacing/16`: label `body-12-med`, then a value block at gap `spacing/4` —
`Dashboard/display-28-med` over a `body-12-med` `neutral/500` sub-line.

**No progress bar.** Same light/dark token mapping as `stat-card`.

**Component properties:** `Label` · `Value` · `Sub` (TEXT).

⚠ The padding difference between the two cards is measured, not an error. `stat-card` is 12,
`metric-card` is 16.

---

## `card-shell`

Set `276:521` · **6 variants** (3 × 2). Default **1120 × 200**, `content` slot fills.

| Size | Radius | Padding | Where |
|---|---|---|---|
| `lg` | **`radius/16`** | `spacing/12` | hero card, table card |
| `md` | `radius/12` | `spacing/12` | stat and run-rate cards |
| `sm` | `radius/8` | 0 | inner surfaces — table grid wrapper, inset panels |

Light `neutral/white` + 1px `neutral/100`; dark `neutral/900` + 1px `neutral/800`.

**Two radius tiers are deliberate** — outer containers 16, nested cards 12, inner surfaces 8.
Ruled 13 Aug 2026. `--gw-radius-16` already existed; the screens were using a **raw 16**, which is
why it looked like a missing token.

---

## `topbar`

Set `279:629` · **2 variants** (`Theme`). **1440 × 60**.

Padding `px-40` (`spacing/40`), `SPACE_BETWEEN`, vertically centred. Bottom border 1px only.

| Part | Light | Dark |
|---|---|---|
| Fill | `neutral/50` | `neutral/900` |
| Bottom border | 1px `neutral/100` | 1px `neutral/800` |
| Title | `neutral/black` | `neutral/white` |
| Caret icon | `neutral/600` | `neutral/300` |

`dashboard-title` — gap `spacing/8`: `gushwork-logo-(internal-use)` **32 × 32**, the dashboard
name in **`Dashboard/display-20-sem`** ⚠ no token, then a `CaretDown` 16 in a 24 × 24
`radius/4` tile.

`actions` — gap `spacing/8`: a `control Kind=button, Style=outlined, Size=36` (`Sync Now`) and
`icon-toggle-group`.

⚠ **The source uses a raw 14px vertical padding.** Replaced with vertical centring on a fixed 60h
— identical result, and on-token. Noted 13 Aug 2026.

⚠ The rail title is **the dashboard's name, not the company's** — v1 ruling, still holds.

---

## `sidebar`

Set `280:1032` · **4 variants** (`State` × `Theme`).

| State | Width | Height |
|---|---|---|
| `expanded` | **240** | 828 |
| `collapsed` | **64** | 828 |

Fill `neutral/50` / `neutral/900`; **right** border 1px `neutral/100` / `neutral/800`.
`SPACE_BETWEEN` vertical — nav at the top, footer pinned at the bottom.

- `collapse-row` — padding `spacing/4`, an `icon-button Size=20`. Chevron is `CaretDoubleLeft`
  when expanded, **`CaretDoubleRight`** when collapsed. Right-aligned expanded, centred collapsed.
- `list-groups` — padding `spacing/20` (collapsed: `spacing/8`), gap `spacing/24`
- `group-label` — padding `py-4 px-8`, **`body-10-sem`** on `neutral/400`
- nav rows — `control Kind=nav`, `FILL` width
- `footer` — padding `spacing/20` sides and top, **`spacing/32`** bottom; a `control Kind=user`

**`body-10-sem` is an existing library style** — Inter Semi Bold 10/15, an exact match for the
group label. Nothing new was created for it; the screens simply had it unbound.

⚠ **`collapsed` is NEW — it was never designed.** The collapse chevron existed in the screens but
no collapsed state did. 64 wide with 32 × 32 icon cells at `radius/8`; labels and group headers
hidden; footer shows the avatar only. Declared 13 Aug 2026. The width is a judgement call.

⚠ The v1 rail is **260** wide (`dashboard-build.md`); this sidebar is **240**, measured from the
screens. If you are building the v1 `dashboard-build` shell, its 260 still applies — 8 + 260 +
1164 + 8 = 1440. These are two different shells; do not mix the numbers.

---

## `page-header`

Set `278:567` · **2 variants** (`Theme`). **1120 × 113** — exactly the source.

Vertical, gap `spacing/24`, no fill.

- Title — **`Dashboard/display-44-sem`** ⚠ no token — `neutral/black` / `neutral/white`
- `controls-row` — `SPACE_BETWEEN`, gap `spacing/16`, centred
  - `filters` — gap `spacing/16`: a `tab-group`, then `period-meta` (`Day 18 of 30`,
    `button-10-med`, `neutral/600` / `neutral/300`)
  - `action` — a `control Kind=button, Style=outlined, Size=36` (`Compare`)

⚠ Distinct from `section-header` below, and from the v1 `section/header` (1164 × 146, a 32px
`h5` title). Three different headers now exist; pick by tier — page title, section title, or the
v1 sticky section header.

---

## `section-header`

Set `276:560` · **2 variants** (`Theme`). **1120 × 24**.

Padding `px-8` (`spacing/8`), `SPACE_BETWEEN`, gap `spacing/8`, no fill.

- `title-group` — gap `spacing/8`: title `body-16-sem` `neutral/black` / `neutral/white`, then a
  qualifier `body-16-reg` `neutral/500` / `neutral/300` (`for last month`, `per biz day`)
- a `legend` instance on the right, optional

The qualifier is part of the pattern, not decoration — it states the period the section covers.

---

## `legend`

Component `276:522` (not a set). **236 × 16** — exactly the source.

Gap **`spacing/32`** between items; within an item, gap `spacing/4`. Each item is a `status-dot`
8px plus a `body-12-med` label on `neutral/700`.

Ships `On track` · `Pending` · `Behind` — matching the three `status-dot` states.

**Dark override:** label → `neutral/300`. The dots stay at `/400`.
