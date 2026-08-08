# `dashboard-login-screen` — the gate in front of a dashboard

Figma: `↳ dashboard/ component+pattern-library`, set **`2325:1202`**. Measured 7 Aug 2026 off all
three symbols — not extrapolated from one.

**1440 × 840, white.** A split screen: a black 800 × 800 welcome panel on the left, a 460-wide
sign-in column on the right. Every dashboard that needs auth starts here.

## Variants — `Type`, three values

| `Type` | Node | What the user gets |
|---|---|---|
| `Password` | `2325:1199` | one password field + a black **Continue** |
| `Google` | `2325:1200` | a single white **Continue with Google** — no field at all |
| `Google + Email` | `2325:1201` | email field + black **Continue with Email**, an **OR** divider, then **Continue with Google** |

Text is exposed as six props: `dashboardTitle` · `description` · `welcomeTitle` ·
`welcomeDescription` · `creatorInfo` · `type`.

## The left panel — identical in all three

| Part | Measured |
|---|---|
| Panel | **absolute at `left: 20, top: 20`**, **800 × 800** — square, not full-height |
| Fill | `--gw-color-neutral-black` · `--gw-radius-20` · `p-40` · `overflow: hidden` |
| Layout | column, `gap-10`, `justify-content: center` |
| Text block | `flex-1`, **600 wide**, `gap-32` |
| `welcomeTitle` | **Vert Grotesk Display Medium 60**/1.2 · `--gw-color-neutral-25` |
| `welcomeDescription` | `--gw-text-body-20-reg` — Inter Regular 20/1.4 · `--gw-color-neutral-400` |
| `creatorInfo` | Inter Regular, pinned to the bottom via a second `flex-1` with `justify-end` |
| Backdrop | the **dashed 40px square lattice** in `--gw-color-neutral-800` |

**The panel is 800 × 800 in an 840-tall screen** — 20px of white above and below, never
full-bleed. And the lattice here is **dashed `neutral/800`**, not the solid `primary/400` outline
used by `cta-image`. Same idea, different treatment; don't copy one to the other.

## The right column — identical header in all three

**Positioned `left: calc(50% + 410px)`, `top: 50%`, translated −50%/−50%. 460 wide.** It is
centred on a point 410px right of centre, not on the remaining space — a margin change does not
move it.

| Part | Measured |
|---|---|
| Header block | `gap-20`, centre-aligned |
| Logo tile | `--gw-color-neutral-black`, **padding 15, radius 15, around a 30px symbol** |
| Content | `gap-10`, centred |
| `dashboardTitle` | Vert Grotesk **Semibold 32**/1.2 |
| `description` | `--gw-text-body-16-med` · `--gw-color-neutral-600` |

**The logo tile is a 2× scaled instance.** `gushwork-logo-(internal-use)` is a 32px tile with
`--gw-space-8` around a 16px symbol; here it renders at 60px with 15px padding around a 30px
symbol. Figma still reports the bindings as `--spacing/8` and `--radius/8` while emitting 15 —
**the variable and the rendered value disagree because the instance is scaled.** Build it at the
measured 15/15/30, and treat any `spacing/8` reading on a scaled instance with suspicion.

## Per-variant structure

| | `Password` | `Google` | `Google + Email` |
|---|---|---|---|
| Column gap | 0 | **32** | **32** |
| Inner container gap | 40 | 0 — header only | 40 |
| Field | "Enter password" | — | "Enter your email" |
| Primary button | black **Continue** | — | black **Continue with Email** |
| Divider | — | — | **OR** |
| Google button | — | ✓ | ✓ |

### The field — a stripped `input/text-field`

`--gw-color-neutral-50` fill · **56 tall** · `px-16 py-8` · `--gw-radius-8` · `gap-12` ·
`overflow: hidden`. Inner block is `flex-1`, 40 tall, `gap-8`, vertically centred. Placeholder is
Inter Medium 14 on `--gw-color-neutral-500`, and there is an 18px `Processing/None` slot on the
right that renders empty.

### The black button matches `Button` `Size=Large` + icon

`--gw-color-neutral-black` · **`pl-24 pr-20 py-16`** · **`--gw-radius-12`** · full width ·
`gap-8` · label 16 on `--gw-color-neutral-white` · 18px `ArrowRight` ·
`drop-shadow(0 16px 16px rgba(88,92,95,.1))`.

That padding and radius are exactly the measured `Button` `Large` + icon geometry — see
`button.md`. The **drop shadow is the addition**; the `Button` set carries no shadow.

### The Google button — and the two variants disagree

| | `Type=Google` | `Type=Google + Email` |
|---|---|---|
| Height | **72** | **48** |
| Radius | **`--gw-radius-16`** | **12** |
| Trailing `ArrowRight` | **yes** | **no** |

Shared: white fill, **0.81px** `--gw-color-neutral-200` border, `pl-24 pr-20 py-16`, `gap-8`,
18px Google glyph, label 16 on `--gw-color-neutral-black`, same drop shadow.

**Two variants of one component render the same button three ways different.** Nothing says which
is intended. Flagged, not normalised — see *Findings*.

### The `OR` divider — `Google + Email` only

`gap-8`, full width: a `flex-1` 1px rule, the word **OR** in Inter Medium 14 on
`--gw-color-neutral-400`, then a second `flex-1` rule.

## Findings

| Finding | Detail |
|---|---|
| **The Google button is inconsistent across variants** | 72 tall at radius 16 with an arrow in `Google`; 48 tall at radius 12 without one in `Google + Email`. Needs a ruling. |
| **`dashboardTitle` binds a raw `black`** | Every other title in the system uses `--gw-color-neutral-black` `#0d0d0d`. This one is `#000000`, so a palette change misses it — the same defect as `Button Style=White`. |
| **`0.81px` border** | Not a token and not a round number; it is a 1px border on a scaled instance. Build 1px and report it. |
| **The logo tile's variable and value disagree** | Bound to `spacing/8` and `radius/8`, rendering 15 and 15, because the instance is scaled 2×. |

## Rules

**Use this for any dashboard behind a login.** It is the dashboard-side entry point, the way
`dashboard-build` is the page shell — don't hand-build a sign-in screen.

**Pick `Type` by what auth actually exists.** `Google` alone is the shortest path and the right
default when SSO is the only method. Reach for `Google + Email` only when both are genuinely
supported — an OR divider in front of one working option is a dead end.

**The six text props are the only things to change.** Don't restyle the panel, move the column,
or swap the lattice. If a screen needs more than these six strings, it is not this component.

**Never put a blue fill on either button.** Same rule as the rest of the dashboard — black
carries interaction, blue carries data and status. See `controls.md`.
