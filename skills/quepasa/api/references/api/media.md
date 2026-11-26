# Media and profile pictures

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `GET /api/v5/media/messages`

Download stored message media.

- Unversioned alias `GET /api/media/messages` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and messageid.
- HTTP 200. binary.

### `GET /api/v5/media/pictures/info`

Inspect profile picture metadata.

- Unversioned alias `GET /api/media/pictures/info` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token, chatid and optional pictureid.
- HTTP 200. `Picture`.

### `POST /api/v5/media/download`

Retrieve media from WhatsApp into local message storage.

- Unversioned alias `POST /api/media/download` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and messageid. Use a message-media route to retrieve bytes.
- HTTP 200. `DownloadResult`.

### `POST /api/v5/media/messages/get`

Download stored message media with JSON selectors.

- Unversioned alias `POST /api/media/messages/get` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and messageid.
- HTTP 200. binary.

### `POST /api/v5/media/pictures/get`

Inspect profile picture metadata with a JSON target.

- Unversioned alias `POST /api/media/pictures/get` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token, chatid and optional pictureid.
- HTTP 200. `Picture`.

### `POST /api/v5/media/pictures/info`

Inspect profile picture metadata with a JSON target.

- Unversioned alias `POST /api/media/pictures/info` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token, chatid and optional pictureid.
- HTTP 200. `Picture`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### DownloadResult

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `id` | string | Required |

### Picture

`Response`

| Field | Type | Presence |
| --- | --- | --- |
| `info` | `PictureInfo` | Optional |

### PictureInfo

| Field | Type | Presence |
| --- | --- | --- |
| `url` | string | Optional |
| `id` | string | Optional |
| `type` | string | Optional |
| `chatid` | string | Optional |
| `wid` | string | Optional |

### Response

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `status` | string | Optional |
| `debug` | Array of string | Optional |
