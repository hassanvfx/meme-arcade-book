#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template="$root_dir/book/templates/lulu-us-trade-interior-template.docx"
output_dir="$root_dir/book/build"
prepared_dir="$(mktemp -d)"
trap 'rm -rf "$prepared_dir"' EXIT

[[ -f "$template" ]] || "$root_dir/scripts/create_interior_template.sh"
mkdir -p "$output_dir" "$prepared_dir/chapters"
files=("$root_dir/book/front-matter-before-toc.md" "$root_dir/book/front-matter-after-toc.md")
for source in "$root_dir"/book/chapters/[0-9][0-9]-*.md; do
  target="$prepared_dir/chapters/$(basename "$source")"
  python3 "$root_dir/scripts/prepare_print_chapter.py" "$source" "$target"
  files+=("$target")
done
for source in "$root_dir"/book/appendices/*.md; do
  target="$prepared_dir/chapters/$(basename "$source")"
  python3 "$root_dir/scripts/prepare_print_chapter.py" "$source" "$target"
  files+=("$target")
done
pandoc "${files[@]}" --metadata-file="$root_dir/book/manuscript.yaml" --reference-doc="$template" --lua-filter="$root_dir/scripts/book_layout.lua" --standalone --output="$output_dir/memearcade-interior.docx"
python3 "$root_dir/scripts/normalize_docx_trim.py" "$output_dir/memearcade-interior.docx"
echo "Wrote $output_dir/memearcade-interior.docx from the canonical Markdown corpus."
