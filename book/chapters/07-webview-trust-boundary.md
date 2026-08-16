---
title: Two Runtimes One Application
slug: webview-trust-boundary
---

# Two Runtimes, One Application: WebView as a Trust Boundary

`WKWebView` is not a decorative view. It is a second runtime inside an iOS application: it loads remote documents, executes JavaScript, manages browser storage, follows navigations, decodes media, and can be terminated or disrupted independently of the native process. A hybrid product becomes reliable only when it treats that runtime as a trust boundary.

The boundary is not an argument against web content. A remote game can iterate quickly, bring its own rendering and interaction model, and make a catalog of experiences practical without rebuilding every game as native UI. The native app contributes a different kind of value: it owns the device-level policy around the game. It decides when a page is active, which navigation is permitted, whether data is retained, how a failure appears, and which native capabilities a remote page may request.

The public [GamePlayer](https://github.com/hassanvfx/GamePlayer) repository makes those choices inspectable. Its `MAWebViewFactory` creates each view with a non-persistent `WKWebsiteDataStore`, JavaScript and inline/autoplay media enabled for gameplay, and a navigation delegate. `MAWebNavigationPolicy` allows only HTTPS URLs with a host; tests reject HTTP, `file:`, `data:`, `javascript:`, custom schemes, and invalid URLs. The player cell applies the policy to both navigation actions and responses, loads only when a page becomes primary, and exposes native action controls without installing a JavaScript bridge or injecting native script. Its README also records the critical trade-off: allowing any HTTPS host is flexible for CDNs and cross-domain assets, but a curated catalog should move toward an explicit host allowlist.

MemeArcade, the App, is described only through this generalized boundary. Its private source, URLs, policies, bridge decisions, and remote content are not published. Any private implementation excerpt or diagram beyond approved responsibility-level material requires explicit human approval.

## Name the two runtimes

The easiest mistake is to call the WebView “part of the app” and stop there. It is part of the user experience, but it does not automatically receive the app's authority. The native runtime and web runtime should have distinct capability sets.

| Capability | Native shell | Remote web content | Default posture |
| --- | --- | --- | --- |
| App navigation and presentation | Owns | Requests only through narrow contract | Native-owned |
| Game rendering and input | Hosts/contains | Owns inside authorized page | Web-owned |
| Device permissions | Requests and explains | No implicit authority | Native-owned |
| Cookies/web storage | Configures retention | Uses available web context | Minimize/ephemeral when appropriate |
| Deep links and external URLs | Validates/routs | Cannot silently open arbitrary schemes | Native policy |
| Product state restoration | Validates durable hints | Cannot assume a web process survives | Native-owned |
| Native actions | Implements | No access by default | Add only reviewed capabilities |

This division is a product decision. A game may legitimately need JavaScript, audio, touch input, and cross-origin assets. It does not therefore need arbitrary native routing, a way to invoke app features, or persistent cookies across every player session. The capability should be granted because a documented user experience requires it, not because a bridge is easy to add.

```
Native shell
  ├── selects an approved game reference
  ├── creates/configures isolated WebView
  ├── enforces navigation and lifecycle policy
  ├── renders native loading/error/recovery state
  └── owns device actions and product routing
                  │
                  ▼
        Remote page / game runtime
  ├── renders and handles game interaction
  ├── may load only approved navigation
  └── has no native authority by default
```

## Navigation policy is a gate, not a URL check in one place

GamePlayer's public policy is intentionally simple: require a nonempty HTTPS host. It applies the decision before a navigation starts and again when a navigation response arrives. Checking both matters because a request can redirect, a document can navigate, and an initially valid-looking action can lead somewhere a product did not intend to host.

The rule rejects several dangerous or inappropriate categories by default:

- `http` lacks the transport security requirement of HTTPS.
- `file` would point into a local-file context rather than remote approved content.
- `data` and `javascript` are executable/document schemes that should not be treated like a game URL.
- custom schemes can jump to a different app or capability and need their own explicit routing policy.
- missing or malformed URLs should fail closed, not be coerced into a request.

This is not a claim that HTTPS alone makes content trustworthy. HTTPS protects transport to the requested host; it does not evaluate a page's behavior, its third-party dependencies, or the appropriateness of every redirect. A mature catalog adds a source-of-truth rule: validated catalog data, a controlled provider allowlist, signed configuration, or another product-specific approval path.

| Policy level | Example rule | Benefit | Remaining risk |
| --- | --- | --- | --- |
| Scheme-only | HTTPS required | Blocks obvious unsafe/local schemes | Any HTTPS host may still be reached |
| Host allowlist | Hosts must match curated providers | Narrows remote surface | CDN/asset migration needs maintenance |
| Path/origin rules | Specific origins and paths allowed | Strongest predictable contract | Can be brittle if content evolves |
| User-mediated external route | Open external destination only after clear action | Preserves app context | Requires a deliberate UX path |

Choose the narrowest rule that supports the product. Do not silently widen it after a game fails to load. First determine whether the game is intended to use a new host, whether that host is under an acceptable provider relationship, and whether the user experience needs a visible external transition rather than an in-place navigation.

## Ephemeral data is a product choice

GamePlayer configures `.nonPersistent()` website data storage. In practical terms, the WebView's cookies and web storage do not accumulate as a long-lived shared browser profile across player sessions. That is a sensible default for a feed of independent remote games: a reused cell should not silently carry browsing identity or storage from one game into another.

Ephemeral storage has costs. A game may reload more often, lose an expected web-session preference, or require a new sign-in flow if the product legitimately supports web accounts. Persistent storage can improve continuity, but it creates a stronger data-retention obligation: define which origin shares the store, what it may retain, how it is cleared, and what a user expects after sign-out or account switch. There is no “free” default. There is only a storage policy that the product can explain.

The same caution applies to cache configuration. GamePlayer's player cell uses a reload-ignoring-local-cache request when it activates an item, while the app separately uses an avatar cache with URL, MIME, and size validation. These are different artifacts with different failure modes. A cache for a public image is not permission to persist a remote game session. Keep the purpose and retention of each store separate.

## JavaScript and bridges: grant the minimum capability

Interactive games commonly require JavaScript and media playback. The public factory enables both because disabling them would make many playable web experiences nonfunctional. That grant is bounded by the navigation and data-store rules around it. It does not imply that native code must inject script, expose `WKScriptMessageHandler`, or provide an arbitrary command channel to the page.

GamePlayer's public security model chooses no JavaScript bridge and no native script injection. This is a strong default for a generic remote-game host because every bridge message becomes an input-validation and versioning problem. If a product needs a bridge, define it as a small protocol rather than a bag of string commands:

```text
Web event:    { version, type, opaqueSessionReference }
Native checks: origin, schema, version, rate limit, active-session identity
Native result: a product-neutral event, never direct arbitrary method execution
```

The native side should reject unknown types, impossible state transitions, malformed values, messages from a non-primary session, and events that do not originate from the expected content context. It should not accept a web-supplied URL and load it, treat a web-supplied account identifier as authenticated truth, or allow a page to invoke privileged device actions. Keep bridge semantics observable with redacted event categories, and maintain compatibility intentionally when either runtime changes.

The best bridge is often no bridge. If a native overlay can own save, share, more, or exit actions—as GamePlayer's public cell demonstrates—then the web page does not need a route into those device capabilities. A native action handler can receive the already validated game reference and decide what the product is willing to do.

## Lifecycle is part of trust

A WebView may finish loading after its cell is reused, fail provisionally before a response exists, terminate under memory pressure, or become hidden after a paging transition. These are not just performance events. They are moments when stale content can be displayed in the wrong product context unless lifecycle ownership is explicit.

GamePlayer assigns the active page as the interactive primary page and lazy-loads it. Reused cells reset their interface and replace their web view before rendering a different item. The implementation handles finished and failed navigations with native loading/error UI; later chapters examine its memory and activation economics in more detail. The trust lesson here is that a page's authority should end with the session that created it. Reuse must not accidentally preserve a previous game's document, callbacks, or visual state.

On any failure, favor a native, understandable recovery path. The native container can show that a game could not load, offer retry if the reference remains valid, or return the user to a feed. It should not silently retry an unbounded number of times, carry an old WebView into a different item, or treat an invisible page as safe to keep doing work.

## A capability review for a hybrid feature

Before shipping a WebView host, review the feature as a table of grants:

| Question | Example decision |
| --- | --- |
| Which origins can the initial document and redirects reach? | HTTPS plus curated allowlist where feasible |
| Which storage survives the session? | Non-persistent by default; documented exception only |
| Is JavaScript needed? | Enable only if interactive content requires it |
| Is a bridge needed? | No by default; versioned, validated protocol if justified |
| How do external links behave? | Explicit native route or user-mediated handoff |
| What happens on failure/termination? | Native error state, bounded retry, safe return |
| What does the app log? | Redacted lifecycle/failure categories, never raw sensitive content |

The goal is not to prohibit rich web content. It is to ensure the product can answer what it has granted and why. A capability that nobody owns becomes an incident later.

## Keep authority on the side that can enforce it

Some responsibilities are tempting to delegate to the web page because the page is already displaying the game. Resist that shortcut when the responsibility depends on iOS policy or user consent. The remote page should not decide that a notification may be scheduled, that a native account is authenticated, that a deep link is safe, or that a file can be opened. It can request a narrowly defined experience; the native host validates the request against current application state and system permission.

Likewise, do not make the WebView a hidden session manager. A page can hold its own ephemeral game state while it is alive, but the application should not assume that state survives cell reuse, backgrounding, process termination, or a content update. If a user-facing recovery flow needs durable context, store the smallest native-owned, validated hint described in Chapter 4 and resolve it again under present policy.

This discipline reduces accidental privilege escalation. A compromised or simply buggy remote page has less ability to reach device resources, and a native product change has less chance of breaking the game by changing an undocumented bridge behavior. The boundary is also an organizational advantage: web and iOS teams can evolve independently when the contract is explicit, versioned, and narrow.

When a new capability is proposed, write a short decision record: user outcome, remote input shape, native validation, granted device action, failure behavior, logging/redaction policy, owner, and expiry/review date. If that record feels disproportionate, the capability may not justify a bridge at all. Simple native overlays and ordinary browser navigation are often safer than a permanent cross-runtime API.

The constraint is productive: it forces the experience to be explainable, testable, revocable, carefully observable, and safe under a changing remote runtime.

## Generalized MemeArcade view

The approved MemeArcade view is a native product shell that hosts remote content through an explicit WebView boundary: native code retains navigation, lifecycle, device policy, and product routing; remote content owns its authorized interactive surface. The public GamePlayer repository demonstrates one possible implementation with HTTPS-only navigation, non-persistent web data, no JavaScript bridge, and lazy activation. It is not proof that MemeArcade uses the same exact configuration.

No private MemeArcade hostnames, origins, WebView configuration, bridge protocol, headers, cookies, content, scripts, routes, source, security findings, or performance measurements are approved for publication. Any detail beyond the generalized responsibility map requires explicit human approval.

## Reader activity: make a capability table

Open [GamePlayer](https://github.com/hassanvfx/GamePlayer) directly. Inspect `MAWebNavigationPolicy`, `MAWebViewFactory`, the navigation tests, and the security-model section of its README. Create a two-column table for a hypothetical web game: “capability required for the game” and “native capability it must not receive by default.”

Then decide whether HTTPS-only policy is enough for that game or whether a host allowlist is required. State the operational cost of your choice. The expected observation is that a WebView is safest when every granted capability is deliberate, bounded, and owned by the native application.
