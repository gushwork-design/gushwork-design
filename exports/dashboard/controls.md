# Controls — tab, dropdown, toggle

Figma: group `control` (`1578:744`).

Navigation, selection, and switching elements. Used inside `section/header`,
`section/table` toolbars and footers, and anywhere a dashboard needs in-place filtering.

**Scope: dashboard / product.**

---

## `controls/tab`

Set `1589:605` · **9 variants** (3 × 3), complete.

| Property | Values |
|---|---|
| `Size` | `Small`, `Medium`, `Large` |
| `Show` | `Selected`, `Hover`, `Default` |

| Node | Variant | Size |
|---|---|---|
| `1589:572` | `Size=Small, Show=Selected` | 230×28 |
| `1589:583` | `Size=Medium, Show=Selected` | 293×46 |
| `1589:594` | `Size=Large, Show=Selected` | 313×48 |
| `1590:617` | `Size=Small, Show=Hover` | 230×28 |
| `1590:628` | `Size=Small, Show=Default` | 230×28 |
| `1590:639` | `Size=Medium, Show=Hover` | 293×46 |
| `1590:650` | `Size=Medium, Show=Default` | 293×46 |
| `1590:661` | `Size=Large, Show=Hover` | 313×48 |
| `1590:672` | `Size=Large, Show=Default` | 313×48 |

Ships **5 tab items**. `Show` is an interaction state, not a choice — the component
handles it.

| Size | Outer pad | Item pad | Font |
|---|---|---|---|
| `Small` | 4 | 8 × 4 | 12px |
| `Medium` | 8 | 12 × 8 | 14px |
| `Large` | 8 | 12 × 8 | 16px |

`section/header` uses `Size=Medium, Show=Selected`.

```
COMPONENT (HORIZONTAL, gap:8, pad per size)
└── 5× FRAME "tab item" (HORIZONTAL, gap:4)
    └── TEXT "Tab"
```

---

## `controls/dropdown`

Set `1589:669` · **9 variants**.

| Property | Values |
|---|---|
| `Size` | `Small`, `Medium`, `Large` |
| `State` | `Closed`, `Open` |
| `Color` | `Grey`, `White` |

| Node | Variant | Size |
|---|---|---|
| `1589:606` | `Size=Small, State=Closed, Color=Grey` | 120×28 |
| `1589:612` | `Size=Medium, State=Closed, Color=Grey` | 144×44 |
| `1589:618` | `Size=Large, State=Closed, Color=Grey` | 170×48 |
| `1589:624` | `Size=Small, State=Open, Color=Grey` | 140×164 |
| `1589:639` | `Size=Medium, State=Open, Color=Grey` | 160×180 |
| `1589:654` | `Size=Large, State=Open, Color=Grey` | 180×192 |
| `2199:739` | `Size=Small, State=Closed, Color=White` | 96×28 |
| `2199:744` | `Size=Medium, State=Closed, Color=White` | 144×44 |
| `2199:749` | `Size=Large, State=Closed, Color=White` | 170×48 |

**`Color=White` exists in `Closed` only.** There is no `Color=White, State=Open`
variant — if you need an open white dropdown, that is a gap to report.

**The structure annotation (`2152:17853`) documents only `Size × State` = 6 variants and
never mentions `Color`.** The `Color` property is real and undocumented. Use the table
above, not the annotation.

Pick `Color` by the surface the trigger sits on — `Grey` on the default gray dashboard
canvas, `White` on a white panel.

```
State=Closed
COMPONENT (HORIZONTAL, gap:8, pad per size)
├── FRAME "content row" (HORIZONTAL, gap:4)
│   ├── INSTANCE "CalendarBlank" (leading icon, swappable)
│   └── TEXT label
└── INSTANCE "CaretDown" → VECTOR

State=Open
COMPONENT (VERTICAL, gap:4)
├── FRAME "trigger row" (same as Closed)
└── INSTANCE "input/dropdown-options" (VERTICAL, pad:4, gap:4)
    └── 4× FRAME "hover" (HORIZONTAL, pad:8) → TEXT "Option n"
```

| Size | Pad | Gap | Trigger font | Option font |
|---|---|---|---|---|
| `Small` | 8 | 8 | 12px | 12px |
| `Medium` | 12 | 12 | 14px | 12px |
| `Large` | 16 | 16 | 16px | 14px |

Note `State=Open` instances `input/dropdown-options` — the **web** input primitive —
rather than the dashboard `dropdown-options` (`2124:199`). Two different option-list
components are in play across the two dropdown families; see `section-elements.md`.

Used by `section/table` for the sort control and the page-size control, both at
`Size=Small`.

---

## `controls/toggle`

Set `1591:578` · **6 variants** (3 × 2), complete.

| Property | Values |
|---|---|
| `Size` | `Large`, `Medium`, `Small`, **`X-Small`** (ruled — see below, not yet in Figma) |
| `State` | `Off`, `On` |

