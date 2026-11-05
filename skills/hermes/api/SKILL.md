---
name: hermes-api
description: "Complete authorized Hermes helpdesk requests from ordinary language: locate the customer or WhatsApp group, open an attendance, send text and PDF attachments, and verify the result. Discover the live API and use the connected user's Identity Vault token when a ready-made tool is missing. Also manage your own profile/avatar and private notes. Do not infer lack of access from missing tools or environment variables."
metadata:
  version: "0.3.0"
---

# Hermes API

Hermes is Sufficit's helpdesk, built on Chatwoot and extended. Routes change between
releases, so **this skill teaches how to discover the API, not a frozen list of routes**.
The server's own OpenAPI document is the source of truth; when it disagrees with this
text, follow the document.

## Genius: use the connected Hermes tools first

When running inside Genius with `hermes_*` tools, the plugin resolves the personal
API token from Identity Vault (`personal/hermes/production/api-token`). The absence
of `HERMES_*` environment variables does not mean the connected account is missing.
Use `hermes_connection_test` to obtain the authenticated account IDs. A successful
check is evidence that credentials work; preserve that evidence for subsequent steps.
Missing specialized tools do not mean missing API access. Discover/activate the exact
`hermes_*` tool first; if unavailable or lacking a required field, continue through
[the API/Vault fallback](references/connected-execution.md). This fallback is also
for Genius, not only external scripts. Respect actual permission denials.

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
- If no token is configured for the instance, say so plainly. Do not ask a person to paste
  one into a chat.

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
