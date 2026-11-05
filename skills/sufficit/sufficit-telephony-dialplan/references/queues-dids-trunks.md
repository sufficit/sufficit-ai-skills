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
