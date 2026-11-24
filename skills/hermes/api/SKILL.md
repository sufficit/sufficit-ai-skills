---
name: hermes-api
description: "Connect your own Hermes (Chatwoot) account: conectar Hermes, pegar token de acesso, onde obter e salvar token no Vault, configurar ou verificar conexao. Use the Hermes helpdesk API for contacts, attendances, messages/PDF and Kanban (funis, etapas, cartões, relatórios e operações em lote). Discover the native tools or use the authorized API."
metadata:
  version: "0.5.1"
---

# Hermes API

Hermes is Sufficit's helpdesk, built on Chatwoot and extended. Routes change between
releases, so **this skill teaches how to discover the API, not a frozen list of routes**.
Follow the server's OpenAPI for documented operations. For plugin routes omitted from
the spec, use the corresponding Hermes plugin source or supported client.

## Fleet helpdesk investigations and message handling

Use the agent's configured identity, account and inboxes. For a delegated history
request use `hermes_telephony` with `operation=conversation_search`, the current
mission ID and inclusive local dates. The requester should supply the customer
name as well as any verified context ID. Check both contact matches and message
mentions. A staff thread often names a customer whose own contact has a different
name. Report the conversation, date, speaker and inbox. An incoming message in a
staff group can be a colleague's report. Attribute a request to the customer
only when the participant and wording establish that. Report partial coverage.

In a customer-facing attendance, inspect the account, conversation and channel
before acting. Read text, caption and attachment metadata. Use the authorized
original for contents; indicate when the file could not be interpreted. Use
the connector's outgoing text or multipart attachment operation for the actual
file (audio, image, video or document). A private note, a quoted message and
a public reply have different audiences. Verify the returned message ID, inbox,
recipient, visibility and attachment. Report delivery only when the provider
confirms it. Interactive buttons, templates and other structured content depend
on the channel and its current API. Never silently convert an unsupported format
or resend after an ambiguous outcome. A private investigation returns evidence
to the requesting agent; it does not initiate a customer-facing conversation.

## Optional native plugin in Genius

Discover the required native tool first. If it is absent and `plugin_runtime` is
available, call `action: "list"`, then `action: "install", id: "sufficit.hermes"`
from the compatible official signed catalog. Re-query the tool catalog after
installation; the tools load on this device in the current session. Reuse an
already available plugin. A deliberately disabled plugin needs re-enabling through
Genius's plugin controls; preserve the user's setting. An older app without the
manager, or a catalog without a compatible package, needs an app update to install
native packages. Installation does not authorize
provider operations or moving the task to another computer.

## Genius: use the connected Hermes tools first

When running inside Genius with `hermes_*` tools, the plugin resolves the personal
API token from Identity Vault (`personal/hermes/production/api-token`). The absence
of `HERMES_*` environment variables does not mean the connected account is missing.
Use `hermes_connection_test` to obtain the authenticated account IDs. A successful
check is evidence that credentials work; preserve that evidence for subsequent steps.
Missing specialized tools do not mean missing API access. Discover/activate the exact
`hermes_*` tool first and apply the optional-plugin installation above when absent; if the installed tools still lack a required field, continue through
[the API/Vault fallback](references/connected-execution.md). This fallback is also
for Genius, not only external scripts. Respect actual permission denials.

## Kanban cards, funnels and stages

For cartões, itens, funis, etapas, bulk actions or board reports in Hermes, read
[the Kanban Board API guide](references/kanban.md). It maps plugin routes and
payloads, account permissions and checks for partial writes. Use the account
resolved from the authorized credential, including when the request names Fleet Suporte.

## Connect Hermes / pegar e salvar o token

For a missing/invalid personal token **or a beginner asking where to get and save
it**, provide these two destinations before ending the reply:

