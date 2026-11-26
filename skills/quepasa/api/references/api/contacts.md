# Contacts and identity resolution

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `DELETE /api/v5/contacts/block`

Block or unblock a WhatsApp contact.

- Unversioned alias `DELETE /api/contacts/block` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.BlockContactRequest JSON.
- Request schemas. `api.BlockContactRequest`.
- HTTP 200. `models.QpResponse`.

### `GET /api/v5/contacts`

List contacts available to a linked session.

- Unversioned alias `GET /api/contacts` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and optional search filters.
- HTTP 200. `api.ContactsResponse`.

### `GET /api/v5/contacts/identifier`

Resolve a WhatsApp contact identifier.

- Unversioned alias `GET /api/contacts/identifier` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and either phone or lid.
- HTTP 200. `ContactIdentifier`.

### `POST /api/v5/contacts/availability`

Check WhatsApp registration for phone numbers.

- Unversioned alias `POST /api/contacts/availability` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and JSON phone numbers.
- HTTP 200. `api.IsOnWhatsAppResponse`.

### `POST /api/v5/contacts/block`

Block or unblock a WhatsApp contact.

- Unversioned alias `POST /api/contacts/block` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.BlockContactRequest JSON.
- Request schemas. `api.BlockContactRequest`.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/contacts/get`

Look up WhatsApp contacts.

- Unversioned alias `POST /api/contacts/get` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and api.ContactSearchRequest JSON.
- Request schemas. `api.ContactSearchRequest`.
- HTTP 200. `api.ContactsResponse`.

### `POST /api/v5/contacts/save`

Save a WhatsApp contact.

- Unversioned alias `POST /api/contacts/save` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.ContactSaveRequest JSON.
- Request schemas. `api.ContactSaveRequest`.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/contacts/search`

Search WhatsApp contacts.

- Unversioned alias `POST /api/contacts/search` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and api.ContactSearchRequest JSON.
- Request schemas. `api.ContactSearchRequest`.
- HTTP 200. `api.ContactsResponse`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### ContactIdentifier

`Response`

| Field | Type | Presence |
| --- | --- | --- |
| `phone` | string | Optional |
| `lid` | string | Optional |

### Response

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `status` | string | Optional |
| `debug` | Array of string | Optional |

### api.BlockContactRequest

| Field | Type | Presence |
| --- | --- | --- |
| `wid` | string | Unspecified |

### api.ContactSaveRequest

| Field | Type | Presence |
| --- | --- | --- |
| `firstname` | string | Unspecified |
| `fullname` | string | Unspecified |
| `phone` | string | Unspecified |
| `synctophone` | boolean | Unspecified |

### api.ContactSearchRequest

| Field | Type | Presence |
| --- | --- | --- |
| `has_lid` | boolean | Unspecified |
| `has_title` | boolean | Unspecified |
| `phone` | string | Unspecified |
| `query` | string | Unspecified |

### api.ContactsResponse

| Field | Type | Presence |
| --- | --- | --- |
| `contacts` | Array of `whatsapp.WhatsappChat` | Unspecified |
| `debug` | Array of string | Unspecified |
| `lists_syncing` | boolean | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `total` | integer | Unspecified |

### api.IsOnWhatsAppResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `registered` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `total` | integer | Unspecified |

### models.QpResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

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
