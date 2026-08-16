---
title: Async Await and Production Orchestration
slug: async-await-production-orchestration
---

# Async/Await: From Recipe App to Production Orchestration

`async` and `await` make asynchronous code easier to read, but they do not automatically make it correct. A network request can still outlive the screen that asked for it. A response can still arrive after the user selected something else. A cache can still return stale data. A decoding failure can still become a blank screen because nobody decided how to represent it. Production concurrency begins when work has an owner, a lifetime, and a user-visible outcome.

The public [receipe-app](https://github.com/hassanvfx/receipe-app) is a useful small laboratory. Its `RecipesViewModel` is `@MainActor` and publishes recipes, a selected recipe, an API error/message, and loading state. Its `APIService` is an actor that accepts a `URLSession` and a mock mode, exposes a high-level `fetchRecipes()` method, uses a generic `get` function for `Decodable & Sendable` responses, and maps decode/server failures into its own error cases. Its image cache is another actor: it returns a cached image when available or downloads one, then schedules a disk write in a detached background task. The repository's tests cover mocked valid, empty, and malformed recipe responses, plus cache behavior.

That is enough to teach the central production question: **when an asynchronous result arrives, is its owner still interested in it?** MemeArcade, the App, applies the same discipline to catalog/feed work and product services. The exact service types, endpoints, models, payloads, and implementation remain private. The reusable lesson is that network results must become validated product state through an explicit owner—not through whichever callback happens to finish last.

## A task needs an owner

Every asynchronous operation should answer three questions before it starts:

1. Which feature or coordinator requested this work?
2. Under what condition should the work be cancelled or ignored?
3. How will success, empty data, cancellation, and failure appear in product state?

The owner may be a view model, an application coordinator, a refresh controller, or a domain service. It should not be a transient SwiftUI view body. Views can appear repeatedly; recomputation is not a durable task lifetime. A view expresses an intent such as “refresh” or “select this item.” The owner starts the task, stores it if needed, and decides whether its result still applies.

```
User intent
    │
    ▼
Feature owner starts Task
    │                         cancellation / replacement
    ├──────► service actor ───────────────────────────────► stop or ignore
    │                    │
    │                    ▼
    │            transport + decode
    │                    │
    ▼                    ▼
validated domain result ──► main-actor product state ──► SwiftUI
```

The diagram separates a task from a result. Cancellation is cooperative: asking a task to cancel does not prove no work will finish. Therefore a feature owner should also identify a result. If a second refresh replaces the first, the first result should be ignored even if the underlying transport finishes after cancellation. A generation token, current request identifier, or identity comparison can make that rule explicit.

```swift
// Teaching sketch; not private MemeArcade code.
@MainActor
final class CatalogModel: ObservableObject {
    @Published private(set) var state: LoadState<[GameSummary]> = .idle
    private var task: Task<Void, Never>?
    private var generation = 0

    func refresh() {
        task?.cancel()
        generation += 1
        let requestGeneration = generation
        state = .loading

        task = Task {
            do {
                let items = try await service.fetchCatalog()
                guard !Task.isCancelled, requestGeneration == generation else { return }
                state = .loaded(items)
            } catch is CancellationError {
                // A replaced request is not a user-facing failure.
            } catch {
                guard requestGeneration == generation else { return }
                state = .failed(map(error))
            }
        }
    }
}
```

The exact `LoadState` design may vary, but the rule should not: do not let obsolete work overwrite newer user intent.

## Isolate mutable services, not user decisions

The Recipe App's `APIService` actor holds its session and mocking configuration. Its generic fetch function decodes off the main path and converts errors into a smaller service failure vocabulary. This is an important split. A service owns mutable transport-related concerns; a `@MainActor` view model owns UI state. Neither needs to know every detail of the other.

Actors are not merely a replacement for serial queues. They express that only one task at a time may touch an actor's isolated state. Use them for shared caches, request coordination, token refresh, or mutable service configuration. Do not use an actor as a dumping ground for UI decisions. A catalog service can say “these records decoded” or “the request failed”; it should not decide whether the app dismisses a player or selects a tab.

The same separation protects a hybrid application. The service that obtains a catalog is not the same owner as the WebView that renders a selected game. The product shell decides whether a validated catalog item becomes a route. The player feature decides whether its own activation task is still relevant. The web runtime cannot elevate a transport response into product authority by itself.

| Responsibility | Good owner | Must not decide |
| --- | --- | --- |
| Fetch and decode a resource | Service actor | App navigation or visible copy |
| Render loading/error state | Main-actor feature model | Transport implementation details |
| Choose whether a result still applies | Feature owner/coordinator | Server behavior it cannot observe |
| Cache bytes or images | Cache actor | Current product route |
| Validate remote data for a route | Product/feature policy | Private backend intent |

## Failure is a state, not a log line

The public recipe service distinguishes decoding failures, server failures, and an unknown URL construction failure. Its tests deliberately exercise valid, empty, and malformed responses. That is better than relying only on a happy-path live endpoint because it forces the application to say what each condition means.

An empty catalog is not necessarily an error. A malformed item may be skippable if the rest of the response remains useful, or it may indicate the response cannot be trusted. An offline failure may allow cached content. A policy rejection may require a hard stop. The mapping belongs near the product boundary, where a team can decide what the user sees and what privacy-safe evidence is recorded.

Avoid presenting raw `NSError` descriptions as product copy. They are unstable, often unhelpful, and can expose implementation context. Map low-level failures into a small set of user-facing states: retryable network problem, unavailable content, invalid response, permission required, or something went wrong. Preserve technical detail only in redacted logs where it is useful and authorized.

```
URLSession / decoding / policy errors
                 │
                 ▼
         domain failure category
                 │
        ┌────────┴────────┐
        ▼                 ▼
 user-facing recovery   privacy-safe observation
```

This keeps the UI honest without making it a diagnostic console.

## Cache is an optimization, not product truth

The Recipe App's `ImageCache` uses an actor, a file-system directory, a URL-derived file name, and a detached background write. It returns an image immediately after a network load rather than waiting for the disk write. Its own README identifies the trade-off: the file system is the cache's source of truth, and a stronger production design could add an in-memory index, reconciliation, a size budget, and eviction policy.

That is an excellent teaching moment. A cache exists to improve latency or reduce work. It must be disposable. If a cache becomes the only source from which an application can reconstruct critical product state, then it has become a database without the migration, consistency, or ownership design discussed in the previous chapter.

For a feed, cache catalog images or safe public assets when it helps the user experience. Bound the space, observe hit/miss behavior without recording sensitive URL data, and tolerate cache loss. Do not cache a remote permission, a privileged endpoint, or an unvalidated session as though it were durable authority. A cache miss should make the product slower, not incorrect.

| Cache choice | Benefit | Risk to manage |
| --- | --- | --- |
| In-memory cache | Fast reuse | Memory pressure and eviction |
| Disk cache | Survives process lifetime | Storage growth and stale files |
| Background write | Fast first render | Write may not finish before termination |
| URL-based key | Simple lookup | Normalize and avoid leaking sensitive identity |
| Persisted index | Better eviction/reconciliation | Becomes another durable schema |

## Concurrency across the native and web boundary

A common hybrid failure starts with a simple race. A player cell becomes visible, starts preparing remote content, then loses primary status during a fast scroll. If the activation task is not owned by the cell/controller lifecycle, its result can arrive late and attach a WebView to the wrong visual state. If a catalog refresh changes the item, a previous request may still supply stale metadata. If the app backgrounds, work may be cancelled or the process may disappear entirely.

Treat these as normal states, not exceptional accidents. Give each activation a reference and a lifecycle. Cancel tasks when their owner goes away. Check identity before applying completion. Re-enter the main actor only to update UI-owned state. Let the native shell decide a safe fallback when work cannot complete. Chapters 8 and 9 will apply this model to GamePlayer's native paging and WebView economics.

The performance trade-off is subtle. Starting tasks early can improve perceived responsiveness, but it also increases wasted work, memory, network activity, and the number of completions that must be discarded safely. Starting only after a user settles on a stage conserves resources but may delay activation. There is no universal answer; measure on target hardware and make cancellation correctness the prerequisite for any optimization such as prewarming.

## Test the lifecycle, not just the response

The Recipe App's mocked responses make a crucial kind of test cheap: the application can see valid, empty, and malformed inputs without relying on a live service. Extend that idea to lifecycle. A production test plan should be able to create a slow response, start a replacement request, cancel the first owner, and prove that the older completion never changes visible state. It should test an empty result separately from a decode failure. It should confirm that a cache miss and a cache write failure do not turn into the same user-facing condition.

This is where dependency injection becomes practical rather than ceremonial. Inject a session, clock, cache, or service protocol only where a test needs control. The public Recipe App uses a session and mock mode in its service initializer. A larger application may inject a catalog client or an image loader protocol. The test does not need to know how the real endpoint works; it needs a controllable answer at the boundary.

```swift
// Illustrative test intent, not a copy of a private test suite.
func testReplacementRefreshIgnoresOlderCompletion() async {
    let client = ControlledCatalogClient()
    let model = await CatalogModel(service: client)

    await model.refresh()          // request A
    await model.refresh()          // request B replaces A
    await client.completeA(with: .oldItems)
    await client.completeB(with: .newItems)

    await expect(model.state).toEqual(.loaded(.newItems))
}
```

The shape matters more than the helper names. The test proves that the latest user intent wins. It should also prove the opposite when appropriate: a task that remains relevant should deliver a result even if the view temporarily rerenders. Do not equate every SwiftUI lifecycle event with cancellation. Tie task ownership to a documented feature or coordinator lifetime.

Observability closes the loop. Record a privacy-safe event when a request begins, completes, is cancelled, or maps to a user-visible failure category. Avoid logging full request bodies, user identifiers, or raw remote URLs unless there is a reviewed reason to do so. The goal is to distinguish “the service was slow” from “the user replaced the request” from “the response could not be accepted.” Those distinctions will matter when a hybrid session crosses native and web runtimes.

Async code becomes tractable when tests and telemetry share its vocabulary: owner, operation identity, cancellation, result category, and visible outcome. Without those terms, a task that “sometimes disappears” stays a mystery. With them, it becomes a state transition that can be reproduced and improved.

This vocabulary also makes reviews shorter and more precise. Instead of asking whether a new `Task` “looks safe,” ask what owns it, when it is cancelled, whether a late completion can still apply, and how the user recovers. Those questions work equally well for a one-screen recipe demo, a feed refresh, or a remote game activation. They are the connective tissue between Swift concurrency syntax and reliable product behavior.

They keep concurrency review grounded in customer-visible consequences instead of framework folklore or accidental timing assumptions.

## Generalized MemeArcade view

The approved generalized MemeArcade view is that catalog/feed and product service work use owned, cancellable asynchronous operations whose results are validated before they become visible state. This book does not publish private service names, endpoints, request shapes, payloads, cache keys, data models, task graphs, logging records, or performance measurements. Any specific implementation excerpt or operational claim requires explicit human approval.

The public Recipe App is not a miniature copy of MemeArcade. It is a smaller executable example of the same discipline: isolate mutable work, represent loading and failure honestly, test response variants, and avoid letting a late result override current intent.

## Reader activity: follow one request and cancel it

Open [receipe-app](https://github.com/hassanvfx/receipe-app) directly. Trace `RecipesViewModel` to `APIService.fetchRecipes()`, then into the generic request/decode path. Identify where mocked success, empty, and malformed input enter the service. Next, inspect `ImageCache` and write down what happens when a disk write has not completed before the next lookup.

Finally, add a cancellation point to the trace: imagine the recipe list is dismissed while its request is outstanding. Which owner should cancel or ignore the result, and which state should the user see if the feature is shown again? The expected observation is that async/await makes the path readable, but ownership and validation make it production-safe.
