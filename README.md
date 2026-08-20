# sg-sentinel.sgit.ai — the SG/Sentinel website

The website for **SG/Sentinel**, a design for an app-coupled edge security and
logging layer built on the sgit project's own primitives instead of rented AWS WAF +
CloudWatch/Firehose. The load-bearing idea: **Layer 1 decides and signals** (a
CloudFront Function with no I/O — it cannot write and must not enforce), **Layer 2
acts and writes** (the sole actor and sole I/O owner), and a deferred Layer 3 thinks
asynchronously.

> **⚠ Important: SG/Sentinel has not been built.** This site publishes a set of
> research documents and ideas the project lead created in May 2026 — 19 design
> briefs (18 May), two implementation briefs and a prototype exercise (23 May) — as
> *"this is how I would build it"*, in the hope that **somebody builds this**: the
> project lead would really like to use this next generation of WAF security layer
> in his projects, but has no plans to build it at the moment, unless somebody wants
> to fund it. The code snapshot and test claims on the site describe that May 2026
> prototype exercise — a design artefact, not a deployed or maintained system.

Live site: https://sg-sentinel.sgit.ai (GitHub Pages, deployed from `dev`).

## Where the content came from

Everything is built from `sg-sentinel-website-packet` (v0.27.61, 23 May 2026):

- `briefs/` — all 23 packet documents, byte-verbatim: the 19-brief v0.27.58 design
  series, the v0.27.59/v0.27.60 implementation briefs, the testing manual, and the
  website brief itself. **The source of truth for every claim on the site.**
- `code/sentinel/` — the 115-file `sentinel/` package snapshot as built. Every code
  excerpt on the site is verbatim from these files; nothing is invented.
- `documents/` — a generated reader page per document (summary, key concepts, key
  ideas, in-page markdown rendering); regenerate with
  `python3 admin/build/gen_documents.py`.

Content rules inherited from the website brief: accuracy above all; don't overclaim
status (the live AWS path is code-complete and unit-tested via in-memory doubles,
**not yet run against a real CloudFront distribution** — stated wherever status
appears); real code and real commands only; no invented metrics.

## Structure

- `index.html` — hero + the problem + the hand-built L1→signal→L2 SVG + status
- `architecture.html` — the layer correction, the signal spine, the three targets
- `rules.html` — the tiny core's six rules (verbatim, with ATT&CK tags) and the
  fractal-graph direction
- `research.html` — 68 days of design, the tabletop simulations, the 25 gaps,
  prior art
- `try-it.html` — every `sg sentinel` command, from the testing manual
- `roadmap.html` — built vs code-complete vs deferred, honestly
- `admin/` — engineering: comms (tasks & requests), versions, build tooling
- `assets/site.css` — shared stylesheet (sgit.ai design language)

No build step is needed to view: open `index.html` and it works. The only runtime JS
is the in-page markdown reader on document pages (falls back to the raw file).

## Release process

1. Bump `admin/build/version.txt` (vX.Y.Z, exactly once per release) and add a row to
   `admin/versions.html`; update `admin/comms.html`.
2. If documents changed: `python3 admin/build/gen_documents.py`
3. `node admin/build/validate.js`
4. `git commit -am "site vX.Y.Z: ..." && git push origin dev`

Every push to `dev` runs `.github/workflows/deploy-pages.yml`: validate → auto-tag
(`vX.Y.Z`, verified against version.txt and the commit subject, next-minor enforced) →
deploy to GitHub Pages. Same pipeline as
[SGit-AI__Website](https://github.com/SGit-AI/SGit-AI__Website) and
[SGit-AI__Website__NHI](https://github.com/SGit-AI/SGit-AI__Website__NHI).

All content CC BY 4.0 unless noted. Code under the repository licence.
