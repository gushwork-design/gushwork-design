# Decisions — the standing rulings

Every open question in the system, ruled. **Ruled 8 Aug 2026 by Utsav.**

Each ruling has an ID. Export files point here rather than restating the reasoning, so there is
one place to change a decision and one place to read it.

A ruling is not a measurement. **Where Figma has a value, the value wins and there is nothing to
rule** — that is the lesson of `button.md`, where three hovers were ruled by hand and all three
turned out to be sitting in Figma already. Everything below is either a genuine gap in the
source, a conflict the source cannot resolve on its own, or a defect in the source that a build
must not reproduce.

---

## R0 — Figma outranks the spec document, always

**Where `RECONCILIATION.md` records a conflict between a measured component and the written
spec, the measurement wins.** This resolves §2.1, §2.2, §2.3 and §2.4 at once and any future
conflict of the same kind.

**Why.** The spec describes an intended system; the file *is* the system. Building to the spec
produces screens that do not match the components anyone opens in Figma. The four recorded
conflicts are not near-misses — the navbar differs in variant count, prop names and fill; the
dashboard button spec proposes a blue style that does not exist.

**In particular, variant keys keep their irregular spacing** — `Outlined/ black`,
`Outlined / white`, `Text/ black`. These are identifiers. The spec's tidied forms do not resolve.

**What this does not mean.** A measurement that is *wrong on its own terms* — off-palette,
failing contrast, internally inconsistent — is still a defect. R6, R7, R9 and R10 below all
override a measured value. R0 settles spec-vs-Figma, not Figma-vs-sense.

---

## R1 — `input/text-field` is a shared atom

**`input/text-field` `1562:705` moves to `foundation/text-field.md`. Both skills read it.**

**Why.** It is drawn in the web library, but `dashboard-login-screen` instantiates it, and the
dashboard library has no field of its own. The two live options were to promote it or to
duplicate it into the dashboard set; duplicating creates two sources of truth for one control
and guarantees drift, which is the exact failure the system exists to prevent. A text input has
no marketing-versus-product character to justify two of them.

**Consequence.** `foundation/` is now the home for anything both surfaces use — badge, logo,
icons, and this. **If a second dashboard component turns out to reach into `exports/web/`,
promote it here too** rather than letting the boundary blur one exception at a time.

---

## R2 — the text field has no hover state

**`State=Hover` is byte-identical to `State=Default`. Build no hover treatment on a text field.**

**Why.** This is measured, not missing: same `neutral/50` fill, same type, same everything. The
field's affordance is the caret (`cursor: text`), and its feedback is `Selected`. An earlier pass
ruled `neutral/100` here — that was a third answer Figma does not support, and it is withdrawn.

**This is the one exception to** *"every interactive element has a hover state"* in
`exports/dashboard/states.md`. That rule is about **click targets**. A text input is not one.

**`:focus-visible` remains mandatory** — more so here, because the fill does not move either, so
without it a keyboard user gets no signal at all.

---

## R3 — the Google button is 48 / radius 12 / no arrow

**`dashboard-login-screen` renders its Google button at 48 tall, `--gw-radius-12`, with the
Google mark leading and no trailing arrow — in both variants that carry it.**

Figma disagrees with itself: `Type=Google` draws 72 / radius 16 / with a trailing arrow;
`Type=Google + Email` draws 48 / radius 12 / none. Two variants of one component, two buttons.

**Why 48/12/none wins.**

- **Radius 12 matches the black button** it stacks with. At 16 the two buttons in
  `Google + Email` would not agree with each other, which is visible and wrong.
- **72 is out of scale with the whole system.** `Button Large` is 48; nothing else in either
  surface is 72 tall. The 72 is not a considered size, it is an untouched draft.
- **The trailing arrow is misleading on this button.** On the black primary, `ArrowRight` means
  "proceed". Repeating it on a secondary OAuth button says the same thing twice and gives two
  controls the same weight of promise.
