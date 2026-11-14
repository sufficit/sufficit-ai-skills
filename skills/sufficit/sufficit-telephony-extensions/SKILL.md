---
name: sufficit-telephony-extensions
description: "Manage Sufficit Telephony extensions (ramais) and their preferences through the live corporate API: list and inspect the extensions of a company, create a new extension with SIP credentials, change per-extension preferences such as call recording, and verify each change. Also covers device auto-provisioning by MAC (provisioning server, TFTP/HTTP/HTTPS, Intelbras TIP 125i, Grandstream, Cisco, Linphone QR). Use when a request mentions ramais, provisioning de ramal, provisionamento de aparelho, MAC, SIP extension credentials, preferencias do ramal or ligar/desligar gravacao. Not for raw Asterisk PJSIP peer files."
metadata:
  version: "0.8.0"
---

# Sufficit Telephony: extensions and preferences

Operate the real telephony system as the authenticated user, within the roles the
API already enforces. Use the current domain contracts and deployed behavior to confirm paths, parameters
and formats; this skill adds the flow and the business semantics of extension
(ramal) management. Routes change between releases: never assume a method, path
or parameter from memory.

## Scope and boundaries

- An **extension (ramal)** belongs to exactly one **company**. Every read and
  write is scoped to a company: confirm the target company before any write and
  never widen an operation to another company because a query returned empty.
- This skill covers creation, listing, inspection, update, enable/disable of
  extensions, per-extension preferences (recording and whatever else the API
  exposes) and the SIP credentials an endpoint needs to register.
- Call routing — attendance flows, applications, destinations, queues, voicemail
  as a destination — is covered by
  [sufficit-telephony-dialplan](../sufficit-telephony-dialplan/SKILL.md).
  Attendant-style reads (recordings, listing voicemail boxes) start at
  [sufficit-api](../sufficit-api/SKILL.md).
- Helpdesk agents (Hermes/Chatwoot users, agent API tokens, agent-to-extension
  links) are administered with
  [sufficit-hermes-agents](../sufficit-hermes-agents/SKILL.md).
- Editing literal Asterisk `extensions.conf` or PJSIP peer files inside a
  repository is a different task (`asterisk-dialplan` skill); do not run dialplan
  recipes against the managed telephony API and do not treat this skill as peer
  configuration.

## Default new extensions

