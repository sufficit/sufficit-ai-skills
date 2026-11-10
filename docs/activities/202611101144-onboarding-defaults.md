# Owner-defined telephony onboarding defaults

The owner clarified the defaults after Rafael asked the group to choose protocols,
recording and a queue: new endpoints use SIP and PJSIP simultaneously, recording
is enabled, all intended onboarding endpoints join Principal, and waiting callers
hear only the default hold music, without custom announcements.

## Training and native activation

Updated sufficit-telephony-extensions to 0.4.0 and sufficit-telephony-dialplan to
0.3.0. The generic runbook and onboarding reference now carry these explicit house
choices. Principal is resolved in the customer context, or created conditionally;
a differently named existing queue is not silently substituted, renamed or emptied.
The product editor supplies the other routine defaults: 80 s total wait, capacity
20, ringall when advertised (otherwise linear), 45 s agent attempt and 1 s retry.
Empty musicClass selects default hold music. Custom greeting/periodic/agent audio
and spoken position/estimated wait are disabled; ringing-only/ring-instead-of-music
are false. Endpoints inherit no recording-suppression policy from the queue.

The exact singular extension list route is documented together with ById and the
three creation operations. The runbook explicitly re-reads tech_sip, tech_pjsip
and recording; a success receipt alone cannot demonstrate the chosen flags.
Customer GUIDs identify the target despite cosmetic spelling differences. An
already authorized onboarding includes API setup and DID routing: an existing
announcement alone does not require redundant permission. CAS and independent
reads preserve concurrent/unrelated changes. A 409 never proves an empty list.

Applied the updated instructions to Rafael's existing native routing skill
(ddd0385b-9425-4d07-95ae-308260fe58fe). Four bindings remain, with no reset or
new tool grant. Fresh session composition confirmed the new defaults. The existing
routing/WhatsApp knowledge prefix was preserved. No customer write or test group
message was performed during this training maintenance.

## Necessary API corrections

Creation previously allowed SIP or PJSIP exclusively. EndPointCreation now accepts
SIP+PJSIP, stores both independent flags and validates both on idempotent replay.
Omitted technology/recording default to dual/true; explicit single-protocol requests
from other supported workflows remain compatible. Generated passwords and
insert-only/conflict behavior are preserved; existing endpoints are not rewritten.

The latest real support response also reported setup HTTP 400 invalid user id.
Legacy CheckUp POST/status read only the Microsoft NameIdentifier claim, ignoring
the standard Identity sub issued to the system agent. They now use the standard
GetUserId; the setup action shares a side-effect-free customer authorization gate
with GET /Telephony/CheckUp/Preflight. Starting requires dialplanupdate for that
customer; status requires access to the process's customer. No administrator or
manager role was added to the agent.

API source e3c9d29 and relational regression ff42666 were pushed to main. The
reviewed candidate retained the installed runtime dependencies and excluded
parallel unreviewed endpoint-management files. Both eveo-apps and castrum-apps
were published through standard protected transactions under standing approval.
Independent installed API SHA-256 matched on both hosts:
25c09a189437dfd6ee605100bf6dfda1568f63fa3043a4cb514634e21e9d10e9.
With Rafael's actual identity on each: health 200, setup preflight 200, creation
preview 409 for the customer's still-missing initial setup, unused creation status
204 and nonexistent-DID routing 404 after authorization. The real setup was not
started by these publication checks. The local candidate is removed after this
verified rollout; server rollback copies stay under the normal retention policy.

## Validation and limits

- Before the fix, dual creation, omitted-default choices and sub-based setup status
  failed; the browser-identity control passed.
- 239 focused candidate API tests passed (creation, setup identity/scope, customer
  authorization, internal permissions, checkout, voice, DID isolation and Markdown).
  Three additional legacy relational-schema cases passed, including persisted
  dual flags and recording=true. Replay does not rotate passwords or overwrite
  an existing request with changed protocol/recording choices.
- Full isolated candidate run: 1499 pass, four fail. Those four are known baseline
  architecture/native image/commercial-history failures; no new failure family was
  introduced. The full suite is not reported green. Candidate XML/Swagger checks pass.
- Candidate assembly closure: zero missing custom references, 2829 types load under
  the real runtimeconfig/deps. Validation was isolated from parallel work and an
  unstable latest-package restore using the installed DLL baseline and pinned
  10.0.14 test packages. No dependency upgrade was published.
- 45 Python skill tests pass. All 185 packages pass integrity/provenance checks;
  package validators, versions, index and Markdown checks pass.
- Isolated original-prompt sessions 22a9addf-3f10-4380-aa6c-65f7c49b6c06 and
  4e91b1b2-be61-42ef-9b6f-f08e01d6e6fe completed without writes. Both select dual
  protocols, recording=true, Principal and default music. The second confirms setup
  preflight 200 and treats the existing announcement replacement as already within
  authorized onboarding, without name reconfirmation. It still guessed a plural
  endpoint list route and disclosed the resulting 404. The exact singular route
  was then added to generic/native instructions and directly verified with the
  same agent identity: HTTP 200 and an empty list. No third full model run is
  claimed for this final route clarification.

The customer's actual onboarding remains a normal authorized support operation,
not a side effect of publishing defaults. Saved state, registered phones, applied
dialplan and working audio remain separate verification stages.
