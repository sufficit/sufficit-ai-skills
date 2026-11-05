# Agent provisioning runbook

Create a helpdesk agent in a Hermes (Chatwoot) account and hand it over safely.
Flow-first: discover each call in the live OpenAPI before running it, then
record what the deployed API actually offered (field names, required arguments,
response shape) in this file as part of the change that first validated it.

## Pre-flight

1. Confirm the authorizing user, the target account (conta/instance) and the
   person who will become an agent (full name; corporate e-mail).
2. List the account's existing agents: confirm the e-mail is free (also across
   other visible accounts) and note the roles already in use, so the new agent
   gets a role consistent with the account's practice.
3. Decide what the agent needs: role (agent/administrator), availability, an
   API token (see [tokens.md](tokens.md)) and a telephony extension link —
   the extension itself is provisioned with
   [sufficit-telephony-extensions](../../sufficit-telephony-extensions/SKILL.md).

## Creation

1. Discover the creation operation (search terms: `agent`, `user`, `chatwoot
   user create`, `hermes agent create`).
2. One call per logical effect: create the agent with name, e-mail and role;
   do not bundle token issuance or extension linking into the creation call
   unless the contract requires it.
3. First access: report exactly what the deployed API does about the first
   password (invitation e-mail, forced reset, admin-set). Do not invent or set
   passwords unless the contract and the authorizing user explicitly say so.
4. Verify by an independent read: the agent appears in the account's list with
   the expected role and state.

## Extension link

1. Confirm the extension exists in the owning company and is intended for this
   agent; never create the link from an assumption.
2. Discover where the API exposes the agent-to-extension relation (agent
   detail, extension detail or a dedicated relation endpoint) and change only
   that; verify by re-reading both sides.

## Handover

1. Deliver what the agent needs to start (access path, invitation status) —
   and the API token separately, if one was issued — through the channel the
   authorizing user explicitly authorized.
2. Logging in, setting the first password and answering the first conversation
   are the user's steps; offer to verify the agent's state through the API.
3. Record the completion target (account, agent name/e-mail, role, extension
   number when linked, date) without any secret.

## Rollback

If creation partially succeeded, re-read the agent state before retrying — do
not blindly repeat a write with an ambiguous outcome. Suspending the agent is
the reversal when the API offers it; confirm nothing (queues, flows, open
conversations) started referencing it first.
