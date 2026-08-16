---
title: Local Notifications as Edge Infrastructure
slug: pushscheduler-local-notifications
---

# Pushscheduler: Local Notifications as Edge Infrastructure

Notifications are often discussed as a growth channel, which makes it easy to skip the more important architectural question: **where does the event originate, and who is allowed to decide it is worth interrupting someone?** If the device already knows the content and timing of a reminder, a local notification can be the simplest, most private implementation. If a server-side event, another person, or cross-device state must trigger the interruption, local scheduling is the wrong tool and remote push is required.

The public [Pushscheduler](https://github.com/hassanvfx/Pushscheduler) repository is an experimental SwiftUI lab for this device-owned half of the problem. It requests and inspects notification permission, persists notification plans in `UserDefaults`, replaces/refreshes/clears a namespaced family of requests, limits its scheduled plan to 32 pending requests, shows foreground presentation, validates local deep-link payloads, and surfaces a selected route rather than opening it automatically. The implementation splits responsibility across an alert orchestrator, schedule vault, notification navigator, alert conductor, and studio UI.

That decomposition matters for MemeArcade, the App. A product may want to re-engage a reader after a device-known moment: a locally scheduled follow-up, a reminder they asked for, or a safe “ready” state produced while the app is still responsible for the timing. The product must not pretend that a local notification is an APNs message, a guarantee of delivery, or evidence that a remote game/server reached a condition. This chapter explains the boundary through public code and generalized architecture only. No private notification copy, payload, route, plan, source, device data, or analytics is published.

## Local versus remote is an origin decision

Start with the trigger, not the notification UI.

| Trigger origin | Appropriate mechanism | Why |
| --- | --- | --- |
| Device knows a chosen reminder time | Local notification | No server decision is needed |
| App creates a local follow-up plan | Local notification | Plan can persist and refresh on the device |
| Server observes a completed job | Remote push or in-app refresh | Device cannot reliably invent this external event |
| Another user sends a message | Remote push | Trigger exists outside one device |
| Account state changes elsewhere | Remote push / sync | Requires cross-device authority |
| User is active in foreground | In-app UI, optionally notification presentation | Do not interrupt blindly |

Local notifications continue after the app process exits once the system has accepted a request, but “continues” is not the same as “guarantees a business outcome.” A user can deny or later disable permission, change device settings, remove the app, clear a notification, or tap after the underlying product state has changed. The app must treat a tap as a fresh input requiring validation, not as a command to restore an old route.

```
User intent / device-owned plan
            │
            ▼
validate + persist plan ──► schedule local request ──► iOS delivers if permitted
            │                                                   │
            └── refresh / replace / clear                       ▼
                                            notification tap → validate route → native navigation
```

## Permission is a state machine

Asking for permission is not a one-time button action. It is a state machine with product consequences. The public `MAAlertOrchestrator` exposes both `requestPermission()` and `currentPermissionStatus()`, while the conductor/UI can represent that status and offer a Settings handoff. That is a better model than assuming a permission prompt means the user has opted in forever.

For every entry point, decide what happens when permission is undetermined, denied, authorized, provisional, or otherwise limited by the system. Do not block the primary game/feed experience behind a reminder permission. Explain the value at the moment it is relevant; if the user declines, preserve the core experience and offer a future Settings path only when it is useful.

| Permission state | Product behavior |
| --- | --- |
| Not determined | Explain a specific benefit, then request only after user intent |
| Authorized | Schedule only validated, user-appropriate plans |
| Denied | Do not retry prompts; offer a non-blocking Settings route when relevant |
| Changed in Settings | Re-read status before scheduling/refreshing |
| Foreground | Decide whether to show an in-app/foreground presentation deliberately |

The important ownership rule is that the notification layer reports permission state; the product decides whether and how to request it. A scheduler should not manufacture persuasive copy, change app navigation, or quietly turn every user action into a prompt.

## Persist the plan, not a pile of requests

Pushscheduler stores a notification plan, not merely an unmanaged list of pending requests. Its orchestrator constructs a validated plan, saves it through `MAScheduleVault`, clears only its own scheduled request family, then refreshes pending items. During refresh it reads the current pending requests, filters namespaced identifiers, calculates remaining capacity under a 32-request cap, and schedules only upcoming plan items that are not already pending.

This is a useful device-infrastructure pattern. The plan is the source of intent; system notification requests are a projection that may need reconstruction after app relaunch, replacement, or capacity change. Without a plan, an app can only inspect the current pending queue and guess whether it still represents the user's choice.

```text
Validated plan (durable intent)
       │
       ├── schedule projection: pending UNNotificationRequests
       ├── refresh projection after launch / change
       └── clear only owned request identifiers
```

The same distinction from Chapter 4 applies. A persisted plan is historical input. Validate its schema, identifiers, time values, and copy before using it; recover safely from corrupt data; make a reset explicit. Do not store credentials, unrestricted remote URLs, private game payloads, or product state that must be refreshed from a server. The public vault's recovery behavior is a useful model: a corrupted plan should not prevent the application from starting.

## Namespaced identifiers and bounded schedules

Notification centers are shared at the app level. Removing all pending notifications because one feature changed is a classic ownership bug. Pushscheduler avoids it by using MA-namespaced identifier families and filtering scheduled versus “game ready” requests. The pattern is portable: each feature owns identifiers it can recognize, replace, and clear without disturbing another device feature.

The 32-request cap in the public lab is a conservative application policy, not a universal platform limit to copy blindly. It forces the scheduler to make capacity visible: create a small window of upcoming reminders, refresh it when appropriate, and reject/handle a plan that cannot be represented safely. A product should set its own budget after considering platform limits, UX, and the risk of filling a queue with stale interruptions.

| Scheduling decision | Why it matters |
| --- | --- |
| Identifier family | Enables precise replacement and cleanup |
| Bounded copy/IDs | Avoids malformed or oversized payloads |
| Capacity policy | Stops unbounded queues and makes refresh necessary |
| Time validation | Prevents impossible past/invalid schedules |
| Replace rather than append | Keeps latest user intent authoritative |
| Clear delivered and pending owned requests | Prevents stale re-entry paths |

The system should be able to answer: which plan created this request, whether that plan is still current, and what action clears it.

## A notification tap is untrusted input

It is tempting to treat a local notification as trusted because the app created it. But it may have been scheduled by an older app version, persist after a state reset, or contain a malformed/corrupt payload. A tapped notification is an entry point into the application and deserves the same routing discipline as a deep link.

Pushscheduler's `MANotificationNavigator` accepts only a local `pushscheduler://` scheme, validates payloads, bounds input length, maps a recognized destination, and deliberately surfaces rather than auto-opens the selected route. That final choice is important. The navigator tells the product “a route was requested”; the product checks current state and chooses whether it is valid to navigate now.

```swift
// Teaching sketch; not private MemeArcade code.
func handleNotificationTap(_ payload: NotificationPayload) {
    guard let route = navigator.validatedRoute(from: payload) else {
        return showSafeDefault()
    }
    coordinator.consider(route, under: currentProductState)
}
```

The `consider` step can reject an expired reference, require the user to select an account, refresh a catalog, or route to a stable native surface. Never load a web URL supplied by a notification payload without the same origin and catalog validation described in Chapters 6 and 7.

## Foreground presentation and respectful interruption

When the app is foregrounded, a notification may be redundant or disruptive. The public lab includes foreground toasts and notification callbacks, making the presentation a deliberate UI choice instead of an accidental duplicate interruption. A production product should decide whether the foreground experience needs a toast, a badge, a quiet state update, or no presentation at all.

Respect is an implementation requirement. Schedule only events that have a clear user benefit, provide a clear way to change/disable the plan, avoid repeated reminders that no longer match the product state, and never use local scheduling to imitate a remote social or server event. If a game-ready message is genuinely local, say what local condition made it ready. If readiness belongs to a service, wait for the service-owned trigger.

Measure the scheduler's health with privacy-safe aggregates: permission status category, plan creation/replacement/clear result, number of owned pending requests, validation rejection category, and route outcome. Do not report notification body text, full deep links, game content, or account identifiers as routine telemetry. A high tap rate does not make an interruption appropriate; product judgment remains necessary.

## Local scheduling is not APNs

APNs remote notifications involve server credentials, device-token lifecycle, provider delivery, payload construction, and a remote trigger. Pushscheduler intentionally includes none of those concerns. This is a feature of the teaching example: it lets a reader understand the local edge of notification architecture without claiming that a serverless plan can solve cross-device or externally-triggered product needs.

When a product grows into remote push, retain the same internal boundaries: permission/status, validated payload, bounded route, foreground presentation, metrics, and safe navigation. The transport changes; the device-side trust model does not disappear. A remote payload should be treated as at least as untrusted as a local persisted plan.

## Test schedules as time-dependent state

Notification code is easy to demo and easy to leave untested because time, permission, and system delivery are involved. Pushscheduler makes several seams injectable—notification center, plan store, timing policy, and calendar—which allows its tests to examine behavior without waiting for a real day to pass. Carry that approach into any product scheduler.

Test the planner separately from the system request projection. Given a fixed clock and a plan, verify that invalid identifiers, malformed copy, impossible clock values, duplicate request identifiers, and capacity overflow are rejected or recovered as intended. Given an existing plan plus a simulated set of pending request identifiers, verify that refresh schedules only future owned items and does not remove unrelated notifications. Given corrupted stored data, verify that the app returns a safe empty/default state rather than failing launch.

Then test re-entry. A route produced from a valid fixture should reach the coordinator as a request, not cause navigation before current account, catalog, and permission policy have a chance to decide. A malformed route should result in a safe default. A cancelled plan should remove both pending and delivered notifications from its owned family when that is the stated product behavior.

| Test level | Example assertion |
| --- | --- |
| Policy unit test | Identifier/copy/deep-link validator rejects malformed input |
| Plan test | Replacement retains only current plan intent |
| Projection test | Refresh respects capacity and avoids duplicate owned requests |
| Vault test | Corrupt serialized plan recovers safely |
| Route test | Tap produces a validated request, not automatic navigation |
| UI journey | Permission denial still leaves the core app usable |

The system notification center remains the delivery authority, so tests should avoid pretending they prove every device-level delivery behavior. They do prove the application logic surrounding delivery: what it asks for, what it schedules, what it owns, and how it recovers. That is the part of notification architecture the iOS application can actually make dependable.

Review those tests whenever notification copy, route formats, account boundaries, or scheduling rules change. A notification is an application entry point that may fire long after the original UI disappeared. The longer its lifetime, the more valuable it is to keep its plan, payload, and recovery behavior small, explicit, and independently testable.

That discipline protects both the reader's attention and the product's ability to explain why an interruption appeared, what it means now, and how it can be dismissed.

## Generalized MemeArcade view

The approved MemeArcade lesson is that device-owned re-engagement may be modeled as a validated local plan, a bounded projection into system notification requests, and a native-owned route decision on re-entry. Local notifications are used only when timing/content are owned by the device; server- or cross-device-originated events require a different remote-push design.

No private MemeArcade notification text, plan, identifier, schedule, deep link, route, game reference, account state, source, payload, analytics, remote-push configuration, token, or server behavior is approved for publication. Any product-specific notification evidence requires explicit human approval.

## Reader activity: trace a local plan

Open [Pushscheduler](https://github.com/hassanvfx/Pushscheduler) directly. Trace one plan from permission status through validation, vault persistence, namespaced pending request, foreground/tap handling, and route selection. Identify which state is durable intent and which is merely the current system projection.

Then design one reminder for a hypothetical game app. State why its trigger is device-owned, what clears it, how a denied permission changes the experience, and how a tapped route is validated before navigation. The expected observation is that local notifications are small, powerful pieces of edge infrastructure only when their origin, ownership, and re-entry path are explicit.
