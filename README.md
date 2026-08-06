# Gushwork Design System

A governed design system for **Gushwork**, packaged as a Claude Code plugin.

Gushwork is the AI Marketing Team that researches, writes, publishes, and ranks content
across AI search engines — ChatGPT, Perplexity, Gemini — and traditional search, then pipes
qualified inbound leads to your inbox.

This repo exists so that anything Claude generates for Gushwork comes out on-brand by
default: the right components for the right surface, real tokens instead of guessed hexes,
and a hard stop rather than an invented component when something genuinely doesn't exist yet.

## Install

```bash
claude plugin install https://github.com/utsav-gushwork/gushwork-design.git
```

Then just describe what you're building. The skills trigger on the work, not on being named:

- *"Build a pricing page for Gushwork"* → `gushwork-web`
- *"Add a KPI row to the leads dashboard"* → `gushwork-dashboard`

## Two surfaces, two skills

The system covers two surfaces that look and behave differently, so they are two skills with
disjoint trigger vocabularies. They are deliberately **not** merged.

| Skill | Surface | Fires on |
|---|---|---|
| [`gushwork-web`](skills/gushwork-web/SKILL.md) | Public marketing site | landing page, ad lander, hero, fold, CTA section, pricing, comparison table, testimonial, case study, FAQ, navbar, footer |
| [`gushwork-dashboard`](skills/gushwork-dashboard/SKILL.md) | Logged-in product | dashboard, app screen, KPI card, analytics panel, data table, side nav, filters, tabs, toasts |

Spacious white-and-blue marketing surfaces on one side; dense gray-canvas product surfaces
with black-and-outline actions on the other. Blue is a primary action on the website and a
signal-only colour in the product.

## Foundation — referenced, never duplicated

Both skills point at these. Neither restates them, and neither should.

| File | Holds |
|---|---|
| [`foundation/tokens.css`](foundation/tokens.css) | 188 custom properties — colour, type, spacing, radii, shadows — pulled from the Figma **variables** |
| [`foundation/voice.md`](foundation/voice.md) | Voice, casing, punctuation, the primary-CTA ruling, banned words |
| [`foundation/shared-components.md`](foundation/shared-components.md) | The atoms genuinely shared across both surfaces — Badge, Gushwork logo, Phosphor icons |

## Rules in the skill, structure in the exports

Each `SKILL.md` holds only **usage rules** — default → exception, which component when, what
never to do — and stays short enough to load cheaply on every invocation. The bulky variant
enumerations, dimensions, and node IDs live in `exports/`, which the skills reference by
filename.

```
gushwork-design/
├── README.md
├── .claude-plugin/plugin.json
├── foundation/
│   ├── tokens.css
│   ├── voice.md
│   └── shared-components.md
├── skills/
│   ├── gushwork-web/SKILL.md
│   └── gushwork-dashboard/SKILL.md
└── exports/
    ├── web/          page-shell · folds · fold-elements · atoms · cards · button · avatar · images
    └── dashboard/    dashboard-build · sections · section-elements · button · avatar · controls · toast
```

## The composition ladder

Both surfaces mirror each other. Compose downward; never place a lower tier directly into a
page shell's slot.

```
web         atoms  →  fold-elements  →  Folds     →  Page Build
dashboard          section-elements  →  Sections  →  Dashboard Build
```

## Three components exist separately per surface

Buttons, Avatars, and Logos are **not** shared, and mixing them is the most common way output
goes off-system. Both skills carry a "which one?" pointer.

| | Web | Dashboard |
|---|---|---|
| **Button** | `Button` `1457:668` — `Blue` / `Black` / `Outlined/ black` / … | `Button` `2203:931` — `Primary` / `Outline` / `Ghost` |
| **Avatar** | `client/avatar` — grayscale squircle, real client photos | `Avatar` `1658:24023` — generated character, app users |
| **Logo** | `gushwork-logo` — full marketing wordmark | `gushwork-logo-(internal-use)` — 32×32 symbol tile |

