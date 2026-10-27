---
name: seo-geo
description: Audit and improve landing-page SEO (Search Engine Optimization), GEO (Generative Engine Optimization), AEO (Answer Engine Optimization), and Open Graph previews. Use for Google/Bing visibility, AI answer discovery and citations, structured data, or wrong WhatsApp images, favicons and brand logos.
metadata:
  version: "1.0.0"
  author: "Sufficit"
---

# SEO, GEO and answer optimization

Make a landing page identifiable, fetchable and understandable in shared links,
conventional search and AI search. Follow the requested scope: an audit produces
findings; an implementation changes the authorized site. Creating this skill does
not authorize applying it to production or submitting URLs to external services.

## Choose the outcome

Treat these labels as overlapping practices, not independent ranking systems:

| Practice | Intended outcome | Evidence to collect |
| --- | --- | --- |
| SEO — Search Engine Optimization | Discoverable, indexable pages with useful conventional search results | Crawl/index reports, relevant query impressions, clicks and conversions |
| GEO — Generative Engine Optimization | Accurate discovery and representation in generated answers | Dated query samples, citations, referral traffic and factual accuracy |
| AEO — Answer Engine Optimization | Clear answers to specific user questions | Visible answer quality and observed answer placement when available |
| Open Graph / social previews | Correct brand and page identity in shared links | Initial metadata, fetched image and actual target-app preview |

AEO overlaps with SEO and GEO. A social preview is a separate presentation surface;
fixing it does not demonstrate improved ranking. Define the user's target surface
before selecting checks. No practice guarantees placement, indexing or citations.

## Establish evidence

Identify the exact public URL, affected surface, approved brand assets and hosting
framework from available project context. Read repository instructions and existing
metadata before editing. A screenshot demonstrates the displayed result, not which
metadata field, cache or crawler produced it. Do not diagnose a host from a logo's
appearance. Record observed facts separately from hypotheses.

Inspect the response HTML and headers as well as the rendered browser DOM. Check
redirects and the actual image bytes. Never treat a successful browser screenshot
or a changed source file as proof that a remote crawler receives the intended head.

Choose the relevant reference:

- Wrong shared image, favicon, stale preview or framework default:
  [social previews and identity](references/social-previews.md).
- Search visibility, content, indexing or AI retrieval:
  [search and AI discovery](references/search-and-ai.md).
- Provider requirements, dates and research limitations:
  [primary sources](references/sources.md). Recheck live documentation before
  relying on changing crawler names, supported formats, limits or tool behavior.

## Implement proportionately

Prioritize broken public access and incorrect brand identity, then canonical and
indexing conflicts, then metadata/content quality. Fix metadata where the framework
owns the head; do not append a second competing set. Supply critical sharing tags
in the initial HTML through the existing SSR, static generation or server template.
Do not introduce a framework migration to repair a small metadata defect.

Use approved logo artwork. If new social-card design is required in a Sufficit
project, follow its DESIGN.md and the project's design workflow. Keep metadata
changes separate from an unrequested visual redesign. Respect existing indexing
and AI-training choices; search optimization is not consent to enable training.

Use structured data only for real entities and facts supported by page content.
Never invent ratings, locations, prices, credentials, statistics or endorsements.
Do not add hidden instructions to AI crawlers, keyword stuffing, or bot-only sales
claims. Do not present llms.txt, schema markup or crawler access as a ranking fix.

## Validate and deliver

For each affected route, report evidence rather than a synthetic SEO score:

| Surface | Acceptance evidence |
| --- | --- |
| Share metadata | Initial HTML has the intended nonconflicting metadata; image URL fetches and decodes; brand survives a square crop |
| Search identity | Correct reachable favicon and organization logo, each assessed separately |
| Crawl/index eligibility | Final response, canonical, robots directives and infrastructure agree with the intended policy |
| Structured data | JSON parses; supported types checked with a suitable validator; claims match visible content |
| Public behavior | Deployed URL fetched after an authorized deployment; actual target-app preview checked when available |

Use the existing build and checks appropriate to changed files. Check representative
nested routes and tracking-query variants when they share metadata generation.
For browser-dependent checks use available browser tooling; report unavailable
external validators or account-only reports as unverified.

Deliver findings ordered by impact, with URL/file, evidence, proposed or applied
change and verification result. Distinguish local implementation, deployed output,
platform cache refresh and actual indexing/citation. No tool can guarantee the
last two. Do not report a WhatsApp fix without observing a new WhatsApp preview;
if that observation is unavailable, state exactly what HTTP evidence was verified.
