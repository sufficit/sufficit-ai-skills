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
  An explicit GUID identifies the customer: report the returned title when the
  supplied name has a typo, without blocking for cosmetic reconfirmation.
- List extensions, contracted services, DIDs and catalog queues first. On an
  empty customer, the approved four-extension onboarding pattern is 6001–6004;
  when numbers were explicitly specified, preserve them. Names are optional in
  the current creation API; do not block solely because each extension lacks a
  person's name. Do not create Identity users or reset account passwords.
- Select only the DID actually owned by this context. A single unambiguous inbound
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

GET `/Telephony/CheckUp/Preflight?contextId=<GUID>` checks the actor and domain
authorization without starting setup. Current setup accepts the normal Identity
`sub` as well as browser NameIdentifier. A legacy 400 `invalid user id` is an API
identity-extraction defect to report, not evidence that another manager grant or
a user-provided credential is needed.

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
If checkup reports no current telephony service while a native contract is active,
do not invent another zero-price service. The legacy checkup reads legacy services;
an empty legacy list does not invalidate the native contract. Discover operations
in the live versioned OpenAPI (currently `/swagger/v2/swagger.json`, not only v1).
If the business helper rejects the full schema at 1 MiB, use the provisioned
`python3 /data/support/api-schema QueueDestination` for paths and referenced DTOs;
it reads public metadata only, without exposing credentials.
GET `/Sales/LegacyService/Session` supplies epoch/snapshotId. Send them as headers
`X-Sufficit-Sales-Epoch` and `X-Sufficit-Sales-Snapshot` in subsequent calls.
GET `/Sales/LegacyService/Initialization?contextid=<GUID>` distinguishes
hasCurrentService, currentNativeContractId and telephonyPrepared. A 409 authority
message means refresh these headers, not unavailable permission or missing route.
For an active native contract and telephonyPrepared=false, discover and use POST
`/Sales/LegacyService/Preparation` with `{contextId,contractId}` using that exact
contract. This prepares the existing PBX bridge without creating or changing any
commercial service, price, period or charge. The authorized onboarding includes
this operational preparation. Re-read Initialization and preview afterwards.
An unknown POST outcome requires a state read; do not recreate a service as fallback.
If the route is absent/refused, report its actual HTTP result and preserve this stage.
Only the absence of any current contract leads to the separately reviewed initial
service-creation flow; never infer authorization to create paid/free service coverage
from a request to create extensions alone.

After successful setup, re-read preview; do not construct the prefix locally.
The authorized onboarding includes this API setup step; do not ask for a second
authorization solely because CheckUp mutates the customer. A read-only test is
restricted independently and never starts it. A 409 does not prove the extension
list is empty: read it before creating anything. Do not say everything is ready
when prerequisite reads or actual setup are still pending.

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
First GET that path with `id=<didId>&contextId=<customerId>` for its routing snapshot.
Body: contextId, queueId, ringingOnly and all expected* fields copied from that
snapshot, preserving null/false. DID/ById and search omit legacy CAS columns;
do not guess their defaults or repeatedly retry a 409 from an incomplete snapshot.
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

Fleet conversations retain old mission identifiers in history. Every workspace
call must use the current `# Missão` from this turn's host instructions. If a call
reports that the mission is not running for this agent, check that current ID
before claiming missing write permission; do not retry the same stale ID or ask
for broader access. Read the current document, preserve its existing content and
write updates through the group's workspace tool. A failed read is not proof
that the file is empty or that a write was refused.
