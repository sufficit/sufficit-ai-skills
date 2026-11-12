# Extension provisioning runbook

Create an extension (ramal) for a company and hand it over safely. Flow-first:
discover each call in the live OpenAPI before running it, then record what the
deployed API actually offered (field names, required arguments, response shape)
in this file as part of the change that first validated it.

## Pre-flight

1. Identify the requester's authority and target company. A person's name/e-mail
   is needed for credential handover when applicable, not as a prerequisite for
   creating generic onboarding extensions.
2. Resolve the company through the API and verify it matches the supplied GUID
   or unambiguous name. Ask only if the target is ambiguous or contradictory;
   an exact customer GUID does not need another permission question.
3. When the scenario arrives as a **PBX central address** (host:port, for
   example `35.198.6.30:26499`) instead of a company: that address is not an
   identifier. List the companies visible to the authenticated user and find
   the one whose central matches the given address or whose existing extensions
   match the numbering pattern given (for example 6011/6012). If more than one
   candidate remains, stop and ask the authorizing user which company owns the
   central; never guess the mapping.
4. List GET `/Telephony/EndPoint?ContextId=<GUID>&Limit=100` (singular EndPoint)
   and confirm the intended number is free. A list at its limit may be incomplete;
   narrow or paginate with the supported search contract. Do not guess plural
   `/Telephony/EndPoints` or stop on that guessed path's 404. **If the number already exists disabled or inactive, do not create a
   duplicate and do not silently enable it**: re-read and report its state
   (owner, last data, preferences) and let the authorizing user decide between
   re-enabling it and removing and recreating it.
5. Inspect the existing naming/technology choices when available. For an empty
   customer, use the domain creation preview to obtain the canonical title;
   never invent a prefix or require two existing extensions. Credentials are
   assigned by the server: the customer's default password when one is set,
   otherwise a generated one. Do not infer a password from other extensions.
6. Map what the extension will serve: queue membership, attendance flows and
   voicemail notification reference extensions; creating the extension alone
   wires none of them. Routing changes follow
   [sufficit-telephony-dialplan](../../sufficit-telephony-dialplan/SKILL.md);
   a helpdesk agent (Hermes/Chatwoot user, API token, link to the extension)
   follows [sufficit-hermes-agents](../../sufficit-hermes-agents/SKILL.md).

## Creation — current EndPoints contract

Use the authenticated EndPoints helper or the equivalent discovered domain tool.
Invoke the provisioned REST helper serially: its rotating refresh credential has
a single-writer lock. Concurrent helper calls can fail on that lock; this is not
proof of an API permission failure. Do not inspect credential files or repeatedly
kill a token refresh to shorten a query.
The authoritative sources are EndPointController.Creation.cs and EndPointCreation.cs
in sufficit-endpoints; the product client is EndPointCreationClient.cs in sufficit-blazor.

1. GET `/Telephony/EndPoint/Creation/Preview?contextId=<GUID>&number=6001`:
   returns contextId, number and canonical title. Numbers are exactly four digits,
   6000–6999 excluding 6500–6599 (reserved for queues). A 409 saying initial
   telephony setup is missing requires the customer-scoped setup/checkup flow;
   it is not a duplicate-number or authorization failure. Read the onboarding reference.
2. POST `/Telephony/EndPoint/Create` with JSON:
   `requestId` (new stable GUID per intended extension), `contextId`, `number`,
   `description` (may be empty), `technology` (standard: `"SIP+PJSIP"`), `recording` (standard: `true`),
   and `expectedTitle` exactly from preview. Retain requestId and the request
   before sending. Both protocols must be enabled and recording must be on for
   normal new extensions. Do not ask these choices again. The current API also
   preserves explicit single-protocol requests from other supported workflows;
   do not use a single protocol as the onboarding default. Omitted creation
   technology/recording now default to dual/true. Omit `password`: the API then
   uses the customer's default password when one is set and generates one
   otherwise. Send `password` only when the requester asked for a specific secret
   on this extension (exactly 10 characters: letters, digits or `! $ & *`).
3. GET `/Telephony/EndPoint/Creation/Status?contextId=<GUID>&requestId=<GUID>`
   reconciles a timeout or uncertain POST. Also re-read the customer's extension
   list. Never change requestId/number just because a request failed. Existing
   disabled endpoints, 409 conflicts and 503 storage failures require distinct
   handling; none authorizes an upsert or overwriting existing credentials.
