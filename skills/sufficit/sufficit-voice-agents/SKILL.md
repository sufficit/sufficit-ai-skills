---
name: sufficit-voice-agents
description: "Create and operate Sufficit AI voice agents (phone agents) for your company entirely through the Sufficit APIs: agent, persona, ElevenLabs voice agent, SIP number, virtual extension, training publication, test calls, training proposals and HTTP tools that call your own systems (for example an ERP such as IXC). Use when asked to set up, change, publish, test or diagnose a voice agent of a Sufficit telephony customer. Includes how to check for and apply updates of this skill."
metadata:
  version: "1.2.0"
---

# Sufficit voice agents

A voice agent is one Fleet agent that also talks on the phone. The conversation runs at ElevenLabs inside the
Sufficit account, the audio goes straight from the Sufficit PBX to ElevenLabs over SIP, and the agent appears in your
PBX as a virtual extension. You manage everything through APIs; there is no screen for it and nobody needs to be
contacted for routine work. Each API owns its part:

| API | Owns |
|---|---|
| Fleet `https://fleet.sufficit.com.br/api/fleet/v1` | agent, persona, voice binding, ElevenLabs agent and SIP number, training, test calls, proposals |
| Telephony `https://endpoints.sufficit.com.br` | extensions, queues, DIDs, campaigns (Fleet calls it for you when creating the virtual extension) |
| Identity `https://identity.sufficit.com.br` | users, tokens and permissions |

The live OpenAPI is the authority on paths and fields: `https://fleet.sufficit.com.br/swagger/v1/swagger.json`.
Read it before the first call of a session; this skill adds the order, the rules and the meaning.

## Check for updates first

Once per session, before working, compare the installed `metadata.version` above with
`https://raw.githubusercontent.com/sufficit/sufficit-ai-skills/main/skills/sufficit/sufficit-voice-agents/release.json`.
If the remote version is higher, read the remote [CHANGELOG](CHANGELOG.md) entries newer than yours and update before
continuing. Details in [updating this skill](references/updating.md). A failed check is not a blocker: say so once and
continue with the installed version. Never claim to be up to date without a successful comparison.

## Access

- Send `Authorization: Bearer <token>`. The token is a personal Fleet token of a user of your company, created at
  `https://fleet.sufficit.com.br/api-tokens` (scope `fleet.api`). Keep it in your secret store, never in prompts,
  URLs, logs or files you share.
- The user needs the AI permission (entitlement) in your company context. Agents and system users cannot manage voice:
  a human user's token is required for every route below.
- Your company must be admitted to voice. Read `GET contexts/{contextId}/voice`: `enabled: true` means you can proceed.
  `contextId` is your company id (the telephony context Guid).
- `401`: token expired or revoked, create a new one. `403`: the user lacks the permission or the resource belongs to
  another company; never retry with another context. `409`: state or revision conflict, read the current state first.

## Build a voice agent, in order

All paths are relative to `https://fleet.sufficit.com.br/api/fleet/v1`. Ids are Guids you generate. Full payloads:
[API reference](references/api.md).

1. **Agent.** Create a public-only privilege profile and a mission template in your context
   (`PUT catalog/profiles/{id}`, `PUT catalog/templates/{id}`), then `POST agents` (it starts paused). Reuse an
   existing agent when the user names one.
2. **Persona and instructions.** `PUT agents/{id}/persona` (who the agent is, tone, what it may and may not say) and
   `PUT agents/{id}/instructions`. Read first and send the current `expectedRevision`. This is the training source.
3. **ElevenLabs agent and SIP number.** `POST agents/{id}/voice/provider` with optional `firstMessage`, `voiceId`,
   `language` (default `pt`) and `voicemailDetection` (only for agents that call out). It creates the ElevenLabs agent
   from the Sufficit-tuned template, its SIP number and its tools, and registers them to your company. It is
   idempotent: after any error or timeout, call it again; it never creates a second agent or number.
4. **Free extension.** `GET agents/{id}/voice/setup` returns your telephony context and a suggested free extension.
5. **Voice binding, disabled.** `PUT agents/{id}/voice` with `telephonyContextId` (your company id), `templateId`,
   `providerAgentId` and `phoneNumberId` from step 3, `extension` from step 4 (optional: the agent's Id always
   identifies its virtual extension; a number only makes it dialable by number), `allowedExtensions` (your extensions
   treated as trusted staff), `mode: "synchronized"`, `memoryAccess` (`none` or `read`; `write` only when the user
   asks), `publicAccess` (see below), `enabled: false`, `expectedRevision: null` on creation.
