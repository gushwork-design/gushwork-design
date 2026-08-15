# Dashboard components — v2 set

Measured 13 Aug 2026 from a purpose-built component sheet, not from annotations.

**Provenance is different from every other file in `exports/`.** These components live in the
**product** file, not the design system library:

| | |
|---|---|
| File | **GW Dashbords** — `Q9L6q38dEj3Qu1JkjiT13y` |
| Page | `Dashboard Components` — `257:371` |
| Root frame | `GW Dashboard Components` — `259:384` |
| Contents | **26 component sets + 1 component = 155 variants** |

They are **not published to Gush Design System v2.0**, so instances of them are only available
inside the GW Dashbords file. For code generation that does not matter — the measured values are
what you build from — but do not tell anyone they can drag these out of the Assets panel in a
different file. Promotion into the library is an open item; see the notice.

## Why this set exists

The dashboard screens in GW Dashbords were built by **detaching library components and
overriding them** — `list-item` detached 34 times into nine different jobs, `controls/tab`
detached 11 times with two different container specs. The library's own dashboard components
(`Button` 28/44h r8, `controls/dropdown` on `neutral/50`, `table-row` at 44h with 14/20 text)
**did not match what shipped**, which is why they were bypassed rather than used.

This set documents what the screens actually render. Where the library and the screens disagreed,
**the screens won** — ruled by Utsav, 13 Aug 2026.

## What this supersedes — and what it does not

Only the parts genuinely replaced. Everything else in `exports/dashboard/` stays authoritative.

| Old file | Status |
|---|---|
| `button.md` | **Superseded** by `controls.md` → `control` `Kind=button`. 28/44h r8 → **36h r12**, gap 8 → **4** |
| `controls.md` | **Partly superseded** — `controls/tab` → `tab-group` + `tab-item`; `controls/dropdown` → `control` `Kind=select`. **`controls/toggle` is unchanged and still current** |
| `section-elements.md` | **Partly superseded** — `kpi-card`/`analytics-card` → `stat-card`/`metric-card`; `table-row` → `table-row` + `table-cell`; `progress-bar` → `primitives.md`. **`Graph` is NOT covered here and remains authoritative in the old file** |
| `sections.md` | **Partly superseded** — `section/header` → `chrome.md` `section-header` + `page-header`; `section/Container` → `card-shell`. **The Sections composition ladder is unchanged** |
| `states.md` | **Partly superseded** — empty and loading now have real components (`feedback.md`). **The focus ruling is unchanged and still mandatory** |
| `toast.md` | **Still authoritative.** ⚠ But a *second* toast was built on the sheet with renamed properties (`Tone` × `Theme` instead of `State` × `Mode`) — unrequested drift. Use the library one; see `feedback.md` |
| `avatar.md` · `build-rules.md` · `dashboard-build.md` · `login-screen.md` | **Unchanged.** Untouched by this work |

## Files

| File | Components |
|---|---|
| `primitives.md` | `status-dot` · `progress-bar` · `badge` · `checkbox` · `divider` |
| `controls.md` | `control` (button/select/nav/user) · `icon-button` · `tab-item` · `tab-group` · `icon-toggle-group` · `input` |
| `data-table.md` | `table-cell` · `table-row` · `pagination` |
| `cards-and-chrome.md` | `stat-card` · `metric-card` · `card-shell` · `topbar` · `sidebar` · `page-header` · `section-header` · `legend` |
| `feedback.md` | `tooltip` · `modal` · `empty-state` · `skeleton` |
| `overlays.md` | `ring` · `dashboard-switcher` · `date-range-picker` — **added 15 Aug 2026**, plus a `tooltip` colour correction |

## Dark theme is variants, not a mode

The library's `Brand` collection has **one mode, `Gushwork`**. There is no dark mode in variables,
so the dark screens work by pointing each layer at a *different* token. This set encodes that as a
`Theme=light｜dark` variant on **surface-bearing components only** — anything with a fill or a
border. Ruled by Utsav, 13 Aug 2026.

