---
name: gushwork-dashboard
description: Builds Gushwork product and dashboard interfaces on-brand — dashboards, app screens, product UI, KPI cards, analytics panels, data tables, side navigation, section headers, filters, tabs, toggles, toasts, and user/account chrome. Use this whenever the request is a logged-in product surface for Gushwork: "build a dashboard", "add a KPI row", "a leads table", "an analytics screen", "the app's side nav", "a settings page". Not for marketing pages — use gushwork-web for landing pages, heroes, folds, and any public-facing site work.
---

# Gushwork dashboard

You are building a **logged-in product surface** for Gushwork. Dense, gray-canvas,
black-and-outline actions, blue reserved for signals. This is not the marketing site.

Announce at the start: "Using the Gushwork dashboard skill."

## Read these first

| For | Read |
|---|---|
| Every colour, size, radius, shadow, type style | `foundation/tokens.css` |
| Voice, casing, banned words, CTA copy | `foundation/voice.md` |
| Badge, Gushwork logo, Phosphor icons | `foundation/shared-components.md` |
| Declaring anything you had to build yourself | `foundation/new-component-notice.md` |
| Shell, scrolling, fill and responsive detail | `exports/dashboard/build-rules.md` |

**Never restate a token value or a voice rule here or in your output.** Reference the token.

Three tiers, because "never invent a number" is unfollowable for page layout and a rule
that can't be followed gets ignored where it matters:

1. **Colour, type, radius, shadow, spacing — always a token. No exceptions.** If one of
   these has no token, that is a finding to report, never a value to invent.
2. **Layout dimensions documented in `exports/`** — the 260 rail, 1164 container, 32px logo
   tile, 28px small button — use the documented figure exactly.
3. **A layout dimension with no documented figure**: choose sensibly, but **say in one line
   that you chose it.** Don't pass your own number off as coming from the system.

## Measuring a component — read the set, never an instance

Every value in `exports/dashboard/` is measured off Figma. When you add or correct one:

**Pull `get_design_context` on the component set, or on a variant symbol inside it — never
on an instance.** An instance read misreports type weight: instances inside
`dashboard-build` return `Inter:Bold` for text that the component set defines as
`Inter:Medium` or `Inter:Semi_Bold`. This shipped a wrong rail twice.

How to tell them apart in `get_metadata`: a `<symbol>` is a definition, an `<instance>` is a
use. Set nodes list `<symbol>` children, one per variant.

Two further checks worth doing every time, because each has caught a real error here:

- **Compare box geometry numerically**, not by screenshot. Read Figma's `x/y/w/h` from
  `get_metadata` and assert against `getBoundingClientRect()`. Eyeballing passed a rail that
  was 9px out per group.
- **Sample the render for colour.** `get_screenshot` then read the pixel. Annotation text
  does not carry fills, and inference is unreliable — a nav icon that "should" be muted grey
  is actually the same `neutral-900` as its label.

If an annotation and the component disagree, the component wins and the disagreement is a
finding. `dashboard-build`'s annotation claims `gap:8` where the coordinates prove 0.

## Before building a dashboard — ask, don't assume

A dashboard is a set of decisions about what matters. Guessing produces a screen that looks
right and answers nothing. **Unless the request already answers them, ask these first:**

1. **What are the KPIs?** Which one to three numbers is this screen accountable for? Those
   become the kpi-cards. Everything else is a supporting metric.
2. **What should someone see first?** The top of the slot is the most valuable space in the
   product. What belongs there decides the section order.
3. **What will they do with it?** Monitoring, diagnosing, or acting. Monitoring wants
   headline numbers and a trend. Diagnosing wants breakdowns and filters. Acting wants a
   table with row actions. The answer changes which Sections you reach for.
4. **How often does it change, and who looks at it?** Drives whether the header needs a
   refresh indicator, filters, or a date range at all.

Ask them in one short message and wait. Two or three questions answered beats a screen
rebuilt three times.

