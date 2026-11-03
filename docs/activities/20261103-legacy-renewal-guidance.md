# Legacy renewal guidance — 2026-11-03

Nilza's DEOFORTE incident showed Genius treating the native renewal handoff's canRenew=false as a universal refusal, then stopping at a legacy authority 409. Source inspection confirms the audited legacy flow requires Session epoch/snapshot headers; the current Genius tool supports these headers. The installed client version and actual request payload were not available, so a missing-header cause is consistent with the incident, not independently proven from its request trace.

Published guidance changes in sufficit-api 1.0.20: prominent routing by each contract source; mixed customers; native automation off is not legacy; authority-session recovery with both tool headers; no automatic migration or payment marking; stale revision/ambiguous write handling without duplicate renewal. Existing Session/writer guards remain unchanged.

Validation: all 179 package digests and references validated; generated index current; Markdown coverage passed; 38 managed skill installation tests passed. This is instruction validation, not a live renewal or a behavioral replay of Nilza's session. No customer data or financial records were changed.

Delivery: pending skills CI and immutable Genius catalog publication. The live plan tracks completion.
