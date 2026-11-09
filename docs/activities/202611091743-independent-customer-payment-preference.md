# Customer preference without checkout

Updated `sufficit-api` to 1.0.31 to use the dedicated GET/POST
`/Sales/Customers/{contextId}/PaymentPreferences` instead of configuring a
consolidated billing link for a preference-only request. The reference includes
explicit nullable fields, expected-day concurrency, context permissions,
read-back, safe handling of uncertain outcomes and the distinction between
customer preference, existing links, contracts and issued charges.

The earlier browser test stopped at an unavailable checkout on the authorized
test customer, who has no eligible monthly service. That exposed a real API gap:
the dedicated operation now works independently of those conditions. The API
implementation is linked at its reviewed commit. The historical billing writer
remains documented only for requested billing-link configuration, not as a
preference-only fallback.

Preserved the concurrently delivered initial free-coverage workflow (1.0.30).
Updated the release metadata, card and both package digests. Validation: all 185
packages, catalog versions, generated index, Markdown coverage and skill quick
validation passed; all 40 repository unittest tests passed.

Operational acceptance on eveo-apps passed through the installed native Genius
`sufficit_api_search` / `sufficit_api_call` implementation using the existing
signed-in credential provider. The live OpenAPI exposes both operations and the
required nullable request fields. On authorized CLIENTE PARA TESTE 103333
(9acb8479-321a-4ba0-b95c-9505e3057492), the dedicated read returned no preference,
the test saved day 9, independently read day 9, rejected an obsolete expectation
with 409, then restored and independently verified null. Contract snapshots were
identical before/after. The API audit contains the two successful writes.

API implementation: 152e7f9f8981e35a68bbe38d36d71236d787a662, observed build
1.26.1109.2049 on eveo-apps. The test proves native tool/API execution; it does not
claim an autonomous model acceptance run or installed Genius skill synchronization.
The secondary API hosts were not deployed in this task.
