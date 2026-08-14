# Primitives — dot, progress, badge, checkbox, divider

Page `Dashboard Components` (`257:371`) in **`Q9L6q38dEj3Qu1JkjiT13y`** — the product file, not
the library. See `README.md` in this folder for why.

**Scope: dashboard / product.** None of these carries a `Theme` variant — they are fills and
text only, so dark is an override. Each section lists it.

---

## `status-dot`

Set `261:375` · **4 variants**, complete.

| Property | Values |
|---|---|
| `Status` | `on-track` · `pending` · `behind` · `neutral` |

**8 × 8, `radius/20`.** No stroke, no padding.

| Status | Fill |
|---|---|
| `on-track` | `green/400` |
| `pending` | `yellow/400` |
| `behind` | `red/400` |
| `neutral` | `neutral/400` |

**8px is the only correct size.** The screens contain eight dots — six at 8px and two at 12px,
and **both 12px instances are hidden**. Every visible dot is 8px. Ruled 13 Aug 2026.

**Dark:** unchanged. The dark screen renders `green/400` at full strength — the dot is one of the
few things that does *not* step down to `/300`.

⚠ Note the standing surface default: *"No bare coloured status dots — use a Badge."* This
component exists because the section-header legend and the stat-card label genuinely use a bare
dot. It is for **those two places**, not a general status affordance. For status on a row or a
card, still use Badge.

---

## `progress-bar`

Set `261:392` · **8 variants** (2 × 4), complete.

| Property | Values |
|---|---|
| `Size` | `sm` · `md` |
| `Status` | `on-track` · `pending` · `behind` · `neutral` |

| Size | Height | Where |
|---|---|---|
| `sm` | **2** | inside a table cell, under the metric value |
| `md` | **4** | hero card, stat-card |

Track `neutral/200`, `radius/40`, default width 160, `clipsContent`.
Fill child is named **`fill`** — `radius/40`, height fills the track. **Resize `fill` to set the
percentage**; there is no numeric property.

| Status | Fill |
|---|---|
| `on-track` | `green/400` |
| `pending` | `yellow/400` |
| `behind` | `red/400` |
| `neutral` | `neutral/200` |

**Dark override:** track → **`neutral/600`**, fill → the **`/300`** step (`green/300`,
`red/300`). Measured off the dark stat-card, not inferred.

⚠ This is a hairline data bar. It is **not** the library's `section/progress-bar`, which is a
whole 1084 × 116 card with a 32px blue labelled bar. Both are real and they do different jobs —
see `sections.md` for that one.

---

## `badge`

Set `270:424` · **8 variants** (2 × 4), complete.

| Property | Values |
|---|---|
| `Size` | `sm` · `md` |
| `Tone` | `success` · `warning` · `danger` · `neutral` |

| Size | Radius | Padding | Height | Label |
|---|---|---|---|---|
| `sm` | `radius/4` | `py-4 px-8` | **20** | `button-12-med` |
| `md` | `radius/8` | `py-4 px-12` | **24** | `body-12-sem` |

Gap `spacing/4`. Both sizes hug.

**The tint step differs by size** — `sm` uses the `/25` step, `md` uses `/50`:

| Tone | `sm` fill | `md` fill | Text |
|---|---|---|---|
| `success` | `green/25` | `green/50` | `green/500` |
| `warning` | `yellow/25` | `yellow/50` | `yellow/500` |
| `danger` | `red/25` | `red/50` | `red/500` |
| `neutral` | `neutral/50` | `neutral/100` | `neutral/700` |

Why: 28 of the 29 badges in the screens are the `sm` shape on a `/25` tint; the single `md` badge
("Behind", 64 × 24) is on `red/50`. The size-keyed tint reproduces both exactly rather than
averaging them. Ruled 13 Aug 2026.

**This is the dashboard's own pill and it is not the shared `Badge`.** `foundation/shared-components.md`
Badge remains the cross-surface component. Use this one for in-table deltas and row status where
the 20h shape matters; use shared Badge for `Sample data` and anything a web surface also shows.

**Dark:** inherits. Override the tint if the surface demands it.

---

## `checkbox`

Set `263:383` · **4 variants** (2 × 2), complete.

| Property | Values |
|---|---|
| `Theme` | `light` · `dark` |
| `State` | `unchecked` · `checked` |

**24 × 24, `radius/8`, padding `spacing/4`.** Tick is `Check` at **16px, Weight=Bold**, hidden on
`unchecked`.

| Theme | State | Fill | Border | Tick |
|---|---|---|---|---|
| `light` | `unchecked` | none | 1px `neutral/200` | — |
| `light` | `checked` | `neutral/black` | 1px `neutral/200` | `neutral/white` |
| `dark` | `unchecked` | none | 1px **`neutral/600`** | — |
| `dark` | `checked` | **`neutral/white`** | 1px `neutral/600` | **`neutral/black`** |

All four measured from the screens — the dark pair included. The dark checked state is a **full
inversion**, matching the dark active tab and the dark primary button.

⚠ `radius/8` on a 24px box is deliberate and measured. It is not a scaled instance.

---

## `divider`

Set `263:390` · **6 variants** (3 × 2), complete.

| Property | Values |
|---|---|
| `Tone` | `default` · `subtle` · `strong` |
| `Orientation` | `horizontal` · `vertical` |

**Uses a fill, not a stroke** — a 1px stroke on a zero-height node collapses in auto-layout and
Figma centre-aligns strokes while CSS puts borders inside the box. A filled 1px frame survives
both.

| Tone | Fill | Where |
|---|---|---|
| `default` | `neutral/100` | card edges, table header underline |
| `subtle` | `neutral/25` | between table body rows |
| `strong` | `neutral/800` | dark theme, either position |

`horizontal` is 160 × 1, `vertical` is 1 × 160 — both meant to be stretched. In a table row the
vertical divider is set to fill the row height.
