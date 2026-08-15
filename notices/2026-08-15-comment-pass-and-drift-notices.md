# v1.39.0 — the Figma comment pass, three new components, and update notices

**15 Aug 2026**

## What changed for you

**If you have already built a dashboard:** open it. It now tells you when the components it was
built from have moved on, names what changed, and gives you a `How to update` button that copies a
ready-to-paste prompt. It appears once per change, never blocks the page, and stays silent if it
cannot reach the registry.

**If you are about to build one:** three components that did not exist are now specified —
`ring`, `dashboard-switcher`, `date-range-picker` — in `exports/dashboard/v2/overlays.md`.

## Fifteen measured corrections

Every one came from a comment on the Figma file and was re-measured from node properties first.
The full working is in `dashboard-component-audit.md` sections 10–12. The ones most likely to be
in your build:

- **badge** — dark tints are `<Tone>/Alpha/10` with a `<Tone>/300` label. Green and amber had **no**
  dark override at all and were painting their light `/25` tints on a dark surface.
- **topbar** — a button's glyph is bound to the same variable as its label, not the muted icon
  colour. `Sync Now` is `Neutral/50` in dark. `Compare` carries a fill and a stronger stroke.
- **sidebar** — the nav column is `SPACE_BETWEEN` over two blocks, so Settings and Admin pin to the
  bottom; the footer carries a 1.5px `Neutral/100` top stroke.
- **metric-card / page-header** — the ring's band is **2px**, from `arcData.innerRadius 0.8`, not
  the 5px stroke. It was 2.5× too heavy.
- **tooltip** — the light bubble is `Neutral/900`, not black.

## Two rules worth knowing

**`strokesIncludedInLayout` decides whether a stroke is layout or paint.** Two frames with identical
sizing gave opposite results until we read that boolean. An earlier note in this repo said "INSIDE
consumes on HUG, not on FIXED" — that fitted the numbers and was wrong.

**A hover needs contrast against its text *and* separation from its surface.** Checking only the
first misses the hover that equals the surface it lands on and renders as no hover at all. Four of
those shipped.

## Update

```bash
claude plugin marketplace update gushwork && claude plugin update gushwork-design@gushwork
```

Restart Claude Code after. A new version takes effect on the **next** start.
