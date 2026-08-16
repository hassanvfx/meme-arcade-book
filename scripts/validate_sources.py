"""Validate the committed public-source lock without requiring network access."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "research/source-registry.json").read_text(encoding="utf-8"))
LOCK = json.loads((ROOT / "research/source-lock.json").read_text(encoding="utf-8"))


def main() -> None:
    expected = {item["name"]: item["url"] for item in REGISTRY["repositories"]}
    locked = {item["name"]: item for item in LOCK["repositories"]}
    missing = sorted(set(expected) - set(locked))
    if missing:
        raise SystemExit("Source lock is incomplete; run make materialize-sources: " + ", ".join(missing))
    for name, url in expected.items():
        entry = locked[name]
        if entry["url"] != url or len(entry.get("revision", "")) != 40:
            raise SystemExit(f"Invalid source lock entry for {name}")
    print(f"Source lock validation passed for {len(expected)} repositories.")


if __name__ == "__main__":
    main()
