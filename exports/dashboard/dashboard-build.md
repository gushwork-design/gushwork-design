# Dashboard Build — the page shell

Figma: `↳ dashboard/ component+pattern-library`, group `dashboard-build` (`2146:17344`).
Component set `2140:16479`.

The top-level shell for **every** product/dashboard page. The dashboard-side
counterpart to the web's Page Build: where Page Build assembles a marketing page from
Folds, Dashboard Build frames a product page and its Sections drop into the slot.

## Variant properties

| Property | Values | Note |
|---|---|---|
| `Property 1` | `Default` | Single variant. The property is unnamed — `Property 1` is Figma's auto-generated name and is the literal key. |

Slot property: `Slot` — accepts main content.

## Structure — fixed, do not rearrange

```
Property 1=Default
COMPONENT (1440×888, HORIZONTAL, gap:8, pad:8)
├── FRAME "side-panel" (260×880, r:20, VERTICAL, gap:60, pad:24/16)
│   ├── FRAME "container" (228×445, VERTICAL, gap:40)
│   │   ├── FRAME "dashboard-title" (HORIZONTAL, gap:8)
│   │   │   ├── INSTANCE "gushwork-logo-(internal-use)" (32×32, r:8)
│   │   │   │   └── INSTANCE "gushwork-logo" (16 px, White, Only Symbol=yes)
│   │   │   └── TEXT "Dashboard title" (18px)
│   │   └── FRAME "list-groups" (VERTICAL, gap:24)
│   │       └── 3× FRAME "list-group" (VERTICAL, gap:0)
│   │           ├── INSTANCE "list-item" (Label=yes) → TEXT "LIST LABEL" (10px)
│   │           └── 2-3× INSTANCE "list-item" (default) → icon + "List Item" (14px)
│   └── FRAME "footer" (228×64, HORIZONTAL, gap:58, pad:8/0)
│       └── INSTANCE "user-card" (State=Default, r:12)
│           ├── FRAME "user info" (HORIZONTAL, gap:8)
│           │   ├── INSTANCE "Avatar" (Admin=true, Blue)
│           │   └── FRAME "name" (VERTICAL, gap:4)
│           │       ├── TEXT "Bruce Wayne" (12px)
│           │       └── TEXT "Designation" (10px)
│           └── FRAME "menu btn" (20×20, r:4)
│               └── INSTANCE "DotsThreeOutlineVertical"
└── FRAME "dashboard-container" (1164×872, r:20, VERTICAL, gap:0, pad-bottom:120)
    ├── INSTANCE "section/header" (VERTICAL, gap:20, pad:40/40/20/40)
    │   ├── TEXT page title (32px)
    │   └── FRAME "toolbar" (HORIZONTAL)
    │       ├── FRAME "controls" (HORIZONTAL, gap:12)
    │       │   ├── INSTANCE "controls/tab" (Medium, Selected)
    │       │   └── 3× FRAME "dropdown" (r:8) → label + CaretDown
    │       └── FRAME "refresh" (HORIZONTAL, gap:8)
    │           ├── TEXT "Updated 4s ago" (10px)
    │           └── FRAME "refresh btn" (28×28, r:8) → INSTANCE "ArrowClockwise"
    └── SLOT "Slot" (VERTICAL, gap:40, pad:40)
        └── (empty — accepts dashboard Sections)
```

## Fixed dimensions

| Part | Value |
|---|---|
| Shell | 1440×888, padding 8, **gap 0** — see below |
| Nav rail (`side-panel`) | **260** wide × 880, radius 20, padding 24/16 |
| Nav rail inner width | 228 |
| Content container | 1164×872, radius 20, padding-bottom 120 |
| Content slot | vertical, gap 40, padding 40 |
| Page header | padding 40/40/20/40, gap 20, title 32px |
| User card row | 228×48, radius 12 |

### Appearance — from design context (`2102:14019`) and the render

**The `side-panel` has no fill.** It is transparent, `--gw-radius-20`, padding
`16px` horizontal / `24px` vertical, `justify-content: space-between`. An earlier pass
here drew it as a white card; it is not one. The grey you see behind it is the shell.

| Part | Value |
|---|---|
| shell background | **`--gw-color-neutral-100`** (`#e7e8e9`) — sampled from the render |
| `side-panel` | **no fill** · `--gw-radius-20` · pad 16/24 · space-between |
| `dashboard-container` | `--gw-color-white` · `--gw-radius-20` |
| `dashboard-title` | logo tile + **Vert Grotesk Display Semibold 18px**, `--gw-color-black` |
| logo tile | `--gw-color-black` · `--gw-radius-8` · pad `--gw-space-8` · wraps the 16px White symbol |
| `container` gap | `--gw-space-40` between title and list-groups |
| `list-groups` gap | `--gw-space-24` between groups · **0 within a group** |
| group label | a `list-item` — **Inter Semi Bold 600, 10px**, uppercase, line-height 15, `--gw-color-neutral-400`, pad 4/8 |
| nav row | `list-item` — pad 8, gap 8, r8, Regular 16 icon, **Inter Medium 500, 14px**, `--gw-color-neutral-900` |
| user-card wrapper | **1px top border `--gw-color-neutral-alpha-10-black`**, pad 8/0, width 228 |

> **Those two weights were wrong here until 7 Aug 2026** — this table said Bold 14 and Bold 10,
> because it was written from a design-context read of the **instance inside this shell**, which
> reports `Inter:Bold` for both. The `list-item` **set** (`2102:13507`) says Medium 500 and
> Semi Bold 600. **The set wins.** `section-elements.md` had it right and this file contradicted
> it; a rail was built wrong from this table. When the two disagree, go to the set.

