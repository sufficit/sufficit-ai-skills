# Legacy renewal guidance — 2026-11-03

Nilza's DEOFORTE incident showed Genius treating the native renewal handoff's canRenew=false as a universal refusal, then stopping at a legacy authority 409. Source inspection confirms the audited legacy flow requires Session epoch/snapshot headers; the current Genius tool supports these headers. The installed client version and actual request payload were not available, so a missing-header cause is consistent with the incident, not independently proven from its request trace.

Published guidance changes in sufficit-api 1.0.20: prominent routing by each contract source; mixed customers; native automation off is not legacy; authority-session recovery with both tool headers; no automatic migration or payment marking; stale revision/ambiguous write handling without duplicate renewal. Existing Session/writer guards remain unchanged.

Validation: all 179 package digests and references validated; generated index current; Markdown coverage passed; 38 managed skill installation tests passed. This is instruction validation, not a live renewal or a behavioral replay of Nilza's session. No customer data or financial records were changed.

Delivery: main commit `ca7c06b3d77448c805d1a5a80ca941335f5fe28a`. Skills CI 41665058266 passed. Genius catalog sync 41665171359 passed and the public v2 catalog independently returned this exact revision; its pinned release.json is version 1.0.20. Existing installed skills can retain an older revision: inspect Extensions → Skills and install the new revision through the normal client flow. No Genius binary release was needed. Nilza's installed package and a renewed service in her session remain unverified.
