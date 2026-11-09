# Customer preferred due-day guidance

Updated `sufficit-api` to 1.0.29 after an agent could not locate the customer-wide
payment preference and tried contract calendar edits instead.

## Changes and evidence

- Added the [customer due-day workflow](../../skills/sufficit/sufficit-api/references/customer-due-day.md), reachable from the skill entrypoint and sales reference. Its pinned source links identify the customer field, consolidated writer, payload and blockers.
- `POST /Sales/BillingCheckout/Link` with `contractId: null` saves both `Customer.DueDay` and the link day. Read and preserve the checkout configuration; a preference-only request does not authorize enabling checkout or reconciling a card agreement.
- Distinguished customer preference, link day, contract calendars, issued charges and renewal policy. Documented the production OpenAPI visibility limitation of the raw customer reader.
- Updated discovery metadata, card, package digest and generated index. Catalog-version validation exposed two pre-existing stale entries; reviewed their declared versions and synchronized `clear-technical-writing` (1.2.1) and `quepasa-production` (0.1.1) without editing either package.

## Validation and delivery

Initial checks: 185 packages and the changed skill passed validation; the index
was current. Catalog-version checking found the stale entries above. The 40-test
suite initially had one failure because the temporary execution plan was not
linked in the Markdown hierarchy. Final results are recorded below after correction.

No production customer was read or mutated. Source review proves the documented
implementation; it does not establish that a particular customer has unified
billing enabled or that the Genius installation has synchronized this revision.

Final validation: all 40 unittest tests passed; all 185 package manifests and
digests passed; `quick_validate.py` accepted `sufficit-api`; catalog versions,
generated skill index and Markdown coverage passed. `git diff --check` passed.

Delivery target: direct commit and push to `main` in `sufficit-ai-skills`. The
repository's existing validation workflow requests Genius catalog synchronization
after validation (or leaves the hourly synchronization as fallback); this record
does not claim that synchronization or production activation has completed.
