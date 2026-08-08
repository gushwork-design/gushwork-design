# v1.23.0 — six more dashboard components measured; the chart palette blocker resolved

**8 Aug 2026.** Second measurement pass. Six of the eight remaining unverified dashboard
components read off their sets. **Running total: 17 checked, 15 had been recorded wrong.**

| Component | Verdict |
|---|---|
| `controls/dropdown` | **5 values wrong**, including one invented element |
| `table-row` `Hover` / `Selected` | 1 ruling right, 1 state never recorded, 1 binding bug |
| `section/Container` | **fully correct** — first clean one |
| `Graph Type=Bar` | 1 internal inconsistency |
| `Graph Type=Line` | the recorded blocker was a **misreading** |
| `Graph Type=Grouped Bar` | 3 raw hexes, 1 genuine palette gap |

## `controls/dropdown` — a ruling invented a checkmark

Both dropdown sections were previously **RULED** on the belief that Figma recorded only sizes.
Figma had everything. Five things were wrong:

| | Ruled | Measured |
|---|---|---|
| Menu border | 1px inset `neutral-100` | **1px `neutral/50`** |
| Option type | `body-12-med` | **`button-12-med`** — line-height 1 |
| Option hover | `neutral-25` | **`neutral/50`** |
| Menu width | implied to match the trigger | **160 vs 144**, right-aligned |
| **Selected mark** | `Check` 12px in `primary-500` | **does not exist** |

**The checkmark is the one that matters.** A build following the old ruling renders an affordance
the design does not have, and a single-select dropdown then shows two competing signals for the
current value.

Also wrong: the `Color=White` ruling described its border as "a 1px inset ring … matching how the
Grey variant is constructed". **Grey has no ring at all** — it is a bare fill. White's ring is a
real border that occupies layout. The token was right; the reasoning was invented.

## `table-row` — Selected and Hover are the same colour

`State=Hover` was ruled at `neutral/25` by borrowing `list-item`'s hover. **That ruling is
correct** — confirmed, not assumed. `State=Selected` had never been recorded at all, and it is
**the same `neutral/25`**. A selected row is distinguished *only* by a 16 × 16 black checkbox
holding a 12px white `Check`. Hovering a selected row changes nothing.

Do not invent a darker selected fill to separate them.

**The cell text binds a raw `#6a7077`** — exactly `neutral-600`, but unbound, so a palette change
would miss every table cell in the system. R4 applies.

## `section/Container` — correct

Every value already recorded checks out: 1084 wide, radius 12, `p-12`, `gap-16`, `neutral/25`
shell; `primary/alpha/10` icon tile; Semi Bold 14 title on `neutral/800`; white inner card with a
`neutral/50` hairline; the caret flip. **First component in either pass to need no correction.**

## The chart palette blocker was narrower than we thought

`skills/gushwork-dashboard/SKILL.md` carried this as a hard gap: *"`Graph Type=Line`'s second
series has no colour and `Grouped Bar`'s three are raw hex. Any multi-series chart is blocked."*

**`Line` has no second series.** Its data is four SVG assets rather than styled elements, which
is why a CSS-level read found a colourless second shape. Downloading them settles it:

| Asset | Measured |
|---|---|
| The line | `#0070FF` = `--gw-color-primary-500`, `stroke-width: 2` |
| The shape read as "series 2" | a vertical **linear gradient**, `#0070FF` 30% → 0% — the area fill *under* the line |
| Grid lines | `#E7E8E9` = `--gw-color-neutral-100` |
| Crosshair | `#0070FF`, `stroke-dasharray: 2 2` |

So `Line` is single-series by design and never needed a categorical palette. **Only `Grouped Bar`
did**, and it is now ruled — R11:

| Series | Measured | Build |
|---|---|---|
| 1 | `#a1cdfe` | `--gw-color-primary-200` — within ~11/765, an unbound token |
| 2 | `#9784ff` | **`--gw-color-chart-violet`** — new token; the system has no violet ramp |
| 3 | `#fed14a` | `--gw-color-yellow-200` — within ~4/765, an unbound token |

Added to `tokens.css` as `--gw-color-chart-1/2/3`. **Three series is the ceiling** — a fourth
category is a finding to report, not a colour to pick.

## An undocumented tooltip

`Graph Type=Line` carries a hover tooltip that appears in **no export**: `neutral/25` surface,
0.5px `neutral/100` border, radius 4, `p-8`, `--gw-shadow-s2`, a `Clock` + time header, a
headline, and a breakdown block behind a **0.7px dashed left rule** in 8px type. Now recorded in
`sections.md`.

Its shadow shows the same Tailwind flattening as the login button's S3 — the class says
`drop-shadow(0 2px 2px)`, the style annotation says `Shadows/S2` at *radius 4*. **The annotation
is the token.**

## Two one-off drifts inside single components

- **`Bar`'s value labels**: the first is `neutral/black`, the other two `neutral/900`. Same role,
  two colours. Build `neutral/900`.
- **`Grouped Bar`'s category labels**: one of seven is `neutral/black` where the rest are
  `neutral/600`. Build `neutral/600`.

Both look like a stray selection during drawing rather than intent. Reported, not absorbed.

## Not done

**`section/With Dropdown` (`2140:16131`) and `section/table` (`2209:17021`) were not read.** They
are the last two unverified dashboard components. Given a rate of 15 wrong out of 17, assume
their recorded values are provisional until someone opens the symbols.

`table-row` `Type=Header` (3 variants) also remains ruled rather than measured, and is flagged as
provisional in `section-elements.md`.