The two button sets are **both literally named `Button`** and expose a `Style` property whose
values are completely disjoint. This is intentional and permanent — never merge or alias
them.

**Badge is genuinely shared**, same component on both surfaces — web cards and tables,
dashboard KPI cards.

## Out of scope is a first-class answer

Both skills compose from existing components first. When a request genuinely needs a
component, surface, or deliverable that isn't in the system yet — slides, flyers, a tool, a
component with no match — the skill says so and points at Utsav on Slack rather than
inventing something plausible. Falling back beats shipping off-system.

Slides, flyers, and tools are planned; the structure above is built to absorb them as
additional skills without touching the foundation.

## Two sources, and where they disagree

Everything in `exports/` is **measured** — read off specific Figma nodes and traceable to a
node ID. A separate *Master Specification* generated by the Figma agent also describes the
system, and the two conflict in about a dozen places, including one governance rule (whether
a blue button fill is allowed on dashboards).

**[`RECONCILIATION.md`](RECONCILIATION.md)** records every conflict, which source each export
follows, and the six questions that need a ruling. Read it before trusting either source on
the navbar, the dashboard button, the dashboard avatar, toasts, or content width.

The short version: where they disagree, the exports follow the measured node, because that is
what actually renders. The likeliest explanation for the biggest conflicts is that
`↳ web/ component-library` — 21 component sets — has never been read, since the MCP's page
listing only ever returns `00 · Cover`. If a second navbar and button set live there, most of
the conflicts dissolve into "two components, document both".

## Known issues in the Figma source

The Figma file is the source of truth, and it contradicts itself in places. Every one of
these is flagged inline where it matters rather than silently smoothed over — the exports
document **what the component actually renders**, since that's what ships.

- **Canvas swatch labels have drifted from the variables.** All 12 Neutral and 7 of 12
  Primary hex labels are from a superseded palette, and 10 of 31 typography spec rows
  contradict their own variables. `tokens.css` is generated from the **variables**, which are
  authoritative. Never read a value off the canvas.
- **The primary CTA appears three different ways** — `Book a demo` (51 nodes), `Book a call`
  (42 nodes), `Book a Demo` (3 nodes). Ruled: **`Book a Demo`**, a fixed capitalised string
  and an explicit exception to sentence case. See [`foundation/voice.md`](foundation/voice.md).
- **Variant keys carry irregular spacing and are load-bearing** — `Outlined/ black` vs
  `Outlined / white`, nine folds prefixed `fold/ ` and three not, `size` lowercase on
  `client/avatar`, Figma auto-generated `Property 1` / `Variant4` / `Mode3`–`Mode6`. Copied
  exactly, never normalised.
- **Rules that disagree with their own components** — `fold/ Cards Grid (small)` documents 3
  cards and renders 4; the `Special/*` button rule asks for sizes the set doesn't contain;
  kpi-card has 6 of 18 `Mode × Type` combinations; Avatar has one `Admin=true` variant.
- **Mismatched and missing descriptions** — `talking-guy` carries a description copied from a
  different component; `Agent Card` has no Info Frame at all; no fold-element has its own
  Rules of Usage.
- **Structural defects** — `footer/…/list-item` is a broken component set; stray U+2028 LINE
  SEPARATOR characters in three rule blobs break Figma MCP serialization and are why
  whole-page metadata reads fail.

Renaming Figma variants is a breaking change for anything keyed to them, so none were renamed
in building this. The list above is the fix queue, not a changelog.

## Source of truth

Figma — **Gush Design System v2.0**, file key `VKcb4fgVyOHKfQonMgN772`. Marketing components
on `↳ web/ pattern-library` with worked pages on `↳ web/ template-library`; product components
on `↳ dashboard/ component+pattern-library` (`1658:24112`).

When the Figma file changes, update the affected `exports/` file and re-check the rule in the
matching `SKILL.md`. Tokens come from the variables — re-pull them, don't hand-edit.
