---
type: Engineering Journal
title: "Meme Arcade promotional landing"
description: "Promotional GitHub Pages home for the public Meme Arcade app and its case-study book."
tags: [engineering, github-pages, app-store]
status: stable
generated:
  by: clineflow/2.0.0
  at: 2026-08-18T18:11:47Z
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

## 2026-08-16 - Lulu book destination

Updated the book callout to the current Lulu listing and its title, *Modern iOS Architecture: Deconstructing the $3B MemeArcade*.

## 2026-08-17 - Printed and free ebook CTAs

Renamed both book CTAs to “Case Study Printed Edition” while retaining the Lulu hardcover URL. Added a direct “Free Case Study Ebook” PDF CTA in both the hero and lower case-study callout. The hero keeps the App Store and printed edition on its first desktop row, with the ebook on a second row; the lower callout is side by side on desktop and stacks on mobile.

## 2026-08-18 - Temporary TestFlight download CTA

Temporarily redirected the primary app-download CTA to the user-supplied TestFlight invite URL, `https://testflight.apple.com/join/QTNgQV4e`, and renamed it to “ Get the App.” The previous public App Store URL remains as a commented source line directly above the temporary URL for a quick rollback.

## 2026-08-18 - Official badge and CTA hierarchy

Added the user-supplied official Apple download badge as an SVG asset, retaining vector quality and broad modern-browser support. The badge remains the primary TestFlight CTA. On desktop it occupies its own row above the book buttons; “Case Study Printed Edition” uses the existing purple primary treatment beside the outlined “Free Case Study Ebook” CTA. On mobile, the three CTAs stack one per row.

## 2026-08-18 - Bottom-card download CTA

Added the same centered official download badge to the lower case-study card in its own row below the descriptive paragraph and above the existing book links. The badge points to the same temporary TestFlight URL as the hero CTA.

## 2026-08-18 - Bottom-card badge refinement

Moved the lower card’s download CTA below the book links and added generous vertical spacing so it has a distinct final row. It now uses the user-supplied black official Apple lockup; the hero continues to use the existing white lockup.

## 2026-08-18 - Free ebook URL refresh

Updated the shared free-ebook destination to the user-supplied dated PDF URL. Both landing-page ebook CTAs use the shared constant and therefore change together.

## 2026-08-18 - Stable free ebook route

Reverted the landing-page ebook constant to the stable `assets/modern-ios-architecture-memearcade-free-ebook.pdf` route after replacing that file in the separate website publishing repository with the user-supplied dated PDF edition. The public URL is unchanged while it serves the updated 180-page document.

## 2026-08-18 - Footer activity-link removal

Removed the `Source activities` link from the landing-page footer. The activity pages remain available by direct URL, while the footer now retains only Support, Privacy, and Terms.

# Decisions

The app-download destination remains the single primary CTA. It temporarily points to TestFlight during this beta period; the commented App Store URL is the explicit rollback target. The printed edition and free ebook are intentionally secondary, both beside/below the hero CTA and in a compact contextual callout. The landing copies only artwork covered by the public reader-bridge approval and makes no claims about private implementation, services, or product metrics. GitHub Pages deploys through Actions because the built site resides in the ignored `site/build` directory, not in a publishable branch root.

# Testing

- `npm run build` from `site/` passed with Docusaurus broken-link checking enabled.
- Inspected the generated home HTML to confirm the App Store and Lulu URLs, base-path-aware image URLs, descriptive screenshot alt text, and retained support/legal/activity links.
- `./validate-okf` and `git diff --check` passed.
- The workflow uses Node 20, `npm ci`, the existing production build command, and the official GitHub Pages actions.
- `npm run build` from `site/` passed after adding the deployment workflow.
- `npm run build` from `site/` passed after the hero artwork aspect-ratio correction.
- `npm run build` from `site/` passed after restoring the square-icon rendering.
- `./validate-okf` and `git diff --check -- site/src/pages/index.js` passed after the footer-link removal.
- `npm run build` from `site/` passed after updating the Lulu book destination.
- `npm run build` from `site/` passed after adding the printed-edition and free-ebook CTAs.
- `npm run build` from `site/`, `./validate-okf`, and `git diff --check` passed after the temporary TestFlight CTA update.

# Open Issues

None.

# References

- [MemeArcade visual case study](memearcade-book-execution.md)
- [App Store support pages](app-store-support-pages.md)
