# `dashboard-login-screen` — the gate in front of a dashboard

Figma: `↳ dashboard/ component+pattern-library`, set **`2325:1202`**. Measured 7 Aug 2026 off all
three symbols — not extrapolated from one.

**Re-measured 8 Aug 2026 from node coordinates on all three variants.** The symbol read had got
the CSS of each part right and the *arithmetic between* the parts wrong. What changed:

| | Was | Now |
|---|---|---|
| Lattice opacity | not recorded | **`opacity: 0.3`** on the `BG` frame |
| Lattice fills | not recorded | **three cells** filled `neutral/900` |
| Black button height | implied 48, as `Button Large` | **50** — `py-16` around an 18px icon |
| Black button shadow | raw `drop-shadow(0 16px 16px …)` | **`--gw-shadow-s3`**, a real token |
| Field → button gap | not recorded | **16** |
| Right column | `calc(50% + 410px)` + translate | **`x = 900`**, per-variant `y` |
| The field's home | assumed dashboard | **`↳ web/ component-library`** |
| Google buttons | assumed `Button` instances | **plain frames**, inheriting nothing |

None of it was visible from a single symbol read, and the first four were invisible from a
*per-element* read too — they live on parents, or in the gaps between children. **Read the frame,
then read its children, then check the two agree.**

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

| Part | Measured | Node |
|---|---|---|
| Panel | **absolute at `left: 20, top: 20`**, **800 × 800** — square, not full-height | `2321:20494` |
| Fill | `--gw-color-neutral-black` · `--gw-radius-20` · `overflow: hidden` | |
| Text block | at **40, 40**, **600 × 355**, `gap-32` | `2321:21407` |
| `welcomeTitle` | **Vert Grotesk Display Medium 60**/1.2 · `--gw-color-neutral-25` · box 600 × 72 | `2321:21404` |
| `welcomeDescription` | `--gw-text-body-20-reg` — Inter Regular 20/1.4, tracking `-0.006em` · `--gw-color-neutral-400` · at y **104** | `2321:21406` |
| `creatorInfo` | same `--gw-text-body-20-reg` on `--gw-color-neutral-400`, in a **720 × 355 box at 40, 405** with `justify-end` | `2323:21411` |
| Backdrop | the dashed 40px lattice — **see below** | `2323:21853` |

**The panel is 800 × 800 in an 840-tall screen** — 20px of white above and below, never
full-bleed. The two text blocks tile the panel exactly: `40 + 355 + 10 + 355 + 40 = 800`.

### The lattice — ✗→✓ two corrections

**`BG` `2323:21853` carries `opacity: 0.3`.** The opacity sits on the parent frame, so a read of
any individual cell reports a full-strength `1px dashed neutral/800` and misses it entirely. This
is the same class of trap as the scaled logo tile below: **a per-child read cannot see what the
parent applies.** When something renders heavier than the Figma canvas, check the group.

**Build it as one border per grid line, not 400 bordered boxes.** The frame is a 20 × 20 tiling of
40px cells, each with a 1px dashed border on all four sides. Figma centre-aligns strokes, so two
adjacent cells overlap into one line; CSS puts borders *inside* the box, so the same markup
renders every shared edge at **2px** — double weight everywhere except the outer rim. Give each
cell `border-right` and `border-bottom` only and put `border-top`/`border-left` on the container.

**Three cells carry a `--gw-color-neutral-900` fill.** Row-major, 0-indexed from the top-left:

| Cell | Column | Row | Node |
|---|---|---|---|
| 155 | 15 | 7 | `2323:22009` |
| 174 | 14 | 8 | `2323:22028` |
| 306 | 6 | 15 | `2323:22160` |

155 and 174 touch corner-to-corner on the descending diagonal; 306 sits alone, low and left. The
placement is deliberate and asymmetric — **do not scatter them randomly or re-roll the positions**,
and do not read them as a pattern that continues. Three cells, these three, in every variant.

The lattice here is **dashed `neutral/800` at 30%**, not the solid `primary/400` outline used by
`cta-image`. Same idea, different treatment; don't copy one to the other. Note that `cta-image`
also fills exactly three squares out of its own lattice — the motif is shared even though the
stroke treatment is not.

## The right column — identical header in all three

**Absolutely positioned at `x = 900`, 460 wide.** 900 = 720 + 180, so its centre lands at
**1130 = centre + 410** — it is centred on a point 410px right of screen centre, not on the
remaining space. A margin change does not move it. Its `y` and height differ per variant:

| Variant | `y` | Height | Node |
|---|---|---|---|
| `Password` | 263 | 314 | `2321:20462` |
| `Google` | **292** | **256** | `2323:22256` |
| `Google + Email` | **200** | **440** | `2323:22736` |

Each is vertically centred: `263 + 314/2 = 292 + 256/2 = 200 + 440/2 = 420 = 840/2`. ✓ **Centre the
column and let its height fall out of the content** — do not hard-code any of these `y` values.

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

Every variant opens with the same **header block, 460 × 152**: a 60px logo tile, `gap-20`, then a
`content` block at `y 80` holding `dashboardTitle` (460 × 38) and `description` at `y 48`
(`gap-10`). Identical in all three, down to the pixel.

| | `Password` | `Google` | `Google + Email` |
|---|---|---|---|
| Column height | 314 | 256 | **440** |
| Column gap | — one child | **32** | **32** |
| `container` | 460 × 314, `gap-40` | 460 × 152 — header only | 460 × 314, `gap-40` |
| Field group | 460 × 122, **`gap-16`** | — | 460 × 122, **`gap-16`** |
| Field | "Enter password" | — | "Enter your email" |
| Primary button | black **Continue**, 50 tall | — | black **Continue with Email**, 50 tall |
| Divider | — | — | **OR** at `y 346` |
| Google button | — | 72 tall at `y 184` | 48 tall at `y 392` |

