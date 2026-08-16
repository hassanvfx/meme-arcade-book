#!/usr/bin/env python3
"""Flatten the final interior master and reject unsafe PDF resources for Lulu."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter

RENDER_DPI = 300


def resolved(value: object) -> object:
    return value.get_object() if hasattr(value, "get_object") else value


def resources(page: object) -> dict:
    return resolved(page.get("/Resources", {}))  # type: ignore[union-attr, return-value]


def used_xobjects(page: object) -> set[str]:
    contents = page.get_contents()  # type: ignore[union-attr]
    if contents is None:
        return set()
    return set(re.findall(r"/([^\s/]+)\s+Do", contents.get_data().decode("latin-1", errors="ignore")))


def used_fonts(page: object) -> set[str]:
    """Return fonts that actually draw text, ignoring ReportLab's empty default BT block."""
    contents = page.get_contents()  # type: ignore[union-attr]
    if contents is None:
        return set()
    data = contents.get_data().decode("latin-1", errors="ignore")
    selections = list(re.finditer(r"/([^\s/]+)\s+[-+]?\d*\.?\d+\s+Tf", data))
    names: set[str] = set()
    for index, selection in enumerate(selections):
        end = selections[index + 1].start() if index + 1 < len(selections) else len(data)
        if re.search(r"\b(?:Tj|TJ)\b", data[selection.end() : end]):
            names.add(selection.group(1))
    return names


def has_transparency(page: object) -> bool:
    if resolved(page.get("/Group", {})).get("/S") == "/Transparency":  # type: ignore[union-attr]
        return True
    res = resources(page)
    for state in resolved(res.get("/ExtGState", {})).values():
        state = resolved(state)
        if state.get("/ca", 1) != 1 or state.get("/CA", 1) != 1 or state.get("/SMask") not in (None, "/None"):
            return True
    for name, item in resolved(res.get("/XObject", {})).items():
        if str(name).lstrip("/") not in used_xobjects(page):
            continue
        item = resolved(item)
        if item.get("/SMask") is not None or item.get("/Mask") is not None:
            return True
    return False


def embedded(font: object) -> bool:
    font = resolved(font)
    descriptor = resolved(font.get("/FontDescriptor", {}))
    if not descriptor:
        descendants = resolved(font.get("/DescendantFonts", []))
        if descendants:
            descriptor = resolved(descendants[0].get("/FontDescriptor", {}))
    return any(descriptor.get(key) is not None for key in ("/FontFile", "/FontFile2", "/FontFile3"))


def audit(pdf: Path) -> None:
    errors: list[str] = []
    for number, page in enumerate(PdfReader(str(pdf)).pages, 1):
        if has_transparency(page):
            errors.append(f"page {number}: transparency remains")
        selected_fonts = used_fonts(page)
        for name, font in resolved(resources(page).get("/Font", {})).items():
            if str(name).lstrip("/") in selected_fonts and not embedded(font):
                errors.append(f"page {number}: {name} is not embedded")
    if errors:
        raise SystemExit("Lulu resource audit failed:\n- " + "\n- ".join(errors))
    print(f"PASS: {pdf.name} has embedded fonts and no transparency resources.")


def rasterized_page(source: Path, number: int, folder: Path):
    prefix = folder / "page"
    subprocess.run([shutil.which("pdftoppm") or "pdftoppm", "-f", str(number), "-l", str(number), "-r", str(RENDER_DPI), "-png", str(source), str(prefix)], check=True)
    png = next(folder.glob("page-*.png"))
    with Image.open(png) as image:
        image.convert("RGB").save(folder / "opaque.pdf", "PDF", resolution=RENDER_DPI)
    return PdfReader(str(folder / "opaque.pdf")).pages[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    source = args.pdf.resolve()
    if args.audit_only:
        audit(source)
        return
    reader = PdfReader(str(source))
    # Page 1 is the image title plate and page 4 is the generated ReportLab
    # contents leaf; flatten both so the PDF never relies on base-14 fonts.
    targets = {1, 4} | {number for number, page in enumerate(reader.pages, 1) if has_transparency(page)}
    with tempfile.TemporaryDirectory(prefix="memearcade-lulu-") as temporary:
        writer = PdfWriter()
        for number, page in enumerate(reader.pages, 1):
            if number in targets:
                folder = Path(temporary) / str(number)
                folder.mkdir()
                page = rasterized_page(source, number, folder)
            writer.add_page(page)
        writer.add_metadata(reader.metadata or {})
        with source.open("wb") as handle:
            writer.write(handle)
    print("Flattened 300 ppi opaque pages: " + ", ".join(map(str, sorted(targets))))
    audit(source)


if __name__ == "__main__":
    main()
