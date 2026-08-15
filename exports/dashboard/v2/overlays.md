# Overlays — ring, dashboard-switcher, date-range-picker

Measured 14–15 Aug 2026 while building `preview/gtm-command-center.html`. Sources: `overview`
236:31785, `sidebar` 236:31801, and `lodaing` **409:11644** — the second loading frame, which is
where both dropdowns live. Everything here is measured unless a line says RULED.

The three components below did not exist in the v2 set. `ring` and `dashboard-switcher` were built
from a single frame each; `date-range-picker` is the largest component in the dashboard and had
never been specified anywhere.

---

## `ring` — the circular progress indicator

`Frame 2147260134`, 20×20, `cornerRadius 50`, holding **two** `ELLIPSE` nodes.

| | Track | Progress |
|---|---|---|
| size | 20×20 | 20×20 |
| `arcData.innerRadius` | **0.8** | **0.8** |
| `arcData` sweep | `0 → 2pi` | `1.5pi → …` |
| stroke weight / align | 5 / `INSIDE` | 5 / `INSIDE` |

### The band is 2px, and it does not come from `strokeWeight`

**`innerRadius 0.8` on a 20px ellipse means the annulus runs r=8 → r=10 — a 2px band.** The 5px
`INSIDE` stroke sits on a shape that is only 2px thick, so it cannot widen it. Reading the 5 as the
band width draws it **2.5× too heavy**, which is exactly what shipped and got reported.

In CSS: an SVG circle at **`r=9` with `stroke-width=2`**, so the outer edge lands at the measured
r=10. Sweep starts at the top — `transform="rotate(-90 …)"` — and runs clockwise.

### Two placements, two track colours

| Where | Track | Progress | Sweep |
|---|---|---|---|
| `page-header`, beside `Day 18 of 30` | `Colors/Neutral/200` | `Colors/Primary/500-main` | `1.500pi → 2.700pi` = **60%** |
| `metric-card` sub-line | **`Colors/Neutral/100`** | `Colors/Green/400` | e.g. `1.500pi → 3.340pi` |

The run-rate ring sits in `Frame 2147260133`, `AL:H gap 4`, cross-axis `CENTER`, after the
`need N / biz day` text.

> The design's own sweeps are approximate — `Demos` measures 92% against a computed 89%. The build
> computes them from the numbers rather than tracing the arcs.

---

## `dashboard-switcher` — the topbar title menu

`dropdown-options` in 409:11644. Opened by the `24×24 r4` caret button after the title
(`CaretDown`, `Weight=Bold, Size=16`).

| | |
|---|---|
| menu | **207×102**, `AL:V gap 4 pad 4`, `r8`, `Colors/Neutral/white`, 1px `Colors/Neutral/50` `INSIDE`, `DROP_SHADOW` |
| row | **197×28**, `AL:H gap 8 pad 8`, `r4` |
| row hovered | fill `Colors/Neutral/50` |
| label | 12px, `Colors/Neutral/900` |
| options | `Meta Performance Dashboard` · `Cold Email Dashboard` · `Onboarding Dashboard` |

### `strokesIncludedInLayout: true` — the stroke is layout here, not paint

207 wide with `pad 4` yields **197**-wide rows, not 199, even though the rows are `FILL`; and the
frame hugs to **102** for 100 of content. Both are the 1px `INSIDE` stroke participating in layout,
because this frame sets `strokesIncludedInLayout: true`.

Build it with a real `border` under `border-box`. The picker below sets the same property **false**,
so there an inset shadow is correct. See the rule at the bottom of this file.

---

## `date-range-picker`

`date-range-dropdown` in 409:11644 — **560×420**, `r12`, `Colors/Neutral/white`, 1px
`Colors/Neutral/50`, `DROP_SHADOW`. Opened by the `Custom` date tab.

```
560 × 420
├── main-content-split      560 × 360   AL:H, c:MIN          ← the right pane does NOT stretch
│   ├── left-presets-pane   228 × 360   right border Neutral/50
│   │   └── presets-list    228 × 360   AL:V gap 2, pad 12/8/8/8
│   │       └── preset-item 212 × 36    AL:H pad 8/16, r4
│   └── right-calendar-pane 332 × 320   AL:V gap 16, pad 16
│       ├── inputs-header-row 300 × 36  AL:H gap 8, c:CENTER
│       ├── weekday-headers   300 × 16  7 cells, 36 wide
│       ├── Line              300       1.5px Neutral/50
│       └── calendars-stack   300 × 188 AL:V gap 20      ← scrolls
└── footer-action-bar       560 × 60    AL:H gap 8, pad 12/20, m:MAX
```

