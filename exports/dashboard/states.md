# States — focus, hover, empty, loading

**Everything in this file is RULED, not measured.** Figma defines none of it, and that absence
was producing a different answer on every build. These are the answers. Use them; do not
re-decide them.

Ruled by Utsav, 7 Aug 2026.

**Scope: dashboard / product.** The same focus rule applies on web.

---

## Focus — every focusable element, both surfaces

**No component in the Figma file defines a focus state.** Not `Button`, not `controls/*`, not
`list-item`, not `table-row`, not `user-card`. Keyboard users were getting whatever the browser
happened to do, which on a restyled `<button>` is often nothing at all.

```css
:is(button, a, [tabindex], input, select, textarea):focus-visible {
  outline: var(--gw-focus-ring);
  outline-offset: var(--gw-focus-offset);
  border-radius: var(--gw-radius-4);
}
```

- `--gw-focus-ring` and `--gw-focus-offset` are in `foundation/tokens.css`. They compose from
  `--gw-color-primary-alpha-40` and introduce no new colour.
- **`:focus-visible`, not `:focus`** — a mouse click should not leave a ring behind.
- **Never `outline: none` without a replacement.** This is the one rule in this file that is an
  accessibility requirement rather than a preference.
- Blue is correct here. A focus ring is a **signal**, not a control state — see the
  data-vs-control-state rule in `controls.md`.

## Interactive targets must be real controls

A row that looks pressable and is not is worse than a missing hover.

- Anything clickable is a `<button>` or an `<a>` — never a `<div>` with a click handler.
- Anything **not** clickable never gets a hover, a pointer cursor, or a focus ring. The nav
  group label is the worked example: see `list-item` in `section-elements.md`.

## Hover

Per-control values live with their components — `controls.md` for tabs, dropdowns, toggle and
buttons; `section-elements.md` for `list-item`, `table-row` and `user-card`. Two rules sit
above them:

1. **Every *click target* has a hover state.** If a variant exists in Figma without a
   measured fill, the value is in the component's export file. Do not invent a third answer.
2. **Hover moves one step, in the direction of the element's own selected state.** A tab moves
   toward white because `Selected` is white. A grey trigger moves to `neutral-100`. It never
   jumps two steps or changes hue.
3. **Check that Figma is actually silent before you fill the silence.** All three `Button` hover
   fills were ruled by hand on the belief that the `State=Hover` symbols carried none. They
   carried them the whole time, and all three rulings were wrong — see `button.md`.

**The one exception to rule 1 is the text field.** `input/text-field`'s `State=Hover` is
byte-identical to `State=Default` across all 14 variants — measured, not missing. A text input's
affordance is the caret, not a fill, and its feedback is `Selected`. `DECISIONS.md` → **R2**,
`foundation/text-field.md`. Rule 1 is about **click targets**; a field is not one.

All hover transitions use `--gw-motion-fast`, guarded by `prefers-reduced-motion`.

---

## Empty state — RULED, pending Figma

`foundation/output-targets.md` requires an empty state per Section and records that the library
ships none. It ships one now.

**Compose from `section/Container`.** The Section keeps its normal header — icon tile, title,
caret — so the page structure does not change shape when data is missing. The empty content
goes in the body:

| Part | Value |
|---|---|
| container | the Section's normal `sec__body` — white, 1px `--gw-color-neutral-50`, `--gw-radius-8` |
| layout | vertical, centred, gap `--gw-space-8`, padding `--gw-space-48` block / `--gw-space-20` inline |
| title | `--gw-text-body-16-sem` · `--gw-color-neutral-900` |
| body | `--gw-text-body-14-reg` · `--gw-color-neutral-600` · max-width 420 |
| action | one `Button` — `Primary` if there is an obvious next step, otherwise omit it |

**Copy rule: say what is missing and what to do, in that order.** "No leads yet — connect a
form to start capturing them." Never "No data" alone, and never blame the user.

**Do not repeat the page or section name in the body** — the Section header already carries it,
and it reads badly for plural names ("Leads is not part of this sample").

## Loading state — RULED, pending Figma

Same provenance: required by `output-targets.md`, drawn nowhere. `Skeleton` and `Spinner` are
named in `foundation/shared-components.md` as *intended* components and do not exist.

**Skeleton, not spinner.** The shell renders before the numbers arrive on every page, so the
layout is already known — hold its shape rather than covering it.

| Part | Value |
|---|---|
| block | `--gw-color-neutral-100`, `--gw-radius-4`, sized to the text or number it replaces |
| animation | a gentle opacity pulse, `--gw-motion-fast` × 8, or none under `prefers-reduced-motion` |
| structure | one block per real element — do not collapse a kpi-card to a single grey rectangle |

**The rule that matters more than the styling:** never render a `0`, a `—`, or a plausible
number while data is in flight. A `0` that means "not loaded" reads as "we got no leads", and
that misreading is expensive. This restates `output-targets.md`; it is repeated here because
it is the failure that actually ships.

---

## Sample and placeholder data

When the numbers are yours rather than measured, the `Sample data` marker is **not optional**.

- A `Badge`, `Color=Yellow`, in the `section/header` — see the title row in `sections.md`.
- It sits in the header's **title row**, not the toolbar, so it cannot scroll out of view.
- Remove it the moment real data lands.

Never invent a number implying a business outcome — revenue, conversion, pipeline — without it.
