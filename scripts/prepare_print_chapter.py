"""Create temporary print copies while preserving canonical site Markdown."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "book/qrcode-manifest.json").read_text(encoding="utf-8"))


def main() -> None:
    source, destination = map(Path, sys.argv[1:])
    text = re.sub(r"\A---\n.*?\n---\n", "", source.read_text(encoding="utf-8"), count=1, flags=re.DOTALL).rstrip()
    chapter_id = source.name[:2]
    activity = next((item for item in MANIFEST["chapters"] if item["id"] == chapter_id), None)
    if activity:
        article = f"\n\n**Companion article:** <{activity['article_url']}>" if activity.get("article_url") else ""
        repository_path = ""
        if activity.get("repository") and activity.get("path"):
            repository_path = f"\n\n**Repository path:** `{activity['repository']}/{activity['path']}`"
        qr = ROOT / "book/assets/qrcodes" / f"chapter-{chapter_id}.svg"
        if not qr.is_file():
            raise SystemExit(f"Missing QR asset for chapter {chapter_id}: {qr}")
        text += (
            f"\n\n\\newpage\n\n## Explore the original public source\n\n"
            f"![QR code for the original public source]({qr}){{ width=1.15in }}\n\n"
            f"**Source:** <{activity['source_url']}>{article}{repository_path}\n\n"
            f"**Try:** {activity['activity']}\n\n**Expected:** {activity['expected']}\n"
        )
    destination.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
