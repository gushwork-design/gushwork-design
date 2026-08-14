# Toast

> ## ⚠ THIS FILE IS AUTHORITATIVE — but a duplicate component now exists
>
> A second toast was built on the v2 sheet (`279:875`) with the **same geometry and colours** but
> **renamed properties** — `Tone` × `Theme` instead of `State` × `Mode`. That rename was not
> requested and is unresolved drift.
>
> **Use this component and this file.** The rulings here — 4s auto-dismiss, errors never
> auto-dismiss (**R10**), the 276px / ~32-character ceiling — have no equivalent in v2, and this is
> the set that is **published in the library**.
>
> Resolution needed: either delete the sheet copy, or rename its properties to match. See
> [`v2/feedback.md`](v2/feedback.md).

Set `1579:614` · **8 variants** · 360 wide.

| Property | Values |
|---|---|
| `Mode` | `Light`, `Dark` |
| `State` | `Error`, `Warning`, `Success`, `Info` |

**The properties are `Mode` × `State`.** An earlier version of this file called the second
one `Type` and listed a `CTA` boolean — neither exists.

## Appearance — from the set

Set `1579:614` · **8 variants** — `Mode` [`Light`, `Dark`] × `State` [`Error`, `Warning`, `Success`, `Info`].

Shared: 360 wide · `--gw-radius-8` · **padding `8px 16px`** (px-16, py-8 — an earlier revision
wrote this as `16px 8px`, which is the CSS shorthand for the opposite and was built that way) ·
gap `--gw-space-8` · `align-items: flex-start` ·
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

## Auto-dismiss — 4 seconds. RULED.

**Toasts auto-dismiss after 4 seconds.** `--gw-toast-dismiss` in `foundation/tokens.css`.
Ruled by Utsav, 7 Aug 2026. This file previously said the timeout was undefined; it no longer
is, and it must not be re-decided.

Three behaviours go with it, so a second toast never eats the first:

- **A new toast resets the timer**, it does not stack another one.
- **Manual dismiss clears the timer**, so nothing ghost-hides a later message.
- **Pair it with a live region** (`role="status"`) — a message that disappears in 4s must be
  announced when it appears.

**Both remaining questions are now RULED** — `DECISIONS.md` → **R10**.

- **`State=Error` does not auto-dismiss.** It stays until dismissed. An error the user did not
  see is an error that did not happen, and errors are exactly the toasts carrying something the
  user must act on. Success and info are confirmations — losing one costs nothing.
- **The timer pauses while the pointer is over the toast**, and on keyboard focus, resuming on
  leave. That is the general fix for "it vanished while I was reading it", and it costs nothing
  on the toasts nobody looks at.

An error toast that never auto-dismisses **must** have a reachable dismiss control.

There is **no CTA or action slot**. Do not add one.

## The message must fit one line — the width is measured

360 is a measured width and **is never widened to fit copy.** With the measured `px-16 py-8`
padding, the 20px status icon, the 16px close and 16px of gaps, the message column is exactly
**276px**:

```
360 − 16 − 16 (padding) − 20 (icon) − 16 (close) − 16 (2 gaps) = 276
```

At `--gw-text-body-16-med` that is roughly **32 characters**. Write to it. `Export ready —
40 pages` fits; `Export ready — 40 pages, last 28 days` wraps to two lines and looks broken
against the `align-items: flex-start` icon.

> An earlier revision of this section said **292px**, computed from the inverted `16px 8px`
> padding this file used to record. The padding is `px-16 py-8`, so the column is 276. If you
> wrote copy to 292, re-check it.

If the message genuinely cannot be said in 34 characters, that is a finding — not a reason to
stretch the component.