**If the user supplies a reference — a screenshot, a URL, an existing tool — read it for
CONTENT, never for layout.** Their KPIs, labels and data are the useful part. Their card
arrangement, colour choices and type scale are not, and importing them produces something
that looks Gushwork-ish while being off-system. Map the content onto the Sections below and
say what you changed.

## Choosing a `section/card-layout` variant

`KPI cards` is a real decision, not a default. **Pick by how many numbers genuinely lead.**

| Variant | Use when | Layout |
|---|---|---|
| `KPI cards=1` | One north-star metric. The strongest choice — one big number, six supports. | 1 KPI left + 6 analytics right |
| `KPI cards=2` | A natural pair — volume and cost, leads and conversion. | 2 KPIs left + 6 analytics right |
| `KPI cards=3` | Three genuinely co-equal headlines. | 3 KPIs on top + 6 analytics below |

**Reaching for `3` every time is the common failure.** If two of the three are supporting
detail, they belong in the analytics row and the variant is `1`. There is no variant above 3
— a fourth headline metric means the page is trying to do two jobs.

**Cards fill the section, they do not sit at their intrinsic width.** `card-layout` is 1084
wide (the 1164 container less its 40px slot padding). At `KPI cards=3` that is three cards at
356 and six analytics at 174. The 286 and 160 in `section-elements.md` are the components'
own widths — a floor, not a fixed size. A row of cards that stops short of the section edge
is wrong.

## Build rules — the five non-negotiables

Full detail, tables and reasoning: `exports/dashboard/build-rules.md`. Reference
implementation: `preview/meta-ads-app.html`.

1. **Exactly one region scrolls — the Slot.** `html, body { overflow: hidden }`, shell locked
   to the viewport, rail `overflow: hidden` with only its nav list scrolling so the user-card
   stays pinned. If the document scrolls, the rail scrolls away with it.
2. **`.slot > * { flex: 0 0 auto }`.** Sections are flex items in a fixed-height column and
   will otherwise be *compressed* instead of the slot scrolling — this collapsed a 228px
   chart body to 56px.
3. **Horizontal measured values are exact; never clamp them.** 260 rail, 1084 section, the
   `card-layout` splits, table data columns. On wide screens change the **column count**, not
   the sizes. Cards *fill* their section — 286 and 160 are floors.
4. **Vertical measured values are the ceiling of a clamp.** A tall viewport renders the
   component exactly as drawn; a short one compresses rather than pushing content below the
   fold.
5. **Align charts by grid, not by matching gaps.** Each bar label shares a grid row with its
   bar. Two independent columns accumulate ~2px of drift per row — measured at 14px.

And one habit: **anything not measured gets a comment saying so** — the fluid shell, hidden
scrollbars, every clamp minimum. A later reader must never mistake a judgement call for a
Figma value.

## The composition ladder — compose downward, never sideways

```
section-elements  →  Sections  →  Dashboard Build
```

| Tier | What it is | Where |
|---|---|---|
| **Dashboard Build** | The page shell. 260px nav rail + content container. **Every dashboard page is this component.** | `exports/dashboard/dashboard-build.md` |
| **Sections** | Self-contained rows and panels that drop into the shell's slot. | `exports/dashboard/sections.md` |
| **section-elements** | The parts a Section assembles — kpi-card, analytics-card, table-row, dropdown, list-item, user-card. | `exports/dashboard/section-elements.md` |

Three hard rules:

1. **Start from Dashboard Build.** Never hand-build dashboard chrome — no bespoke sidebar,
   no custom page frame. Fill its slot.
2. **The slot takes Sections only.** Never place a section-element or loose content
   directly in the slot. If nothing fits, use `section/Container` and put custom content
   in *its* slot.
3. **Reach for a section-element through the Section that contains it.** Don't place one
   standalone.

## Which component? — the decision table

