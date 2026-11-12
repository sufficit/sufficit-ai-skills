# Voice agent API reference

Base `https://fleet.sufficit.com.br/api/fleet/v1`, header `Authorization: Bearer <personal Fleet token>`,
`Content-Type: application/json`. Confirm fields in `https://fleet.sufficit.com.br/swagger/v1/swagger.json`; the
deployed schema wins over this page. Errors are RFC 7807 problem details with `title` and `correlationId`; quote both
when reporting a failure.

## Company admission (read only)

`GET contexts/{contextId}/voice`

```json
{ "contextId": "…", "telephonyContextId": "…", "name": "…", "enabled": true,
  "supportEmail": "…", "revision": "…", "providerAgentIds": ["agent_…"] }
```

Admission and the support contact are set by Sufficit; the write route answers 403 to customers.

## Agent

| Step | Route | Body |
|---|---|---|
| Profile | `PUT catalog/profiles/{profileId}` | `{ contextId, expectedRevision: null, reason, configuration: { id, contextId, name, … } }` — no tools, code, volumes or credential grants (those need Sufficit) |
| Template | `PUT catalog/templates/{templateId}` | `{ contextId, expectedRevision: null, reason, configuration: { id, contextId, name, profileId, brief } }` |
| Create | `POST agents` | `{ contextId, profileId, name, runtimeMode, reason }` — `name` is a slug: `^[a-z0-9][a-z0-9-]{1,79}$` (e.g. `atendimento-voz`); the spoken name goes in the persona |
| Read | `GET agents/{id}`, `GET agents?contextId=` | |
| Persona | `GET` then `PUT agents/{id}/persona` | `{ profile, expectedRevision }` |
| Instructions | `GET` then `PUT agents/{id}/instructions` | `{ instructions, tools: null, expectedRevision }` |

Catalog responses return `{ revision, configuration }`; keep `revision` for the next edit.

## Voice

| Step | Route | Body / result |
|---|---|---|
| Create provider | `POST agents/{id}/voice/provider` | `{ firstMessage?, voiceId?, language?, voicemailDetection? }` → `{ providerAgentId, phoneNumberId, sipUri, toolIds, created }` |
| Read provider | `GET agents/{id}/voice/provider` | same shape, or empty when not created |
| Setup | `GET agents/{id}/voice/setup` | `{ telephonyContextId, customerName, number, providerAgentId, phoneNumberId, ready }` |
| Binding | `GET` / `PUT agents/{id}/voice` | see below |
| Virtual extension | `POST agents/{id}/voice/provision` | `{ telephonyContextId, number, expectedRevision }` → `{ id, contextId, number, title, virtual, canRegister }` |
| Publish training | `POST agents/{id}/voice/publish` | `{ model? }` → `{ versionId, state, message }` |
| Test call | `POST agents/{id}/voice/calls` | `{ requestId, number, purpose }` → `{ id, state }`; `state`: `accepted`, `rejected`, `uncertain` |
| Proposals | `GET agents/{id}/voice/proposals` | newest first, `state`: `pending`, `approved`, `rejected` |
| Decide | `POST agents/{id}/voice/proposals/{proposalId}` | `{ approve }` |

Binding body (`PUT agents/{id}/voice`):

```json
{
  "telephonyContextId": "<your company id>",
  "templateId": "<template id>",
  "historyGroupId": null,
  "providerAgentId": "agent_…",
  "phoneNumberId": "phnum_…",
  "extension": "6050",
  "allowedExtensions": ["6001", "6002"],
  "enabled": false,
  "expectedRevision": null,
  "mode": "synchronized",
  "memoryAccess": "none"
}
```

- The response carries `revision`; every later `PUT` and `provision` must send it.
- `telephonyContextId` must be your own company and `providerAgentId` must come from `voice/provider`; anything else
  answers 403.
- `extension`: 3–10 digits, free in your PBX (use `voice/setup`). `allowedExtensions`: up to 100, the extensions
  allowed to call the agent.
- `enabled: true` is refused (409) until the training of that same ElevenLabs agent is published and the virtual
  extension exists. The message says which part is missing.
- Changing the binding while a call is running answers 409; retry after the call.
- `voice/calls` `number`: an internal extension (`6xxx`) or 10–15 digits with area code. A previous `uncertain` call in
  the last 20 minutes blocks a new one: read the state first.

## Idempotency summary

| Route | Safe to repeat |
|---|---|
| `voice/provider` | yes, always |
| `voice/provision` | yes, with the same revision |
| `voice/publish` | yes; republishing the same text keeps the same version |
| `voice/calls` | only with the same `requestId`; a new id is a new call |
| `PUT voice`, persona, instructions | with the current `expectedRevision` |
