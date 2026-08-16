# Appendix F: Reproducible Interior Publishing Protocol

This repository produces the Lulu US Trade 6×9 **interior only**. It prints the assigned ISBN in the copyright page, but does not generate an exterior cover, spine, barcode placement, or Lulu wrap template. Lulu.com is the ISBN imprint and Waken AI Labs is the editorial brand. The approved visual is an interior title plate. Keeping that boundary explicit prevents the page-count-dependent cover work from being mistaken for an interior deliverable.

## One canonical corpus, several renditions

Published prose exists once in Markdown under `book/chapters/` plus approved front matter and appendices. The website is not a second course: it is a bridge that directs readers to original public repositories and articles. The print system makes a temporary rendition of the corpus with generated reader panels/QR codes, then converts it through a versioned DOCX template. Corrections always begin in canonical Markdown, never in the generated DOCX, QR panel, or PDF.

The public production record for this edition lives at [hassanvfx/meme-arcade-book](https://github.com/hassanvfx/meme-arcade-book). It contains the canonical publishing corpus, source locks, validation scripts, and reproducibility records; it is not a replacement for the original companion repositories and articles linked by the reader bridge.

```text
canonical Markdown + front matter + reader manifest
  → print rendition with generated source panels
  → versioned 6×9 DOCX template
  → LibreOffice headless PDF (authoritative)
  → normalization/flattening and Lulu audit
  → publication manifest with hashes, TOC, pages, validation
```

LibreOffice headless is the authoritative renderer for this project, using an isolated temporary profile for every conversion. This follows the reproducible `ai-on-mac` master-PDF pattern: the DOCX is rendered once through a deterministic command-line route, then committed assembly and PDF-audit scripts produce a traceable candidate. The renderer does not replace human judgment; page-by-page review and a physical proof remain mandatory.

## Assembly order and contents

The interior order follows the established `ai-on-mac` cadence: title plate, copyright, dedication, generated contents, About the Author, acknowledgements, courtesy page, ClineFlow preamble, chapters, then appendices. Chapter openers retain their dedicated layout and chapter ends receive generated direct-source reader panels.

The table of contents is generated only after rendered pagination is available. A script reads rendered page positions, writes entries, re-renders, and verifies the final positions. Never type printed page numbers into source Markdown. A last-minute paragraph, font substitution, or title adjustment can move every later page.

## Automated beta gate

Before a beta proof, run source-lock verification, Markdown/front-matter checks, chapter/evidence audits, direct reader-bridge/QR checks, the Docusaurus production build, DOCX/PDF construction, and preflight. The release manifest records manuscript/template/artwork hashes, source lock data, generated TOC entries, page count, validation output, and the master-PDF hash. It is a ledger of inputs and results, not a substitute for visual review.

## Lulu interior preflight

The final PDF must have 6×9-inch portrait single pages, no encryption, embedded fonts, safe margins/gutter, and appropriately prepared placed images. Transparency is flattened where the workflow requires it; placed interior imagery is audited against the 300 ppi target. The no-bleed template is intentional. A future full-bleed interior requires a different Lulu-aware template and a changed preflight, not merely a larger image.

Review every rendered page at print-relevant size: title plate, copyright/dedication cadence, TOC numbers, headings, running heads, folios, tables, diagrams, QR readability, widows/orphans, image sharpness, and blank-page behavior. A command can confirm dimensions and embedded resources; only a human can confirm that the book reads and looks finished.

## Release gates

The workflow stops for human approval at six points: market wording; any private-code reference; chapter/appendix manuscript text; interior artwork; final PDF visual review and Lulu settings; and the physical proof. Record each decision in the ClineFlow journal. Once a proof reveals an issue, make the correction in canonical Markdown or versioned assets, regenerate every dependent rendition, repeat preflight, and write a new manifest. Do not patch the final PDF by hand.

The handoff is therefore a reproducible, validated interior master and its manifest. The author separately creates the exterior wrap using Lulu's current template and the final confirmed page count.

## Beta-to-master checklist

1. Freeze a named beta from canonical Markdown and record its source/template/art hashes.
2. Generate reader panels and QR codes from the direct-source manifest; do not hand-edit them.
3. Render the DOCX through the authoritative LibreOffice-headless path to discover layout issues and produce the candidate master.
4. Derive the contents from the rendered pagination and rebuild until its entries agree with the final rendered pages.
5. Export the candidate master from LibreOffice headless with its isolated profile, then run exact page-size, single-page, font, image, transparency, margin/gutter, and encryption checks.
6. Render every page to images for a human page-by-page review. Check the title plate, opening cadence, tables, code, diagrams, QR contrast, and blank pages as carefully as prose.
7. Write a release manifest only after all automated gates pass, then obtain the required editorial/PDF/Lulu approvals and order a physical proof.

The proof is a test of the actual printing system, not a ceremonial final step. If it reveals clipped headings, a margin issue, soft image, unreadable QR, an awkward blank, or a pagination change, correct the source and rebuild the entire chain. The reproducibility record is valuable precisely because it makes that iteration controlled rather than mysterious.

## Page-by-page visual review rubric

A preflight tool can prove page dimensions, but it cannot tell whether a human reader can comfortably use the book. Render the candidate PDF to page images and review it in sequence. Begin with the structural pages: the title plate should look intentional at 6×9, copyright and dedication should have breathing room, the contents must agree with printed folios, and About/Acknowledgements/ClineFlow material should follow the planned cadence. Check each chapter opener for the blue title/rule/folio treatment inherited from the established production pattern. Check each chapter ending for a reader panel that clearly names the original public source and has enough QR contrast and physical size to scan.

For body pages, inspect the first and last line of each page, heading isolation, widow/orphan behavior, table wrapping, code samples, diagrams, URLs, and footnote/citation legibility. A forced page break can be correct when it protects a chapter opener, but a blank page that results from accidental overflow needs a source-level correction. Review at normal reading scale as well as zoomed scale; a page may be technically complete yet look crowded, asymmetrical, or visually abrupt at print size.

Image checks are editorial and technical. Confirm every placed image is intentional, attributed or approved, sharp enough for the final scale, and inside safe margins. Confirm that decorative art is limited to approved interior usage. This project contains no external front-cover proof: the turtle plate is an interior page, while the author separately owns the exterior wrap, spine, barcode, and Lulu cover-template work. Do not let a PDF thumbnail or a site image create the misleading impression that a cover has been delivered here.

Run a second pass specifically for accessibility and reader handoff. Large titles need sufficient contrast; tables must retain their column meanings when they wrap; code must not rely exclusively on color; QR panels must include a printed direct URL or source name so a reader is not blocked by a camera failure. Links on GitHub Pages should be keyboard reachable, use descriptive labels, and open original sources rather than a manuscript mirror. The app-download card must continue to state that MemeArcade, the App is the technical case study and that the $3B label is broader market framing, never an app valuation.

Finally compare the rendered master with the release manifest. The corpus hash, DOCX-template hash, interior artwork hashes, page count, final TOC entries, validation results, renderer declaration, and PDF hash should all match the candidate under review. If the document changes after review, it is a new candidate: regenerate the manifest, rerun the audit, and review the changed pages plus any pages whose pagination moved. This may seem strict, but it is the difference between a reproducible interior and a file that merely happened to print once.

## Edition control

Give every review artifact an edition label and a clear status: `draft`, `beta`, `release-candidate`, or `master`. A filename alone is not enough; record the status, date, source revision, exporter, and manifest hash in the journal. A beta may be shared for manuscript and layout comments, but it is not upload-ready. A release candidate is technically complete but still awaits visual/Lulu approval. A master is the exact approved interior whose manifest and PDF hash are handed to the author for the separate cover-wrap workflow.

Keep corrections narrow and traceable. If a reviewer changes a market sentence, revise its evidence sheet and citation record. If a page break changes, regenerate the TOC and inspect later folios. If a source bridge moves, update the manifest, QR asset, activity page, and chapter link together. If interior art changes, update its hash and repeat image review. These rules avoid a common publishing failure: a correct source tree paired with a stale PDF, or a correct PDF paired with a stale manifest.

Do not overwrite the previous approved master. Retain its manifest and review notes so that an edition can be reconstructed, compared, or rolled forward with intent. The process is deliberately conservative because print interiors have a long tail: readers, reviewers, and Lulu may interact with a file long after the repository has moved on.

One final rule keeps the system honest: a successful command is a recorded fact about that command, not an approval proxy. The source audit, site build, QR generator, DOCX conversion, PDF inspection, and manifest all reduce preventable errors. None can decide that a market sentence is fair, a private boundary is adequately generalized, a page is attractive, or a physical proof is acceptable. Those are human decisions, named and dated in the journal before the interior is called final.

That separation of automated evidence from human judgment is the publishing system's final control: reproducible mechanics serve editorial accountability, rather than replacing it.

It also keeps later editions understandable, auditable, and safe to revise.

That durable trail lets an editor verify exactly what was printed, why it was accepted, and which source changes require renewed review.
