# Dashboard component sheet v2 — new elements and deviations

Built 13 Aug 2026. Files: `exports/dashboard/v2/*.md`, `skills/gushwork-dashboard/SKILL.md`,
`preview/review-sheet.html`, `DECISIONS.md` (R14–R16), deprecation banners on
`exports/dashboard/{button,controls,section-elements,sections,states,toast}.md`.

Figma: **GW Dashbords** `Q9L6q38dEj3Qu1JkjiT13y`, page `Dashboard Components` `257:371`.
**24 component sets + 3 components = 132 variants.**

**Rendered on the review sheet** under `03 · Dashboard — v2 component sheet`, filed by group with
node IDs in every header — 93 specimens, real Phosphor glyphs from `assets/icons`. Verified
**numerically, not by eye**: 45 assertions comparing each rendered width, height, radius, padding
and fill against the measured value, **45 passed**. Two defects were caught that way and fixed —
fixed-width specimens were being compressed by the grid cell, and `icon-toggle-group` rendered 68
instead of 66 because CSS puts a border outside the box where Figma insets it.

**Not rendered:** hover, focus and disabled states (v2 defines hover only on `table-row`); the open
dropdown menu; `Graph`, which v2 does not cover; and the full five-column table width. Specimens
drawn narrower than the component say so in their own note.

## Why this happened

The dashboard screens in GW Dashbords were built by **detaching library components and overriding
them** — `list-item` detached **34 times** across nine sizes to serve as button, select, icon
button, pagination arrow, nav row and user card; `controls/tab` detached **11 times** with two
different container specs. 277 library instances, **zero components** built for the dashboard, and
no local variable collection.

The library's own dashboard components did not match what shipped: `Button` 28/44h `radius/8` gap 8
against the screens' 36h `radius/12` gap 4; `controls/dropdown` on `neutral/50` against white +
`neutral/400`; `table-row` 44h with 14/20 text against 56h with 12/16. Utsav ruled the **screens
authoritative** on 13 Aug 2026, component by component.

Everything below was measured from node properties — paddings, gaps, radii, strokes, type — not
from annotations and not from screenshots.

## Created — no library equivalent existed

### `input` — `Type=text｜search` × `State=placeholder｜filled｜focus`
The dashboard has **no text input of any kind**. Built from the `select` outlined spec so it sits
in the same family: 240 × 36, `radius/8`, `py-8 px-12`, white + 1px `neutral/400`,
`button-14-med`. `focus` swaps the border to `neutral/black` and shows a 1 × 16 caret.
`foundation/text-field.md` remains the shared atom for **forms**; this is the dense inline field.

### `tooltip` — `Theme=light｜dark`
The charts render an inline tooltip; no component existed. `radius/8`, `py-8 px-12`,
`body-12-med`, 10 × 6 arrow. `Theme=light` is the inverted one — `neutral/900` bubble, white text.

### `modal` — `Theme=light｜dark`
No dialog existed anywhere in the system. 480 wide, `radius/16`, pad `spacing/24`, gap
`spacing/16`, `Shadows/S2`. Header + body + right-aligned plain/primary footer.
**No scrim** — there is no scrim token, so a backdrop is a gap rather than a value to invent.

### `empty-state` — `Theme=light｜dark`
`states.md` ruled empty states as "compose from `section/Container`" on 7 Aug. This turns that
ruling into a component: 480 wide, pad `spacing/40`, a 40px `radius/full` icon circle,
`body-16-sem` title, `body-12-med` body, optional primary action.

### `skeleton` — `Type=line｜title｜block` × `Theme`
The loading screen implies a skeleton pattern; none existed. `neutral/100` / `neutral/800`.
**No shimmer animation is defined** — a gap.

### `sidebar` `State=collapsed`
The collapse chevron (`CaretDoubleLeft`) existed in the screens; **the collapsed state was never
designed.** Built at **64 wide** with 32 × 32 icon cells at `radius/8`, labels and group headers
hidden, footer showing the avatar only, chevron flipped to `CaretDoubleRight`. The 64 is a
judgement call.

### Also created, replacing loose frames rather than components
`status-dot` · `divider` · `checkbox` · `card-shell` · `legend` · `table-cell` · `icon-button` ·
`page-header` · `section-header` · `pagination` · `topbar` · `icon-toggle-group` — each of these
existed in the screens only as unnamed `Frame 2147260xxx` groups.

## Modified — deviations from measured v1 values

Each is a case where the library component and the screens disagreed and the screens won.

