# Toast

Figma: group `toast` (`1553:14919`), set `1579:614`.

A brief, non-intrusive feedback message that appears temporarily to confirm an action or
report a status, without disrupting the user's flow.

## Variant properties — 8 variants (4 × 2), complete

| Property | Values |
|---|---|
| `State` | `Error`, `Warning`, `Success`, `Info` |
| `Mode` | `Light`, `Dark` |

| Node | Variant | Node | Variant |
|---|---|---|---|
| `1579:534` | `Mode=Light, State=Error` | `1579:574` | `Mode=Dark, State=Error` |
| `1579:544` | `Mode=Light, State=Warning` | `1579:584` | `Mode=Dark, State=Warning` |
| `1579:554` | `Mode=Light, State=Success` | `1579:594` | `Mode=Dark, State=Success` |
| `1579:564` | `Mode=Light, State=Info` | `1579:604` | `Mode=Dark, State=Info` |

All 360×40.

## Status — same colour-signal language as Badges and input states

| State | Colour | Meaning | Icon |
|---|---|---|---|
| `Error` | Red | A hard failure | `WarningCircle` |
| `Warning` | Yellow | A soft caution | `WarningCircle` |
| `Success` | Green | A completed action | `CheckCircle` |
| `Info` | Blue | Neutral information | `Info` |

`Error` and `Warning` share the `WarningCircle` icon and are distinguished by colour
alone. Colour tokens are in `foundation/tokens.css`; the signal vocabulary is defined
once in `foundation/shared-components.md` under Badge and inherited here.

**Note:** `Info` is the one place blue is a defined signal on the dashboard. The
dashboard ban on blue applies to *button fills*, not to status colour.

## Colour treatment

Each status has a `Light` and a `Dark` version. **Match it to the dashboard surface** —
light toast on light surfaces, dark on dark. Same discipline as Badge.

## Placement

Fixed **40px from the bottom, horizontally centred** on screen.

## Dismiss

Each toast has a close (`×`).

## Structure

```
toast (360×40)
├── FRAME (icon wrapper) — 20×24
│   └── INSTANCE [Status Icon] (20×20)
│       • WarningCircle  (Error, Warning)
│       • CheckCircle    (Success)
│       • Info           (Info)
├── FRAME (hidden/secondary content) — 149×40  [HIDDEN]
│   ├── INSTANCE "UserCircle" (20×20)
│   ├── TEXT (63×16)
│   └── TEXT (149×20)
├── TEXT "label" (276×24)        ← the toast message
└── FRAME (close button wrapper) — 16×24
    └── INSTANCE "X" (16×16)
```

**Keep it to one line of message.** The label slot is 276×24 — a single line at 16px.
Longer copy will clip. If the message needs two lines, it isn't a toast.

The 149×40 secondary-content frame is hidden in every variant. It holds a `UserCircle`
avatar and two text nodes, suggesting an unshipped attributed-notification variant. Leave
it hidden.

## Unresolved in the source

The rules text (`2146:17848`) contains two open author queries that have never been
answered, so these behaviours are **undefined**:

1. `[confirm surface-match + default]` — against the light/dark colour-treatment rule.
   Which `Mode` is the default when the surface is ambiguous is not stated.
2. `[confirm: also auto-dismiss after a timeout, or manual close only?]` — **whether
   toasts auto-dismiss is not defined.** The component ships a close button; no timeout
   is specified anywhere.

Do not invent a timeout value. If a request needs auto-dismiss timing, that is a ruling
to ask for, not a default to pick.
