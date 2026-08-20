# sg-sentinel.sgit.ai — Layer 1 decides and signals; Layer 2 acts and writes

> SG/Sentinel is an app-coupled edge security and logging layer built on your own
> primitives instead of rented AWS WAF + CloudWatch/Firehose. Because the app knows
> what a valid request looks like, the edge **allowlists** rather than denylists —
> no invalid request reaches the origin. Rules are data, versioned in git, carrying
> their own metadata.

*Source: <https://sg-sentinel.sgit.ai/index.html> · site v0.1.0 · markdown twin of the front page.*

---

## The problem

Renting your own blind spot: no real-time view of traffic, logging as a major cost
line (CloudWatch + Firehose per-GB), and a rule-opaque WAF priced like rent. Under it
all, one fear: a client-side bug once caused runaway redirect traffic, and nothing at
the edge would catch the next one before the bill did.

## The idea

| | Generic WAF | SG/Sentinel |
|---|---|---|
| Posture | Denylist known-bad | **Allowlist known-good** |
| Knows the app? | No | **Yes — coupled to routes, schemas, contracts** |
| Rules | Vendor-configured, rented | Data in git with attack/confidence/compliance metadata |
| Every block | Often unexplainable | **Has a logged, inspectable reason** |
| Logging | CloudWatch → Firehose | Clean, replayable records straight to S3 |

## The architecture

**Slow analysis, fast enforcement, in three layers.** Layer 1 (CloudFront Function,
no I/O — it cannot write and must not enforce) decides and emits a structured signal,
`Schema__Sentinel__Signal`. Layer 2 (Lambda@Edge, the sole actor and sole I/O owner)
validates the signal, enforces pass / 403 / 404, and writes one replayable log record
to the sink. Layer 3 (deferred) thinks asynchronously — never inline. The signal
envelope is byte-identical across all targets; only the transport and the sink swap.
[The full architecture](architecture.html).

## The proof

Same rule engine across three targets — local Node, local Docker
(CloudFront-environment simulation), live AWS — with a parity matrix asserting
identical decisions across all of them. **149 unit tests passing; both MVP use cases
(logging to S3, blocking obvious-bad) working end to end.** Status, precisely:
local-direct and local-docker are proven and tested; the live AWS path is
code-complete and unit-tested via in-memory doubles but has not yet been run against
a real CloudFront distribution. [Try it](try-it.html) · [Roadmap](roadmap.html).

## The method

Designed over 68 days of iterative briefs, pressure-tested with tabletop simulations
that surfaced 25 gaps before any code was written — fast-track redesigned as
zero-trust acceleration, honeytokens as an intent signal, per-IP keying dropped
against residential proxies. [The research](research.html) ·
[all 23 documents, readable in-page](documents/index.html) ·
[the code snapshot](code/index.html).

## Site

- [Comms: tasks & requests](admin/comms.html)
- [Release history](admin/versions.html)
- [llms.txt](llms.txt)
- [sgit.ai](https://sgit.ai) · [nhi.sgit.ai](https://nhi.sgit.ai)
