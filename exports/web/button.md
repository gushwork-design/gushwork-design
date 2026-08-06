# Web Button

## Which button?

**This is the marketing-web button.** There is a *different* component with the same
name for the dashboard.

| Surface | Component | Node | `Style` values |
|---|---|---|---|
| **Marketing web** | `Button` — this file | `1457:668` | `Blue`, `Black`, `Outlined/ black`, `Outlined / white`, `Text/ black`, `Special/ With People`, `Special/ Glowing`, `White` |
| Dashboard / product | `Button` — see `exports/dashboard/button.md` | `2203:931` | `Primary`, `Outline`, `Ghost` |

**Both sets are literally named `Button`, and both expose a property named `Style` whose
value sets are disjoint.** `Style=Blue` is valid here and invalid on the dashboard.
`Style=Primary` is valid there and invalid here. Neither component's rule text states its
own scope, which is why this block exists.

Figma: group `button` (`1674:37755`), set `1457:668`.

---

## Variant properties — 220 of 288

| Property | Values |
|---|---|
| `Style` | `Blue`, `Black`, `Outlined/ black`, `Outlined / white`, `Text/ black`, `White`, `Special/ With People`, `Special/ Glowing` |
| `State` | `Active`, `Hover`, `Disabled` |
| `Size` | `Small`, `Medium`, `Large` |
| `Icon Placement` | `None`, `Trailing`, `Leading`, `Icon Only` |

**Note the inconsistent spacing inside the style keys** — `Outlined/ black` has a space
only *after* the slash, `Outlined / white` has one on *both* sides, `Text/ black` after
only. These are literal keys. Copy them exactly; do not normalise.

Six styles are complete at 36 variants each (3 `State` × 3 `Size` × 4 `Icon Placement`).

**The two `Special/*` styles have only 2 variants each**, both at
`Size=Large, Icon Placement=Trailing`:

| Node | Variant |
|---|---|
| `1480:2412` | `Style=Special/ With People, State=Active, Size=Large, Icon Placement=Trailing` |
| `1485:5830` | `Style=Special/ With People, State=Hover, Size=Large, Icon Placement=Trailing` |
| `1480:2421` | `Style=Special/ Glowing, State=Active, Size=Large, Icon Placement=Trailing` |
| `1485:5839` | `Style=Special/ Glowing, State=Hover, Size=Large, Icon Placement=Trailing` |

There is **no** Special button at Small or Medium, no Disabled state, and no other icon
placement. The rule below asks for usage the component cannot satisfy — see Source notes.

---

## Choosing `Style` — a three-level decision

Work down in order. Background wins over page type.

### 1. Is the button on a coloured background?

| Background | Primary | Secondary |
|---|---|---|
| **Blue** | `White` | `Outlined / white` |
| **Black** | `Blue` | — |

### 2. Otherwise, pick by page type

| Page type | Primary | Secondary |
|---|---|---|
| **Brand page** | `Black` | `Outlined/ black` |
| **Ad page** | `Blue` | `Outlined/ black` |

Page type comes from `page-build`'s `Type` property (`Brand` | `Ads`), set once at the
page level and inherited downward. See `page-shell.md`.

### 3. Special styles — only when asked

- `Special/ With People` — only when explicitly asked.
- `Special/ Glowing` — usually in forms, or to add emphasis when required.

### `Text/ black`

36 variants, fully built, and **documented nowhere in the rule**. Treat it as the
lowest-emphasis tier — a text link styled as a button — and confirm before using it as a
primary or secondary CTA.

## Size

| Size | Use |
|---|---|
| `Medium` | **All folds.** The default. |
| `Large` | Only when asked. |
| `Small` | Navbars, and other elements per the design direction. |

## Appearance — from design context, not the annotation

**`border-radius` is `--gw-radius-12` on every size and style.** These are *not* pills.
The value is a raw 12px in Figma and is not variable-bound, so it will not show up in a
`get_variable_defs` call — it has to be read from the component.

| `Size` | Height | Width `None` | Width `Trailing`/`Leading` | `Icon Only` | Label token |
|---|---|---|---|---|---|
| `Small` | 36 | 99 | 123 | 36 × 36 | `--gw-text-button-14` |
| `Medium` | 44 | 126 | 151 | 44 × 44 | `--gw-text-button-16` |
| `Large` | 56 | 144 | 166 | **58 × 58** | `--gw-text-button-18` |

Gap between label and icon is `--gw-space-8` (`--gw-space-12` on the Special styles).
`Large` carries padding `16px 20px 16px 24px` — **asymmetric**, more on the leading side.
Shadow is `--gw-shadow-s2`. Widths are the component's intrinsic sizes; a button that
hugs its label will differ, but the heights are fixed.

**`Icon Only` at `Large` is 58×58, not 56×56** — the one size that doesn't match its row.

**Do not copy the dashboard button's dimensions.** Those are 88×28 / 115×44 / 134×48 and
belong to a different component — see `exports/dashboard/button.md`.

## Icon Placement

`None`, `Leading`, `Trailing`, or `Icon Only`. Icons are Phosphor instances — use `Bold`
weight inside buttons. See `foundation/shared-components.md`.

**The trailing icon is `ArrowUpRight`** (Figma `112:4802`), committed at
`assets/icons/arrow-up-right.svg`. It is 18px inside a `Large` button. The `Leading` and
`Icon Only` default glyph is a plus.

## Label copy

**Sentence case, with one fixed exception: the primary CTA reads `Book a Demo`.**

The rule text in Figma says "Book a call"; the page shell, navbar, footer, hero, and CTA
fold all render "Book a demo", as do four of the six rules that mention it. Neither is
the standard — **write `Book a Demo`**, capitalised, and do not generalise that
capitalisation to any other label. See `foundation/voice.md` for the full ruling and the
evidence.

Secondary CTA is `Calculate ROI with Gushwork`.

## Phone breakpoint

- **Buttons go full-width**, spanning the container — "Fill" in Figma, `width: 100%` in
  code.
- When a fold has both a primary and a secondary, they **stack vertically — primary on
  top, secondary below — with a 12px gap.**

## Type token

Button labels use `--gw-text-button-12` / `-14` / `-16` / `-18` from
`foundation/tokens.css`, not the Body ramp.

## Source notes

Rule node `1972:4146`. Three defects worth knowing:

1. **It contradicts itself on Special buttons.** It says `Special/ Glowing` "should be
   used usually in forms or to add emphasis whenever required" and separately that
   "Medium buttons will be used in all folds" — but Special exists only at `Large`,
   `Trailing`, `Active`/`Hover`. Any request for a Medium or Disabled Special button
   cannot be filled.
2. **It never mentions `Text/ black`**, a fully built 36-variant style.
3. **Its CTA instruction ("Book a call") conflicts with the canvas and four other
   rules.** It also uses curly `" "` where every other rule in the file uses straight
   quotes, so string-matching the CTA across rules fails without normalising.

The group's Component Frame label reads `Label: Dropdown` (`1674:37763`) — stale
copy-paste, not meaningful.
