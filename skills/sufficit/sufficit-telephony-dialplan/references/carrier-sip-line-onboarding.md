# Carrier SIP line onboarding

“Cadastrar uma linha SIP como a Datora” normally calls for registering a carrier
account on an existing interconnection. A DID controls ownership and inbound
routing. A catalog trunk describes a SIP peer. Identify which outcome the
request needs before choosing the API.

1. Resolve the DID and customer from the trusted conversation context and
   available DID, sales and carrier records. Normalize the number for lookup
   and keep the carrier's SIP username as supplied. Check for an existing DID,
   PJSIP registration or legacy registration before creating anything. A number
   prefix or a carrier name can narrow the search. Neither authorizes a write
   to a customer or implies a shared trunk. Ask one focused question only for
   the missing fact that blocks the operation.
2. Identify the existing interconnection by its GUID and verified carrier
   mapping. For TIP Brasil, legacy ingress channels named `in-tip` are a
   confirmed carrier hint for call evidence. They do not establish the new line's
   registrar, credentials or node. Reuse the workflow from Datora and confirm
   TIP's own approved profile. Check whether the supplied IP is the remote
   registrar, an inbound source or a local address to be allowlisted. Use the
   validated profile for auth mode, port, transport, node and URI format. SIP
   account credentials alone do not establish whether the carrier requires
   REGISTER or only authenticates INVITE.
3. For SIP REGISTER, use an authorized API that adds the credential and PJSIP
   registration to that verified interconnection. Datora's
   `POST /Telephony/datora/activation` is a dedicated worker endpoint with a fixed
   carrier, context and node profile. It does not accept TIP. The generic
   `/Telephony/trunk/single` and `provisioningsync` workflow generates peer,
   AOR, auth and identify objects. It does not create outbound registrations.
   Peer provisioning applies only if the verified carrier mode calls for it.
4. In Endpoints, the shared catalog exposes
   `GET /Telephony/Routes/Interconnection?interconnectionId=…`,
   `POST /Telephony/Routes/Interconnection` and
   `GET /Telephony/Routes/RegistrationStatuses?interconnectionId=…`.
   These routes require an Administrator and operate on the shared
   interconnection. The POST accepts the aggregate including hosts,
   credentials, matches and registrations. Do not send a partial aggregate
   or infer approval to edit the entire shared configuration from a request
   for one line. Prefer a scoped, additive API with duplicate checks and
   stable operation identity when available. If the authorized deployment
   offers only the administrator aggregate, record the exact carrier and
   operation needed and escalate to its owner. Do not ask for a broad role,
   change the PBX or write to the database. A `403 insufficient_scope` on
   `GET /Telephony/trunk` only describes that request. An omitted context or
   empty GUID selects global scope there. Confirm the actual operation and
   permission before concluding that all carrier APIs are unavailable.
5. Pass secrets through the approved private channel or server-side credential
   mechanism. Keep the secret out of chat replies, notes, shell arguments,
   logs and saved examples. If it appeared in a group, treat it as exposed
   and have it rotated before using it for live enrollment. Check the approved
   customer ownership and any destination before a separate DID/route change.
6. Report the highest stage supported by evidence: persisted registration,
   registered on the expected PBX node, inbound call on the verified carrier
   channel, and delivery to the approved destination. Verify outbound service
   separately when requested. HTTP success or SIP Registered alone does not
   prove call delivery. After an uncertain write, query the exact registration
   and its status before retrying so a second registration is not created.

Check the deployed API contract and the executor's effective access before any
operation. When a scoped TIP registration operation is absent or inaccessible,
complete the available reads and report the exact gap plus the pending facts.
