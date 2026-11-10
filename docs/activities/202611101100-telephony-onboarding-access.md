# Telephony onboarding training and API authorization

The owner clarified the operational scope: customer onboarding includes extensions
6001–6004, a waiting queue, its members, and the owned DID pointing to that queue.
The original assistant only searched incomplete OpenAPI documents and concluded
that extension creation did not exist.

## Delivered training and connection

Updated sufficit-telephony-extensions to 0.3.0 and sufficit-telephony-dialplan to
0.2.0. The reusable onboarding reference covers company/title resolution, initial
telephony preparation, insert-only extension creation, stable request IDs/status
reconciliation, conditional queue/member creation and DID compare-and-set routing.
It handles an empty customer, optional extension descriptions, missing policy
choices, partial execution, exact customer scope, secret handling and honest
runtime verification. A missing/oversized OpenAPI is discovery failure, not proof
that an API does not exist. The authenticated Fleet REST helper is supported and
must be invoked serially because refresh rotation has a single-writer lock.

The fixed-actor Queue catalog bridge now supports queue and member creation with
UUIDv7 plus If-None-Match, and updates with exact strong If-Match. It retains a
fixed service/actor, keeps the shared credential on the portal, rejects cross-
customer member creation and does not expose DELETE or shell execution. Installed
bridge SHA-256: 39bac92fedfed62070e516029f5fe66ac0b1ac1655d1e24b5814a8f9ff1fd8f8.
Live GET for the target customer's catalog returned HTTP 200 and no queues.

Native Fleet installation found the four-skill limit. No limit was raised and no
existing binding was dropped. Onboarding was consolidated into the current routing
skill ddd0385b-9425-4d07-95ae-308260fe58fe; all four existing bindings remain, and
new-session composition contains the complete training. The initially saved
standalone draft was not bound or used. Existing active sessions were not restarted.

## Authorization and production

Fresh Identity userinfo confirmed the agent already has dialplanupdate,
telephonyadmin and customer read grants for all authorized customers. No manager,
administrator, OAuth scope or duplicate entitlement was added. API replicas differed:
eveo-apps had the new extension domain policy while castrum-apps still rejected the
same identity. After the parallel creation-policy publication, the supported
preview returns 409 for missing initial customer telephony setup, not 403.

EndPoints commit 06e80a2 updates DID QueueDestination to accept both telephonyadmin
and dialplanupdate in the request context, preserving managers' existing access.
Before writing it verifies the target new-engine queue belongs to that customer.
DID compare-and-set behavior and unrelated billing/answer settings are preserved.
No direct database writes or FreePBX bypass were used.

Published the reviewed candidate through the standard deploy.py transaction on
eveo-apps. Installed API DLL SHA-256 matches the tested candidate:
40631701863f6258717b1a6f19952d5be822fc3805bd9c214cbd587d470dedcc.
Independent reads confirmed health 200, creation preview 409 (missing setup),
creation status for an unused request 204, and authenticated DID routing 404 for
an intentionally nonexistent DID (authorization passed; no write occurred).
An initial staging upload was stopped by the operator before any live swap to
include the existing TLS asset, then republished successfully with configuration
and dependencies preserved. Only the intended deployment/transfer PIDs were stopped.

## Validation

- 45 Python tests pass, including five bridge contract tests.
- All 185 packages pass digest/provenance validation; version/index/Markdown gates
  and both updated package validators pass.
- Four API authorization/foreign-queue regressions fail against the installed
  baseline and pass with the correction. The required focused candidate suites
  (creation, customer authorization, internal permissions, checkout, voice and
  Markdown) pass: 232 tests. Eight Markdown tests also pass after final documentation.
- Assembly closure: no missing custom reference; 2,829 API types load under the
  candidate's actual deps/runtimeconfig. Existing business DLLs were retained.
- Full candidate suite: 1,489 pass, seven fail. The same seven fail against the
  unchanged installed baseline; its four new regression failures disappear in
  the candidate. No new full-suite failure was introduced. The remaining baseline
  failures concern image/native support, source architecture, Swagger/XML and
  commercial history expectations. They were not silently changed or called green.
- Isolated Rafael retest aac1ce2e-b969-4ca7-9c9d-646512df3038 used the exact original
  request. It resolved the customer's actual title, read all four creation previews,
  identified missing initial setup, read the empty Queue catalog and described the
  complete onboarding sequence, stable IDs, conditional writes and verification.
  It did not claim missing creation support, request an API route, mutate customer
  data or send WhatsApp messages. The first parallel REST probes hit transport/lock
  errors; serialized reads succeeded and the final guidance addresses that behavior.

## Secondary completion

On 2026-11-10 the owner approved castrum-apps publication and standing authorization
("sim, sempre"). EndPoints config.json and its deployment guide now allow routine
authorized publication on eveo-apps and castrum-apps without another host confirmation;
apoint-apps stays manual and subject to availability.

The standard protected transaction published the identical reviewed candidate on
castrum-apps. Only the API DLL differed before promotion; runtime dependencies
matched. Independent installed hash equals the primary/candidate hash above.
With Rafael's actual identity: health 200, creation preview 409 (initial setup
missing), unused creation status 204, and nonexistent-DID routing 404 after
authorization, replacing its prior 403. The 27 deployment tests passed. No customer
onboarding or WhatsApp test message was executed. The local candidate was removed
after both hosts were confirmed; standard server rollback copies were preserved.

All implementation, training activation, validation, commits and publication steps
are complete. The permanent [customer onboarding contract](../../skills/sufficit/sufficit-telephony-extensions/references/customer-onboarding.md)
retains the reusable workflow and boundaries.
