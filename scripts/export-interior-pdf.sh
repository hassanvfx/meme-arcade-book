#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="$root_dir/book/build"
input="$build/memearcade-interior.docx"
raw="$build/memearcade-interior-raw.pdf"
output="$build/memearcade-interior.pdf"
soffice_bin="${SOFFICE_BIN:-soffice}"

[[ -f "$input" ]] || { echo "Missing DOCX; run make book first." >&2; exit 1; }
profile="$(mktemp -d)"
trap 'rm -rf "$profile"' EXIT
"$soffice_bin" -env:UserInstallation="file://$profile" --headless --convert-to pdf --outdir "$build" "$input"
mv "$build/memearcade-interior.pdf" "$raw"
python_bin="${PYTHON_BIN:-/Users/hassan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3}"
"$python_bin" "$root_dir/scripts/assemble_master.py" "$raw" "$output"
"$python_bin" "$root_dir/scripts/prepare_lulu_pdf.py" "$output"
rm -f "$raw"
echo "Wrote LibreOffice-headless interior master: $output"
echo "LULU CANDIDATE: audited for embedded fonts, 300 ppi full-page rasters, flattened transparency, and 6 × 9 trim."
echo "HUMAN REVIEW REQUIRED: approve the manuscript, private-boundary wording, visual proof, Lulu settings, and physical proof before upload."
