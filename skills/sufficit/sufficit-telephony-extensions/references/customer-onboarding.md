# Customer telephony onboarding

Use this workflow when the requester wants initial PBX setup, for example four
extensions 6001–6004, one waiting queue and the customer's DID pointing to it.
This is one customer-scoped operation with several independently verified effects.
A request to create four extensions alone does not implicitly authorize queue/DID
changes; use the complete onboarding scope only when requested or established by
the customer's approved onboarding policy.

## Recover a prior customer request

If a colleague asks what the customer requested during first-level support, check the case or group history for a verified customer context UUID. In a Fleet group
with an assigned first-level consultant, use `mcp__fleet_workspace__send` with
`operation=support_ask`, the active `missionId`, the manager's `message_id`,
a focused `question` with the case reference and dates, and either the verified
`customerContextId` or a specific `customerSearch` (name, phone or email).
The specialist uses `conversation_search` on the active private mission with
inclusive dates in São Paulo time. Cite confirmed conversations and dated public
messages. Return probable matches as references to verify before using their
contents to advise a customer. An empty or partial result describes only the
configured inbox and search coverage.
The consultant can work privately even when absent from the WhatsApp group.
Fleet resumes the host agent when the consultant finishes. Keep the receipt for
status checks. During the return turn, ask for a specific clarification privately
with the same tool, `operation=support_followup`, the current `missionId` and
`question`. Fleet carries forward the customer, specialist and previous answer.
For example, if the answer mentions a greeting, ask which conversation documents
it. If the specialist reports that the source is inaccessible, report that limit.
Give the requester the finding and its source when available.
Missing evidence leaves the request unknown. A consultation only retrieves
information; changes to the customer's PBX require their own authorized scope.

## Resolve the intended state

- Keep the supplied customer context GUID. Resolve the display name with
  GET `/Contact/Title?contactid=<GUID>`; Customer 204 is not proof of absence.
  An explicit GUID identifies the customer: report the returned title when the
  supplied name has a typo, without blocking for cosmetic reconfirmation.
- List extensions, DIDs and catalog queues first. On an
  empty customer, the approved four-extension onboarding pattern is 6001–6004;
  when numbers were explicitly specified, preserve them. Names are optional in
  the current creation API; do not block solely because each extension lacks a
  person's name. Do not create Identity users or reset account passwords.
- If the authorized scope includes routing an inbound number, select only a DID actually owned by this context. A single unambiguous inbound
  DID can be selected from the API; several candidates require the requester to
  select one. Do not ask again for a GUID or DID already provided or discoverable.
- Apply the approved new-extension standard: both SIP and PJSIP enabled,
  recording=true. Do not ask technology or whether to record again.
- All intended onboarding extensions go into the queue named **Principal** in
  this customer. Reuse the exact same-customer Principal if present; otherwise
  create it. A differently named existing queue (for example atendimento) is not
  the default target. Do not rename, delete or empty other queues.
- No custom audio: no greeting, periodic or agent announcement, spoken queue
  position/estimated wait or wait-menu recording. Play only the system's default
  hold music. Do not require audio uploads or choose an arbitrary media catalog item.
- For unspecified distribution/time/capacity options, use the current product's
  new-queue defaults, preserving the explicit owner overrides above. Do not turn
  routine onboarding into a questionnaire about every optional field. A genuinely
  ambiguous target or a genuinely conflicting instruction still requires
  clarification; names, both protocols, recording and Principal/default music do not.
  An existing DID announcement/different destination alone is not a new approval
  requirement when the authorized onboarding explicitly points the DID to Principal:
  report before/after, preserve unrelated properties and use compare-and-set.

## Prepare customer telephony

Read GET `/Telephony/EndPoint/Preparation?contextId=<GUID>` for the
validated customer. Its response includes `contextId` and `telephonyPrepared`.
A registered customer can be prepared with zero services. This operation uses
the same customer-scoped `dialplanupdate` authorization as extension creation.

When `telephonyPrepared=false`, POST the same URL with no body, then re-read
GET and confirm `telephonyPrepared=true` for the same context. This ensures the
customer's FreePBX mapping, context and includes. It leaves contracts and billing
outside the workflow. On timeout or 503, reconcile with GET before retrying.
If the deployed API lacks this route, report the actual response and identify
preparation as pending for that API version. A commercial service or a full
legacy checkup is outside the scope of this operation.

Re-read `GET /Telephony/EndPoint/Creation/Preview?contextId=<GUID>&number=<number>`
to obtain the server-generated title before each extension creation. A 409 for
missing configuration indicates pending preparation. Read the extension list
before creating anything, even when preparation was missing.

## Ensure the customer default password

Do this **before creating any extension**, once per customer:
POST `/Telephony/EndPoint/DefaultPassword/Ensure?contextId=<GUID>` answers
`{ contextId, created }`. `created=true` means a random compatible password was
just stored as the customer's default; `created=false` means one already existed
and was kept. The value is never returned and you do not need it: extensions
created afterwards without a `password` receive it automatically, so all the
customer's phones can be installed with the same secret.

This is a facilitator, not an imposition. If the requester asks for individual
passwords, a specific password on one extension, or no shared password, do that
instead: send the explicit `password` on creation, or skip this step when they
decline a shared one. Never rewrite existing extensions to match the default,
and never replace an existing default on your own initiative. Track this item in
the onboarding checklist as ensured/kept/declined, without the value.

A 403 here is the same customer authorization as creation (manager or
`dialplanupdate` for that customer); a 404 means the deployed API predates this
operation: report it and continue with server-generated passwords.

## Create extensions

Follow [provisioning.md](provisioning.md) once per intended number. Reuse correct
existing endpoints without changing their passwords, even when they differ from
the customer default. Keep stable request IDs,
confirm reads after each effect, and stop on a concrete failure. A partial result
is resumable, not a reason to delete/recreate everything. Never post SIP passwords
in the group, shared summary or audit.

