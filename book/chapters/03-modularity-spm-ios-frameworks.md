---
title: Modularity as Architecture
slug: modularity-spm-ios-frameworks
---

# Modularity as Architecture: Swift Package Manager and iOS Frameworks

Modularity is often introduced as tidiness: put related files together, make a framework, keep the project navigator pleasant. That is useful, but it misses the production reason to create a module. A module is a promise about **who may depend on whom**. It makes one capability available through a contract while keeping its implementation free to change behind that contract.

For a hybrid iOS application, that promise is not abstract. A player feature should not need to know how a notification schedule is persisted. A storage implementation should not choose the selected tab. A WebKit host should not become the only place where product navigation can happen. When those relationships are only conventions in one Xcode target, convenience slowly turns into coupling. Swift Package Manager gives the team a way to make the dependency direction visible and testable.

The public [ios-framework repository](https://github.com/hassanvfx/ios-framework) is intentionally small enough to inspect in one sitting. It contains a top-level `Package.swift`, a `FrameworkLib` target, a test target, and a separate `DemoApp` that imports the library. Its value is not the size of its source. It is the shape of the experiment: build a package as a real product, then prove its integration from an app that uses it.

## A package is a boundary, not a folder

Swift Package Manager reads `Package.swift` as a declaration of an external contract. The public example declares a library product named `FrameworkLib`, a source target with the same name, and a separate test target. It also declares the platform floor: iOS 15, macOS 12, and watchOS 8. Those lines answer real questions before anyone opens a view controller:

- What capability is being distributed?
- Which platforms are part of its compatibility promise?
- Which targets may compile against its public API?
- Where do tests live relative to the capability they protect?

The source target in the repository is deliberately minimal: it exports a public `Framework` type. The demo app imports `FrameworkLib` while retaining a tiny SwiftUI application root. This is a useful baseline because it separates two kinds of code that are often mixed together: the reusable capability and the app that demonstrates, configures, and composes that capability.

```
              DemoApp
                 │ imports
                 ▼
          FrameworkLib product
                 │ exposes
                 ▼
          FrameworkLib target
                 │ verified by
                 ▼
        FrameworkLibTests target
```

The arrow never points back upward. A reusable target may not import the demo application to discover its configuration or navigation state. Once that happens, the package is no longer a package; it is a hidden feature folder with extra build steps.

For a junior developer, this is a simple question to ask before extracting code: can another app use this feature by importing its public API without copying a screen, an app delegate, or a global singleton? For a senior engineer, the same question exposes product risk. If a capability cannot be exercised outside the only application that currently uses it, its release, testing, versioning, and migration costs are all entangled with the entire product.

## The tandem-app pattern

The repository calls its separate app a “tandem app.” Apple documents the related local-package workflow: an Xcode application can depend on a package that is edited locally, so changes in the package are reflected during app development without first publishing a release. The public README extends that idea with a configuration script that can rename the template and optionally prepare a repository for it. [Apple: developing a package in tandem with an app](https://developer.apple.com/documentation/xcode/developing-a-swift-package-in-tandem-with-an-app) [Apple: editing a local package dependency](https://developer.apple.com/documentation/xcode/editing-a-package-dependency-as-a-local-package)

The tandem app is not a showcase for every possible use case. Its discipline is more useful: demonstrate only enough to prove that the package can be integrated. A demo that quietly accumulates product-specific networking, analytics, account flow, and styling is no longer a test of the package boundary. It becomes a second application that needs its own architecture.

In practice, a tandem app should answer four questions:

1. Can an app resolve and import the package using its intended integration path?
2. Can it construct the public entry point with ordinary configuration?
3. Can a visible, testable interaction prove the package is doing its job?
4. Can the package change internally without requiring the app to reach into private implementation detail?

Those questions are as relevant to an internal module as they are to an open-source SDK. The source may remain private while its boundary becomes clear.

## Extract responsibilities, not screens

The wrong reason to make a package is “this folder has become large.” The better reason is “this responsibility has a coherent API, lifecycle, and test surface.” A feature can be large and still need to stay close to its host application if its behavior is inseparable from product navigation. A small service can deserve a package if it owns a stable capability such as encrypted local storage, notification scheduling, or a reusable WebView policy.

Use a responsibility map before you create targets:

| Candidate capability | Useful public API | Inputs it may accept | Dependencies it must not own |
| --- | --- | --- | --- |
| Device storage | read/write validated values | explicit keys, values, migration policy | SwiftUI navigation and feed selection |
| Notification scheduling | schedule, cancel, refresh plans | permission status, validated destination | backend campaigns and product tab state |
| Hybrid player host | present an authorized game reference | approved URL/origin policy, lifecycle callbacks | app-wide account state and catalog fetching |
| Catalog client | fetch domain records | transport configuration, cancellation | view hierarchy and WebView lifecycle |

This table does not dictate that every row must be its own package. It tests the idea. If the proposed capability requires five unrelated app models, an application coordinator, and a WebView instance merely to run a unit test, its boundary is not mature yet. If it accepts narrow domain inputs, has explicit outputs, and can be tested with substitutes for its environmental dependencies, extraction is likely to reduce rather than relocate complexity.

## Dependency direction is an architectural test

Imagine a module named `PlayerKit` that hosts a remote game. It may depend on a small `PlayerDomain` model package and platform frameworks such as WebKit. The app may depend on `PlayerKit` and supply a route coordinator. But `PlayerKit` should not import `AppShell` simply to tell the app what to do next. Instead, it can expose a callback, delegate, async stream, or value representing a product-neutral event. The application translates that event into its own route or analytics decision.

```swift
// Illustrative public boundary; not private MemeArcade code.
public protocol PlayerEventHandling: AnyObject {
    func playerDidRequestExit()
    func playerDidFail(_ failure: PlayerFailure)
}

public final class PlayerHost {
    public init(reference: GameReference,
                policy: NavigationPolicy,
                events: PlayerEventHandling) { /* ... */ }
}
```

This pattern protects both sides. The player package learns only that it has an event handler; the application decides whether “exit” means return to a feed, dismiss a modal, save a preference, or do nothing. Likewise, the app cannot reach into a web view and mutate its internal state merely because it happens to know the implementation type.

The same thinking applies to data flow. If a package exports a view model that includes transport-layer errors, database handles, and application route enums, it has leaked three boundaries through one API. A more durable contract exports domain values and failure categories that the caller can render or route according to its own product policy.

## Tests are the price of a public contract

The public `ios-framework` package includes a `FrameworkLibTests` target even though the initial example has only a placeholder test. That shape matters. The moment a type becomes public, it becomes a compatibility promise. Tests should describe that promise in behavior, not in the package's private arrangement of files.

For a storage package, test that an invalid record does not become a valid domain object. For a notification package, test that a denied permission produces a known outcome rather than silently scheduling nothing. For a player package, test the navigation policy with approved and rejected origins. For a service package, test cancellation and error mapping. These tests create a shared language for a capability and make refactoring less risky.

The tandem app complements unit tests. Unit tests prove a small contract; the app proves that Xcode can resolve the package, the host lifecycle is sound, and the public entry point is usable in a real UI. UI tests in the demo app should remain focused on that integration rather than recreate the package's entire test suite.

## Versioning and the cost of extraction

Once code leaves an app target, it starts to acquire release economics. A package needs a versioning strategy, changelog discipline, compatibility policy, and an answer for local development versus tagged distribution. The `ios-framework` README points to a separate semantic-version tagging utility, which is a reminder that publishing is not a `Package.swift` feature. It is an agreement with users of the API.

Do not prematurely extract a moving implementation only because it could someday be reused. An internal package is often enough while the contract is forming. Tag and distribute it when a second consumer, a release boundary, or an independent ownership model makes compatibility meaningful. The important thing is to keep the app from depending on undeclared implementation detail; the repository location can follow later.

| Choice | Benefit | Cost | Appropriate when |
| --- | --- | --- | --- |
| One app target | Fast exploration | Hidden coupling grows | A behavior is still being discovered |
| Internal package | Explicit seam, local development | More target and test maintenance | A capability has a stable owner |
| Published package | Reuse across repositories | Compatibility and release burden | Multiple consumers need a supported API |
| Shared source folder | Low ceremony | No meaningful contract | Rarely; only for temporary migration |

## A safe extraction sequence

The cleanest package boundaries are rarely designed perfectly on the first day. They are discovered through a sequence that reduces risk rather than multiplying it. Start by naming the responsibility inside the existing app target and moving only its pure models, protocols, and tests behind a local interface. This step reveals what the code was accidentally borrowing from the application: global configuration, presentation state, date providers, telemetry clients, or singleton storage.

Next, replace those hidden borrowings with explicit dependencies. A package should accept a policy or a protocol where it needs one, not import the app layer where the policy happens to be defined. Keep the app as the composition root: it selects concrete implementations and supplies configuration. The package remains responsible for the capability's behavior once those choices arrive.

Then create the package target and move the contract together with its tests. Build the host application after every small move. A failed build is useful feedback: it identifies a dependency that has not been honestly modeled yet. Resist the temptation to restore the old dependency through a back door merely to get a green build.

Finally, use a tandem app or an existing feature integration to exercise the public entry point. Ask whether an engineer unfamiliar with the package can tell how to initialize it from the public API alone. If the answer is no, improve the contract before publishing a version. Documentation and examples belong at the boundary because they are part of what users of the boundary must understand.

```
App target implementation
        │ identify a cohesive responsibility
        ▼
Local protocol + behavior tests
        │ make environmental dependencies explicit
        ▼
Package target + public API
        │ prove real integration
        ▼
Tandem app / feature host
        │ only then consider a versioned release
        ▼
Supported capability
```

This sequence makes modularity a change-management tool. It does not require a rewrite, and it does not confuse “moved code” with “stable contract.” The package earns independence only after its inputs, outputs, and failure modes are explicit.

It also gives product teams a practical review question: if the app were replaced tomorrow, which part of this capability should still compile unchanged? The answer is the candidate module. Everything else is composition, policy, or a dependency that must be declared deliberately.

That clarity is the real product of a package boundary, long before reuse becomes a roadmap item.

## Generalized MemeArcade view

MemeArcade, the App, is not presented as a reusable SDK and its source remains private. The approved lesson is narrower: organize boundaries by responsibility, keep native product orchestration separate from specialized infrastructure, and make dependency direction explicit before extracting reusable components. The chapters on persistence, GamePlayer, and Pushscheduler show public examples of the kinds of capabilities that can eventually become stable seams.

We do not publish private package names, manifests, target graphs, source files, internal endpoints, or product-specific dependency rules. Any private implementation excerpt, exact module diagram, or claim about a particular private boundary requires explicit human approval. The reusable knowledge is the test: a capability should explain its inputs, outputs, lifetime, and forbidden dependencies without requiring the reader to see private source.

## Reader activity: inspect a tandem boundary

Open [ios-framework](https://github.com/hassanvfx/ios-framework) directly. Read `Package.swift`, then compare the `FrameworkLib` target with the `DemoApp` import. Draw the dependency direction and write one sentence for each side:

- The package promises ______ to an app.
- The app supplies ______ that the package must not own.

Then choose one conceptual MemeArcade capability—storage, player hosting, notification scheduling, or a catalog client—and make the same two-sentence contract. The expected observation is that a package boundary becomes useful only when it removes a dependency rather than hiding one. In the next chapter, persistence gives us a concrete device-level capability on which to apply this test.
