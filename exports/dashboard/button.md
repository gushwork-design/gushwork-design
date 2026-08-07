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

Values previously in this file were written from instances. Measured on `2203:931`:

| | Fill / border | Label |
|---|---|---|
| `Primary` | **`--gw-color-neutral-black` `#0d0d0d`** — not `neutral-900` | `--gw-color-neutral-white` |
| `Outline` | **2px `--gw-color-neutral-100`** — not 1px `neutral-200`, and no fill | `--gw-color-neutral-black` |
| `Ghost` | none | `--gw-color-neutral-black` |
| any `Disabled` | unchanged | **`--gw-color-neutral-250` `#bcbec2`** |

| `Size` | Height | Text Only | With icon | Icon Only | Padding | Radius | Label |
|---|---|---|---|---|---|---|---|
| `Small` | 28 | 88 | 112 | 28 | — | 8 | 12 |
| `Medium` | 44 | 115 | 141 | 44 | `px-20 py-16` | **8** | `body-14-med` 14/20 |
| `Large` | 48 | 134 | 156 | 48 | **`pl-24 pr-20 py-16`** | **12** | 16, leading 1 |

**`Large` is radius 12 with asymmetric horizontal padding** — 24 leading, 20 trailing. Every
other size is radius 8 and symmetric. Neither is guessable from the smaller sizes.
