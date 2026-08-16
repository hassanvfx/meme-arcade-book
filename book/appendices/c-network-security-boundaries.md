# Appendix C: Network Observation and Security Boundaries

Network tooling is useful only when paired with consent, scope, and restraint. This appendix provides an ethical method for observing traffic that a reader is explicitly authorized to inspect. It does not authorize interception of third-party services, extraction of credentials, circumvention of platform controls, or publication of private endpoints and payloads. The Rezona public repository is used as a study in evidence discipline, not as an accusation about a company or its infrastructure.

## Authorization comes first

Before configuring a proxy, record who owns the device and account, which environment may be observed, what purpose the capture serves, which people may see it, how long it will exist, and how it will be deleted. Prefer a sandbox, a test account, a mock service, or a public teaching project. If authorization is unclear, stop. Technical access is not permission.

| Allowed learning outcome | Not an allowed outcome |
| --- | --- |
| Model a request shape with redacted, authorized evidence | Publish a production URL, token, cookie, or full payload |
| Confirm that a client handles timeout/cancellation/failure | Infer unobserved backend algorithms or data stores |
| Test a development proxy in a controlled environment | Bypass certificate controls or inspect another person's traffic |
| Improve a client contract and report a responsible issue | Name a company as irregular based on incomplete observation |

## Minimize what is collected

Start with the smallest question: for example, “Does this development client map a non-success response to a recoverable state?” Capture only enough metadata to answer it. Never retain credentials, authorization headers, cookies, device identifiers, personal data, payment data, full URLs with sensitive query strings, or user-generated content. Replace values with type-preserving labels such as `<redacted-token>` or `<opaque-id>`; remove records immediately if they are not needed for the stated purpose.

An evidence note should contain an authorization statement, the date, tool and version, controlled environment, reproduction steps, redaction method, a narrow observation, and a limit. A good limit might read: “This shows how the inspected client behaved in this controlled run; it does not establish server implementation, other-user behavior, or production policy.”

## Model the client boundary

The safest useful artifact is a typed client model, not a raw capture dump. Describe a request in terms of method category, input validation, response category, cancellation, retry ownership, and mapping to a domain result. Keep the transport object inside the adapter; return a small domain value or known failure category to the feature. A SwiftUI view should not receive raw headers or JSON merely because the client had to process them.

```text
validated input → owned request task → response classification
      → domain result / recoverable failure → native presentation
```

This same boundary improves hybrid apps. A WebView navigation action is external input; a host policy decides whether it is accepted. A deep link in a local-notification payload is external input; a native route parser validates it. Similar shapes make security review repeatable across network, web, and notification systems.

## Proxies and MITM in development

Use tools such as Proxyman only in a development or authorized test context. A proxy certificate changes the trust environment, so document its installation and remove it when the test is complete. Do not normalize disabled certificate validation or broad exceptions into production behavior. Test the failure case as well: an application should make a safe recovery decision when a request cannot be trusted or completed.

An observation is not a vulnerability report by itself. If you identify a plausible security concern in an authorized system, preserve the minimum evidence necessary, avoid public disclosure, and use the owner's responsible-reporting process. The book publishes no live incident details, private hostnames, or exploit instructions.

## Observed, inferred, and unknown

Label every research statement. **Observed** means the authorized run or public source showed the behavior. **Attributed** means a named public source made the statement. **Inferred** means an interpretation that must remain conditional. **Unknown** means no evidence supports a conclusion. This vocabulary is especially important when a UI, API, or remote game looks simple: a client-visible response cannot prove the server's storage, ranking, moderation, financial, or security logic.

The goal is not to make inspection less rigorous. It is to make the result more trustworthy. A narrow redacted observation, paired with its limits and an improved client contract, is more valuable than an impressive-looking capture that cannot be ethically shared or reproduced.

## Incident and disclosure path

If authorized testing reveals behavior that could materially affect users, do not turn the observation into a chapter anecdote or a social post. Preserve a minimal, redacted record; verify the scope without increasing collection; identify the owner; and use the organization's documented security or support channel. Include the environment, date, reproduction conditions, expected/safe behavior, observed category, and the evidence limit. Do not attach tokens, certificates, unredacted captures, or instructions that would enable misuse.

For a book revision, the editorial question is narrower: does the public material teach a durable engineering practice without exposing a real system? If yes, use a synthetic diagram or a generalized type-level example. If no, omit it. Any private incident, endpoint, security finding, capture, or implementation reference requires explicit human approval before it can appear in research or prose, and approval is not assumed simply because an author had authorized access. A responsible technical book makes its security boundary visible precisely by refusing to make sensitive material its proof.