The field group is `56 + 16 + 50 = 122`. ✓ The `Password` and `Google + Email` containers are
byte-identical apart from the placeholder and the label — `Google + Email` simply appends a
divider and a second button below the same 314-tall block.

### The field — a **web** component borrowed by a dashboard screen

`--gw-color-neutral-50` fill · **56 tall** · `px-16 py-8` · `--gw-radius-8` · `gap-12` ·
`overflow: hidden`. Inner block is `flex-1`, 40 tall, `gap-8`, vertically centred. Placeholder is
Inter Medium 14 on `--gw-color-neutral-500`, and there is an 18px `Processing/None` slot on the
right that renders empty. The field sits **16 above** the button, not 20 or 24.

**`input/text-field` is `1562:705` — it lives in `↳ web/ component-library`, in the
`input-fields` group, with 14 variants.** It is not a dashboard component. The dashboard library
has no text field of its own, so this login screen — a dashboard pattern — instantiates a web one.
**This is the only cross-surface dependency in the dashboard set.**

That matters because the two skills are surface-scoped: a dashboard build otherwise never reads
`exports/web/`. When you build this screen, the field's full variant matrix, its states, and its
usage rules are all in `exports/web/component-library.md` — go there, don't re-derive them from
the single stripped instance used here.

**It also needs a ruling.** Either the field is promoted to a shared atom in `foundation/`,
alongside the other things both surfaces use, or the dashboard grows its own and this screen
switches to it. Leaving it as a silent reach across the boundary means a change made for a
marketing form quietly changes the login screen. Flagged, not resolved — see *Findings*.

### The black button — `Button` `Size=Large` + icon, but **50 tall**

`--gw-color-neutral-black` · **`pl-24 pr-20 py-16`** · **`--gw-radius-12`** · full width ·
`gap-8` · label `--gw-text-button-16-med` (Inter Medium 16, **line-height 1**) on
`--gw-color-neutral-white` · 18px `ArrowRight` · **`--gw-shadow-s3`**.

Two ✗→✓ corrections from the coordinate pass:

- **It renders 50 tall, not 48.** `Button` `Large` is 48; here `py-16` wraps an **18px icon**, so
  `16 + 18 + 16 = 50`. The extra 2px comes from the icon being taller than the 16px label.
  Padding and radius still match `Large` + icon exactly — the height does not.
- **The shadow is `--gw-shadow-s3`, a real token** (`0 16px 32px -12px #585c5f1a`). Figma's
  Tailwind output reports `drop-shadow-[0px_16px_16px_rgba(88,92,95,0.1)]` because Tailwind's
  `drop-shadow` cannot express spread, so it flattens `radius 32, spread -12` into `16px`. The
  style annotation names `Shadows/S3` outright. **When the class and the style annotation
  disagree, the annotation is the token — use it.**

The `Button` set itself carries no shadow; adding S3 is this screen's own decision.

The measured `ArrowRight` glyph is **14.065 × 11.816 centred in an 18px slot** — not an 18px
glyph. Harvested to `assets/icons/arrow-right.svg`.

### The Google button — and the two variants disagree

| | `Type=Google` | `Type=Google + Email` |
|---|---|---|
| Height | **72** | **48** |
| Radius | **`--gw-radius-16`** | **12** |
| Trailing `ArrowRight` | **yes** | **no** |

Shared: white fill, **0.81px** `--gw-color-neutral-200` border, `gap-8`, 18px Google glyph, label
16 on `--gw-color-neutral-black`, same `--gw-shadow-s3`.

**Neither is a `Button` instance** — both are plain frames named "Button", so their padding is
whatever centres the content: the 72 sits its 18px glyph at `y 27` (27/27), the 48 at `y 15`
(15/15). **15 is not a `Button` vertical padding at any size.** Nothing about these buttons
inherits from the `Button` set.

The **Google mark is a real asset**, `Platform=Google, Color=Original` — a four-path SVG at
17.64 × 18. Harvested to `assets/brand/google-g.svg`. Do not substitute a letter "G" in a
coloured circle; it is a third-party brand mark with a fixed form.

**Two variants of one component render the same button two ways different.** Nothing says which
is intended. Flagged, not normalised — see *Findings*.

### The `OR` divider — `Google + Email` only

460 × 14 at `y 346`, `gap-8`, `justify-center`: a `flex-1` 1px `--gw-color-neutral-200` rule
(**212 wide**), the word **OR** in `--gw-text-button-14-med` — Inter Medium 14, line-height 1 —
on `--gw-color-neutral-400` (**20 wide**), then a second 212 rule. `212 + 8 + 20 + 8 + 212 = 460`. ✓

It sits **32 below the container and 32 above the Google button** — the same gap on both sides.

## Findings

| Finding | Detail |
|---|---|
| **The field is a web component used on a dashboard screen** | `input/text-field` `1562:705` belongs to `↳ web/ component-library`. The dashboard has no field of its own. Promote it to a shared atom, or give the dashboard one — but don't leave the boundary crossed silently. |
| **The Google button is inconsistent across variants** | 72 tall at radius 16 with an arrow in `Google`; 48 tall at radius 12 without one in `Google + Email`. Needs a ruling. |
| **Neither Google button is a `Button` instance** | Both are hand-built frames named "Button". The 48-tall one uses 15px vertical padding, which no `Button` size does. They inherit nothing — a change to the `Button` set will not reach them. |
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
