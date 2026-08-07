# Folds — the full-width page sections

Figma: frame `fold` (`1948:8108`) on `↳ web/ pattern-library`.

The full-width sections a marketing page is built from. Each is a responsive section that
composes atoms (heading, buttons, cards, eyebrows) into a repeatable block. **Folds are
the middle layer: atoms build folds; Page Build stacks folds into a page.**

There is **one** Info Frame for all 12 folds — no fold has its own description or rules.
Everything below comes from the shared rules (`2089:23406`), the shared structure blob
(`2089:23403`), and the component sets themselves.

## Composition hierarchy — don't rebuild across levels

- Atoms (`Button`, `Card / Information`, `eyebrow`, `Agent Card`…) build a fold.
- Folds stack into a full page via **Page Build**.
- **A fold reuses atoms by instance.** A Cards Grid fold is a heading + `Card / Information`
  cards + `Button`. **Don't hand-build a card inside a fold.**

## Pick the fold by content and intent

| Fold | Use for | Node | Variants |
|---|---|---|---|
| `fold/ Hero` | The opening fold | `1731:55983` | 10 |
| `fold/ Testimonial` | Client proof | `1790:6285` | 4 |
| `fold/ Cards Grid` | Feature / benefit grid, up to 6 cards | `1790:7329` | 24 |
| `fold/ Cards Grid (small)` | A single row of cards | `2085:21418` | 2 |
| `fold/ FAQs` | Accordion list | `1790:7851` | 2 |
| `fold/ With image` | Split layout — text one side, image the other | `1793:6561` | 2 |
| `fold/Timeline` | Week-based steps | `1809:21318` | 2 |
| `fold/Comparison Table` | 4-column comparison — feature + 3 competitors | `1824:6836` | 2 |
| `fold/ Video` | Video player fold | `2085:17304` | 2 |
| `fold/AI Agents` | Marquee grid of Agent Cards | `2085:18017` | 2 |
| `fold/ CTA` | Wraps the footer CTA component | `2085:20750` | 2 |
| `fold/ other` | Generic fold for custom content | `1790:6807` | 2 |

**Note the prefix inconsistency.** Nine folds use `fold/ ` with a space after the slash;
three do not — `fold/AI Agents`, `fold/Timeline`, `fold/Comparison Table`. These are
literal names.

`fold/ other` is undocumented everywhere else in the file and doesn't surface in component
search. It exists and it works.

## Shared toggles — most folds inherit these

| Property | Type | Default |
|---|---|---|
| `Breakpoint` | VARIANT | `Desktop` — `Desktop` / `Phone` (or `Mobile`) |
| `container` | SLOT | — swappable content container |
| `Expand` | BOOLEAN | `true` |
| `Show CTA` | BOOLEAN | `true` |
| `Show Card 3` – `Show Card 6` | BOOLEAN | `true` |

**Use `Show Card 3`–`6` to add or drop cards rather than deleting instances manually.**

> **Measured correction.** The `Show Card` toggles live on **`fold/ Cards Grid (small)`** only,
> and they are **`Show Card 4` and `Show Card 5`** — two, both default `false`, so it renders
> three cards and tops out at five. `fold/ Cards Grid` has none; its axes are `Card Style`,
> `Card Image` and `Card Layout`. See *Measured appearance* below before relying on this table.

**"Most folds" is doing real work in that sentence — 4 of 12 inherit nothing.**
`fold/AI Agents`, `fold/ CTA`, `fold/Timeline`, and `fold/Comparison Table` have only
`Breakpoint`.

## Per-fold detail

### `fold/ Hero` — `1731:55983` · 10 variants

| Property | Values |
|---|---|
| `Breakpoint` | `Desktop`, `Phone` |
| `Layout` | `Home`, `Centered`, `+ Create New`, `Split`, `Form` |

Slot: `image` (`1735:26`).

**Does not use the shared `fold/fold-element/heading`** — it has its own heading structure.

`+ Create New` is Figma's UI affordance leaked into the data as a real variant value — it
is the custom-layout slot, not a preset. The rule lists the layouts as
`Home, Centered, Split, Form, + Create New`; the page-build rule refers to them by
different names in an unresolved bracket (see `page-shell.md`).

`Layout=Form` embeds `fold/fold-element/form`. `Layout=Home` includes the client-logo strip.