1. [Seus tokens no Hermes](https://chatwoot.sufficit.com.br/app/profile/access-tokens).
   This is the direct production token page, not a guessed settings menu. Ask the
   user to sign in if needed, choose **Meus tokens**, and **Revelar/Copiar** an
   existing active personal token. Do not tell everyone to create or rotate one.
2. Discover and call `vault_prepare_entry` with
   `name: "hermes/production/api-token"`; show its **actual returned URL** as
   **Salvar no Vault**. Tell the user to paste the token there and save, never in
   chat. Preparing this link does not save or overwrite a credential, so it is
   appropriate for guidance even when the user asks to preserve their connection.
   In the result, `saved: false` means **this preparation call saved nothing**;
   `exists: true` means an entry already exists. Do not say an existing active
   credential is unsaved or needs replacement. Check `vault_get_info` if its
   actual state matters. If preparation fails, explain that failure; never invent
   a replacement URL.

A Vault path alone, a Hermes home/profile link, or “open the connection settings”
is insufficient. For old Hermes versions without that page, the verified fallback
is [profile settings](https://chatwoot.sufficit.com.br/app/profile/settings).
After the user saves, check Vault metadata and `hermes_connection_test` before
claiming connection success or resuming the original task.

Prefer completing the authorized connection through the current user's existing
browser session when the available tools can transfer the token safely. Before
retrieving/revealing a token, read [personal browser-to-Vault connection](references/token-onboarding.md)
for identity verification, secret-safe transfer, login/MFA and token creation
boundaries. Do not require this extra read just to provide the two guided links.

The user supplies the business outcome, not API paths, token locations, inbox IDs or
commands. Resolve technical details yourself from the account and contact evidence.
A request to open an attendance **and send the supplied message/PDF** authorizes both
steps; do not require the user to open it manually or repeat that instruction.

For an existing contact that needs a conversation or a different responsible agent:

1. Resolve the contact with `hermes_contacts_search`. When names are ambiguous,
   confirm the intended contact before writing.
2. Use `hermes_contact_conversations_list(account_id, contact_id)` directly instead
   of walking account-wide pages. It returns up to 20 recent conversations visible
   to the authenticated user, not a complete history; an empty result is not proof
   that no older or inaccessible conversation exists.
3. Resolve the intended inbox with `hermes_inboxes_list`. If multiple inboxes fit
   use the contact's channel bindings and recent history to resolve the intended one. Ask only if materially different destinations still fit.
4. On an explicit request to open an attendance, call `hermes_conversation_create`
   with `account_id`, `contact_id`, `inbox_id`. The provider can reuse an existing
   conversation according to inbox policy; use the returned conversation ID.
   Creation does not send a message. Omit `source_id` unless the actual contact/inbox
   source identifier is known; never invent it. Unsupported channels may refuse
   creation and require resolving the contact's channel identity first.
5. Resolve the responsible agent by `hermes_agents_list`, then use
   `hermes_conversation_assign(account_id, conversation_id, assignee_id)` only when
   requested. Account membership does not guarantee eligibility for every inbox.
6. Creating and assigning use the same external-write approval metadata as
   `hermes_messages_send`; respect the host's configured confirmation policy and
   the user's explicit authorization. The tools verify the conversation afterward.
   If the result is unconfirmed, read it again before repeating a write.
7. Sending a customer message is a separate authorized action through
   `hermes_messages_send`, after reading the conversation history. Do not treat
   creating or assigning an attendance as permission to send a message.

For file delivery, read [attendance and PDF delivery](references/attendance-pdf.md).
For direct API use, including a Genius fallback, follow the discovery workflow below.
Environment variables are one credential source outside Genius, not a prerequisite.

## Address, instances and credentials

- Each instance comes from your environment as a URL + token pair: a single one as
  `HERMES_URL` / `HERMES_TOKEN`, or several as `HERMES_<INSTANCE>_URL` /
  `HERMES_<INSTANCE>_TOKEN` (e.g. `PRODUCTION`, `DEVELOPMENT`). List the names, never the
  values: `env | grep -o '^HERMES_[A-Z_]*' | sort`. Never guess another host.
- Production and development are **separate servers**: different tokens, user ids and
  data. A request "in production and development" means doing the work twice, once per
  instance, and verifying each.
- Your personal token goes in `Authorization: Bearer <token>`. The `api_access_token`
  header is deprecated and some proxies reject it with 401.
- Never print, echo, log, commit or send the token. Pass it through an environment variable
  or a file, never inside a URL. When quoting it, mask it (`abcd…`).
- If no token is configured for the instance, follow [token onboarding](references/token-onboarding.md).
  Do not ask a person to paste one into a chat or end with only a Vault path.

## Discover before you call

Below, `$HERMES_URL` / `$HERMES_TOKEN` stand for the pair of the instance you are working on.

1. `GET $HERMES_URL/api` (public): `version`, plus the health of the queue and data
   services. Note the version; it tells you which spec you are reading.
2. `GET $HERMES_URL/swagger/swagger.json` (public, OpenAPI 3, ~450 KB): every route with
   method, summary, tags, parameters, request body and security scheme. **Ignore its
   `servers` entry** (it points to upstream Chatwoot); always use `$HERMES_URL`.
3. Search the document instead of reading all of it, e.g.:

   ```bash
   curl -fsS "$HERMES_URL/swagger/swagger.json" -o /tmp/hermes.json
   jq -r '.paths | to_entries[] | .key as $p | .value | to_entries[]
     | select(.value|type=="object") | "\(.key|ascii_upcase) \($p)  — \(.value.summary) [\(.value.tags|join(","))]"' /tmp/hermes.json \
     | grep -i 'profile'
   jq '.paths["/api/v1/profile"].put.requestBody' /tmp/hermes.json
   ```

   Without `jq`, the same search in Python:

   ```bash
   python3 - <<'PY'
   import json
   d = json.load(open('/tmp/hermes.json'))
   for path, ops in d['paths'].items():
       for method, op in ops.items():
           if isinstance(op, dict) and 'profile' in (path + str(op.get('summary'))).lower():
               print(method.upper(), path, '-', op.get('summary'), op.get('tags'))
   PY
   ```

   Resolve `$ref` values under `.components.schemas` to see payload fields.
4. Only then build the request. Missing documentation is not proof of missing access.
   Check relevant official server documentation or available source for an omitted field
   (such as attachments), recording the evidence. Never brute-force routes. If no
   supported contract can be found, report the precise documentation gap.

## Who am I

`GET $HERMES_URL/api/v1/profile` with your token returns your `id`, `name`, `email`,
`avatar_url` and the `accounts` you belong to (with `id` and `role`). Do this first on each
instance:

- It proves the token works (401 = invalid or expired token).
- It gives the `account_id` for every `/api/v1/accounts/{account_id}/…` route.
- It shows your role. An `agent` only sees the inboxes they were added to. An
  `administrator` sees the whole account. Do not take visibility as permission to act.

## Update your own profile and avatar

`PUT $HERMES_URL/api/v1/profile`:

- Text fields (`name`, `display_name`, `message_signature`…): JSON `{"profile": {...}}`.
- Avatar: `multipart/form-data` with the file in `profile[avatar]`:

  ```bash
  curl -fsS -X PUT "$HERMES_PRODUCTION_URL/api/v1/profile" \
    -H "Authorization: Bearer $HERMES_PRODUCTION_TOKEN" \
    -F "profile[avatar]=@avatar.png;type=image/png"
  ```

  Use a square JPG/PNG/WebP. Unless someone gives you another image, use your official
  Sufficit avatar: `SUFFICIT_AVATAR_URL` when set. Download it to a local file first
  (`curl -fsSL -D headers.txt "$SUFFICIT_AVATAR_URL" -o avatar.img`) and take the type
  from `Content-Type` in `headers.txt` (or `file avatar.img`); name the file with the matching
  extension (`.jpg`, `.png`, `.webp`) and pass that `type=` to curl.
- Verify: the response, or a new `GET /api/v1/profile`, must show a new `avatar_url`.
  Report success only after this check, per instance.

## Conversations and notes

- List and read: `GET /api/v1/accounts/{account_id}/conversations` (filters `status`,
  `assignee_type`, `inbox_id`, `page`) and `…/conversations/{id}/messages`. Big accounts
  hold 100k+ conversations: always filter and paginate, and stop when you have what you
  need. Never walk every page.
- **Private note** (visible only to agents): `POST …/conversations/{id}/messages` with
  `{"content": "…", "message_type": "outgoing", "private": true}`.
- **A public reply reaches the customer.** Never send one unless you were explicitly told
  to answer that customer in that conversation. Help agents with private notes by default.
- Do not change status, assignee, labels or teams of a conversation unless asked to.

## Reading responses

- 401 = token missing or invalid. 403 = your role does not allow it. 404 = wrong route,
  or a resource outside your account or inbox. 422 = invalid payload: read the `message`
  or `errors` field and fix the body.
- Lists usually come as `{"data": {"meta": …, "payload": [...]}}` or `{"payload": [...]}`.
  Check the shape in the spec before parsing.
- On writes, confirm the effect with a GET before telling anyone it is done.