| Node | Variant | Size |
|---|---|---|
| `1591:572` | `Size=Large, State=Off` | 60×32 |
| `1591:573` | `Size=Medium, State=Off` | 52×28 |
| `1591:574` | `Size=Small, State=Off` | 44×24 |
| `1591:575` | `Size=Large, State=On` | 60×32 |
| `1591:576` | `Size=Medium, State=On` | 52×28 |
| `1591:577` | `Size=Small, State=On` | 44×24 |

```
State=Off   COMPONENT (HORIZONTAL, gap:4, pad:4)
            ├── FRAME "knob"
            └── FRAME "track space"

State=On    COMPONENT (HORIZONTAL, gap:4, pad:4)
            ├── FRAME "track space"   ← child order swapped
            └── FRAME "knob"
```

`On` and `Off` are the same tree with the child order reversed — the knob slides by
auto-layout, not by absolute positioning. `State` is bound to data, not a design choice.

### `Size=X-Small` — 36 × 20. RULED, pending Figma.

Ruled by Utsav, 7 Aug 2026. `Small` at 44×24 is **too heavy for a section header**, where it
sits beside a 12px caret, a 14px label and 24px badges — it becomes the largest thing in the
row. There was nothing below `Small`, so builds either used an oversized toggle or invented
one.

The size **continues the set's own ramp** — every measured step adds 8 to the width, 4 to the
height and 4 to the knob, with padding fixed at 4 and travel = track − knob:

| Size | Track | Knob | Travel |
|---|---|---|---|
| `Large` | 60 × 32 | 24 | 28 |
| `Medium` | 52 × 28 | 20 | 24 |
| `Small` | 44 × 24 | 16 | 20 |
| **`X-Small`** | **36 × 20** | **12** | **16** |

**Use `X-Small` inside a section header, a table row, or any dense toolbar.** `Small` remains
the default for a settings row or a form.

### Appearance — MEASURED off the set, 7 Aug 2026

| Part | Value |
|---|---|
| track `Off` | `--gw-color-neutral-200` |
| track `On` | **`--gw-color-neutral-900`** — **not blue** |
| knob | `--gw-color-white` on `--gw-shadow-s2`, `--gw-radius-full` |
| transition | `--gw-motion-fast` on the track fill |

**`State=On` is `neutral/900`.** This was independently arrived at twice on the same day — once
by measuring the set, and once by ruling that a flipped toggle is interaction state rather than
data (see below). They agree. A blue toggle is wrong on both counts.

## Blue is a data colour. Black is a control-state colour. RULED.

Ruled by Utsav, 7 Aug 2026. This supersedes the narrower "never a blue button **fill**"
phrasing, which left control states unclassified and let blue leak into selection.

| Carries | Colour | Examples |
|---|---|---|
| **Data and status** | blue | `section/progress-bar` fill, chart series and bars, Info toasts, blue badges, focus rings |
| **Interaction state** | black / near-black | a selected calendar date, `controls/toggle` `State=On`, any selected / active / pressed state |

**If you are about to fill something blue, ask which of the two it is.** A chosen date and a
flipped toggle are the user's state, not the data — they go black.

**Which black?** Use the component's own measured value where one exists — `controls/toggle`
`State=On` is `neutral/900`, `Button Primary` is `neutral/black` `#0d0d0d`. Where none exists,
`--gw-color-black`. The two are one step apart and the measurement wins over the pattern.

Action tiers are unchanged: `Primary` black, `Outline`, `Ghost`. Never a blue button fill.

**This rule was corroborated by measurement, not just reasoning.** The 7 Aug re-measurement pass
found `controls/toggle` `State=On` already drawn `neutral/900` in Figma while builds were
rendering it blue — the rule and the file agreed; only the implementations were wrong.

## Hover, open and focus — RULED. The variants exist; their fills never did.

`controls/tab Show=Hover` and the dropdown states exist in Figma with **no measured fill**, so
every build guessed. These are the values, each derived from the nearest measured neighbour:

| Control | State | Value | Why this value |
|---|---|---|---|
| `controls/tab` | hover (unselected) | `--gw-color-neutral-alpha-50-white` | moves **toward** the white `Selected` state instead of darkening away from it |
| `controls/dropdown` `Color=Grey` | hover | `--gw-color-neutral-100` | one step up from its `neutral-50` trigger |
| `controls/dropdown` `Color=White` | hover | `--gw-color-neutral-25` | one step down from white |
| `Button` `Primary` | hover | `--gw-color-neutral-900` | the lightest near-black in the ramp |
| `Button` `Outline` / `Ghost` | hover | `--gw-color-neutral-25` | the measured `list-item` hover |
| any focusable element | focus | `--gw-focus-ring` at `--gw-focus-offset` | see `states.md` |

All hover transitions use `--gw-motion-fast`.

## `controls/dropdown` — MEASURED 8 Aug 2026

Read off `1589:612` (Grey/Medium/Closed), `2199:744` (White/Medium/Closed) and `1589:639`
(Grey/Medium/Open). **Both sections below were previously RULED, and the rulings were wrong in
five places** — including one element that does not exist.

### The trigger

