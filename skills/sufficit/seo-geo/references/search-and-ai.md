# Conventional search and AI discovery

Use the dated [source register](sources.md); recheck provider controls before editing.

## Technical baseline

- Fetch the intended public page successfully without authentication or challenges.
  Inspect robots.txt, HTML robots and X-Robots-Tag together. robots.txt controls
  crawling, not reliable removal from an index; a blocked crawler cannot read a
  page's noindex directive. Private data requires access control.
- Align redirects, internal links, sitemap entries and absolute canonical URLs.
  Canonicalization is a signal, not a guarantee. Do not canonicalize every distinct
  campaign/service page to the homepage. Consolidate real duplicates and tracking
  variants deliberately. Avoid publishing staging/preview hostnames as canonicals.
- Use real href links and expose meaningful text without requiring interaction.
  For client-rendered pages inspect fetched HTML and rendered content separately.
  Existing SSR or prerendering can improve predictable retrieval; measure before
  expanding a metadata repair into architectural work.
- Keep the sitemap limited to intended canonical, indexable URLs with honest
  modification dates. Verify language and hreflang only for actual equivalents.
- Review mobile readability, accessible navigation, meaningful image alternatives
  and page performance. Diagnose measured bottlenecks rather than promising a
  ranking increase from a lab score.

## Entity and content quality

State what the business offers, who it serves, coverage, contact details and real
limitations in readable text. Prefer useful headings, direct explanations and
verifiable evidence. Make comparisons and commercial conditions precise. Dates,
authorship and source citations should reflect real maintenance and expertise.
Do not manufacture FAQ sections merely to target a search feature.

Use JSON-LD types that describe the actual entity: Organization and WebSite where
appropriate; Service, Product or LocalBusiness only when their semantics fit.
Use stable entity @id values to connect page, organization and offering. Keep
sameAs limited to genuine official profiles. Validate JSON syntax and schema
semantics; a valid schema.org type is not automatically a Google rich-result type.
Do not promise FAQ rich results or fabricate aggregateRating. Do not add schema
facts unsupported by the visible experience.

## Answer-oriented content (AEO)

Use actual customer questions to identify missing explanations. Give a concise,
self-contained answer near the relevant heading, then supporting evidence,
conditions and examples. Explain who an offering fits and when it does not.
Preserve qualifications beside numbers and claims so extracted answers remain
accurate. Use tables for genuine comparisons and lists for real procedures.
Do not repeat search phrases mechanically or rewrite every section as a FAQ.
This improves usability and extractability; it does not guarantee answer selection.

## Distinguish search from training

| Provider/control | Meaning and action |
| --- | --- |
| Google Search / AI Overviews / AI Mode | Standard search eligibility applies, including indexing and snippet eligibility; no special AI schema or text file is required |
| OAI-SearchBot | OpenAI search discovery; check robots rules and infrastructure access against current official documentation |
| GPTBot | Potential model-training crawl; preserve the owner's independent training policy |
| ChatGPT-User | User-triggered retrieval, not the switch for automatic search indexing; robots behavior can differ |
| Other AI providers | Identify their current official search, training and user-fetch controls separately before editing |

Do not replace robots.txt with a generic allow-all block. Read existing groups and
path restrictions; specific agent groups can change which restrictions apply.
If the owner wants search allowed and training blocked, implement that policy
explicitly without discarding existing private-path rules. A user-agent string
alone is not proof of bot identity; use providers' published verification methods
when changing network rules.

Treat llms.txt as an optional experiment only when there is a concrete consumer
and maintenance rationale. It is not an established prerequisite for Google AI
features, and no source here proves it improves ranking or citations. Do not put
secrets or instructions to override an assistant's behavior in public AI files.

## Measurement

Record the baseline and changes by URL. Use Search Console and Bing Webmaster
Tools if available for crawl/index status and query performance. Check actual
referrals and conversions as well as impressions. AI citations fluctuate with
query, time and product; record the exact query and date for manual observations.
Crawler visits alone do not prove indexing, recommendation or citation.
Account access and external URL submissions are distinct from local code checks.
