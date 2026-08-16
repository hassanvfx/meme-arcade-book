"""Normalize a Pandoc DOCX to Lulu's 6×9 non-bleed interior trim."""

from __future__ import annotations

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
ET.register_namespace("w", W)


def main() -> None:
    source = Path(sys.argv[1])
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        with zipfile.ZipFile(source) as archive:
            archive.extractall(folder)
        document = folder / "word/document.xml"
        tree = ET.parse(document)
        sizes = tree.findall(".//w:pgSz", NS)
        if not sizes:
            for section in tree.findall(".//w:sectPr", NS):
                sizes.append(ET.SubElement(section, f"{{{W}}}pgSz"))
        if not sizes:
            raise SystemExit("DOCX has no Word section properties")
        for size in sizes:
            size.set(f"{{{W}}}w", "8640")
            size.set(f"{{{W}}}h", "12960")
        for section in tree.findall(".//w:sectPr", NS):
            margins = section.find("w:pgMar", NS)
            if margins is None:
                margins = ET.SubElement(section, f"{{{W}}}pgMar")
            for name, value in {"top": "1080", "bottom": "1008", "left": "1008", "right": "1008", "gutter": "0"}.items():
                margins.set(f"{{{W}}}{name}", value)
        tree.write(document, encoding="utf-8", xml_declaration=True)
        rebuilt = folder / "normalized.docx"
        with zipfile.ZipFile(rebuilt, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in folder.rglob("*"):
                if path.is_file() and path != rebuilt:
                    archive.write(path, path.relative_to(folder))
        shutil.copy2(rebuilt, source)
    print(f"Normalized {source} to 6 × 9 in non-bleed trim.")


if __name__ == "__main__":
    main()
