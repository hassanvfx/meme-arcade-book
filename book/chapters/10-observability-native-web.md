---
title: Seeing Across Native and Web
slug: observability-native-web
---

# Seeing Across Native and Web

A hybrid failure is rarely located where the user experiences it. A person sees “the game did not open.” The cause may be a stale catalog item, a rejected navigation, a slow network, a malformed response, an inactive cell, a WebContent process termination, a cancelled task, or a native route that was never applied. Without a shared vocabulary, each team investigates only its own runtime and the incident becomes a collection of partial stories.

Observability is the architecture that connects those stories without exporting private game data, user content, or raw browser traffic. It begins with an event grammar: an activation was requested, a candidate became primary, a session started, a policy allowed or rejected a navigation, a page finished or failed, a native action returned, and the session left or was reused. Each event answers a question about a state transition. None needs to contain a full URL, page body, cookie, account identifier, or touch trace.

The public components provide small examples. GamePlayer's pager already has native lifecycle boundaries—current-index changes, page-settle notifications, active/inactive cell state, navigation decisions, and native loading/error presentation. Recipe App's main-actor view model has explicit loading and API-failure state, while its logging service exposes distinct debug, info, warning, and error levels. These are ingredients, not a complete production telemetry system. The lesson is to turn them into a coherent cross-runtime trace with privacy and retention limits.

MemeArcade, the App, is discussed only in that generalized form. No private production log, trace, event schema, URL, game payload, user data, metric, source, or implementation excerpt is approved for publication. Any such material requires explicit human approval.

## Make events describe transitions

An event name should describe what changed, not what a developer happened to log while debugging. `primary_selected` is more useful than `cell 12 appeared`; `navigation_rejected` is more useful than `WK error`; `catalog_decode_failed` is more useful than a generic `error`. The event should be stable enough that an iOS engineer, web engineer, support lead, and product analyst use the same word for the same boundary.

Start with a small session model:

```text
native_route_requested
  → catalog_item_validated
  → candidate_configured
  → primary_selected
  → web_load_started
  → web_load_finished | web_load_failed | navigation_rejected
  → native_action_requested | session_left_primary
  → session_cleared | cell_reused
```

This is not a required sequence for every application. A cached item may skip a network stage; a reader may leave before a document starts; a failure may take the user to a native recovery screen. The value is that any path can be described without guesswork.

| Event | Native owner | What it establishes | What it must not include |
| --- | --- | --- | --- |
| `candidate_configured` | Pager/cell | A specific lifecycle slot has an item | Raw game URL or full catalog record |
| `primary_selected` | Pager | Native intent settled on a stage | Touch stream or user content |
| `web_load_started` | Player host | An authorized session began | Cookies, headers, request body |
| `navigation_rejected` | Policy | A navigation failed validation | Full rejected URL unless securely reviewed |
| `web_load_failed` | Player host | A bounded page load did not complete | Unredacted error object/payload |
| `session_left_primary` | Pager | The stage lost interaction authority | Behavioral profile of the user |
| `cell_reused` | Cell | Resources should no longer describe prior item | Prior content or session data |

For a junior engineer, this table turns logging from print statements into an ownership exercise. For a senior engineer, it creates a vocabulary for dashboards, alert thresholds, tests, and incident reports.

## Correlate without identifying the person

The native and web portions of one activation need a correlation key. A generated, short-lived session token can serve that purpose. It is created when native code selects a primary item and retired when the session leaves or is reused. It is not an account ID, a permanent game ID, or a hash of a URL. Its only job is to connect events that already belong to the same bounded native lifecycle.

```
session token S-123
  native: primary_selected
  native: web_load_started
  native: navigation_rejected
  native: session_left_primary
  native: session_cleared
```

If a reviewed bridge exists, the native host may attach the token to a small protocol event after validating origin and session identity. Do not put it into arbitrary page JavaScript, a query string, or browser storage by default. The less data crosses the runtime boundary, the easier it is to reason about its privacy, expiry, and revocation.

