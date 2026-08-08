#!/usr/bin/env bash
# Regenerate preview/changelog-sheet.html — the changelog as a rendered sheet.
#
# DERIVED, never hand-written, from the same source as every other release view:
# `scripts/_releases.sh`, which reads the version field out of `.claude-plugin/plugin.json`
# at every commit that moved it. Edit this script, not the HTML — the next run overwrites it.
#
# The sheet is built only from tokens in foundation/tokens.css and rules already verified in
# preview/_meta_ads_app.css. Anything not from those two is marked ADDED in the CSS below and
# has to be reported, per foundation/new-component-notice.md.
#
# Usage:  bash scripts/changelog-sheet.sh          # rewrite the sheet
#         bash scripts/changelog-sheet.sh --check  # exit 1 if it is out of date
set -euo pipefail
cd "$(dirname "$0")/.."
. scripts/_releases.sh

OUT="preview/changelog-sheet.html"

esc() { sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'; }

# "<uuid> <title>" -> an anchor. Bare titles render as plain text; nothing renders as an
# em dash, which is what "nobody could vouch for this" looks like.
session_cell() {
  local raw="${1:-}" uuid title
  if [ -z "$raw" ]; then printf '<span class="none">—</span>'; return; fi
  uuid="${raw%% *}"; title="${raw#* }"
  case "$uuid" in
    [0-9a-f]*-[0-9a-f]*-*)
      printf '<a class="lnk" href="claude://resume/%s" title="%s"><svg class="gl"><use href="#i-chat"/></svg><span>%s</span></a>' \
        "$uuid" "$(printf '%s' "$title" | esc)" "$(printf '%s' "$title" | esc)" ;;
    *) printf '<span class="none">%s</span>' "$(printf '%s' "$raw" | esc)" ;;
  esac
}

