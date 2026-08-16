"""Compose the single Lulu interior master from rendered corpus pages."""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "book/assets/title/memearcade-interior-title-plate.png"
BLUE = HexColor("#29499B")
INK = HexColor("#202020")
SHORT_TITLE = "Modern iOS Architecture: Deconstructing the $3B MemeArcade"
FOLIO_FONT = "MemeArcadeTimesNewRoman"
FOLIO_FONT_PATH = Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_page(draw) -> PdfReader:
    stream = io.BytesIO()
    canvas = Canvas(stream, pagesize=(432, 648))
    draw(canvas, 432, 648)
    canvas.save()
    return PdfReader(io.BytesIO(stream.getvalue()))


def register_folio_font() -> None:
    """Embed the macOS TrueType face rather than emitting a base-14 footer font."""
    if FOLIO_FONT not in pdfmetrics.getRegisteredFontNames():
        if not FOLIO_FONT_PATH.is_file():
            raise SystemExit(f"Missing required folio font: {FOLIO_FONT_PATH}")
        pdfmetrics.registerFont(TTFont(FOLIO_FONT, str(FOLIO_FONT_PATH)))


def title_page() -> PdfReader:
    def draw(canvas, width, height):
        with Image.open(ART) as image:
            ratio = image.height / image.width
        placed_height = height
        placed_width = placed_height / ratio
        canvas.setFillColor(HexColor("#FFFFFF"))
        canvas.rect(0, 0, width, height, stroke=0, fill=1)
        canvas.drawImage(ImageReader(str(ART)), (width - placed_width) / 2, 0, placed_width, placed_height, mask="auto")
    return generated_page(draw)


def contents_page(entries: list[tuple[str, int | None]]) -> PdfReader:
    def draw(canvas, width, height):
        canvas.setFillColor(HexColor("#FCFBF7"))
        canvas.rect(0, 0, width, height, stroke=0, fill=1)
        canvas.setFillColor(BLUE)
        canvas.rect(54, height - 64, width - 108, 2, stroke=0, fill=1)
        canvas.setFillColor(HexColor("#111111"))
        canvas.setFont("Times-Bold", 22)
        canvas.drawString(54, height - 98, "Contents")
        y = height - 132
        for title, page in entries:
            canvas.setFont("Times-Roman", 10)
            canvas.drawString(54, y, title)
            if page is not None:
                number = str(page)
                canvas.setFont("Times-Bold", 10)
                canvas.drawRightString(width - 54, y, number)
                start = 54 + stringWidth(title, "Times-Roman", 10) + 8
                canvas.line(start, y - 2, width - 54 - stringWidth(number, "Times-Bold", 10) - 8, y - 2)
            y -= 18
        canvas.setFont("Times-Italic", 8)
        canvas.drawString(54, 35, "Generated from the rendered canonical manuscript.")
    return generated_page(draw)


def footer(page_number: int) -> PdfReader:
    """Return the ai-on-mac-style folio overlay for one physical page."""

    def draw(canvas, width, height):
        canvas.setStrokeColor(HexColor("#CCD4DC"))
        # Preserve the ai-on-mac footer treatment while keeping all printed
        # glyphs above this interior's 0.625-inch Lulu safe margin.
        canvas.line(54, 66, width - 54, 66)
        canvas.setFillColor(INK)
        canvas.setFont(FOLIO_FONT, 7.5)
        canvas.drawString(54, 52, SHORT_TITLE)
        canvas.drawRightString(width - 54, 52, str(page_number))

    return generated_page(draw)


def chapter_titles() -> list[str]:
    titles = []
    for path in sorted((ROOT / "book/chapters").glob("[0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if heading:
            titles.append(heading.group(1))
    return titles


def locate(reader: PdfReader, title: str) -> int | None:
    # Writer/PDF text extraction may introduce minor glyph artifacts (for
    # example ``Thee`` for ``The``). Compare each page opening with the
    # rendered heading and take the clearly best match; a word-overlap match
    # can otherwise select an earlier body page containing generic terms.
    target = "".join(re.findall(r"[a-z0-9]+", title.lower()))
    best_score = 0.0
    best_page: int | None = None
    for number, page in enumerate(reader.pages, 1):
        extracted = "".join(re.findall(r"[a-z0-9]+", (page.extract_text() or "").lower()))
        score = SequenceMatcher(None, target, extracted[: len(target) * 3]).ratio()
        if score > best_score:
            best_score = score
            best_page = number
    return best_page if best_score >= 0.45 else None


def main() -> None:
    source, output = map(Path, sys.argv[1:])
    if not ART.is_file():
        raise SystemExit(f"Missing interior title artwork: {ART}")
    register_folio_font()
    reader = PdfReader(str(source))
    titles = chapter_titles()
    entries = []
    for title in titles:
        rendered_page = locate(reader, title)
        entries.append((title, rendered_page + 2 if rendered_page is not None else None))
    first_chapter_rendered_page = locate(reader, titles[0]) if titles else None
    first_chapter_physical_page = (
        first_chapter_rendered_page + 2 if first_chapter_rendered_page is not None else None
    )
    writer = PdfWriter()
    writer.add_page(title_page().pages[0])
    # The first two rendered pages are copyright and dedication. The remaining
    # front matter belongs after the generated contents page.
    writer.add_page(reader.pages[0])
    writer.add_page(reader.pages[1])
    writer.add_page(contents_page(entries).pages[0])
    for rendered_page, page in enumerate(reader.pages[2:], start=3):
        if first_chapter_rendered_page is not None and rendered_page >= first_chapter_rendered_page:
            physical_page = rendered_page + 2
            page.merge_page(footer(physical_page).pages[0])
        writer.add_page(page)
    with output.open("wb") as handle:
        writer.write(handle)
    manifest = {
        "edition": "interior-only master",
        "interior_pdf": str(output.relative_to(ROOT)),
        "interior_sha256": digest(output),
        "source_pdf": str(source.relative_to(ROOT)),
        "source_sha256": digest(source),
        "title_art": {"path": str(ART.relative_to(ROOT)), "sha256": digest(ART)},
        "page_count": len(writer.pages),
        "toc_entries": [{"title": title, "page": page} for title, page in entries],
        "folios": {
            "start": "first rendered chapter heading",
            "first_physical_page": first_chapter_physical_page,
            "numbering": "physical page number",
            "footer_title": SHORT_TITLE,
            "font": "Times New Roman (embedded TrueType)",
            "front_matter": "unfoliated",
        },
    }
    (output.parent / "publication-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output} and publication manifest.")


if __name__ == "__main__":
    main()