After the FreePBX-backed creation batch, apply `fwconsole reload` once and verify
each SIP peer and PJSIP endpoint as required by the
[application step](provisioning.md#apply-the-freepbx-batch-before-handover).
Do not declare onboarding ready while legacy SIP peers are missing.

## Create the waiting queue and members

Use the operator's authenticated EndPoints connection and confirm the
[queue operations](../../sufficit-telephony-dialplan/references/queues-dids-trunks.md#queue-operations-through-endpoints)
in OpenAPI v2. The shared catalog supports the following operations:

- GET `/api/queue/contexts/<context:N>/queues`.
- PUT `/api/queue/contexts/<context:N>/queues/<queueId:N>` creates a new UUIDv7
  resource with `If-None-Match: *`; updates use the returned strong `If-Match`.
  Body: title, maxWaitSeconds, maxWaiting, enabled, destination and options from
  the approved policy. Use title=`"Principal"`. New-queue defaults from
  QueueChange/QueueOptions.ForNewQueue are maxWaitSeconds=45, maxWaiting=20,
  enabled=true, destination="", strategy="linear", agentTimeoutSeconds=45,
  retrySeconds=1 (unless an explicit customer policy says otherwise). Keep the
  other product defaults. An empty destination is allowed; never invent a fallback.
  Override media options: greeting="", periodicAnnouncement="", agentAnnouncement="",
  musicClass="", announcementIntervalSeconds=0, announcePosition=false,
  announceEstimatedWait=false, ringingOnly=false and ringInsteadOfMusic=false.
  Empty musicClass uses system-default music on hold; ringingOnly=true or
  ringInsteadOfMusic=true would contradict the owner's requested hold music.
  Keep queue recording inherited from the recording-enabled endpoints; do not
  set a policy that suppresses recording.
- GET `/api/queue/contexts/<context:N>/queues/<queueId:N>/members` returns current
  members and authorized destinations. Use the returned full extension identity.
- PUT the same path plus `/<memberId:N>` creates each membership with a stable
  UUIDv7 and `If-None-Match: *`. Existing members use their strong revision instead.
  Bind only same-customer confirmed extensions; enabled=true/paused=false means
  eligible, not proof that a phone is registered. Preserve other members.

Catalog writes use the customer route without a node ID. EndPoints handles
the private ARI credential and records the authenticated operator.
After 409/412 or transport uncertainty, re-read the catalog by the SAME IDs before
retrying. Reconcile exact state; do not mint another queue or member ID.

## Point the DID to the queue

When the authorized scope includes inbound routing and the customer has an owned DID, continue here. If no DID is available, record inbound routing as pending and complete the authorized extensions and queue.

Re-read the owned DID and preserve its billing, answer and other properties.
The canonical queue ingress is `sufficit-app-queue,<queueId:N>,1`, without contextId.
The queue's own destination field is its exit/fallback, not its ingress.
Use the authorized DID routing operation selected by the product contract;
`POST /Telephony/DID/QueueDestination?id=<didId>` is the compare-and-set operation.
First GET that path with `id=<didId>&contextId=<customerId>` for its routing snapshot.
Body: contextId, queueId, ringingOnly and all expected* fields copied from that
snapshot, preserving null/false. DID/ById and search omit legacy CAS columns;
do not guess their defaults or repeatedly retry a 409 from an incomplete snapshot.
Do not alter billing or use SQL/CLI as fallback. Confirm authorization for the
actual operation before writing; a read grant does not prove write access.
After a conflict re-read instead of overwriting concurrent routing. After a
timeout read the DID instead of blindly repeating POST.

## Clear a DID destination

For an authorized disconnection, confirm the DID still belongs to the requested
customer. Read GET /Telephony/DID/Destination with its id and that contextId.
Send the returned snapshot unchanged to DELETE /Telephony/DID/Destination.
On 204, read the snapshot again and verify the destination fields are empty.
A 404 for the original context can mean ownership has changed. Stop and report
the discrepancy. On 409, review the new route before any retry. A hangup route
already disconnects incoming calls. Preserve that state when it meets the request.

## Consolidate and report

Track the default password step, each extension, queue, membership, DID destination and runtime verification
as existing/created/confirmed/pending/blocked. Re-read independently. A saved
catalog or API HTTP 200 does not prove loaded dialplan, registered phones or audio.
Runtime checks must be non-destructive; disruptive server operations still follow
the owner's specific approval rule. Update the group's normal working record with
progress and decisions, keeping confidential identifiers/credentials out of public
summaries. State exactly what is working and what remains; do not send a generic
"cannot create" when only one stage is blocked. Training/permission maintenance
does not retroactively execute the customer's original request.

Fleet conversations retain old mission identifiers in history. Every workspace
call must use the current `# Missão` from this turn's host instructions. If a call
reports that the mission is not running for this agent, check that current ID
before claiming missing write permission; do not retry the same stale ID or ask
for broader access. Read the current document, preserve its existing content and
write updates through the group's workspace tool. A failed read is not proof
that the file is empty or that a write was refused.

## Customer default outbound caller ID

Confirm the customer context and read `GET /Telephony/Outbound/CallerId?contextId={guid}`.
For an owned Brazilian DID, use `PUT /Telephony/Outbound/CallerId` with the same
`contextId` and `number` (55, area code and subscriber number, digits only).
An explicit null restores automatic selection. Read the preference back.
This changes presentation while preserving the selected route and explicit extension
overrides. A 403 on outbound service assignments does not establish whether this
operation is available. Report the actual operation and result. Only a call to an
agreed test receiver can confirm which number the carrier presented.