Components with **no** `Theme` variant — `status-dot`, `progress-bar`, `badge`, `divider` and
`legend` — inherit, and their dark overrides are listed in each file. **Everything else is themed:**
21 of the 26 sets carry `Theme`, including `table-row`, `table-cell`, `icon-button`, `input`,
`tab-group` and `icon-toggle-group`, which were open items on 13 Aug and are now built.

Measured light → dark mapping:

| Surface | Light | Dark |
|---|---|---|
| Topbar / sidebar | `neutral/50` | `neutral/900` |
| Card fill | `neutral/white` | `neutral/900` |
| Card border | `neutral/100` | `neutral/800` |
| Table header row | `neutral/25` | `neutral/black` |
| Table body row | *no fill* | `neutral/black` |
| Row divider | `neutral/25` | `neutral/800` |
| Display headings | `neutral/black` | `neutral/white` |
| Card label | `neutral/700` | `neutral/400` |
| Sub / percentage text | `neutral/500` | `neutral/500` — **unchanged** |
| Progress track | `neutral/200` | `neutral/600` |
| Success / danger | `green/400` · `red/400` | `green/300` · `red/300` |
| Status dot | `green/400` | `green/400` — **unchanged** |
| Muted icon | `neutral/600` | `neutral/300` |

## Component properties

Added 14 Aug 2026. Overrides no longer depend on layer names alone:

| Set | Properties |
|---|---|
| `control` | `Label` (TEXT, 30/32 variants — the `user` kind has two texts so it is excluded) · `Leading icon` (BOOL, 22/32 — selects and the user card have none) · `Trailing icon` (BOOL, 28/32 — nav rows have none) |
| `badge` · `tab-item` | `Label` (TEXT) |
| `table-cell` | `Value` (TEXT, 8/10 — the two `status` variants hold a badge instance, not text) |
| `stat-card` | `Label` · `Value` · `Sub` · `Percent` (TEXT) |
| `metric-card` | `Label` · `Value` · `Sub` (TEXT) |
| `tooltip` | `Message` (TEXT) |

⚠ **Adding a TEXT property resets existing instance overrides to the property default.** Doing
this reverted 32 nested values across `table-row` and `sidebar` to `681/706` and `Button`. All were
repaired, but if you add a property to a set that is already instanced, re-check the instances.

## ⚠ Open gap — the display type ramp has no tokens

The dashboard's display type uses five styles created for this sheet, local to the product file.
**None of them maps to an existing `--gw-text-*` token**, so generated code has nothing correct to
reference. Per `CONTRIBUTING.md` this is a gap to raise in Figma, not lines to add to `tokens.css`.

