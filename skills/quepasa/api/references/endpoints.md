# QuePasa route reference

Source: QuePasa Swagger specification version `5.26.0922.1322` (55 paths) and the v5 canonical routes checked in the source code and the production gateway (version `5.26.0929.1644`). The values between `<…>` are examples; no token, key or real number appears here.

## Conventions

- Base: `$QUEPASA_URL`. Two surfaces coexist:
  - v5 canonical: `$QUEPASA_URL/api/v5/...` — preferred.
  - legacy (v4): `$QUEPASA_URL/api/...`, `$QUEPASA_URL/api/v4/...` and also at the root (`$QUEPASA_URL/...`). That's what Swagger describes.
- Session authentication: `X-QUEPASA-TOKEN` header (in v5 also accepted as `?token=` or `"token"` in the body — always prefer the header, so the token does not end up in URL log).
- User key: `X-QUEPASA-USERKEY`, only for account/session routes (`/api/v5/sessions`). View multiple sessions; see alerts in SKILL.md.
- In v5, common parameters are accepted by header, query or body:

| Parameter | Header | Query | Body |
| --- | --- | --- | --- |
| token | `X-QUEPASA-TOKEN` | `token` | `token` |
| group | `X-QUEPASA-GROUPID` | `groupid`, `groupId`, `group_jid` | `groupid`, `groupId`, `group_jid` |
| message | `X-QUEPASA-MESSAGEID` | `messageid`, `id` | `messageid`, `messageId`, `id` |
| chat | `X-QUEPASA-CHATID` | `chatid`, `chatId` | `chatid`, `chatId` |

- Standard answer: `{"success": bool, "status": "text", ...}`. `success:false` is flawed even with HTTP 200.

## Surface v5 (canonical)

### System (public, no token)

| Method | Route | Usage |
| --- | --- | --- |
| `GET` | `/api/v5/system/version` | running version |
| `GET` | `/api/v5/health` | health |

### Messages

| Method | Route | Usage |
| --- | --- | --- |
| `POST` | `/api/v5/messages` | send (`chatid`, `text`, `trackid`, `inreply`, `url`, `content`, `fileName`, `poll`, `location`, `contact`, `sticker`, `link`) |
| `GET` | `/api/v5/messages` | cache history; filters `messageid`, `chatid`, `type`, `category`, `search`, `fromme`, `fromhistory`, `trackid`, `timestamp`, `page`, `limit` (standard 50, max. 500) |
| `POST` | `/api/v5/messages/get` | a message by `messageid` |
| `PATCH` | `/api/v5/messages` | edit text (`messageid`, `text`) |
| `DELETE` | `/api/v5/messages` | revoke (`messageid`) |
| `POST` | `/api/v5/messages/retry` | redirect message to webhooks/queues |
| `POST` / `DELETE` | `/api/v5/messages/react` | react / remove reaction (`chatid`, `messageid`, `emoji`, `fromme`) |
| `POST` | `/api/v5/messages/poll/vote` | vote on a cached poll (`messageid`, `options` names case-insensitive and/or `indexes` 1-based; both empty removes the vote); response `options` = exact names voted. Same version note as pins |
| `GET` | `/api/v5/messages/pin?chatid=` | pins still in force in a chat (`pins[]`: `messageid`, `pinnedby`, `eventat`, `expiresat`); built from recorded pin events, same version note as below |
| `POST` | `/api/v5/messages/pin` | pin / unpin for everyone (`messageid`, `action` = `pin`\|`unpin`, `duration` = `86400`\|`604800`\|`2592000` seconds, default 7 days). Only in builds newer than 5.26.1016.2016; older ones answer a plain `404 page not found` |
| `POST` | `/api/v5/messages/links` | clickable link card (`chatid`, `url`, `text`, `title`, `description`) |
| `POST` | `/api/v5/messages/actions` | experimental buttons (1 to 3); WhatsApp Web shows only warning |
| `POST` | `/api/v5/messages/lid/direct` | direct text for a `…@lid` (test) |

### Groups

