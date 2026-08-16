#!/usr/bin/env python3
"""Verify generated TOC and reader panels in the assembled interior PDF."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "book/build/memearcade-interior.pdf"
PUBLICATION = ROOT / "book/build/publication-manifest.json"
BRIDGE = ROOT / "book/qrcode-manifest.json"
FOLIO_TITLE = "Modern iOS Architecture: Deconstructing the $3B MemeArcade"


def normalized(text: str) -> str:
    return "".join(re.findall(r"[a-z0-9]+", text.lower()))


def locate(reader: PdfReader, title: str) -> int | None:
    target = normalized(title)
    best_score = 0.0
    best_page: int | None = None
    for number, page in enumerate(reader.pages, 1):
        opening = normalized(page.extract_text() or "")[: len(target) * 3]
        score = SequenceMatcher(None, target, opening).ratio()
        if score > best_score:
            best_score, best_page = score, number
    return best_page if best_score >= 0.45 else None


def has_folio(page_text: str, page_number: int) -> bool:
    """The generated overlay is appended after source text in PDF extraction."""
    return page_text.rstrip().endswith(f"{FOLIO_TITLE}\n{page_number}")


def main() -> None:
    if not PDF.is_file() or not PUBLICATION.is_file():
        raise SystemExit("Build the interior master before validating generated print material.")
    reader = PdfReader(str(PDF))
    publication = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
    errors: list[str] = []

    toc_entries = publication.get("toc_entries", [])
    if len(toc_entries) != len(bridge["chapters"]):
        errors.append("TOC entry count does not match the chapter reader bridge")
    for entry in toc_entries:
        page = entry.get("page")
        actual = locate(reader, entry["title"])
        if not isinstance(page, int) or page < 1 or page > len(reader.pages):
            errors.append(f"TOC page is invalid for {entry['title']!r}: {page!r}")
        elif actual != page:
            errors.append(f"TOC page mismatch for {entry['title']!r}: manifest {page}, rendered {actual}")

    folios = publication.get("folios", {})
    first_folio = folios.get("first_physical_page")
    if not isinstance(first_folio, int) or first_folio < 1 or first_folio > len(reader.pages):
        errors.append(f"Folio start is invalid: {first_folio!r}")
    else:
        first_toc_page = toc_entries[0].get("page") if toc_entries else None
        if first_toc_page != first_folio:
            errors.append(f"First TOC folio mismatch: TOC {first_toc_page!r}, footer starts {first_folio}")
        for number, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            if number < first_folio and has_folio(text, number):
                errors.append(f"Front-matter page {number} unexpectedly has a folio")
            elif number >= first_folio and not has_folio(text, number):
                errors.append(f"Body page {number} is missing its physical-page folio")

    panel_pages = []
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        if "Explore the original public source" in text:
            panel_pages.append(number)
            if "QR code for the original public source" not in text:
                errors.append(f"Reader panel on page {number} has no generated QR mark")
            if "Source:" not in text or "Try:" not in text or "Expected:" not in text:
                errors.append(f"Reader panel on page {number} is incomplete")
    if len(panel_pages) != len(bridge["chapters"]):
        errors.append(f"Expected {len(bridge['chapters'])} reader panels, found {len(panel_pages)}")

    if errors:
        raise SystemExit("Print-interior validation failed:\n- " + "\n- ".join(errors))
    print(f"PASS: {len(toc_entries)} rendered TOC entries, physical-page folios, and {len(panel_pages)} QR reader panels match the interior.")


if __name__ == "__main__":
    main()
