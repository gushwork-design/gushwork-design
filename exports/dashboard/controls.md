# Controls — tab, dropdown, toggle

Figma: group `control` (`1578:744`).

Navigation, selection, and switching elements. Used inside `section/header`,
`section/table` toolbars and footers, and anywhere a dashboard needs in-place filtering.

**Scope: dashboard / product.**

---

## `controls/tab`

Set `1589:605` · **9 variants** (3 × 3), complete.

| Property | Values |
|---|---|
| `Size` | `Small`, `Medium`, `Large` |
| `Show` | `Selected`, `Hover`, `Default` |

| Node | Variant | Size |
|---|---|---|
| `1589:572` | `Size=Small, Show=Selected` | 230×28 |
| `1589:583` | `Size=Medium, Show=Selected` | 293×46 |
| `1589:594` | `Size=Large, Show=Selected` | 313×48 |
| `1590:617` | `Size=Small, Show=Hover` | 230×28 |
| `1590:628` | `Size=Small, Show=Default` | 230×28 |
| `1590:639` | `Size=Medium, Show=Hover` | 293×46 |
| `1590:650` | `Size=Medium, Show=Default` | 293×46 |
| `1590:661` | `Size=Large, Show=Hover` | 313×48 |
| `1590:672` | `Size=Large, Show=Default` | 313×48 |

Ships **5 tab items**. `Show` is an interaction state, not a choice — the component
handles it.

| Size | Outer pad | Item pad | Font |
|---|---|---|---|
| `Small` | 4 | 8 × 4 | 12px |
| `Medium` | 8 | 12 × 8 | 14px |
| `Large` | 8 | 12 × 8 | 16px |

`section/header` uses `Size=Medium, Show=Selected`.

```
COMPONENT (HORIZONTAL, gap:8, pad per size)
└── 5× FRAME "tab item" (HORIZONTAL, gap:4)
    └── TEXT "Tab"
```

---

## `controls/dropdown`

Set `1589:669` · **9 variants**.

| Property | Values |
|---|---|
| `Size` | `Small`, `Medium`, `Large` |
| `State` | `Closed`, `Open` |
| `Color` | `Grey`, `White` |

| Node | Variant | Size |
|---|---|---|
| `1589:606` | `Size=Small, State=Closed, Color=Grey` | 120×28 |
| `1589:612` | `Size=Medium, State=Closed, Color=Grey` | 144×44 |
| `1589:618` | `Size=Large, State=Closed, Color=Grey` | 170×48 |
| `1589:624` | `Size=Small, State=Open, Color=Grey` | 140×164 |
| `1589:639` | `Size=Medium, State=Open, Color=Grey` | 160×180 |
| `1589:654` | `Size=Large, State=Open, Color=Grey` | 180×192 |
| `2199:739` | `Size=Small, State=Closed, Color=White` | 96×28 |
| `2199:744` | `Size=Medium, State=Closed, Color=White` | 144×44 |
| `2199:749` | `Size=Large, State=Closed, Color=White` | 170×48 |

**`Color=White` exists in `Closed` only.** There is no `Color=White, State=Open`
variant — if you need an open white dropdown, that is a gap to report.

**The structure annotation (`2152:17853`) documents only `Size × State` = 6 variants and
never mentions `Color`.** The `Color` property is real and undocumented. Use the table
above, not the annotation.

Pick `Color` by the surface the trigger sits on — `Grey` on the default gray dashboard
canvas, `White` on a white panel.

```
State=Closed
COMPONENT (HORIZONTAL, gap:8, pad per size)
├── FRAME "content row" (HORIZONTAL, gap:4)
│   ├── INSTANCE "CalendarBlank" (leading icon, swappable)
│   └── TEXT label
└── INSTANCE "CaretDown" → VECTOR

State=Open
COMPONENT (VERTICAL, gap:4)
├── FRAME "trigger row" (same as Closed)
└── INSTANCE "input/dropdown-options" (VERTICAL, pad:4, gap:4)
    └── 4× FRAME "hover" (HORIZONTAL, pad:8) → TEXT "Option n"
```

| Size | Pad | Gap | Trigger font | Option font |
|---|---|---|---|---|
| `Small` | 8 | 8 | 12px | 12px |
| `Medium` | 12 | 12 | 14px | 12px |
| `Large` | 16 | 16 | 16px | 14px |

Note `State=Open` instances `input/dropdown-options` — the **web** input primitive —
rather than the dashboard `dropdown-options` (`2124:199`). Two different option-list
components are in play across the two dropdown families; see `section-elements.md`.

Used by `section/table` for the sort control and the page-size control, both at
`Size=Small`.

---

## `controls/toggle`

Set `1591:578` · **6 variants** (3 × 2), complete.

| Property | Values |
|---|---|
| `Size` | `Large`, `Medium`, `Small` |
| `State` | `Off`, `On` |

| Node | Variant | Size |
|---|---|---|
| `1591:572` | `Size=Large, State=Off` | 60×32 |
| `1591:573` | `Size=Medium, State=Off` | 52×28 |
| `1591:574` | `Size=Small, State=Off` | 44×24 |
| `1591:575` | `Size=Large, State=On` | 60×32 |
| `1591:576` | `Size=Medium, State=On` | 52×28 |
| `1591:577` | `Size=Small, State=On` | 44×24 |

```
State=Off   COMPONENT (HORIZONTAL, gap:4, pad:4)
            ├── FRAME "knob"
            └── FRAME "track space"

State=On    COMPONENT (HORIZONTAL, gap:4, pad:4)
            ├── FRAME "track space"   ← child order swapped
            └── FRAME "knob"
```

`On` and `Off` are the same tree with the child order reversed — the knob slides by
auto-layout, not by absolute positioning. `State` is bound to data, not a design choice.

---

## Source notes

The Controls description (`1578:749`) is accurate but generic. The group has **no
"Rules of Usage" text at all** — only a description and a Component Structure blob
(`2152:17853`), and that blob omits the `Color` property on `controls/dropdown`. The
usage guidance above is derived from how `section/header` and `section/table` actually
instance these controls.
