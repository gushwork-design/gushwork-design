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
