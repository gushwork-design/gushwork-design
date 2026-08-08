# v1.24.0 — the dashboard surface is fully measured

**8 Aug 2026.** The last two components read off their sets. **All nineteen dashboard components
have now been checked against Figma. Seventeen had been recorded wrong.**

## `section/With Dropdown` — the transcribed tree was wrong in four places

The structure tree in `sections.md` came from Figma annotations, not the component. Reading
`2140:16131` corrects it:

| | Transcribed | **Measured** |
|---|---|---|
| Metric value | `20px` | **Vert Grotesk Display Medium 18**/1.2 |
| First data card | `6 cells + 2 compact` | **10 cells**, all identical |
| Second data card | `9 cells` | **6 cells** |
| Data card border | not stated | **none** |

**The data card has no border, and `section/Container`'s inner card does** (1px `neutral/50`).
Two sections that read as siblings are built differently — don't copy one's card into the other.

**Three text tiers, all 10px uppercase, separated only by colour**: metric label `neutral/600`,
sub-section title `neutral/500`. **The quieter colour is the heading**, which is backwards from
every other hierarchy in the system. Easy to get the wrong way round.

**The data row overflows its card.** It is drawn 1036 wide inside a 1028 content box, and
`overflow: clip` hides the last 8px. Build the row `width: 100%`.

Its header control is **`section/section-element/dropdown` `2142:583`, 466 wide — not
`controls/dropdown`**, which is a different component with different geometry. It carries **two
badges**, and the second is a green "Active" status that is part of the drawn component rather
than example content. Both badges are hand-built frames, not instances of the `badge` set, so
they inherit nothing from it.

## `section/table` — the caret is 12px off centre

**1084 × 674**, tiling exactly: `12 + 28 + 16 + 606 + 12`. The header is 1060 × 28 and the
container is 1060 × 606, holding a single `section/section-element/table` instance at full size.
The section is a shell; all the table's structure belongs to that element.

**✗ The collapse caret is not vertically centred.** The title block spans y 4–24 (centre 14); the
caret spans y 20–32 (centre 26). **12px apart**, and the caret's bottom overflows the 28-tall
header by 4. `section/Container` centres the two correctly, so this is `section/table` alone.
Build it centred and report the drift.

## Where the dashboard surface now stands

| | |
|---|---|
| Components checked | **19 of 19** |
| Recorded wrong | **17** |
| Correct as recorded | `section/Container`, and `table-row`'s hover ruling |

**Still provisional:** `table-row` `Type=Header` (3 variants) remains ruled rather than measured.
It is flagged as such in `section-elements.md`. Of the rulings checked in these two passes, one
was right, one described an element that does not exist, and three were wrong on values Figma
had all along — so an unread ruling is not worth trusting.

## What this pass changed about how the system works

Nothing about the components. Two things about the method, both already in `CONTRIBUTING.md`:

**A transcribed tree is not a measurement.** Both `section/With Dropdown` and `section/table` had
detailed-looking structure trees that came from annotation text. They read as authoritative and
were wrong in six places between them. The same class of error as a structure blob reporting
variant keys it does not own.

**Ruling is the riskiest thing a maintainer does.** Five rulings were checked across these two
passes. One held. The rest either contradicted a value Figma already carried, or invented an
element outright — `controls/dropdown`'s selected checkmark being the clearest case, since a
build following it renders an affordance the design does not have.
