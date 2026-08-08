# v1.21.0 — login screen re-measured, `Button` hover values corrected

**8 Aug 2026.** Three defects were reported against the `dashboard-login-screen` render. Fixing
them turned up a fourth thing that was wrong everywhere, not just on the login screen.

## What was reported

1. the background lattice should be very subtle
2. the Google icon is not showing
3. buttons and email fields are not showing; no hover states

## What was actually wrong

**(1) The lattice.** Two separate causes, both mine.

- The `BG` frame `2323:21853` carries **`opacity: 0.3`**. I had read the individual cells, which
  report a full-strength `1px dashed neutral/800` and say nothing about the parent's opacity.
- I rendered 400 cells each with a border on all four sides. Figma centre-aligns strokes so
  adjacent cells overlap into one line; CSS puts borders inside the box, so **every shared edge
  drew at 2px**. Now each cell draws only its right and bottom edge, with top and left on the
  container — one line per grid line.

Both were needed. Opacity alone on a doubled grid would still have been wrong.

**(2) The Google mark** was a text `"G"` I had written as a placeholder. The real asset —
`Platform=Google, Color=Original`, a four-path SVG — is now harvested to
`assets/brand/google-g.svg`. The `ArrowRight` is harvested too, at its measured
14.065 × 11.816 inside an 18px slot.

**(3) The buttons and fields were rendering** — that part of the report was the missing hover
states making them look inert, plus the lattice pulling the eye. Hovers are now live.

**(4) Three cells in the lattice are filled** `neutral/900` — at (col 15, row 7), (col 14, row 8)
and (col 6, row 15). Reported by Utsav, then verified against the 400-cell dump. I had missed
them entirely.

## The correction that reaches past the login screen

`button.md` carried three **ruled** hover values, written on the belief that the `State=Hover`
symbols had no fill. **They do.** All three rulings were wrong:

| `Style` | Was ruled | Measured | Node |
|---|---|---|---|
| `Primary` | `neutral-900` `#262a2e` | **`neutral/850` `#333333`** | `2203:839` |
| `Outline` | `neutral-25` `#f7f8f9` | **`neutral/35` `#f5f5f5`** | `2203:875` |
| `Ghost` | `neutral-25` `#f7f8f9` | **`neutral/50` `#f1f2f3`** | `2203:911` |

Figma's hovers are one step stronger than the guess in every case. `Outline` also keeps its 2px
`neutral/100` border across both states, and `Ghost` and `Outline` do **not** share a value —
the ruling assumed they did.

**Anything built against those ruled hovers has slightly wrong hover fills.** The gaps are small
in hex and none of them is visible in a screenshot.

## Other measurements corrected

| | Was | Now |
|---|---|---|
| Black button height | 48 (as `Button Large`) | **50** — `py-16` around an 18px icon |
| Its shadow | raw `drop-shadow(0 16px 16px …)` | **`--gw-shadow-s3`** — Tailwind can't express spread, so it flattened `radius 32, spread -12` |
| Field → button gap | unrecorded | **16** |
| Right column | `calc(50% + 410px)` + translate | **`x = 900`**; `y` 263 / 292 / 200 by variant |
| `Google` variant column | I had rendered `y 314` | **292** — I had guessed it |
| Google buttons | assumed `Button` instances | **plain frames** — the 48-tall one uses 15px vertical padding, which no `Button` size does |

## The one that needs your decision

**`input/text-field` `1562:705` is a web component.** It lives in `↳ web/ component-library`
under `input-fields`, with 14 variants. The dashboard library has no text field at all — so this
dashboard screen reaches across the surface boundary, and it is the only place in the dashboard
set that does.

That matters because the two skills are surface-scoped: a dashboard build otherwise never opens
`exports/web/`. Left as-is, a change made for a marketing form silently changes the login screen.

Two ways out, both fine, but it should be a decision:

- **promote the field to a shared atom** in `foundation/`, next to the badge and the logo; or
- **give the dashboard its own**, and switch this screen to it.

Flagged, not resolved.

## Also fixed

`preview/review-sheet.html` had **no `<meta charset>`**. Every em-dash, arrow and `×` in the
sheet was rendering as mojibake over HTTP. It now opens with a doctype and `charset=utf-8`.

## Still open

- The Google button is 72/16/with-arrow in `Type=Google` and 48/12/without in
  `Type=Google + Email`. Two variants of one component, two different buttons. Needs a ruling.
- `dashboardTitle` binds a raw `#000000` rather than `--gw-color-neutral-black` `#0d0d0d`.
- The `0.81px` border on both Google buttons is a 1px border on a scaled instance.
- The field's own hover and the white Google button's hover have no Figma counterpart. They are
  ruled here — `neutral/100` and `neutral/35` — and labelled as ruled in the sheet.