| Need | Use | Read |
|---|---|---|
| Any dashboard page | `dashboard-build` | `dashboard-build.md` |
| Page title + tabs + filters + refresh | `section/header` — one per page, sticky | `sections.md` |
| Headline metrics + supporting metrics | `section/card-layout`, `KPI cards` = 1, 2, or 3 | `sections.md` |
| A goal / progress readout | `section/progress-bar` | `sections.md` |
| Metric data that needs filtering in place | `section/With Dropdown` | `sections.md` |
| Browsable product data — leads, campaigns, entries | `section/table` | `sections.md` |
| A chart | `section/section-element/Graph` — `Bar` compares items, `Line` shows change over time, `Grouped Bar` shows several measures per item | `sections.md` |
| Anything else, or custom content | `section/Container` **(the rules call it `section/Other` — the real name is `Container`)** | `sections.md` |
| A button | `Primary` (black) / `Outline` / `Ghost` — **never a blue fill** | `button.md` |
| Tabs, filter dropdown, toggle | `controls/tab`, `controls/dropdown`, `controls/toggle` | `controls.md` |
| Status feedback after an action | `toast` — `Error` / `Warning` / `Success` / `Info` | `toast.md` |
| A status pill anywhere | **Badge** | `foundation/shared-components.md` |
| A metric's direction | kpi-card `Type` = `Positive` / `Negative` / `Neutral` | `section-elements.md` |
| Nav rail grouping | `list-item` with `Property 1=Variant4, Label=yes` for the uppercase group header | `section-elements.md` |

## Cross-surface: which one?

Three components exist **separately per surface**. Getting this wrong is the most common
way dashboard output goes off-system.

| | Use on a dashboard | Not this — that's web |
|---|---|---|
| **Button** | `Button` (`2203:931`) — `Style` = `Primary` / `Outline` / `Ghost` | The web `Button` (`1457:668`) — `Blue` / `Black` / `Outlined/ black` / … |
| **Avatar** | `Avatar` (`1658:24023`) — generated character, app users | `client/avatar` — grayscale squircle, real client photos |
| **Logo** | `gushwork-logo-(internal-use)` (`2102:13508`) — 32×32 symbol tile | `gushwork-logo` — the full marketing wordmark |

**Web and dashboard use two different button component sets by design** — this is
intentional, not a Figma bug to be tidied away. Both are literally named `Button`, and
both expose a `Style` property whose values are completely disjoint:

| | `Style` values |
|---|---|
| **Dashboard** `2203:931` | `Primary` · `Outline` · `Ghost` |
| **Web** `1457:668` | `Blue` · `Black` · `Outlined/ black` · `Outlined / white` · `Text/ black` · `White` · `Special/ With People` · `Special/ Glowing` |

`Style=Primary` is dashboard-only. `Style=Blue` is web-only and invalid here. If you find
yourself reaching for a blue filled button, you have picked up the wrong component. Never
merge, alias, or substitute the two sets.

**Badge is genuinely shared** — same component, both surfaces. See
`foundation/shared-components.md`.

## Surface defaults

These sit above the individual component rules.

- **Never a blue button fill.** Action tiers are black / outlined / text-only. Blue stays
  valid as a *signal* — Info toasts, blue badges. The ban is on fills.
- **`section/header` is sticky** at the top of every page unless explicitly asked
  otherwise.
- **Collapsible Sections default to expanded.** Collapse exists so users can manage a
  dense dashboard — not to hide primary content by default.
- **The Admin avatar is only for owners and admins.** Everyone else gets a standard avatar,
  assigned freely.
- **Match `Mode` to the surrounding Section** on kpi-cards and analytics-cards; match
  Badge and toast light/dark treatment to the surface they sit on.
- **Button and control sizes match their neighbours** — usually `Small` or `Medium` on a
  dashboard.
- No emoji. No bare coloured status dots — use a Badge. See
  `foundation/shared-components.md`.

## Copy

Dashboard buttons are **product action labels**, not marketing CTAs — `Export`,
`Add campaign`, `Save changes`. The `Book a Demo` rule in `foundation/voice.md` governs
marketing CTAs and does not apply here. Sentence case still does.