The owner-defined standard is SIP **and** PJSIP together, with recording enabled.
Use `technology="SIP+PJSIP"` and `recording=true` on creation; one protocol alone is
not the default. Do not ask the user to choose technology or whether to record.
Never turn off an existing endpoint or reset its password to apply new defaults.
After a FreePBX-backed creation batch, apply `fwconsole reload` once and verify
legacy SIP peers and PJSIP endpoints before handover; follow the
[application step](references/provisioning.md#apply-the-freepbx-batch-before-handover).

## Registering a device

PJSIP uses the ENDPOINT `id` without hyphens for account/auth/AOR, not the numeric
extension title or customer GUID. New-device profile: `voip.sufficit.com.br:26498`,
TCP, existing endpoint password through the secure portal/provisioning flow.
Port26499 is legacy chan_sip. GUID AORs are expected; a numeric-user404 does not
prove broken generation. Masked helper fields cannot establish a password mismatch.
Read [registration diagnostics](references/registration.md) before diagnosing a
registration failure or proposing a credential reset.

## Customer default password

A customer usually keeps **one password for all its extensions**, so installing
phones is easier. The API stores that preferred password per customer and uses
it whenever an extension is created without a password. It is a facilitator,
not an imposition:

- Before creating extensions for a customer, make sure the default exists with
  POST `/Telephony/EndPoint/DefaultPassword/Ensure?contextId=<GUID>`. It generates
  one only when there is none, never replaces an existing one and does not return
  the value. Then create the extensions without a `password`.
- The requester may always ask for a different password on one extension, a
  generated one, or no shared password at all. Follow that request; do not
  argue for the default and do not rewrite it to match.
- Never change existing extensions to "align" them with the default, and never
  replace or remove a customer's default unless the requester asks for exactly that.
- You do not need to read the value to do onboarding. Read it (GET
  `/Telephony/EndPoint/DefaultPassword?contextId=<GUID>`) only when the person who
  will configure the devices asks for it, and deliver it under the rules of
  "Credentials and secrets" below.

## Customer onboarding

For initial setup (extensions, a waiting queue and the incoming DID), read
[references/customer-onboarding.md](references/customer-onboarding.md). Keep one
customer-scoped checklist across the whole workflow; creating extensions alone
does not complete onboarding.

## Tools and discovery

Inside Genius, discover each operation with `sufficit_api_search` and run it with
`sufficit_api_call`; search in English when a Portuguese query finds nothing
(`extension`, `telephony`, `endpoint`, `preference`). Outside Genius, follow the
discovery workflow of the `sufficit-api` skill. A provisioned authenticated domain helper (such as Fleet's
`dotnet /data/support/api-client/api-helper.dll endpoints METHOD /path [json-file]`)
is a supported API transport when discovery tools are unavailable. Never bypass
a refused API with database writes, FreePBX CLI or generated-file edits, and never ask the user for a token, API key or
second login: the connected credential already carries the roles.

## Operation flow

1. Resolve the target company explicitly (for example via `companies current`)
   and confirm it matches the request. When the scenario names a **PBX central**
   (host:port) instead of the company, first resolve which company owns that
   central — see the pre-flight of
   [references/provisioning.md](references/provisioning.md) — and never assume
   the mapping. Keep the company selected across the follow-up questions of the
   same task.
2. Read before writing: list the company's extensions and inspect the target
   one. An extension number is an identifier, not a quantity; keep it exact.
3. Inspect existing extensions when available, but an empty customer is a normal
   onboarding case. Resolve the canonical login through Creation/Preview and let
   the server assign credentials: the customer's default password when one is set
   (see "Customer default password"), otherwise a generated one. Do not demand existing extensions or invent
   a customer prefix. New extensions default to both SIP and PJSIP enabled
   (`technology="SIP+PJSIP"`) and recording=true. These are approved house defaults;
   do not ask the requester to choose a protocol or recording for normal onboarding.
4. Provisioning a new extension follows
   [references/provisioning.md](references/provisioning.md): one call per logical
   effect, verification by independent reading, safe delivery of credentials.
5. Changing per-extension settings follows
   [references/preferences.md](references/preferences.md).
   Configuring a physical phone or softphone to download its settings (server,
   protocol, port, path, MAC registration, download evidence) follows
   [references/device-provisioning.md](references/device-provisioning.md);
   it is a different system from extension creation.
6. Disabling or removing an extension changes live call handling: confirm the
   exact target (company + extension number), check what references it (queue
   membership, flows, voicemail notification) and report what was and was not
   verified.

## Credentials and secrets

- SIP secrets and API tokens are issued to be delivered once: do not print them
  in logs, chats, summaries or committed files.
- Never invent a SIP secret yourself, and never a patterned one (`1234`, the
  company name, shared prefixes): a patterned secret is a security defect, not a
  convention. Let the system issue it. The customer's stored default password is
  different: it is a random secret the customer chose to share across its own
  extensions, kept by the API, and using it for that customer is approved.
- A secret the requester dictates for an extension must fit the API rule (exactly
  10 characters: letters, digits or `! $ & *`; never `@`). If it does not, report
  the rule instead of adjusting the value yourself.
- Deliver credentials only to the person who will use them, through a channel
  the authorizing user explicitly authorized. Sending credentials to a third
  party (another company, an external address) is a separate decision that only
  the authorizing user can make explicitly in text; a provisioning request does
  not authorize it by itself.
- On refusals: `403` means the authenticated roles do not allow the operation —
  report which call was refused, do not ask for a new login. `401` means the
  session must be reconnected once. `409` means re-read the state before
  deciding. `422` means fix only the fields the contract named.

## Validation

After each write, re-read the affected extension and report company, extension
number, what changed and the final state — without secrets. When the deployed
API does not expose an operation this skill describes, follow the document,
report the limitation and do not invent a route or simulate success.

## Sources and provenance

Authored by Sufficit from the `Sufficit.Telephony` guides (wiki) and the
corporate API workflow. Release 0.1.0 taught the flow; 0.2.0 adds the
house-format rule, central-to-company resolution, secret policy and
disabled-number handling from the first dry-run review. Release 0.6.0 adds the customer default password as an onboarding step that runs before extension creation (a facilitator, never an imposition), plus update, password, alias, user-link and removal operations. Release 0.5.1 adds the owner-defined dual-protocol/recording creation standard and
Principal/default-hold-music onboarding policy. Release 0.3.0 documents the current insert-only creation contract and full
customer onboarding, including limited discovery, initial setup and reconciliation.
OpenAPI v1 may omit telephony; a v2 document exceeding a helper limit is a
discovery failure, not proof that creation is unsupported. Use the maintained
contract in [references/provisioning.md](references/provisioning.md), then verify
live preflight authorization. A generic insufficient_scope header on 403 does
not identify which scope or business entitlement is missing.

## Restricted Fleet catalog bridge

[scripts/queue_catalog_bridge.py](scripts/queue_catalog_bridge.py) is installed only
on the trusted Queue portal behind an SSH forced command whose actor GUID is fixed
by deployment. It never accepts a host, key or audit actor from the agent request.
The agent invokes its existing queue-catalog wrapper. Creation uses UUIDv7 plus
If-None-Match; updates require a strong revision. The domain API still validates
member ownership and queue options. Do not execute this server helper locally to
bypass the provisioned connection.

## Talk to Sufficit

Report to Sufficit, as a support thread, what still fails after reading the state and retrying once, a capability you
need that is missing, or a question the API cannot answer: `POST /Support/Threads` with the same credential, `source:
"skill:sufficit-telephony-extensions"`. Once per session, also read the threads waiting for the company
(`GET /Support/Threads?contextId={contextId}&waitingFor=customer`) and act on them within this skill's rules. Full
contract: skill [`sufficit-support`](https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/sufficit/sufficit-support).
