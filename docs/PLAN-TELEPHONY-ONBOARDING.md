# Telephony onboarding training and access

Objective: teach reusable customer onboarding (extensions 6001–6004, queue and DID routing) and repair Rafael's API access without performing customer writes during training.

1. COMPLETE — confirm endpoint/queue/DID contracts, injected skill path and exact permission boundary behind the observed 403.
2. COMPLETE — update extension/dialplan training with onboarding workflow, recovery semantics and current API contracts; provision least-scope domain access using supported Identity/Fleet APIs.
3. COMPLETE — validate skill/catalog integrity and live read-only access; run an isolated behavioral test without customer mutations.
4. IN PROGRESS — commit/push reviewed changes to main, activate training through the supported Fleet/Genius path, record evidence and limitations.

Acceptance: Rafael can identify the current creation/queue/routing workflows, preserve customer scope and idempotency, distinguish missing data from discovery/authorization failures, and pass live preflight reads. No SQL writes, broad scope bypass, secret disclosure, retroactive customer onboarding or test WhatsApp messages.

Findings: Identity already grants global dialplanupdate/telephonyadmin/client privileges to Rafael; no duplicate or platform manager grant is needed. The creation permission fix is rolling out in a parallel API release: the same preflight now reaches HTTP 409 (customer initial telephony setup missing), instead of 403. The existing Queue bridge permits only existing-member edits and must expose controlled create semantics. DID QueueDestination currently requires manager even for an authorized dial-plan editor.

Implementation: extension/dialplan references updated; fixed-actor Queue bridge supports conditional queue/member creation and is installed. Existing four skill bindings preserved; onboarding consolidated into the current routing skill (native Fleet limit is four). API DID gate now accepts customer domain entitlements and refuses foreign queue targets. No Identity claims were added: existing grants were confirmed in a freshly refreshed userinfo result. Candidate authorization/security suites: 232 pass. Full candidate run: 1467 pass, 29 fail; investigating startup/content-root and commercial source-contract failures before promotion.

Validation checkpoint: published baseline dependencies preserved; 232 focused API tests pass and assembly closure loads all 2,829 types with no missing references. Full-suite failures are candidate test-host setup plus an unrelated commercial history expectation; isolated diagnosis underway. Skills: 45 Python tests pass, all 185 packages validate. Live Queue catalog GET 200. New-session composition includes onboarding and preserves four bindings. Read-only behavioral retest started (aac1ce2e-b969-4ca7-9c9d-646512df3038).

Primary publication and production authorization proof complete (API 06e80a2; tested/installed hash 40631701863f6258717b1a6f19952d5be822fc3805bd9c214cbd587d470dedcc). All training checks pass; original-prompt read-only retest completed successfully. Secondary castrum-apps publication remains pending explicit owner approval required by EndPoints config.json. Keep the candidate and this plan for that step; do not mark the whole rollout complete.