### Presets

Nine rows, in order: `Custom` · `Last 7 days` · `Last week (Sun - Sat)` · `Last 14 days` ·
`Last 28 days` · **`Last 30 days`** · `Last 90 days` · `Quarter to date` · `Last 12 months`.
Label 14px `Colors/Neutral/900`; the selected row carries a `Colors/Neutral/50` fill.

Nine 36px rows + eight 2px gaps + 12/8 padding = **exactly 360**. The list does not scroll.

### Date fields

`136 × 36`, `r8`, fill `Colors/Neutral/25`, 1px `Colors/Neutral/200`, `pad 8/12`, label 14px
`Colors/Neutral/900`. Separator `to` at 12px `Colors/Neutral/400`.

### Calendar

| | |
|---|---|
| month title | 12px `Colors/Neutral/500`, e.g. `JUL 2026` |
| weekday letters | 12px `Colors/Neutral/400` |
| day row | 300 × 32, `pad 2/0` |
| day cell | 36 × 28, label 12px `Colors/Neutral/900` |
| in-range fill | `Colors/Neutral/50` |
| endpoints | 28px black pills |
| scrollbar thumb | `Frame 2147260244` — 4 × 69, `r20`, `#bbbec4` = **`Colors/Neutral/300`** |

### The range band is contiguous — do not build it with `space-between`

Figma **merges consecutive in-range cells into one wrapper**. Row 4 of the measured frame is a
single **300-wide** fill; row 3's is **149**, which is 3.5 columns of 300/7 — so the band starts at
the *centre* of the start pill and covers the inter-cell space.

Seven 36px cells in a 300 row with `space-between` leaves 48px spread as six 8px gaps, and the band
renders as **strips**. Build the row as seven contiguous `1fr` columns; give each endpoint a
half-column band on its inner side and draw the pill as an overlay above it.

### Footer

`m:MAX` — the buttons are **right**-aligned. `Cancel` 71×36 `r12`, label `Colors/Neutral/black`.
`Apply` 63×36 `r12`, `Colors/Neutral/black` fill **and** stroke, white label.

### Not in the source

- **No dark frame exists for this component.** Every dark value in the build is RULED.
- The endpoint pill is merged into the range wrapper, so its 28px diameter is read off the rendered
  frame, not an isolated node.
- The frame draws `Last 30 days` selected while showing **Jul 15–31** — seventeen days. Reproduce
  the opening state as drawn; compute on interaction.
- `calendars-stack` is a vertical stack with a scrollbar thumb, so the design anticipates **more
  than one month**. Only `JUL 2026` is drawn. The build renders Aug 2025 → Jul 2026 so that
  `Last 90 days` and `Last 12 months` have a real start pill — that span is RULED.

---

## `tooltip` — correction to `feedback.md`

Measured from the component set `282:727`, both variants:

| | `Theme=light` | `Theme=dark` |
|---|---|---|
| bubble | **`Colors/Neutral/900`** | `Colors/Neutral/white` |
| label | `Colors/Neutral/white` | `Colors/Neutral/900` |
| radius | 8 | 8 |
| padding | 8 / 12 | 8 / 12 |
| type | `Body/body-12-med` | `Body/body-12-med` |
| arrow | `POLYGON` 10 × 6, bubble fill | same |

**The light bubble is `Neutral/900`, not black.** Binding it to an invert alias
(`--s-invert` = `Neutral/black`) is one step too dark.

---

## The rule this file exists to record

**`strokesIncludedInLayout` decides whether a stroke is layout or paint. Read the property.**

| | `dashboard-switcher` | `date-range-picker` |
|---|---|---|
| `strokesIncludedInLayout` | **`true`** | **`false`** |
| sizing | width FIXED, height HUG | width FIXED, height HUG |
| 1px `INSIDE` stroke | eats FILL width (rows **197**, not 199) and adds to the hug (**102** for 100) | no effect — panes still 228 + 332 = **560** |
| CSS | `border` under `border-box` | **inset box-shadow** |

The two frames have *identical* sizing and opposite results, so the sizing mode cannot be the
cause. An earlier pass recorded this as "INSIDE consumes on HUG, not on FIXED" — that fits the
numbers and is wrong, and a component built from it reproduced neither frame. Getting it backwards
puts every measurement 2px out.