### `fold/ Testimonial` — `1790:6285` · 4 variants

| Property | Values |
|---|---|
| `Breakpoint` | `Desktop`, `Phone` |
| `Style` | `Video`, `Single` |

**Pick `Style` by the proof format:** `Video` for a video testimonial, `Single` for a quote
with the client's photo and signature.

Carries **both** an `Expand` and an `Extend` boolean (`1748:0` and `1801:0`) — every other
fold has only `Expand`. Their difference is undocumented.

The structure blob claims `Breakpoint` has `(+ Breakpoint3, Breakpoint4)`. **Those do not
exist.**

### `fold/ Cards Grid` — `1790:7329` · 24 variants

| Property | Values |
|---|---|
| `Breakpoint` | `Desktop`, `Phone` |
| `Card Style` | `3`, `1`, `2`, `4` — note the option order; `3` is listed first |
| `Card Image` | `With`, `Without` |
| `Card Layout` | `Grid`, `Single`, `Stacked` |

The largest fold set. Up to 6 cards via `Show Card 3`–`6`. Cards come from
`Card / Information` — see `cards.md`.

### `fold/ Cards Grid (small)` — `2085:21418` · 2 variants

`Breakpoint` only. A single row, 3–5 cards, no style/image/layout choice.

**The documented default is wrong.** Both the rule and the structure blob say 3 cards show
by default. The actual defaults are `Show Card 3`=**true**, `Show Card 4`=false,
`Show Card 5`=false, `Show Card 6`=**true** — so **4 cards render.** Set the toggles
explicitly rather than trusting the default.

### `fold/ FAQs` — `1790:7851` · 2 variants

`Breakpoint` only, plus booleans `Question 6` through `Question 10` (all default `false`).

**5 questions by default, up to 10** via the toggles. Uses
`fold/fold-element/accordion`.

### `fold/ With image` — `1793:6561` · 2 variants

`Breakpoint`, plus slots `container` (`1735:21`) and `Slot` (`1793:0`) for the image/media
area, plus the shared `Expand` / `Show CTA` / `Show Card 3`–`6` booleans.

Split layout: text one side, image the other. Observed at 1240 wide with a 580/580 split
and a 660 offset. Its in-fold `Button` is hidden by default in the worked page examples —
the CTA is opt-in via `Show CTA`.

### `fold/Timeline` — `1809:21318` · 2 variants

`Breakpoint` [`Desktop`, `Phone`] only.

**Dark theme.** Horizontal on desktop, vertical on phone. Uses
`fold/fold-element/timeline-tab` and `fold/fold-element/progress-bar`.

The structure blob says this fold has `Property 1: Default (⚠️ has errors — both variants
share same name)`. **That note is stale** — the set has a proper `Breakpoint` property with
two correctly-named variants and no errors.

### `fold/Comparison Table` — `1824:6836` · 2 variants

`Breakpoint` only. A **4-column comparison** — feature name + 3 competitors.

Desktop uses `fold/fold-element/table-header` + `table-row`. **Phone replaces the table
entirely** with `table-phone-card` + `table-toggle`.

**Distinct from the dashboard's `section/table`** — this is a fixed marketing
feature-comparison, not a live data grid.

### `fold/ Video` — `2085:17304` · 2 variants

`Breakpoint`, plus slot `container` and the shared booleans. A video player fold with a
`Play` control.

### `fold/AI Agents` — `2085:18017` · 2 variants

| Property | Values |
|---|---|
| `Breakpoint` | **`Phone`, `Desktop`** — the only fold whose options are ordered Phone-first |

A marquee grid of `Agent Card`s — 4 rows × 9.

**The structure blob claims this fold "Uses `Mobile` not `Phone`".** It is wrong and
inverted: the actual values are `Phone` and `Desktop`. `Mobile` appears on Cards, under the
`Device` property — not here.

### `fold/ CTA` — `2085:20750` · 2 variants

`Breakpoint` only. **Wraps `footer/footer-elements/cta`** — the same CTA component used in
the footer.

**It carries its own Blue/Black and CTA-copy rules — don't restyle it.** See
`page-shell.md` for the footer CTA's colour behaviour and copy.

### `fold/ other` — `1790:6807` · 2 variants

`Breakpoint`, plus slot `container` and the shared booleans. **Use when nothing above
fits.** The web equivalent of the dashboard's `section/Container`.