Replace every placeholder. The components ship `List Item 1`, `Card title`,
`Column Header`, `Entry name`, `Dropdown option 01`, `Bruce Wayne`. None of it is real
copy.

## Known gaps in the source — do not paper over these

Encoded so you don't silently invent an answer:

- **Toast auto-dismiss is undefined.** The rule leaves it as an open question. Don't pick a
  timeout.
- **`controls/dropdown` has no `Color=White, State=Open` variant.**
- **kpi-card has only 6 of 18 `Mode × Type` combinations.** Check `section-elements.md`
  before specifying one.
- **Avatar has only one `Admin=true` variant** (`Style=1, Color=Blue`). Any other admin
  combination resolves to nothing.
- Several keys are Figma auto-generated and load-bearing — `Property 1`, `Variant4`,
  `Mode3`–`Mode6`. Use them exactly as written; don't tidy them.
- **The dashboard and web secondary-button keys differ by two letters** — dashboard is
  `Outline`, web is `Outlined/ black`. Close enough that a careless find-and-replace or a
  substring match silently crosses surfaces. Match the whole key, not a prefix.

If a request needs a value or variant that doesn't exist, say so. Don't interpolate a
radius, invent a Mode, or guess a timeout.

## When the library is missing something

Two different situations. Do not confuse them.

### Fall back — a whole deliverable or surface the system does not cover

A slide deck, a flyer, a standalone tool, a marketing page (that is `gushwork-web`), or a
surface with no Sections at all. **Do not build these.** Tell the user plainly that it is
not in the Gushwork design system yet and point them at Utsav on Slack to get it added:
`https://gushwork.slack.com/team/U06UAR183TR`. Say it in your own words.

### Build it — a small element missing from an otherwise buildable screen

A dashboard that needs a stat tile, a segmented toggle, an empty state, a stepper, a
date-range picker — something the Sections almost cover but not quite. **Build it, then
declare it.** Refusing to render a whole screen over one missing chip is worse than
building the chip and saying so.

Three conditions, all required:

1. **Compose from what exists first.** Most "missing" things are a `section/Container` with
   the right contents, or a Section you have not considered. Check `sections.md` and
   `section-elements.md` before concluding anything is absent.
2. **Build it from tokens only.** Colour, type, radius, shadow and spacing come from
   `foundation/tokens.css`. A new element may combine existing values in a new shape; it
   may never introduce a new value. If it needs a value with no token, that is a finding —
   report it, do not invent the value.
3. **Mark it in the code.** A comment at the element saying it is new, what it was needed
   for, and that it is pending library review. Anyone reading the file later must be able to
   tell your element from a measured one.

### Then notify — every time, without being asked

**If you created or modified any element, you must tell the user before you finish.** Not
buried in a summary — a clear block at the end of your reply.

**Short message, linked detail.** Write the full record to `notices/YYYY-MM-DD-<slug>.md`,
commit it, then give a **four-line** notice that links to it. Format and the Slack message:
**`foundation/new-component-notice.md`**. Nobody reads a twenty-line Slack message on a
phone.

The notice file must state: what was **created** and why the library had no equivalent, what
was **modified** with the exact measured value you deviated from, the **tokens** used so
review can confirm nothing was invented, and **where** each lives.

It must also carry a **"Worth a decision"** section naming the one or two items that are
genuine judgement calls rather than obvious adaptations. That section is what makes it a
review rather than a list.

**Never let a created element pass silently.** The whole point of a governed system is that
drift is visible. An undeclared component is worse than a refusal, because it looks
official.

## Source of truth

Figma — Gush Design System v2.0, file `VKcb4fgVyOHKfQonMgN772`, page
`03 · Dashboard → ↳ dashboard/ component+pattern-library` (`1658:24112`).

The exports in `exports/dashboard/` are transcribed from that page's annotations, with the
inconsistencies flagged inline. Where a rule and the actual component disagree, the exports
document **the component** and note the discrepancy — the component is what renders.
