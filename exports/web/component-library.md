# `↳ web/ component-library` — the measured inventory

Figma page `112:414`. **Read 7 Aug 2026.** This page had never been read before: whole-page
metadata calls were failing, and the working assumption was that a second navbar and a second
button set lived here. Neither is true — see *What this resolves* below.

**23 component sets · 525 variants**, in 11 groups.

## The sets

| Group | Set | Node | Variants |
|---|---|---|---|
| `button` | **`Button`** | `1457:668` | **220** |
| `badge` | `badge` | `1582:628` | **108** |
| `image` | `image` | `1815:8655` | **46** |
| `inline-input` | `input/inline-input` | `1584:1579` | 24 |
| `ai-agents` | `agent-icon` | `1606:581` | 20 |
| `card` | `Card / Information` | `1647:734` | 14 |
| `input-fields` | `input/text-field` | `1562:705` | 14 |
| `input-fields` | `input/phone-field` | `1562:5506` | 14 |
| `clients` | `client/avatar` | `1619:722` | 12 |
| `tooltip` | `tooltip` | `1554:348` | 9 |
| `eyebrow` | `eyebrow` | `1516:410` | 6 |
| `card` | `Card / Testimonial` | `1647:720` | 5 |
| `input-fields` | `input/ dropdown-options` | `1490:3488` | 5 |
| `card` | `Card / Pricing` | `1647:743` | 4 |
| `input-fields` | `input/dropdown` | `1562:5769` | 4 |
| `card` | `Card / Announcement` | `1647:738` | 3 |
| `input-fields` | `input/card` | `1562:5807` | 3 |
| `input-fields` | `input/checkbox` | `1977:4776` | 3 |
| `input-fields` | **`Frame 2147259995`** | `1553:3350` | 3 |
| `card` | `Card / Review` | `1647:726` | 2 |
| `card` | `Card / Case Study and Blog` | `1647:746` | 2 |
| `card` | `Card / Other` | `1647:723` | 2 |
| `input-fields` | **`Frame 2147259996`** | `1553:3351` | 2 |

## What this resolves

**Utsav's ruling of 6 Aug — "there is no second component library" — is now confirmed by
measurement**, where before it rested on his say-so against the README's standing hypothesis that
a second navbar and button set would explain the conflicts.

Counted off the page: exactly one `Button` (`1457:668`, the 220-variant set already documented),
and **no navbar at all** — navbar and footer live on `↳ web/ pattern-library`.

So the conflicts between the measured exports and the Master Specification are **real
disagreements, not two components mistaken for one.** The exports follow the measured node, which
is what renders. The README's "the likeliest explanation is a second set" note is wrong and
should be struck.

**`image` has 46 variants.** The docs variously claim 47, then 46, and their tables sum to 45.
**46 is correct** — counted off the set.

**`agent-icon` has 20 variants**, consistent with 10 agents × `add emphasis [false, true]`.

## Newly surfaced — not in any earlier inventory

- **`badge` carries 108 variants.** Its rule documents six colours. 108 is a much larger matrix
  than anything written down, and it is the component both surfaces share. Needs its own pass.
- **`Card / Announcement` (`1647:738`)** and **`Card / Other` (`1647:723`)** complete the seven
  card sets; earlier notes named only five by name.
- **`input/card` (`1562:5807`)**, 3 variants — an input type absent from the input-fields rule.
- **Two unnamed component sets inside `input-fields`** — `Frame 2147259995` (`1553:3350`, 3
  variants) and `Frame 2147259996` (`1553:3351`, 2 variants). Figma auto-names shipped as real
  sets. They are the icon sets whose sibling frames both read `Label: Processing`.

## Page hygiene, confirmed

**21 stray hidden `Frame 2147223955` nodes** sit at the page root, each 149 × 40, ahead of the 11
real groups. They are the "21 component sets" figure that earlier inventories reported — the
count was right, the interpretation was not. They are empty leftovers, not components.

## Still unmeasured here

This is an inventory, not an appearance pass. **None of these 23 sets has had its internals
measured** — the variant matrices, dimensions and bound tokens still come from annotations.
`Button`, `badge` and `image` between them account for 374 of the 525 variants and should go
first.
