# Appendix A: Architecture Atlas

This atlas is a responsibility map for the book's case-study vocabulary. It is deliberately not a private MemeArcade diagram or package graph. The names below describe roles that recur across the public companion projects and the generalized architecture discussion. They let a reader reason about ownership without receiving private source, endpoints, catalog data, or product policy.

## The composition view

```text
User intent
  → native product shell
  → route and session policy
  → feature capability
       ↘ durable state
       ↘ cancellable client/catalog boundary
       ↘ hybrid player and WebView policy
       ↘ local notification scheduler
  → typed result, recovery state, and redacted observation
```

The native shell owns the application's visible state and its user-facing decisions. A capability owns one narrow behavior. Infrastructure adapters turn durable storage, transport, WebKit, or notification-system APIs into narrow contracts. This direction matters: the storage adapter cannot select a tab; a pager cannot decide a campaign; a remote page cannot own account or route policy.

| Area | Owns | Does not own | Useful test seam |
| --- | --- | --- | --- |
| Product shell | Intent, route, screen state, recovery presentation | Raw WebKit/URLSession details | State reducer or view-model fixture |
| Domain/policy | Valid references, allowed transitions, failure categories | Brand copy and private credentials | Pure unit tests |
| Storage adapter | Restore/save validated device state | Navigation or account decisions | In-memory/temporary store |
| Client boundary | Request lifetime, decoding, mapping to domain result | Backend inference or raw JSON in views | Stub transport and cancellation test |
| Player host | Native pager lifecycle, one bounded remote stage | Catalog ranking and global route ownership | Synthetic stage reference/event sink |
| Web policy | Navigation/response acceptance and capability boundary | Private host lists or exceptions | Allow/reject table |
| Scheduler | Device-owned notification-plan projection | Server/APNs behavior or marketing policy | Pending-request fixture |
| Observation adapter | Redacted transition/failure event | User content, tokens, full URLs, raw payloads | Event schema snapshot |

## Runtime flow

A generalized session is not an exact claim about the private app. It is a safe sequence of handoffs that readers can use to review any hybrid iOS feature:

1. The native shell accepts a user intent and reads only validated restoration state.
2. A feature starts cancellable catalog or service work under an owner with a known lifetime.
3. The result becomes a domain reference, not an unbounded backend object.
4. A native pager may mark a cell as a candidate, but only the primary cell is entitled to activate a remote stage.
5. The WebView policy evaluates navigation and response behavior; remote content remains external input.
6. A native action is returned as a typed request, then the product shell decides whether it is allowed.
7. A device-owned schedule, if any, is validated and projected into local notification requests.
8. Re-entry repeats validation rather than trusting stale routes or payloads.

At every arrow, record a small transition event without user content. The same map supports debugging: if a session fails, first ask which owner had the value, what validation ran, and which recovery behavior was available.

## Persistence and notification maps

Durable storage has a different clock from interface state. A screen can disappear while a save is pending; a process can be interrupted between a write and the next launch. Store only values that the device can safely own, restore into a validated representation, then let product state decide what to display. Encryption, key handling, migration, retention, and reset behavior must be intentional rather than accidental consequences of a convenience API.

Local notifications follow a similar projection pattern:

```text
validated device plan → named local requests → system delivery → validated route request → native product decision
```

The plan is not the same thing as system requests, and receipt is not permission to navigate automatically. This distinction prevents duplicates, stale delivery, and untrusted payloads from acquiring more authority than they deserve.

## Hybrid trust model

The hybrid boundary separates two runtimes. Native code owns device policy, product navigation, local state, and capability grants. Remote content owns only its authorized presentation and interaction surface. HTTPS is a transport baseline, not a sufficient trust decision. A policy should make schemes, hosts, response behavior, storage mode, JavaScript allowances, bridge capability, and lifecycle reset behavior explicit. It should be reviewed whenever a capability expands.

The public GamePlayer example makes this shape inspectable: native paging and primary selection remain native, while one stage hosts a constrained remote session. The book does not publish private origins, bridge contracts, headers, cookies, or remote-game behavior.

## How to use the atlas

Use the tables as a design-review checklist. For a proposed feature, name its owner, lifetime, input validation, output type, persistence rule, trust boundary, observation fields, and safe failure state. If a component needs an app singleton, a private model, or a live account simply to exercise its contract, move that product concern back to the composition root. A clean map is not a promise that every part is a Swift package; it is evidence that responsibilities can be tested and changed without hidden authority.

## Architecture review worksheet

Use this worksheet before accepting a new dependency or remote capability. It is intentionally short enough to complete during planning, then revise during implementation.

| Prompt | A useful answer looks like |
| --- | --- |
| What event begins the work? | A user intent or validated restoration, not an incidental view redraw |
| Who owns cancellation? | One named feature/session owner with a known end-of-life event |
| What crosses the seam? | Small domain types and typed failures, never raw credentials/payloads |
| What is durable? | A device-safe representation with a migration/rejection path |
| What is remote? | A constrained input surface governed by explicit navigation/capability policy |
| What can be observed? | Redacted lifecycle outcomes with a retention and access rule |
| What is the safe failure? | A visible native recovery state that does not invent data or authority |

If any row requires a private implementation detail to be intelligible, document the category rather than publishing the detail. The purpose of an atlas is not to expose more architecture; it is to make the architecture that can be responsibly discussed coherent.

## Change-impact pass

When a capability changes, trace its impact through the map before merging it. A new durable field can affect migration, encryption, restore validation, UI state, logs, and notification routes. A new WebView capability can affect allowlists, process lifetime, accessibility, incident response, and the private data a remote page might receive. A new client result can affect cancellation, cache invalidation, error presentation, and reader-facing claims. The map does not prescribe a single implementation, but it makes downstream owners visible early enough to involve them.

This pass is also the appropriate place to separate a general teaching diagram from a private design. The appendix may state that a product composition root supplies policy to an adapter. It may not publish a real private target graph, internal service name, endpoint, host list, message format, or production measurement without explicit human approval. Treat that approval as a release gate, not a writing convenience. A diagram becomes more useful when its edges are labeled with responsibility, validation, and lifetime rather than private identifiers that other readers cannot safely reuse.
