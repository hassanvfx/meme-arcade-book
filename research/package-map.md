---
type: Architecture Research
title: Public companion package map
status: draft
---

# Package map

## GamePlayer

- `MAArcadeApp` / `MAFeedScene`: SwiftUI lifecycle and UIKit host boundary.
- `MAFeedPagerController`: native collection-view paging, drag thresholds, settling, and refresh.
- `MAStagePlayerCell` / `MAWebViewFactory`: reusable isolated game session.
- `MAWebNavigationPolicy`: HTTPS-only navigation boundary.

## Pushscheduler

- `MAAlertConductor`: SwiftUI state and notification callbacks.
- `MAAlertOrchestrator`: local schedule creation and refresh.
- `MAScheduleVault`: persisted plans and corrupt-state recovery.
- `MANotificationNavigator`: payload validation and destination mapping.

Production equivalence is not assumed; map it separately from the private sibling checkout.
