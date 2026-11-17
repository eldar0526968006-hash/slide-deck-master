#!/usr/bin/env bash
# Export an HTML deck to PDF + PPTX next to it. Usage: tools/export-deck.sh decks/<name>/index.html
set -euo pipefail
deck="$1"; dir="$(dirname "$deck")"; name="$(basename "$dir")"
tmp="$(mktemp -d)"
root="$(cd "$(dirname "$0")/.." && pwd)"
abs="$(realpath "$deck")"
(cd /tmp && node "$root/tools/shoot-slides.cjs" "$abs" "$tmp" >/dev/null)
python3 "$root/tools/build-exports.py" "$deck" "$tmp" "$dir/$name"
rm -rf "$tmp"
