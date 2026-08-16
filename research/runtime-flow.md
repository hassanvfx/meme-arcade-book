---
type: Architecture Research
title: Runtime flow
status: draft
---

# User-session flow

1. Native app launches and loads product/feed state.
2. UIKit owns vertical page movement; the primary item owns the active game session.
3. A reusable `WKWebView` loads the selected remote game under HTTPS-only policy and non-persistent web data.
4. Product state is persisted according to the production implementation under review.
5. When the device itself knows a suitable reminder, local notification infrastructure persists and schedules the plan.
6. A notification tap validates the payload, selects a route, and returns control to native navigation.

This is the approved generalized production trace: application root → product state and tab selection → feed provider/resolver → native vertical pager → primary WebView game session → persisted product state → optional local scheduling → validated native re-entry. It describes responsibility boundaries, not private URLs, payloads, or backend implementation.
