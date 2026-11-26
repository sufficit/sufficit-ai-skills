# Chats and conversation history

QuePasa 5.26.1125.1212, canonical API v5.

## Behaviors

- `GET /chats` derives a paginated list from stored messages for ordinary direct chats (`@s.whatsapp.net`). It excludes WhatsApp group JIDs even if messages for them exist. Read joined groups separately with `GET /groups` and merge `chats[].chat_id` with `groups[].JID` if the consumer needs a combined conversation list.
- Missing history may also leave a direct chat absent. Normalize a null chats array or an omitted group array to an empty array before joining results.

### List the first page of stored direct chats

```bash
curl --fail-with-body --silent --show-error "$QUEPASA_API/chats?page=1&limit=50" \
  -H "X-QUEPASA-USERKEY: $QUEPASA_USER_KEY" \
  -H "X-QUEPASA-TOKEN: $QUEPASA_SESSION_TOKEN" | jq '(.chats // [])[] | {chat_id, title}'
```

Repeat with successive pages as needed. Use the [groups reference](groups.md) for joined groups.

## Operations

### `DELETE /api/v5/chats/lists`

Apply or remove a WhatsApp list assignment.

- Unversioned alias `DELETE /api/chats/lists` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and chat/list identifiers.
- HTTP 200. `api.ConversationListsResponse`.

### `GET /api/v5/chats`

List stored direct chats for one session, newest first.

- Unversioned alias `GET /api/chats` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token. Query page (default 1), limit (default 50, max 200), search.
- HTTP 200. `Chats`.

### `GET /api/v5/me/chats`

Aggregate stored direct chats across owned sessions.

- Unversioned alias `GET /api/me/chats` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Query page, limit and search.
- HTTP 200. `UserChats`.

### `POST /api/v5/chats/archive`

Archive or unarchive a chat.

- Unversioned alias `POST /api/chats/archive` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, JSON chatid and archive flag.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/chats/lists`

Apply or remove a WhatsApp list assignment.

- Unversioned alias `POST /api/chats/lists` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and chat/list identifiers.
- HTTP 200. `api.ConversationListsResponse`.

### `POST /api/v5/chats/lists/get`

Read WhatsApp list assignments for a chat.

- Unversioned alias `POST /api/chats/lists/get` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and chatid.
- HTTP 200. `api.ConversationListsResponse`.

### `POST /api/v5/chats/presence`

Set chat typing or other presence.

- Unversioned alias `POST /api/chats/presence` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, JSON chatid and presence.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/chats/read`

Mark a chat as read.

- Unversioned alias `POST /api/chats/read` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and chatid.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/chats/unread`

Mark a chat as unread.

- Unversioned alias `POST /api/chats/unread` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and chatid.
- HTTP 200. `models.QpResponse`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### Chat

| Field | Type | Presence |
| --- | --- | --- |
| `chat_id` | string | Required |
| `title` | string | Optional |
| `phone` | string | Optional |
| `lid` | string | Optional |
| `last_text` | string | Optional |
| `last_id` | string | Optional |
| `last_fromme` | boolean | Required |
| `timestamp` | date-time | Required |
| `total` | integer | Required |

### Chats

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `total` | integer | Required |
| `page` | integer | Required |
| `limit` | integer | Required |
| `chats` | Array of `Chat` or null | Required |

### UserChat

`Chat`

| Field | Type | Presence |
| --- | --- | --- |
| `token` | string | Required |
| `session_id` | string | Optional |
| `wid` | string | Optional |

### UserChats

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `total` | integer | Required |
| `page` | integer | Required |
| `limit` | integer | Required |
| `chats` | Array of `UserChat` | Required |

### api.ConversationListsResponse

| Field | Type | Presence |
| --- | --- | --- |
| `affected` | integer | Unspecified |
| `chatid` | string | Unspecified |
| `debug` | Array of string | Unspecified |
| `list` | `whatsapp.WhatsappChatList` | Unspecified |
| `lists` | Array of `whatsapp.WhatsappChatList` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `syncing` | boolean | Unspecified |

### models.QpResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### whatsapp.WhatsappChatList

| Field | Type | Presence |
| --- | --- | --- |
| `active` | boolean | Unspecified |
| `id` | string | Unspecified |
| `name` | string | Unspecified |
