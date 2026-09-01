# Lead-magnet template

The downloadable PDF behind an ad landing page. US Letter, nine pages, print-ready and
text-selectable.

```bash
./render.sh          # -> lead-magnet.pdf
```

Needs Google Chrome and, on the first run, a network connection: Phosphor icons (fill and bold
weights) load from the jsDelivr CDN and are then embedded as a font subset. Fonts, tokens and
brand assets all come from the repo — the template owns no copies.

## Using it

Copy the folder, then keep the page types you need and delete the rest:

```bash
cp -r templates/lead-magnet templates/<your-doc-slug>
```

The nine pages of the reference build — the "Can AI find your business?" prompt pack — double
as the component library. Every interior component appears at least once.

## What comes from where

| | |
|---|---|
| Colour, radius | `foundation/tokens.css` — every `--gw-*` in this file is a real system token |
| Print type ramp | template-local `--lm-*`. Deliberate: see `exports/lead-magnet/document.md` |
| Fonts | `../../fonts/` |
| Logo | `../../assets/logo/` |
| Cover hero, chip icon | `../../assets/lead-magnet/` |
| Measured specs | `exports/lead-magnet/` |

## Before you call an edit done

Pages are fixed-height with `overflow:hidden`, so overflow is **silent**. Measure the lowest ink
— text **and** drawn rectangles — against 752. The check is in
`exports/lead-magnet/document.md`. This is not optional; eyeballing has passed a clipped page.

The cover and closer are owned by Figma frames. Re-fetch the node before editing either.
