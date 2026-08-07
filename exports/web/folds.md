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

> **Measured correction.** `fold/ Cards Grid` — the fold this rule is most obviously about —
> **has no `Show Card` properties at all.** Its real axes are `Card Style`, `Card Image` and
> `Card Layout`. See *Measured appearance* below before relying on this table.

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

**All 12 folds now have measured frame geometry and variant matrices.** Internals are measured
for `With image`, `FAQs`, `CTA` and `Cards Grid`; the remaining eight have geometry but their
inner spacing and type are still annotation-only.

## Fold width is 1240 — except three

Measured on every fold. The container is **1240 desktop / 343 phone**, and the exceptions are
deliberate or defects:

| Fold | Desktop | Phone | |
|---|---|---|---|
| Most folds | 1240 | 343 | the norm |
| `fold/ Hero` | **1440** | **375** | full-bleed — the symbol includes the page margin |
| `fold/AI Agents` | **1440** | **375** | full-bleed — the marquee runs edge to edge |
| `fold/Comparison Table` | **1242** | **337** | **off by +2 / −6. No reason for it — a defect.** |

Build to 1240/343 unless the fold is one of the two full-bleed ones. Do not reproduce the
Comparison Table's 1242/337.

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

## `fold/ CTA` — `2085:20750`

Props: `breakpoint` only. Nests `ClientAvatar` and `footer/footer-elements/cta-image`, which is
why the fold cannot be restyled independently.

Measured: 1240 container, 600-wide inner block, 440 tall panel, `radius/40` avatars at 56×40,
gaps 40 / 20 / 12 / 8. Type is h3 44 and h4 38 over `body-14`/`body-16` Inter Medium.

**Binds `colors/secondary/500-main` (`#111827`).** That is a *Secondary* collection — see the
token findings below.

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

**There are no `Show Card 3`–`Show Card 6` properties on this fold.** The shared-toggles table
above lists them and instructs you to use them instead of deleting instances. They do not exist
here — the fold hard-builds **six** cards in two rows of three, and the only content toggle is
`showCta`. Treat that rule as applying to whichever fold actually carries those booleans, not
this one.

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

**The two card rows have different gaps — row 1 is `gap-8`, row 2 is `gap-10`.** Since cards are
`flex-1`, that makes row 1's cards 2px wider than row 2's. It is a drawing slip, not a design.
**Use 10 for both** and note it, rather than reproducing a visible misalignment.

`Card / Information` carries its own `subtext` boolean, so a card can drop its body copy without
a different style.

## `fold/ Hero` — `1731:55983` · frame geometry only

Too large for a single design-context read; the 10 variant symbols measure:

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