| Style (local) | Spec | Nearest token | Why it does not match |
|---|---|---|---|
| `Dashboard/display-44-sem` | 44/120% Semibold 600 | `--gw-text-h3` | h3 is **700**, not 600 |
| `Dashboard/display-36-med` | 36/120% Medium 500 | — | no 36 step; h4 is 700 38px |
| `Dashboard/display-28-med` | 28/120% Medium 500 | — | no 28 step; h6 is 600 26px |
| `Dashboard/display-22-med` | 22/**100%** Medium 500 | `--gw-text-h7` | h7 is line-height **1.4**, not 1.0 |
| `Dashboard/display-20-sem` | 20/100% Semibold 600 | — | no 20 display step |

Until this is closed: **use the literal spec from the table above and comment that it has no
token.** Do not silently substitute `h3` or `h7` — the weight and line-height differences are
visible, and `h7`'s 1.4 line-height adds ~9px per card title.

Everything else in this set binds to real tokens. Of 515 painted fills across the sheet, **zero
are unbound** on any authored node; the only unbound paints are inside imported library instances
(`Avatar`, Phosphor icons).


---

## Corrections from the GTM Command Center build — 14–15 Aug 2026

Building `preview/gtm-command-center.html` against `overview` 236:31785, `sidebar` 236:31801 and
`lodaing` 409:11644 turned up measurements this set had wrong or missing. Full working in
`dashboard-component-audit.md` sections 10–11.

### Values corrected

| Component | Was | Measured |
|---|---|---|
| `ring` (new) | — | band is **2px** from `arcData.innerRadius 0.8`, not the 5px `strokeWeight` |
| `tooltip` light bubble | an invert alias → `Neutral/black` | **`Neutral/900`** |
| sidebar nav icons | a muted icon colour | **the same variable as their label** — all 11 bound to `Neutral/900` |
| topbar button glyphs | a muted icon colour | **the same variable as their label**, both buttons, both themes |
| `Sync Now` label, dark | white | **`Neutral/50`** |
| `Compare` | same treatment as `Sync Now` | **fill + stronger stroke**: white/`Neutral/400` light, `Neutral/800`/`Neutral/600` dark |
| theme toggle | both cells `r8`, muted inactive glyph | active **`r8`**, inactive **`r4`**; glyphs `Neutral/900`/white light, `Neutral/50`/black dark |
| sidebar footer divider | absent | a **per-side stroke** — `strokeTopWeight 1.5`, `Neutral/100` |
| sidebar nav column | one scrolling list | `SPACE_BETWEEN` over **two** blocks; Settings + Admin pin to the bottom |
| collapse control | 24×24 in a 32 row | **20×20** in a **28** row |
| chart grid / target dash | 3/4 and 6/6 | **4/4** and **12/4** |
| chart marker | one blue dot | **two** dots, 5×5, `Primary/500` on the curve and `Neutral/200` on the target |
| card-header subtext | stacked under the title | **`AL:HORIZONTAL` gap 12** |
| Channel Breakdown toolbar | a column-chooser icon button | a **`Showing for` select**, 116×32, `Neutral/400` stroke |
| badge tints, dark | green + amber kept their **light** `/25` solids (no dark override existed) | **`<Tone>/Alpha/10`** fill with a **`<Tone>/300`** label |

**This closes the `Compare` vs `Sync Now` dark-mode gap** recorded in `dashboard-component-audit.md`
section 9 — both are now measured rather than ruled.

### Things that were never in the source

Recorded so nobody hunts for them:

- **No dark frame for the date picker.** Every dark value in it is ruled.
- **No solid vertical marker in the chart.** All twelve line nodes are dashed gridlines; a
  "today" rule was invented by the build and removed.
- **The collapsed sidebar was never designed** (v1 judgement call, 64 wide). The rail tooltips,
  the stacked user card and the `Syncing` state are all build-side behaviour, not measurements.
- **`CHAN_COLS[0]` is `channnel`** — three n's, a typo in the frame, transcribed verbatim.

### Three inconsistencies inside the frames — reproduce, don't correct

1. Loading bar draws **210 of 400 = 52.5%** under a **`58%`** label.
2. Chart today-marker sits at **78%** while the page header reads `Day 18 of 30` (**60%**); the
   tooltip reads `Actual 1104 / Target 1235` against an axis topping out at **340**.
3. Date picker shows **`Last 30 days`** selected with a **Jul 15–31** range — seventeen days.

### Column labels are inconsistently cased in the frames

`DATE` · `Domain` · `assigned AE` · `channel` · `monthly` · `annual ARR` · `Status`, and
`channnel` · `demos` · `Show-ups` · `Pending` · `Closes` · `ARR`. Invisible in a table header
(CSS uppercases it) and glaring in a `Sort by` menu. Title-case for menus, keep acronyms whole
(`ARR`, `AE`, `ROI`), and leave the transcribed strings alone.


### Dark theme: declare every alias in both blocks

`--tone-good-bg` and `--tone-warn-bg` were declared only in `:root`, so green and amber badges
painted their **light** `/25` tints on a dark surface. An alias missing from the dark block does not
fail — it silently keeps the light value, which is why this survived several review passes.

Measured pattern, from `Behind` in `dark-mode` 236:33407:

| | light | dark |
|---|---|---|
| badge fill | `<Tone>/25` (`/50` at `md`) | **`<Tone>/Alpha/10`** |
| badge label | `<Tone>/500` | **`<Tone>/300`** |

`preview/_verify_gtm_command_center.py` now asserts that all six tone aliases appear twice.