**The annotation's `gap:8` on the shell is wrong.** Figma's own coordinates place
`side-panel` at x=8 width 260 — ending at 268 — and `dashboard-container` at x=268. They
are **flush**; there is no gap. An 8px gap makes the container 1156 instead of 1164.

**The default shell shows no selected nav row.** All `list-item`s render identically.

`list-item` carries `hover` and `selected`, and **their fills are measured** — `hover` is
`--gw-color-neutral-25`, `selected` is `--gw-color-neutral-50`. See `section-elements.md`. (This
file previously said they were unmeasured; they are not.)


### Layout — verified box by box against Figma's coordinates

Nine boxes, all matching. Reproduce these exactly; several are counter-intuitive.

| Box | x | y | w | h |
|---|---|---|---|---|
| `side-panel` | 8 | 8 | 260 | **880** |
| `dashboard-container` | **268** | 8 | 1164 | **872** |
| `container` (title + groups) | 24 | 32 | 228 | 445 |
| `dashboard-title` | 24 | 32 | 228 | 32 |
| `list-groups` | 24 | 104 | 228 | 373 |
| `list-group` 1 | 24 | 104 | 228 | 119 |
| `list-group` 2 | 24 | 247 | 228 | 119 |
| `list-group` 3 | 24 | 390 | 228 | 87 |
| user-card wrapper | 24 | 800 | 228 | 64 |

Three traps:

1. **The rail is 880 tall; the container is 872.** The rail runs flush to the bottom of the
   1440×888 shell with no bottom padding, while the container keeps its 8px gap. The shell's
   padding is effectively `8px 8px 0`.
2. **`space-between` on the rail has exactly TWO children** — the `container` (which holds
   the title *and* the list-groups, gap `--gw-space-40`) and the user-card wrapper. Treating
   title, groups and user-card as three siblings pushes the groups to the vertical centre,
   which is wrong.
3. **The group-label row is 23 tall, not 32.** It is a `list-item`, but with `4px 8px`
   padding and a 15px line-height rather than a nav row's 8px padding — `4 + 15 + 4 = 23`.
   Inheriting the 32px nav-row height throws every group 9px out and cascades down the rail.

Group heights follow from that: `23 + 3×32 = 119` for a four-row group, `23 + 2×32 = 87`
for a three-row one, with `--gw-space-24` between groups and **no gap inside one**.

## Rules

**Use this shell for every dashboard — and only this shell.** Every dashboard page
*is* this component. The 260px rail and the content container are fixed. Never
hand-build dashboard chrome; use Dashboard Build and fill its slot. (Same discipline
as always starting a deck from the blank base — one source of truth for the frame.)

**Fill the slot with Sections.** The content slot accepts dashboard Sections —
`section/card-layout`, `section/progress-bar`, `section/With Dropdown`,
`section/section-element/Graph`, `section/Container`, `section/table`. Compose the page
by dropping Sections in. **Never place section-elements or loose content directly** in
the slot. If nothing fits, use `section/Container` and put custom content in its slot.

**Header is sticky; content is per-page.** `section/header` stays pinned at the top on
every page. Its content — page title, tabs, filter dropdowns, refresh — changes per
page. The shell and the sticky behaviour do not.

**Nav items group when needed.** The rail lists `list-item`s, grouped under uppercase
label rows (`list-item` with `Label=yes`, i.e. `Property 1=Variant4`) when the
navigation needs sections. Use a flat list when it doesn't. Add or remove list-groups
per the page structure.

**Follow the build structure.** Rail (internal logo + grouped list-items + user-card)
and container (sticky header + section slot). Only the slot content, the nav items, and
the header content change page to page.

## Composition — reuse, don't rebuild

The shell already instances its building blocks, and each inherits its own rules:

| Instanced | Rules live in |
|---|---|
| `gushwork-logo-(internal-use)` | `foundation/shared-components.md` |
| `list-item` | `section-elements.md` |
| `user-card` (embeds `Avatar`) | `section-elements.md`, `avatar.md` |
| `section/header` | `sections.md` |

Do not restyle any of them here.

## Surface-level dashboard rules

From `dashboard-usage-rules` (`2177:11486`). These sit above the individual component
rules and set defaults for the whole surface.

- Every dashboard page uses **Dashboard Build** for its structure. Don't hand-build
  chrome.
- Page content is composed from **Sections**, not loose elements.
- `section/header` is **sticky** at the top on every page, unless explicitly asked
  otherwise.
- Use controls (tabs, filter dropdowns, refresh) as the page requires.
- **Buttons:** use the dashboard Button component and follow its rules — `Primary`
  (black) / `Outline` / `Ghost`, sized to surrounding controls. **Never a blue button
  fill on dashboards.** Blue remains valid as a status/signal colour (Info toasts, blue
  badges) — the ban is on button *fills* only.
- **Avatars:** the Admin avatar is only for admins/owners. All other users get standard
  avatars.
- Everything else follows the rules of the specific component.

## Source notes

- The rules text (`2177:11496`) opens with pasted authoring chat — *"Good call — the
  dashboard button now has its own component… Slimmed the buttons section down to a
  pointer:"* — before the real rules begin. Ignore the preamble.
- The property is unnamed (`Property 1`). Renaming it in Figma would let this doc drop
  the caveat.
