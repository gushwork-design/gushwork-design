# Page shell — Page Build, navbar, footer, announcement banner

Figma: `↳ web/ pattern-library`. Worked examples on `↳ web/ template-library` (`1658:24579`).

The top of the web ladder. **Page Build** assembles a complete page; **navbar** and
**footer** are its fixed top and bottom.

---

## `page-build`

Group `1948:8116` · set `1735:61598` · **8 variants**.

| Property | Values | Default |
|---|---|---|
| `Breakpoint` | `Desktop`, `Phone` | `Desktop` |
| `Type` | `Brand`, `Ads` | `Brand` |
| `Blank` | `no`, `yes` | `no` |

| Boolean | Default |
|---|---|
| `Show extra-container-1` (`1835:18`) | `false` |
| `Show extra-container-2` (`1835:27`) | `false` |

**Reach for Page Build to build a complete page rather than placing sections loose.**

### Fixed vertical order — do not rearrange

```
navbar/navbar                      Brand → full nav links · Ads → single CTA button
└── content
    ├── fold/ Hero                 headline, description, CTA buttons, demo image
    ├── extra-container-1          SLOT — hidden by default
    ├── below-fold content frame
    │   └── container              SLOT — where the rest of the folds go
    └── extra-container-2          SLOT — hidden by default
footer/footer                      Brand → full footer (CTA + links) · Ads → copyright line
```

### `Type` is the governing axis

**`Brand` for main-website pages, `Ads` for paid-ad landing pages.**

**Set it once at the page level and let components inherit.** It drives the downstream
button rule — `Brand` → `Black` primary, `Ads` → `Blue` primary — and switches the navbar
and footer to their stripped variants. See `button.md`.

### `Blank`

`Blank=yes` gives an empty canvas — navbar + footer + one full-page `content` slot — to
compose freely. `Blank=no` gives the pre-composed hero + folds.

The rule marks this with `[confirm Blank property exists]`. **It does exist**, with values
`no` | `yes`.

### Slot properties — 10, with duplicate names

| Slot | Node | Purpose |
|---|---|---|
| `content` | `1735:25` | Full-page slot, used in `Blank=yes` variants |
| `container` | `1735:53` | Inner content slot within the fold section |
| `extra-container-1` | `1833:77` | Optional expandable section between hero and below-fold |
| `extra-container-2` | `1833:68` | Optional expandable section inside the below-fold area |
| `Slot2` | `1735:58` | undocumented |
| `Slot 2` | `1735:63` | undocumented — differs from `Slot2` only by a space |
| `container` | `1735:68` | second `container` |
| `container3` | `1735:73` | undocumented |
| `content` | `1833:50` | second `content` |
| `content` | `1833:59` | third `content` |

The structure blob says `Slot Properties (~10)` and then documents only 3. The four named
above are the ones with documented purposes; the rest are duplicates and leftovers. Use the
documented four.

### How to choose

Pick the layout by the requirement, page type, and intent. Ad page → `Type=Ads`. **Use the
extra containers only when the page needs sections beyond the default hero + below-fold.**

---

## Worked example compositions

Two `page-build` instances on the template-library page. Use them as reference orders.

**Short page — `1833:102537`** (1440×3785):

```
navbar/navbar
content
├── fold/ Hero
├── extra-container-1        [hidden]
└── below-fold
    └── container
        ├── fold/ Testimonial
        ├── fold/ Video
        └── fold/ With image      → heading + Button [hidden] + image Slot
    extra-container-2        [hidden]
footer/footer
```

**Long page — `1735:75169`** (1440×10259) — same shell, `container` holds:

```
fold/ Testimonial
fold/ With image
fold/ With image
fold/ Cards Grid
fold/ Cards Grid              (3-up × 2 rows of Card / Information)
fold/Timeline
fold/ Cards Grid (small)
fold/ Cards Grid
fold/ Testimonial             (1 wide + 2 narrow Card / Testimonial)
fold/ CTA
fold/ FAQs
```

Both hide `extra-container-1` and `extra-container-2`. Every in-fold `Button` is hidden —
fold CTAs are opt-in via `Show CTA`. Every `fold - stacked` mobile fallback is hidden on
the desktop variant.

Layout figures: page 1440 wide; content column **1240**, centred with 100px side margins;
the below-fold frame insets 16px to 1408, then the `container` slot insets to 1240 at
84/120.

