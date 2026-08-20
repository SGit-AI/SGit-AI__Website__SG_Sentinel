# Brief: Build The SG/Sentinel Website

**version** v0.27.61
**date** 23 May 2026
**type** Website brief
**to** Implementing agent (website)
**packet** `sg-sentinel-website-packet` (this zip)

---

## 1. Your Job

Build a **static website** that explains SG/Sentinel — the idea, the architecture, the research behind it, and the working MVP — to a technical audience. Everything you need is in this zip. You are not writing new research; you are turning ~57,000 words of design briefs plus a working implementation into a clear, credible, navigable site.

**Deliverable:** a self-contained static site (HTML/CSS, minimal JS, no build step required to view — open `index.html` and it works). No backend. No login. Deployable to S3/CloudFront or GitHub Pages as-is.

## 2. What's In This Packet

| Folder | Contents | How to use it |
|---|---|---|
| `01-design-series-v0.27.58/` | **19 briefs**, the full design series (day 68) — architecture, data flows, execution model, rules engine, behavioural spec, 2 tabletop simulations, gap-resolution addendum, research brief, planning brief | **The primary source.** This is the thinking. Mine it for the concepts, the principles, and the narrative |
| `02-implementation-briefs/` | `v0.27.59` architecture brief + `v0.27.60` dev brief for the MVP | The concrete architecture: layers, signal contract, three targets, acceptance criteria. Use for the "How it works" and "Status" material |
| `03-repo-docs/` | The MVP testing manual (every CLI command across all three targets) | Source for a "Try it" / usage page. Real commands, real output |
| `04-code-snapshot/` | The actual `sentinel/` Python + JS package as built (115 files) | Proof it's real. Source for genuine code excerpts — **use real code, never invent snippets** |

Read `02-implementation-briefs/v0.27.59…` first (shortest path to understanding the system), then the planning brief and architecture brief in `01-`, then skim the rest.

## 3. The Story The Site Must Tell

Told in this order. This is the spine of the site.

1. **The problem.** Edge security and logging today means renting AWS WAF + CloudWatch/Firehose: expensive, rule-opaque, and a real-time blind spot. You can't see your traffic as it happens, you can't reason about why a request was blocked, and the bill scales with your success.
2. **The idea.** An app-coupled edge guard built on your own primitives. Because the app knows what a valid request looks like, the edge can allowlist rather than denylist — *no invalid request reaches the origin*. Rules are data, versioned in git, carrying their own metadata (attack technique, confidence, compliance mapping).
3. **The architecture.** Slow analysis, fast enforcement, in three layers. **Layer 1 decides and signals; Layer 2 acts and writes; Layer 3 (deferred) thinks.** L1 is a CloudFront Function with no I/O — it cannot write and must not enforce, so it emits a structured *signal*; L2 is the sole actor and sole I/O owner. This separation is the load-bearing idea of the whole system — give it real estate.
4. **The proof.** It exists and runs. Same rule engine across three targets — local (Node), local Docker (CloudFront-environment simulation), live AWS (CloudFront Function + Lambda@Edge) — with a **parity matrix** asserting identical decisions across all three. 149 unit tests passing; both MVP use cases (logging to S3, blocking obvious-bad) working end to end.
5. **The method.** Worth its own page: this was designed over 68 days of iterative briefs, pressure-tested with **tabletop simulations** that surfaced 25 gaps before any code was written, then resolved in an addendum. The design process is itself part of the story.
6. **What's next.** Honestly stated: fingerprint/fast-track, anomaly scoring, the Layer 3 async/LLM tier, the unified evidence-and-compliance graph, multi-CDN.

## 4. Suggested Site Structure

Keep it small and dense. Six pages, not twenty.

```
index.html          Hero + the problem + the three-layer diagram + status at a glance
architecture.html   The layer model, the signal contract, the three targets, data flow
rules.html          Rules as data: the tiny core's 6 rules, metadata, the fractal-graph direction
research.html       The design method: 68 days, the tabletop sims, the 25 gaps, prior art
try-it.html         The CLI: install, run locally, real commands + real output
roadmap.html        What's built vs deferred, honestly
```

Merge pages if the content is thin. Do not pad.

## 5. Content Rules (Non-Negotiable)

- **Accuracy above all.** Everything on the site must be traceable to this packet. If the briefs don't say it, don't claim it.
- **Don't overclaim status.** The MVP is real, but be precise: local-direct and local-docker are proven and tested; the **live AWS path is code-complete and unit-tested via in-memory doubles but has not yet been run against a real CloudFront distribution**. Say so. Credibility with this audience comes from precision, not marketing.
- **Real code only.** Pull excerpts from `04-code-snapshot/` verbatim (the L1 JS engine is the best single artefact to show — it's short, complete, and demonstrates "decide + signal, never act"). Never fabricate a snippet.
- **Real commands only.** Take them from the testing manual in `03-repo-docs/`.
- **No invented metrics.** No made-up cost savings, latency numbers, or benchmarks. The cost argument is qualitative ("avoids per-request WAF and Firehose pricing by writing directly to S3") until measured — the briefs flag measurement as an open item.
- **Technical register.** The audience is engineers and security architects. Assume they know what CloudFront, Lambda@Edge, and a WAF are. No hand-holding, no hype adjectives.

## 6. Design Direction

- **Aesthetic:** technical documentation meets systems diagram. Dark or near-dark theme suits the subject; high-contrast, monospace for anything code-adjacent, generous whitespace. Think engineering-blog seriousness, not SaaS landing page.
- **The diagram is the hero.** The L1→signal→L2 flow deserves a proper hand-built SVG (not an image asset): L1 box (no I/O, decides, emits `Schema__Sentinel__Signal`) → the signal envelope → L2 box (enforces, writes to sink). Show the three targets as a variation on the same diagram — same L1, same L2, only the transport and sink swap. Make it legible on mobile.
- **Typography over decoration.** One good serif or grotesque for headings, a monospace for code. No stock photography, no icon soup, no gradient-heavy hero.
- **Self-contained:** inline the CSS, keep JS to almost nothing (syntax highlighting and nav at most). No framework required, no npm install to view.
- Responsive, keyboard-navigable, semantic HTML, sensible `<title>`/meta per page.

## 7. Definition Of Done

1. Opens from `index.html` with no build step; all internal links work.
2. All six narrative beats (§3) present and in order.
3. The three-layer architecture diagram is a hand-built, legible, responsive SVG.
4. Every code excerpt and CLI command is verbatim from the packet.
5. Status claims match §5 exactly — including the live-AWS caveat.
6. Readable on mobile; passes a basic accessibility pass (contrast, headings, alt text).
7. A short `README.md` in the site root: what it is, how to deploy it, where the content came from.

## 8. Things To Avoid

- Turning the tabletop simulations into a wall of text — extract the **interesting** gaps (fast-track redesign as zero-trust acceleration, honeytokens as an intent signal, per-IP keying being insufficient against residential proxies) and tell them as short stories.
- Claiming SG/Sentinel replaces a commercial WAF today. It's an MVP with a deliberate tiny core and an explicit deferred list.
- Copying whole briefs onto pages. Synthesise. Link or excerpt; don't paste 3,000 words.
- Inventing a company, team, testimonials, pricing, or a logo lockup that implies a product launch.

---

Build the site from the packet, keep it honest, and let the architecture do the talking.
