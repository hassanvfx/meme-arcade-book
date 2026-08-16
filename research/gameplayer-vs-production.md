---
type: Comparison Research
title: GamePlayer versus production
status: draft
---

# Public component facts

GamePlayer keeps vertical scrolling in a UIKit pager, limits active interaction to the primary page, reuses player cells, lazy-loads games, clears web state before reuse, uses non-persistent web data, and exposes no JavaScript bridge. It recommends measurement before adjacent-page preloading.

# Approved comparison

Both systems isolate hybrid-player responsibility from broader product orchestration. GamePlayer is the public laboratory: UIKit controls paging and reuse, WebKit hosts the active game, and SwiftUI supplies the application lifecycle. MemeArcade applies the same division inside a product that also owns tabs, onboarding, fullscreen session coordination, catalog resolution, native overlays, persistence, and re-entry policy.

The editorial lesson is not that a public component is production code. It is that a reusable player becomes safer when its ownership contract is explicit: native code owns navigation, paging, lifecycle, and product actions; the remote page owns only its web interaction.

# Redaction decision

Publish generalized lifecycle diagrams and public GamePlayer examples. Keep private cell implementation, game URLs, catalog contents, instrumentation, and product callbacks out of the manuscript unless individually approved.
