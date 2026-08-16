---
type: Editorial Research
title: TOC corrections from evidence
status: draft
---

# Initial correction

Do not promise previous/current/next WebView prewarming. GamePlayer explicitly lazy-loads the primary page and recommends profiling before adding adjacent preloads.

# Resolved checks

- The production app has a SwiftUI root and a dedicated UIKit/WebKit vertical-pager module; hybrid runtime chapters retain this framing.
- The production app exposes a local notification scheduler boundary. The manuscript will not infer APNs or any remote notification provider.
- The production app has application-state data-store integration. The manuscript will explain persistence as a boundary without copying schemas or claiming every state field survives relaunch.

# Editorial approval needed

Human review remains required for any private-code excerpt, market assertion, or production-specific performance claim.
