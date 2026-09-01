# Lead-magnet interior pages — components

Ground is `--gw-color-neutral-25`; every surface on top is **white** with a
`--gw-color-neutral-100` hairline. This inverts the usual grey-card-on-white convention —
anything you add must be a white surface or it disappears into the wash.

## Running head

The only page chrome. There is **no footer**.

```
◩ Gushwork visibility pack                     Part 1 of 4 · Page 03 of 09
──────────────────────────────────────────────────────────────────────────
```

| | |
|---|---|
| Left | `assets/logo/gushwork-symbol-original.svg` at 20px + document name, 13.5px `--gw-color-neutral-600` |
| Right | `Section · Page NN of NN`, same size and colour |
| Rule | 1px `--gw-color-neutral-100`, 15px above it, **46px** below |

The repo's logo SVGs carry only a `viewBox` and no intrinsic `width`/`height`. `width:auto`
therefore resolves against the UA default and the head sits ~1.5pt differently than it does with
an SVG that declares its size. Harmless, but it is why a ported build does not diff to zero.

**Page numbers are literal strings.** Add or remove a page and every head needs renumbering by
hand.

## Components

| Component | Class | Notes |
|---|---|---|
| Prompt row | `.prow` | White, 16pt radius, 17×20 padding. Black **rounded-square** numeral `.pnum` — 30×30, 9px radius, zero-padded. Not the blue circle used elsewhere in the system |
| Prompt note | `.pnote` | Hairline above, 12.5px `--gw-color-neutral-600`, inside the row |
| Featured prompt | `.prow--lead` | 17px text, 32px numeral. For a page whose single prompt is the point |
| Dense page scope | `.page--dense` | Tightens row padding and gap. One page needed it to clear the bottom margin |
| Card | `.card` / `.card--blue` | 24pt radius. Blue variant is `--gw-color-primary-50` on `--gw-color-primary-100` |
| Two plain columns | `.setupcols` | No card chrome — hairline-separated lists on the wash |
| Write-on rule | `.wscell` / `.wsline` / `.name3` | **Must be `display:block`** — an inline `<span>` drops its height and the rule silently vanishes |
| Worksheet grid | `.wsgrid` | Label and hint on one baseline row of fixed height, rule beneath. The fixed height is what keeps rules aligned when a hint wraps |
| Y/N tick pair | `.tick` | Never name an inner element `.yn` inside a `<td class="yn">` — that collision mangles the table |
| Score bands | `.band--1/2/3` | Blue intensity ramp: `primary-50` → `primary-100` → solid `primary-500`, so the worst score carries the heaviest ink |
| Tally row | `.tally` | Ten tickable boxes, tabular numerals |
| Note bar | `.notebar` | Blue-50 claim + detail. The bridge between sections |
| Comparison table | `.etable` | Engine rows with tick pairs and write-on rules |

## Traps that have cost a rebuild

- **Write-on rules must be `display:block`.** As inline spans they collapse to nothing and the
  worksheet renders as labels with no lines under them.
- **`.eyebrow` and any inline-flex button need `align-self:flex-start`** inside the flex-column
  page, or they stretch to full width.
- **Never reuse a class name between a `<td>` and its inner spans.** `.yn` on both mangled the
  three-engine table.
