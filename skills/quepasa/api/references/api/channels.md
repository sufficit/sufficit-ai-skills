# WhatsApp channels

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `DELETE /api/v5/channels/follow`

Follow or unfollow a channel.

- Unversioned alias `DELETE /api/channels/follow` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and channel identifier.
- HTTP 200. `api.ChannelActionResponse`.

### `GET /api/v5/channels`

List followed WhatsApp channels.

- Unversioned alias `GET /api/channels` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token.
- HTTP 200. `api.ChannelListResponse`.

### `GET /api/v5/channels/info`

Inspect a channel by JID or invite.

- Unversioned alias `GET /api/channels/info` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and jid or invite query.
- HTTP 200. `api.ChannelInfoResponse`.

### `POST /api/v5/channels`

Create a channel.

- Unversioned alias `POST /api/channels` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.ChannelRequest JSON.
- Request schemas. `api.ChannelRequest`.
- HTTP 200. `api.ChannelInfoResponse`.

### `POST /api/v5/channels/follow`

Follow or unfollow a channel.

- Unversioned alias `POST /api/channels/follow` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and channel identifier.
- HTTP 200. `api.ChannelActionResponse`.

### `POST /api/v5/channels/messages`

Publish text in an owned or administered channel.

- Unversioned alias `POST /api/channels/messages` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.ChannelRequest JSON.
- Request schemas. `api.ChannelRequest`.
- HTTP 200. `api.ChannelPublicationResponse`.

### `PUT /api/v5/channels/mute`

Change a channel mute setting.

- Unversioned alias `PUT /api/channels/mute` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, channel identifier and JSON mute flag.
- HTTP 200. `api.ChannelActionResponse`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### api.ChannelActionResponse

| Field | Type | Presence |
| --- | --- | --- |
| `channel_id` | string | Unspecified |
| `following` | boolean | Unspecified |
| `muted` | boolean | Unspecified |

### api.ChannelInfoResponse

| Field | Type | Presence |
| --- | --- | --- |
| `channel` | `whatsapp.WhatsappChannel` | Unspecified |

### api.ChannelListResponse

| Field | Type | Presence |
| --- | --- | --- |
| `channels` | Array of `whatsapp.WhatsappChannel` | Unspecified |
| `total` | integer | Unspecified |

### api.ChannelPublicationResponse

| Field | Type | Presence |
| --- | --- | --- |
| `channel_id` | string | Unspecified |
| `message_id` | string | Unspecified |
| `timestamp` | integer | Unspecified |

### api.ChannelRequest

| Field | Type | Presence |
| --- | --- | --- |
| `channel_id` | string | Unspecified |
| `description` | string | Unspecified |
| `invite` | string | Unspecified |
| `message_id` | string | Unspecified |
| `muted` | boolean | Unspecified |
| `name` | string | Unspecified |
| `text` | string | Unspecified |
| `token` | string | Unspecified |

### whatsapp.WhatsappChannel

| Field | Type | Presence |
| --- | --- | --- |
| `can_publish` | boolean | Unspecified |
| `description` | string | Unspecified |
| `id` | string | Unspecified |
| `invite` | string | Unspecified |
| `muted` | boolean | Unspecified |
| `name` | string | Unspecified |
| `role` | string | Unspecified |
| `state` | string | Unspecified |
| `subscribers` | integer | Unspecified |
