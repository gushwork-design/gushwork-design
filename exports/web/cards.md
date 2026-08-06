# Cards

Figma: group `card` (`1674:37764`) on `↳ web/ component-library`.

Seven card types. Pick by what the card holds.

## Pick the type by content

| Type | Holds | Set node | Variants |
|---|---|---|---|
| `Card / Testimonial` | First-party client proof captured by us — a video testimonial, or a quote with the client's photo and signature | `1647:720` | 5 of 8 |
| `Card / Review` | Third-party proof pulled from Trustpilot or G2 — author header + short quote | `1647:726` | 2 |
| `Card / Information` | Generic content card — title + body, optional leading icon and top-right action. **The default for arbitrary content.** | `1647:734` | 14 of 16 |
| `Card / Announcement` | Product update — category/date/"New" chips + title + body | `1647:738` | 3 of 4 |
| `Card / Pricing` | A plan — name + impact tag + price + feature list + CTA | `1647:743` | 4 |
| `Card / Case Study and Blog` | Image + category + headline; links to the full story | `1647:746` | 2 |
| `Card / Other` | Blank editable card. **Use when nothing above fits.** | `1647:723` | 2 |

**`Testimonial` vs `Review` — pick by source.** Our own captured proof (video, or
photo + quote) → `Testimonial`. Pulled from Trustpilot or G2 → `Review`.

## Variant properties

| Set | Properties |
|---|---|
| `Card / Testimonial` | `Device` [`Desktop`, `Mobile`] × `Expanded` [`no`, `yes`] × `Style` [`01`, `02`] · slot `image` |
| `Card / Review` | `Device` [`Mobile`, `Desktop`] |
| `Card / Information` | `Device` [`Desktop`, `Mobile`] × `Image` [`With`, `Without`] × `Style` [`1`, `2`, `3`, `4`] · slot `card-element` · bool `Subtext` (default true) |
| `Card / Announcement` | `Device` [`Desktop`, `Mobile`] × `State` [`Default`, `Hover`] |
| `Card / Pricing` | `Device` [`Desktop`, **`Phone`**] × `Type` [`Single card`, `3 cards`] |
| `Card / Case Study and Blog` | `State` [`Default`, `Hover`] — **no `Device` property** |
| `Card / Other` | `Device` [`Desktop`, `Mobile`] |

### Gaps

- `Card / Information` is missing `Desktop / With / Style 3` and `Desktop / With / Style 4`
  — 14, not 16.
- `Card / Testimonial` is missing 3 of 8.
- `Card / Announcement` is missing 1 of 4.

Requesting a missing combination resolves to nothing.

### Breakpoint key inconsistencies — all load-bearing

- The axis is **`Device`** on Cards but **`Breakpoint`** on Folds and Page Build.
- Values are **`Desktop` / `Mobile`** on five sets but **`Desktop` / `Phone`** on
  `Card / Pricing`.
- **`Card / Case Study and Blog` has no `Device` property at all**, so the rule's claim
  that "desktop and phone are built-in breakpoint properties on the component" is false
  for that type.
- `Style` numbering differs: `Card / Information` uses `1`,`2`,`3`,`4`;
  `Card / Testimonial` uses zero-padded `01`,`02`.

## Composition — reuse, don't rebuild

Cards compose existing components. **Pull them from their own components; don't restyle
them inside the card.**

| Used inside cards | Rules live in |
|---|---|
| `eyebrow` — e.g. the Trustpilot rating eyebrow on pricing | `atoms.md` |
| `Button` — the primary CTA | `button.md` |
| `client/avatar` — author photos | `avatar.md` |
| `image` — the image slot | `images.md` |
| `fold/fold-element/progress-bar` — inside `Card / Testimonial` | `fold-elements.md` |

**Badge is not used inside any Card.** It reaches folds through
`fold/fold-element/heading`'s `Show badge` property instead. If you want a status pill on
a card, that is not an established pattern — confirm first.

## CTA copy

The card's primary CTA is **`Book a Demo`** — a fixed string, capitalised.

The rule says `Book a demo` and cites "the system-wide button rule" as its authority. That
cross-reference is false — the button rule says "Book a call". Neither is correct: write
`Book a Demo`. See `foundation/voice.md` for the ruling.

## Breakpoints

`Device` is a built-in property (except on `Card / Case Study and Blog`). On phone,
**multi-column grids collapse to a single column and side-by-side internals stack.**

## Structure — `Card / Information`

The most-used type, as instanced in the worked page examples:

```
Card / Information (408×579 in a 3-up grid)
├── FRAME (408×287)
│   ├── FRAME (24 inset, 360×31)
│   │   ├── TEXT "Card title"
│   │   └── INSTANCE leading/action icon (20×20, top-right)
│   └── TEXT body (360×192, at y:71)
└── INSTANCE "image" (408×280)
    └── SLOT "Slot"
```

At 3-up inside a 1240 container the cards are 408 wide with 8px gaps; a second row uses
406.67 to fill exactly. Descendant instances observed: `ListMagnifyingGlass`, `image`,
`Sparkle`.

## Structure — `Card / Testimonial`

```
Card / Testimonial (780×320 wide form, 220×320 narrow form)
├── FRAME (516×304)                            [hidden in narrow form]
│   ├── FRAME (516×276) → FRAME (468×228)
│   │   ├── TEXT quote
│   │   └── TEXT "sig"                          ← client signature
│   └── FRAME (516×28)
│       └── INSTANCE "fold/fold-element/progress-bar" (492×4)
└── FRAME (240×304 wide / 204×304 narrow)
    ├── SLOT "image"                            ← client photo
    ├── FRAME (…×239) → INSTANCE "Button"       ← play / expand control
    └── FRAME (…×65)
        ├── TEXT "client-name"
        └── TEXT "designation-company"
```

A row of testimonials pairs one **wide** card (quote + photo + progress bar) with two
**narrow** cards (photo only, quote frame hidden) inside a 1240 container. Clicking a
narrow card expands it — that is what `Expanded` controls.

Note this card instances a **fold-element** (`progress-bar`), which inverts the
documented ladder. See `folds.md` for the caveat.

## Never

- Fabricate a client logo, photo, quote, or review. Cards carry proof; proof must be real.
- Ship the placeholder lorem ipsum that `Card / Information` ships with, or the literal
  string `Card title`.
- Restyle an eyebrow, button, or avatar inside a card.
- Use `Card / Other` when a specific type fits.

## Source notes

Rule node `2003:10795`. Naming is inconsistent across three places for every type — the
rule uses kebab (`case-study-and-blog`), the set uses Title Case with spaced slashes
(`Card / Case Study and Blog`), and the on-canvas label uses lowercase
(`card / case study and blog`). Use the set name.
