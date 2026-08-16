"""Validate the manifest connecting chapters, activities, public sources, and QR targets."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest = json.loads((ROOT / "book/qrcode-manifest.json").read_text(encoding="utf-8"))
    if manifest["branch"] != "main" or not manifest["base_url"].startswith("https://hassanvfx.github.io/meme-arcade-book/"):
        raise SystemExit("Reader bridge must retain its stable GitHub Pages index.")
    ids: set[str] = set()
    for entry in manifest["chapters"]:
        if entry["id"] in ids:
            raise SystemExit(f"Duplicate chapter activity: {entry['id']}")
        ids.add(entry["id"])
        for key in ("chapter", "evidence"):
            if not (ROOT / entry[key]).is_file():
                raise SystemExit(f"Missing {key} for Chapter {entry['id']}: {entry[key]}")
        if not entry.get("source_url", "").startswith("https://"):
            raise SystemExit(f"Chapter {entry['id']} must link directly to its original public source.")
        if not all(entry.get(key) for key in ("activity", "expected")):
            raise SystemExit(f"Incomplete reader activity for Chapter {entry['id']}")
    print(f"Reader bridge validation passed for {len(ids)} activities.")


if __name__ == "__main__":
    main()