| Method | Route | Body / parameters |
| --- | --- | --- |
| `GET` | `/api/v5/groups` | lists the session groups |
| `POST` | `/api/v5/groups` | create: `{"title": "…", "participants": ["<jid>"]}` |
| `POST` | `/api/v5/groups/get` | details; `groupid` |
| `POST` | `/api/v5/groups/leave` | exit; `groupid` |
| `PUT` | `/api/v5/groups/name` | `{"group_jid": "…", "name": "…"}` |
| `PUT` | `/api/v5/groups/description` | `{"group_jid": "…", "topic": "…"}` |
| `PUT` | `/api/v5/groups/photo` | `{"group_jid": "…", "image_url": "…"}` or `{"remove_img": true}` |
| `PUT` | `/api/v5/groups/permissions` | `groupid` + `{"members_can_send_messages": bool, "members_can_edit_group_settings": bool}` (as omitted = unchanged) |
| `PUT` | `/api/v5/groups/participants` | `{"group_jid": "…", "action": "add"\|"remove"\|"promote"\|"demote", "participants": ["<jid>"]}` |
| `GET` | `/api/v5/groups/requests` | pending entry applications; `groupid` |
| `POST` | `/api/v5/groups/requests` | `{"group_jid": "…", "action": "approve"\|"reject", "participants": ["<jid>"]}` |
| `GET` / `POST` | `/api/v5/groups/invite` | current invitation link → `url` |
| `DELETE` | `/api/v5/groups/invite` | revoke link and return new |

There are no v5: `/api/v5/groups/getall`, `/api/v5/groups/create` (404) and `GET /api/v5/groups/get` (405, is `POST`). Those names are from the legacy surface.

### Media

| Method | Route | Usage |
| --- | --- | --- |
| `GET` | `/api/v5/media/messages?messageid=<id>` | media binary (includes vCard `text/x-vcard` shared contact) |
| `POST` | `/api/v5/media/messages/get` | idem with `messageid` in the body |
| `GET` | `/api/v5/media/pictures/info?chatid=<jid>` | profile/group photo |

`/api/v5/download` does not exist (404); the legacy is `/api/download?messageid=…`.

### Chats and contacts

| Method | Route | Usage |
| --- | --- | --- |
| `GET` | `/api/v5/chats` | Session conversations |
| `POST` | `/api/v5/chats/read`, `/api/v5/chats/unread` | mark as read/unread (`chatid`) |
| `POST` | `/api/v5/chats/archive` | `{"chatid": "…", "archive": bool}` |
| `POST` | `/api/v5/chats/presence` | "type"/"recording" (`chatid`, `type`, `duration`) |
| `GET` | `/api/v5/contacts` | contacts |
| `GET` | `/api/v5/contacts/identifier?phone=…` or `?lid=…` | convert phone ↔ LID |
| `POST` | `/api/v5/contacts/search` | `{"query": "…", "phone": "…"}` |
| `POST` | `/api/v5/contacts/get` | user information |
| `POST` | `/api/v5/contacts/availability` | What numbers have WhatsApp |
| `POST` / `DELETE` | `/api/v5/contacts/block` | block / unblock (`wid`) |
| `POST` | `/api/v5/contacts/save` | save contact |

### Dispatches (webhooks and queues)

| Method | Route | Usage |
| --- | --- | --- |
| `GET` / `POST` / `DELETE` | `/api/v5/dispatches/webhooks` | session webhooks |
| `GET` / `POST` / `DELETE` | `/api/v5/dispatches/rabbitmq` | RabbitMQ queues |

The form used in webhook production is the legacy `POST /webhook` with the session token (body `url`, `forwardinternal`, `trackid`, `extra`). There is no `/api/v5/webhooks` or `/api/v5/webhook`.

### Sessions (careful: affect number)

| Method | Route | Usage |
| --- | --- | --- |
| `GET` | `/api/v5/sessions` | list sessions visible to the user key — includes tokens |
| `POST` | `/api/v5/sessions/get` | one session (token) |
| `PUT` | `/api/v5/session/name`, `/api/v5/session/photo` | number profile |
| `POST` | `/api/v5/session/restart`, `/enable`, `/disable`, `/pair`; `GET` `/qrcode`, `/paircode` | Lifecycle — with explicit request only |
| `PATCH` / `DELETE` | `/api/v5/sessions` | change / delete session — with explicit request only |

## Legacy area (Swagger 5.26.0922.1322)

