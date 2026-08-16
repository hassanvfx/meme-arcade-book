"""Generate stable SVG QR assets from the single reader-bridge manifest."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.graphics import renderSVG
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing

ROOT = Path(__file__).resolve().parents[1]


def write_svg(name: str, url: str, output: Path) -> dict[str, str]:
    widget = qr.QrCodeWidget(url)
    bounds = widget.getBounds()
    drawing = Drawing(bounds[2] - bounds[0], bounds[3] - bounds[1])
    drawing.add(widget)
    target = output / f"{name}.svg"
    renderSVG.drawToFile(drawing, str(target))
    return {"name": name, "url": url, "asset": str(target.relative_to(ROOT))}


def main() -> None:
    manifest = json.loads((ROOT / "book/qrcode-manifest.json").read_text(encoding="utf-8"))
    output = ROOT / "book/assets/qrcodes"
    output.mkdir(parents=True, exist_ok=True)
    entries = [write_svg("start-here", manifest["start_here"]["url"], output)]
    entries += [write_svg(f"chapter-{item['id']}", item["source_url"], output) for item in manifest["chapters"]]
    (output / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(entries)} QR assets.")


if __name__ == "__main__":
    main()
