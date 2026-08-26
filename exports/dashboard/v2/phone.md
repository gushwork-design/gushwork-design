# Phone shell — topbar, drawer, dock

Measured 26 Aug 2026 off **GW Dashbords** `Q9L6q38dEj3Qu1JkjiT13y`, section `phone` (`515:2414`):
frames `phone` (`515:2176`) and `phone-menu open` (`515:2307`), both **375 × 720**.

**This closes a gap that was open until now.** Every earlier version of `exports/dashboard/`
recorded that no phone or tablet dashboard spec existed, and told builds to scale the 1440 canvas
down instead. A phone design now exists. Below 600 use this file; from 600 up see **R17** in
`DECISIONS.md`.

**Scope: dashboard / product.**

---

## What is measured and what is not

The two frames are a **shell spec**. Neither contains page content — no cards, no tables, no
section headers. So everything here is the chrome, and any phone treatment of *content* is a
build decision, not a measurement. Two that have been ruled rather than measured are listed at
the bottom.

---

## `topbar` — phone

**375 × 60**, fill `neutral/50`, padding `px-16 py-14`, `SPACE_BETWEEN`, `clipsContent`.

⚠ **Bottom border is 1.5px `neutral/100`, not the desktop 1px.** 1.5 is the phone chrome weight
throughout both frames. It is not a scaling artefact — the frame is drawn 1:1 at 375.

| Part | Measured |
|---|---|
| `dashboard-title` | gap `spacing/8` |
| logo tile | **20 × 20**, fill `neutral/black`, holding a **10px** symbol |
| title | **Vert Grotesk Display Semibold 16**, line-height 1, `neutral/black`, nowrap |
| switcher caret | a **20 × 20** tile (`p-4`, `radius/4`) holding `CaretDown` **12px** |
| drawer trigger | `controls/tab` **36 × 36**, `radius/8`, 1px `neutral/200`, inner `p-4 radius/4`, `List` **16px** |

**The trigger sits alone at the far right** (x 323 of 375). Nothing else is in the right cluster —
the theme toggle is not in the topbar on phone. See `dock` below.

### ⚠ The logo tile is a SCALED instance

It reports padding **5** and radius **5** against a component defined at `spacing/8` and
`radius/8`, and renders 20 × 20 around a 10px glyph. 20/32 = 5/8 = 10/16 = **0.625** — it is the
desktop 32 × 32 tile at 62.5%.

Reproduce the **drawn** 20 × 20 and 10px glyph. For the corner, `radius/4` is the nearest real
token to the scaled 5; do not write a raw 5px, and do not carry `radius/8` across, which is
visibly rounder at this size. **Whether the phone tile should be its own component rather than a
62.5% instance is an open question.**

### ⚠ The title is a SIXTH display size

Vert Grotesk **Semibold 16** matches none of the five documented `Dashboard/display-*` steps
(44 / 36 / 28 / 22 / 20). Per **R15**, use the literal spec and say it has no token. See the gap
table in `README.md`.

---

## `sidebar` as a drawer — phone

Frame `515:2343`, **240 × 660**, at x **135**, y **60**.

- **Anchored RIGHT.** 135 + 240 = 375, so it slides in from the right edge, not the left.
- Starts **below** the 60px topbar and runs to the bottom.
- Fill `neutral/50`; **left border 1.5px `neutral/100`** — the mirror of the desktop rail's right
  border, at the phone weight.
- `SPACE_BETWEEN` vertical: nav groups at the top, a pinned group at the bottom. Same structure as
  the desktop rail.
- `list-groups` padding **12** (desktop is 20), gap `spacing/24`.

Rows are the measured `list-item`, unchanged from desktop:

| Part | Measured |
|---|---|
| group label | `px-8 py-4`, `radius/8`, **`body-10-sem`** uppercase on `neutral/400`, **23** tall |
| nav row | `p-8`, gap `spacing/8`, `radius/8`, icon **16**, label `button-14-med` on `neutral/900`, **32** tall |
| selected row | fill **`neutral/100`** |

⚠ **No scrim.** `515:2307` draws none — the strip of page beside the open drawer is unchanged.
There is no scrim token in the system either. If you need an outside-tap target, use a
transparent one; do not add a dim the design does not have.

⚠ **No user-card in the phone drawer.** The desktop rail pins a `control Kind=user` at the
bottom; this frame pins `Settings` and `Admin` groups there instead. Which of the two a phone
build should carry is **not settled** — the frame simply shows one product's choice.

---

## `dock` — the bottom-left cluster

Frame `515:2183`, at **left 20, bottom 20**, flex, gap **8**, cross-centred.

**This is where the theme toggle lives on phone.** It is not in the topbar.

| Part | Measured |
|---|---|
| refresh | `list-item` **36 × 36**, fill `neutral/white`, 1px `neutral/200`, `px-12 py-8`, `radius/12`, drop-shadow `0 16px 16px rgba(88,92,95,0.1)`, `ArrowsClockwise` 16. Its label is present but **hidden** — icon-only. |
| theme toggle | `controls/tab` **66 × 36**, fill `neutral/white`, 1px `neutral/200`, `p-4`, gap `spacing/2`, `radius/12`, effect **`Shadows/S3`** = `--gw-shadow-s3` exactly |
| toggle cells | 28 × 28 — active `neutral/black` fill at **`radius/8`**, inactive no fill at **`radius/4`**, glyphs 12px |

⚠ **The phone toggle carries a fill, a border and a shadow.** The desktop topbar toggle has
none of the three. Same component, different treatment by surface — do not carry one across.

The active/inactive radius split (8 vs 4) is the same correction recorded for the desktop toggle
in `README.md`.

**Omit the refresh button when the dashboard has nothing to sync.** A closed-out report has no
refresh; shipping the affordance anyway is a dead control.

---

## Ruled, not measured

Both are build decisions on top of a shell-only spec, and both are flagged where they are used.

1. **Content breakpoints below 600.** The frames show no page content, so the reflow of
   `card-layout`, the analytics column count and the display-ramp step-downs are ruled. See
   **R17**.
2. **`section-header` on phone.** The measured header (`276:560`) puts its qualifier inline
   beside the title, both at 16. That does not fit 375 under a 28px page title, so on phone the
   qualifier becomes a stacked subtext at `body-14-reg`, gap 4. **Phone only** — the measured
   inline treatment holds at every width from 600 up. Ruled with Utsav, 26 Aug 2026.
