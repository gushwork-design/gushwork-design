# The unavailable state — a ruling, and a doc correction

Ruled 28 Aug 2026. Files: `exports/dashboard/states.md`, `foundation/output-targets.md`,
`exports/dashboard/component-registry.json`, `skills/gushwork-dashboard/SKILL.md`

Raised by a teammate building a dashboard that reads five separate stores, any one of which
can fail. Nothing in the system said what a card should look like when the read fails, so
every build would have answered it differently.

## Created

### Unavailable — a third data state, alongside empty and loading

`states.md` ruled **empty** and **loading** on 7 Aug 2026 and stopped there. Failed was never
ruled, and it is a third condition rather than a shade of either: empty means we read the
source and it held nothing; unavailable means we could not read it at all.

The ruling is one line — **an element that encodes a quantity is removed, never zeroed.** A
progress bar at 0%, a percentage of `0%`, a sub-line of `of 0` and a value of `—` are all
measurements. They say "we looked, and the answer is nothing", which is a different claim from
"we could not look", and it is the claim a reader acts on.

That principle was already half-ruled. The loading section says: *never render a `0`, a `—`, or
a plausible number while data is in flight; a `0` that means "not loaded" reads as "we got no
leads", and that misreading is expensive.* The gap was its scope, not its reasoning — it covered
in-flight and never covered failed. R10 points the same way for toasts: an error the user did
not see is an error that did not happen.

**Scope: any data-bearing card or section.** The card keeps its surface, radius, padding, label
and footprint, so the page does not change shape because a store went down. Only the parts
carrying a quantity change: `status-dot` to `Status=behind`, the value to
`--gw-text-body-14-med` / `--gw-color-neutral-500`, sub-line and percentage and progress bar
removed, and one `Badge` `Color=Red` naming the source that failed.

## Modified

### `foundation/output-targets.md` — it pointed every build at a folder that does not exist

The file told every build: *`components/dashboard/README.md` lists what exists. Import from
there before writing a component.* There is no `components/dashboard/` in this repo, and not
one `.tsx` or `.jsx` anywhere in the plugin. Anyone following the instruction hit a wall.

Corrected to point at the measured specs in `exports/`, which is what a components folder would
have been compiled from anyway. **Building the folder is still open** — it is a real decision
about whether to commit to the React path, and it is in the backlog rather than being decided
here.

### `component-registry.json` — `stat-card` and `metric-card` to 1.42.0

`breaking: false`. Existing builds render correctly; they have no failure treatment, which is a
gap rather than a defect. Owners get the amber "improved" notice, not the red one.
`kpi-card` and `analytics-card` are in scope for the ruling but are v1 section-elements and not
in the registry, so nothing was bumped for them.

## Worth a decision

**The copy in the value slot.** The proposal was `Could not compute`; the ruling says
`Unavailable`, with the failed source named in the badge. The reasoning is that the reader can
already see the number is missing — what they cannot see is which of five stores went down, and
that is the only fact that tells them whether the rest of the page is trustworthy.
`Could not compute` describes our failure rather than their problem and spends the same room.
This is a one-line change in `states.md` if you disagree.

**Where the retry lives.** Ruled out of the card and onto the `section/header`, where the
refresh control already exists, and only when it is wired. A 218 × 132 card has no room, and a
drawn-but-dead control is a trap that has shipped three times.

## Tokens

No new value of any kind. Every part composes existing tokens:

- `--gw-text-body-14-med`, `--gw-color-neutral-500` — the value slot
- `status-dot` `Status=behind` — `red/400`, an existing variant of a complete set
- `Badge` `Color=Red`, `Size=Small` — existing variants; dark uses the standard
  `Red/Alpha/10` + `Red/300` pairing from `foundation/shared-components.md`
- surface, radius, padding, label — unchanged from the measured `stat-card`

One correction carried into the ruling: the proposal specified `Badge Tone=danger`. **Badge has
no `Tone` property** — it is `Theme · Color · Icon · Size`. The value is `Color=Red`.

Nothing here is drawn in Figma yet, in keeping with the rest of `states.md`, which is ruled and
pending Figma by design.
