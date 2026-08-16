# Modern iOS Architecture: Deconstructing the $3B MemeArcade

By Hassan Uriostegui · Waken AI Labs

This repository is the production source for a 6×9 interior-only technical book and its GitHub Pages reader bridge. `book/chapters/` is the single source of published prose for the interior; GitHub Pages does **not** mirror the manuscript or act as the course source. It directs readers to the original public repositories and articles, while the print pipeline renders the canonical corpus into the Lulu-ready interior.

The repository never ships the MemeArcade product source. Public companion repositories support code-reading activities; production architecture is described through evidence sheets, diagrams, generalized examples, and approved short excerpts only.

## Start here

1. Run `./scripts/materialize-sources.sh` to clone the public reference repositories into ignored `cache/repositories/` and refresh `research/source-lock.json`.
2. Read [the research index](research/README.md), then complete the evidence sheets before expanding the manuscript.
3. Validate the reader bridge with `make validate-reader-bridge`, generate QR codes with `make qrcodes`, and build the site with `make site`.

## Publishing contract

The canonical Markdown is the manuscript for print, not a web copy of the course. GitHub Pages is a reader bridge: its activities and QR codes open the original public repositories and articles directly. The print route builds a DOCX with a versioned 6×9 reference template, exports a PDF through LibreOffice headless, derives the table of contents from rendered pagination, and records the result in a publication manifest. The deliverable is the interior only: the assigned ISBN is printed in the copyright page, while exterior cover, spine, barcode placement, and Lulu cover-template work are intentionally excluded.

See [the reproducible publishing protocol](book/appendices/reproducible-publishing-protocol.md) and the active [engineering journal](knowledge/journals/memearcade-book-execution.md).
