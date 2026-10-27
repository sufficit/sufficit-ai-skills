# Social previews and brand identity

Consult [sources](sources.md) for current provider documentation. The workflow below
is an engineering diagnostic procedure; platform-specific rendering is not guaranteed.

## Separate the surfaces

| Surface | Main input to inspect | Common mistaken fix |
| --- | --- | --- |
| Shared link card | Open Graph metadata, actual image response, platform cache | Replacing only favicon.ico |
| Browser tab / search favicon | link rel=icon and its resource | Changing only og:image |
| Organization identity in search | Organization JSON-LD logo and consistent entity details | Assuming it controls WhatsApp |
| Installed / home-screen app | Manifest icons and apple-touch-icon | Assuming manifest updates every social card |

## Diagnose before changing

1. Preserve the exact shared URL, timestamp and app. Follow redirects and record
   status, final URL, Content-Type, cache headers and any X-Robots-Tag. Fetch with
   GET: HEAD can behave differently and does not prove that the body is an image.
2. Parse the original response head with an HTML parser. Inspect title,
   description, canonical, all og:* and twitter:* tags, icon links and JSON-LD.
   Check duplicate or conflicting tags, inherited layout defaults and the order
   of multiple og:image values. Open Graph gives preference to the first value
   when conflicting arrays are interpreted; image subproperties belong with
   their associated image. A regex hit elsewhere in HTML is insufficient.
3. Compare the fetched head with the browser DOM. If only hydration supplies the
   tags, move their generation into the project's initial response. Inspect
   framework metadata configuration, generated routes and static asset defaults.
4. Download each candidate image without cookies, referer or login. Verify final
   status, MIME type, decodability, dimensions and visible artwork. A 200 response
   containing a login page or SPA fallback is a failure. Check TLS, redirect loops,
   signed URL expiry, anti-hotlink rules, CDN/WAF challenges and robots access.
5. Repeating a request with a documented crawler user-agent can reveal response
   differences, but does not reproduce the provider's IP, network or cache.
   Use verified crawler logs when available; do not disable the WAF globally.

## Produce a coherent metadata set

Provide page-specific title and description, one canonical URL, and the Open Graph
core fields og:title, og:type, og:url and og:image. Add og:description, og:site_name
and the actual locale when appropriate. Use absolute public HTTPS image URLs and
keep og:url consistent with the chosen canonical. Image alt text describes the
artwork; declared width, height and MIME type must match the resource.

For an X card, inspect its current documented requirements before adding
name="twitter:card" and related title, description, image and alt tags. Do not
assume every application implements the same fallback rules.

Use approved brand art, never a template/vendor icon. A 1200 × 630 JPEG/PNG with
important artwork inside a generous central safe area is a practical starting
point, not an Open Graph requirement or a universal WhatsApp specification.
Preview both the full image and a center square crop at small size. Keep the
company identifiable without tiny text. Choose an opaque background when needed
for contrast; verify actual file size and the target platform's current limits.

For Google search favicon eligibility, inspect the root of the relevant hostname,
not just the landing route. Use a stable square icon URL, crawlable home page and
image, and verify Google's current size guidance. Google supports one favicon per
hostname; subdirectories cannot each demand a different search favicon.
For Organization.logo, Google's documented minimum is 112 × 112; ensure a reachable
supported image and legibility against white. These are separate assets/roles even
when they share the same approved source artwork.

## Cache and verification

After an authorized deployment, fetch the public HTML and image again. Check CDN
responses separately from a platform's saved preview. For a materially changed
social image, a versioned asset filename can avoid reusing stale image bytes;
update its metadata URL while preserving the page canonical. This does not force
an app to refetch cached page metadata. Keep favicon URLs stable where possible.

Use platform inspection tools when available and permitted. Meta's Sharing
Debugger is evidence for Meta scraping, not proof that a WhatsApp cache was purged.
Observe a newly composed share in the actual target app. Old messages may retain
old previews. Do not promise a cache TTL or immediate refresh without documented,
observed evidence. Do not keep changing the page URL with random query strings as
a permanent fix.
