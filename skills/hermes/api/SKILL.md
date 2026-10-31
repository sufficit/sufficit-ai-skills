---
name: hermes-api
description: "Use the Hermes HTTP API (Sufficit's Chatwoot-based helpdesk) as your own user: discover the live API from the server's OpenAPI document instead of memorizing routes, authenticate with your personal token (Authorization Bearer), confirm who and which account you are, update your own profile and avatar, read conversations and post private notes. Use when a request mentions Hermes, Chatwoot, helpdesk profile/avatar, conversations, inboxes, contacts or notes, in production or development."
metadata:
  version: "0.1.0"
---

# Hermes API

Hermes is Sufficit's helpdesk, built on Chatwoot and extended. Routes change between
releases, so **this skill teaches how to discover the API, not a frozen list of routes**.
The server's own OpenAPI document is the source of truth; when it disagrees with this
text, follow the document.

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

   Resolve `$ref` values under `.components.schemas` to see payload fields.
4. Only then build the request. If a route is missing from the spec, it probably does not
   exist in this version. Report that instead of trying variations against production.

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
  (`curl -fsSL "$SUFFICIT_AVATAR_URL" -o avatar.img`, then check the type with `file`).
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