## Cross-references — reuse, don't redefine

| Fold | Instances | Rules in |
|---|---|---|
| `fold/ CTA` | `footer/footer-elements/cta` | `page-shell.md` |
| `fold/AI Agents` | `Agent Card` / `agent-icon` | `fold-elements.md`, `atoms.md` |
| `fold/ Testimonial`, `fold/ Cards Grid` | `Card / Information` | `cards.md` |
| All headings | `eyebrow` via `fold/fold-element/heading` | `atoms.md`, `fold-elements.md` |
| Buttons | `Button` | `button.md` |

## CTA copy

Any fold CTA is **`Book a Demo`** — a fixed string, capitalised.

The fold rule says `Book a demo`, and **the canvas disagrees with even that for six
folds**: the inline CTA buttons in `fold/ With image`, `fold/ Video`, `fold/ Testimonial`,
`fold/ Cards Grid` (32 nodes), `fold/ Cards Grid (small)`, and `fold/ other` all render
**"Book a call"** — 42 nodes in total. `fold/ Hero` and `fold/ CTA` render "Book a demo".

**Write `Book a Demo` regardless of what the fold ships.** See `foundation/voice.md` for
the full ruling.

## Breakpoints

**Every fold ships Desktop + Phone.** On phone: multi-column grids collapse to one column,
side-by-side internals stack, buttons go full-width, and a primary + secondary pair stacks
vertically with a 12px gap.

The `Breakpoint` default is stated as `Desktop` in the fold shared-properties table but as
`Phone` in the footer structure blob. Set it explicitly.

## Ladder violation to know about

The fold rule says atoms build fold-elements build folds. **`Card / Testimonial` — an
atom — instances `fold/fold-element/progress-bar`,** which inverts the ladder. That is how
the file is built. Don't replicate the pattern in new work.

## Never

- Hand-build a card, button, eyebrow, or heading inside a fold. Instance them.
- Delete card instances to reduce a grid — use `Show Card 3`–`6`.
- Restyle `fold/ CTA` — it inherits the footer CTA's rules.
- Ship a fold without its Phone variant considered.

---

# Measured appearance

Everything above this line was transcribed from the page's annotations. Everything below was
**measured off the rendered components** on 7 Aug 2026, and where the two disagree the measured
figure wins.

**Figma is right. Build what it says.** Where a measured value looks like a slip — an odd width,
two gaps that should match — it is recorded as measured and **reported**, never quietly corrected
here. An export that tidies a value is worse than an odd number: the build then disagrees with
the file everyone designs in, and nobody can tell which one is authoritative. Deviations are the
build's decision to declare in a notice, not this file's to pre-empt.

**All 12 folds are measured** — frame geometry, variant matrices, and internals. What remains
unmeasured is only the **Phone** side of each fold and Hero's other four layouts, both of which
have geometry recorded below.

## Fold width is 1240 — except three

Measured on every fold. The container is **1240 desktop / 343 phone**, and the exceptions are
deliberate or defects:

| Fold | Desktop | Phone | |
|---|---|---|---|
| Most folds | 1240 | 343 | the norm |
| `fold/ Hero` | **1440** | **375** | full-bleed — the symbol includes the page margin |
| `fold/AI Agents` | **1440** | **375** | full-bleed — the marquee runs edge to edge |
| `fold/Comparison Table` | **1242** | **337** | 1240 of rows **+ its 1px border each side** |

**Comparison Table's 1242 is not an anomaly** — measuring its internals explains it. The rows are
1240 wide and the Table Body wraps them in a 1px `neutral/100` border, so the frame is
1240 + 1 + 1 = 1242. Build the rows at 1240 and let the border add the rest. The 337 on phone is
6 short of 343 and does **not** have the same explanation; use it as measured.

## Measured frame heights

Heights are content-driven, so treat these as the drawn state rather than a constraint.

| Fold | Desktop | Phone |
|---|---|---|
| `fold/ Hero` | 540–1234 by layout | 460–1003 |
| `fold/ Testimonial` `Style=Video` | 1067 | 1975 |
| `fold/ Testimonial` `Style=Single` | 347 | 430 |
| `fold/ Cards Grid` | 639–841 without image · **1549 with** | 632–1067 |
| `fold/ Cards Grid (small)` | 597 | 1171 |
| `fold/ FAQs` | — | — |
| `fold/ Video` | 850 | 548 |
| `fold/Timeline` | 656 | 649 |
| `fold/Comparison Table` | 511 | 1071 |
| `fold/AI Agents` | 696 | 660 |
| `fold/ other` | 712 | 788 |