6. **Virtual extension.** `POST agents/{id}/voice/provision` with `telephonyContextId`, `number` (the extension) and
   the binding `revision`. The extension appears in your PBX pointing at the agent.
7. **Publish training.** `POST agents/{id}/voice/publish`. It turns persona and instructions into an immutable
   version and publishes it to the ElevenLabs agent with read-back. Repeat after every persona or instruction change;
   nothing reaches the phone until published. Optional `model` pins the conversation model.
8. **Enable.** `PUT agents/{id}/voice` again with `enabled: true` and the current `expectedRevision`. Enabling checks
   that the SIP number, the extension and the published training all point to the same agent; a failure names the
   step to redo.
9. **Test.** `POST agents/{id}/voice/calls` with a new `requestId`, `number` (an internal extension of your company
   first) and `purpose`. Then call the agent's extension from an allowed extension.

## Tools for your own systems (HTTP tools)

Agents can call your own APIs (ERP, CRM, billing; for example IXC) through **HTTP tools** you declare. They are
declarations, not code: Fleet builds each request from the parameters the agent fills in, adds your credential, calls
your system and returns only the response fields you chose. Full contract and an IXC example:
[HTTP tools](references/http-tools.md).

1. Store the secret once: `POST credentials?contextId={contextId}` (write-only, kept in the Sufficit Vault).
2. Declare the tool: `PUT contexts/{contextId}/http-tools/{toolId}` with method, HTTPS address, typed parameters,
   credential and `responseFields`.
3. Test it: `POST contexts/{contextId}/http-tools/{toolId}/test` with sample parameters. This calls your real system.
4. Grant it: `PUT agents/{agentId}/http-tools`. Tools that change data (`effect: "write"`) need `allowWrite: true`.
5. Voice agents receive tool changes on the next `voice/publish`.

## Callers from outside (queues, DIDs, IVR)

The agent is a virtual extension of your PBX (Id, optional number) and shows in the telephony panel, where calls can
be followed, listened to and whispered. Anyone who reaches it through a queue, DID or IVR, or from an extension not in
`allowedExtensions`, is a **public caller**: the number is not authenticated. `publicAccess` on the binding decides
what such a call may trigger:

| Value | Public caller gets |
|---|---|
| `none` | training only, no tool |
| `read` (default) | call context and HTTP tools with `effect: "read"` |
| `full` | also the agent's Fleet task, memory and write HTTP tools granted with `allowWrite` |

Write in the persona how the agent confirms identity (for example CPF) before giving personal or financial data.

## Safety

- **`voice/calls` rings a real phone.** Call only numbers the user asked for, with a stated purpose. Test on an
  internal extension of your company before any outside number. Reuse the same `requestId` to retry: a new one can
  place a second call. If the result is `uncertain`, read the state before trying again.
- Outbound campaigns to lists of people are a separate product (skill `sufficit-campaigns`); do not loop over
  `voice/calls` to build one.
- The agent never denies being an AI when sincerely asked. Do not write persona text that tells it to.
- Never put passwords, tokens, card numbers or personal data in persona or instructions: they are published to the
  phone agent.
- Only change agents of your own company. Never reuse an ElevenLabs agent id you did not get from step 3.
- HTTP tools: prefer `effect: "read"`; grant write tools only to agents that need them and describe in the tool what
  must be confirmed with the caller. Keep `responseFields` minimal: whatever is returned may be spoken aloud.

## Operating

- **What the agent learned.** `GET agents/{id}/voice/proposals` lists suggestions the agent made during calls.
  `POST agents/{id}/voice/proposals/{proposalId}` with `{ "approve": true|false }`. Approved training enters the next
  publication (step 7), never the live agent directly.
- **Pause.** `PUT agents/{id}/voice` with `enabled: false`. Calls stop reaching it; nothing is deleted.
- **Voice, greeting and language** are chosen in step 3. Changing them on an existing agent is not in the API yet;
  ask support. Everything the agent says comes from persona and instructions, so most changes are step 2 + step 7.
- **Diagnose.** Read `GET agents/{id}/voice`, `GET agents/{id}/voice/provider` and `GET agents/{id}/voice/setup`
  before changing anything. Report the exact route and status that failed.

## Support

Escalations go to the support contact in `GET contexts/{contextId}/voice` (`supportEmail`). Contact it only for what
the API cannot do: a new voice library, admitting the company to voice, or a failure that persists after reading
the state and retrying an idempotent call once.
