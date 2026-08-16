---
type: Engineering Journal
title: "Meme Arcade promotional landing"
description: "Promotional GitHub Pages home for the public Meme Arcade app and its case-study book."
tags: [engineering, github-pages, app-store]
status: stable
generated:
  by: clineflow/2.0.0
  at: 2026-08-15T06:00:00Z
---

# Goal

Make the GitHub Pages home a responsive promotional landing that leads with the public Meme Arcade App Store listing and offers the related Lulu case-study book as a secondary CTA.

# Status

- [x] Planned
- [x] In progress
- [x] Complete

# Work Log

## 2026-08-15 - Landing implementation

Replaced the reader-bridge home with a dark neon promotional landing. It uses the approved public icon and the three supplied case-study screenshots, links to the public App Store listing, and adds the requested Lulu book destination. Source activities and App Store support/legal routes remain accessible.

# Decisions

The App Store is the single primary CTA. The book is intentionally secondary, both beside the hero CTA and in a compact contextual callout. The landing copies only artwork covered by the public reader-bridge approval and makes no claims about private implementation, services, or product metrics.

# Testing

- `npm run build` from `site/` passed with Docusaurus broken-link checking enabled.
- Inspected the generated home HTML to confirm the App Store and Lulu URLs, base-path-aware image URLs, descriptive screenshot alt text, and retained support/legal/activity links.
- `./validate-okf` and `git diff --check` passed.

# Open Issues

None.

# References

- [MemeArcade visual case study](memearcade-book-execution.md)
- [App Store support pages](app-store-support-pages.md)
