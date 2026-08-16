"""Check that canonical chapters carry evidence, source, and audience boundaries."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "book/chapters"
APPENDICES = ROOT / "book/appendices"
FRONT_MATTER = [
    ROOT / "book/front-matter-before-toc.md",
    ROOT / "book/front-matter-after-toc.md",
]
MANIFEST = json.loads((ROOT / "book/qrcode-manifest.json").read_text(encoding="utf-8"))


def main() -> None:
    findings: list[str] = []
    word_count = 0
    manifest_chapters = {entry["chapter"]: entry for entry in MANIFEST["chapters"]}
    corpus_files = sorted(CHAPTERS.glob("[0-9][0-9]-*.md"))
    corpus_files += sorted(APPENDICES.glob("*.md"))
    corpus_files += [path for path in FRONT_MATTER if path.is_file()]
    for chapter in corpus_files:
        text = chapter.read_text(encoding="utf-8")
        word_count += len(re.findall(r"\b[\w'-]+\b", text))
        relative = str(chapter.relative_to(ROOT))
        if relative in manifest_chapters:
            evidence = ROOT / manifest_chapters[relative]["evidence"]
            if not evidence.is_file():
                findings.append(f"{relative}: missing evidence sheet {evidence.relative_to(ROOT)}")
        if "private" in text.lower() and "approval" not in text.lower():
            findings.append(f"{relative}: private-source discussion must state approval boundary")
    print(f"Canonical corpus: {word_count} words (target: 35,000–45,000).")
    if findings:
        raise SystemExit("Book audit failed:\n- " + "\n- ".join(findings))
    print("Book audit passed.")


if __name__ == "__main__":
    main()
