#!/usr/bin/env python3
"""Generates the documents/ reader pages — one per captured markdown document.

Run from anywhere: python3 admin/build/gen_documents.py
Each page carries the common apparatus (metadata, summary, key concepts, key
ideas, "on this site") and then renders the raw markdown in-page via
assets/mdreader.js. The raw file under briefs/ stays the source of truth —
the page is presentation. Adding a document = adding a dict here.
Same pattern as nhi.sgit.ai's documents section.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "documents"
SITE_VERSION = (ROOT / "admin/build/version.txt").read_text().strip()

LEAD = "Dinis Cruz (project lead) and collaborators"
AGENTS = "Architect / Developer agents, directed by the project lead"
CC = "CC BY 4.0"

DOCS = [
 # ── implementation briefs (read these first) ─────────────────────────────
 dict(slug="mvp-architecture",
  title="SG/Sentinel MVP Implementation Architecture: The sg sentinel Surface, The Three Targets, And The Signal Spine",
  md="v0.27.59__arch-brief__sg-sentinel-mvp-implementation-architecture.md",
  version="v0.27.59", date="23 May 2026", dtype="Arch brief (MVP implementation)", author=AGENTS, licence=CC,
  summary="The shortest path to understanding the system, and the document that carries the governing correction: Layer 1 never acts and never writes — it only decides and signals; Layer 2 is the sole actor and sole I/O owner. A CloudFront Function has no network and no filesystem, so it physically cannot write and by design must not enforce; blocking becomes a logged action with an enforcement side-effect. The brief fixes Schema__Sentinel__Signal as the byte-identical parity spine across three execution targets (local-direct, local-docker, live AWS), scopes the MVP to two use cases on a tiny core of six deterministic rules, places sg sentinel as a top-level peer surface composing the existing sg aws primitives, and makes the three-target parity matrix the definition of done.",
  concepts=[
   ("L1 decides + signals; L2 acts + writes", "../architecture.html#correction", "the load-bearing correction the whole MVP is built on"),
   ("The signal spine", "../architecture.html#signal", "Schema__Sentinel__Signal — one contract, byte-identical everywhere; only transport and sink swap"),
   ("The three targets", "../architecture.html#targets", "local Node, local Docker CF-env simulation, live AWS — same engine, asserted identical"),
   ("The parity matrix", "../architecture.html#parity", "identical signals, records and enforcement, or it's a P1"),
  ],
  ideas=[
   "Because L2 is a dumb actor, rules live in JS only — parity is about the envelope, not about re-running rule logic in two languages.",
   "The ephemeral test distribution runs cache-disabled (TTL 0) so origin-request Lambda@Edge sees literally every hit.",
   "Locked decisions are inherited verbatim by the implementing agent — the brief is also a decision record.",
   "Everything else in the design series is explicitly deferred; the point is to prove the spine on the smallest slice that delivers real value.",
  ],
  pages="The backbone of the architecture page; the status language on the front page and roadmap follows its acceptance criteria."),
 dict(slug="mvp-implementation",
  title="SG/Sentinel MVP Implementation: File-By-File Plan, Schemas, And The Parity Test",
  md="v0.27.60__dev-brief__sg-sentinel-mvp-implementation.md",
  version="v0.27.60", date="23 May 2026", dtype="Dev brief (implementation)", author=AGENTS, licence=CC,
  summary="The executable plan the MVP was built from: which files, which fields, which order, which tests — in six phases, each independently green, front-loading the offline use cases and deferring the riskiest piece (live Lambda@Edge) to last. It specifies the exact Type_Safe schemas, the single-file dependency-free L1 engine with the six rules inline, the L2 actor with privacy-mode hashing, the identical sink key layout across S3 and local FS, and the parity-matrix test with its canonical six-request set. The gotchas section records where the live target bites: no environment variables on Lambda@Edge, us-east-1 authoring, numbered versions, edgelambda trust, asynchronous replica deletion.",
  concepts=[
   ("The six build phases", "../architecture.html", "skeleton → L1 engine → L2 + sinks + harness → docker → deploy path → live run + parity"),
   ("The canonical request set", "../try-it.html#rules", "six requests, expected verdicts and rules — the fixture every target must decide identically"),
   ("House conventions", "../code/index.html", "Type_Safe everywhere; one boto3 seam per client; in-memory doubles; no mocks, no network in unit tests"),
   ("The gotchas", "../architecture.html#target-a", "CloudFront Functions and Lambda@Edge constraints, recorded so they are not learned the hard way"),
  ],
  ideas=[
   "Signal transport refinement: drop base64 — the header value is raw compact JSON, since CF Functions JSON.stringify natively and JSON contains no CR/LF.",
   "The JS emits snake_case keys identical to the Python schema field names so the codec maps one-to-one.",
   "Parity comparison normalises non-deterministic fields (timestamps, AWS request ids) — the rule decision is what must match.",
   "\"If you find yourself wanting to add a feature from the design series that isn't in this brief, stop: it is deferred by design.\"",
  ],
  pages="The schemas and code on the architecture and rules pages are excerpted from what this brief specified and the snapshot confirms was built."),
 dict(slug="testing-manual",
  title="SG/Sentinel MVP — Testing Manual (sg sentinel *)",
  md="sg-sentinel-testing-manual.md",
  version="—", date="23 May 2026", dtype="Testing manual (repo doc)", author=AGENTS, licence="Not stated in source",
  summary="How to exercise every sg sentinel command across the three targets — the source of every command on the try-it page. It documents the rules/local/logs/blocks/deploy/status surfaces, the offline stack with the CF-env simulation as default, the live AWS flow with its mutation gate and teardown discipline, and the test suite with its opt-in docker and live legs. It also records how far the MVP grew past the dev brief: Textual operator TUIs over every surface, a structured TUI API, a read-only LLM chat grounded in live state (Bedrock Nova, read actions only), and the traffic generator + httpget echo origin whose bare-origin-versus-fronted contrast is the impact measurement.",
  concepts=[
   ("The command surface", "../try-it.html#surface", "every sg sentinel command, with --json everywhere and mutation-gated deploys"),
   ("The offline stack", "../try-it.html#local", "real L1 + real L2 + local sink; curl the CF-env sim directly and get the signal back"),
   ("The TUIs and the read-only chat", "../try-it.html#tui", "operator screens, the TUI API, and an LLM that can inspect everything and change nothing"),
   ("Impact measurement", "../try-it.html#traffic", "the labelled corpus against a bare origin vs a Sentinel-fronted one"),
  ],
  ideas=[
   "Source IPs are hashed in the stored record by default; blocks why understands both the raw IP and its hashed form.",
   "The chat stays honest by construction: only read actions are exposed, every answer shows its tool calls and cost.",
   "gen latency is harness cost, not CloudFront runtime — real edge latency needs a live distribution.",
  ],
  pages="Rendered nearly whole as the try-it page; the TUI/chat/traffic sections update the roadmap's built list."),
 # ── the design series, day 68 (18 May 2026) ──────────────────────────────
 dict(slug="principles",
  title="The Edge Security And Logging Layer: Principles For A Gateway That Sits In Front Of Everything",
  md="v0.27.58__arch-brief__edge-security-and-logging-layer-principles.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="The founding document. Three concrete problems converge — no real-time traffic visibility, a CloudWatch+Firehose pipeline that is expensive for what it delivers, and an AWS WAF that feels rent-like and over-complex — underpinned by a real fear: a client-side bug once caused runaway redirect traffic, and nothing at the edge would catch the next one before the bill did. The principles: substrate-independent; sits in front of everything; controllable and refactorable (owned code, LLM-engineerable); the best layer for each job. Plus the goal that names the posture: make the site genuinely hostile to malicious, buggy and wasteful traffic.",
  concepts=[
   ("The problem", "../index.html#problem", "blind spot + cost line + rent — the motivation, stated concretely"),
   ("Hostile to bad traffic", "../rules.html#six", "the easy-win blocks are this principle's first instalment"),
   ("The cost argument", "../roadmap.html#open", "qualitative until measured — the site holds that discipline"),
  ],
  ideas=[
   "The edge layer is insurance against self-inflicted cost explosions as much as against attackers.",
   "Rules handle the common case at the edge; the LLM handles the ambiguous case and improves the rules over time — never on the hot path.",
   "The naming bikeshed that ended with SG/Sentinel started here.",
  ],
  pages="The problem section of the front page is this brief distilled."),
 dict(slug="execution-model",
  title="The Edge Layer Execution Model: Layered Responders And The No-Invalid-Request Principle",
  md="v0.27.58__arch-brief__edge-layer-execution-model-layered-responders.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="The execution model: CloudFront Functions as the sub-millisecond quick decision point (no I/O, embedded data only), Lambda@Edge as the capable layer, and an async third layer off the hot path — first responder, second responder, third responder. Two principles anchor it. No invalid request should reach the server: because we control both client and server we know exactly what valid traffic looks like, so the edge allowlists rather than denylists. And the edge should be hostile to our own applications too — an own-app request that doesn't match the valid profile is a bug, caught at the edge like an attack would be.",
  concepts=[
   ("The layered responders", "../architecture.html", "push each decision to the fastest, cheapest layer that can make it"),
   ("No invalid request", "../index.html#idea", "allowlist, not denylist — the posture inversion"),
   ("Not everything has to be online", "../research.html#series", "respond within a period of time, not instantly — what makes Layer 3 viable"),
   ("The symmetry principle", "../roadmap.html#deferred", "deploying an endpoint updates the edge; the profile is a deploy artefact"),
  ],
  ideas=[
   "\"Slow analysis, fast enforcement\" — the phrase the whole architecture answers to.",
   "The cache-hit versus cache-miss distinction is a controllable lever, and later a tabletop gap.",
   "Hostility to our own traffic turns the edge into a correctness check as well as a security check.",
  ],
  pages="The three-layer model on the front page and architecture page descends from this brief, with L1's role later corrected to decide-and-signal only."),
 dict(slug="edge-mvp",
  title="The Edge Layer MVP: Visibility, Blocking, Deployment, And The App-Coupled WAF",
  md="v0.27.58__dev-brief__edge-layer-mvp-visibility-blocking-deployment.md",
  version="v0.27.58", date="18 May 2026", dtype="Dev brief", author=LEAD, licence=CC,
  summary="The first MVP scoping: visibility (real-time logs replacing Firehose), blocking (a WAF that knows the app it protects), deployment (create/destroy/teardown, automated and visualised). Its central insight names the differentiator: most WAFs operate blind to the application they protect, which is the source of their complexity and their false positives; coupling the guard to the app inverts that. It also introduces the two-way conversation with edge functions — ping them, query them, ask what they know, configure them through an API — and the \"what do you know about me?\" transparency feature for legitimate users.",
  concepts=[
   ("The app-coupled WAF", "../index.html#idea", "the intelligence comes from the application, not from generic threat databases"),
   ("The three MVP problems", "../roadmap.html#built", "visibility, blocking, deployment — what the built MVP answers"),
   ("Don't play ball with attackers", "../rules.html#data", "drop silently, deflect, waste their time — asymmetry as a stance"),
  ],
  ideas=[
   "Legitimate users get transparency and minimal capture; suspected attackers get opacity and friction — the edge can tell the difference because it knows what good looks like.",
   "Optimise at the right altitude: shaving 5ms off a Lambda that then makes a 50ms network call is wasted effort.",
   "The MVP is judged against concrete debugging goals (clone traffic, too-many-requests, mobile load), not abstract WAF feature checklists.",
  ],
  pages="The visibility and blocking use cases became the MVP's two use cases; the deployment discipline became sg sentinel deploy."),
 dict(slug="rules-engine",
  title="SG/Sentinel: The Rules Engine Where Rules Are Everything",
  md="v0.27.58__arch-brief__sg-sentinel-rules-engine.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="Settles the name — SG/Sentinel — and states the central inversion: rules are not configuration on top of an engine; rules are the engine, and should be 98% of the code. The core is a tiny, tight, high-privilege machine for executing rules; everything else — every block, allow, log, cleanup — is a rule at lower privilege. From this follow the update-risk gradient (changing a rule is low-risk and constant; changing the engine is high-risk and rare), per-rule least privilege (each rule asks for exactly the data it needs), RFD-style version control per rule, and the LLM usage pattern: heavy in development and testing, minimal in production, never inline.",
  concepts=[
   ("Rules are the engine", "../rules.html", "the inversion the rules page opens with"),
   ("The tiny core", "../rules.html#six", "small enough to audit thoroughly, stable enough to trust"),
   ("LLMs author rules, never run them inline", "../roadmap.html#deferred", "slow smart work decides what the rules should be; fast deterministic rules enforce"),
  ],
  ideas=[
   "The behaviour of the entire platform at any moment is a readable function of which rules are enabled.",
   "A rule is a function with an IAM scope — single-responsibility, explicit data grant, testable in isolation.",
   "Rules-as-vault: the rule repository is version-controlled content; a deployment is a manifest of pinned rule versions.",
  ],
  pages="The rules page's framing; the MVP's flat six-rule list is this model's deliberate first slice."),
 dict(slug="rule-architecture",
  title="SG/Sentinel Rule Architecture Strategy: Rules As A Fractal Graph",
  md="v0.27.58__arch-brief__sg-sentinel-rule-architecture-strategy.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch / research brief", author=LEAD, licence=CC,
  summary="How the rules are structured: as a fractal graph — rules within rule sets, packs that activate only when a triggering rule fires, rules that select which rules run next — so the cost of a request is proportional to the rules it traverses, not the total rule count. Each rule carries rich metadata (semantic-graph position, compliance mapping, ATT&CK technique, next-rule connections, confidence, layer, data needs) and IDs-everywhere traceability follows every request through its lifecycle. The research half mines the existing body of work: CRS anomaly scoring for combining opinion rules, paranoia levels for tuning, the standard attack categories, and the honest caveat that regex rules are adversarially evadable.",
  concepts=[
   ("The fractal graph", "../rules.html#graph", "the designed structure the MVP's flat list grows into"),
   ("Rich rule metadata", "../rules.html#data", "attack tags, confidence and actions — present in the registry from day one"),
   ("The art-of-the-possible reduction", "../index.html#idea", "encrypted objects and static pages make the valid space tiny, so the invalid is obvious"),
   ("Reuse vs build", "../research.html#prior-art", "reuse CRS patterns and anomaly scoring; build the app-coupling, the graph, the traceability"),
  ],
  ideas=[
   "A request for /etc/passwd is never valid; a PHP page on a static site is never valid — the easy wins are easy because the valid space is constrained.",
   "The deterministic-to-opinion spectrum lets rules express how sure they are; the engine combines confidences instead of treating every rule as binary.",
   "Our edge over pure-CRS WAFs is the app-coupling plus the async LLM layer that catches what regex misses.",
  ],
  pages="The rules page's graph section and metadata table; the six MVP rules are this brief's easy-win category, built first as it prescribed."),
 dict(slug="interactivity",
  title="SG/Sentinel Interactivity And Deployment Phases: Two-Way Layer Invocation, Local-Everywhere, And Dev/Main/Prod Rules",
  md="v0.27.58__arch-brief__sg-sentinel-interactivity-and-deployment-phases.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="\"SG/Sentinel is not a spectator sport\": every layer is individually invocable and the layers can be triggered in sequence from the front gate — essential in isolated deployments where the gateway may be the only reachable surface. The whole solution runs locally, identically to production. Dangerous dev-only rules (a rule that enables/disables other rules; bypass-all; full-state dump) are invaluable in development and phase-gated so they never reach production; the production bundle contains only the rules production runs. Rules promote dev → main (= QA) → prod, with main equalling production so what is tested is exactly what ships.",
  concepts=[
   ("Local-everywhere", "../try-it.html#local", "realised in the MVP as targets B and C, fully offline"),
   ("Dangerous dev-only rules", "../rules.html#graph", "maximum power in dev, minimum surface in prod — safe because bundles are phase-aware"),
   ("The value-equation inversion", "../index.html#idea", "security that the application controls, instead of a bolted-on thing that gets its teeth removed"),
  ],
  ideas=[
   "The traditional WAF failure mode, named: it breaks things, so it gets set to allow-all — decorative security.",
   "Never ship a rule to a live server that is not being invoked.",
   "Main-equals-production removes the gap between what was tested and what runs.",
  ],
  pages="The three-target offline story and the deploy-parity language across the site come from here."),
 dict(slug="codebase-extension",
  title="SG/Sentinel As An Extension Of The Codebase: Type-Safe Validation, Agentic Development, And Security Zones",
  md="v0.27.58__arch-brief__sg-sentinel-as-codebase-extension.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="Security as part of the codebase, not a separate bolted-on tool — possible now because agentic development, local-everywhere and owned code removed the barriers (licensing, deployment friction, the local-production gap) that always made it fail before. Type-safe runtime validation is the mechanism: security logic is disproportionately validation logic, and a type-safe boundary at the edge means everything behind it can trust the data — security at the edge reduces complexity everywhere behind the edge. Sentinel is, architecturally, the application's trust boundary; horses-for-courses places each check at its right altitude.",
  concepts=[
   ("Sentinel as the trust boundary", "../architecture.html#correction", "untrusted outside, validation at the boundary, trusted inside"),
   ("Type_Safe as the validation mechanism", "../code/index.html", "the same discipline the codebase uses internally, applied at the edge — visible in every schema"),
   ("The agentic development model", "../research.html#method", "developer, AppSec, QA and architect agents working the same locally-runnable code"),
  ],
  ideas=[
   "Validation happens once at the boundary; downstream code stops re-validating defensively.",
   "Developer-friendliness and security quality are the same thing viewed from two angles.",
   "Codebase-continuous does not mean review-light: the trust-boundary code is the most-reviewed code.",
  ],
  pages="Why every schema in the code snapshot is Type_Safe; the conventions box on the code page."),
 dict(slug="delegation",
  title="SG/Sentinel Delegation And Choke-Points: Designing Code To Run Behind The Gate",
  md="v0.27.58__arch-brief__sg-sentinel-delegation-and-choke-points.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="The deeper continuation of the codebase-extension brief: concentrate checks at the choke-points between trust zones instead of validating everywhere defensively; design application code knowing it runs behind Sentinel so it can delegate validation and authorisation to it; and treat any behavioural difference between QA and production as a major bug (deploy parity). The \"no 404s at the API layer\" signal turns the layered architecture into a self-checking system: an error deep in the stack that the gate should have caught is information about where the security model has a gap.",
  concepts=[
   ("Deploy parity", "../architecture.html#parity", "the P1 invariant, realised in the MVP as the parity matrix"),
   ("Choke-points", "../architecture.html#correction", "the checks concentrate where trust zones meet; Sentinel is the outermost"),
   ("No 404s at the API layer", "../research.html#observations", "deep-layer errors as signals of shallow-layer gaps"),
  ],
  ideas=[
   "Same-code-everywhere is the killer feature: the rule tested locally is byte-for-byte the rule in production, so deployment holds no surprises.",
   "Every request becomes a way to make the system better — checks migrate to their correct altitude as errors reveal misplacement.",
   "Progressive lock-down: start permissive, observe, tighten to minimal as the valid profile is learned.",
  ],
  pages="Deploy parity became the parity matrix; the L1 engine being byte-identical across targets is this brief's same-code principle, moved to JS by the CloudFront constraint."),
 dict(slug="time-dimension",
  title="Time As A First-Class Dimension In SG/Sentinel: Faster For The Good, Detected-Before-Damage For The Bad",
  md="v0.27.58__arch-brief__sg-sentinel-time-as-first-class-dimension.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="Two inversions of conventional WAF thinking. First: because we know what good looks like, security can make good users faster — fingerprint and allowlist the known-good, skip the expensive checks, and security stops being a tax everyone pays. Second: detect before damage, not instantly — an attacker probing makes many requests, and we need to catch them before they do harm, not on request one; we want them to make one mistake, a call none of our code ever makes, and the allowlist makes that mistake visible. The success metric follows: not requests blocked, but damage prevented, with legitimate users unaffected.",
  concepts=[
   ("Detect before damage", "../research.html#tabletop", "the time budget for detection is the probing window — minutes, not milliseconds"),
   ("Make good users faster", "../roadmap.html#deferred", "the fast-track design — deferred, and rewritten by the tabletop as zero-trust acceleration"),
   ("The multiple timelines", "../architecture.html", "immediate, real-time-plus, near-real-time, analytical, historical — each serving the others"),
  ],
  ideas=[
   "Most WAFs hold no state after the decision; Sentinel makes the state object as rich as possible and refines the decision over time.",
   "The fast layers enforce known decisions; the slow layers detect unknown attackers — the combination needs no instant malice-detection.",
   "Damage prevented beats requests blocked as a success metric.",
  ],
  pages="The detect-before-damage story in the research page's tabletop section; the fingerprint sits at the top of the deferred list because this brief made it the spine."),
 dict(slug="developer-friendliness",
  title="SG/Sentinel Developer-Friendliness And The Evidence Graph: What The Engine Knows, And Why That Makes Development Better",
  md="v0.27.58__arch-brief__sg-sentinel-developer-friendliness-and-evidence-graph.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="Developer-friendliness has a direct correlation with the quality of the code — a primary design objective, not a side effect. Its flagship feature: the evidence graph, a semantic, growing record of everything Sentinel currently knows about an IP, user or request, including why every decision was made — queryable as \"what do you know about me?\", a dev-only superpower excluded from production bundles by construction. Vault-per-user gives the graph a storage home with anonymity modes from know-nothing to know-everything, and the zero-knowledge property bounds its sensitivity: Sentinel knows what happened, never what was inside.",
  concepts=[
   ("The evidence graph", "../roadmap.html#deferred", "deferred, but the log record and request-id traceability are its wired-in first loop"),
   ("Dev-only insecure code is safe", "../rules.html#graph", "the best way to keep code from being exploited in production is for it not to be there"),
   ("Every block has an inspectable reason", "../architecture.html#signal", "shipped in the MVP: reason and rule_id ride in every signal and record"),
  ],
  ideas=[
   "The LLM in the mix means checks that require interpretation are now tractable — out-of-band, on the analytical timeline.",
   "Wire the data loop first, enrich second: don't build the graph as a backend abstraction.",
   "Code often gets added to compensate for missing data; ask instead where the most efficient place to compute it is.",
  ],
  pages="The \"what do you know about me?\" instinct survives in the MVP as blocks why and the read-only chat over live state."),
 dict(slug="research-standards",
  title="SG/Sentinel: Learning From Standards, Open Source, And Threat-Intelligence Services",
  md="v0.27.58__research-brief__sentinel-learning-from-standards-and-services.md",
  version="v0.27.58", date="18 May 2026", dtype="Research brief", author=LEAD, licence=CC,
  summary="Compatibility over reinvention: tag rules with MITRE ATT&CK techniques (T1190 first), consume the OWASP Core Rule Set as a baseline layer via SecLang, study Coraza as the reference library-first engine, and speak STIX/TAXII for threat-intel feeds. The threat-intel service landscape is mapped (AbuseIPDB, GreyNoise, Spamhaus, OTX and others) with the critical caveat that reshaped the design: nearly 4 in 10 attacking IPs are now residential or compromised home connections, so IP reputation is context, never verdict. The zero-knowledge boundary is drawn explicitly: no malware or file-hash scanning at the Sentinel layers, ever — traffic, IP and behavioural intelligence only.",
  concepts=[
   ("Prior art, positioned", "../research.html#prior-art", "OPA, Sigma, CRS/Coraza, deception, zero-trust — what each contributed"),
   ("ATT&CK tagging", "../rules.html#data", "shipped in the MVP registry: every blocking rule carries its technique"),
   ("IP reputation is context, not verdict", "../research.html#tabletop", "the residential-proxy reality that killed per-IP keying"),
  ],
  ideas=[
   "Threat intel runs on the async timelines, feeding the evidence graph — Sentinel can afford rich enrichment precisely because it never needs it inline.",
   "The Sigma compile-to-backend model is the concrete mechanism for staying multi-CDN.",
   "Contribute back once patterns are proven — the de-commoditising strategy in reverse.",
  ],
  pages="The prior-art table on the research page; the ATT&CK tags in the rules table; the deferred threat-intel row on the roadmap."),
 dict(slug="compliance",
  title="Compliance As A Living Graph: Mapping Standards To What SG/Sentinel Actually Deploys",
  md="v0.27.58__arch-brief__sg-sentinel-compliance-as-living-graph.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch / strategy brief", author=LEAD, licence=CC,
  summary="Compliance as a computed property of the running system, not a checkbox: build graph-based versions of the major standards (GDPR, ISO 27001, OWASP Top 10, OWASP AI), map each requirement to the platform capabilities and Sentinel rules that satisfy it, and the posture becomes a live readout — enable a logging rule and specific requirements flip to met; disable it and they flip back. The platform contributes inherent properties (encryption, zero-knowledge, audit trails) for free; Sentinel contributes the dynamic, rule-dependent ones. Specific and computed also means validatable by third parties — the opposite of a vague claim.",
  concepts=[
   ("The living compliance graph", "../roadmap.html#deferred", "deferred with the unified graph; the rule metadata schema keeps its slot"),
   ("The three graphs are one", "../research.html#observations", "rule prevents technique, satisfies requirement, observed as evidence"),
   ("Rules carry standard mappings", "../rules.html#data", "the metadata schema this vision needs, present from day one"),
  ],
  ideas=[
   "\"No WAF in front of the product\" genuinely breaks named requirements; encrypted-by-construction genuinely satisfies others — posture reflects reality in both directions.",
   "Conservative claims by design: show partial and unmet, never overclaim — the mapping supports certification, it is not certification.",
   "LLM-generated graph standards, multi-party-checked, community-verified, possibly standards-as-vaults in their own repo.",
  ],
  pages="On the roadmap's deferred list; its business-value framing informs how the site presents the compliance direction without overclaiming."),
 dict(slug="behavioural-spec",
  title="SG/Sentinel Rules Of The Game: The Behavioural Specification In English",
  md="v0.27.58__arch-brief__sg-sentinel-rules-of-the-game-behavioural-spec.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief (behavioural spec)", author=LEAD, licence=CC,
  summary="The answer key: the behaviour of the whole system written in plain English, following a request step by step from arrival through Layer 1's ID-and-log, the deterministic rules, the decision, Layer 2 validation, the application, async analysis, and the log landing in S3. Eight governing principles head it — no invalid request reaches the application; log every hit; every block has a reason; the same code runs everywhere — and the open behaviour questions (where does the fingerprint allowlist live? when exactly is the log finalised?) are flagged deliberately for the tabletop simulations to probe.",
  concepts=[
   ("The execution flow", "../architecture.html", "steps 0–8, later narrowed by the MVP to the L1→signal→L2 spine"),
   ("The eight rules of the game", "../index.html", "the principles every behaviour must honour"),
   ("Flagged open questions", "../research.html#tabletop", "the spec deliberately leaves the gaps visible for the simulations to find"),
  ],
  ideas=[
   "When the code is implemented, the question is: does it behave like this document describes? If yes, it is correct.",
   "Writing behaviour in English before code is what made the tabletop possible.",
   "The spec is designed to be refined — gaps found by simulation fold back in before implementation.",
  ],
  pages="The behavioural authority behind the parity matrix; the research page's tabletop section tests exactly this document."),
 dict(slug="tabletop-1",
  title="SG/Sentinel Tabletop Simulation Part 1: Generic Flows And Logging",
  md="v0.27.58__arch-brief__sg-sentinel-tabletop-simulation-1-generic-and-logging.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief (tabletop simulation)", author=LEAD, licence=CC,
  summary="Five simulated requests — a static-page happy path, a returning fast-tracked user, a privacy-mode logging request, a cache hit, a freshly-deployed page the profile doesn't know yet — traced layer by layer against the behavioural spec, honestly: eleven gaps found, two major. GAP 2.1 exposed that Layer 1 (no I/O) cannot check a dynamic fingerprint allowlist, pointing at signed-token fast-track; GAP 5.1 showed the symmetry principle blocking legitimate deploys, forcing the known-good profile to become an atomically-deployed artefact with observe-mode first.",
  concepts=[
   ("The tabletop method", "../research.html#tabletop", "requests traced on paper, gaps flagged with proposed resolutions, before any code"),
   ("The fingerprint storage gap", "../research.html#tabletop", "GAP 2.1 — the finding that moved fast-track to a signed token"),
   ("IP escrow", "../roadmap.html#deferred", "GAP 3.1 — \"IP logging off\" is too binary; capture-but-encrypt is the designed mode"),
  ],
  ideas=[
   "The log-finalisation owner (who writes the record, when) only became a question when a request was actually traced — exactly what the exercise is for.",
   "Cache-hit traffic sees only Layer 1, so Layer 1 must suffice for cached static content — a cache-policy-meets-security-policy coupling.",
   "Evidence-graph keying and anonymity mode must be designed together.",
  ],
  pages="First half of the 25 gaps on the research page; GAP 1.1's log-finalisation answer became \"L2 writes the record\" in the MVP."),
 dict(slug="tabletop-2",
  title="SG/Sentinel Tabletop Simulation Part 2: Blocking Malicious Activity",
  md="v0.27.58__arch-brief__sg-sentinel-tabletop-simulation-2-blocking.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief (tabletop simulation)", author=LEAD, licence=CC,
  summary="The attack half: an obvious-bad probe, a WordPress scan, a brute-force on a valid login endpoint, a fast-tracked user turning malicious, a slow patient probe from rotating IPs, and an in-profile exploit — fourteen gaps, seven major. The consequential cluster: fast-track must never skip authorisation (9.1/9.2, the fundamental redesign); per-IP is insufficient against distributed attacks (8.2/10.3, multi-dimensional evidence keying); Sentinel is blind to auth outcomes without a reverse coupling from the app (8.3); and no-invalid-request is necessary but not sufficient — in-profile exploits need content rules and, ultimately, a secure application (11.1/11.2, the honest limit).",
  concepts=[
   ("Fast-track redesigned", "../research.html#tabletop", "the gap that changed the architecture — told in full on the research page"),
   ("Per-IP insufficiency", "../research.html#tabletop", "residential proxies defeat per-source limits; key per target too"),
   ("The honest limit", "../roadmap.html#limits", "defence in depth, not sole defence — stated as a design output, not a caveat"),
  ],
  ideas=[
   "The one positive finding: no-invalid-request beats slow distributed probing by construction — every out-of-profile request is blocked individually, regardless of rate or rotation.",
   "\"Drop silently\" is not a thing HTTP can do — block actions needed concrete HTTP-level definitions (GAP 6.1 → drop_403 / deflect_404).",
   "The gaps were found on paper, not in production — the entire value of the exercise.",
  ],
  pages="Second half of the tabletop section; GAP 6.1's HTTP-level actions ship in the MVP as the action enum."),
 dict(slug="addendum",
  title="SG/Sentinel Consolidated Addendum: Prior Art, Cross-Cutting Observations, And Gap Resolutions",
  md="v0.27.58__addendum__sg-sentinel-prior-art-observations-gap-resolutions.md",
  version="v0.27.58", date="18 May 2026", dtype="Addendum", author=LEAD, licence=CC,
  summary="The bridge between the design series and the build: rather than retrofit fourteen briefs, one document captures the prior art to position against (OPA/Rego, Detection-as-Code/Sigma, deception technology, zero-trust), five cross-cutting observations (the three graphs are one; replay-from-S3 is the test corpus; Sentinel guards its own control plane; rule retirement is missing; the fingerprint is the spine), and the consolidated resolutions to every tabletop gap — fast-track as signed-token zero-trust acceleration, honeytoken-touch revoking trust, the known-good profile as a deploy artefact, per-target rate limiting, IP-escrow mode, and HTTP-level block actions.",
  concepts=[
   ("The gap resolutions", "../research.html#tabletop", "the corrected behavioural spec the MVP was built against"),
   ("The five observations", "../research.html#observations", "listed in full on the research page"),
   ("Honeytokens as the intent signal", "../research.html#tabletop", "IAM verifies identity; deception confirms intent"),
  ],
  ideas=[
   "Independent convergence on established disciplines is reassuring (the design is sound) and useful (mature implementations to learn from).",
   "Rule retirement: if a control covers a behaviour more efficiently than a rule, implement the control and save the compute.",
   "Production traffic stored replayably in S3 answers \"would this new rule have blocked anything legitimate?\" almost for free.",
  ],
  pages="The single most-cited document on this site: the research page's prior-art and observations sections, and several roadmap rows, trace here."),
 dict(slug="planning",
  title="SG/Sentinel Future Research And The Path To MVP",
  md="v0.27.58__planning-brief__sg-sentinel-future-research-and-path-to-mvp.md",
  version="v0.27.58", date="18 May 2026", dtype="Planning brief", author=LEAD, licence=CC,
  summary="The boundary marker: \"we have enough design to focus next on building the first MVP\" — further design has diminishing returns until implementation surfaces real-world learning. It lists the memos still worth recording (the fast-track reconception first; incident response and the after-block lifecycle; Sentinel's own failure modes), the prior-art deep-dives to run during implementation (OPA, Sigma's compile pipeline, Coraza, deception patterns, BeyondCorp), what is deliberately parked, and a ten-step MVP sequence with its definition of done — including the cost measurement that closes the founding argument's loop.",
  concepts=[
   ("The MVP boundary", "../roadmap.html", "what to build first, what to defer — the roadmap page follows this discipline"),
   ("The parked list", "../roadmap.html#deferred", "parking is sequencing, not abandoning"),
   ("Gaps gate steps", "../research.html#tabletop", "each MVP step lists the tabletop resolutions it depends on"),
  ],
  ideas=[
   "Fail-open versus fail-closed for Sentinel itself is an open question flagged as existential — the guard's own failure modes need their own memo.",
   "The concrete cost model is the loop that validates the founding motivation.",
   "The v0.27.59/60 implementation pair narrowed even this brief's scope further — tiny core won.",
  ],
  pages="The roadmap page is this brief's discipline applied to the built MVP."),
 dict(slug="architecture-flows",
  title="SG/Sentinel Architecture And Data Flows: How It All Fits Together",
  md="v0.27.58__arch-brief__sg-sentinel-architecture-and-data-flows.md",
  version="v0.27.58", date="18 May 2026", dtype="Arch brief", author=LEAD, licence=CC,
  summary="The component map and the two founding use cases, end to end. Logging: Layer 1 captures every hit, the data is cleaned and structured, and Sentinel's job ends when the record lands in S3 — existing downstream code picks up from there, a deliberately tight boundary. Blocking: easy wins deterministic at Layer 1, app-coupled validation at Layer 2, async feedback from Layer 3 updating the fast layers. Together with the TUI mockups it was written to be the acceptance criteria the dev team implements against.",
  concepts=[
   ("The component map", "../architecture.html", "layers, S3, evidence, rule-set, TUI, CLI — the full picture the MVP narrowed"),
   ("Sentinel's logging ends at S3", "../architecture.html#l2", "the boundary that kept use case 1 scoped and achievable"),
   ("Two use cases as the proving slice", "../index.html#proof", "logging and blocking exercise the core of everything"),
  ],
  ideas=[
   "The two use cases were chosen because they are the minimal end-to-end slice that proves the architecture.",
   "Every block has a logged reason — an acceptance criterion here, a schema field in the built system.",
   "The honest risks section flags scope creep as a named enemy of the MVP.",
  ],
  pages="The architecture page is this document plus the v0.27.59 correction (L1 no longer blocks inline — it signals)."),
 dict(slug="tui-mockups",
  title="SG/Sentinel TUI Mockups: The Operator Surfaces As Acceptance Criteria",
  md="v0.27.58__dev-brief__sg-sentinel-tui-mockups.md",
  version="v0.27.58", date="18 May 2026", dtype="Dev brief", author=LEAD, licence=CC,
  summary="Nine ASCII-art mockups of the operator surfaces — deployment reality, live traffic, blocks, logs + S3 browsing, rules management, rule detail and testing, the deployed code, threat intel, and the deploy flow — with one principle running through all of them: every UI must be chatbot-friendly, backed by a structured TUI API, so you can talk to the surface as well as click it. The deployed-code view carries the trust punchline: \"this is the exact code running in prod right now\", readable because the tiny core is small.",
  concepts=[
   ("The operator surfaces", "../try-it.html#tui", "five of the mocked screens shipped in the MVP: rules, logs, blocks, status, traffic"),
   ("Chatbot-friendly by construction", "../try-it.html#tui", "the TUI API underneath is what the read-only LLM chat runs on"),
   ("The deployed-code view", "../architecture.html#l1", "sg sentinel tui status shows the exact materialised L1 engine"),
  ],
  ideas=[
   "The TUI is the visual surface; the chat is the conversational surface; both are views of the same TUI API.",
   "Mockups as acceptance criteria: concrete enough to implement, explicitly not final designs.",
   "The deferred-feature mockups (threat intel, fractal graph) were deliberately not built — they need deferred features.",
  ],
  pages="The testing manual's §6–7 show these mockups made real; the try-it page documents them."),
 # ── the packet's own brief ────────────────────────────────────────────────
 dict(slug="website-brief",
  title="Brief: Build The SG/Sentinel Website",
  md="00-WEBSITE-BRIEF.md",
  version="v0.27.61", date="23 May 2026", dtype="Website brief", author="Project lead → implementing agent", licence="Not stated in source",
  summary="The brief that scoped this site: turn ~57,000 words of design briefs plus a working implementation into a clear, credible, navigable static site. It fixes the narrative spine (problem → idea → architecture → proof → method → what's next), the content rules this site follows — accuracy above all, don't overclaim status, real code only, real commands only, no invented metrics — and the definition of done, including the hand-built architecture SVG and the precise live-AWS caveat. Captured here for the same reason everything else is: the provenance discipline applies to the site itself.",
  concepts=[
   ("The six narrative beats", "../index.html", "the front page follows the spine in order"),
   ("The content rules", "../roadmap.html", "precision over marketing — the status language everywhere on this site"),
   ("The definition of done", "../admin/index.html", "how the site is validated and released"),
  ],
  ideas=[
   "\"Credibility with this audience comes from precision, not marketing.\"",
   "\"Use real code, never invent snippets\" — every excerpt on this site is verbatim from the snapshot.",
   "\"Build the site from the packet, keep it honest, and let the architecture do the talking.\"",
  ],
  pages="Became this site; the engineering page documents how its rules are enforced by the validate gate and CI."),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · documents · sg-sentinel.sgit.ai</title>
<meta name="description" content="Original document, readable in-page: summary, key concepts and key ideas, then the full markdown. {dtype}, {date}.">
<link rel="canonical" href="https://sg-sentinel.sgit.ai/documents/{slug}.html">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<nav class="site"><div class="row">
  <a class="brand" href="../index.html">sg-sentinel<span>.sgit.ai</span></a>
  <span class="stage-pill">mvp</span>
  <a class="ver" href="../admin/versions.html" title="Site release history">{ver}</a>
  <a class="nl" href="../architecture.html">Architecture</a>
  <a class="nl" href="../rules.html">Rules</a>
  <a class="nl" href="../research.html">Research</a>
  <a class="nl" href="../try-it.html">Try it</a>
  <a class="nl" href="../roadmap.html">Roadmap</a>
  <a class="nl here" href="index.html">Docs</a>
  <a class="nl" href="../code/index.html">Code</a>
  <a class="nl" href="../admin/comms.html">Comms</a>
  <a class="gh" href="https://github.com/SGit-AI/SGit-AI__Website__SG_Sentinel">★ GitHub</a>
</div></nav>

<main class="doc">
<div class="crumb"><a href="../index.html">sg-sentinel.sgit.ai</a> / <a href="index.html">documents</a> / {slug}</div>
<h1>{title}</h1>

<div class="docmeta">
  <span class="k">Type</span><span class="v">{dtype}</span>
  <span class="k">Version</span><span class="v">{version}</span>
  <span class="k">Date</span><span class="v">{date}</span>
  <span class="k">Author</span><span class="v">{author}</span>
  <span class="k">Licence</span><span class="v">{licence}</span>
  <span class="k">Source</span><span class="v"><a href="../briefs/{md}">raw markdown</a> · <a href="https://github.com/SGit-AI/SGit-AI__Website__SG_Sentinel/blob/main/briefs/{md}">view on GitHub</a></span>
</div>

<h2 id="summary">Summary</h2>
<p>{summary}</p>

<h2 id="concepts">Key concepts</h2>
<ul>
{concepts}
</ul>

<h2 id="ideas">Key ideas</h2>
<ul>
{ideas}
</ul>

<h2 id="on-site">On this site</h2>
<p>{pages}</p>

<h2 id="read">Read the document</h2>
<div class="mdread-label">📄 Original document · {version} · {date} · rendered from the <a href="../briefs/{md}">raw markdown</a> (the source of truth)</div>
<div class="mdread" id="mdread" data-src="../briefs/{md}"><noscript><p class="dim">In-page rendering needs JavaScript — <a href="../briefs/{md}">open the raw markdown</a>.</p></noscript></div>

<div class="pagenav">
  <a href="index.html">← All documents</a>
  <a href="../briefs/{md}">Raw markdown →</a>
</div>
</main>

<footer class="site"><div class="cols">
  <div>
    <div class="brandline">sg-sentinel<span>.sgit.ai</span></div>
    <p>SG/Sentinel — an app-coupled edge security and logging layer: L1 decides and signals, L2 acts and writes, L3 (deferred) thinks. All content CC BY 4.0 unless noted.</p>
    <p class="verline">site <a href="../admin/versions.html">{ver}</a> · <a href="../admin/index.html">engineering</a></p>
  </div>
  <div>
    <h4>The system</h4>
    <a href="../architecture.html">Architecture</a>
    <a href="../rules.html">Rules as data</a>
    <a href="../try-it.html">Try it</a>
    <a href="../roadmap.html">Roadmap</a>
  </div>
  <div>
    <h4>The record</h4>
    <a href="../research.html">The design method</a>
    <a href="index.html">Documents</a>
    <a href="../code/index.html">The code</a>
  </div>
  <div>
    <h4>Site</h4>
    <a href="../admin/comms.html">Comms</a>
    <a href="../admin/versions.html">Versions</a>
    <a href="../llms.txt">llms.txt</a>
    <a href="https://sgit.ai">sgit.ai</a>
    <a href="https://github.com/SGit-AI/SGit-AI__Website__SG_Sentinel">GitHub</a>
  </div>
</div></footer>

<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="../assets/mdreader.js"></script>
</body>
</html>
"""

def concepts_li(items):
    return "\n".join(
        f'  <li><a href="{u}"><b>{html.escape(t)}</b></a> — {d}</li>' for t, u, d in items)

def ideas_li(items):
    return "\n".join(f"  <li>{i}</li>" for i in items)

OUT.mkdir(exist_ok=True)
for d in DOCS:
    md_file = ROOT / "briefs" / d["md"]
    assert md_file.exists(), f"missing source markdown: {md_file}"
    page = PAGE.format(ver=SITE_VERSION, slug=d["slug"], title=html.escape(d["title"]),
        md=d["md"], version=d["version"], date=d["date"], dtype=d["dtype"],
        author=d["author"], licence=d["licence"],
        summary=d["summary"], concepts=concepts_li(d["concepts"]),
        ideas=ideas_li(d["ideas"]), pages=d["pages"])
    (OUT / f"{d['slug']}.html").write_text(page)
    print(f"wrote documents/{d['slug']}.html")
print(f"{len(DOCS)} document pages at {SITE_VERSION}")