**`Card Image=With` roughly doubles a Cards Grid** — 1549 against 639–841. Worth knowing before
you put one above the fold.

## The container is 1240 desktop / 343 phone

Confirmed identically on `With image` and `FAQs`: `max-w-[1240px] w-[1240px]` desktop,
`max-w-[343px] w-[343px]` phone. That is the fold's own width, inside `page-build`'s margins.

## Headings are `neutral/black` `#0d0d0d` — not `neutral-900`

Every fold heading measured binds `colors/neutral/black` (`#0d0d0d`), and body copy binds
`colors/neutral/600` (`#6a7077`). `neutral-900` (`#262a2e`) is the **dashboard** text colour.
Using it on a marketing page is a surface mix-up, and it is subtle enough to pass review.

## `fold/ With image` — `1793:6561`

Props: `breakpoint` · `showCta` (default `true`) · `slot`.

| | Desktop | Phone |
|---|---|---|
| Fold width | 1240 | 343 |
| Column gap | `spacing/80` — 80 | `spacing/40` — 40, stacked |
| Text block padding | `py-80` | — |
| Heading | h3 · Vert Grotesk Bold 44/1.2 | h4 · 38/1.2 |
| Body | `body-18-med` 18/1.6, max-w 680 | `body-16-med` 16/24 |
| Heading→body gap | 20 | 20 |
| Image slot | fills, `radius/20`, `neutral/50` on `neutral/100` border | 400 tall, `radius/16` |
| Button | 44 tall, `px-20 py-16`, radius 8, gap 8, 18px trailing icon | same, full-width |

**The slot has a real placeholder** — `neutral/50` fill, 1px `neutral/100` border, `radius/20`.
That is the empty state, not a missing image.

**On phone the image comes first**, above the text. Desktop is text-left / image-right.

## `fold/ FAQs` — `1790:7851`

Props: `breakpoint` · `question6`–`question10`, all **boolean, default `false`**. Five
accordions are hard-built; 6–10 are the toggles. The "5 by default, up to 10" rule is correct.

| | Desktop | Phone |
|---|---|---|
| Layout | two columns, gap `spacing/100` — 100 | stacked, gap 40 |
| Heading column | 480 wide (max-w 800) | full width |
| Accordion column | 660 wide | full width |
| Accordion gap | `spacing/8` — 8 | 8 |
| Accordion | `p-12`, radius 12, `overflow-clip` | same |
| Question | `body-18-sem` 18/1.6 · `neutral/800` | same |
| Answer | `body-16-med` 16/24 · `neutral/600` | same |
| Caret | 32 box, `neutral/50`, `radius/8`, 16px `CaretDown` | same |

**Collapsed answers are `opacity-0` at `size-px`, absolutely positioned** — present in the DOM,
not removed. Match that if you want the measured markup.

The subhead carries an inline link — *"Talk to us"*, underlined, `decoration-dotted`, at a **raw
`#0070ff`** rather than the `primary/500-main` token. Cosmetically identical, but it is a
hardcoded hex in the source.

## `fold/ CTA` — `2085:20750` · Desktop measured

Props: `breakpoint` only.

**It is a full-width blue panel, not a centred block.** An earlier revision of this file
described it from aggregate token counts rather than its structure and got it wrong — the 600 is
the image block, and the `radius/40` 56×40 shapes are avatars nested *inside* `cta-image`, not
part of the fold's own layout.

| Part | Measured |
|---|---|
| Root | 1240, `radius/20`, `gap-60`, **`drop-shadow(0 16px 16px rgba(88,92,95,.1))`** |
| Panel | full width, **440 tall**, `primary/500-main` fill, `radius/16`, `overflow-clip` |
| Inner row | `justify-between`, full height, max-w **1400** |
| Left column | `flex-1`, **`pl-60`**, `gap-40` |
| Heading | `h3` 44/1.2 Vert Grotesk Bold, **white** — *"Let Gushwork run your marketing team in the background."* |
| Body | 16/24 Inter Medium on **`neutral/alpha/80-white`** |
| Primary button | **white fill**, `radius/10`, **`pl-16 pr-12 py-12`**, 14/20 on `secondary/500-main`, 16px icon — *"Book a demo"* |
| Secondary button | 1px **`neutral/alpha/30-white`** border, no fill, `px-16 py-12`, `radius/10`, white 14/20 — *"Calculate ROI with Gushwork"* |
| Right | `footer/footer-elements/cta-image`, **600 × 440**, `overflow-clip` |

