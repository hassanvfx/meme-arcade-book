---
title: From MemeArcade to Reusable Architecture
slug: reusable-architecture
---

# From MemeArcade to Reusable Architecture

The goal of a case study is not to copy its product. It is to identify the contracts that remain useful when the catalog, brand, business model, remote provider, and user journey all change. In a hybrid iOS application, those contracts are rarely whole screens. They are responsibility boundaries: a product state transition, a durable-state adapter, a cancellable client, a WebView policy, a pager lifecycle, a notification plan, or a privacy-aware event grammar.

MemeArcade, the App, is private and product-specific. Its value as a case study is precisely that it forces a distinction between what should be extracted and what must remain contextual. A reusable component is not “the MemeArcade player with different colors.” It is a smaller capability with explicit inputs, outputs, lifetimes, trust rules, tests, and forbidden dependencies.

The public repositories demonstrate different pieces of that extraction discipline: `ios-framework` makes a package and tandem app visible; `ios-storage` isolates durable device state; `receipe-app` isolates concurrent transport/cache work; GamePlayer isolates a native pager and constrained web session; Pushscheduler isolates local notification planning/routing; and `rezona-api` demonstrates evidence boundaries around client observations. This final chapter turns those pieces into an extraction method.

## Begin with the contract that already exists

Teams often begin extraction by moving files into a folder called `Core` or by creating a package because a target feels large. That changes source layout without necessarily changing coupling. Start instead with a contract that the rest of the app already needs:

- “Given a validated game reference and navigation policy, host one bounded remote stage.”
- “Given a device-owned plan, create, refresh, and clear only the local notification requests this feature owns.”
- “Given a `Codable` state representation, restore it safely and observe future durable changes.”
- “Given a catalog query, return validated domain values or a known failure category.”

Each sentence identifies an input, a responsibility, and a result. It should also identify what the capability does **not** own. A player host does not own the global route; a scheduler does not decide marketing policy; storage does not decide which screen appears; a client does not expose raw transport detail to a SwiftUI view.

```
Reusable capability
  inputs: validated domain values + explicit policy/dependencies
  owns:   one coherent behavior and its local lifecycle
  outputs: domain result / typed event / failure category
  forbids: global navigation, private product data, hidden singletons, unrelated UI
```

This contract-first test prevents a common failure: extracting a module that still imports half of the application and therefore cannot be used, tested, or released independently.

## A reusable architecture map

The following map groups the book's capabilities by their natural responsibility. It is a proposal for reasoning, not a claim about MemeArcade's private package graph.

| Capability | Stable contract | Possible public teaching source | Product-specific concerns that stay outside |
| --- | --- | --- |
| Product shell | intents → route/session state | SwiftUI/Combine article | Brand navigation, account policy, experiments |
| Durable state | restore/save validated representation | ios-storage | Private schema, retention, keys, migrations |
| Catalog client | query → domain page/failure | receipe-app, rezona-api method | Endpoints, ranking, credentials, backend logic |
| Player host | reference + policy → typed lifecycle/action events | GamePlayer | Catalog, provider agreements, game content |
| Web policy | URL/response → allow or reject | GamePlayer | Private hosts/origins and exceptions |
| Local scheduler | validated plan → owned requests/route request | Pushscheduler | Copy, campaign rules, user targeting |
| Observability adapter | state transition → redacted event | GamePlayer + Recipe App | Private vendors, dashboards, user data |

Notice that none of the reusable contracts says “knows MemeArcade.” The product composes them. That is the architectural center of gravity: reusable parts move downward into policy-constrained capabilities; product decisions remain at the composition root.

## Extract in dependency order

Not every boundary should become a package immediately. Start with pure domain models and policy protocols because they have few dependencies. Then extract infrastructure adapters whose inputs can be explicit. Extract UI hosts only after their lifecycle and callback contracts are stable. Keep product composition in the app target until a second consumer or release boundary makes independent distribution valuable.

```text
Domain values / protocols
        ↓
Pure validation and policy
        ↓
Infrastructure adapters (storage, client, scheduler)
        ↓
Feature host (pager, WebView container)
        ↓
Application composition (route, account, product choices)
```