- The `Type=Google` button is alone on its screen, so it has nothing to differentiate itself
  *from* — the size difference buys nothing.

**Report the drift when you build it.** Fixing `Type=Google` in Figma is a maintainer task.

---

## R4 — titles use `--gw-color-neutral-black`, never raw `#000000`

**`dashboardTitle` in `dashboard-login-screen` binds a raw `black`. Build
`--gw-color-neutral-black` `#0d0d0d`.**

**Why.** Every other title in both surfaces uses the token. A raw `#000000` is invisible to a
palette change and is a full shade off the black actually used everywhere else — it does not
match the panel beside it. This generalises: **any raw hex that has a token is a binding bug in
the source; build the token and report it.**

---

## R5 — sub-pixel borders round to 1px

**Build `1px`. A `0.81px` border is a 1px border on an instance Figma has scaled.**

Both Google buttons report `0.81px`; the login logo tile reports `spacing/8` while rendering 15
for the same reason. **A non-integer border or radius is an artifact of scale, not a design
value** — no one specified 0.81. Round to the nearest integer and say you did.

---

## R6 — `Yellow Warning` builds `--gw-color-yellow-500`

**`input/text-field`'s `Feedback=Yellow Warning` binds `#c18c0b`, which is in no ramp. Build
`--gw-color-yellow-500` `#d97706`.**

**Why.** `Red Warning` binds `#e11d48`, which is exactly `red-500`. Yellow should mirror it.
`#c18c0b` is nearest `yellow-500` by a wide margin — the alternative, `yellow-600` `#b45309`, is
roughly twice as far. An off-palette hex means a palette change misses this field.

---

## R7 — avatar backgrounds are the `-25` step of their own hue

**Normalise: Blue → `--gw-color-primary-25`, Orange → `--gw-color-orange-25`.**

Measured, the backgrounds are inconsistent in two different ways — Blue uses the `-50` step where
Red, Yellow and Green use `-25`, and Orange abandons its hue entirely for `neutral-50`. Bodies
are consistently the `-300` step in all five.

**Why.** Three of five agree on `-25`, so `-25` is the pattern and the other two are the
exceptions. Orange on `neutral-50` is plainly a mistake — every other avatar tints its background
with its own hue, and a grey-backed orange avatar reads as a different component. Both
replacement tokens exist. Report the drift.

---

## R8 — the `image` typos are a documentation bug; build the correct spellings

**Use `image/strategy-and-pages` and `image/product-&-service-cards`. There is nothing to
preserve and no mapping to carry.**

The unresolved bracket in the Rules of Usage — *"[decide before handoff: fix the typos … in Figma
now, or keep them exactly as-is permanently]"* — **asks a question about a situation that does not
exist.** `exports/web/images.md` checked the canvas: **the actual variant keys are spelled
correctly.** The misspellings `startegy` and `serivce` appear only in the structure documentation
blob `2065:15565`, which also names the typo'd form as the property default.

So there is no key-renaming risk, because there is no misspelled key. **The doc is wrong, not the
component.** Correcting the blob is a maintainer task with nothing bound to it.

**Where two of our own files disagree, the one that measured the canvas wins** — the same rule as
set-over-instance. `exports/web/component-library.md` read the typos out of the doc blob and
reported them as keys; `images.md` read the canvas. `images.md` is right, and
`component-library.md` has been corrected.

The same blob states three different totals for one property — 47, 46, and per-category tables
summing to 45. **The canvas has 46.**

---

## R9 — on dark surfaces, body text is at most `--gw-color-neutral-400`

**`--gw-color-neutral-400` `#959ba4` is the darkest neutral permitted for text on
`--gw-color-neutral-black` or `--gw-color-neutral-900`.**

The footer currently sets its copyright in `neutral-700` on black — about **2.3:1**, against a
4.5:1 floor — and its legal links in `neutral-600`, about **3.9:1**. Both fail.

Measured contrast on `neutral/black` `#0d0d0d`:

