---
name: sufficit-hermes-agents
description: "Administer helpdesk agents in Hermes (Chatwoot) through the live corporate API: create an agent user in an account (conta) with name, e-mail and role, manage availability, issue and rotate agent API tokens, link an agent to a telephony extension (ramal) and offboard agents. Use when a request mentions criar usuario/agente no Chatwoot ou Hermes, conta/instance, token de API do agente, vincular ramal ao agente or desativar agente. Not for self-service agent reads (hermes-api) and not for the ramal itself (sufficit-telephony-extensions)."
metadata:
  version: "0.1.0"
---

# Sufficit Hermes: agent administration

Administer the human attendants of Hermes (Chatwoot) as an authenticated
administrator. The deployed OpenAPI is the authority on paths, parameters and
formats; this skill adds the flow and the business semantics of agent
administration. Routes change between releases: never assume a method, path or
parameter from memory.

## Scope and boundaries

- An **agent** is a user of a Chatwoot **account** (conta/instance). Every write
  is scoped to an account: confirm the account (number or identifier) matches
  the request before writing and never widen an operation to another account.
- This skill covers creating, listing, inspecting, updating, suspending and
  removing agent users; agent roles and availability; issuing and rotating agent
  **API tokens**; and linking an agent to a telephony extension.
- Reading one's own profile, conversations and notes as the agent themself is
  the `hermes-api` skill. Attendant-style reads across channels start at
  `sufficit-api`.
- The **ramal itself** (SIP credentials, preferences, numbering) is
  [sufficit-telephony-extensions](../sufficit-telephony-extensions/SKILL.md);
  this skill only makes the link between an agent and an existing extension.
- First access: many flows deliver the invitation by e-mail or require the user
  to set the first password themselves. Never invent or set a password on the
  user's behalf unless the deployed API and the authorizing user explicitly say
  so; discover what the contract offers and report it.

## Tools and discovery

Inside Genius, discover each operation with `sufficit_api_search` and run it
with `sufficit_api_call`; search in English when a Portuguese query finds
nothing (`agent`, `user`, `chatwoot`, `hermes`, `token`, `access token`).
Outside Genius, follow the discovery workflow of the `sufficit-api` skill. Do
not bypass missing tools with `curl`, shell or database access, and never ask
the user for a token, API key or second login: the connected credential already
carries the roles.

## Operation flow

1. Resolve the target account explicitly (for example account/instance 4) and
   confirm it matches the request; keep it selected for the whole task.
2. Read before writing: list the account's agents and confirm the intended
   e-mail is not already in use — in this account or any other visible one. If
   the e-mail already exists, report where and stop; do not create variants of
   it.
3. Creating an agent follows
   [references/provisioning.md](references/provisioning.md).
4. Tokens follow [references/tokens.md](references/tokens.md).
5. Linking an agent to an extension: confirm both exist first — the agent in
   this account and the extension in the owning company (resolution rules in
   the telephony skill) — then discover where the API exposes the link (agent
   detail, extension detail or a dedicated relation) and change only that.
6. Offboarding: check what the agent still owns (open conversations, queue
   memberships) before removing; revoke tokens and unlink the extension as
   separate steps; report what was and was not verified.

## Credentials and secrets

- Agent API tokens are secrets: issue, deliver once, never echo them into
  logs, chats, summaries or committed files.
- Deliver a token only to the person who will use it, through a channel the
  authorizing user explicitly authorized. Sending a token to a third party
  (another company, an external address) is a separate decision that only the
  authorizing user can make explicitly in text; a provisioning request does not
  authorize it by itself.
- On refusals: `403` means the authenticated roles do not allow the operation —
  report which call was refused, do not ask for a new login. `401` means the
  session must be reconnected once. `409` means re-read the state before
  deciding. `422` means fix only the fields the contract named.

## Validation

After each write, re-read the affected agent and report account, name, e-mail,
role, what changed and the final state — without secrets. When the deployed API
does not expose an operation this skill describes, follow the document, report
the limitation and do not invent a route or simulate success.

## Sources and provenance

Authored by Sufficit from the Hermes/Chatwoot administration workflow and the
corporate API. Release 0.1.0 is flow-first: the exact calls must be confirmed
against the live OpenAPI on first real use and recorded in
[references/provisioning.md](references/provisioning.md) in that same change.
