# Voice

The single source for how Gushwork writes. Both skills reference this file; neither
restates it. If you are choosing a word, a label, or a capital letter, the answer is
here.

## Who is speaking

A confident senior strategist talking to a busy founder. Direct, plainspoken, never
hype. The reader is short on time and has heard every marketing claim already — the
only thing that earns their attention is a number.

- **"We"** for Gushwork. **"You"** for the reader. Never "our clients" when you mean
  "you".
- **Lead with the outcome and the number.** "1.3M search impressions in 12 months",
  not "dramatically improved search visibility".
- Verbs of impact: **rank, publish, pipe, grow, compound**. Gushwork *pipes qualified
  leads to your inbox* — it does not "facilitate lead generation".
- Never a feature list without a metric attached.

## Casing — sentence case, everywhere

Sentence case for headings, subheadings, buttons, eyebrows, badges, nav items, table
headers, and form labels. Capitalise the first word and proper nouns. Nothing else.

Title case is permitted **only** for product and service nouns inside body copy —
`AI Search Engines`, `Content & SEO` — for the fixed navigation labels the product
already ships, and for **the primary CTA `Book a Demo`**, which is a fixed string
and a deliberate exception. See CTA copy below.

This rule is stated in four separate Figma component rules (card `2003:10795`, fold
`2089:23406`, navbar `2076:9861`, footer `2076:15468`) and is violated in three
places on the canvas. Those are bugs, not precedents:

| On canvas | Should be | Where |
|---|---|---|
| `See Customer Stories` | `See customer stories` | `fold/ Hero`, `I1731:59019;1453:3951` |
| `EXPLORE THE PRODUCT` | `Explore the product` | `navbar/navbar` `1706:1744`, submenu `1658:27235` |
| `Contact now!` | `Contact now` | `footer/…/cta-image` `1712:2505` |
| `Who It's for` | `Who It's For` (match the other four instances) | `navbar/navbar` `1706:1721` |

## Punctuation

- **No exclamation marks.** Anywhere. One exists on the canvas (`Contact now!`) and
  it is wrong.
- **No emoji.** Not as bullets, not as decoration, not as status signals. Status is
  carried by a Badge or a Phosphor icon — see `shared-components.md`.
- Oxford commas on. Curly quotes (`'` `"`) in prose. Em-dashes for asides.
- No italics in display or heading copy. Emphasise with weight (600 → 700), colour,
  or an eyebrow instead.

## CTA copy

**The primary CTA always reads exactly `Book a Demo`** — capital B, capital D. Change
it only when explicitly asked.

This is a **deliberate exception to the sentence-case rule above.** It is a fixed
brand string, not a sentence. Do not "correct" it to `Book a demo`, and do not
generalise the capitalisation to any other button.

The Figma file contradicts itself three ways on this string, so the ruling is recorded
here rather than inferred. Ruled by Utsav, 6 Aug 2026:

| Variant | Where it appears in Figma |
|---|---|
| `Book a demo` | 51 canvas nodes (`page-build`, `navbar`, `footer`, `footer/…/cta`, `fold/ Hero`, `fold/ CTA`) and four rules: fold `2089:23406`, navbar `2076:9861`, footer `2076:15468`, card `2003:10795` |
| `Book a call` | 42 canvas nodes (every content fold's inline CTA, 32 of them in `fold/ Cards Grid`) and two rules: web button `1972:4146`, inline-input `1979:4803` |
| **`Book a Demo`** | the three phone bottom-CTA buttons in the navbar structure blob — **the only nodes already correct** |

**Write `Book a Demo` regardless of which variant the component ships.** All three
Figma variants are open findings against the file; the ruling supersedes every one of
them. Note also that the card rule cites "the system-wide button rule" as its
authority while that rule actually says "Book a call" — the cross-reference is false
and should not be trusted in either direction.

**Secondary CTA** is `Calculate ROI with Gushwork` (28 nodes). A softer variant
`Not sure? Calculate ROI with us` exists on `fold/ Hero` (`1731:46100`) for the same
action — prefer the standard wording unless the fold is deliberately conversational.

**Form CTAs** are specific to their action and stay that way: `Check my lead
potential`, `Pick a time`. Do not normalise these to "Book a demo".

## Banned words

Never ship these:

`synergy` · `best-in-class` · `revolutionize` · `revolutionary` · `next-gen` ·
`unlock` · `leverage` (as a verb) · `seamless` · `cutting-edge` · `game-changing` ·
`world-class` · `supercharge` · `10x` · `ninja` · `rockstar`

Also avoid the empty intensifiers — `truly`, `simply`, `just`, `literally`,
`incredibly` — and hedges that undercut a claim: `may help you`, `can potentially`.
If the number is real, state it flatly.

## Placeholder copy

The Figma file ships lorem ipsum inside `Card / Information` and generic strings like
`Card title`, `Column Header`, `Entry name`, `List Item`, `Dropdown option 01`. None
of it is brand copy. Replace every placeholder with real copy in Gushwork voice, or
ask for the copy. Never ship `lorem ipsum` or `List Item 1`.
