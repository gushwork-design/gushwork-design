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

**Never restate a token value or a voice rule here or in your output.** Reference the token.

Three tiers, because "never invent a number" is unfollowable for page layout and a rule
that can't be followed gets ignored where it matters:

1. **Colour, type, radius, shadow, spacing — always a token. No exceptions.** If one of
   these has no token, that is a finding to report, never a value to invent.
2. **Layout dimensions documented in `exports/`** — the 260 rail, 1164 container, 32px logo
   tile, 28px small button — use the documented figure exactly.
3. **A layout dimension with no documented figure**: choose sensibly, but **say in one line
   that you chose it.** Don't pass your own number off as coming from the system.

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

## Components that do NOT exist — fall back, don't build

A Figma-agent-generated specification circulating alongside this system documents dashboard
components that are **not in the file**:

`Modal` · `Empty State` · `Dropdown Menu` · `Notification Badge` · `Segmented Control` ·
`Breadcrumbs` · `Date Picker` · `Pagination` (as a standalone component)

The same spec describes a 240px collapsible sidebar, a 56px app top bar, an initials-based
avatar, and a **`Blue` dashboard button**. **None of those is in this file.** The rail is
260px, the page header is 1164×164 with a 32px Vert Grotesk title, the avatar is an
illustrated character, and blue button fills are banned — ruled 6 Aug 2026.

Its structural claims were checkable in nine places and wrong in all nine. **Treat it as a
lead, never as authority.** If a request needs one of the above, use the out-of-scope
fallback below.

Full detail: `RECONCILIATION.md`.

## When the request is out of scope

**Always try to fulfil the request by composing existing components first.** Most requests
that sound novel are a `section/Container` with the right contents, or a Section you
haven't considered. Check `sections.md` and `section-elements.md` before concluding
anything is missing.

Fall back **only** when the request genuinely needs a component, surface, or deliverable
type that isn't in this skill yet — a slide deck, a flyer, a standalone tool, or a
component with no match in the exports.

When you do fall back, tell the user plainly that the thing they've asked for isn't in the
Gushwork design system yet, and point them at Utsav on Slack to get it added:
`https://gushwork.slack.com/team/U06UAR183TR`. Say it in your own words — don't paste the
same sentence every time.

**Never invent a component or guess at a brand rule to fill a gap.** Falling back is
always better than producing something off-system.

## Source of truth

Figma — Gush Design System v2.0, file `VKcb4fgVyOHKfQonMgN772`, page
`03 · Dashboard → ↳ dashboard/ component+pattern-library` (`1658:24112`).

The exports in `exports/dashboard/` are transcribed from that page's annotations, with the
inconsistencies flagged inline. Where a rule and the actual component disagree, the exports
document **the component** and note the discrepancy — the component is what renders.