Routes related to `$QUEPASA_URL` (also valid with `/api` and `/api/v4` in front). `*` = mandatory. All use `X-QUEPASA-TOKEN`, except where indicated. Prefix exceptions: `/v5/...` lines only exist under `/api` (i.e. `/api/v5/...`) and `/api/settings/...` already brings the prefix. `/health` accepts `X-QUEPASA-USER`/`X-QUEPASA-PASSWORD` optional; `/api/settings/runtime-limits` is administrative.

### Environment

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/environment` | Get environment settings | — |

### Application

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `POST` | `/account` | Manage user accounts | body: `password`, `username` |
| `POST` | `/spam` | Send spam messages | body: `chatId`, `text` |

### Bot

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/command` | Execute bot commands | query `action`* |

### Chat

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `POST` | `/chat/archive` | Archive or unarchive chat | body: `archive`, `chatid` |
| `GET` | `/chat/lists` | Manage WhatsApp lists on one conversation | query `chatid`*; body: `chatid`, `listid` |
| `POST` | `/chat/lists` | Manage WhatsApp lists on one conversation | query `chatid`*; body: `chatid`, `listid` |
| `DELETE` | `/chat/lists` | Manage WhatsApp lists on one conversation | query `chatid`*; body: `chatid`, `listid` |
| `POST` | `/chat/markread` | Mark chat as read | body: `chatid` |
| `POST` | `/chat/markunread` | Mark chat as unread | body: `chatid` |
| `POST` | `/chat/presence` | Control chat presence | body: `chatid`, `duration`, `type` |
| `GET` | `/lists` | Manage WhatsApp lists | body: `color`, `id`, `listid`, `name` |
| `PUT` | `/lists` | Manage WhatsApp lists | body: `color`, `id`, `listid`, `name` |
| `POST` | `/lists` | Manage WhatsApp lists | body: `color`, `id`, `listid`, `name` |
| `DELETE` | `/lists` | Manage WhatsApp lists | body: `color`, `id`, `listid`, `name` |

### Connection

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/paircode` | Generate pairing code | query `phone`*; query `historysyncdays` |
| `GET` | `/scan` | Generate QR code | — |

### Settings

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/api/settings/runtime-limits` | Read global runtime limits | — |
| `PUT` | `/api/settings/runtime-limits` | Replace global runtime limits | body: `overrides` |
| `DELETE` | `/api/settings/runtime-limits` | Restore inherited runtime limits | — |

### Contacts

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `POST` | `/contact/save` | Save contact | body: `firstname`, `fullname`, `phone`, `synctophone` |
| `POST` | `/contact/search` | Search contacts | body: `has_lid`, `has_title`, `phone`, `query` |
| `GET` | `/contacts` | Get contacts | — |
| `POST` | `/contacts/block` | Block contact | body: `wid` |
| `DELETE` | `/contacts/block` | Unblock contact | body: `wid` |
| `POST` | `/isonwhatsapp` | Check WhatsApp registration | body: `phones` |
| `GET` | `/useridentifier` | Get user identifier (LID) | query `phone`; query `lid` |
| `POST` | `/userinfo` | Get user information | body: `jids` |

### Sending

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `POST` | `/messages/lid/direct` | Send text directly to @lid | body: `chatid`, `inreply`, `text`, `trackid` |
| `POST` | `/send` | Send any type of message (text, streamed file, poll, base64 content, location, contact, sticker, link) | body: `chatId`, `contact`, `content`, `fileName`, `link`, `location`, `poll`, `sticker`, `text`, `url` |
| `POST` | `/senddocument` | Send document with forced document type | body: `chatId`, `content`, `fileName`, `text`, `url` |
| `POST` | `/v5/messages/actions` | Send an experimental WhatsApp action message | body: `actions`, `chatid`, `footer`, `id`, `text`, `title`, `trackid` |
| `POST` | `/v5/messages/links` | Send a cross-client clickable link card | body: `chatid`, `description`, `id`, `text`, `title`, `trackid`, `url` |

