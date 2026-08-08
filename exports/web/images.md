# Image library

Figma: group `image` (`1948:8196`) · set `1815:8655` · **46 variants** · 4000×3266.

An illustration and product-screenshot asset library. Each variant is a composed UI mockup
built from groups and frames — not a bitmap.

## Variant properties

| Property | Values |
|---|---|
| `category` | `image`, `solution-image`, `problem-image`, `+ Create New` |
| `variant` | 46 values, listed below |

Slot property `Slot#1809:3` — available on the `+ Create New` variant for custom content.

`+ Create New` is Figma's "create new option" UI affordance that leaked into the data as a
real variant value. It is not a real asset; it is an empty slot. Do not select it unless
you are deliberately supplying a custom illustration.

## Pick `category` first

| Category | What it is | Use in |
|---|---|---|
| `image` | Product feature screenshots — 38 variants | Feature folds, cards, dashboards-in-a-fold |
| `solution-image` | Larger illustrative "after" state — 3 variants | Hero and comparison sections |
| `problem-image` | Larger illustrative "before" state — 3 variants | Hero and comparison sections |
| `+ Create New` | Empty slot | Custom illustration only |

Then **match the `variant` name to the fold's topic.** The names are semantic — pick
`image/keyword-ranking` for a fold about rankings, not a visually similar one.

**Pair problem with solution.** `solution-image` and `problem-image` mirror each other;
when a fold contrasts before and after, use the matching pair.

## `category=image` — 38 variants

Two size tiers. Small cards (~407×214) for agent features; wide panels (~610×345) for
dashboard and analytics views.

| Variant | Size |
|---|---|
| `image/strategy-and-pages` | 615 × 216 |
| `image/creative-agent` | 615 × 272 |
| `image/campaign-agent` | 407 × 214 |
| `image/learning-agent` | 407 × 214 |
| `image/follow-up-agent` | 408 × 214 |
| `image/verified-leads` | 615 × 216 |
| `image/brand-memory` | 615 × 216 |
| `image/spam-filter` | 615 × 240 |
| `image/search-query-card` | 615 × 224 |
| `image/traffic-trend` | 610 × 346 |
| `image/traffic-breakup` | 610 × 346 |
| `image/performance-analysis` | 610 × 346 |
| `image/lead-count-over-time` | 610 × 345 |
| `image/top-pages-by-score` | 610 × 345 |
| `image/keyword-ranking` | 610 × 345 |
| `image/assign` | 610 × 346 |
| `image/adding-notes` | 610 × 353 |
| `image/new-lead` | 610 × 351 |
| `image/lead-notification` | 610 × 350 |
| `image/lead-journey` | 610 × 356 |
| `image/connect-domain` | 610 × 373 |
| `image/domain-status` | 610 × 349 |
| `image/network-of-pages` | 610 × 360 |
| `image/llms-txt` | 610 × 359 |
| `image/website-analysis` | 610 × 332 |
| `image/analysing-buyer-searches` | 610 × 300 |
| `image/categorizing-search-queries` | 610 × 300 |
| `image/creating-pages` | 610 × 318 |
| `image/analysing-your-competitors` | 610 × 328 |
| `image/image-website` | 610 × 317 |
| `image/infographics` | 610 × 333 |
| `image/updating-pages` | 610 × 356 |
| `image/photos-&-colors` | 610 × 319 |
| `image/design-&-dev` | 407 × 214 |
| `image/page-cards-loading` | 406 × 214 |
| `image/giving-changes` | 540 × 310 |
| `image/buyer-profile` | 540 × 324 |
| `image/product-&-service-cards` | 620 × 320 |
| `image/Frame 2147259566` | — |

## `category=solution-image` — 3 variants

| Variant | Size |
|---|---|
| `solution-image/lead-notification` | 570 × 440 |
| `solution-image/confident-buyer` | 580 × 480 |
| `solution-image/got-mentioned` | 580 × 600 |

## `category=problem-image` — 3 variants

| Variant | Size |
|---|---|
| `problem-image/slow-speed` | 580 × 439 |
| `problem-image/confused-buyer` | 580 × 480 |
| `problem-image/buyer-searching-using-ai` | 580 × 600 |

## The problem/solution pairs

| Problem | Solution |
|---|---|
| `problem-image/confused-buyer` (580×480) | `solution-image/confident-buyer` (580×480) |
| `problem-image/buyer-searching-using-ai` (580×600) | `solution-image/got-mentioned` (580×600) |
| `problem-image/slow-speed` (580×439) | `solution-image/lead-notification` (570×440) |

Matched by name and by size. The rule marks the pairing intent as unconfirmed
(`[confirm pairing intent]` in `2066:15571`), so treat this table as strongly implied
rather than ruled.

## Sizes are not uniform

Widths range 406–620 and heights 214–600 within a single category. **The parent layout
must handle flexible sizing.** Do not assume a fixed aspect ratio or force a size.

## Variant names are keys — keep them stable

Renaming a variant changes its key and breaks every instance. Use the names above exactly.

## Source notes

- **Two typos exist in the documentation only, not in the components.** The structure doc
  (`2065:15565`) lists `image/startegy-and-pages` and `image/product-&-serivce-cards`. The
  actual canvas variants are spelled correctly — `image/strategy-and-pages` and
  `image/product-&-service-cards`. The doc also sets the typo'd name as the property
  default. Use the correct spellings above.
- The unresolved bracket in the rule — *"[decide before handoff: fix the typos … in Figma
  now, or keep them exactly as-is permanently]"* — is **built on a wrong premise**: the
  typos are not in Figma, they are in the doc. Nothing needs renaming; the doc needs
  correcting. **RULED on that basis** — `DECISIONS.md` → **R8**. This file's reading of the
  canvas is what settled it; `component-library.md` had reported the typos as keys because it
  read the doc blob, and has been corrected.
- **The doc states three different totals for one property**: "47 total options", then
  "All Variants (46 total)", and its per-category tables sum to 45. **The canvas has 46.**
  The 46th, missing from the doc, is `image/Frame 2147259566` — an unnamed frame promoted
  into a variant key. It is undocumented and unnameable; avoid it.
- `+ Create New` renders as the malformed doubled value
  `category=+ Create New, variant=+ Create New+Create New`.
- `image` is the only web group with a Component Structure blob, and the only one whose
  Info Frame holds two text-groups (`2066:15570` rules, `2065:15564` structure).
