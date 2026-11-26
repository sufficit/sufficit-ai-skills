# Conversation lists

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `DELETE /api/v5/lists`

Delete a conversation list.

- Unversioned alias `DELETE /api/lists` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and list ID.
- HTTP 200. `api.ConversationListsResponse`.

### `GET /api/v5/lists`

List WhatsApp conversation labels and their chat assignments.

- Unversioned alias `GET /api/lists` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token.
- HTTP 200. `api.ConversationListsWithContactsResponse`.

### `PATCH /api/v5/lists`

Update a conversation list.

- Unversioned alias `PATCH /api/lists` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token plus JSON list ID and changed attributes.
- HTTP 200. `api.ConversationListsResponse`.

### `POST /api/v5/lists`

Create or rename a conversation list.

- Unversioned alias `POST /api/lists` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token plus JSON list attributes.
- HTTP 200. `api.ConversationListsResponse`.

### `POST /api/v5/lists/search`

Search or aggregate conversation lists across visible sessions.

- Unversioned alias `POST /api/lists/search` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. JSON token (required), query, active, chatIds and includeChats. assignedChats maps each list ID to its matched chat IDs.
- Request schemas. `ListSearchRequest`.
- HTTP 200. `ListSearch`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### ListSearch

| Field | Type | Presence |
| --- | --- | --- |
| `lists` | Array of `whatsapp.WhatsappChatList` | Required |
| `total` | integer | Required |
| `query` | string | Required |
| `assignedChats` | Array of Map of string | Optional |

### ListSearchRequest

| Field | Type | Presence |
| --- | --- | --- |
| `token` | string | Required |
| `query` | string | Optional |
| `active` | boolean | Optional |
| `chatIds` | Array of string | Optional |
| `includeChats` | boolean | Optional |

### api.ConversationListWithContacts

| Field | Type | Presence |
| --- | --- | --- |
| `active` | boolean | Unspecified |
| `contacts` | Array of `whatsapp.WhatsappChat` | Unspecified |
| `id` | string | Unspecified |
| `name` | string | Unspecified |
| `total` | integer | Unspecified |

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

### api.ConversationListsWithContactsResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `lists` | Array of `api.ConversationListWithContacts` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `syncing` | boolean | Unspecified |

### whatsapp.WhatsappChat

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Unspecified |
| `lid` | string | Unspecified |
| `lists` | Array of `whatsapp.WhatsappChatList` | Unspecified |
| `name` | `whatsapp.WhatsappContactName` | Unspecified |
| `phone` | string | Unspecified |
| `title` | string | Unspecified |

### whatsapp.WhatsappChatList

| Field | Type | Presence |
| --- | --- | --- |
| `active` | boolean | Unspecified |
| `id` | string | Unspecified |
| `name` | string | Unspecified |

### whatsapp.WhatsappContactName

| Field | Type | Presence |
| --- | --- | --- |
| `businessName` | string | Unspecified |
| `display` | string | Unspecified |
| `firstName` | string | Unspecified |
| `fullName` | string | Unspecified |
| `pushName` | string | Unspecified |
| `source` | string | Unspecified |
| `username` | string | Unspecified |