| | `Color=Grey` | `Color=White` |
|---|---|---|
| Fill | `--gw-color-neutral-50` | `--gw-color-neutral-white` |
| Border | **none** | **1px `--gw-color-neutral-100`** |
| Padding · radius | `p-12` · `--gw-radius-12` | identical |
| Label | `--gw-text-body-14-med` on `--gw-color-neutral-900` | identical |
| Caret | `CaretDown` **12px**, `gap-4` from the label | identical |

Layout is `justify-between` — label group left, caret hard right. `Medium` is 144 × 44; `p-12`
around a 20px line box = 44. ✓

**✗→✓ The Grey variant has no ring.** The old ruling gave White "a 1px inset ring … matching how
the Grey variant is constructed". Grey is a bare fill with no border at all, and White's ring is
a real **border** — it occupies layout. The token was right; the reasoning and the construction
were not.

**`Color=White` exists only at `State=Closed`.** Nine variants = 3 sizes × Grey(Closed, Open) +
3 sizes × White(Closed). There is no White + Open.

### `State=Open` — measured, not ruled

Figma had all of this. It was never a gap.

| Part | Measured |
|---|---|
| Wrapper | column, **`gap-4`**, `items-end`, **160 wide** at `Medium` |
| Trigger | as above, plus **`min-w-140`**; the caret **flips** (`-scale-y-100`) |
| Menu | `--gw-color-neutral-white` · **1px `--gw-color-neutral-50`** · `--gw-radius-8` · `p-4` · `gap-4` · `overflow: clip` · **`--gw-shadow-s3`** · `w-full` |
| Option row | `p-8` · `--gw-radius-4` · **`--gw-text-button-12-med`** on `--gw-color-neutral-900` · `gap-8` |
| Option hover | **`--gw-color-neutral-50`** |

**The menu is wider than its trigger** — 160 against 144, right-aligned by `items-end` on the
wrapper. The menu is not `width: 100%` of the trigger.

Five corrections against the old ruling:

| | Ruled | **Measured** |
|---|---|---|
| Menu border | 1px inset `neutral-100` | **1px `neutral/50`** |
| Option type | `body-12-med` | **`button-12-med`** — line-height 1, not the body ramp |
| Option hover | `neutral-25` | **`neutral/50`** |
| Selected mark | `Check` 12px in `primary-500` | **does not exist** — no check, tick or mark of any kind is in the symbol |
| Menu width | implied to match the trigger | **160 vs 144**, right-aligned |

Fill, radius, shadow, padding, gap, option padding, option radius and the caret flip were all
ruled correctly. **The invented checkmark is the one that matters** — a build following the old
ruling renders an affordance the design does not have, and a single-select dropdown then shows
two competing signals for the current value.

**Closes on outside click and on `Escape`.** Both, not one. Still a behaviour ruling — Figma
carries no interaction model.

## `dropdown-options` `Style=Calendar` — appearance. RULED.

Geometry is measured (200 × 172, 7 day headers + 35 cells at 24×24, `--gw-radius-4`). The
states were not:

| Part | Value |
|---|---|
| day header | `--gw-text-body-10-sem` · `--gw-color-neutral-400` |
| day cell | `--gw-text-body-10-med` · `--gw-color-neutral-900` |
| hover | `--gw-color-neutral-100` |
| **selected** | **`--gw-color-black`** with `--gw-color-white` text — a control state, not data |
| selected + hover | `--gw-color-neutral-900` |
| outside the month | transparent text, not interactive |

**Known gap — there is no range affordance.** The variant is a bare 7×5 grid: no start/end
cell, no in-between fill, no two-month view. A `Custom` date filter in a `section/header`
almost certainly wants a range. **Single-select is what the component supports** — if you need
a range, that is a finding to report, not a thing to invent.

---

## Source notes

The Controls description (`1578:749`) is accurate but generic. The group has **no
"Rules of Usage" text at all** — only a description and a Component Structure blob
(`2152:17853`), and that blob omits the `Color` property on `controls/dropdown`. The
usage guidance above is derived from how `section/header` and `section/table` actually
instance these controls.

> **Re-measured 7 Aug 2026 off the sets, correcting values written from instances.**
>
> - `controls/toggle` (`1591:578`) — **`On` is `--gw-color-neutral-900`, not blue.** `Off` is
>   `--gw-color-neutral-200`. Built as **two white knobs, one at `opacity: 0`** — `p-4`, `gap-4`,
>   `--gw-radius-40`, knob `--gw-radius-60` with `Shadows/S3`. Knob 16/20/24 gives 44×24, 52×28,
>   60×32.
> - `controls/tab` (`1589:605`) — **five tabs, not three.** Container `--gw-color-neutral-50`,
>   `gap-8`; `Small` is `p-4 r8`, `Medium`/`Large` `p-8 r12`. **Every label is
>   `--gw-color-neutral-900`** — inactive tabs are not greyed. `Selected` adds
>   `drop-shadow(0 16px 16px rgba(88,92,95,.1))`.
> - The set nodes are `1589:605`, `1589:669` and `1591:578`. The ids previously recorded here
>   (`1589:572`, `1591:572`, `2152:17853`) are symbols or stale.