**`cta-image` is not a bitmap.** At `image=Testimonial, color=Blue, breakpoint=Desktop` it is a
drawn pattern: **141 outlined 40 × 40 squares** in `primary/400` (`#338cff`) on a
`primary/500-main` ground, laid on a 40px grid — x from 40 to 560, y from 0 to 400, so a
**14 × 11 lattice of 154 slots with 13 deliberately left empty**. There is no image asset to
export, and nothing to go missing; it renders from geometry alone. Its own props are
`breakpoint` · `color` · `image`, 24 variants in total.

**This is the one fold whose buttons use `radius/10` and 14px labels** — everything else uses
radius 8 with 16px. It also confirms the CTA copy split: this fold ships **"Book a demo"**.

**Binds `colors/secondary/500-main` (`#111827`)** for the primary button's label — see the token
findings below.

Because the right-hand 600 is `cta-image`, the fold cannot be restyled independently; changing
it means changing the footer element.

## `fold/ Cards Grid` — `1790:7329` · the annotations are wrong about this one

**Real props: `breakpoint` · `cardStyle` · `cardImage` · `cardLayout` · `showCta`.**

Three axes the rules never mention, and they are what the 24 variants actually are:

| Property | Values | Rule |
|---|---|---|
| `Card Style` | `1` `2` `3` `4` | which `Card / Information` style fills the grid |
| `Card Image` | `With` `Without` | `With` roughly doubles the fold's height |
| `Card Layout` | `Grid` `Single` `Stacked` | **`Grid` is Desktop-only; `Single` and `Stacked` are Phone-only** |

That last row is the one to internalise: 8 Desktop variants are all `Grid`, and the 16 Phone
variants split into `Single` and `Stacked`. Asking for `Card Layout=Grid` on Phone resolves to
nothing.

**There are no `Show Card` properties on this fold.** It hard-builds **six** cards in two rows of
three, and `showCta` is its only content toggle. The shared-toggles rule about `Show Card 3`–`6`
describes **`fold/ Cards Grid (small)`**, which carries `Show Card 4` and `Show Card 5` — two
booleans, not four. See below.

### Measured — `Breakpoint=Desktop, Card Style=1, Card Image=Without, Card Layout=Grid`

| Part | Measured |
|---|---|
| Root | 1240 wide, 785 tall, `gap-60`, centre-aligned column |
| Heading block | **620** wide, `gap-20`, centred |
| eyebrow | `neutral/white` fill, **0.5px** `neutral/100` border, 24 tall, radius **100**, `gap-4`, 14px icon, `button-12-med` on `neutral/900` |
| Heading | h3 · 44/1.2 Vert Grotesk Bold · `neutral/black` · centred |
| Body | `body-18-med` 18/1.6 · max-w **580** · `neutral/600` · centred |
| Card | `flex-1` from an intrinsic **336**, `neutral/25` on 1px `neutral/100`, radius 16 |
| Card inner | `p-16`, `gap-12`; 24px icon; title `body-18-sem` on `neutral/black`; subtext `body-16-reg` on `neutral/800` |
| CTA | blue `primary/500-main`, 44 tall, `px-20 py-16`, radius 8 |

**The two card rows use different gaps — row 1 is `gap-8`, row 2 is `gap-10`.** Build both as
measured. Because cards are `flex-1`, row 1's cards come out 2px wider than row 2's; that is what
the component does. Flagged as a possible slip for review, but not corrected here — a "tidied"
export that silently disagrees with Figma is worse than an odd number, because the next person
cannot tell which is authoritative.

`Card / Information` carries its own `subtext` boolean, so a card can drop its body copy without
a different style.

## `fold/ Cards Grid (small)` — `2085:21418` · Desktop measured

Props: `breakpoint` · `showCard4` · `showCard5` · `showCta`.

