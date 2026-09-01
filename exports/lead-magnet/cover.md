# Lead-magnet cover — measured

Source: **`GW Meta / Google Ads`**, frame `Letter - 2`, `node-id=1746-7661`,
file key `O6g05YAT980r85VaDQha4h`.

Exactly Letter, so the page is laid out at true Figma coordinates in `pt`. **These numbers are
measured. Do not round them.**

| Element | Position · size | Spec |
|---|---|---|
| Ground | full bleed | `--gw-color-black` `#0d0d0d`, plus the blueprint grid |
| Filled grid cells | `(387,124)` and `(412,149)`, 25×25 | Same tone as the grid lines — a diagonal step |
| Logo | `40,40` · 126.29×24 | **Blue symbol + white wordmark.** `assets/logo/gushwork-logo-blue-white.svg` |
| Content block | `40,144` · 532 wide | flex column, **gap 20pt** |
| Chip row | h 24, gap 8 | solid: white bg, `.5pt` `--gw-color-neutral-100` border, Inter Medium 12, `--gw-color-neutral-900`, 14pt icon · ghost: `.5pt` `--gw-color-neutral-800` border, Inter Medium 12, `--gw-color-neutral-100` |
| Headline + standfirst | 532×170 | flex column, **gap 12pt** |
| Headline | 532×134 | `Heading/h2` — Vert Grotesk Display Bold **56/1.2**, white, hard break |
| Standfirst | 532×24 | `Body/body-16-med` — Inter Medium **16/24**, white, `-0.2%` |
| Body | 532×60 | `Body/body-14-reg` — Inter Regular **14/20**, `--gw-color-neutral-400`, `-0.2%` |
| Hero image | card at `40,477` · 532×275 | radius **16pt**, `box-shadow: 0 16pt 32pt -12pt rgba(88,92,95,.10)` (`Shadows/S3`) |

## The headline needs a 4pt nudge

`position: relative; top: 4pt` on the 56pt headline. Figma sets the first baseline at
ascent-from-top; CSS half-leads the line box. The nudge aligns the glyphs to the frame without
changing the layout box. Verified by band-diffing the render against the frame export — every
element then lands within 1pt.

## The hero export must be cropped

The 4× frame export is 572×315pt: it carries 20pt of shadow bleed left and right, 4pt top, and
it bakes in a **flat `#0d0d0d` margin with no grid**. Dropping it straight onto the page punches
a grid-free 572×315 hole.

Crop it to the card exactly — px `80,16,2208,1116` of the 4× export = 532×275pt — and rebuild
the radius and the S3 shadow in CSS. The grid then shows through around and below the card, as
it does in the frame.