The arrows point downward: higher layers may depend on lower-layer contracts; lower layers should not import the application to discover what to do. `ios-framework`'s tandem-app pattern gives a practical test. If a demo app can import a package and exercise its public entry point without copying global product state, the boundary is becoming real. If the package needs a global app singleton, an app route enum, or private service configuration just to compile, continue refining its inputs.

For example, a `PlayerHost` can accept a `GameReference`, a navigation-policy protocol, and an event sink. It should not import `AccountManager`, `HomeTab`, or a proprietary catalog client. The app supplies those concerns when it composes the host. That makes the host testable with fixtures and lets a second product use it under a different routing policy.

## Types are better seams than callbacks without contracts

A reusable component needs a language for crossing its boundary. Prefer small domain types and protocols over unstructured dictionaries, unbounded notification-center messages, or strings that mean different things in different features.

```swift
// Teaching sketch; not a private API.
public struct StageReference: Sendable, Equatable {
    public let opaqueID: String
}

public enum StageEvent: Sendable, Equatable {
    case loadStarted
    case loadFailed(StageFailure)
    case requestedAction(StageAction)
    case leftPrimary
}

public protocol StageEventSink: AnyObject {
    func receive(_ event: StageEvent, for reference: StageReference)
}
```

The example does not need to expose a URL, raw browser message, account identity, or full catalog record. It gives the host enough information to perform its job while reserving product interpretation for the app. That is a privacy boundary as well as a modularity boundary.

Use the same discipline for notification routing. A scheduler can emit a validated `RouteRequest`, not open a URL. A store can return a `RestorationResult`, not mutate the app's navigation state. A client can return a `CatalogPage`, not a transport JSON object. Each typed result gives tests a stable surface and keeps product data from leaking into components that do not need it.

## Decide what must remain product-specific

Extraction is successful when it leaves important product decisions where they belong. The following areas should resist generic SDK treatment until there is a true shared contract and explicit approval:

- Brand voice, notification copy, artwork, onboarding, and accessibility language.
- Catalog ranking, moderation, content/provider agreements, and entitlement rules.
- Account state, user-generated content, private endpoints, server payloads, credentials, and analytics identifiers.
- Host allowlists, security exceptions, bridge capability decisions, and incident data.
- Growth experiments, pricing, marketing logic, and any claim about market/business performance.

These are not “messy details” to hide inside a component. They are the product. A generic library that quietly includes them becomes difficult to audit and dangerous to reuse. Keep them in an application policy layer with clear owners and appropriate access controls.

| Extract when | Keep product-specific when |
| --- | --- |
| Input/output and lifecycle can be stated without brand context | Behavior depends on accounts, contracts, ranking, or editorial choice |
| A second consumer could use the capability safely | Reuse would expose private data or policy |
| Tests can use public fixtures | Tests require production endpoints/content |
| Failure/recovery behavior is generic | Failure needs product-specific communication or compliance |
| Versioning has a clear compatibility promise | The contract is still changing with the product |

## Versioning is a promise to consumers

When a component has more than one consumer, a version is not a tag decoration. It is a statement about compatibility. `ios-framework`'s README points from local tandem development toward tagged package distribution, and that transition should happen only when the public surface is ready to support it.

Before publishing a reusable module, establish:

1. A supported platform/toolchain baseline.
2. A public API that does not expose private product models.
3. Fixtures and tests that prove the contract without live services.
4. A changelog and deprecation approach.
5. Clear ownership for security updates, policy changes, and release decisions.

Do not promise semantic-version stability for a feature still being redesigned every week. An internal package with a local tandem app may be the correct intermediate step. It gives the team a real boundary and tests without forcing a public distribution obligation too early.

## Reuse the quality gates too

The most valuable extraction is often a quality gate rather than a runtime component. Every module can carry the same habits:

- Explicit source/evidence boundaries and no private material in public fixtures.
- Deterministic formatting, linting, unit tests, and focused UI/journey tests.
- Contract tests for validation, cancellation, route handling, and recovery.
- Privacy review for logs, metrics, persistent state, and bridge payloads.
- A reader/demo app that proves integration without becoming another product.