**This is the fold the `Show Card` rule belongs to** — and it is `Show Card 4` and `Show Card 5`,
both defaulting to **`false`**. So the fold renders **three cards by default, five at most.** The
shared-toggles table's "3–6" is wrong on both the range and the fold.

| Part | Measured |
|---|---|
| Root | 1240, `gap-60`, centred |
| Heading | the shared `fold/fold-element/heading` at its full **800** width |
| Card row | single row, `gap-8` |
| Card | `Card / Information` `Style=4` — `neutral/25` on `neutral/100`, `radius/16`, `gap-12` |
| Card inner | `p-16`, `gap-24` |
| Icon container | **40 box, `neutral/black` fill, `radius/8`, `p-8`, 20px glyph** |
| Title | `body-18-sem` · `neutral/black` |
| Subtext | `body-16-reg` · `neutral/600` |
| CTA | blue `primary/500-main`, 44 tall, radius 8 |

**`Style=4` puts the icon in a filled black 40px tile**, where `Style=1` (used by the big Cards
Grid) sets a bare 24px glyph on the card background. That is the visible difference between the
two card styles.

Note the subtext colour differs between the two folds — `neutral/600` here, `neutral/800` on
`Cards Grid` `Style=1`. Both as measured.

## `fold/fold-element/heading` — `1732:3742` · the shared heading

Props: `breakpoint` · `length` · `showBadge` · `showSubtext`.

Intrinsically **800 wide**, `gap-20`, centred: eyebrow → `h3` 44 on `neutral/black` → `body-18-med`
at max-w **680** on `neutral/600`.

**`fold/ Cards Grid` overrides it to 620 wide**; `Cards Grid (small)` and `Video` use the full
800. Both toggles are real — `Video` switches badge and subtext **off** and ships heading-only.

## `fold/ Video` — `2085:17304` · Desktop measured

Props: `breakpoint` · `showCta`.

| Part | Measured |
|---|---|
| Root | 1240, `gap-60`, centred |
| Heading | shared heading with `showBadge=false`, `showSubtext=false` — the h3 alone |
| Video well | full width, **`aspect-[1240/580]`**, `neutral/400` fill, `neutral/100` border, `radius/20` |
| Play button | centred, 56 tall, `pl-24 pr-20 py-16`, radius 12 |
| — its fill | `neutral/alpha/10-black` with **`backdrop-blur-[2px]`** |
| — its border | **2px** `neutral/alpha/10-white` |
| — its label | `button-18-med` · `neutral/white` · 18px `Play` glyph, `gap-8` |
| CTA | blue `primary/500-main`, 44 tall, radius 8 |

**The play button is glassmorphic** — a translucent black fill over a 2px translucent white
border with a 2px backdrop blur. Nothing in the annotations says so, and it does not survive
being rebuilt as a plain button. The asymmetric padding (24 left, 20 right) optically centres the
label against the leading icon.

Props: `breakpoint` · `style` (`Video` / `Single`). No CTA, no slot.

| Part | Measured |
|---|---|
| Root | 1240, centred, `py-40`, `gap-60` |
| Quote | **Vert Grotesk Display Semibold 44**/1.2 · `neutral/900` · centred · **fixed 1011 wide** |
| Attribution row | `gap-12`, centred |
| Avatar | `client/avatar` `size=large` — 64 × 48, **radius 100** |
| Name | `body-14-sem` 14/21 · `neutral/900` |
| Role | `body-12-med` 12/16 · `neutral/500` |

**Build all three as measured.** Two are worth *reporting* because they point at gaps in the
token set, not because the fold is wrong:

1. **The quote is Vert Grotesk Semibold 44, and no token covers it.** `h3` is 44 **Bold**; the
   display ramp has no 44 Semibold. Set it explicitly and report the missing ramp step — the
   fold is not wrong, the ramp is short.
2. **It colours the quote `neutral/900`, where other fold headings use `neutral/black`.** Both
   are real tokens. Use `neutral/900` here because that is what this component binds.
3. **The quote box is a fixed 1011 wide** inside the 1240 container. Not a round number, but it
   is the measured value — use it.

The avatar measurements confirm `avatar.md` exactly — 64 × 48, radius 100, a 72 × 48 photo inside
a 64-wide clip. That file was already right.

## `fold/Timeline` — `1809:21318` · Desktop measured

