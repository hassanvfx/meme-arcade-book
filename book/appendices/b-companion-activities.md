# Appendix B: Companion Repository Activities

The companion is a reader bridge, not an online duplicate of this book. The canonical prose lives in the print corpus. Each chapter-end panel and GitHub Pages activity opens the original public repository or article directly, then provides a bounded task and an expected observation. This design keeps the public source authoritative for its own code and keeps the book from becoming a stale fork of a tutorial.

## How the bridge works

One committed manifest records, for every activity, the chapter, original source URL, optional article, repository/path, task, expected observation, evidence sheet, and QR identity. Generators use that one record to create the small GitHub Pages activity page and its printed QR panel. A broken link is therefore a build failure, not a correction that must be made independently in the site and the manuscript.

The QR code encodes the direct source URL. It does not encode a private application address, a tracking identity, or a page that mirrors source content. If the reader has the print book without a current site build, the code still points at the original material.

| Chapter area | Direct public source | Reader task | Expected result |
| --- | --- | --- | --- |
| Author context | WWDC14/Ultrakam article | Separate author history from app claims | A scope note |
| Native shell | SwiftUI/Combine article | Trace a publisher-to-view transition | A state-ownership sketch |
| Modularity | ios-framework and SPM article | Map library, test, and tandem-app direction | A dependency sketch |
| Persistence | ios-storage and DataStore article | Trace restore and observation boundaries | A restoration boundary |
| Async work | receipe-app | Follow request, cancellation, and visible failure state | An async ownership sketch |
| Network observation | rezona-api | Separate observed behavior from inference | A redacted request model |
| Web/player | GamePlayer | Examine policy, pager, reuse, lifecycle, and event boundaries | A bounded lifecycle diagram |
| Notifications | Pushscheduler | Identify plan, permission, request, and route ownership | A local-notification state flow |
| Extraction | ios-framework | Write a contract/fixture/forbidden-dependency proposal | A reusable boundary |

## A reader's evidence notebook

For every activity, write five short fields: the source revision or publication date; the file or section inspected; an observation; the claim the observation can support; and a limit on what it cannot support. This notebook prevents an attractive README sentence or an observed response from becoming a claim about an entire production system.

For source code, distinguish a public teaching implementation from a production prescription. Inspect its test target, configuration, error paths, and documented limitations before deciding a pattern is reusable. For an article, distinguish explanatory intent from a verified measurement or market claim. For a network observation, preserve only authorized, minimized, redacted evidence and never infer backend behavior that cannot be observed.

## Activity safety rules

Do not use the activities to probe systems without authorization. Do not submit credentials, copy cookies/tokens, publish payloads, redistribute game content, or treat a source repository as permission to access a live service. The Rezona material is an explicit boundary exercise: it teaches attributable evidence and client modeling, not a verdict about a company or backend.

GamePlayer activities may reference a catalog only after redistribution rights are confirmed. Until then, use local/synthetic references or inspect the source structure. The App Store card on the landing page is merely a public download bridge for MemeArcade, the App; it is not evidence for the book's market framing.

## Maintaining stable activities

When a source moves or a repository changes shape, update the manifest and evidence sheet together, regenerate QR assets/pages, validate every direct URL, and record the result in the ClineFlow journal. Never replace a missing source with copied course prose. If an activity can no longer be supported by a public source, retire or rewrite its claim before publishing a new print run.

The durable promise is simple: the book explains the architecture, the original public projects remain the executable references, and every bridge tells the reader exactly what to inspect and what conclusion it can honestly support.

## Bridge maintenance checklist

Before an edition or deployment, verify that every activity uses a direct `https` source URL; repository name/path are descriptive rather than a substitute for the URL; an evidence sheet exists; a task asks the reader to inspect a bounded behavior; and the expected observation is a conclusion a public source can support. Regenerate the QR assets from the manifest and scan a sample from a rendered proof on a real phone. Then build the site in production mode and click the CTA with a keyboard as well as a pointer.

When a public article becomes unavailable, do not use an archive or copied text as a quiet replacement. Mark the activity for editorial review, identify a current public source or remove the claim, update the chapter's prose if its evidence changes, and preserve the decision in the journal. This small discipline makes the bridge a durable reference tool instead of a fragile marketing layer.

## What an activity does not prove

An activity is a guided inspection, not certification of a reader's implementation. A GamePlayer exercise can demonstrate the public repository's pager structure and documented policy choices; it cannot prove the behavior, revenue, security posture, or content agreements of a different production app. A storage exercise can show a teaching implementation's persistence boundary; it cannot establish that encryption alone solves retention or account-policy questions. A network exercise can support a redacted observation of an authorized client; it cannot establish backend facts. Keeping these limits adjacent to the task helps readers develop evidence habits instead of transferring confidence from one context to another.

The same rule protects the private case study. The bridge must never become a route to private code, internal builds, credentials, endpoints, or unapproved product documents. Any activity that would require private implementation detail needs explicit human approval and normally should be redesigned around a public teaching source. The book's value comes from the architecture lens and the inspectable companions, not from pretending a private app is a downloadable course artifact.
