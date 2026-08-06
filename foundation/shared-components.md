# Shared components

Atoms used on **both** surfaces. Referenced by both skills; restated in neither.

Everything else is surface-specific — see `exports/web/` and `exports/dashboard/`.
Three components look shared but are not: **Buttons, Avatars, and Logos each exist
separately per surface.** The Logo section below covers both, because one component
serves marketing and a different one serves product chrome. For Buttons and Avatars,
go to the per-surface exports.

---

## Badge

The status/label pill. Used by web cards and tables, and by dashboard kpi-cards and
dropdowns.

**Component set** `badge` · node `1582:628` · **108 variants** (complete).

| Property | Values |
|---|---|
| `Theme` | `Light`, `Dark` |
| `Color` | `Neutral`, `Red`, `Green`, `Yellow`, `Blue`, `Black` |
| `Icon` | `no`, `trailing`, `leading` |
| `Size` | `Small`, `Medium`, `Large` |

### Colour carries meaning — pick by what you are signalling

| Colour | Signals |
|---|---|
| `Neutral` | No signal. **The default** when nothing is specified. |
| `Red` | Bad / error / negative. |
| `Green` | Good / success / positive. |
| `Yellow` | Okay / warning / in-between. |
| `Black` | Neutral, but higher emphasis than `Neutral`. Use when a neutral badge needs to stand out. |
| `Blue` | **Undefined.** The rule never says what blue signals. Do not reach for it to mean "info" — ask first. |

Never use colour decoratively. A green badge on a falling metric is a bug.

### Icons

- **Leading icon** supports or clarifies the label. Optional.
- **Trailing icon** carries the signal as an arrow: up-arrow on green (positive),
  down-arrow on red (negative). On `Neutral`, `Blue`, or `Black` the arrow direction
  depends on context.

### Surface treatment

Each colour has a light and a dark treatment. **Match the surface the badge sits
on** — light badge on a light surface, dark on dark. Do not mix.

### Notes on the source

- The rule (`1979:10774`) calls the default colour **"Grey"**; the actual variant
  value is **`Neutral`**. "Grey" appears nowhere in the component. Use `Neutral`.
- The rule defines five signals but the component ships six colours — `Blue` is
  undocumented, then referenced later in the rule's own Icons paragraph as though it
  had been defined.
- The badge description claims support for **"counts"**. There is no count or
  numeric variant. Do not build one.
- **Provenance:** Badge physically lives on the *web* component-library page, and its
  rule text is surface-agnostic — it never says web, dashboard, or both. Treating it
  as shared is a deliberate decision recorded here, matching how it is actually used
  (dashboard kpi-cards and dropdowns instance it). The Figma file does not state it.

---

## Gushwork Logo

Two different components. Pick by surface first, then by background.

### Which one?

| Surface | Use | Node |
|---|---|---|
| Marketing web — navbar, footer, hero, any brand or ad page | `gushwork-logo` | `1670:30247` |
| Dashboard / product chrome — the rail mark | `gushwork-logo-(internal-use)` | `2102:13508` |

Never use the internal-use tile on a marketing surface. Never use the marketing logo
as the dashboard rail mark.

### Marketing — `gushwork-logo`

**40 variants** (complete).

| Property | Values |
|---|---|
| `Size` | `16 px`, `20 px`, `24 px`, `40 px`, `80 px` — **note the space before `px`** |
| `Type` | `Original`, `White`, `Dark`, `Blue Icon + White text` |
| `Only Symbol` | `yes`, `no` |

The variant keys carry a space (`16 px`). The rule prose writes them without one
(`16px`). Copying sizes out of the prose produces keys Figma will not resolve — use
the keys above.

**Pick `Size` by context, at a step.** Never render below `16 px` and never at an
in-between size.

**Pick `Type` by background:**

| Type | When |
|---|---|
| `Original` | Blue icon + dark wordmark. **The default.** All white and light backgrounds. |
| `White` | Dark backgrounds. The default choice for dark surfaces. |
| `Dark` | Near-black icon + wordmark. When brand blue can't be used or is being avoided — monochrome and single-colour contexts. |
| `Blue Icon + White text` | Dark backgrounds, **only when asked**. The alternative to `White`. |

**`Only Symbol = yes`** gives the icon-only mark with no wordmark. Use where space is
tight or the wordmark would be redundant.

### Committed assets — use these, never redraw the mark

| File | Variant |
|---|---|
| `assets/logo/gushwork-logo-original.svg` | `Type=Original` lockup — blue symbol + dark wordmark |
| `assets/logo/gushwork-logo-white.svg` | `Type=White` lockup |
| `assets/logo/gushwork-logo-dark.svg` | `Type=Dark` lockup |
| `assets/logo/gushwork-symbol-original.svg` | `Only Symbol=yes`, blue |

Exported from Figma at `Size=80 px` and stripped of the swatch-frame chrome Figma bakes
into a node export. They carry a `viewBox` and no fixed width/height, so scale them with
CSS to the `Size` step you need.