**Not a dark full-bleed fold — a dark rounded card.** `neutral/black` fill, **radius 20**,
`p-60`, `gap-60`, 1240 wide.

| Part | Measured |
|---|---|
| Heading | `h5-bold` — Vert Grotesk Bold **32**/1.2 · `neutral/white` · 740 wide |
| Subhead | `body-16-med` · `neutral/400` |
| Corner icon | `Lightning`, 40 |
| Columns | 5, each 380 tall, `flex-1`, **dashed left+right border** in `neutral/700` |
| `timeline-tab` | **222** wide, `p-12`, `radius/12`, `neutral/100` fill, `body-16-sem` on `neutral/black` |
| Active tab | `primary/500-main` fill, `neutral/white` text — the one blue fill on the fold |
| Week label | `body-14-med` · `neutral/400` · `py-4`, bottom-aligned |
| Callout | 320 wide, `neutral/900` on `neutral/800` border, `radius/12`, `p-16`, `gap-12`, `Shadows/S3` |

**The tabs are a staircase in 56px steps** — `top` 0, 56, 112, 168, 224 across the five columns.
That is the whole visual idea of the fold; even spacing would flatten it.

The callout's eyebrow (`WEEKS 3-4`) is Inter Medium 14 with `leading-none`, which is the
`button-14-med` token doing duty as a label. Uppercase is applied in the copy, not by CSS.

## `fold/Comparison Table` — `1824:6836` · Desktop measured

Props: `breakpoint` only. Root has **no fixed width** — it sizes from the table.

| Part | Measured |
|---|---|
| Root | `gap-60`, centred |
| Heading | **620** wide, `h3` 44 on `neutral/black`, **no eyebrow and no subtext** |
| Table Body | **1px** `neutral/100` border, `radius/20`, `overflow-clip` |
| Every cell border | **1.5px** `neutral/100` |
| Header row | 1240 wide, cells **60** tall, `neutral/white` fill |
| Header type | Inter **Bold** 16/24 on `secondary/500-main` |
| Gushwork header cell | **the logo SVG at 105.24 × 20**, not text |
| Feature column | `flex-1`, `p-12`, fill `#f7f8f9`, `body-16-med` on `secondary/500-main` |
| Gushwork column | **280** fixed, fill `#f2f8ff`, `body-14-sem` on **`primary/500-main`** |
| Competitor columns | **280** each, `bg-white`, `body-14-med` on `secondary/500-main` |
| Rows | 7 |

**The Gushwork column is the only place blue is used** — a tinted `#f2f8ff` cell with blue
semibold text against plain white competitor cells. That contrast is the fold's whole argument;
losing it makes the table decorative.

**Three colours here are raw hex where a token exists** — `#f7f8f9` is `neutral/25`, `#f2f8ff` is
`primary/25`, and the competitor cells use bare `bg-white`. Recorded as measured; reported as a
binding gap, since a palette change would not reach them.

This fold is also where the **`secondary/500-main`** collection is used most heavily — every text
colour in the table binds it rather than `neutral/*`.

**Type conflict worth reporting:** this fold reports `Body/body-16-reg` with `letterSpacing -0.6`,
while `Cards Grid` and `Cards Grid (small)` report the same named style at `-0.2`. One name, two
values, depending on where you read it.

## `fold/ other` — `1790:6807` · Desktop measured

Props: `breakpoint` · `showCta`. The generic fold, and it is deliberately almost empty:

| Part | Measured |
|---|---|
| Root | 1240, `gap-60`, centred |
| Heading | the shared heading at full **800**, badge and subtext both on |
| `container` | **an empty div, full width, 320 tall** — no fill, no border, no radius |
| CTA | blue `primary/500-main`, 44 tall, radius 8 |

**The container is 320 tall with no styling at all** — unlike `With image`'s slot, which ships a
`neutral/50` placeholder. So `fold/ other` gives you a bare 320px band between a heading and a
CTA. Anything you put in it is yours to style, and 320 is a starting height, not a constraint.

## `fold/AI Agents` — `2085:18017` · Desktop measured

Props: `breakpoint` only. Full-bleed **1440**, `gap-60`, `pb-40`, `overflow-clip`.

**Four rows of nine `Agent Card`s, offset to fake a marquee:**

| Row | Offset |
|---|---|
| 1 | none |
| 2 | `pl-80` |
| 3 | `pr-120` |
| 4 | `pl-80` |

