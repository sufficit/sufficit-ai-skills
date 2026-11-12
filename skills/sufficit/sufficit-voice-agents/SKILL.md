---
name: sufficit-voice-agents
description: "Create and operate Sufficit AI voice agents (phone agents) for your company entirely through the Sufficit APIs: agent, persona, ElevenLabs voice agent, SIP number, virtual extension, training publication, test calls and training proposals. Use when asked to set up, change, publish, test or diagnose a voice agent of a Sufficit telephony customer. Includes how to check for and apply updates of this skill."
metadata:
  version: "1.0.0"
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
   `providerAgentId` and `phoneNumberId` from step 3, `extension` from step 4, `allowedExtensions` (extensions allowed
   to call the agent; empty = nobody calls in), `mode: "synchronized"`, `memoryAccess` (`none` or `read`; `write`
   only when the user asks), `enabled: false`, `expectedRevision: null` on creation.
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
