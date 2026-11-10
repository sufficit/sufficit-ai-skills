# Customer telephony onboarding

Use this workflow when the requester wants initial PBX setup, for example four
extensions 6001–6004, one waiting queue and the customer's DID pointing to it.
This is one customer-scoped operation with several independently verified effects.
A request to create four extensions alone does not implicitly authorize queue/DID
changes; use the complete onboarding scope only when requested or established by
the customer's approved onboarding policy.

## Resolve the intended state

- Keep the supplied customer context GUID. Resolve the display name with
  GET `/Contact/Title?contactid=<GUID>`; Customer 204 is not proof of absence.
- List extensions, contracted services, DIDs and catalog queues first. On an
  empty customer, the approved four-extension onboarding pattern is 6001–6004;
  when numbers were explicitly specified, preserve them. Names are optional in
  the current creation API; do not block solely because each extension lacks a
  person's name. Do not create Identity users or reset account passwords.
- Select only the DID actually owned by this context. A single unambiguous inbound
  DID can be selected from the API; several candidates require the requester to
  select one. Do not ask again for a GUID or DID already provided or discoverable.
- Obtain required technology, recording and queue distribution settings from an
  approved customer/house preset or the request. Do not silently invent defaults
  for SIP/PJSIP, recording, commercial terms, queue media or overflow destinations.
  Ask one compact question for genuinely missing decisions, after completing reads.

## Prepare customer telephony

GET Creation/Preview for the first desired extension resolves the prefix.
If it returns 409 for missing initial configuration, use the supported customer
setup/checkup, not direct database/FreePBX commands. Current legacy contract:
POST `/Telephony/CheckUp?ClientID=<GUID>` starts a mutating customer setup process;
202 returns its GUID. GET `/Telephony/CheckUp?CheckUpId=<GUID>` follows the process.
CheckUpController.cs is the source. This is not a read-only diagnostic: it may
provision contracted services and update runtime configuration. Execute only
inside an authorized customer onboarding/setup request and the applicable
operational policy; a training test never starts it. Do not substitute global
checkup methods. On uncertainty, query the original process before another POST.
After successful setup, re-read preview; do not construct the prefix locally.

## Create extensions

Follow [provisioning.md](provisioning.md) once per intended number. Reuse correct
existing endpoints without changing their passwords. Keep stable request IDs,
confirm reads after each effect, and stop on a concrete failure. A partial result
is resumable, not a reason to delete/recreate everything. Never post SIP passwords
in the group, shared summary or audit.

## Create the waiting queue and members

Use the configured Queue catalog API, not guessed `/Telephony/Queue` routes on
EndPoints. The supported contract from QueueClient.cs and ARI ManagementApi.cs is:

- GET `/api/queue/contexts/<context:N>/queues`.
- PUT `/api/queue/contexts/<context:N>/queues/<queueId:N>` creates a new UUIDv7
  resource with `If-None-Match: *`; updates use the returned strong `If-Match`.
  Body: title, maxWaitSeconds, maxWaiting, enabled, destination and options from
  the approved policy. An empty destination is allowed; never invent a fallback.
- GET `/api/queue/contexts/<context:N>/queues/<queueId:N>/members` returns current
  members and authorized destinations. Use the returned full extension identity.
- PUT the same path plus `/<memberId:N>` creates each membership with a stable
  UUIDv7 and `If-None-Match: *`. Existing members use their strong revision instead.
  Bind only same-customer confirmed extensions; enabled=true/paused=false means
  eligible, not proof that a phone is registered. Preserve other members.

Keys remain at the trusted BFF/bridge; never copy its Bearer into agent prompts.
The provisioned Fleet bridge `/data/support/queue/queue-catalog REQUEST.json`
accepts GET requests with contextId and optional queueId/members; PUT uses contextId,
queueId, optional memberId and body. For creation add `create:true` and omit revision;
for updates omit create and include the exact strong revision. Only use this form
when that connection version is installed. A historical existing-member-only
bridge is an access limitation; it does not prove missing queue creation support.
No nodeId is required for catalog writes. Never choose the first online node.
After 409/412 or transport uncertainty, re-read the catalog by the SAME IDs before
retrying. Reconcile exact state; do not mint another queue or member ID.

## Point the DID to the queue

Re-read the owned DID and preserve its billing, answer and other properties.
The canonical queue ingress is `sufficit-app-queue,<queueId:N>,1`, without contextId.
The queue's own destination field is its exit/fallback, not its ingress.
Use the authorized DID routing operation selected by the product contract;
`POST /Telephony/DID/QueueDestination?id=<didId>` is the compare-and-set operation.
Body: contextId, queueId, ringingOnly, expectedAsterisk, expectedDestinationId,
expectedTypeName, expectedAnswer, expectedBilled, copied from the fresh read.
Do not alter billing or use SQL/CLI as fallback. Confirm authorization for the
actual operation before writing; a read grant does not prove write access.
After a conflict re-read instead of overwriting concurrent routing. After a
timeout read the DID instead of blindly repeating POST.

## Consolidate and report

Track each extension, queue, membership, DID destination and runtime verification
as existing/created/confirmed/pending/blocked. Re-read independently. A saved
catalog or API HTTP 200 does not prove loaded dialplan, registered phones or audio.
Runtime checks must be non-destructive; disruptive server operations still follow
the owner's specific approval rule. Update the group's normal working record with
progress and decisions, keeping confidential identifiers/credentials out of public
summaries. State exactly what is working and what remains; do not send a generic
"cannot create" when only one stage is blocked. Training/permission maintenance
does not retroactively execute the customer's original request.
