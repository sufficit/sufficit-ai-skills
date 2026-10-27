# Primary source register

Research date: 2026-10-26. These are concise implementation notes, not copied
provider manuals. Revisit relevant sources when applying the skill, particularly
crawler controls, image constraints and platform tooling.

| Source | Supported decision | Research status |
| --- | --- | --- |
| [Open Graph protocol](https://ogp.me/) | Core tags, image subproperties, locale, arrays and first-value preference | Read |
| [Google Search Essentials](https://developers.google.com/search/docs/essentials) | Technical eligibility, helpful content, crawlable links and spam boundaries | Read |
| [Google AI features](https://developers.google.com/search/docs/appearance/ai-features) | Existing SEO applies; indexed and snippet-eligible pages; no special AI file/schema requirement | Read |
| [Google favicon](https://developers.google.com/search/docs/appearance/favicon-in-search) | Hostname scope, square icon, stable URL and crawling requirements | Read |
| [Google Organization](https://developers.google.com/search/docs/appearance/structured-data/organization) | Organization disambiguation and logo guidance; no appearance guarantee | Read |
| [Google robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro) | Crawl blocking differs from noindex and access control | Read |
| [Google canonicals](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) | Consistent canonicalization signals and duplicate consolidation | Read |
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots) | Search, training and user-triggered retrieval are distinct; published IP information | Read |
| [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a) | Primary reference for Bing/Copilot policy checks | Search result was accessible; direct page returned a JavaScript shell. Recheck before asserting detailed rules |
| [Meta sharing documentation](https://developers.facebook.com/docs/sharing/webmasters/) | Platform-specific image and scraper constraints | Fetch returned HTTP 429; exact limits and WhatsApp cache behavior were not verified |

## Application tools (not research evidence)

- [Google Rich Results Test](https://search.google.com/test/rich-results): check
  supported search features, not every schema.org type or actual indexing.
- [Schema.org validator](https://validator.schema.org/): check schema vocabulary;
  successful validation is not a search-feature entitlement.
- [Meta Sharing Debugger](https://developers.facebook.com/tools/debug/): inspect
  Meta scraping; do not infer that it invalidates WhatsApp caches.
- [X Cards documentation](https://developer.x.com/en/docs/x-for-websites/cards/overview/abouts-cards):
  consult current requirements when X is a target; not verified in this research.

## Initial motivating evidence

A supplied WhatsApp screenshot showed a Sufficit link card for
landing.sufficit.com.br displaying a white triangle inside a black circle. The
screenshot establishes an incorrect displayed identity reported by the owner.
No production HTTP audit was performed while creating this package; it does not
establish whether og:image, favicon fallback, an inherited template, a redirect
or stale cache caused the preview. Do not preserve private conversation details
or participants' identities in this public package.
