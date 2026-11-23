# Incoming calls fail while outgoing calls work

Treat the public number as the reported symptom, not the diagnosed failure.
Outgoing service does not prove incoming delivery; a disconnected extension can
look like a failed line to its user. Trace the affected customer's actual path.

## Evidence sequence

1. Resolve the customer and exact DID, including country/area code. Read its
   configured destination and distinguish provider, public number and terminal.
2. Use the supported DID testing workflow when equipped and authorized. Discover
   its current operations through the deployed API; do not insert work rows or
   change test origins/settings to force eligibility. Read the run and attempts.
   `Arrived` plus an inbound channel proves that test reached the PBX. A successful
   Originate request only proves acceptance. `no_origin`/zero attempts means the
   test did not run. No arrival after attempts can also be an origin-route failure.
   The anti-ring test may reject an arriving call unanswered: BUSY/Failure on the
   originating leg does not override a correlated recorded arrival. Preserve the
   no-ring filter; never substitute an ordinary customer call for that workflow.
3. Read the active destination chain: time condition/time zone/override, IVR
   options and timeout/default, then each queue's enabled state, members, pauses
   and overflow. Queue `destination` is an exit, not the entrance. Resolve every
   referenced ID within its owning context. List the customer's queues through
   [EndPoints](queues-dids-trunks.md#queue-operations-through-endpoints) and
   select the returned ID. A failed PBX read does not block the API reads.
4. For the intended terminals, check current registration/contact and reachability
   using the actual SIP/PJSIP technology and authorized connector. Read all
   relevant members, not just the first page/printed portion. For TCP, a stored
   contact without a corresponding live transport can be stale. `Unmonitored`
   is not a positive reachability result; an old contact or qualify result does
   not prove a current registration. Check DND, forwarding and queue eligibility
   separately when those reads are available.
5. If authorized and equipped, use bounded diagnostic calls to the affected
   terminals and queue ingress, with a finite timeout and cleanup of only the
   channels created by the test. Do not run unbounded ringing or disturb active
   calls. Record event/call identifiers, times, transport and terminal outcomes.
   Missing capability is a concrete limitation; do not claim a test was run.
6. Correlate an actual failed customer call by origin, DID, time and LinkedId.
   In the deployed consolidated Call/Search contract, each result's `key` is its
   LinkedId (verify the current schema/response). Pass that returned value to
   GET /Telephony/Call/Channels with the same `contextid` and `linkedid=key`.
   A missing `linkedid` query parameter calls for resolving the call identity,
   not abandoning correlation. These authenticated API reads are independent
   of PBX SSH and should be completed while a live-registration read is blocked.
   Never manufacture a LinkedId from a channel name, timestamp or customer GUID.
   Separate customer calls from known internal tests. A time gap before Dial may
   be IVR, announcement or waiting; read that configuration before blaming delay.

Complete available independent checks before asking the customer for information
that only the customer can supply. If the faulty terminal is identifiable, report
it and its queue impact; do not assume that it explains every reported failure.

## Call-state interpretation

- `Dial`/DialBegin, a SIP channel name, CDR duration and `NOANSWER` prove at most
  an attempted leg. They do not prove the device returned ringing. Duration is
  not a ringing timer. Require correlated `Newstate=Ringing`/SIP 180 or equivalent
  evidence for ringing signaling. SIP 183 is early progress/media, not by itself
  evidence of physical ringing.
- Ringing signaling does not prove audible ringing on the device. `ANSWERED`
  can be the PBX/IVR answering before agent dispatch, not a person answering.
  Identify the answering leg and bridge; two-way audio needs its own acceptance.
- One arriving call proves that call's path, origin and time. It does not establish
  continuous availability, every origin's routing or recovery of an earlier fault.
  Empty CDR results do not prove no INVITE arrived: early rejection and query
  filters may hide it. State query coverage and the last verified observation.

## Diagnostic tools and blocked stages

Use the supported connector and authenticated helper. Discover methods/parameters
instead of trying plausible route names. If the helper accepts
`service METHOD /path [json-file-or-dash] [headers-file]`, pass a JSON file as the
body argument; inline JSON may be interpreted as a filename. Verify Content-Type
and supported stdin semantics after HTTP 415. Inspect the actual HTTP response and
stderr: piping through `head` can hide a failing process behind exit status zero.
Save complete responses and select fields/page results; truncated terminal output
cannot establish that later resources are absent or exhaust the list.

An SSH key ignored for overly open permissions is a connector installation
failure, not proof that the PBX denied the customer or that an extension is
missing. Report the failed operation and exact diagnostic. Do not print key/token
contents, try another identity, change permissions or widen grants unless that
maintenance is authorized. Continue supported API reads while the connector is
blocked. Report completed checks, blocked checks and the precise resume condition.

## Carrier and interconnection comparison

For a reproducible complaint, including a case where an internal test succeeds,
coordinate mobile-origin calls with the managers through the agent's established
private WhatsApp channel. Ask them to call the confirmed DID from their own
mobile phones and report the carrier for each test; compare different carriers
when available. Collect origin, timestamp/timezone, audible result and correlated
PBX/endpoint evidence. Do not infer the current carrier from a mobile prefix.
Do not publish the private coordination to the customer or claim a sent request
without a delivery receipt. Preserve pending human responses as pending.

Use the [first-contact and manager-test training](first-contact.md) for the
customer follow-up and the private request wording. If messaging is not equipped,
return the private request and actual capability limit for human execution;
training does not add a sending tool, select arbitrary recipients or create groups.

## Queue dispatch by node

Start with an existing attempt. Identify the customer context, DID, local time
and time zone, call LinkedId, queue ID and node that actually handled the queue.
The phone can register on a different node. A shared catalog lists configuration.
Its members response returns a zero node ID and `dispatchEnabled=false` by
design. Member registration, ringall and absence of pause describe eligibility
only in part. For dynamic members, also check login.

For a Stasis/ARI queue, use the authorized node-scoped call history and visit
events. Match queue, time and call channel to the visit ID. If the CDR is late,
use the controller events available for that node. Read entry, offers, connection
and final status for the same visit. An entry followed by abandonment proves
the caller reached the queue. Claim zero offers only if the offer history is
complete. A correlated `queue_connected` followed by `completed` confirms a
connection. Name the answering extension only when the offer or channel identifies
it. A voice test can independently report a greeting and a human response.
For a scoped read returning 403 or 404, record the node and missing evidence
and use the available authorized sources. A legacy Asterisk queue listing
does not enumerate ARI visits.

After a change, compare the failed and successful visits with their respective
nodes. Report which path recovered and which path still needs verification.
Use an existing correlated visit before asking someone to call again.
