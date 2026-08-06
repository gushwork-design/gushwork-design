# Icons

The complete Phosphor library — the icon set the Gushwork Figma file imports.

```
assets/icons/
├── thin/        1512 svg
├── light/       1512 svg
├── regular/     1512 svg   ← the default
├── bold/        1512 svg
├── fill/        1512 svg
├── duotone/     1512 svg
└── _figma-verified/  4 svg  ← ground truth, see Provenance
```

`@phosphor-icons/core` v2.1.1, MIT. 9,072 files, 4.6 MB.

## Lookup

`assets/icons/{weight}/{kebab-name}.svg` — e.g. `assets/icons/bold/arrow-up-right.svg`.

Upstream names non-regular files `arrow-up-right-bold.svg`; that suffix is stripped here so
the name is identical across every weight and only the directory changes.

## Which weight

From how the components actually instance icons — the Figma icon group carries no weight
guidance of its own.

| Weight | Use |
|---|---|
| `regular` | inline and navigational icons. **The default.** |
| `bold` | inside buttons; the small icon tiles in dashboard section headers |
| `fill` | filled glyphs — a badge glyph, a caret in a dropdown trigger |
| `light` · `thin` | subtle or large decorative contexts |
| `duotone` | decorative and illustration contexts only |

## Colour

Every file carries `fill="currentColor"` on the root `<svg>`, so an icon inherits its
parent's text colour. Never hardcode an icon fill.

**Inline the markup — don't load through `<img>`.** An `<img src="….svg">` renders in a
separate document and cannot inherit `currentColor`; the glyph falls back to black whatever
the surrounding colour. Verified. Use an inline `<svg>`, a `<symbol>`+`<use>` sprite, or an
icon component.

## Size

`viewBox="0 0 256 256"` on every file — set the rendered size in CSS. Match the
`Icons/{size}` token you are working to: 12 · 16 · 20 · 24 · 28 · 32 · 36 · 40. Buttons use
18px, which is not a token step — it is the button component's own internal size.

## Provenance

The Figma library is Phosphor, imported. Extracting all 1,248 sets from Figma directly was
not viable: variant node IDs are not derivable from a set ID, so each icon needs a
`get_metadata` call *then* a download — roughly 2,500 calls for a single weight, ~15,000 for
all six.

So the package was taken from upstream and **verified against Figma**. Four icons were first
harvested directly from the file at `Weight=Regular, Size=24`:

| Icon | Figma set | Variant node |
|---|---|---|
| `caret-down` | `112:4354` | `1426:26933` |
| `arrow-up-right` | `112:4802` | `1426:29845` |
| `target` | `112:13686` | `1426:87560` |
| `arrow-clockwise` | `112:5600` | `1426:35032` |

Those four are kept in `_figma-verified/` as ground truth. Coordinate spaces differ — the
Figma export is `0 0 24 24`, upstream is `0 0 256 256` — so a literal path diff proves
nothing. They were overlaid at matched size instead: **all four register exactly, with no
fringing.** The shapes are identical, so the upstream package is the same artwork.

Re-run that check with `preview/icon-verify.html` if the package is ever bumped.

## Known discrepancy — 1,512 vs 1,248

The Figma file has **1,248** icon component sets. This package has **1,512** per weight. It
is a superset: Phosphor 2.1.1 is newer than the import.

**~264 icons here are not in the Figma library.** Using one is off-system even though the
file is present. There is no manifest of the 1,248, so this cannot currently be checked
automatically — if an icon looks unusual for the brand, confirm it exists in Figma before
shipping it.

Three sets in Figma are still named `component_set-element` (`112:12523`, `112:12537`,
`112:17221`), so they are unsearchable by icon name and cannot be matched against this set
either.
