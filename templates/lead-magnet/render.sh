#!/bin/bash
# Renders lead-magnet.html -> lead-magnet.pdf (US Letter, 9pp). Run from this folder.
set -e
cd "$(dirname "$0")"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --allow-file-access-from-files --run-all-compositor-stages-before-draw \
  --virtual-time-budget=20000 --hide-scrollbars \
  --print-to-pdf="lead-magnet.pdf" "file://$PWD/lead-magnet.html" 2>/dev/null
echo "wrote lead-magnet.pdf"
