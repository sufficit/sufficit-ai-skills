# Queues, inbound DIDs and outbound trunks

## Queues

- Queue **members are configured extensions**: to add an attendant, the
  extension must already exist (see
  [extension provisioning](../../sufficit-telephony-extensions/references/provisioning.md));
  adding membership is a queue update, not an extension creation.
- `configuredWaitSeconds` is the queue's **configured wait limit in seconds**,
  not a live or average wait time; report it as configured.
- Membership changes are live: after changing members, re-read the queue and
  confirm the final member list before reporting.

## Internal queue numbers and migrated FreePBX callers

A native queue is addressed by GUID. Its short/internal dial number is a separate
compatibility route, not a SIP endpoint, DID, member extension or queue policy
field. A catalog without an `extension` field does not prove the number is absent.
An EndPoint lookup failure for that number does not prove the destination is invalid.
Searching EndPoints OpenAPI alone cannot discover installed compatibility dialplan.

For an intercom/extension that dials a queue number:

1. Preserve the supplied digits exactly. Resolve the caller's customer and actual
   authenticated SIP/PJSIP context. Do not drop/add digits or guess a `-custom`
   suffix. A registered device only proves registration, not working calls.
   Check both the supplied number and supported short-code normalization. In the
   installed FreePBX integration, `_6XXX` can resolve the authenticated customer's
   prefix and Goto `<prefix><short-code>` in that customer's context. Recognition
   of the short-code pattern is not proof the normalized destination is reachable.
   Do not require full-number dialing or reconfigure the device merely because
   the numeric map lists full prefixed numbers. Never invent an intermediate
   five-digit form by arbitrarily stripping leading zeros.
2. Use the authorized PBX **read-only diagnostic connector** to inspect:
   `sip show peer <caller>` or `pjsip show endpoint <caller-id>`, then
   `dialplan show <full-number>@<actual-caller-context>`.
   Validate identifiers as alphanumeric/dash/underscore before substituting them.
   If the account has both SIP and PJSIP records, inspect both registrations and
   use the context of the device's actual active technology. An unavailable PJSIP
   endpoint with no contacts is not the context of a device registered on chan_sip.
   If both are active, use call execution evidence or state the ambiguity; never
   choose a context from a catalog record or old memory alone.
3. Inspect the numeric projection with
   `dialplan show <full-number>@sufficit-freepbx-queue-numbers`.
   The installed source is `sufficit-freepbx/generated/queue-number-routes.conf`;
   the loader is `sufficit-freepbx/app-queue-number.conf`. Older installed layouts
   may differ: discover actual includes rather than assuming checkout equals runtime.
   Report the exact target `sufficit-app-queue,<queueId:N>,1` if present.
4. Read the customer's native queue catalog and match that GUID to its title,
   enabled state and members. On the configured catalog bridge, GET the customer's
   **queue list**, then select `items[id]`; a per-queue GET may return405 even when
   listing and conditional PUT work. `queue.destination` is the exit/fallback,
   not its entry number. Never infer queue identity from the title or fallback.
5. Separate **map exists** from **caller can reach it**. A route visible from
   `from-internal` may be absent from a tenant-specific context. Inspect the caller's
   real include/Goto path. If the exact map exists but that path falls through to
   bad-number, diagnose route visibility; do not propose declaring the number again.
6. No CDR match does not prove no SIP INVITE arrived: rejection before CDR or
   incomplete filters may hide it. Use existing bounded diagnostics/logs if
   available; do not enable global SIP debug, create calls or reload the PBX merely
   to read this mapping.

Queue/member policy changes use the supported catalog API. Numeric projection or
include repairs belong to the maintained FreePBX integration/publication path;
never write business tables, generated dialplan or the legacy database ad hoc.
Database read-only rules prohibit direct business SQL writes; they do not prohibit
preparing a source-controlled dialplan fix or a reviewed publication. Treat these
as separate boundaries: business writes through APIs, maintained PBX source/config
publication, and operational approval for disruptive commands. For google-voip,
request the owner's explicit approval for the concrete command/impact before a
shared production reload. Do not claim a database rule forbids all file edits or
reloads, or that approval permits direct SQL or ad-hoc generated-file changes. A real missing
management operation should become a concrete engineering issue with caller
context, exact number, expected queue GUID and runtime evidence, not a request
for the user to discover the API. Do not claim the intercom is repaired from
configuration reads alone.

## Inbound: DID

- A DID is an inbound number resource; routing starts at the DID pointing to a
  flow. Discover DID operations with `did` / `inbound number` searches.
- Never use a DID search to answer a voicemail question: voicemail is a
  different resource. The company's number list does not prove personal
  ownership of any voicemail box.

## Outbound: individual trunk (tronco individual)

- One external call at a time (single channel); no minute limit.
- 30 external calls per day, counted as 90 every 72 hours: a busy day may exceed
  30 while the 3-day window stays under 90. Blocked calls (no free channel) do
  not count; unanswered dialed calls do count.
- Caller identification is always active: the destination sees the company
  number. Destinations: any valid number.
- A company can have only **one** active individual trunk and cannot combine it
  with the flexible trunks (Flex/Flex+): choosing is a business decision, not a
  routing default.
- When another outbound service is also contracted, overflow calls may leave
  through it.

## Recording along the path

Calls answered by extensions are recorded per the extension's recording
preference (see
[extension preferences](../../sufficit-telephony-extensions/references/preferences.md));
queue membership does not change that. Ring-only, unanswered calls have no
recording.
