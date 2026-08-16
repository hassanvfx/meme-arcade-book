---
type: Comparison Research
title: Pushscheduler versus production
status: draft
---

# Public component facts

Pushscheduler models local—not remote—notifications: permission state, persisted plans, schedule replacement, a conservative request cap, foreground handling, validated `pushscheduler://` routes, and corrupt-plan recovery.

# Approved comparison

The production repository has a dedicated local scheduler and a notification-prompt milestone policy. This supports the book's device-bound notification chapter, but it does not establish that all product re-engagement is local or that any remote-push provider exists. The public chapter will therefore teach local notification architecture through Pushscheduler and describe MemeArcade only as a product that has a separate on-device scheduler boundary.

# Redaction decision

Do not publish private notification copy, identifiers, timing policy, payload schemas, or routing targets. Use Pushscheduler's public validation model for all executable examples.