GamePlayer and Pushscheduler make this concrete by pairing focused source modules with quality scripts and test targets. `rezona-api` does it differently: manifests, checksums, collection journals, and a declared limit on what the aggregate proves. The common idea is evidence. A reusable component should make its promises testable and its unknowns visible.

## Run the reuse test before publishing a package

Before a boundary earns a package name, run a short design review with a deliberately boring question: could another application use this without learning anything it should not know? The point is not to predict every future consumer. It is to find accidental dependence on the current product while the change is still inexpensive.

Start with a fixture-only integration. A small demo target should be able to construct the public types, supply a policy implementation, trigger the meaningful lifecycle transitions, and inspect typed results without an account, a production service, or a live remote page. This is the practical lesson of a tandem app: the library gets a consumer that is close enough to reveal API friction but separated enough to reveal hidden coupling. An integration that requires special environment variables, copied app models, an authenticated session, or a global route coordinator has not crossed a healthy boundary.

Then inspect the failure paths. A client package needs a cancellation result and a recoverable failure category; it should not turn an error into a brand-specific alert. A player host needs a rejection or load-failure event; it should not decide whether the app retries, offers support, or changes tabs. A notification package needs to report an invalid plan or capacity conflict; it should not choose the campaign copy. The application is the right place to translate a generic outcome into a product decision.

Finally, run an ownership review. For every stored value, event field, URL-like input, log field, and callback, ask who is allowed to create it, who can observe it, how long it survives, and what happens when it is invalid. If the answer names a user account, a provider agreement, private content, or a business experiment, the information normally belongs above the reusable boundary. This review makes reuse safer because it treats privacy and security as interface design rather than cleanup work after a package has spread.

The result does not need to be a public open-source library. A private internal package can still be successful when its contract is explicit, its fixtures are synthetic, its dependencies are narrow, and its owner can update it deliberately. The distinction is important: reusable means a capability can move without dragging product context along; publishable means a separate legal, security, support, and maintenance decision has also been made.

## An extraction proposal for the next product

If a new iOS product needs a hybrid feed, do not start by importing a monolithic “arcade framework.” Start by choosing the smallest capabilities it actually needs:

1. Define domain references and failure categories without URLs or account data.
2. Build a native product shell that owns routes and feature intent.
3. Add a validated catalog/client adapter with cancellation and fixtures.
4. Add a constrained player host with explicit WebView policy and typed events.
5. Add device persistence only for safe, durable values.
6. Add a local scheduler only for device-owned triggers.
7. Add redacted event instrumentation at each ownership handoff.
8. Extract a package only after a capability has a stable, tested contract and a real consumer.

This sequence produces an architecture that can grow in the same direction as the product: more content, more routes, more providers, or more devices without multiplying global state and undocumented cross-runtime messages.

## Generalized MemeArcade view

The approved MemeArcade conclusion is that reusable architecture is the extraction of stable responsibility contracts—state, persistence, client, player host, WebView policy, scheduling, and observability—while product-specific data, content, routes, business rules, and private implementation remain in the application boundary. The private product is not a reusable SDK and is not published through this book.

No private package graph, source, module name, API, endpoint, payload, catalog, account data, notification copy, metric, security policy, or business logic is approved for publication. Any private excerpt or exact implementation claim requires explicit human approval.

## Reader activity: propose one honest extraction

Open [ios-framework](https://github.com/hassanvfx/ios-framework), [GamePlayer](https://github.com/hassanvfx/GamePlayer), and [Pushscheduler](https://github.com/hassanvfx/Pushscheduler) directly. Choose one capability from this chapter and write a one-page extraction proposal: public inputs, outputs, lifecycle, forbidden dependencies, fixtures, tests, and the product policy that stays outside.

The expected observation is that a reusable component becomes smaller as its contract becomes clearer. If the proposal needs private account models, endpoints, content, or global navigation to work, it is not ready to leave the product boundary.
