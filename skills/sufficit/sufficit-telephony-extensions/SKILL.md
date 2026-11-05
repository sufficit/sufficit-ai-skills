---
name: sufficit-telephony-extensions
description: "Manage Sufficit Telephony extensions (ramais) and their preferences through the live corporate API: list and inspect the extensions of a company, create a new extension with SIP credentials, change per-extension preferences such as call recording, and verify each change. Use when a request mentions ramais, provisioning de ramal, SIP extension credentials, preferencias do ramal or ligar/desligar gravacao. Not for raw Asterisk PJSIP peer files."
metadata:
  version: "0.1.0"
---

# Sufficit Telephony: extensions and preferences

Operate the real telephony system as the authenticated user, within the roles the
API already enforces. The deployed OpenAPI is the authority on paths, parameters
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
- Editing literal Asterisk `extensions.conf` or PJSIP peer files inside a
  repository is a different task (`asterisk-dialplan` skill); do not run dialplan
  recipes against the managed telephony API and do not treat this skill as peer
  configuration.

## Tools and discovery

Inside Genius, discover each operation with `sufficit_api_search` and run it with
`sufficit_api_call`; search in English when a Portuguese query finds nothing
(`extension`, `telephony`, `endpoint`, `preference`). Outside Genius, follow the
discovery workflow of the `sufficit-api` skill. Do not bypass missing tools with
`curl`, shell or database access, and never ask the user for a token, API key or
second login: the connected credential already carries the roles.

## Operation flow

1. Resolve the target company explicitly (for example via `companies current`)
   and confirm it matches the request. Keep that company selected across the
   follow-up questions of the same task.
2. Read before writing: list the company's extensions and inspect the target
   one. An extension number is an identifier, not a quantity; keep it exact.
3. Provisioning a new extension follows
   [references/provisioning.md](references/provisioning.md): one call per logical
   effect, verification by independent reading, safe delivery of credentials.
4. Changing per-extension settings follows
   [references/preferences.md](references/preferences.md).
5. Disabling or removing an extension changes live call handling: confirm the
   exact target (company + extension number), check what references it (queue
   membership, flows, voicemail notification) and report what was and was not
   verified.

## Credentials and secrets

- SIP secrets and API tokens are issued to be delivered once: do not print them
  in logs, chats, summaries or committed files.
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
corporate API workflow. Release 0.1.0 teaches the flow; the exact provisioning
calls must be confirmed against the live OpenAPI on first real use and recorded
in [references/provisioning.md](references/provisioning.md) in that same change.
