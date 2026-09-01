# Lead-magnet document — page shell

The downloadable PDF behind an ad landing page. Nine pages in the reference build; the shell
is what stays constant.

| | |
|---|---|
| Page size | **US Letter, 612 × 792 pt** (`@page { size: 8.5in 11in; margin: 0 }`) |
| Margin | **40 pt** on all four sides — measured off the Figma cover frame, not chosen |
| Content column | **532 pt** |
| Output | Chrome headless print-to-PDF. Text stays selectable, so prompts can be copied |

## Two coordinate systems, deliberately

The cover and closer are Letter-sized Figma frames, so they are rebuilt at **true Figma
coordinates in `pt`** with absolute positioning — the frame and the page are 1:1 and every
number is measured. Interior pages are ordinary flex-column flow in `px`.

**This is why the type ramp is not tokenised.** `--gw-text-*` is px-based for web. `56pt` is
not `56px`; consuming the token on the cover would shrink every heading by a quarter. The
template declares its print ramp as template-local `--lm-*` custom properties. Everything
`--gw-*` in the template is a real system token; everything `--lm-*` is local to the document.

## Checking that a page fits — do not eyeball this

Pages are fixed-height with `overflow:hidden`, so an overflow is **silent**: the content is
simply clipped and the render still looks plausible.

Measure the lowest ink on each page — across **text lines and drawn rectangles both** — and
compare it to **752** (792 less the 40pt bottom margin):

```python
lows = [l["bbox"][3] for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
        if "".join(s["text"] for s in l["spans"]).strip()]
lows += [d["rect"].y1 for d in page.get_drawings() if 2 < d["rect"].height < 700]
clearance = 752 - max(lows)          # healthy: 15–60pt. Negative: clipped.
```

Text-only checks are not enough. One build passed with the closer's CTA box outline running to
**755.3** — the type cleared the margin, the box did not.

On the dark pages, threshold above the blueprint grid (line delta ≈ 8/255) or the grid reads as
content.

## The blueprint grid

Both dark pages carry it. 1pt lines on a **25 pt pitch**, phased so verticals land on
`x ≡ 12 (mod 25)` and horizontals on `y ≡ 24 (mod 25)`. Line colour `#151517` on `#0d0d0d` —
about 8/255 above the ground, invisible unless you amplify the export.

Two details that cost time:

- **Bake the phase into each gradient's 25pt period.** Using `background-position` to phase it
  tile-edges a spurious extra line at x=0.
- The grid **fades** — roughly top→bottom with extra falloff bottom-right, from ≈8/255 at the
  top to 1–3 at the bottom. Two ink-coloured washes over the grid reproduce it, since the
  ground is flat and a wash is then equivalent to a mask.
- A page carrying the grid must set **`background-color`**, never the `background` shorthand,
  which silently wipes the grid's `background-image`.

The cover frame has the grid. **The closer frame (1769:3965) does not** — carrying it onto the
closer is a deliberate override so the two dark pages match. See `RECONCILIATION.md`.
