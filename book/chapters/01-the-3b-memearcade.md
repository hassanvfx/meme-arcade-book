---
title: Introduction — The $3B MemeArcade
slug: introduction
---

# The $3B MemeArcade: What We Can—and Cannot—Deconstruct

An arcade cabinet has always been a compact agreement between many systems. A player sees a screen, a joystick, and a coin slot; behind that simple surface are hardware constraints, a game loop, distribution, operations, and the rules that make a session feel immediate. AI-native games and interactive apps have inherited the same problem at a much larger boundary. Their experience may be generated, refreshed remotely, or shaped by an online model, but a person still encounters it through a particular device, operating system, network, and moment of attention.

This book is about the iOS architecture that makes that encounter dependable. Its case study is **MemeArcade, the App**: an iOS product whose private implementation is not published here. Its title, **The $3B MemeArcade**, is deliberately broader. It names the emerging AI-gaming market in which products such as MemeArcade are being built. It is never a claim that MemeArcade, the App, has a $3 billion valuation, has raised that amount, or generates that amount of revenue.

The rounded figure has a bounded source. Mordor Intelligence projects a 2026 global market of USD 3.05 billion for generative AI in game environment and narrative design. Research and Markets estimates USD 3.4 billion for the broader AI-in-games market in the same year. These are different studies with different scopes; they corroborate that the category is multi-billion-dollar, but they must not be added together. In this book, **MemeArcade Market** means that category context; **MemeArcade, the App** means the technical product we study. [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/generative-ai-in-game-environment-and-narrative-design-market) [Research and Markets](https://www.researchandmarkets.com/reports/6081189/ai-in-games-market-report)

That distinction matters because precise language is an architectural habit. Engineers learn early not to confuse a view with its model, a cache with its source of truth, or an observed request with a server guarantee. The same discipline applies to an editorial case study. We will say what is public, what is generalized from an approved private observation, and what remains outside the book.

## A market signal, not a product valuation

The AI-gaming category is no longer only a prediction. In June 2026, Axios reported that Sekai raised a $20 million Series A around text-prompt mini-app creation. In May 2026, Fortune reported $56 million in new funding for Astrocade, an AI-created game platform. These reports are useful as dated evidence that investors and builders are pursuing new forms of interactive creation. They do not prove that every AI-gaming product has the same architecture, audience, economics, or safety model. [Axios, June 1, 2026](https://www.axios.com/2026/06/01/sekai-mini-app-startup-funding) [Fortune, May 5, 2026](https://fortune.com/2026/05/05/astrocade-raises-56-million-series-b-sequoia-video-games-platform-ali-amir-sadeghian/)

Gizmo is another contextual signal. Business Insider reported in March 2026 that the team behind the AI mini-game app joined Meta's Superintelligence Labs; the report says the deal's financial terms were not disclosed. We use that story only to understand the competition for people, tools, and distribution in consumer AI. It is not evidence about MemeArcade, the App, and it does not authorize speculation about another company's implementation. [Business Insider, March 5, 2026](https://www.businessinsider.com/ex-snapchat-engineers-behind-gizmo-join-meta-superintelligence-labs-2026-3)

The useful engineering question is therefore not, “Which company will win?” It is: **what must an iOS application own when playable, generative, and remote experiences arrive through a device?** The answer is not “everything.” A hybrid product is healthier when it gives each runtime a legible job.

```
MemeArcade Market (editorial context)
        │
        │  informs the problem space; does not value the app
        ▼
MemeArcade, the App (private case study)
        │
        ├── Native shell: identity, navigation, device state
        ├── Product services: catalog, orchestration, policy
        ├── Hybrid runtime: authorized web content and gameplay
        └── Device capabilities: storage, notifications, lifecycle
```

The lines in that diagram are responsibilities, not a claim about unpublished module names or private endpoints. They are the working vocabulary for the rest of this book.

## The question beneath the technology

SwiftUI, Combine, Swift Package Manager, async/await, WebKit, and local notifications can look like separate topics. In a production app they converge on one question: **which component is allowed to make which decision, and for how long?**

Take a user who opens a game from a vertical feed. The native application may decide that a cell is the current candidate for activation. It may retain navigation ownership while the web runtime owns the game loop. A request service may fetch a catalog while a durable store remembers a harmless preference needed to restore the session. A notification scheduler may create a local reminder, but it cannot invent authorization that the user has not granted. Each boundary exists because every system fails differently.

This is why “native versus web” is a poor framing. The durable framing is **native orchestration and web participation**. The native shell is where device-bound responsibility belongs: lifecycle, permission, navigation, state restoration, accessibility, privacy, and the policy that determines whether a remote destination may load. The web runtime can be excellent at shipping playable content, iterating rapidly, and carrying interaction logic. Neither runtime should quietly impersonate the other.

For a junior developer, this is a practical rule: let the code that owns a fact be the code that changes it. If iOS owns which tab is selected, a web view should not silently replace that decision. If a remote game owns its rendering loop, the native cell should not attempt to recreate it. For a senior engineer, the same rule becomes an operational concern: trace ownership so that a timeout, cancellation, process termination, or permission denial has a predictable recovery path.

## The public components, and the private case study

The book does not ask readers to trust a private source dump. Instead, it moves between inspectable public examples and carefully bounded observations from MemeArcade, the App.

The public examples are deliberately smaller than the product:

- The [SwiftUI and Combine article](https://uriostegui.medium.com/building-reactive-applications-with-swiftui-and-combine-a-tutorial-on-ios-app-simple3d-25d18eef7649) introduces reactive state and view updates.
- [ios-framework](https://github.com/hassanvfx/ios-framework) gives us a concrete Swift Package Manager and tandem-app boundary.
- [ios-storage](https://github.com/hassanvfx/ios-storage) provides a public persistence discussion, including state that survives a process lifetime.
- [receipe-app](https://github.com/hassanvfx/receipe-app) is the small async/await laboratory: a request, a decode, a loading state, an error state, and a cancellation question.
- [rezona-api](https://github.com/hassanvfx/rezona-api) is a public client-observation exercise, useful for reasoning about request models without inventing backend behavior.
- [GamePlayer](https://github.com/hassanvfx/GamePlayer) is the primary visible example of native paging paired with web gameplay.
- [Pushscheduler](https://github.com/hassanvfx/Pushscheduler) isolates local notification scheduling as device infrastructure rather than a server feature.

MemeArcade, the App, supplies the composition problem: how such concerns meet in one product. We describe that composition through type-level responsibilities, diagrams, lifecycle narratives, and trade-offs. We do not publish full private files, credentials, internal endpoints, raw payloads, proprietary schemas, or unapproved business logic. A private code excerpt, production log, or product-specific diagram requires explicit human approval before it can appear in this manuscript.

This boundary is not a disclaimer appended after the interesting part. It creates better teaching material. A reader who learns to ask “what capability is crossing this boundary?” can apply that question to any project. A reader who memorizes a private class name cannot.

## From Ultrakam to a hybrid application

My own path into this question began in a much more visibly native era. In [“The Time Apple Featured My App at WWDC14”](https://uriostegui.medium.com/the-time-apple-featured-my-app-at-wwdc14-a42dc4cd19bb), I describe Ultrakam and the experience of building for the iPhone platform at a time when a focused native application could carry nearly all of its behavior in one runtime.

That history does not make an argument from nostalgia. It makes the contrast clearer. The device is still where a user grants permission, receives interruption, restores a task, and judges whether an experience feels coherent. What changed is the number of collaborators behind one screen: package boundaries, concurrent tasks, remote content, a WebView process, caches, and optional re-engagement systems. The modern architecture challenge is to keep those collaborators from turning one user action into an untraceable chain of guesses.

The chapters ahead keep returning to a simple proposition:

> Native did not disappear. Native moved up the stack.

In a hybrid iOS application, native code may do less rendering than it once did, but it frequently carries more responsibility. It is the place where product intent meets operating-system reality.

## What the Rezona chapter does—and does not do

One companion repository deserves special care. The network-observation chapter uses the public [rezona-api](https://github.com/hassanvfx/rezona-api) repository to teach an authorized client-side method: capture traffic only when you have permission, remove credentials and personal data, model what the client can actually observe, and label unknowns as unknowns.

That is not an investigation of Rezona as a company, and it is not an accusation of irregularity. A request seen from a client can establish that the client made a request and received a response. It cannot establish an unseen database schema, business practice, security posture, or internal decision. This distinction is especially important when using MITM tooling such as Proxyman. The tool can make a boundary visible; it does not grant authority to cross it.

The chapter will use a conservative vocabulary:

| We can say | We cannot say without separate evidence |
| --- | --- |
| “The authorized client sent this redacted request shape.” | “The backend stores data in this schema.” |
| “The client receives this response field.” | “The company uses this field for this business purpose.” |
| “The client retries under this observed condition.” | “The service guarantees this reliability behavior.” |

That restraint is not merely legal caution. It is sound systems engineering. Good debugging begins by separating observation from inference.

## A working lens for the chapters ahead

Architecture is most useful when it turns a vague failure into a smaller question. “The game did not load” is not yet a question a team can answer. Was the selected item unavailable? Did the catalog request fail? Was an unsupported origin rejected by the navigation policy? Did the WebView process terminate? Did the game load but fail to return a native action? Was a notification scheduled for a state the user had already left? Those are distinct failures with different owners.

The book will repeatedly use four lenses to make that separation visible:

| Lens | Question | Typical iOS responsibility | Typical remote responsibility |
| --- | --- | --- | --- |
| Ownership | Who may change this fact? | Navigation, persisted preferences, permission state | Play session and remote interaction state |
| Lifetime | How long should it survive? | View, scene, app, or local store lifetime | Response, web process, or server-session lifetime |
| Trust | What must be verified before use? | URL/origin policy, deep-link routing, notification input | Content delivery and remote authorization |
| Observation | What evidence can we record safely? | Timings, lifecycle events, redacted failures | Publicly documented interface behavior |

Consider a simple choice: should a game begin loading when its cell becomes visible? A junior implementation might start immediately because visibility appears to equal intent. The lifecycle chapter will show why that assumption is too coarse. A cell may be briefly visible during a fast scroll; its task may need cancellation; its web process can consume memory even after attention has moved elsewhere. The actual design is a policy: identify a candidate, decide when it becomes primary, instrument the outcome, and release or reuse resources according to a measured budget.

The same progression applies to persistence. “Save state” is too broad to guide a production decision. A developer must ask which state is safe to retain on the device, when a write occurs, what happens if the app is killed during that write, and whether restoration will recreate a safe and coherent user path. The DataStore chapter uses a public example to teach those questions. It does not publish MemeArcade's private schema.

This is also the reason this manuscript places trade-offs beside implementation detail. A framework pattern is not architecture merely because it compiles. It becomes architecture when its ownership, lifetime, trust, and observation costs are explicit. The public repositories give readers a chance to inspect compact answers; MemeArcade gives us the larger composition problem.

## Reader activity: establish the evidence boundary

Before moving into code, open the original [WWDC14 / Ultrakam account](https://uriostegui.medium.com/the-time-apple-featured-my-app-at-wwdc14-a42dc4cd19bb). Write two short columns in a notebook:

| Publicly supported context | Not established by the article |
| --- | --- |
| The author's historical experience shipping an iOS application | MemeArcade's current internal architecture |
| A useful contrast between a native-first product and a modern hybrid product | Any market valuation or financing for MemeArcade, the App |
| Why device-level craft continues to matter | Any assertion about a third party's backend or business practices |

The expected observation is that author context is not production evidence. Carry that distinction into every reader activity. It is the discipline that lets this book make a real architectural argument without treating private implementation as public material.

## How to read the book

Each chapter follows the same rhythm:

1. **Concept.** A junior-friendly model establishes the responsibility being discussed.
2. **Public implementation.** You open the original repository or article directly and inspect one bounded pattern.
3. **MemeArcade implementation.** A generalized diagram or lifecycle explains how the same responsibility composes inside the case study.
4. **Production trade-offs.** We examine the cost of the decision under cancellation, memory pressure, permissions, failure, and future change.
5. **Reader activity.** A QR code and companion link take you to the original public source—not to a duplicate web copy of this manuscript.

The GitHub Pages site is intentionally only a reader bridge. It gives you an activity and the expected observation, then sends you to the original public repository or article. The source material remains where it can be inspected in its own context; this book remains the architectural synthesis.

The first substantive chapters begin with state and modularity because an application cannot safely cross a hybrid boundary if it does not know who owns its state. From there we move through persistence, concurrency, network observation, WebView trust, GamePlayer, observability, local notifications, a complete session, and finally the reusable seams that survive the case study.

The goal is not to make every app look like MemeArcade. The goal is to make the next application easier to reason about: a system where every runtime has a job, every boundary has a policy, and every important user path can be explained from launch to return.
