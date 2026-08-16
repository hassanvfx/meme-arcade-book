# Appendix E: ClineFlow Research Journal

The journal is the execution record for this interior-only publication. It answers a practical question that polished books often leave invisible: what evidence, decisions, tools, and approvals produced this exact manuscript and PDF? It is not a diary of every keystroke. It is a compact, reviewable record of material choices.

## What belongs in the journal

Every chapter or production milestone records the date, scope, source evidence, resolved public revisions, claims allowed by that evidence, excluded/private material, artifacts created, validation commands/results, human approvals needed, and next action. Material changes also receive a shorter entry in `knowledge/log.md`, making the project history easy to scan without replacing the fuller record.

| Record | Purpose | Example question it answers |
| --- | --- | --- |
| Source lock | Pin a public repository URL and commit | Which GamePlayer revision supported this wording? |
| Evidence sheet | Separate observation, claim, limit, and approval | Does this statement describe evidence or inference? |
| Decision record | Preserve a consequential editorial/technical choice | Why do QR codes open originals rather than a local course page? |
| Artifact record | Identify generated DOCX, PDF, QR, or manifest | Which inputs created the review master? |
| Validation record | Capture command and result | Did source links and the Docusaurus build pass? |
| Approval gate | Name a decision requiring a human | Has private-code wording or final PDF art been approved? |

## The chapter-close protocol

Before drafting, create or update an evidence sheet. Read the locked public source, identify only claims it can support, and write the private boundary in plain language. Draft from the canonical Markdown file, not from a duplicate web page or generated print copy. Add a direct reader activity only when a stable public source can support it.

At the chapter close, check the editorial contract: junior explanation, a small model/diagram, public implementation, generalized MemeArcade view, production trade-offs, reader task, sources, and an explicit limit. Update the journal and knowledge log, run `./validate-okf` plus the relevant book/bridge checks, then record their results. A passing structural command is evidence of structure; it is not editorial approval or a factual-market review.

## Approval gates are deliberate

Automation cannot decide whether market prose is fair, a diagram is legible, a private reference is sufficiently generalized, or a print page feels right. This project requires a human decision before publication for market claims, any private-code excerpt, manuscript text, interior artwork, final visual PDF review, Lulu configuration, and the physical proof.

Use clear statuses: **draft** means written but not approved; **evidence checked** means sources/limits were reviewed; **approved for beta** means it may enter a review PDF; **approved for release** means the authorized reviewer accepted it for the named edition. Do not convert an absent approval into a checked box because a build passed.

## Reproducibility and restraint

The journal also protects readers and collaborators. Full third-party article archives do not belong in Git; retain citation metadata and short permitted notes. Public repositories may be cached in ignored storage for inspection, but the committed lock preserves their source URL and commit. The private MemeArcade checkout is evidence only. Its code, secrets, internal endpoints, payloads, product data, and unapproved implementation details never become journal attachments or manuscript examples.

When a source is corrected, a link disappears, or an assumption changes, add a dated correction rather than silently rewriting history. Update the source lock/evidence sheet, revise only the canonical manuscript, regenerate dependent assets, rerun validation, and record the result. This is how a future edition can explain not just what it says, but why it was allowed to say it.
