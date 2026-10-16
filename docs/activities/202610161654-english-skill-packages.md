# English skill packages

## Scope and result

The user requested English throughout all skill packages, not only the new
clear-technical-writing skill. Inspected the 166-package catalog and translated
Portuguese instructions, supporting references, cards, and agent metadata in
15 packages. Existing English upstream package content was preserved. Android
catalog summaries were translated; existing Google catalog descriptions were
preserved verbatim. The new writing skill remains part of this session's work.

English reference filenames replace five Portuguese filenames in meta-app-review;
all internal links were updated. README now records the English authoring rule.
API identifiers, exact UI labels, and provider messages retain their literal spelling
where needed, with English surrounding instructions. Illustrative placeholders and
narrative examples were translated. Response language still follows the user request.

## Implementation and provenance

Used a local Portuguese-to-English translation model for the first draft, followed
by editorial revision and comparison with the original contracts. Corrected
translation errors involving negations, financial terms, identifiers, required-field
markers, numeric formats, links, and Markdown structure. No repository content was
sent to a translation service. Temporary tools and original snapshots are under
/tmp and are not part of this repository change.

Updated patch versions for existing affected packages and recalculated their
catalog/manifest SHA-256 digests. Upstream authors, licenses, source URLs, and pinned
revisions remain unchanged. THIRD_PARTY_NOTICES distinguishes local language
adaptations from upstream releases. Refero's upstream English instructions and
references remain unchanged; its discovery card was translated.

| Package | Local version |
| --- | --- |
| `asaas-connection` | 0.1.1 |
| `asaas-payments` | 0.1.1 |
| `asaas-customers` | 0.3.1 |
| `asaas-invoices` | 0.6.1 |
| `github-cli` | 1.2.1 |
| `meta-app-review` | 1.0.7 |
| `refero-design` | 1.0.3 |
| `routeros-management` | 1.0.1 |
| `sufficit-api` | 1.0.3 |
| `sufficit-frontend` | 1.0.2 |
| `device-ui-android` | 0.3.1 |
| `playwright-mcp` | 0.3.1 |
| `quepasa-api` | 0.1.1 |
| `software-development` | 1.1.1 |
| `clear-technical-writing` | 1.0.0 (new package) |

## Validation

- `python3 -B scripts/validate.py`: all 166 packages passed.
- skill-creator `quick_validate.py`: all 15 affected packages passed.
- YAML parsing and release/frontmatter version consistency: passed.
- `python3 -B -m unittest discover -s tests -v`: 9 tests passed.
- Translated-document local links: all resolve.
- API method/path occurrence comparison with original documents: no losses.
- Numeric differences reviewed: version changes, English number formatting,
  and numbers written as words; repaired a dropped pagination term.
- Language scan: remaining Portuguese literals are API identifiers, source URLs,
  real UI labels, or quoted provider messages.
- Existing Google catalog descriptions: verified byte-for-byte preservation.
- `git diff --check`: passed.

The previous sufficit-frontend digest discrepancy is resolved by recalculating the
translated package's digest; global validation now passes. These are documentation
and package-integrity checks, not live API or production behavior tests.

## Delivery

Local working-tree changes only; no commit, push, catalog publication, or production
action. All three plan checkpoints are complete; the temporary plan was removed.
The pre-existing creation record for clear-technical-writing remains as task history.
