"""Objective Lulu interior checks; visual review remains a human gate."""

from __future__ import annotations

import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

POINTS = 72
EXPECTED = (6 * POINTS, 9 * POINTS)
# The no-bleed master reserves at least 0.625 in on every text edge. The
# normalized DOCX uses 0.70 in; this slightly lower threshold allows normal
# font bounding-box variance while protecting Lulu's safe text area.
SAFE_MARGIN = 45
RENDER_DPI = 300


def main() -> None:
    pdf = Path(sys.argv[1])
    reader = PdfReader(str(pdf))
    if not reader.pages:
        raise SystemExit("PDF contains no pages")
    errors = []
    for number, page in enumerate(reader.pages, 1):
        box = page.mediabox
        if abs(float(box.width) - EXPECTED[0]) > 2 or abs(float(box.height) - EXPECTED[1]) > 2:
            errors.append(f"page {number} is {float(box.width)/72:.2f} × {float(box.height)/72:.2f} in, not 6 × 9 in")
    if reader.is_encrypted:
        errors.append("PDF is encrypted")
    # This interior intentionally has only two full-page raster leaves: the
    # flattened interior title plate and generated contents page. They must
    # retain 300 ppi at the 6 × 9 trim size. QR codes are vector source art.
    minimum_pixels = (int(EXPECTED[0] / POINTS * RENDER_DPI), int(EXPECTED[1] / POINTS * RENDER_DPI))
    for number, page in enumerate(reader.pages, 1):
        for image in page.images:
            width, height = image.image.size
            if width < minimum_pixels[0] or height < minimum_pixels[1]:
                errors.append(
                    f"page {number}: raster {image.name} is {width} × {height}px; "
                    f"this full-page interior master requires at least {minimum_pixels[0]} × {minimum_pixels[1]}px (300 ppi)"
                )
    with pdfplumber.open(pdf) as layout:
        for number, page in enumerate(layout.pages, 1):
            # Page 1 is the approved full-page image title plate, with no
            # extractable body text. Subsequent text must remain inside the
            # no-bleed safe area on all four edges.
            chars = [char for char in page.chars if char["text"].strip()]
            if not chars:
                continue
            left = min(char["x0"] for char in chars)
            right = max(char["x1"] for char in chars)
            top = min(char["top"] for char in chars)
            bottom = max(char["bottom"] for char in chars)
            if left < SAFE_MARGIN or right > page.width - SAFE_MARGIN:
                errors.append(f"page {number}: text crosses the {SAFE_MARGIN / POINTS:.3f} in side safe margin")
            if top < SAFE_MARGIN or bottom > page.height - SAFE_MARGIN:
                errors.append(f"page {number}: text crosses the {SAFE_MARGIN / POINTS:.3f} in top/bottom safe margin")
    if errors:
        raise SystemExit("Interior preflight failed:\n- " + "\n- ".join(errors))
    print(
        f"PASS: {len(reader.pages)} portrait 6 × 9 in interior pages; not encrypted; "
        f"text stays within {SAFE_MARGIN / POINTS:.3f} in safe margins; full-page rasters are 300 ppi."
    )
    print("Manual gate: inspect final visual balance, typography, QR scanability, and all rendered pages.")


if __name__ == "__main__":
    main()
