# Dashboard Button

## Which button?

**This is the dashboard/product button.** There is a *different* component with the
same name for marketing web.

| Surface | Component | Node | `Style` values |
|---|---|---|---|
| **Dashboard / product** | `Button` — this file | `2203:931` | `Primary`, `Outline`, `Ghost` |
| Marketing web | `Button` — see `exports/web/button.md` | `1457:668` | `Blue`, `Black`, `Outlined/ black`, `Outlined / white`, `Text/ black`, `Special/ With People`, `Special/ Glowing`, `White` |

**Both component sets are literally named `Button`, and both expose a property named
`Style` whose value sets are disjoint.** `Style=Primary` is valid here and invalid on
web. `Style=Blue` is valid on web and invalid here. If you are on a dashboard, the only
legal styles are the three below. Neither component's own rule text states its scope —
that is why this block exists.

Figma: group `button` (`2205:15680`), set `2203:931`.

---

## Variant properties — 108 variants (3 × 3 × 3 × 4), complete

| Property | Values | Default |
|---|---|---|
| `Style` | `Primary`, `Outline`, `Ghost` | `Primary` |
| `State` | `Default`, `Hover`, `Disabled` | `Default` |
| `Size` | `Small`, `Medium`, `Large` | `Small` |
| `Type` | `Text Only`, `Trailing Icon`, `Leading Icon`, `Icon Only` | `Text Only` |

Every combination exists. Variant names take the form
`Style=Primary, State=Default, Size=Small, Type=Text Only`.

## Action hierarchy — maps to `Style`

| Action | Style | Appearance |
|---|---|---|
| Primary | `Primary` | Black filled |
| Secondary | `Outline` | Outlined / black |
| Third, lowest emphasis | `Ghost` | Text only |

**Never use a blue fill on dashboards.** The tiers here are black / outlined / text
only. Blue remains valid as a status or signal colour — Info toasts, blue badges — the
ban is on button *fills*.

## Size

**Match the size of surrounding elements** (controls, table toolbars). Usually `Small`
or `Medium`. `Large` only when the context calls for it.

| Size | Dimensions (Text Only) | Icon size |
|---|---|---|
| `Small` | 88 × 28 | 16 × 16 |
| `Medium` | 115 × 44 | 18 × 18 |
| `Large` | 134 × 48 | 18 × 18 |

Width grows with content. Reference widths per `Type` at each size:

| Size | Text Only | Trailing / Leading Icon | Icon Only |
|---|---|---|---|
| `Small` | 88 | 112 | 28 × 28 |
| `Medium` | 115 | 141 | 44 × 44 |
| `Large` | 134 | 156 | 48 × 48 |

## Type

Pick by icon need: `Text Only`, `Leading Icon`, `Trailing Icon`, or `Icon Only`.

`Icon Only` + `Ghost` is the established pattern for table pagination arrows — see
`section-elements.md`.

## State

`Default` / `Hover` / `Disabled` are **interaction states, not a choice.** The component
handles them. Don't pick a state when composing; pick `Style`, `Size`, and `Type`.

## Structure

```
Type=Text Only        COMPONENT (HORIZONTAL auto-layout)
                      └── TEXT "Button text"

Type=Trailing Icon    ├── TEXT "Button text"
                      └── INSTANCE "Trailing Icon" → VECTOR

Type=Leading Icon     ├── INSTANCE "Icon" → VECTOR
                      └── TEXT "Button text"

Type=Icon Only        └── INSTANCE "Icon" → VECTOR
```

- All variants use horizontal auto-layout.
- Icons are **swappable instances** (instance swap) — any Phosphor icon. Use `Bold`
  weight inside buttons.
- `Style` controls fill/stroke appearance (solid, outlined, transparent).
- `State` controls interaction feedback.

## Label copy

Sentence case. Placeholder is `Button text` — replace it. Dashboard buttons are action
labels for the product, not marketing CTAs: `Export`, `Add campaign`, `Save changes`.
The `Book a Demo` rule in `foundation/voice.md` governs marketing CTAs and does not
apply to product actions.

## Type token

Button labels use the `Button/*` type ramp, not the Body ramp —
`--gw-text-button-12` / `-14` / `-16` from `foundation/tokens.css`. Line-height 1,
tracking 0; vertical centring comes from padding.

---

## Re-measured off the set, 7 Aug 2026

Earlier values here came from instances. Read off `2203:931`, symbol by symbol.

| | Fill / border | Label |
|---|---|---|
| `Primary` | **`--gw-color-neutral-black` `#0d0d0d`** — not `neutral-900` | `--gw-color-neutral-white` |
| `Outline` | **2px `--gw-color-neutral-100`**, no fill | `--gw-color-neutral-black` |
| `Ghost` | none | `--gw-color-neutral-black` |

**`Disabled` is three different treatments, not one.**

| | Disabled |
|---|---|
| `Primary` | fill swaps to **`--gw-color-neutral-200`**; the label stays **white** |
| `Outline` | border unchanged; label → **`--gw-color-neutral-250`** |
| `Ghost` | still no fill; label → **`--gw-color-neutral-250`** |

### Geometry — padding depends on `Size` **and** `Type`

| `Size` | Height | Radius | `Text Only` | With an icon | Label |
|---|---|---|---|---|---|
| `Small` | 28 | 8 | `px-12 py-8` | — | 12, leading 1 |
| `Medium` | 44 | 8 | `px-20 py-16` | `px-20 py-16` — **still symmetric** | `body-14-med` 14/20 |
| `Large` | 48 | **12** | `px-24 py-16` | **`pl-24 pr-20 py-16`** | 16, leading 1 |

**The asymmetry is `Large` + icon only.** `Large` `Text Only` is symmetric `px-24`, and `Medium`
stays symmetric even with an icon. Widths: `Small` 88 / 112 / 28□, `Medium` 115 / 141 / 44□,
`Large` 134 / 156 / 48□. Icon is 16 at `Small`, 18 above it; `gap-8`.

> An earlier revision of this section claimed Large was always asymmetric and that Disabled
> simply dimmed the label. Both were extrapolated from a single `Ghost` symbol and both were
> wrong — caught before shipping by reading `Primary` and `Outline` too.