Correlation also has a time boundary. A session token should not survive product relaunch merely to make analytics convenient. If durable analysis needs a broader cohort, use a separate consented and privacy-reviewed mechanism. The player session trace is for diagnosing a short interaction, not reconstructing a person's history.

## Build a failure taxonomy before you need one

Recipe App distinguishes service-side decoding and server failures, and its view model makes loading/error state visible. GamePlayer distinguishes a failed navigation from a finished one and exposes a native error label. Combine those ideas into a taxonomy that describes recovery, not just cause:

| Category | Example trigger | Native response | Typical next action |
| --- | --- | --- | --- |
| Input invalid | Catalog record fails local validation | Do not create session | Refresh catalog or skip item |
| Policy rejected | URL/origin/scheme outside current policy | Stop before load | Return to safe native state |
| Transport unavailable | Offline, timeout, transient failure | Preserve clear error state | Retry if still primary |
| Response invalid | Decode/content contract failure | Reject unsafe result | Retry later or report provider issue |
| Web runtime failed | Provisional/load/process failure | Hide stale stage, show native recovery | Reload or leave stage |
| Obsolete completion | User selected another stage | Ignore result | No user-visible error |
| Native action failed | Share/route/permission denied | Explain boundary | Offer permitted alternative |

The category is more useful than an error string. It tells the UI what to show, tells support what to ask, and tells engineering where to start. Preserve low-level diagnostic material only in an appropriate reviewed environment; do not send it indiscriminately to analytics or display it verbatim to a user.

## Logs, metrics, and traces have different jobs

These terms are often mixed together. Separate them:

- **Logs** are discrete records for a developer or incident investigation. They should be structured, rate-limited, and redacted.
- **Metrics** are aggregate counts or durations: activation percentile, rejection rate, error category count, or successful recovery rate.
- **Traces** connect a bounded sequence of operations through a session/operation token.

Use logs when someone needs context, metrics when a team needs a trend, and traces when a team needs to reconstruct a single lifecycle. Do not turn every trace into a permanent log or every log line into a metric label. High-cardinality fields such as URLs, account IDs, error text, or content names can create privacy risk and operationally expensive dashboards.

The public Recipe App's logging examples are useful for teaching level selection, but a production hybrid application should audit what each message contains. Logging a full remote URL or file path may be inappropriate even if it helped during local development. Prefer categories and bounded details: `image_cache_miss`, `catalog_decode_failure`, `stage_load_duration_ms`, `navigation_rejected_scheme`. Use developer-only diagnostics under a controlled configuration when deeper detail is genuinely needed.

## Instrument the handoffs

The most valuable events occur when ownership changes. GamePlayer's native pager settles a page and updates which visible cell is primary. The stage cell starts a web load, then displays either success or a native error. The product can capture coarse timing around those handoffs:

```text
T0 primary_selected
T1 web_load_started
T2 web_load_finished | web_load_failed
T3 first_native_action | session_left_primary
T4 cell_reused
```

From that sequence, a team can derive useful metrics without knowing what content the reader played:

- Activation duration: `T2 - T0`.
- Time spent before leaving: `T3 - T2` when a session becomes active.
- Obsolete work rate: a load outcome after `session_left_primary`.
- Recovery rate: a failed session followed by a successful retry or safe return.
- Policy pressure: rejected navigations divided by attempted active sessions.

Each metric needs a product decision attached to it. A rising policy-rejection rate might mean a provider introduced a new trusted CDN, or it might reveal malformed catalog input. A slower activation percentile might justify a limited prewarm experiment only after validating device and content cohorts. Metrics reveal a question; they do not decide policy alone.

## Privacy is a feature requirement

“We will redact later” is not an observability strategy. Decide data classes before writing events. Categorize fields as forbidden, permitted aggregate, short-lived diagnostic, or explicitly approved sensitive data. Review the schema when adding a bridge, a new provider, a share action, or an account feature.