| Component | Measured v1 | v2 | Still reachable? |
|---|---|---|---|
| `Button` | 28/44/48h, `radius/8`, gap 8 | **36h, `radius/12`, gap 4** | yes — v1 set is still published |
| `controls/tab` | 28h, `radius/8`, gap 8 | **36h, `radius/12`, gap 4** | yes |
| `controls/dropdown` | `neutral/50` fill + `neutral/50` stroke, `p-8` | **white + `neutral/400`** outlined; `neutral/25` + `neutral/200` filled; `py-8 px-12` | yes |
| `table-row` data | 44h, white fill, 14/20 | **56h, no fill, 12/16** | yes |
| `table-row` header | `neutral/50`, `neutral/200` border | **`neutral/25`, `neutral/100` border** | yes |
| `table-row` `Selected` | `neutral/25` — same as Hover | **`primary/alpha-10`** | ⚠ overturns a v1 ruling |
| `kpi-card` | 286 × 198, pad 20, gap 80 | **218 × 132, pad 12, gap 16** | yes |
| `analytics-card` | 160 × 94, `neutral/25`, no border | **274 × 124, pad 16, white + border** | yes |
| `user-card` | 228 × 48, `radius/12`, Avatar **42.7 × 32** | **200 × 32, `radius/8`, Avatar 32 × 32** | Avatar squash is a library defect |
| `section/header` | one 1164 × 146, 32px `h5` | **two** — `page-header` 1120 × 113 (44px) + `section-header` 1120 × 24 | yes |
| Rail width | **260** (`dashboard-build`) | `sidebar` **240** | both real — two different shells, do not mix |
| Topbar vertical pad | raw **14px** | centred on a fixed 60h | identical result, on-token |
| Table header columns | 160 / 160 / 137.3 × 3 | equal **FILL** (146) | set the first two to 160 FIXED to match |
| Status dot | 8px and 12px both present | **8px only** — both 12px instances were hidden | — |
| Header label | `channnel` (typo, lowercase) | **`CHANNEL`**, uppercase | — |
| Table dead cells | hidden `SPEND (USD $)` / `ROI` in every row | dropped | — |

**Corrections to earlier reporting in this same piece of work:** two findings I filed were wrong
and are withdrawn. `Radius/16` **already exists** in the `Brand` collection (the screens used a raw
16); `Body/body-10-sem` **already exists** at exactly 10/15 Semi Bold. Both had appeared missing
because only the variables *used on the inspected page* were read. Nothing new was created for
either. Likewise, the table header and body rows were reported as structurally misaligned — they
are not; the differing child order involves only **hidden** cells, which take no auto-layout space.

## Worth a decision

**1. The display type ramp has no tokens, and this will silently produce wrong output.**
Five styles were created for this sheet — `Dashboard/display-44-sem`, `-36-med`, `-28-med`,
`-22-med`, `-20-sem`. **None maps to a `--gw-text-*` custom property.** `h3` is 44 **Bold** where
the page title is Semibold; `h7` is 22 at line-height **1.4** where the card title is 1.0 (~9px
per title). 36, 28 and 20 have no display step at all. Per `CONTRIBUTING.md` these are gaps to
raise in Figma, not lines to add to `tokens.css` — so until they are variables in the library,
every build must use a literal spec and comment it. **This is the item most likely to go wrong
quietly.**

**2. v2 lives in the product file and is unpublished — it inverts the repo's source-of-truth model.**
Every other file in `exports/` is traceable to a node in `VKcb4fgVyOHKfQonMgN772`. These 27
components live in `Q9L6q38dEj3Qu1JkjiT13y` and cannot be instanced from any other Figma file.
Fine for code generation; wrong for anyone told to find them in the Assets panel. **Promote into
the library, or accept the split and say so in the README.**

Secondary, in order:

- **`table-row` `Selected` overturns a v1 ruling.** v1 has `Selected` ≡ `Hover` ≡ `neutral/25`,
  with selection marked only by the checkbox. v2 uses `primary/alpha-10`. No selected row exists
  in the screens, so this is a ruling, not a measurement — and two tables in the wild will now
  disagree.
- **`toast` was duplicated with renamed properties.** The sheet copy is geometrically identical to
  the library set but keys `Tone` × `Theme` instead of `State` × `Mode`. Unrequested drift.
  Delete it or rename it; do not leave both.
- **Dark coverage is incomplete.** `table-row`, `icon-button`, `input` and `tab-group` have no
  `Theme=dark` variants despite being surface-bearing. `table-row` is the consequential one — dark
  values for it *are* measured (`neutral/black` rows on a `neutral/900` card).
- **No hover, focus or disabled states in v2.** Hover exists only on `table-row`. `button.md`'s
  measured hover fills and `states.md`'s focus ruling remain the only source for these.

## Closed 14 Aug 2026 — the open items above are done

