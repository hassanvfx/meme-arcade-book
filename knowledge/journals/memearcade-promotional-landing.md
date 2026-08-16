---
type: Engineering Journal
title: "Meme Arcade promotional landing"
description: "Promotional GitHub Pages home for the public Meme Arcade app and its case-study book."
tags: [engineering, github-pages, app-store]
status: stable
generated:
  by: clineflow/2.0.0
  at: 2026-08-16T03:30:00Z
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

## 2026-08-15 - GitHub Pages deployment

Added a GitHub Actions workflow that builds `site/` on pushes to `main` and deploys its `site/build` artifact through GitHub Pages. The remote Pages setting still requires a valid GitHub authentication session to select GitHub Actions as its source.

## 2026-08-16 - Hero artwork aspect ratio

Restored the intended 1254 × 1254 square app icon as the hero asset. The hero is now a plain responsive square block; its image fills that block with `object-fit: contain`, with no rotation, glow, overlay, or cropping.

# Decisions

The App Store is the single primary CTA. The book is intentionally secondary, both beside the hero CTA and in a compact contextual callout. The landing copies only artwork covered by the public reader-bridge approval and makes no claims about private implementation, services, or product metrics. GitHub Pages deploys through Actions because the built site resides in the ignored `site/build` directory, not in a publishable branch root.

# Testing

- `npm run build` from `site/` passed with Docusaurus broken-link checking enabled.
- Inspected the generated home HTML to confirm the App Store and Lulu URLs, base-path-aware image URLs, descriptive screenshot alt text, and retained support/legal/activity links.
- `./validate-okf` and `git diff --check` passed.
- The workflow uses Node 20, `npm ci`, the existing production build command, and the official GitHub Pages actions.
- `npm run build` from `site/` passed after adding the deployment workflow.
- `npm run build` from `site/` passed after the hero artwork aspect-ratio correction.
- `npm run build` from `site/` passed after restoring the square-icon rendering.

# Open Issues

None.

# References

- [MemeArcade visual case study](memearcade-book-execution.md)
- [App Store support pages](app-store-support-pages.md)
