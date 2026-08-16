---
title: Native Scrolling, Web Gameplay
slug: gameplayer-native-scrolling-web-gameplay
---

# Native Scrolling, Web Gameplay

The first instinct for a feed of playable web games is often to put a `WKWebView` in every card and let the browser decide what happens. That creates a confusing product: a vertical drag can mean “move to the next game” or “scroll inside this page,” loading work starts for content the reader will never see, and a browser process quietly becomes the owner of the app's most visible interaction.

The better question is not whether WebKit is powerful enough. It is: **which runtime owns each interaction?** In this chapter, native iOS owns the feed, page selection, lifecycle, native affordances, and the security boundary. The remote game owns only its own HTML, JavaScript, and touch interaction after it becomes active.

## The engineering problem

A short-form game feed has two independent jobs. The feed must react to a confident vertical flick, settle on one item, update native chrome, and survive cell reuse. The active game must receive direct touches and load remote assets without making the rest of the application feel like a browser. If those jobs are assigned to the same scrolling surface, the team spends its time resolving gesture exceptions instead of defining a product model.

GamePlayer makes the split concrete. Its native pager owns the collection view, drag threshold, page settling, and refresh gesture. A reusable player cell owns one isolated web-game session and its loading or error presentation. A small SwiftUI bridge lets a SwiftUI application host the UIKit engine rather than asking SwiftUI to reproduce a performance-sensitive, full-screen paging primitive. This is not a vote against SwiftUI. It is a decision to use each framework at the boundary where it is strongest.

## A model a junior engineer can use

Think of the screen as three nested surfaces:

1. **The native shell** knows the app's navigation, safe areas, lifecycle, accessibility, loading state, and actions such as share or save.
2. **The native pager** knows which item is primary and when the user has expressed an intention to change it.
3. **The web stage** knows how to run one game once native code has deliberately granted it the active stage.

Only one page should be primary. That does not merely mean “the one most visible on screen.” It means one page has permission to receive game interaction and begin web work. Candidate pages may be prepared as native cells, but they should not all behave as live browser sessions. This turns an ambiguous scrolling problem into an explicit state transition:

```text
candidate → primary → active web session → leaving → reused/cleared
```

The state machine matters because collection-view reuse is not an implementation detail. A cell that once represented game A can later represent game B. Its web state, callbacks, progress indicator, and native footer must be reset before B is displayed. Otherwise a reader can see stale loading state, old artwork, or—worse—a previously loaded game in the wrong product context.

## Minimal implementation boundary

The following pseudocode is intentionally general. It describes ownership rather than a private implementation:

```swift
final class GameStageCell: UICollectionViewCell {
    func configure(candidate: Game) {
        clearSession()
        renderNativeMetadata(for: candidate)
    }

    func becomePrimary() {
        startWebSessionIfNeeded()
    }

    override func prepareForReuse() {
        super.prepareForReuse()
        clearSession()
    }
}
```

The pager, not the web view, decides when `becomePrimary()` is called. The web view, not the pager, receives game input once active. This small rule prevents a great many accidental couplings: a remote page cannot hijack vertical navigation, and a paging update does not require the page to expose its internal scroll position.

## Lifecycle is product architecture

`WKWebView` is expensive enough that a feed must make its lifetime visible in the architecture. Creating a browser for every catalog item makes resource use proportional to the catalog. Reuse makes it proportional to the visible viewport. Lazy activation makes network work proportional to reader intent.

That is why GamePlayer starts a game only for the primary page. It also uses ephemeral web storage, so browser data does not silently accumulate through a long game session. The policy is useful beyond games: any hybrid list with remote, heavy, or untrusted content benefits from a bounded number of active sessions and from a clear disposal point.

Preloading is not a default. A team can measure the perceived latency of the next game, memory pressure on its target devices, WebKit process churn, and the effect of a nearby preload. Only then can it decide whether a candidate should prepare more than native metadata. A blanket “previous/current/next” strategy may improve one demo while causing termination or jank in a real catalog. Measurement decides; architecture preserves the option.