| Was open | Now |
|---|---|
| No component properties | `Label` (TEXT) + `Leading icon` / `Trailing icon` (BOOLEAN) on `control`; `Label` on `badge` and `tab-item`; `Value` on `table-cell`; `Label`/`Value`/`Sub`/`Percent` on `stat-card`; `Label`/`Value`/`Sub` on `metric-card`; `Message` on `tooltip` |
| `table-row` had no dark variants | **14 variants** (7 × Theme). Rows on `neutral/black` inside a `neutral/900` card, borders and column divider `neutral/800` |
| `table-cell` had no `Theme` | **10 variants**. ⚠ Correction: dark header text is **`neutral/100`**, not the `neutral/400` first recorded |
| `icon-button` had no dark | **6 variants**. `Size=28`'s dark border is `neutral/700` — the chrome step, not the `neutral/800` card step |
| `input` had no dark | **12 variants**, **derived** from the measured dark select (the dark screen has no input) |
| `tab-group` / `icon-toggle-group` were single components | Both now variant sets with a measured `Theme=dark` |
| Duplicated `toast` | Keys realigned to the library's `Mode` × `State` and renamed `toast (local copy of the library set)`. **Not deleted** — the library's dashboard page is unpublished, so its set cannot be imported here; deleting would have left the section with no toast and no way to instance the real one |

**Sheet totals: 26 sets + 1 component = 155 variants** (was 24 + 3 = 132). **21 of 26 sets are
themed.** Per **R16**, only `status-dot`, `progress-bar`, `badge`, `divider` and `legend` inherit.

Every dark composite was then re-pointed at dark children — `topbar` → dark `icon-toggle-group`,
`page-header` → dark `tab-group`, `pagination` → dark `icon-button`s, `modal` → dark close,
`sidebar` → dark nav rows and user card. Audited: **no light child remains inside a dark parent,
0 broken instances, 0 unbound authored fills** (633 bound).

### Four bugs this pass introduced, all caught by auditing rather than looking

1. **Adding a TEXT property reset existing instance overrides to the property default.** 32 nested
   values across `table-row` and `sidebar` silently reverted to `681/706` and `Button`. All
   repaired, and the total row now carries real totals (`1310/1426`, `$808.98K`) rather than the
   data-row values it had. **If you add a property to an already-instanced set, re-check the
   instances.**
2. **Swapping an `icon-button` resets its glyph** to the component default `ArrowsClockwise` — the
   pagination arrows and the modal close briefly became refresh icons. Each swap now re-applies its
   glyph explicitly.
3. **The dark selected row replaced its base fill instead of layering.** `primary/alpha-10` alone
   composited to pale blue with unreadable text; it is now `neutral/black` **plus** the tint.
4. **Mutating while iterating `findAll*` invalidated the node ids** mid-loop. Ids are now resolved
   first, then mutated one at a time.

### Still open after this pass

- **Promotion into the published library** — unchanged; these still live in the product file.
- **The display ramp has no tokens (R15)** — unchanged; needs a library variable, not a local style.
- **`table-row` `selected` still departs from v1**, where `Selected` ≡ `Hover` ≡ `neutral/25`.
- **`review-sheet.html` renders the light theme only.** The dark variants exist in Figma but are not
  drawn on the HTML sheet; its v2 page carries a note saying so. Rendering them is a further pass.

## Tokens

**No new colour, type, radius, shadow or spacing value was introduced.** Of 515 painted fills
across the sheet, **zero are unbound** on any authored node; the only unbound paints sit inside
imported library instances (`Avatar`, Phosphor icons).

One class of defect was found and fixed during the build: 82 `createAutoLayout` wrapper frames
carried Figma's **default white fill**, which would have painted white blocks inside every dark
variant. All cleared.

Colour — `neutral/{white,25,50,100,200,300,400,500,600,700,800,900,black}` ·
`green/{25,50,300,400,500,100}` · `yellow/{25,50,400,500,100}` · `red/{25,50,300,400,500,100}` ·
`primary/{500-main,100,alpha-10}`
Radius — `radius/{4,8,12,16,20,40,full}` · Spacing — `spacing/{2,4,8,12,16,20,24,32,40}`
Type — `body-{12-med,12-sem,14-med,16-reg,16-sem}` · `button-{10-med,12-med,14-med}` ·
`body-10-sem` · Effect — `Shadows/S2`

**Values in use with no token — gaps to raise, not inventions:**

| Gap | Where |
|---|---|
| Display ramp 44-sem / 36-med / 28-med / 22-med / 20-sem | every page and card title |
| No scrim / overlay token | `modal` |
| No shimmer motion token | `skeleton` |
| No disabled state for pagination arrows | `pagination` on page 1 |
| No tooltip pointer positions (top/left/right) | `tooltip` |
| Collapsed sidebar width (64) | `sidebar State=collapsed` — chosen, not measured |