| | Ratio | |
|---|---|---|
| `neutral-700` `#535a61` | ~2.3:1 | ✗ |
| `neutral-600` `#6a7077` | ~3.9:1 | ✗ |
| `neutral-500` `#878b94` | ~5.7:1 | ✓ on black, **✗ 4.2:1 on `neutral-900`** |
| `neutral-400` `#959ba4` | **~6.9:1** | ✓ on both (5.1:1 on `neutral-900`) |

`neutral-400` is the only step that clears the floor on **both** dark surfaces, so it is the
single rule rather than two conditional ones. It is also already what the login panel uses for
its description and creator line — this makes the rest of the system consistent with that.

**This overrides the measured value.** Contrast is a floor, not a preference.

---

## R10 — errors do not auto-dismiss; the timer pauses on hover

**`toast` `State=Error` stays until dismissed. Every other state auto-dismisses at 4s. The 4s
timer pauses while the pointer is over the toast, and resumes on leave.**

**Why.** An error the user did not see is an error that did not happen — and errors are exactly
the toasts that carry something the user must act on. Success and info are confirmations; losing
one costs nothing. Pausing on hover is the general fix for "it vanished while I was reading it",
and it costs nothing on toasts nobody looks at.

---

## R11 — the categorical chart palette

**Three series, and the blocker was narrower than recorded.** `Graph Type=Line` is
**single-series by design** — what an earlier pass read as "a second series with no colour" is
the gradient area fill under the one line. Only `Grouped Bar` needs categorical colours, and it
binds three raw hexes.

| Series | Measured | Build | |
|---|---|---|---|
| 1 | `#a1cdfe` | **`--gw-color-primary-200`** `#99c6ff` | unbound token |
| 2 | `#9784ff` | **`--gw-color-chart-violet`** `#9784ff` — **new token** | genuine gap |
| 3 | `#fed14a` | **`--gw-color-yellow-200`** `#fcd34d` | unbound token |

**Why two map and one does not.** Series 1 and 3 sit within ~11 and ~4 units of an existing ramp
step across 765 — differences no one can see, and far too close to be deliberate choices. They
are almost certainly those tokens, unbound. Series 2 is a violet, and **the system has no violet
or purple ramp at all**, so there is nothing to map it to and rounding it into blue would destroy
the categorical distinction that is the entire point.

**So `#9784ff` becomes a token rather than a hex.** It is added as `--gw-color-chart-violet`
under a new `chart` group — deliberately *not* as `violet-300` in a full ramp, because one
colour is not a ramp and inventing nine steps nobody drew would be worse than the problem.

**Three series is the ceiling.** That is what the palette supports and what `Grouped Bar` draws.
A fourth category is a finding to report, not a colour to pick.

**Line and Bar stay `--gw-color-primary-500`.** Single-series charts do not touch this palette.

---

## Withdrawn

| Ruling | Why |
|---|---|
| `Button` hover fills — `Primary` `neutral-900`, `Outline`/`Ghost` `neutral-25` | **All three were measured in Figma the whole time**, and all three were wrong: `neutral/850`, `neutral/35`, `neutral/50`. See `exports/dashboard/button.md`. |
| Text field hover `neutral-100` | Figma's `State=Hover` is identical to `Default`. Superseded by **R2**. |

Both were ruled on the belief that the source was silent. **Confirm the silence before you fill
it** — that is now a maintainer rule in `CONTRIBUTING.md`.

---

## Still genuinely open

Not ruled, because ruling them needs a decision no measurement supports and no default is
obviously right:

- **`section/Container` empty and loading states** are ruled *pending Figma* in
  `exports/dashboard/states.md`. They stay provisional until the component exists.
- **`controls/toggle` `Size=X-Small`** at 36 × 20 is likewise ruled pending Figma.
- **`Solutions` labels differ between navbar and footer** — `AI Search` vs `AI Search Agent`.
  Same destination, two names. A copy decision, not a system one.
- **`dropdown-options` `Style=Calendar` has no range affordance.** Building one means designing
  it; report the gap rather than inventing a range picker.