**The `0:xxxx` node ids inside these instances are component-internal and not addressable**
by any Figma tool. They are only readable as part of the parent instance.

---

## `navbar/navbar`

Group `1951:8085` · set `1706:1799` · **8 variants**.

| Property | Values | Default |
|---|---|---|
| `Breakpoint` | `Desktop`, `Phone` | `Desktop` |
| `State` | `Default`, `Expanded`, `Collapsed`, `Menu`, `Platform Submenu`, `Solutions Submenu` | `Default` |
| `Type` | `Brand`, `Ads` | `Brand` |

| # | Breakpoint | State | Type | Size |
|---|---|---|---|---|
| 1 | Desktop | `Default` | Brand | 1440 × 60 |
| 2 | Desktop | `Expanded` | Brand | 1440 × 60 |
| 3 | Phone | `Collapsed` | Brand | 375 × 60 |
| 4 | Phone | `Menu` | Brand | 375 × 800 |
| 5 | Phone | `Platform Submenu` | Brand | 375 × 947 |
| 6 | Phone | `Solutions Submenu` | Brand | 375 × 800 |
| 7 | Desktop | `Default` | Ads | 1440 × 60 |
| 8 | Phone | `Collapsed` | Ads | 375 × 60 |

**Bar height is 60px at both breakpoints.** Menu and submenu overlays are taller.

### `Type`

- **`Brand`** — full nav plus a **black** `Book a Demo` CTA. Main-website pages.
- **`Ads`** — logo + **blue** `Book a Demo` only. No nav links, no hamburger. Ad landing
  pages.

**`Ads` has no menu states** — Desktop `Default` and Phone `Collapsed` only.

### Appearance — from design context (`1706:1677`, Desktop/Default/Brand)

| Part | Value |
|---|---|
| bar | `--gw-color-neutral-25` fill · **1px bottom border `--gw-color-neutral-100`** · h 60 · w 1440 |
| inner | `max-width: 1240` · `justify-content: space-between` · flex-1 |
| logo | `gushwork-logo` `Size=24 px, Type=Original, Only Symbol=no` · h 24 · internal gap **4.8px** |
| nav group | gap `--gw-space-32` |
| nav item | **a `Button` instance**, not a text link — h 36 · `8px 12px` · `--gw-radius-8` · `--gw-text-button-14` · `--gw-color-black` |
| caret | 16px, inside the nav-item button |
| CTA | `Button` · `--gw-color-black` fill · h 36 · `8px 12px` · `--gw-radius-8` · gap `--gw-space-8` · label white `--gw-text-button-14` · `ArrowUpRight` **16px** |

Five things here are easy to get wrong and were wrong in an earlier pass of this repo:

1. **The bar has a bottom border.** `1px solid --gw-color-neutral-100`. Not just a fill.
2. **Nav items are `Button` instances**, styled as `Text/ black` at `Small` — they carry the
   button's own 36px height, 8/12 padding and `--gw-radius-8`. Rendering them as bare
   `<a>` text loses the hit area and the hover surface.
3. **The CTA's trailing icon is 16px, not 18.** 18px is the standalone button's icon size;
   the navbar instance overrides it.
4. **The logo's internal gap is 4.8px** at `Size=24 px` — a scaled value, not a spacing
   token. The master spec says `itemSpacing: 6`, which is the value at a different size.
5. **`Who It’s For` uses a curly apostrophe** (U+2019), not `'`. It is a fixed nav label —
   copy it exactly.

### Anomaly — Platform and Solutions use different carets

`Platform` instances **`CaretDown`** (`112:4354`). `Solutions` instances **`CaretUp`**
(`112:4312`). Both sit in the same closed `State=Default` navbar, so both should point the
same way.

This is almost certainly a Figma slip — a caret left flipped after checking the open state.
**Render both as `CaretDown` when closed**, and flag it rather than reproducing it. Recorded
here so the next reader doesn't "fix" the export to match the file.

### Nav items — fixed set, don't add ad hoc

| Item | Type |
|---|---|
| `Who It's For` | plain link |
| `Platform ▾` | dropdown + submenu |
| `Solutions ▾` | dropdown + submenu |
| `Customers` | plain link |
| `Pricing` | plain link |