Row gap and card gap are both `spacing/12`. The agents are **shuffled per row**, not repeated in
order. The stagger plus `overflow-clip` on a 1440 frame is the entire effect — evenly aligned
rows read as a plain grid.

| Part | Measured |
|---|---|
| Heading | 800 wide, `h3` 44 on `neutral/black`, **hard two-line break** |
| Subhead | `body-18-med` max-w 680 on `neutral/600` |
| `Agent Card` | **min-w 270**, `pl-16 pr-20 py-16`, `radius/16`, `neutral/white` on `neutral/100` |
| — shadow | `0 2px 2px rgba(27,28,29,0.04)` — `Shadows/S2` |
| — title | `body-18-sem` · `neutral/black` |
| — subtitle | Inter Medium **12**, `leading-none`, `neutral/500` |

**`agent-icon` is a 60px tile drawn from 8px squares.** Each of the nine agents is a different
dot pattern — `primary/300` (`#66a9ff`) squares at `radius/2`, placed on an 11 / 21 / 31 / 41 px
grid inside the tile. It is a generated glyph, not an icon font, so it cannot be swapped for a
Phosphor icon.

Nine agents in use here: `research` · `refresh` · `authority` · `paid_boost` · `strategy` ·
`content` · `follow_up` · `memory` · `design_&_development`. The card's asymmetric padding
(16 left, 20 right) is as measured.

## `fold/ Hero` — `1731:55983` · `Layout=Centered` measured

| Part | Measured |
|---|---|
| Root | **1440** wide, **`neutral/25` fill** — the hero is tinted, not white |
| Rhythm | `py-120`, `gap-160` — the largest spacing values in the system |
| Container | 1240 |
| Text block | **872** wide, `gap-20`, centred |
| eyebrow | 24 tall, `px-8 py-4`, radius 100, `neutral/white` on **0.5px** `neutral/100` |
| Heading | **`h1` 60**/1.2 Vert Grotesk Bold · `neutral/black` |
| Subhead | `body-18-med` · **`neutral/700`** — darker than the `neutral/600` other folds use |
| Button row | `gap-12` |
| Primary | **`neutral/black` fill**, 44 tall, `px-20 py-16`, radius 8, `neutral/white` label |
| Secondary | **2px** `neutral/100` border, no fill, `button-16-med` on `neutral/black` |

**The Hero primary is `neutral/black` (`#0d0d0d`), not `neutral/900`** — same distinction as the
headings. And **it is the black button, not the blue one**, on this Brand variant; the blue
primary belongs to `Type=Ads`.

**Hero says `Book a demo`.** Confirms the split recorded above — Hero and CTA ship "Book a demo",
the six content folds ship "Book a call". Write `Book a Demo` regardless, per `voice.md`.

### The other four layouts — frame geometry

| Layout | Desktop | Phone |
|---|---|---|
| `Home` | 1440 × 1234 | 375 × 620 |
| `Centered` | 1440 × 590 | 375 × 656 |
| `Form` | 1440 × 729 | 375 × 1003 |
| `Split` | 1440 × 928 | 375 × 764 |
| `+ Create New` | 1440 × 540 | 375 × 460 |

Note these are **1440/375 frame widths**, not the 1240/343 content width — the hero symbol
includes the page margin. `Home` is by far the tallest because it carries the client-logo strip.
Per-layout internals still need measuring, one symbol at a time.

## Token findings from this pass

| Finding | Detail |
|---|---|
| **Letter-spacing was wrong system-wide** | Figma's magnitude is a **percent**, not px. `body-18-med` reports `-0.2` and renders `-0.036px` at 18px. `tokens.css` emitted `-0.2px` — 5–6× too wide on every style. Now emitted in `em`; **fixed**. |
| **`Body/body-18-med` does exist** | The known-issues list said it was the one ramp step missing its Medium. Figma returns it: Inter Medium 18/1.6, letterSpacing −0.2. That entry was wrong. |
| **`colors/neutral/white` has no token** | Used by `fold/ CTA`. Minor, but it is a real bound variable with nothing in `tokens.css`. |
| **`colors/secondary/500-main` `#111827`** | A whole **Secondary** collection that `tokens.css` documents only as a stray legacy `gray/900`. It is bound by a shipping fold, so it is current, not legacy. Needs pulling properly. |