## Gesture ownership: make the handoff visible

The most visible interaction in a game feed is a vertical movement, but that movement is ambiguous. Inside an active game it may mean steer, jump, drag an object, or scroll a game-owned interface. Outside the game it may mean move to the next stage. Letting two recognizers negotiate this implicitly produces the worst kind of bug: it feels intermittent because the winner depends on a particular page's HTML, touch target, and timing.

GamePlayer resolves the ambiguity with native ownership of the pager. Its collection view does not use the ordinary free-scrolling behavior; it installs a pan gesture and calculates a target index from distance and velocity thresholds. The public controller uses a completion-progress threshold and a velocity threshold, then snaps to a bounded page index. It also reserves a pull-to-refresh interaction at the first page. These implementation details matter less than the product rule: a native policy decides whether the reader meant to navigate, and only the selected stage becomes interactive.

There are other valid designs. A feed might provide an explicit next/previous affordance, reserve a native footer gesture region, require a deliberate swipe from an edge, or use an onboarding overlay to teach the handoff. Choose the model that makes the game controls reliable and is understandable with assistive technologies. What does not scale is asking each remote game to cooperate with an undocumented native scroll convention.

| Interaction | Owner | Why |
| --- | --- | --- |
| Vertical page transition | Native pager | It changes product selection and lifecycle |
| Direct game touch | Active WebView | It belongs to the playable surface |
| Like/share/more actions | Native overlay | It invokes product policy and device features |
| Pull-to-refresh at feed start | Native pager | It refreshes catalog-level state |
| Loading/error/retry | Native stage container | It remains available when remote content fails |

This allocation supports accessibility as well as performance. The native shell can expose a labeled page position, provide an accessible action to advance, retain focus around a loading transition, and present an error that VoiceOver users can discover. A remote game can remain independently accessible within its own content. Neither layer should have to infer the other's semantic structure.

## The candidate-to-primary transition

The public pager stores a current index, updates the collection view's offset, and informs visible cells when the active page changes. The player cell receives a playback state; when it is primary it becomes visible and interactive, and only then runs `loadIfNecessary()`. During reuse, it cancels the avatar request, clears its item, stops loading, replaces the document content, and resets its native interface.

That sequence is a compact lifecycle contract:

```text
Candidate cell
  ├── renders title, creator, actions, and placeholder state
  ├── does not begin remote game work
  ▼
Primary cell
  ├── enables WebView interaction
  ├── starts one bounded load for the current item
  ├── reports loading/success/failure through native UI
  ▼
Leaving or reuse
  ├── disables interaction
  ├── cancels ancillary work
  ├── clears document and visual state
  └── may become a candidate for another item
```

The important invariant is identity. A completion for game A must not update a cell that now represents game B. In the public component, the cell's `configure` path resets before assigning a new item and tracks whether the current item has already begun loading. A more elaborate player may use session IDs, task handles, or a dedicated state machine. The architecture is the same: every callback must be tied to the active item and ignored once ownership changes.

## Native chrome is not cosmetic

The stage cell includes native metadata and action controls—creator, title, description, and like/share/more actions—above the remote game. This has a structural advantage: product actions are not dependent on a page implementing the right JavaScript command. The native app can apply account rules, share-sheet policy, accessibility labels, analytics redaction, and error behavior in one place. The game remains playable without becoming a source of authority for the surrounding product.

For a larger application, actions should leave the cell as typed product-neutral events. The cell can say “the active item received a share intent”; an application coordinator decides whether the user is eligible, which share representation is valid, and which native route to present. This avoids coupling a reusable feed component to account state, backend mutations, or a global navigation controller.

```swift
// Illustrative contract; not a private implementation.
enum StageAction { case like, share, more }

struct StageEvent: Sendable {
    var reference: GameReference
    var action: StageAction
}

// The pager emits StageEvent; the application owns its product consequence.
```

