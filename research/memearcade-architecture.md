---
type: Architecture Research
title: MemeArcade architecture reconnaissance
status: draft
---

# Scope

Inspect the sibling production repository without copying code. Build an approved map of targets, modules, data flow, persistence, routing, player infrastructure, notification infrastructure, remote-content trust policy, and state that survives relaunch.

# Approved generalized map

The private application is a single Xcode target with explicit source folders rather than a published SPM package graph. Its visible architecture is still modular by responsibility:

- **Root and state:** a SwiftUI application root, tab container, application state, onboarding coordinator, and fullscreen-session coordinator own product navigation and cross-screen state.
- **Hybrid player:** a dedicated vertical-pager module combines UIKit paging, WebKit gameplay, and narrowly hosted SwiftUI footer surfaces. Feed data, catalog resolution, and product callbacks stay outside the reusable cell boundary.
- **Device services:** data-store integration, local-notification scheduling, image/cache helpers, logging, and deep-link/share helpers are separate services rather than view concerns.
- **Product content:** editorial feeds, catalog seeds, experiments, and resolvers are models/services. Their data formats, endpoints, and product rules are private and must not be copied.

# Publication boundary

The book may publish this responsibility map and diagrams derived from it. It may name public companion types. It must not publish private source, exact endpoints, payloads, identifiers, generated data, or unapproved symbol-level excerpts.

# TOC corrections

- Treat the app as a hybrid SwiftUI/UIKit/WebKit composition, not as a WebView wrapper.
- Treat local scheduling as a device-bound capability; do not infer an APNs or backend flow.
- Treat prewarming as a measurement-led option, never as an architectural promise.