The mobile menu renders the first item as **`Who It's for`** (lowercase *for*) while the
four desktop instances use **`Who It's For`**. Use `Who It's For`.

### States

- **Desktop** — `Default` (bar only) / `Expanded` (a submenu is open).
- **Phone** — `Collapsed` (logo + hamburger) / `Menu` (full-screen overlay) /
  `Platform Submenu` / `Solutions Submenu` (drill-down views with a Back control).

### Submenu

`navbar/navbar-elements/submenu` (`1670:30166`) — `Property 1` [`platform`, `solutions`].
256×205, positioned at 738,52 on the Expanded desktop variant.
`navbar/navbar-elements/submenu-item` (`1658:27569`) — `State` [`Default`, `hover`] ·
instance-swap `Icon` (`1669:0`).

Solutions submenu content:

| Item | Description |
|---|---|
| `AI Search` | Get qualified leads from AI search engines. |
| `Lead Conversion` | Turn more visitors into qualified conversions. |
| `Paid Boost` | Generate qualified leads from paid campaigns. |

### Styling

Background is light gray `#F7F8F9` on every variant — `--gw-color-neutral-25`. Logo is a
`gushwork-logo` instance at `Size=24 px` on desktop, `Size=20 px` on phone. Desktop CTA is
inline; phone `Menu` CTA is full-width pinned to the bottom. Desktop CTA button is 135×36.

Icons used: `List` (hamburger), `X` (close), `CaretDown` (chevron), `ArrowRight`, `Sparkle`,
`ChartLine`, `Rocket`.

Note the navbar shadow comes from `shadows/button`, a lowercase collection separate from
`Shadows/*` — see `foundation/tokens.css`.

---

## `footer/footer` — a three-level nested system

```
footer/footer                              ← top-level, used in pages
└── footer/footer-elements/cta             ← the CTA banner
    └── footer/footer-elements/cta-image   ← the illustration panel
```

Each can be placed standalone, but in a page footer they nest. **`Breakpoint` propagates
down the whole nest.**

### `footer/footer` — set `1720:3801` · 6 variants

| Property | Values | Default |
|---|---|---|
| `Breakpoint` | `Desktop`, `Phone` | `Phone` |
| `Type` | `Brand`, `Ads` | `Brand` |
| `Show CTA` | `True`, `False` | `True` |

Boolean `Show Marquee` (`1720:63`) — default `true`.

#### Appearance — from design context (`1720:3798` Brand, `1720:3800` Ads)

| Part | Value |
|---|---|
| surface | `--gw-color-black` — **not** `neutral-900` |
| top corners | **`--gw-radius-20` on Brand · `--gw-radius-8` on Ads** — the two variants disagree |
| padding | `padding-top: --gw-space-80`, no bottom padding on the Brand variant |
| inner column | `max-width: 1240` · outer stack gap `--gw-space-80` |
| link columns | gap `--gw-space-60` between columns · `--gw-space-20` title-to-list · `--gw-space-12` between links |
| column title | `--gw-text-body-12-sem` · `--gw-color-neutral-200` |
| link | `--gw-text-body-14-med` · `--gw-color-neutral-400` |
| address block | width 600 · `--gw-text-body-12-reg` · `--gw-color-neutral-600` |
| divider | 1px full-width rule above the bottom row |
| copyright | `--gw-text-body-12-med` · `--gw-color-neutral-700` |
| legal links | `--gw-text-body-12-reg` · `--gw-color-neutral-600` · gap `--gw-space-24` |
| socials | 3 buttons, 28 wide, radius **7.226** (not a token), 14px glyphs, absolutely positioned 48px above the bottom row, right-aligned |
| marquee band | `agent-icon` 112 × 112, radius **14.933** + text at **112px Vert Grotesk Semibold**, `--gw-color-neutral-900`, gap `--gw-space-60`, repeated twice with a 12px dot at 80% opacity between |

`Ads` is the whole footer collapsed to one centred line: `padding: --gw-space-16`, copyright
only, `--gw-text-body-12-med` in `--gw-color-neutral-600`.

#### Real link content — use this, not placeholders

| Column | Links |
|---|---|
| Platform | Brand Memory · Page Creation Engine · AI-First CMS · Leads Dashboard · Analytics |
| Solutions | AI Search Agent · Lead Conversion · Paid Boost |
| Company | Pricing · Customers · Careers · Announcements · Alternatives |