The distinction becomes essential if the same player is used in a signed-out preview, a full app session, or a moderation review. The visual affordance can be the same while the product's response differs by policy.

## Test the seams, not just the swipe

GamePlayer includes focused catalog and navigation tests alongside UI tests. That is the right direction. A pager is difficult to validate only with screenshots because the interesting failures occur across state transitions: a short drag should settle back; a fast flick should move one page; an attempt to advance at the end should remain bounded; a refresh should not leave an invisible spinner; an unsafe URL should be rejected before it becomes a web session.

Test at three levels:

1. **Pure policy tests** for URL validation, index calculation, and catalog record validation.
2. **Component tests** for cell reuse, active/inactive state, loading/error presentation, and callback identity.
3. **Journey tests** for a real launch, a page change, a failed game, an accessibility action, and a return to a stable native surface.

The tests should deliberately use fixture URLs and approved content. GamePlayer's README says to redistribute game catalog data only with permission from platforms and creators. This book follows the same boundary: it explains the architecture but does not establish redistribution rights for any game catalog.

## The WebView is a trust boundary

Remote games are not native views wearing a different renderer. They are untrusted web content with their own redirects, asset requests, storage behavior, and failure modes. GamePlayer's public policy is intentionally narrow: HTTPS navigation is allowed; `http`, `file`, `data`, `javascript`, custom schemes, and invalid URLs are cancelled; each player uses a non-persistent data store; there is no JavaScript bridge and no native script injection.

This model makes the default capability small. If a product later needs a native-to-web message bridge, that bridge should be designed as an API with a schema, allowlisted commands, origin checks, validation, observability, and a revocation strategy. It should never be introduced as a convenience callback. Likewise, allowing any HTTPS host is a practical public-component default, not the end state for a curated production catalog. A known provider set should lead to an explicit host allowlist.

## From public component to product integration

MemeArcade has the same responsibility categories inside a larger product: a SwiftUI application root and product state, a dedicated UIKit/WebKit vertical-pager module, catalog/feed services, persistence, native overlay surfaces, and fullscreen session coordination. The book does not reproduce its source or its catalog; any private excerpt requires explicit human approval. The useful architectural observation is that the player is not the application. It is a module with inputs from the product and callbacks back to the product.

That distinction protects both reuse and privacy. A portable player receives a candidate model, a lifecycle decision, a navigation policy, and typed callbacks for native actions. Product code supplies feed choices, account state, experimentation, copy, and navigation destinations. The module does not reach into a global app state to discover an endpoint or decide what a notification should say. When a team can draw that seam, it can test the pager with fixture games, replace a catalog source, and debug a web failure without turning every investigation into a full-app investigation.

## Senior trade-offs

The right implementation is rarely “all UIKit” or “all SwiftUI.” UIKit is a strong fit for a mature collection-view paging engine and reuse semantics. SwiftUI is a strong fit for application composition and isolated native surfaces that benefit from declarative state. WebKit is the required runtime for a remote browser game. The production decision is to minimize translation points: one owner for feed motion, one owner for web lifetime, and one owner for product navigation.

Observe those boundaries with events that answer operational questions: when a candidate became primary, when a web session began and ended, navigation-policy rejections, time to interactive, memory warnings, reuse counts, and whether a native action came from the active page. Avoid logging game URLs, private payloads, or user content unless there is an approved privacy policy. Good observability makes the architecture debuggable without widening the data surface.

## Companion activity

Open the GamePlayer activity linked at the end of this chapter. Trace the pager, stage cell, web-view factory, and navigation policy. Draw a lifecycle diagram with the states candidate, primary, active, leaving, and reused. Then write one sentence for every transition: who initiates it, what resource starts or stops, and what native state remains authoritative.

## Takeaway

Native code is not a thin wrapper around a game website. It is the orchestrator of reader intent, device lifecycle, performance budget, and trust policy. The web stage can stay expressive precisely because it is not also responsible for the application around it.
