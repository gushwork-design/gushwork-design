# Feedback — toast, tooltip, modal, empty-state, skeleton

Page `Dashboard Components` (`257:371`) in **`Q9L6q38dEj3Qu1JkjiT13y`** — the product file, not
the library. See `README.md` in this folder.

**Scope: dashboard / product.** Four of these five are **new** — the screens had none of them.

---

## ⚠ `toast` — a second component now exists, and its property names differ

Set `279:875` on the sheet · **8 variants**.

| | Library `toast` (`1579:614`) | Sheet `toast` (`279:875`) |
|---|---|---|
| Properties | `Mode` (`Light`/`Dark`) × `State` (`Error`/`Warning`/`Success`/`Info`) | `Theme` (`light`/`dark`) × `Tone` (`success`/`warning`/`error`/`info`) |
| Published | **yes** | no |
| Geometry | 360 × 40, `radius/8`, `px-16 py-8` | identical |

**The geometry and colours are the same; only the keys are renamed.** That renaming was not
requested and it is drift — two components, same job, incompatible property names.

**Use the library `toast` and `exports/dashboard/toast.md`.** That file stays authoritative,
including its rulings: 4s auto-dismiss, errors never auto-dismiss (**R10**), and the 276px /
~32-character message ceiling. The sheet copy exists so the section is visually complete; treat it
as a duplicate to be resolved, not as the spec.

**Resolved 14 Aug 2026 — renamed, not deleted.** The copy's keys are now `Mode` × `State`, matching
the library exactly, and it is renamed `toast (local copy of the library set)`. Deleting it was the
first instinct, but the library's dashboard page is **unpublished**, so its set cannot be imported
into this file — deleting would have left the Feedback section with no toast at all and no way to
instance the real one. The library set and `toast.md` remain authoritative.

Appearance, both files:

| Tone | Light fill | Light border | Icon + text | Dark |
|---|---|---|---|---|
| `success` | `green/25` | `green/100` | `green/500` | `neutral/900` + `neutral/800` border, white text, tone-coloured icon |
| `warning` | `yellow/25` | `yellow/100` | `yellow/500` | ” |
| `error` | `red/25` | `red/100` | `red/500` | ” |
| `info` | `primary/alpha-10` | `primary/100` | `primary/500-main` | ” |

Message text `body-12-med`, gap `spacing/8`, icon 16 Weight=Regular. `Mode=Dark` collapses all
four fills to `neutral/900` and **carries the state in the icon alone** — the v1 observation, and
it holds here.

---

## `tooltip`

Set `282:727` · **2 variants** (`Theme`).

**NEW.** The charts render an inline tooltip but no reusable component existed. Declared
13 Aug 2026.

`bubble` — `radius/8`, `py-8 px-12`, `body-12-med`. Plus a **10 × 6** arrow beneath, centred.

| Theme | Bubble | Text | Arrow |
|---|---|---|---|
| `light` | `neutral/900` | `neutral/white` | `neutral/900` |
| `dark` | `neutral/white` | `neutral/900` | `neutral/white` |

**`Theme=light` is the inverted one** — a dark bubble on a light surface, which is the
conventional reading. `Theme=dark` flips to white so it stays legible on a dark canvas. Name the
theme after the *surface*, not the bubble.

⚠ No pointer position variants — the arrow is bottom-centre only. Top, left and right are a
finding.

---

## `modal`

Set `283:864` · **2 variants** (`Theme`). **480 wide**, height hugs.

**NEW.** No dialog existed anywhere in the system. Declared 13 Aug 2026.

`radius/16`, padding `spacing/24`, gap `spacing/16`, effect style **`Shadows/S2`**
(`--gw-shadow-s2`).

- `header` — `SPACE_BETWEEN`: title **`Dashboard/display-22-med`** ⚠ no token, and a
  `icon-button Size=24` carrying `X` 16 Weight=Bold
- `body` — `body-14-med`, `neutral/500` / `neutral/300`, wraps
- `footer` — right-aligned (`MAX`), gap `spacing/8`: a `plain` button then a `primary` button

| Theme | Surface | Border | Title | Body | Close icon |
|---|---|---|---|---|---|
| `light` | `neutral/white` | 1px `neutral/100` | `neutral/black` | `neutral/500` | `neutral/600` |
| `dark` | `neutral/900` | 1px `neutral/800` | `neutral/white` | `neutral/300` | `neutral/300` |

⚠ **No overlay / scrim is included** — the component is the dialog only. There is no scrim token,
so a backdrop is a finding rather than a value to invent.

⚠ **No destructive treatment** — the v1 gap still stands. There is no destructive button style and
no red menu row; a delete confirmation uses the neutral primary.

---

## `empty-state`

Set `283:889` · **2 variants** (`Theme`). **480 wide**, height hugs.

**NEW.** Tables and charts had no zero-data state. `states.md` **ruled** empty and loading on
7 Aug 2026 as "compose from `section/Container`" — this is that ruling turned into a component.
`states.md`'s focus ruling is untouched and still mandatory.

Padding `spacing/40`, gap `spacing/16`, centred on both axes.

- `icon-circle` — **40 × 40**, `radius/full`, fill `neutral/50` / `neutral/800`, holding
  `MagnifyingGlass` 16 Weight=Regular on `neutral/400`
- `copy` — gap `spacing/8`, centre-aligned: title `body-16-sem`, body `body-12-med`
- a `primary` action button, `Size=36`

| Theme | Circle | Title | Body |
|---|---|---|---|
| `light` | `neutral/50` | `neutral/black` | `neutral/500` |
| `dark` | `neutral/800` | `neutral/white` | `neutral/300` |

The action is optional — hide it when there is nothing the user can do.

---

## `skeleton`

Set `282:734` · **6 variants** (3 × 2).

**NEW.** The loading screen (`lodaing`, 1440 × 888) implies a skeleton pattern but none existed.
Declared 13 Aug 2026.

| Type | Size | Radius |
|---|---|---|
| `line` | 280 × 12 | `radius/4` |
| `title` | 200 × 20 | `radius/4` |
| `block` | 320 × 96 | `radius/8` |

Fill `neutral/100` light / `neutral/800` dark. **Resize freely** — the dimensions are starting
points, not measurements.

⚠ **No shimmer animation is defined.** If you animate it, use `--gw-motion-*` and guard
`prefers-reduced-motion`. The absence of a documented shimmer is a gap.

The screens' actual loading state is a centred `Loading & fetching data…` heading over a
progress bar, not a skeleton — see `states.md`. Both are legitimate; the skeleton is for
in-place table and card loading, the progress bar for a whole-screen fetch.
