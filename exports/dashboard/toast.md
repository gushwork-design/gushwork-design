# Toast

Set `1579:614` · **8 variants** · 360 wide.

| Property | Values |
|---|---|
| `Mode` | `Light`, `Dark` |
| `State` | `Error`, `Warning`, `Success`, `Info` |

**The properties are `Mode` × `State`.** An earlier version of this file called the second
one `Type` and listed a `CTA` boolean — neither exists.

## Appearance — from the set

Shared: 360 wide · `--gw-radius-8` · padding `16px 8px` · gap `--gw-space-8` ·
**1px border** · `align-items: flex-start` · `overflow: hidden`.

| `State` | Light fill | Light border | Icon |
|---|---|---|---|
| `Error` | `--gw-color-red-25` | `--gw-color-red-100` | `WarningCircle` |
| `Warning` | `--gw-color-yellow-25` | `--gw-color-yellow-100` | `WarningCircle` |
| `Success` | `--gw-color-green-25` | `--gw-color-green-100` | `CheckCircle` |
| `Info` | `--gw-color-primary-25` | `--gw-color-primary-100` | `Info` |

**`Mode=Dark` collapses all four to one treatment** — fill `--gw-color-neutral-900`, border
`--gw-color-neutral-800`. The state is then carried by the icon alone, not the surface.

| Part | Value |
|---|---|
| message | **`--gw-text-body-16-med`** · `--gw-color-neutral-900` light / `--gw-color-neutral-200` dark |
| status icon | **20px**, in a `padding-block: 2px` wrapper |
| close | `X` (`112:1590`) at **16px**, same 2px wrapper |

**`Error` and `Warning` share the same `WarningCircle` glyph** (`112:446`) — only the fill
colour separates them. Don't look for a distinct error icon.

## Auto-dismiss is still undefined

Nothing in the component specifies a timeout, and there is no CTA or action slot. Do not
invent either.