build() {
  local rows total current oldest first_date last_date md_rows md_missing
  rows="$(releases)"
  total="$(printf '%s\n' "$rows" | grep -c . || true)"
  current="$(printf '%s\n' "$rows" | head -1 | cut -d$'\x1f' -f1)"
  last_date="$(printf '%s\n' "$rows" | head -1 | cut -d$'\x1f' -f3)"
  oldest="$(printf '%s\n' "$rows" | tail -1 | cut -d$'\x1f' -f1)"
  first_date="$(printf '%s\n' "$rows" | tail -1 | cut -d$'\x1f' -f3)"

  # How far behind the subject-derived markdown log is. Counted, not asserted, so the
  # footer cannot go stale if changelog.sh is ever fixed to match.
  md_rows="$(grep -c '^| \*\*v' CHANGELOG.md 2>/dev/null || echo 0)"
  md_missing=$(( total - md_rows ))

  cat <<'HEAD'
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gushwork design system — changelog</title>
<link rel="stylesheet" href="../foundation/tokens.css">
<style>
  /* Every value below is a token or a rule already verified in preview/_meta_ads_app.css.
     Lines marked ADDED are new to this sheet and are listed in the footer note. */
  *,*::before,*::after{box-sizing:border-box}
  body{margin:0;background:var(--gw-color-neutral-100);
       font:var(--gw-text-body-14-reg);color:var(--gw-color-black);
       -webkit-font-smoothing:antialiased;
       display:flex;justify-content:center;
       padding:var(--gw-space-40) var(--gw-space-20)}
  .wrap{width:100%;max-width:1084px}   /* the measured dashboard section width */

  h1{margin:0 0 var(--gw-space-8);font:var(--gw-text-h5);
     letter-spacing:var(--gw-text-h5-tracking);color:var(--gw-color-neutral-900)}
  .sub{margin:0 0 var(--gw-space-24);max-width:70ch;
       font:var(--gw-text-body-14-reg);color:var(--gw-color-neutral-600)}
  .sub code{font:inherit;color:var(--gw-color-neutral-800)}

  /* stat strip — section/Container "With Dropdown" cells, verbatim */
  .cells{display:flex;align-items:stretch;gap:var(--gw-space-8);flex-wrap:wrap;
         background:var(--gw-color-white);border-radius:var(--gw-radius-12);
         padding:var(--gw-space-12);margin-bottom:var(--gw-space-20);
         box-shadow:var(--gw-shadow-s2)}
  .cell{min-width:100px;flex:1;padding:var(--gw-space-4) var(--gw-space-8);
        display:flex;flex-direction:column;gap:var(--gw-space-4);white-space:nowrap}
  .cell__l{font:500 10px/1.6 var(--gw-font-body);text-transform:uppercase;
           color:var(--gw-color-neutral-600)}
  .cell__v{font:500 18px/1.2 var(--gw-font-display);color:var(--gw-color-neutral-900)}
  .cell__sep{width:1px;align-self:stretch;background:var(--gw-color-neutral-100);flex:none}

  /* section shell — verbatim from the verified stylesheet */
  .sec{border-radius:var(--gw-radius-12);padding:var(--gw-space-12);
       background:var(--gw-color-neutral-25);display:flex;flex-direction:column;
       gap:var(--gw-space-12);overflow:hidden}
  .sec__hd{display:flex;align-items:center;justify-content:space-between;
           padding:var(--gw-space-4);width:100%;gap:var(--gw-space-12)}
  .sec__ttl{display:flex;align-items:center;gap:var(--gw-space-8);min-width:0}
  .sec__ico{width:20px;height:20px;border-radius:var(--gw-radius-4);padding:4px;flex:none;
            background:var(--gw-color-primary-alpha-10);color:var(--gw-color-primary-500);
            display:flex;align-items:center;justify-content:center}
  .sec__ico svg{width:12px;height:12px;display:block}
  .sec__t{font:600 14px/1 var(--gw-font-body);letter-spacing:-.2px;
          color:var(--gw-color-neutral-800)}
  .sec__c{font:var(--gw-text-body-12-med);color:var(--gw-color-neutral-500)}
  .sec__body{background:var(--gw-color-white);border:1px solid var(--gw-color-neutral-50);
             border-radius:var(--gw-radius-8);width:100%;overflow-x:auto}

  /* table — table-row measured 8 Aug 2026: padding 12/24, bottom border neutral-200,
     cells body-14-med neutral-600, header body-14-sem neutral-800, hover neutral-25 */
  .dt{width:100%;border-collapse:collapse;background:var(--gw-color-white)}
  .dt th,.dt td{text-align:left;padding:12px 24px;
                border-bottom:1px solid var(--gw-color-neutral-200);
                font:var(--gw-text-body-14-med);color:var(--gw-color-neutral-600);
                letter-spacing:-.028px;vertical-align:baseline}
  .dt th{font:var(--gw-text-body-14-sem);color:var(--gw-color-neutral-800);
         position:sticky;top:0;z-index:1;background:var(--gw-color-white)} /* ADDED: sticky */
  .dt tbody tr:hover{background:var(--gw-color-neutral-25)}
  .dt tr:last-child td{border-bottom:0}
  /* Only the summary wraps. `width:1%` on a nowrap column collapses it to its content, so
     "What changed" absorbs all the slack — the same rule the verified table uses to stop the
     action column growing. Without it the Session titles wrapped to two lines on every row. */
  .dt th:nth-child(1),.dt th:nth-child(2),.dt th:nth-child(4),.dt th:nth-child(5){width:1%}
  .dt td:nth-child(1),.dt td:nth-child(2),.dt td:nth-child(4),.dt td:nth-child(5){white-space:nowrap}
  .dt th:nth-child(3),.dt td:nth-child(3){width:auto;white-space:normal;
                                          color:var(--gw-color-neutral-800)}

  /* day divider — the verified .subttl treatment, spanning the row */
  .grp td{padding:var(--gw-space-12) 24px var(--gw-space-4);
          font:500 10px/1.6 var(--gw-font-body);text-transform:uppercase;
          letter-spacing:0;color:var(--gw-color-neutral-500);
          background:var(--gw-color-neutral-25);border-bottom:0}
  .grp:hover td{background:var(--gw-color-neutral-25)}

  .ver{font:var(--gw-text-body-14-sem);color:var(--gw-color-neutral-900);
       font-variant-numeric:tabular-nums}
  .sha{font-variant-numeric:tabular-nums}     /* Inter, not a mono face — two families only */
  .tm{font-variant-numeric:tabular-nums}

  .badge{display:inline-flex;align-items:center;padding:4px var(--gw-space-8);
         border-radius:var(--gw-radius-4);font:var(--gw-text-body-12-med);white-space:nowrap}
  .badge--n{background:var(--gw-color-neutral-100);color:var(--gw-color-neutral-600)}
  /* ADDED: a primary badge. New rule, no new colour — it is the primary-alpha-10 /
     primary-500 pairing the section icon tile already uses. */
  .badge--p{background:var(--gw-color-primary-alpha-10);color:var(--gw-color-primary-500)}
  .vcell{display:flex;align-items:center;gap:var(--gw-space-8)}

  .lnk{display:inline-flex;align-items:center;gap:var(--gw-space-4);
       color:var(--gw-color-primary-500);text-decoration:none;
       font:var(--gw-text-link-14);letter-spacing:var(--gw-text-link-14-tracking)}
  .lnk:hover{text-decoration:underline}
  .lnk:focus-visible{outline:var(--gw-focus-ring);outline-offset:var(--gw-focus-offset);
                     border-radius:var(--gw-radius-4)}
  .gl{width:14px;height:14px;flex:none;display:block;color:var(--gw-color-neutral-400)}
  .none{color:var(--gw-color-neutral-400)}

  .note{margin-top:var(--gw-space-20);padding:var(--gw-space-16);
        border-radius:var(--gw-radius-8);background:var(--gw-color-primary-25);
        border:1px solid var(--gw-color-primary-100);
        font:var(--gw-text-body-12-reg);color:var(--gw-color-neutral-700)}
  .note p{margin:0 0 var(--gw-space-8)}
  .note p:last-child{margin:0}
  .note code{font:inherit;color:var(--gw-color-neutral-900)}

  @media (max-width:767px){
    body{padding:var(--gw-space-20) var(--gw-space-16)}
    .cell__sep{display:none}
  }
</style></head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <!-- Phosphor. `fill` is re-applied to the symbol: it lives on the source <svg>, and
       stripping that wrapper drops it, which renders every path black. -->
  <symbol id="i-history" viewBox="0 0 256 256" fill="currentColor"><path d="M140,80v41.21l34.17,20.5a12,12,0,1,1-12.34,20.58l-40-24A12,12,0,0,1,116,128V80a12,12,0,0,1,24,0ZM128,28A99.38,99.38,0,0,0,57.24,57.34c-4.69,4.74-9,9.37-13.24,14V64a12,12,0,0,0-24,0v40a12,12,0,0,0,12,12H72a12,12,0,0,0,0-24H57.77C63,86,68.37,80.22,74.26,74.26a76,76,0,1,1,1.58,109,12,12,0,0,0-16.48,17.46A100,100,0,1,0,128,28Z"/></symbol>
  <symbol id="i-commit" viewBox="0 0 256 256" fill="currentColor"><path d="M248,120H183.42a56,56,0,0,0-110.84,0H8a8,8,0,0,0,0,16H72.58a56,56,0,0,0,110.84,0H248a8,8,0,0,0,0-16ZM128,168a40,40,0,1,1,40-40A40,40,0,0,1,128,168Z"/></symbol>
  <symbol id="i-chat" viewBox="0 0 256 256" fill="currentColor"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,210.93a16,16,0,0,0,20.24,20.24l34.05-11.35A104,104,0,1,0,128,24Zm0,192a87.87,87.87,0,0,1-44.06-11.81,8,8,0,0,0-6.54-.67L40,216,52.47,178.6a8,8,0,0,0-.66-6.54A88,88,0,1,1,128,216Z"/></symbol>
</svg>

<div class="wrap">
  <h1>Changelog</h1>
HEAD

  printf '  <p class="sub">Every version of the <code>gushwork-design</code> plugin, newest first.\n'
  printf '     Generated from git by <code>scripts/changelog-sheet.sh</code> — a release is a commit that\n'
  printf '     moved the <code>version</code> field in <code>.claude-plugin/plugin.json</code>, which is the\n'
  printf '     field <code>plugin update</code> actually compares.</p>\n\n'

  printf '  <div class="cells">\n'
  printf '    <div class="cell"><span class="cell__l">Releases</span><span class="cell__v">%s</span></div>\n' "$total"
  printf '    <div class="cell__sep"></div>\n'
  printf '    <div class="cell"><span class="cell__l">Current</span><span class="cell__v">v%s</span></div>\n' "$current"
  printf '    <div class="cell__sep"></div>\n'
  printf '    <div class="cell"><span class="cell__l">First shipped</span><span class="cell__v">%s</span></div>\n' "${first_date% *}"
  printf '    <div class="cell__sep"></div>\n'
  printf '    <div class="cell"><span class="cell__l">Last release</span><span class="cell__v">%s</span></div>\n' "${last_date% *}"
  printf '  </div>\n\n'

  printf '  <div class="sec">\n'
  printf '    <div class="sec__hd">\n'
  printf '      <div class="sec__ttl">\n'
  printf '        <span class="sec__ico"><svg><use href="#i-history"/></svg></span>\n'
  printf '        <span class="sec__t">Release history</span>\n'
  printf '      </div>\n'
  printf '      <span class="sec__c">%s releases · v%s → v%s</span>\n' "$total" "$oldest" "$current"
  printf '    </div>\n'
  printf '    <div class="sec__body">\n'
  printf '      <table class="dt">\n'
  printf '        <thead><tr><th>Version</th><th>Time</th><th>What changed</th><th>Commit</th><th>Session</th></tr></thead>\n'
  printf '        <tbody>\n'

  local day="" first=1
  while IFS=$'\x1f' read -r version sha date summary session; do
    [ -z "${version:-}" ] && continue
    if [ "${date% *}" != "$day" ]; then
      day="${date% *}"
      printf '        <tr class="grp"><td colspan="5">%s</td></tr>\n' "$day"
    fi

    # Patch releases are tagged so a fix is not read as a feature drop.
    local tag=""
    if [ "$first" = 1 ]; then
      tag=' <span class="badge badge--p">current</span>'; first=0
    else
      case "$version" in *.0) ;; *) tag=' <span class="badge badge--n">patch</span>' ;; esac
    fi

    printf '        <tr>\n'
    printf '          <td><span class="vcell"><span class="ver">v%s</span>%s</span></td>\n' "$version" "$tag"
    printf '          <td class="tm">%s</td>\n' "${date##* }"
    printf '          <td>%s</td>\n' "$(printf '%s' "$summary" | esc)"
    printf '          <td><a class="lnk" href="%s/commit/%s"><svg class="gl"><use href="#i-commit"/></svg><span class="sha">%s</span></a></td>\n' \
      "$REPO" "$sha" "${sha:0:7}"
    printf '          <td>%s</td>\n' "$(session_cell "$session")"
    printf '        </tr>\n'
  done <<< "$rows"

  printf '        </tbody>\n      </table>\n    </div>\n  </div>\n\n'
  printf '  <div class="note">\n'
  printf '    <p><strong>Why this sheet exists alongside CHANGELOG.md.</strong> The markdown log derives a\n'
  printf '    release from the commit <em>subject</em> — a row per commit titled <code>vX.Y.Z — …</code>.\n'
  printf '    That convention started at v1.19.0, so it lists <strong>%s of %s</strong> releases —\n' "$md_rows" "$total"
  printf '    %s missing, including <strong>v1.20.0, the login screen</strong>, whose commit was titled\n' "$md_missing"
  printf '    differently. This sheet derives from the version field in the manifest instead, so nothing\n'
  printf '    that shipped can be lost by writing a commit message the wrong way.</p>\n'

  cat <<'FOOT'
    <p><strong>The Session link only resolves on the machine holding the transcript.</strong> It
    is a pointer for the maintainer; for everyone else the commit link is the one that works. An
    em dash means nobody could vouch for the attribution — releases before v1.19.0 predate the
    <code>Session:</code> trailer, and guessing from transcript greps is unreliable because
    forked sessions duplicate each other's history.</p>
    <p><strong>Two additions to the system on this sheet</strong>, both new rules rather than new
    values: a sticky table header, and a primary badge reusing the
    <code>primary-alpha-10</code> / <code>primary-500</code> pairing the section icon tile already
    uses. No new colour, size, radius or shadow.</p>
  </div>
</div>
</body></html>
FOOT
}

if [ "${1:-}" = "--check" ]; then
  if ! diff -q <(build) "$OUT" >/dev/null 2>&1; then
    echo "$OUT is out of date — run: bash scripts/changelog-sheet.sh" >&2
    exit 1
  fi
  echo "$OUT is current."
else
  build > "$OUT"
  echo "Wrote $OUT — $(grep -c '<span class="ver">' "$OUT") releases."
fi
