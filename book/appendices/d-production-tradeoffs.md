# Appendix D: Production Trade-offs

Architecture is a sequence of choices made under product, safety, and operating constraints. The comparisons here are decision aids, not universal rankings. Start by naming the user outcome, the owner, the lifetime, the evidence required, and the failure behavior. Then choose the smallest mechanism that makes those properties clear.

## Interface ownership

| Decision | Prefer this when | Watch for | Review question |
| --- | --- | --- | --- |
| SwiftUI feature shell | Product state, navigation, composition, and accessibility semantics are primary | A view that silently owns service lifetimes | Which object owns the state transition? |
| UIKit container | Paging/scrolling/reuse behavior needs explicit lifecycle control | Duplicate route/product ownership | Can the container emit typed events to SwiftUI? |
| Native presentation | Device policy, account context, or accessibility must be authoritative | Rebuilding remote content unnecessarily | What cannot safely be delegated? |
| Web presentation | Content is provider-owned and constrained by an explicit policy | Treating remote navigation as trusted state | What origin/capability/lifetime is granted? |

SwiftUI and UIKit are not opposing teams. The useful seam is often a SwiftUI product shell that hosts a focused UIKit/WebKit capability. That arrangement makes it easier to isolate reuse and WebView lifecycle while preserving native ownership of routes, account decisions, overlays, and recovery communication.

## Loading and lifecycle

| Choice | Benefit | Cost | Evidence required before adoption |
| --- | --- | --- | --- |
| Lazy primary-only loading | Lower steady resource use and clearer ownership | First activation may be slower | Baseline activation timing and failure rate |
| Adjacent preparation | May improve expected-next transition | More memory/network/process pressure | Target-device measurements and rollback guardrail |
| Broad prewarming | Can hide one latency symptom | Expensive, stateful, hard to cancel | A demonstrated user outcome that smaller fixes cannot achieve |
| Reuse/reset | Bounded allocation and predictable cells | May discard in-progress remote state | Explicit user expectation and recovery behavior |

Visibility is not entitlement. A cell becoming visible does not automatically deserve a network task, WebView, or analytics session. Candidate, primary, active, leaving, and reused states provide a vocabulary for deciding which resources may exist. Measure on representative hardware, include interruption/memory-pressure paths, and keep a rollback path before treating a performance experiment as architecture.

## Data and concurrency

| Choice | Good fit | Failure to prevent |
| --- | --- | --- |
| Actor/service boundary | Shared transport/cache work with concurrent callers | Mutable cache races and unowned tasks |
| `@MainActor` view model | Visible state updates and cancellation on screen lifetime | Background mutation of UI state |
| Durable encrypted store | Device-owned values that survive relaunch | Saving secrets or unvalidated state by convenience |
| Ephemeral WebView store | Remote surfaces where cookie/history persistence is unnecessary | Cross-session state leakage |

Do not cache merely because a response is expensive. Define freshness, capacity, invalidation, cancellation, and what data is acceptable to retain. A restore is an untrusted input from an earlier version of the application; it should be decoded, migrated or rejected, and mapped to a safe visible state.

## Notifications and re-engagement

| Choice | Use when | Keep separate from |
| --- | --- | --- |
| Local notification | The device can schedule a known reminder without a server | APNs token/remote-campaign assumptions |
| Remote notification | A service needs to decide delivery from server-side state | Automatic route authority on receipt |
| Durable plan | The feature needs reconciliation across launch | System pending requests, which are a projection |
| Typed route request | A tap should be evaluated by native product policy | Direct navigation from opaque payload text |

Request permission in context, show the denied state gracefully, namespace only the requests a feature owns, and validate a route again at tap time. Notification copy, targeting, timing, and growth policy are product-specific; a scheduler component should never smuggle them into a generic API.

## Observability and publishing

Metrics answer whether something changed at aggregate scale; logs help reconstruct a bounded event; traces join a controlled lifecycle. None should routinely include raw URLs, tokens, cookies, payloads, account identifiers, or user content. Start with event names, outcome categories, duration buckets, and a short-lived non-user correlation strategy. Establish retention, access, and deletion rules before adding data.

For the book, the comparable trade-off is convenience versus provenance. A second web copy of the manuscript would be convenient but diverges. The reader bridge instead points to original public sources and records task/evidence/QR data in one manifest. The print pipeline favors deterministic generated artifacts, rendered-pagination TOC entries, and an isolated LibreOffice-headless final export over manual page numbers or an untracked hand-edited PDF.