### Groups

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `POST` | `/groups/create` | Create a new group | body: `participants`, `title` |
| `PUT` | `/groups/description` | Set group topic | body: `group_jid`, `topic` |
| `GET` | `/groups/get` | Get group information | query `groupId`* |
| `GET` | `/groups/getall` | Get all groups | — |
| `GET` | `/groups/invite` | Get group invite link | query `groupId`* |
| `DELETE` | `/groups/invite` | Revoke group invite link | query `groupId`* |
| `POST` | `/groups/leave` | Leave group | body: `chatId` |
| `PUT` | `/groups/name` | Set group name | body: `group_jid`, `name` |
| `PUT` | `/groups/participants` | Update group participants | body: `action`, `group_jid`, `participants` |
| `PUT` | `/groups/photo` | Set/Remove group photo | body: `group_jid`, `remove_img` |
| `GET` | `/groups/requests` | Handle group join requests | body: `action`, `group_jid`, `participants`; query `group_jid` |
| `POST` | `/groups/requests` | Handle group join requests | body: `action`, `group_jid`, `participants`; query `group_jid` |
| `GET` | `/invite` | Generate group invite link | query `chatid` |
| `GET` | `/invite/{chatid}` | Generate group invite link | path `chatid`; query `chatid` |
| `PUT` | `/v5/groups/permissions` | Update group permissions | header `X-QUEPASA-TOKEN`*; header `X-QUEPASA-GROUPID`*; body: `members_can_edit_group_settings`, `members_can_send_messages` |

### Message

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `PUT` | `/edit` | Edit message | body: `content`, `messageId` |
| `GET` | `/message/{messageid}` | Get message | path `messageid`* |
| `DELETE` | `/message/{messageid}` | Revoke message | path `messageid`* |
| `POST` | `/messages/react` | Send message reaction | body: `chatid`, `emoji`, `fromme`, `messageid` |
| `DELETE` | `/messages/react` | Remove message reaction | body: `chatid`, `emoji`, `fromme`, `messageid` |
| `POST` | `/read` | Mark messages as read | body: JSON |
| `GET` | `/receive` | Receive messages | query `timestamp`; query `exceptions`; query `type`; query `category`; query `search`; query `fromme`; query `fromhistory`; query `chatid`; query `messageid`; query `trackid`; query `page`; query `limit` |
| `POST` | `/redispatch/{messageid}` | Re-dispatch message | path `messageid`* |

### Media

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/download` | Download media | query `messageid`; query `cache` |

### RabbitMQ

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/rabbitmq` | Manage RabbitMQ configurations | body: `connection_string`, `exchange`, `routing_key`; query `connection_string` |
| `POST` | `/rabbitmq` | Manage RabbitMQ configurations | body: `connection_string`, `exchange`, `routing_key`; query `connection_string` |
| `DELETE` | `/rabbitmq` | Manage RabbitMQ configurations | body: `connection_string`, `exchange`, `routing_key`; query `connection_string` |

### Restoration

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/restore` | Diagnose orphan WhatsApp sessions | — |
| `POST` | `/restore/auto` | Automatically restore one unambiguous orphan session | — |
| `POST` | `/restore/manual` | Manually restore one session link | body: `jid`, `token` |

### Health

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/health` | Health check with optional authentication | header `X-QUEPASA-USER`; header `X-QUEPASA-PASSWORD` |

### Session

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `PUT` | `/session/name` | Set session profile name | body: `name`, `token` |
| `PUT` | `/session/photo` | Set/Remove session profile photo | body: `content`, `image_url`, `remove_img`, `token` |

### Session (info)

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/info` | Get bot information | — |
| `POST` | `/info` | Create bot configuration | body: `broadcasts`, `calls`, `contextid`, `deliveryreceipts`, `devel`, `direct`, `groups`, `messages`, `presence`, `readreceipts`, `readupdate`, `sip_register_enabled`, `sip_register_password` |
| `DELETE` | `/info` | Delete bot information | — |
| `PATCH` | `/info` | Update bot information | body: `settings` |

### Status

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `POST` | `/status/publish` | Publish WhatsApp status | body: `attachment`, `text` |

### Webhooks

| Method | Route | Summary | Parameters |
| --- | --- | --- | --- |
| `GET` | `/webhook` | Manage webhook configurations | body: `bearer_token`, `failure_bearer_token`, `failure_method`, `failure_url`, `method`, `url` |
| `POST` | `/webhook` | Manage webhook configurations | body: `bearer_token`, `failure_bearer_token`, `failure_method`, `failure_url`, `method`, `url` |
| `DELETE` | `/webhook` | Manage webhook configurations | body: `bearer_token`, `failure_bearer_token`, `failure_method`, `failure_url`, `method`, `url` |
