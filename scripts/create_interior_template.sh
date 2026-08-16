#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output="$root_dir/book/templates/lulu-us-trade-interior-template.docx"
pandoc "$root_dir/book/templates/template-source.md" --standalone --output "$output"
echo "Wrote $output"