| Data class | Default | Examples |
| --- | --- | --- |
| Forbidden in routine telemetry | Never emit | Cookies, authorization headers, full payloads, page text, credentials |
| Avoid/high-cardinality | Do not use as labels | Raw URL, account ID, game title, free-form error |
| Permitted coarse signal | Aggregate or short-lived | Failure category, duration bucket, session lifecycle state |
| Reviewed diagnostic material | Controlled access and retention | Redacted trace necessary for an authorized incident |

Set retention deliberately. A real-time operational counter may need only aggregates; a sampled debugging trace may have a short expiry; a security incident may have a separate handling procedure. Give someone ownership of deletion and access. Observability that cannot explain its retention eventually becomes another unbounded store of product data.

## Diagnose an incident from the outside in

When a support report says “a game was blank,” resist opening every log source at once. Start with the user-visible transition: did the native pager select the intended stage; did the player present loading; did the page fail before a response, fail after a response, or never receive permission to navigate; did the user leave before completion; did a safe recovery route appear? The event grammar turns this into a sequence of answerable questions.

1. Locate the bounded native session or reproduction window.
2. Determine the last confirmed transition, not the last noisy log line.
3. Classify the failure using the taxonomy.
4. Inspect only the authorized detail necessary to distinguish the likely owner.
5. Choose a recovery, product fix, provider investigation, or policy adjustment.
6. Add a test or metric only if it will make the next occurrence cheaper to diagnose.

This workflow prevents an incident from becoming a request for more data by default. Often the missing piece is a state transition, not a raw payload. If a navigation was rejected, the important facts may be the policy category and the active-session state—not the entire rejected address. If a load was obsolete, the key fact is that the pager had already selected another item—not every byte of the first page.

Use a small incident record that separates evidence from conclusion:

| Field | Example form |
| --- | --- |
| User-visible outcome | “Stage showed a native retry state after selection.” |
| Observed transitions | `primary_selected → web_load_started → web_load_failed` |
| Confirmed boundary | Native player host observed failure callback |
| Unknowns | Remote service cause, content behavior, backend state |
| Recovery | Retry remains available while the item is current |
| Follow-up | Add a fixture that triggers the same failure category |

The “unknowns” row is essential. It protects a team from turning a diagnosis into a claim about an unobserved backend or remote page. It also directs work toward the next testable question.

Observability should improve the product as well as the on-call experience. If a repeated category cannot be explained to a user or recovered from in the UI, the missing work may be a product state—not a dashboard. A failure taxonomy is successful when it produces clearer retry affordances, safer route fallbacks, and fewer ambiguous blank screens.

Review the vocabulary after every meaningful product change. A new bridge message, account state, provider, or notification entry point adds a possible lifecycle branch. If the branch cannot be named, owned, and observed in a redacted form, it is not ready to be treated as routine production behavior. This discipline keeps the trace small enough to maintain, test, review, audit, and evolve safely under ongoing change, yet broad enough to explain the journeys the product actually offers.

## Generalized MemeArcade view

The approved MemeArcade lesson is a shared, privacy-aware native/web event vocabulary that can diagnose a bounded reader session from selection through recovery or release. Native code owns the session identity, route and policy transitions; the remote runtime is observed through its authorized, minimal integration points. This is not an assertion about private telemetry vendors, event names, dashboards, logs, payloads, URLs, or metrics.

No private production log, trace, analytics record, source, user data, game content, endpoint, identifier, security finding, or performance number is approved for publication. Any specific production evidence requires explicit human approval and a privacy review.

## Reader activity: write a failure taxonomy

Open [GamePlayer](https://github.com/hassanvfx/GamePlayer) directly, then compare its pager lifecycle, navigation policy, and load/error state with Recipe App's loading and service-failure states. Write six event names for one session and put every possible failure into one recovery category from the table above.

For each event, remove every field that is not required to understand the state transition. The expected observation is that a useful hybrid trace can explain what happened without retaining who the reader was, what they typed, or the full content that a remote page rendered.