Addresses: `Regents Inc, 16192 Coastal Hwy, Lewes, DE 19958, United States` ·
`Delfin Technologies India Pvt Ltd, 578, 9th A Main Rd, Indiranagar, Bengaluru, Karnataka
560038, India`. Phone `+1 (888) 451 5522`. Email `growth@gushwork.ai`.

#### Findings — five, all open

1. **Top-corner radius disagrees between variants** — 20px on Brand, 8px on Ads. Same
   component, same edge. One is wrong.
2. **The copyright reads `© 2025`.** Stale as of 2026. It is baked into the component, so it
   will ship stale unless overridden.
3. **Three strings break sentence case** — `All Rights Reserved`, `Terms Of Use`, and the
   marquee's CSS `text-transform: capitalize` which renders `Agents Working 24/7`. Per
   `foundation/voice.md` these should be `All rights reserved`, `Terms of use`, and
   `Agents working 24/7`. Write them corrected.
4. **The copyright fails contrast — RULED, build `--gw-color-neutral-400`.** `neutral-700`
   (`#535a61`) on `--gw-color-black` (`#0d0d0d`) is roughly **2.3:1**, against a 4.5:1 floor;
   the legal links at `neutral-600` are about **3.9:1**. Both fail. `neutral-400` `#959ba4`
   gives **~6.9:1** on black and **~5.1:1** on `neutral-900`, and is the only step that clears
   the floor on both dark surfaces. `DECISIONS.md` → **R9**. Contrast is a floor, not a
   preference — this overrides the measured value.
5. **`Solutions` names differ from the navbar.** The footer says `AI Search Agent`; the
   navbar submenu says `AI Search`. Same destination, two labels.

Two radii here are non-token values — `7.226` on the social buttons and `14.933` on the
marquee `agent-icon`. Both look like scaled artefacts rather than intent. Use the nearest
token (`--gw-radius-8`, `--gw-radius-16`) and note the substitution.

| Breakpoint | Type | Show CTA | Size |
|---|---|---|---|
| Phone | Brand | `True` | 375 × 1813 |
| Phone | Brand | `False` | 375 × 864 |
| Phone | Ads | `False` | 375 × 44 |
| Desktop | Brand | `True` | 1440 × 1024 |
| Desktop | Brand | `False` | 1440 × 568 |
| Desktop | Ads | `False` | 1440 × 44 |

**There is no `Ads` + `Show CTA=True` variant. Ads footers never show the CTA.**

- **`Brand`** — full footer: CTA banner + link columns (Product / Solutions / Company) +
  newsletter + socials + legal + marquee.
- **`Ads`** — minimal: a single copyright line. No CTA, links, socials, or marquee.

**`Show CTA=False`** (Brand only) hides the CTA banner; **links, socials, and marquee still
show.** That is different from the `Ads` collapse.

**`Show Marquee`** toggles the "Agents working 24/7" scrolling ticker. On by default.

Brand structure: nested `cta` instance (`Image=true, Description=true, Color=Blue`) → link
columns → newsletter (**desktop only**) with email input + Subscribe → socials (LinkedIn,
X, Instagram) → legal row `© 2025 Gushwork | All Rights Reserved` · Terms · Privacy →
marquee (`agent-icon` + "Agents working 24/7", infinite scroll).

The legal line hardcodes **2025**. Verify the year before shipping.

### `footer/footer-elements/cta` — set `1715:3476` · 16 variants

| Property | Values | Default |
|---|---|---|
| `Breakpoint` | `Desktop`, `Phone` | `Phone` |
| `Image` | `false`, `true` | `false` |
| `Description` | `false`, `true` | `false` |
| `Color` | `Blue`, `Black` | `Blue` |

| Boolean | Default | Toggles |
|---|---|---|
| `Secondary Button` | `true` | the `Calculate ROI with Gushwork` button |
| `Supportive Text` | `false` | small 12px helper text below the CTAs |

**Colour behaviour — follows the button rule:**

| `Color` | Background | Primary | Secondary |
|---|---|---|---|
| `Blue` | `#0070FF` | white-filled | white-stroke |
| `Black` | `#0D0D0D` | **blue-filled** | white-stroke |

Same as "blue is primary on black surfaces". `Blue` is the footer default.