4. Re-read GET `/Telephony/EndPoint/ById?id=<returnedId>` (or the scoped list)
   and confirm `tech_sip=true`, `tech_pjsip=true`, `recording=true` for the normal
   onboarding request. Do not infer both protocols from a generic success response.
   Creation is insert-only and requestId identifies the created row. Read the
   response id/contextId/number/title/alreadyCreated; the API does not return the
   password. `runtimeApplicationConfirmed=null` means application is unconfirmed,
   not failure and not proof of registration or working audio.

Authorization: current creation accepts an internal manager or dialplanupdate
for that customer (global domain grants apply to all authorized customers).
A role name pasted into a prompt is not authorization. Do not add administrator
or manager to compensate for an old API replica; compare deployed versions and
verify the domain entitlement. Never guess alternative POST paths on 404.
OpenAPI v1 contains mainly gateways; v2 may exceed an older helper's 1 MiB limit.
Use these maintained routes instead of concluding that creation does not exist.

## Apply the FreePBX batch before handover

After creating the intended extensions through the API and confirming their
FreePBX-backed records, run `fwconsole reload` on the owning PBX through the
provisioned server connection, once after the batch rather than once per extension.
This is the required configuration-application step, not a substitute for API
creation. Use it within the authorized provisioning scope and existing server
approval policy; do not request another approval solely for this routine step.
It regenerates/reloads shared PBX configuration, so report its actual scope and
result. Do not restart Asterisk or promise zero call impact.

Verify the command exit/output and then check each enabled protocol independently:
`asterisk -rx 'sip show peer <canonical-title>'` for legacy SIP and
`asterisk -rx 'pjsip show endpoint <endpoint-id:N>'` for PJSIP. Both must exist
for SIP+PJSIP onboarding. A valid PJSIP endpoint does not compensate for a missing
legacy SIP peer. Legacy SIP remains supported: numeric canonical title as account
and auth login, voip.sufficit.com.br:26499, transport from the actual published
legacy profile. PJSIP uses the endpoint GUID profile from [registration.md](registration.md).
Never rotate a password or migrate a phone merely to bypass missing SIP generation.

A saved FreePBX row, HTTP200, pending=true or runtimeApplicationConfirmed=null
is not proof of loaded peers. If reload fails, times out or loses its reply,
inspect current peers and the application result before considering another run;
do not blindly loop reloads. Report created-but-not-applied when still missing,
preserve successful creations and continue investigation without SQL writes,
generated-file edits or duplicate creations. Even successful reload and peer
presence do not prove device registration or working audio.

## Customer default password and later changes

Maintained routes in EndPointController.Management.cs (sufficit-endpoints), with
the same customer authorization as creation:

- GET `/Telephony/EndPoint/DefaultPassword?contextId=<GUID>` reads the customer's
  preferred extension password (null when none).
- PUT `/Telephony/EndPoint/DefaultPassword` with `{contextId, password}` stores
  it, `{contextId, generate:true}` stores a new random one, and `{contextId}`
  alone removes it. None of them changes existing extensions.
- POST `/Telephony/EndPoint/DefaultPassword/Ensure?contextId=<GUID>` generates
  one only when missing; use it before onboarding creations.
- PUT `/Telephony/EndPoint/Update` changes description, qualify, codecs and,
  for internal managers, the outbound caller id; only the fields sent change.
- POST `/Telephony/EndPoint/Password` with `{contextId, endPointId, password}`
  sets one extension's password (omit `password` to generate). Devices already
  registered stop registering until reconfigured: confirm before doing it.
- GET/PUT `/Telephony/EndPoint/DialAliases` and GET/PUT `/Telephony/EndPoint/User`
  handle dial aliases and the linked identity user (by id or sign-in e-mail).
- DELETE `/Telephony/EndPoint?contextId=<GUID>&id=<GUID>` removes an extension
  and its aliases; it is refused with 409 while the dial plan still uses it.

The default password is a convenience for installing devices. Offer it, do not
enforce it: an explicit request for another password always wins.

## Preferences after creation

Apply per-extension preferences (for example recording — see
[preferences.md](preferences.md)) as separate, individually verified updates.

## Handover

1. Deliver the verified [device profile](registration.md) — PJSIP endpoint GUID
   without hyphens as account/auth login, existing secret, host, **port and
   transport** — to the named user through the channel the authorizing user
   explicitly authorized. Port and transport are required by most softphones;
   omitting them is a common cause of failed registrations.
2. Registering a softphone and making the first test call is the user's step;
   offer to check registration state through the API when such a read exists.
3. Record the completion target (company, extension number, date) without any
   secret.

## Rollback

If creation partially succeeded, re-read the extension state before retrying —
do not blindly repeat a write with an ambiguous outcome. Disabling the
just-created extension is the reversal when the API offers it; confirm nothing
started referencing it first.
