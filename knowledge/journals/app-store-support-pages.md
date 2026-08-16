---
type: Engineering Journal
title: "Meme Arcade App Store support pages"
description: "Public GitHub Pages support, privacy, and terms destinations for Meme Arcade 1.0."
tags: [engineering, app-store, support]
status: stable
generated:
  by: clineflow/2.0.0
  at: 2026-08-15T00:00:00Z
---

# Goal

Publish stable HTTPS destinations for the Meme Arcade 1.0 App Store support and legal links.

# Status

- [x] Planned
- [x] In progress
- [x] Complete

# Work Log

## 2026-08-15 - Public App Store destinations

Added Docusaurus pages at `/support/`, `/privacy/`, and `/terms/`. The pages retain the approved local-first disclosure: favorites, play history, and onboarding state are stored on-device; this build has no configured account, payment, push, analytics, attribution, or crash-reporting vendors. Support and content reports route to `hello@waken.ai`.

# Decisions

The existing GitHub Pages base URL is retained so App Store Connect can use stable, repository-owned HTTPS links. A shared CSS module keeps the legal pages consistent and accessible without changing the reader-bridge navigation.

# Testing

Run `npm run build` from `site/`; Docusaurus must complete with no broken-link errors.

# Open Issues

App Review contact name, phone number, and email remain a manual App Store Connect entry.

# References

- [Meme Arcade 1.0 App Store metadata](https://hassanvfx.github.io/meme-arcade-book/)
