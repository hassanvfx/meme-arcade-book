---
title: Persistence as Device Infrastructure
slug: persistence-datastore
---

# Persistence as Device Infrastructure: DataStore in MemeArcade

Persistence is not a database feature added near the end of an application. It is the boundary between a fact that is true only while the process is alive and a fact the product is willing to carry into a future launch. In a hybrid iOS app, that boundary is especially consequential. A user can leave while a remote experience is loading, deny a permission after a preference was chosen, return from a notification, or reopen the app after the operating system has removed it from memory. The device needs a deliberate answer to one question: **what is safe and useful to remember?**

The public [ios-storage](https://github.com/hassanvfx/ios-storage) repository, called DataStore in its README, is a compact teaching model. It connects an `ObservableObject` to a `Codable` state representation through a `DatastoreItem` protocol. On connection, the library restores stored state and observes a Combine publisher for future changes. It includes an encrypted path implemented with CryptoKit's AES-GCM APIs, an actor-based `Datastore`, a throttled save pipeline, and a background-task wrapper around archive work. Those choices make it a useful object lesson: persistence has a model contract, a concurrency contract, an encryption decision, and a recovery policy.

MemeArcade, the App, has application-state data-store integration. This chapter explains the decisions that a product must make—what may survive, how defaults recover, and why stale state must be revalidated—without exposing private schemas, keys, source, or implementation details. Any private schema, storage implementation, or excerpt requires explicit human approval.

## Start with the survival question

Not all state deserves persistence. It helps to sort a value by the question it answers after launch:

| Kind of state | Example | Usually persist? | Reason |
| --- | --- | --- | --- |
| Durable preference | Sound setting, onboarding completion | Often | It is a user choice that remains meaningful |
| Safe restoration hint | Last selected tab or a stable content reference | Sometimes | It can reduce friction if revalidated |
| In-flight UI state | Half-open sheet, scroll velocity, loading spinner | Rarely | It belongs to the current process and scene |
| Remote authority | Session token, server permission, mutable catalog item | Not as app truth | It must be refreshed or validated through current policy |
| Sensitive material | Credentials, private keys, personal data | Only with explicit design | Encryption, access control, retention, and deletion requirements apply |

The common failure is treating persistence as a snapshot of whatever objects happen to be available. That produces a haunted relaunch: an old route points to content that no longer exists, a stale response is rendered as current, or a permission-dependent feature tries to resume without checking permission. A durable store should preserve the minimum information needed to reconstruct a safe user decision, not the maximum amount of live memory.

For a player experience, a stored identifier might be a hint that the user was engaged with a particular item. On relaunch, the app still needs to fetch or validate the current catalog, apply navigation policy, and decide whether the item is available. The identifier is not an authorization token, a remote URL to load blindly, or a guarantee that the session can resume exactly where it stopped.

```
Live state ──► choose safe Codable representation ──► durable store
   ▲                                                     │
   │                                                     ▼
Native UI ◄── validate / migrate / recover ◄── restored representation
```

The important arrow on the way back is validation. Persistence is not a time machine; it is input arriving from an earlier version of the app.

## The DataStore contract

The public `DatastoreItem` protocol makes the persistence decisions visible. A conforming model supplies a storage key, a `Codable` item type, a publisher, a way to read the current item, a default item, and a callback that applies a restored item. Encryption defaults to enabled through the protocol extension, although a conformer can choose otherwise.

That is a useful shape because it separates the observable application model from the serialized representation. A SwiftUI-facing model does not need to make every property public or serializable. It can produce a small state value whose compatibility can be reasoned about independently.

```swift
// A teaching sketch, not private MemeArcade code.
struct PersistedPlayerHint: Codable, Equatable {
    var version: Int
    var lastSelectedID: String?
    var didCompleteOnboarding: Bool
}

@MainActor
final class PlayerPreferences: ObservableObject {
    @Published private(set) var hint = PersistedPlayerHint(
        version: 1, lastSelectedID: nil, didCompleteOnboarding: false
    )

    func restore(_ saved: PersistedPlayerHint) {
        hint = migrateAndValidateLocally(saved)
    }
}
```

The version field is not decoration. A stored representation lives longer than individual releases, so a team needs a migration policy before a field changes meaning. A key such as `model:v1`, shown in the public README, is a simple way to separate incompatible storage generations. The library itself also prefixes item keys with a global version string. The lesson is broader than the exact mechanism: schema change needs an intentional path, not an accidental decode failure.

## Restore first, then observe

The repository's `connect` method calls a restore-and-observe path. It restores a model, then subscribes to its storage publisher; subsequent values are throttled before archival. This sequence prevents one common error: observing the model first and immediately saving its default state over an existing record before restoration has completed.

The exact timing policy belongs to the product. A preference model can often be restored before a window becomes interactive. A feature state may need to wait until a user has authenticated or until a catalog is available. The native shell should represent this visibly: restoring, ready, or recoverable failure. A blank view does not tell a person whether data is loading, absent, corrupt, or unavailable by policy.

Throttling is also a product decision. The public implementation uses Combine's `throttle` on a background queue before it starts an archive task. That is sensible for a value that changes quickly, such as a slider or an observable model with multiple updates in a row. But it creates a durability window: the last change may not have reached disk if the app is terminated before the throttle fires. A product that needs a strong “save now” guarantee needs an explicit flush or checkpoint operation, and it must decide what to do if that operation fails.

| Save strategy | Benefit | Cost | Good fit |
| --- | --- | --- | --- |
| Save every change | Simple mental model | I/O churn, power cost | Rare, tiny and infrequent values |
| Throttle changes | Bounded write rate | Last change may be pending | Preferences and noncritical UI state |
| Explicit checkpoint | Known durability moment | More API and failure handling | Drafts, user confirmations, handoff points |
| Background-only save | Less foreground work | OS may end work early | Supplement, never the only guarantee |

## Encryption is a design, not a checkbox

The public DataStore code creates or retrieves a symmetric key through Keychain APIs and uses CryptoKit AES-GCM for the encrypted storage path. AES-GCM provides authenticated encryption: a successful open operation verifies that ciphertext has not been altered under that key. That is a meaningful protection for an appropriate local record, but it does not settle every security question.

Before persisting sensitive data, decide whether the data should be on the device at all; which Keychain accessibility class and access controls are appropriate; whether backups are acceptable; how a user can delete data; and what the app should do after a key, record, or schema failure. Do not describe a store as “secure” merely because it calls encryption APIs. Security comes from the whole lifecycle: minimization, key handling, access policy, error behavior, observability, and a tested recovery path.

The public implementation is useful precisely because it makes a trade-off visible. In its restore path, any failure in the encrypted load/decrypt/decode sequence falls back to the model's default. That keeps the app from being trapped by a corrupt or missing record. It can also hide the distinction between a brand-new store, an incompatible migration, damaged data, and a lost key. A production product should decide which of those conditions are safe to treat as a reset and which require a user-visible recovery state or privacy-safe diagnostic event.

## Concurrency and the main-actor handoff

The `Datastore` type is declared as an actor, which is a clear attempt to serialize its internal mutable state. The public worker decodes and reads the store through that actor, then dispatches `setStorageItem` back to the main queue. This reflects a familiar SwiftUI constraint: a model observed by the UI should be mutated on the appropriate UI isolation context, while disk and crypto work should not block a render path.

The detail to preserve is not “always call `DispatchQueue.main.async`.” Modern Swift code should prefer actor isolation that makes intent visible, such as a `@MainActor` UI model. The deeper rule is: one component owns serialized storage operations, and a separate UI-owned component applies a validated result. Avoid letting arbitrary views write storage directly. A view should express a user intent; the feature model should decide whether that intent changes state; the persistence adapter should then observe or receive the permitted durable representation.

```
SwiftUI view ──intent──► feature model (@MainActor)
                           │ publishes safe state
                           ▼
                    persistence adapter / actor
                           │ archive or restore
                           ▼
                    validated Codable record
```

This arrangement also makes cancellation and testing clearer. A storage adapter can be tested with an in-memory substitute. A feature model can be tested by injecting a store that returns a known value or throws a known error. The UI test need only prove that the resulting state is presented honestly.

## Migration, deletion, and the right to start clean

Every persisted record eventually meets change. A field is renamed, a default becomes unsafe, an identifier is no longer meaningful, or a product changes what it is willing to keep. Planning for this does not require an elaborate database framework. It requires a versioned representation and a small set of explicit outcomes.

One approach is to decode the oldest compatible value, then migrate it in memory to the current domain state. Another is to use a new key or namespace for a breaking format and discard only the obsolete record. Both can be valid. What matters is that a future app build can tell the difference between “this record is from an old version,” “this record is damaged,” “the user requested deletion,” and “there was never a record.” If all four become a generic default without telemetry or product reasoning, a team loses the ability to diagnose real migration problems.

Deletion deserves equal attention. A sign-out, privacy request, account switch, or reset action should say exactly which device-bound records it removes and which records remain. Do not leave a local restoration hint attached to a person after an account transition merely because it was convenient to cache. Do not erase an independent accessibility preference just because an unrelated feature resets. Data minimization is not only about collecting less; it is about retaining and deleting with precise ownership.

For the hybrid player, a clean start is often the safest fallback. If a persisted selection cannot be reconciled with current catalog policy, return to an ordinary native surface and tell the user what happened if context requires it. Do not force a replay of a remote session, preserve a stale browser process, or construct an unvalidated URL from a stored value. The product can restore continuity without pretending continuity is certainty.

| Recovery condition | Safe default | Possible richer behavior |
| --- | --- | --- |
| No record | Construct a known default | Offer onboarding or a first-run explanation |
| Old compatible record | Migrate to current model | Record a privacy-safe migration outcome |
| Damaged or undecryptable record | Reset only that record | Present recovery help if user work could be lost |
| User reset or sign-out | Delete owned records | Preserve independent device preferences where appropriate |
| Stale remote reference | Return to a native safe route | Re-resolve through current catalog and policy |

The table is intentionally about outcomes rather than storage APIs. A durable store is successful when a person can recover from the past without the app mistaking historical data for present truth.

## Generalized MemeArcade view

The approved generalized MemeArcade observation is that the application integrates state persistence at the device boundary. The publication-safe lesson is to persist only product state that remains meaningful after relaunch, restore it through a validated model, and keep private schemas private. The application root can coordinate restoration while individual features retain ownership of their detail; a remote gameplay runtime cannot make itself durable merely by leaving a WebView alive.

This book does not publish MemeArcade's stored keys, record shapes, encryption strategy, migration history, account data, game identifiers, remote URLs, or private source. Any claim beyond this responsibility-level description requires explicit human approval. The public DataStore example is a teaching artifact, not proof that the production app uses the same data model or crypto configuration.

## Reader activity: classify a persisted value

Open [ios-storage](https://github.com/hassanvfx/ios-storage) directly. Find the public example's `State`, `storageKey`, `storagePublisher`, `getStorageItemDefault`, and `setStorageItem` methods. Then choose one value from a hypothetical game app—last selected tab, a user preference, a deep-link target, or a session token—and answer:

1. Is this value safe to keep after the process ends?
2. Is it a durable user choice, a restoration hint, or remote authority that must be refreshed?
3. What should happen if decoding, decrypting, or migration fails?

The expected observation is that persistence is a recovery contract. The data structure is only the beginning; the real architecture is the policy that decides what a future launch is allowed to believe.
