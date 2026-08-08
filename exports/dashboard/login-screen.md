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
| Text block | at **40, 40**, **600 × 355**, **`gap-24`** — ruled, see below | `2321:21407` |
| `welcomeTitle` | **Vert Grotesk Display Medium 60**/1.2 · `--gw-color-neutral-25` · box 600 × 72 | `2321:21404` |
| `welcomeDescription` | `--gw-text-body-20-reg` — Inter Regular 20/1.4, tracking `-0.006em` · `--gw-color-neutral-400` · at y **96** · **always two lines** | `2321:21406` |
| `creatorInfo` | same `--gw-text-body-20-reg` on `--gw-color-neutral-400`, in a **720 × 355 box at 40, 405** with `justify-end` · **fixed attribution string** | `2323:21411` |
| Backdrop | the dashed 40px lattice — **see below** | `2323:21853` |

**The panel is 800 × 800 in an 840-tall screen** — 20px of white above and below, never
full-bleed. The two text blocks tile the panel exactly: `40 + 355 + 10 + 355 + 40 = 800`.

### Title to subtext is 24, not 32 — RULED

Ruled by Utsav, 8 Aug 2026. Figma draws the text block at `gap-32`; **build 24.** That moves
`welcomeDescription` from y 104 to **y 96**. The 600 × 355 block, `creatorInfo` at 405, and the
panel tiling are all unchanged — only the gap and the subtext's y move. A Figma-side fix to
report, not to silently absorb.

### The two text props are not free copy — RULED

The six text props read like open slots, and they are not. Two of them have fixed jobs, and a
build that treats them as a place for a value proposition gets it wrong — which is exactly what
happened the first time this screen was built outside Figma.

**`creatorInfo` is attribution.** It always reads:

```
Created and owned by {creator first name} on {created date}.
```

Both values come off the dashboard record. It is never marketing copy, a tagline, or a feature
line. Ruled by Utsav, 8 Aug 2026.

**`welcomeDescription` says what the dashboard is and how to use it.** Not a greeting — the
title already greets — and not a status report on what happened while the user was away. It
answers "what is this screen for, and what do I do with it" for someone landing on the product
for the first time. Ruled by Utsav, 8 Aug 2026.

> ✓ `Track how your site performs across AI search and Google, and use the page table to find
> what is worth fixing next.`
> ✗ `Your AI marketing team has been researching and publishing while you were away.` — a status
> update, and it tells a new user nothing about the screen.

**It is also always exactly two lines.** `body-20-reg` is 20/1.4, so two lines is **56px**.
Reserve that height and clamp at two, so a short string cannot collapse the panel's rhythm and a
long one cannot push `creatorInfo` out of its measured box:

```css
min-height: 56px;
display: -webkit-box; -webkit-box-orient: vertical;
-webkit-line-clamp: 2; line-clamp: 2; overflow: hidden;
```

**The clamp is a backstop, not a licence — write to two full lines.** At the measured 600px
column the practical ceiling is about **121 characters**, and it is sensitive to punctuation:
121 chars with a comma wraps to two lines, while the same sentence at 122 with an em-dash wraps
to three and silently truncates. Measure the copy; do not eyeball it.

A one-line subtext is a bug, not a short string.

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

**RULED — it is a shared atom.** `DECISIONS.md` → **R1**. The field now lives in
**`foundation/text-field.md`**, fully measured across all 14 variants, and both skills own it.
Read it there; do not re-derive the field from the single stripped instance used here.

Two things that file settles and this screen must follow:

- **The field has no hover state.** `State=Hover` is byte-identical to `State=Default` — measured,
  not missing. `DECISIONS.md` → **R2**.
- **The fill never changes**, in any of the 14 variants. The login instance is
  `State=Default, Feedback=None`, and it matches that symbol exactly.

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

**RULED — build 48 / `--gw-radius-12` / no arrow, in both variants.** `DECISIONS.md` → **R3**.
Radius 12 matches the black button it stacks with; 72 is out of scale with a system whose largest
button is 48; and a trailing arrow on a secondary OAuth button repeats the primary's promise.
`Type=Google`'s 72/16/arrow is a Figma-side fix — **report the drift when you build it.**

The `0.81px` border builds as **1px** — `DECISIONS.md` → **R5**.

### The `OR` divider — `Google + Email` only

460 × 14 at `y 346`, `gap-8`, `justify-center`: a `flex-1` 1px `--gw-color-neutral-200` rule
(**212 wide**), the word **OR** in `--gw-text-button-14-med` — Inter Medium 14, line-height 1 —
on `--gw-color-neutral-400` (**20 wide**), then a second 212 rule. `212 + 8 + 20 + 8 + 212 = 460`. ✓

It sits **32 below the container and 32 above the Google button** — the same gap on both sides.

## Findings

All five are ruled. Build the **Ruled** column; the **Measured** column is what Figma still says,
and each difference is a Figma-side fix to report, not to silently absorb.

| Finding | Measured | Ruled | |
|---|---|---|---|
| The field is a web component on a dashboard screen | `input/text-field` `1562:705` in `↳ web/ component-library` | **shared atom** — `foundation/text-field.md`, both skills own it | **R1** |
| The Google button differs between variants | 72/16/arrow vs 48/12/none | **48 / radius 12 / no arrow**, both | **R3** |
| `dashboardTitle` binds a raw `black` | `#000000` | **`--gw-color-neutral-black`** `#0d0d0d` | **R4** |
| Sub-pixel border | `0.81px` | **1px** | **R5** |
| Field hover | `State=Hover` ≡ `State=Default` | **no hover treatment** | **R2** |

Two that are not defects, just traps — nothing to rule, but don't be caught by them:

| | |
|---|---|
| **Neither Google button is a `Button` instance** | Both are hand-built frames named "Button". The 48-tall one uses 15px vertical padding, which no `Button` size does. **They inherit nothing** — a change to the `Button` set will not reach them. |
| **The logo tile's variable and value disagree** | Bound to `spacing/8` and `radius/8`, rendering 15 and 15, because the instance is scaled 2×. Build the rendered value. |

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
