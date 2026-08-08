# v1.22.0 — every open decision ruled, and the text field promoted

**8 Aug 2026.** Everything the system had left hanging is now ruled, in one place:
**`DECISIONS.md`**, R0 through R10. Export files point at a ruling instead of restating the
argument, so there is one place to read a decision and one place to change it.

## The rulings

| | Ruling | |
|---|---|---|
| **R0** | Where a measured component and the written spec disagree, **the measurement wins**. Settles all four `RECONCILIATION.md` conflicts at once | new |
| **R1** | `input/text-field` is a **shared atom** — `foundation/text-field.md`, both skills own it | was open |
| **R2** | The text field has **no hover state**. `State=Hover` is byte-identical to `Default` | withdraws a ruling |
| **R3** | The Google button is **48 / radius 12 / no arrow**, in both variants | was open |
| **R4** | Titles use `--gw-color-neutral-black`, **never raw `#000000`** | was open |
| **R5** | Sub-pixel borders **round to 1px** — they are scaled instances, not design values | was open |
| **R6** | `Yellow Warning` builds **`--gw-color-yellow-500`**, not the off-palette `#c18c0b` | new finding |
| **R7** | Avatar backgrounds are the **`-25`** step of their own hue — Blue and Orange are drifted | was open |
| **R8** | The `image` typos are a **documentation** bug, not a key bug — build the correct spellings | was open |
| **R9** | On dark surfaces, text is at most **`--gw-color-neutral-400`** | was open |
| **R10** | **Errors never auto-dismiss**; the 4s timer pauses on hover and focus | was open |

## The text field is now a shared atom — `foundation/text-field.md`

`input/text-field` `1562:705`, **14 variants**, measured symbol by symbol. It was drawn in the
web library, but `dashboard-login-screen` instantiates it and the dashboard has no field of its
own. The two live options were promote or duplicate; duplicating creates two sources of truth for
one control and guarantees drift.

**It is the only component that crossed the surface boundary.** If a second one does, promote it
too rather than letting the boundary blur one exception at a time.

What the measurement found:

- **The fill is `neutral/50` in all 14 variants.** It never changes — not on hover, not on focus,
  not on error. Everything the field communicates is in its content, plus a border and a message
  for warnings.
- **`State=Hover` is byte-identical to `State=Default`.** Measured, not missing. The field's
  affordance is the caret and its feedback is `Selected`, so it has no hover treatment. This is
  the one documented exception to *"every interactive element has a hover state"* — that rule is
  about click targets.
- **It is a floating-label field.** The label shrinks to 12 on `Filled`, but **not** on
  `Selected` — a focused-but-empty field keeps its label at 14 with the caret on the line below.
- **A warning grows it from 56 to 76** — and 76 assumes the message fits one line at 400px wide.
  Narrower than about 330 and the real messages wrap. Let the message block grow; a clipped
  half-line of error text is worse than a field that moves.
- **`Feedback=Yellow Warning` binds `#c18c0b`, which is in no ramp.** Red uses `red-500` exactly.
  R6 builds `yellow-500` `#d97706`, the nearest step by a wide margin.

Three glyphs harvested to `assets/icons/`: `warning-circle`, `check-circle`, `circle-notch`. All
14 variants are on the review sheet.

## One withdrawn ruling, and one that was already withdrawn

| Withdrawn | Why |
|---|---|
| Text field hover → `neutral-100` | Figma's `State=Hover` is identical to `Default`. It was a third answer the set does not have. Superseded by **R2**. |
| `Button` hovers → `neutral-900` / `neutral-25` / `neutral-25` | All three were sitting in Figma the whole time, and all three rulings were wrong. Corrected in v1.21.0. |

Both were ruled on the belief that the source was silent. **`CONTRIBUTING.md` now requires
confirming the silence before filling it** — open the exact symbol whose value you are about to
rule, not the parent, not a sibling.

The mirror case matters as much: the field's hover genuinely *is* identical, and verifying that
turned "no hover" into a finding about the design rather than a gap to paper over. **Silence you
have verified is data. Silence you assumed is a guess wearing a ruling's clothes.**

## A correction between two of our own files

`exports/web/component-library.md` reported `image/startegy-and-pages` and
`image/product-&-serivce-cards` as **variant keys**, and warned that renaming them would detach
instances. `exports/web/images.md` had checked the canvas: **the real keys are spelled
correctly.** The misspellings exist only in the structure documentation blob `2065:15565`.

I drafted R8 from `component-library.md` and had it backwards — preserve-the-typo, map-in-code —
before `images.md` corrected it. Both files now say the same thing, and the standing rule is
recorded: **where two of our own files disagree, the one that measured the canvas wins.** Same
shape as set-over-instance. A structure blob is documentation, not the component.

## Still genuinely open

Not ruled, because ruling them needs a decision no measurement supports:

- `section/Container` **empty and loading states** — ruled *pending Figma*; provisional until the
  component exists.
- `controls/toggle` **`Size=X-Small`** at 36 × 20 — likewise pending Figma.
- **`Solutions` labels differ** between navbar (`AI Search`) and footer (`AI Search Agent`). Same
  destination, two names. A copy decision.
- **`dropdown-options` `Style=Calendar` has no range affordance.** Building one means designing
  it — report the gap rather than inventing a range picker.

## What a build should do differently now

R2, R4, R5, R6, R7, R9 and R10 all change output. **R9 is the one most likely to be wrong in
something already shipped** — footer legal text at `neutral-600` or `neutral-700` on black fails
contrast at ~3.9:1 and ~2.3:1 against a 4.5:1 floor. R7 changes two avatar backgrounds. R10
changes when an error toast disappears, which is behaviour, not appearance, and no screenshot
will catch it.
