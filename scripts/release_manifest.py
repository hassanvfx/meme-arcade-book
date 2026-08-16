"""Record deterministic inputs and output of the LibreOffice interior master."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    ROOT / "book/manuscript.yaml",
    ROOT / "book/lulu-distribution.yaml",
    ROOT / "book/front-matter-before-toc.md",
    ROOT / "book/front-matter-after-toc.md",
    ROOT / "book/templates/lulu-us-trade-interior-template.docx",
    ROOT / "book/templates/lulu-us-trade-6x9-no-bleed-v1.json",
    ROOT / "book/assets/title/memearcade-interior-title-plate.png",
    ROOT / "book/qrcode-manifest.json",
]


def main() -> None:
    output = ROOT / "book/build/release-manifest.json"
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in INPUTS if path.exists()}
    publication = ROOT / "book/build/publication-manifest.json"
    publication_data = json.loads(publication.read_text(encoding="utf-8")) if publication.exists() else {}
    template = json.loads((ROOT / "book/templates/lulu-us-trade-6x9-no-bleed-v1.json").read_text(encoding="utf-8"))
    pdf = ROOT / "book/build/memearcade-interior.pdf"
    soffice = os.environ.get("SOFFICE_BIN") or shutil.which("soffice")
    renderer_version = None
    if soffice:
        renderer_version = subprocess.run([soffice, "--version"], check=True, capture_output=True, text=True).stdout.strip()
    output.write_text(json.dumps({
        "generated_at": datetime.now(UTC).isoformat(),
        "kind": "interior-only Lulu master candidate",
        "export_authority": "LibreOffice headless with an isolated temporary profile; assembled and audited by the committed production scripts",
        "renderer": {"command": "soffice --headless", "version": renderer_version},
        "inputs_sha256": hashes,
        "template": template,
        "interior_pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None,
        "page_count": publication_data.get("page_count"),
        "generated_toc_entries": publication_data.get("toc_entries", []),
        "validation": {"trim": "make preflight", "fonts_and_transparency": "scripts/prepare_lulu_pdf.py --audit-only", "human_visual_review": "required"},
        "excludes": ["exterior cover", "spine", "barcode placement", "cover-wrap production"],
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
