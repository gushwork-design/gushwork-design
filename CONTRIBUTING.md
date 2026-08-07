# Changing the design system

**This file is for maintainers.** If you are building a screen, you do not need it, and you do
not need Figma — everything measured is in `exports/`. Stop here.

Read on only if you are adding a component, correcting a measurement, or re-pulling tokens.

## The one rule that has cost the most

**Read the component *set*, or a variant `<symbol>` inside it. Never an instance.**

An instance read misreports type weight. Instances inside `dashboard-build` return `Inter:Bold`
for text the component set defines as `Inter:Medium` or `Inter:Semi_Bold`. This shipped a wrong
nav rail **twice** before it was understood.

How to tell them apart in `get_metadata`:

| | Is | Trust it? |
|---|---|---|
| `<symbol>` | a definition — one per variant | **yes** |
| `<instance>` | a use of a definition | no, for anything but position |

## Two checks, every time

Each of these caught a real error that eyeballing had passed.

**Compare geometry numerically.** Read Figma's `x/y/w/h` from `get_metadata` and assert against
`getBoundingClientRect()`. A screenshot comparison approved a rail that was 9px out per nav
group — three times over, and it still looked fine.

**Sample the render for colour.** `get_screenshot`, then read the pixel. Annotation text does
not carry fills, and inference is unreliable: a nav icon that obviously "should" be muted grey
is in fact the same `neutral-900` as its label. Two other examples — `kpi-card` at `Mode=light`
renders a **dark** card, and `side-panel` has no fill at all despite being drawn as a white card.

**When an annotation and the component disagree, the component wins** and the disagreement is a
finding to record. `dashboard-build`'s annotation claims `gap:8` where its own coordinates prove
0.

## Tokens come from variables, never the canvas

`foundation/tokens.css` is generated from the Figma **variables**. The canvas swatch labels have
drifted badly — all 12 Neutral hexes and 7 of 12 Primary are from a superseded palette, and 10
of 31 typography rows contradict their own variables.

Re-pull by unioning `get_variable_defs` across many component nodes on every page. The
building-blocks showcase frames are **not** a complete source: of 23 radius swatches only two
are bound, and the swatches labelled 60px and 160px are both bound to `Spacing/56`.

**Never hand-edit `tokens.css`.** If a value has no variable, that is a gap to raise in Figma,
not a line to add here.

## Never rename a Figma variant

Renaming is a breaking change for everything keyed to it. Several keys are Figma
auto-generated and load-bearing — `Property 1`, `Variant4`, `Mode3`–`Mode6` — and irregular
spacing is significant: `Outlined/ black` vs `Outlined / white`, `Size=16 px` with the space.
Copy them exactly. Document reality; don't tidy it.

`RECONCILIATION.md` holds every place the measured exports and the Master Specification
disagree, and which one each export follows. Add to it rather than silently picking a side.

## Shipping the change

See the propagation table in [`README.md`](README.md). The short version:

1. Change Figma **and** measure it into the repo in the same sitting. Figma alone ships nothing.
2. **`bash scripts/stamp-release.sh 1.2.0`** — stamps the version and today's date into all four
   places at once: both manifests and both skills' announce lines.
3. `claude plugin validate .` before you push.
4. Push to `main`. Anyone with `autoUpdate` on gets it at their next start.

**Always stamp.** The announce line is how a teammate finds out they're stale without checking —
their copy reports *its own* date, not today's. If you edit a skill without stamping, that signal
silently lies. It costs one command.

You do **not** need a version bump for content to propagate — the marketplace clone *is* the
plugin, so a refresh is a `git pull` and whatever is on `main` becomes live. The version is how
people tell you what they're running, not the delivery mechanism.

## Closing a notice

When a build hits a gap it files `notices/YYYY-MM-DD-<slug>.md` and sends a four-line Slack
block. Each item in its **"Worth a decision"** section gets one of four verdicts — **Add**,
**Replace**, **Promote**, **Revert** — and the verdict is not done until it is in Figma or in
`exports/`. Format and the full review procedure:
[`foundation/new-component-notice.md`](foundation/new-component-notice.md).

**Promote is the one people forget.** If a deviation held up across nine pages and three
viewport heights, the component is what's wrong, not the deviation.
