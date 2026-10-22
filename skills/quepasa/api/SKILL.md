---
name: quepasa-api
description: "Use the QuePasa HTTP API (gateway WhatsApp in Go) the right way — send text and media, manage groups (create, attendees, name, description, invitations and requests for entry), download shared media and contacts, check history and configure/interpret webhooks — with the session token (X-QUEPASA-TOKEN) and never the user key outside your scope. Use when the request involves QuePasa, WhatsApp via gateway, WhatsApp groups, Hermes/Chatwoot message or integration webhooks with QuePasa."
metadata:
  version: "0.1.2"
---

# QuePasa API

QuePasa exposes a WhatsApp session (one number) per token. This skill teaches the routes that work in production, correct authentication and the known production pitfalls. The complete route reference is in [references/endpoints.md](references/endpoints.md) and webhook format in [references/webhook-payload.md](references/webhook-payload.md).

## Address and credentials

- `QUEPASA_URL` is the gateway base URL (without a trailing slash). Never invent another; use the configured one in the agent environment.
- `GET $QUEPASA_URL/api/v5/system/version` and `GET /api/v5/health` are public: use them to confirm that the gateway responds and which version is running.
- Session token — header `X-QUEPASA-TOKEN: <token>`. Identifies one number. It is the default credential for everything: upload, groups, media, webhook.
- User key — `X-QUEPASA-USERKEY: <key>` header. See several sessions (of various numbers/clients) and `GET /api/v5/sessions` even returns their tokens. It is powerful: use it only for the purpose and session for which it was delivered, never to read, send or change other sessions, and never to "discover" someone else's token.
- Never show token or key in response, log, echoed command, file, issue or message. When quoting, mask (`abcd…`). Don't stick the list of raw sessions in the conversation.

## Rules for reading answers

- Every response has `success` (bool) and `status` (text). `success: false` is flawed even with HTTP 200 — read `status` and report the real reason.
- 401 = missing/invalid token for route; 404 = missing route (check prefix); 405 = wrong method (e.g. `GET /api/v5/groups/get`, which is `POST`).
- Successful delivery brings `message.id`: store it to respond (`inreply`), react, edit or revoke.

## Identifiers (JID)

- Person: `<digits-with-country-code>@s.whatsapp.net` (e.g. `5511999999999@s.whatsapp.net`).
- Group: `<id>@g.us`.
- LID (new WhatsApp opaque identifier): `<number>@lid`. Convert with `GET /api/v5/contacts/identifier?phone=…` or `?lid=…` when needed.

## Send message

`POST $QUEPASA_URL/api/v5/messages` with `X-QUEPASA-TOKEN`:

```json
{ "chatid": "<jid>", "text": "Hello!", "trackid": "my-system", "inreply": "<optional-id>" }
```

- `chatid` is the group (`…@g.us`) or the person (`…@s.whatsapp.net`).
- `trackid` identifies the system you sent; webhook returns this value and allows you to ignore the echo itself (prevents bot loops).
- File: same endpoint with `url` (downloaded by the server) or `content` (`data:<mime>;base64,…`) and `fileName`; view fields `poll`, `location`, `contact`, `sticker`, `link` in reference.
- Confirm `success: true` before telling the user it was sent.

## Pin a message

`POST $QUEPASA_URL/api/v5/messages/pin` with `X-QUEPASA-TOKEN` pins (or unpins) a message for everyone in its chat:

```json
{ "messageid": "<id>", "action": "pin", "duration": 604800 }
```

- `action` is `pin` (default) or `unpin`. `duration` is in seconds and must be `86400` (24 h), `604800` (7 days, default) or `2592000` (30 days); it is ignored when unpinning.
- Only `messageid` identifies the message: it must be in this session's cache (sent or received). The chat and the author come from the cache.
- In groups the session may need to be an admin, depending on the group's settings; WhatsApp's refusal comes back as `success: false`.
- The route exists only in builds newer than `5.26.1016.2016`. An older gateway answers a plain `404 page not found`: report that the gateway needs an update, not that the message or group is missing. Check `GET /api/v5/system/version` when in doubt.

## Administer groups

All with `X-QUEPASA-TOKEN`; the session needs to be group admin to change. The group goes in `?groupid=<jid@g.us>` and/or in the body as `group_jid`.