Content: headline `Let Gushwork run your marketing team in the background.` · primary
`Book a Demo` with `ArrowUpRight` · secondary `Calculate ROI with Gushwork`.

**Use Secondary CTA only when asked. When Secondary CTA is used, do not use supportive
text.** Supportive text is centre-aligned on phone, left-aligned beside the button on
desktop.

### `footer/footer-elements/cta-image` — set `1712:2684` · 24 variants

| Property | Values | Default |
|---|---|---|
| `image` | `AI Agents`, `Testimonial`, `AI Search Engines`, `Lead Notification`, `Get Mentioned By AI`, `+ Create New` | `Testimonial` |
| `Breakpoint` | `Desktop`, `Phone` | `Desktop` |
| `Color` | `Blue`, `Black` | `Blue` |

Slot `container` (`1727:0`) on the `+ Create New` variant.

Desktop 600×440, Phone 343×393. `Blue` renders the pattern in blue tones on `#0070FF`;
`Black` in dark tones on `#0D0D0D`.

**Pick `image` by what the CTA promotes** — match by keyword the same way as the image
library. `image` is the illustration's *subject* and is distinct from footer `Type`.

Note the variant value is `Get Mentioned By AI` (Title Case) while the rendered label reads
`Get mentioned by AI` (sentence case). The label is right; the key is the key.

### `footer/footer-elements/list-item` — `1672:35328` · **broken**

Figma refuses to read this set: *"Component set has existing errors"*. Both variants are
named `Property 1=Default`. It is undocumented in the footer structure blob and its
properties cannot be recovered.

**Do not invent properties for it.** If you need footer link items, use the footer's own
link columns.

---

## `announcement-banner`

Group `1948:8100` · set `1942:9492` · **2 variants** · text property `Banner Text`
(`1942:0`), shipped value *"Bringing high-value B2B commerce to the agentic web."*

- **Sticky to the top of the page**, stays pinned as the page scrolls.
- **The entire banner is one clickable link** — the message and the
  `Read the announcement →` affordance go to the same place. **The close (×) is the only
  exception** — it dismisses and must not trigger the link.
- Content: one short message + `Read the announcement →` + the close (×).
- Desktop is a full-width strip, message centred, × pinned right. Phone is a compact inline
  pill.

**Dismissal persistence is undefined.** The rule leaves it open:
`[confirm: for the session, or permanently remembered?]`. Don't pick one.

---

## The Brand / Ads axis — one decision, four components

Set `Type` once on `page-build`; navbar, footer, and buttons all follow.

| | `Brand` | `Ads` |
|---|---|---|
| `page-build` | pre-composed hero + folds | same shell |
| `navbar` | 5 nav links + submenus, **black** CTA | logo + **blue** CTA only |
| `footer` | CTA + links + newsletter + socials + marquee | single copyright line |
| `Button` primary | `Black` | `Blue` |

**Naming caveat:** the page-build *rule* says "Ad type" / "Ad page" throughout, the
structure blob says "Ads type", and the actual variant value is **`Ads`**. The navbar rule
uses both in one sentence. Use `Ads`.

## Source notes

- The page-build structure blob (`2034:15029`) contains **no variant-property list at all** —
  `Breakpoint`, `Type`, and `Blank` are never named in it. The tables above come from the
  component set directly. It is also full of non-breaking spaces.
- `2089:23403`, `2034:15029`, and `2076:9858` contain **U+2028 LINE SEPARATOR** characters
  immediately after "Component Structure". These break the Figma MCP's serialization and are
  why whole-page metadata reads of this page fail.
- The footer rule and structure blob **contradict each other on the newsletter CTA**: the
  structure lists a `Book a demo` link; the rule says the link *is*
  `Book a call with our team` and merely "normalizes to" `Book a demo`. Write `Book a Demo`.
- **`Book a Demo`** (capital D) appears on all three phone bottom-CTA buttons in the navbar
  structure blob, alongside `Book a demo` for every desktop CTA. **The phone buttons are the
  correct ones** — `Book a Demo` is the ruled string, so the desktop CTAs are the outliers.
  See `foundation/voice.md`.
- `Breakpoint` defaults disagree across blobs: `Desktop` in the fold and navbar docs,
  `Phone` in the footer docs. Set it explicitly rather than relying on a default.