**The wordmark's dark is `#111827` — that is `--gw-color-secondary-500`,** the file's
single-step Secondary, and the same value the legacy `gray/900` variable carries. It is
deliberately *not* `--gw-color-neutral-900` (`#262a2e`) or `--gw-color-black` (`#0d0d0d`).
The blue symbol is `#0070ff` — `--gw-color-primary-500`.

### Dashboard — `gushwork-logo-(internal-use)`

A fixed **32×32** tile, radius 8, padding 8, wrapping
`gushwork-logo (Size=16 px, Type=White, Only Symbol=yes)`. No variants, no choices.
It is the rail mark in `dashboard-build` and nothing else.

**Conflict to be aware of:** 32px is exactly an in-between size, which the marketing
logo's own rule forbids. The internal-use tile is therefore forbidden by the shared
rule while simultaneously being the mandated dashboard asset. Two components, two
scopes — the rule text just doesn't say so. Follow the "which one?" table above.

### Never

- Redraw, recolour, restretch, or rebuild the logo. Use the component.
- Place `Original` on a dark surface or `White` on a light one.
- Add a tagline, container, or effect the component doesn't have.

---

## Icons — Phosphor

The icon library is Phosphor, published into the file as **1,248 component sets**, each
with the same matrix:

| Property | Values |
|---|---|
| `Weight` | `Thin`, `Light`, `Regular`, `Bold`, `Fill`, `Duotone` |
| `Size` | `12`, `16`, `20`, `24`, `28`, `32`, `36`, `40` |

48 variants per icon. Plus a `Social Icons` set (`228:2205`) covering 26 platforms in
`Original` and `Negative` at `Size=32`.

The icon group carries **no weight or size guidance** in Figma — its description says
nothing about which of the 48 to use. The conventions below are drawn from how the
components actually instance icons, and are the defaults to follow:

- **`Regular`** for inline and navigational icons.
- **`Bold`** inside buttons and for the small icon tiles in dashboard section headers.
- **`Fill`** for filled glyphs — a badge glyph, a caret in a dropdown trigger.
- Colour via `currentColor` only. Never hardcode an icon fill.

### Committed icon assets

Icons live in `assets/icons/`, exported from Figma at `Weight=Regular, Size=24`, chrome
stripped, with the baked `#0D0D0D` fill rewritten to `fill="currentColor"` so they inherit
text colour. Size them in CSS; the `viewBox` is `0 0 24 24`.

| File | Figma set | Used by |
|---|---|---|
| `caret-down.svg` | `112:4354` | dropdown triggers, section collapse, nav dropdowns |
| `arrow-up-right.svg` | `112:4802` | button `Trailing` icon, the CTA arrow |

**This is a partial harvest.** The following are instanced by components but not yet
exported — treat a missing file as a finding, not a licence to substitute a Unicode
character or draw a shape:

`Target` (`112:13686`) · `ArrowClockwise` (`112:5600`) · `ChartLine` · `DotsThree` ·
`DotsThreeOutlineVertical` · `ArrowsDownUp` · `Plus` · `Star` · `ArrowCounterClockwise`

**Never substitute a text glyph for an icon.** `⌄` is not `CaretDown`, `⟳` is not
`ArrowClockwise`, `⋮` is not `DotsThreeOutlineVertical`. If the asset isn't in
`assets/icons/`, say so.
- Match `Size` to the surrounding text: `16` beside 14px text, `20` beside 16–18px,
  `32` for the kpi-card header icon.

### Never

- **No emoji, ever** — not as bullets, decoration, or status. If you need a status
  signal, use a Badge or a Phosphor icon.
- **No bare coloured status dots.** Use a Badge.
- Do not draw an icon by hand. If Phosphor doesn't have it, that is a finding.

### Notes on the source

- Three sets are still named `component_set-element` — `112:12523`, `112:12537`,
  `112:17221`. Figma placeholder names, so they are unsearchable by icon name.
- All 20 icon category labels bind the legacy `paragraph-01/P1Regular` type variable
  rather than a `Body/*` token.
- Two stray `Cloud` instances (`271:1054`, `271:1060`) sit loose in the set grid and
  bind the legacy `gray/900`.

---

## What is *not* shared, despite appearances

The `shared-components` page in Figma (`1658:23895`) contains a plain text layer
(`1658:24152`) listing eleven intended shared components:

> Badge · Avatar · Icon Button · Chip · Divider · Tooltip · Spinner · Progress ·
> Skeleton · Tag · Status Indicator

**None of them is implemented on that page.** It is aspirational scaffolding. The one
component that *is* there — `gushwork-logo` — is not in the list. Of the eleven,
`Badge` and `Tooltip` exist on the web page; the rest do not exist anywhere in the
file.

If a request needs an Icon Button, Chip, Divider, Spinner, Progress, Skeleton, Tag, or
Status Indicator as a shared atom: **it does not exist yet.** Do not build one. Fall
back — see the out-of-scope section in either skill.