| Action | Route v5 |
| --- | --- |
| List session groups | `GET /api/v5/groups` |
| Create | `POST /api/v5/groups` `{"title":"…","participants":["<jid>",…]}` |
| Details | `POST /api/v5/groups/get?groupid=…` |
| Participants | `PUT /api/v5/groups/participants` `{"group_jid":"…","action":"add\|remove\|promote\|demote","participants":[…]}` |
| Name | `PUT /api/v5/groups/name` `{"group_jid":"…","name":"…"}` |
| Description | `PUT /api/v5/groups/description` `{"group_jid":"…","topic":"…"}` |
| Photo | `PUT /api/v5/groups/photo` `{"group_jid":"…","image_url":"…"}` or `"remove_img":true` |
| Permissions | `PUT /api/v5/groups/permissions?groupid=…` `{"members_can_send_messages":bool,"members_can_edit_group_settings":bool}` |
| Invitation link | `GET /api/v5/groups/invite?groupid=…` → `url` |
| Revoke link | `DELETE /api/v5/groups/invite?groupid=…` (returns the new) |
| Pedidos de entrada | `GET /api/v5/groups/requests?groupid=…`; aprovar/recusar com `POST` `{"group_jid":"…","action":"approve\|reject","participants":[…]}` |
| Quit | `POST /api/v5/groups/leave?groupid=…` |

The old surface (without `v5`) remains active and uses other names: `GET /api/groups/getall`, `GET /api/groups/get?groupId=…`, `POST /api/groups/create`. Do not mix: `/api/v5/groups/getall` and `/api/v5/groups/create` do not exist (404).

### Invite people

Direct Add (`action: add`) may fail for contact privacy. The preferred pattern is to send the invitation link in private to each person:

1. `GET /api/v5/groups/invite?groupid=<group>` → `url`.
2. For each person, `POST /api/v5/messages` with `chatid` = `<digits>@s.whatsapp.net` and a short text with the link.
3. If the group requires approval, follow `GET /api/v5/groups/requests` and approve only those invited.

Never publish the link in a group of others or public channel; revoke it if it leaks.

## Media, shared and historical contacts

- Download media from a message: `GET /api/v5/media/messages?messageid=<id>` returns the binary with the original `Content-Type`. The old route `/api/v5/download` does not exist (404).
- Shared contact (`type: "contact"`): the webhook text only brings the displayed name; the full vCard (`text/x-vcard`, with the phone) comes through the same media route.
- See message/historical: `GET /api/v5/messages?messageid=<id>` (also accepted `chatid`, `type`, `fromme`, `search`, `page`, `limit`); an exact message: `POST /api/v5/messages/get?messageid=<id>`.

## Webhooks

- Configure with session token: `POST $QUEPASA_URL/webhook` (legacy, without a prefix) with `{"url":"https://…","forwardinternal":false,"trackid":"…"}`; `GET /webhook` list and `DELETE /webhook` removes. There is no `/api/v5/webhooks`; the equivalent v5 is `/api/v5/dispatches/webhooks`.
- Payload useful fields: `id`, `chat.id`, `text`, `type`, `fromme`, `frominternal`, `fromhistory`, `timestamp`, `participant`, `attachment`, `wid`. Details and types in [references/webhook-payload.md](references/webhook-payload.md).
- `wid` is the session number itself (e.g. `<digits>:48@s.whatsapp.net`). In group, a `@<wid-digits>` mention in `text` is someone talking to the bot.
- Ignore `fromme: true`/`frominternal: true` when deciding to respond, so as not to talk to yourself.

## Traps (lived in production)

- Restart the QuePasa service disconnects all sessions for a few moments (all numbers, all customers). Never restart to "test"; if inevitable, it is a human decision during an agreed maintenance window.
- Never test with a copy of a real session: two clients using the same session make WhatsApp take down the legitimate (`stream_replaced`). Use a test session of your own.
- `success: false` with HTTP 200 is error — never report success without `success: true`.
- Route v5 with legacy name (`getall`, `create`, `download`) → 404; check out the table before trying blind variations.
- Do not create, delete, pair (`/session/pair`, QR code) or disable sessions without explicit request: this affects someone's production number.
- Do not use the user key to bypass a 401 session token.
