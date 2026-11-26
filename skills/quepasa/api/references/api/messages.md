# Messages and WhatsApp Status

QuePasa 5.26.1125.1212, canonical API v5.

## Behaviors

- Send with JSON for text and structured messages or `multipart/form-data` with `file` for streamed media. Use a unique `Idempotency-Key` for retryable sends and preserve it only for the same logical operation. A send timeout can leave delivery unconfirmed. Check message state before resending.
- Status media is a single JPEG, PNG, MP4, GIF, MP3, WAV or Ogg file up to 16 MB. Photos, video and GIF can carry text. Voice status is limited to 30 seconds and has no caption. The session token selects the account whose configured Status audience is used.

## Operations

### `DELETE /api/v5/messages`

Revoke a WhatsApp message.

- Unversioned alias `DELETE /api/messages` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and messageid.
- HTTP 200. `models.QpResponse`.

### `DELETE /api/v5/messages/react`

Add or remove a message reaction.

- Unversioned alias `DELETE /api/messages/react` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.ReactionRequest JSON.
- Request schemas. `api.ReactionRequest`.
- HTTP 200. `models.QpResponse`.

### `GET /api/v5/me/messages`

List stored messages across owned sessions.

- Unversioned alias `GET /api/me/messages` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Query page, limit, chatid and search.
- HTTP 200. `UserMessages`.

### `GET /api/v5/messages`

List stored messages for one session.

- Unversioned alias `GET /api/messages` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token. Query chatid and history/pagination filters.
- HTTP 200. `api.ReceiveResponse`.

### `GET /api/v5/messages/pin`

List pins for a WhatsApp chat.

- Unversioned alias `GET /api/messages/pin` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and chatid.
- HTTP 200. `api.PinListResponse`.

### `PATCH /api/v5/messages`

Edit a sent message.

- Unversioned alias `PATCH /api/messages` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, messageid and updated text.
- HTTP 200. `EditResult`.

### `POST /api/v5/messages`

Send text, media or other supported content.

- Unversioned alias `POST /api/messages` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and target chatid. JSON or multipart file. See send behavior.
- HTTP 200. `api.SendResponse`.

### `POST /api/v5/messages/actions`

Send an experimental WhatsApp action message.

- Unversioned alias `POST /api/messages/actions` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.SendActionRequest JSON.
- Request schemas. `api.SendActionRequest`.
- HTTP 200. `api.SendResponse`.

### `POST /api/v5/messages/get`

Read a stored message by its provider ID.

- Unversioned alias `POST /api/messages/get` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token and messageid.
- HTTP 200. `api.MessageResponse`.

### `POST /api/v5/messages/interactive`

Send an interactive message.

- Unversioned alias `POST /api/messages/interactive` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.SendInteractiveRequest JSON.
- Request schemas. `api.SendInteractiveRequest`.
- HTTP 200. `api.SendResponse`.

### `POST /api/v5/messages/lid/direct`

Send text directly to a WhatsApp LID.

- Unversioned alias `POST /api/messages/lid/direct` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.LIDDirectSendRequest JSON.
- Request schemas. `api.LIDDirectSendRequest`.
- HTTP 200. `api.SendResponse`.

### `POST /api/v5/messages/links`

Send a clickable link card.

- Unversioned alias `POST /api/messages/links` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.SendLinkRequest JSON.
- Request schemas. `api.SendLinkRequest`.
- HTTP 200. `api.SendResponse`.

### `POST /api/v5/messages/pin`

Pin or unpin a WhatsApp message.

- Unversioned alias `POST /api/messages/pin` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, messageid and api.PinRequest JSON.
- Request schemas. `api.PinRequest`.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/messages/poll/vote`

Vote on a WhatsApp poll.

- Unversioned alias `POST /api/messages/poll/vote` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token, messageid and api.PollVoteRequest JSON.
- Request schemas. `api.PollVoteRequest`.
- HTTP 200. `api.PollVoteResponse`.

### `POST /api/v5/messages/react`

Add or remove a message reaction.

- Unversioned alias `POST /api/messages/react` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and api.ReactionRequest JSON.
- Request schemas. `api.ReactionRequest`.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/messages/retry`

Re-dispatch a previously stored message through configured transports.

- Unversioned alias `POST /api/messages/retry` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and messageid.
- HTTP 200. `models.QpResponse`.

### `POST /api/v5/status/publish`

Publish a WhatsApp Status.

- Unversioned alias `POST /api/status/publish` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token. JSON api.StatusPublishRequest or multipart file with optional caption.
- Request schemas. `api.StatusPublishRequest`.
- HTTP 200. `models.QpResponse`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### EditResult

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `messageId` | string | Required |

### UserMessage

| Field | Type | Presence |
| --- | --- | --- |
| `token` | string | Required |
| `session_id` | string | Optional |
| `message` | `whatsapp.WhatsappMessage` | Required |

### UserMessages

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `total` | integer | Required |
| `page` | integer | Required |
| `limit` | integer | Required |
| `messages` | Array of `UserMessage` | Required |

### api.LIDDirectSendRequest

| Field | Type | Presence |
| --- | --- | --- |
| `chatid` | string | Unspecified |
| `inreply` | string | Unspecified |
| `text` | string | Unspecified |
| `trackid` | string | Unspecified |

### api.MessageResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `message` | `whatsapp.WhatsappMessage` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### api.PinListResponse

| Field | Type | Presence |
| --- | --- | --- |
| `chatid` | string | Unspecified |
| `debug` | Array of string | Unspecified |
| `pins` | Array of `models.QpMessagePin` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### api.PinRequest

| Field | Type | Presence |
| --- | --- | --- |
| `action` | string | Unspecified |
| `duration` | integer | Unspecified |
| `messageid` | string | Unspecified |

### api.PollVoteRequest

| Field | Type | Presence |
| --- | --- | --- |
| `indexes` | Array of integer | Unspecified |
| `messageid` | string | Unspecified |
| `options` | Array of string | Unspecified |

### api.PollVoteResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `options` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### api.ReactionRequest

| Field | Type | Presence |
| --- | --- | --- |
| `chatid` | string | Unspecified |
| `emoji` | string | Unspecified |
| `fromme` | boolean | Unspecified |
| `messageid` | string | Unspecified |

### api.ReceiveResponse

| Field | Type | Presence |
| --- | --- | --- |
| `_server` | string | Unspecified |
| `debug` | Array of string | Unspecified |
| `limit` | integer | Unspecified |
| `messages` | Array of `whatsapp.WhatsappMessage` | Unspecified |
| `page` | integer | Unspecified |
| `server` | `models.QpSession` | Unspecified |
| `session` | `models.QpSession` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `total` | integer | Unspecified |
| `totalPages` | integer | Unspecified |

### api.SendActionButton

| Field | Type | Presence |
| --- | --- | --- |
| `code` | string | Unspecified |
| `id` | string | Unspecified |
| `phone` | string | Unspecified |
| `text` | string | Unspecified |
| `type` | `whatsapp.WhatsappActionType` | Unspecified |
| `url` | string | Unspecified |
| `webview` | boolean | Unspecified |

### api.SendActionRequest

| Field | Type | Presence |
| --- | --- | --- |
| `actions` | Array of `api.SendActionButton` | Unspecified |
| `chatid` | string | Unspecified |
| `footer` | string | Unspecified |
| `id` | string | Unspecified |
| `text` | string | Unspecified |
| `title` | string | Unspecified |
| `trackid` | string | Unspecified |

### api.SendInteractiveRequest

| Field | Type | Presence |
| --- | --- | --- |
| `actions` | Array of `api.SendActionButton` | Unspecified |
| `button_text` | string | Unspecified |
| `cards` | Array of `whatsapp.WhatsappCarouselCard` | Unspecified |
| `chatid` | string | Unspecified |
| `footer` | string | Unspecified |
| `form` | `whatsapp.WhatsappInteractiveForm` | Unspecified |
| `id` | string | Unspecified |
| `sections` | Array of `whatsapp.WhatsappListSection` | Unspecified |
| `text` | string | Unspecified |
| `title` | string | Unspecified |
| `trackid` | string | Unspecified |
| `type` | string | Unspecified |

### api.SendLinkRequest

| Field | Type | Presence |
| --- | --- | --- |
| `chatid` | string | Unspecified |
| `description` | string | Unspecified |
| `id` | string | Unspecified |
| `text` | string | Unspecified |
| `title` | string | Unspecified |
| `trackid` | string | Unspecified |
| `url` | string | Unspecified |

### api.SendResponse

| Field | Type | Presence |
| --- | --- | --- |
| `code` | string | Unspecified |
| `debug` | Array of string | Unspecified |
| `delivery_unknown` | boolean | Unspecified |
| `message` | `api.SendResponseMessage` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### api.SendResponseMessage

| Field | Type | Presence |
| --- | --- | --- |
| `chatId` | string | Unspecified |
| `id` | string | Unspecified |
| `phone` | string | Unspecified |
| `trackId` | string | Unspecified |
| `whatsmeowId` | string | Unspecified |
| `wid` | string | Unspecified |

### api.StatusPublishAttachment

| Field | Type | Presence |
| --- | --- | --- |
| `content` | string | Unspecified |
| `filename` | string | Unspecified |
| `mime` | string | Unspecified |

### api.StatusPublishRequest

| Field | Type | Presence |
| --- | --- | --- |
| `attachment` | `api.StatusPublishAttachment` | Unspecified |
| `text` | string | Unspecified |

### models.QpMessagePin

| Field | Type | Presence |
| --- | --- | --- |
| `chatid` | string | Unspecified |
| `eventat` | string | Unspecified |
| `expiresat` | string | Unspecified |
| `messageid` | string | Unspecified |
| `pinned` | boolean | Unspecified |
| `pinnedby` | string | Unspecified |

### models.QpMetadata

Map of JSON value

### models.QpResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### models.QpSession

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `call_policy` | `whatsapp.NullableCallPolicy` | Unspecified |
| `contextid` | string | Unspecified |
| `deliveryreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `devel` | boolean | Unspecified |
| `direct` | `whatsapp.WhatsappBoolean` | Unspecified |
| `dispatchTypes` | string | Unspecified |
| `groups` | `whatsapp.WhatsappBoolean` | Unspecified |
| `historysyncdays` | integer | Unspecified |
| `host` | string | Unspecified |
| `id` | string | Unspecified |
| `manually_stopped` | boolean | Unspecified |
| `messages` | `whatsapp.WhatsappBoolean` | Unspecified |
| `metadata` | `models.QpMetadata` | Unspecified |
| `presence` | string | Unspecified |
| `readreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `readupdate` | `whatsapp.WhatsappBoolean` | Unspecified |
| `sip_register_enabled` | `whatsapp.WhatsappBoolean` | Unspecified |
| `storeRetentionDays` | integer | Unspecified |
| `timestamp` | string | Unspecified |
| `token` | string | Unspecified |
| `user` | string | Unspecified |
| `user_id` | string | Unspecified |
| `verified` | boolean | Unspecified |
| `voipmode` | `whatsapp.VoIPMode` | Unspecified |
| `wid` | string | Unspecified |

### whatsapp.CallPolicy

integer

### whatsapp.NullableCallPolicy

| Field | Type | Presence |
| --- | --- | --- |
| `policy` | `whatsapp.CallPolicy` | Unspecified |
| `valid` | boolean | Unspecified |

### whatsapp.VoIPMode

string

### whatsapp.WhatsappAction

| Field | Type | Presence |
| --- | --- | --- |
| `code` | string | Unspecified |
| `id` | string | Unspecified |
| `phone` | string | Unspecified |
| `text` | string | Unspecified |
| `type` | `whatsapp.WhatsappActionType` | Unspecified |
| `url` | string | Unspecified |
| `webview` | boolean | Unspecified |

### whatsapp.WhatsappActionMessage

| Field | Type | Presence |
| --- | --- | --- |
| `actions` | Array of `whatsapp.WhatsappAction` | Unspecified |
| `footer` | string | Unspecified |
| `text` | string | Unspecified |
| `title` | string | Unspecified |

### whatsapp.WhatsappActionType

string

### whatsapp.WhatsappAttachment

| Field | Type | Presence |
| --- | --- | --- |
| `accuracy` | number | Unspecified |
| `checksum` | string | Unspecified |
| `expires_duration` | integer | Unspecified |
| `filelength` | integer | Unspecified |
| `filename` | string | Unspecified |
| `heading` | number | Unspecified |
| `latitude` | number | Unspecified |
| `longitude` | number | Unspecified |
| `mime` | string | Unspecified |
| `seconds` | integer | Unspecified |
| `sequence` | integer | Unspecified |
| `speed` | number | Unspecified |
| `thumbnail` | `whatsapp.WhatsappMessageThumbnail` | Unspecified |
| `timeoffset` | integer | Unspecified |
| `url` | string | Unspecified |
| `waveform` | Array of integer | Unspecified |

### whatsapp.WhatsappBoolean

integer

### whatsapp.WhatsappCarouselCard

| Field | Type | Presence |
| --- | --- | --- |
| `actions` | Array of `whatsapp.WhatsappAction` | Unspecified |
| `image_url` | string | Unspecified |
| `text` | string | Unspecified |
| `title` | string | Unspecified |

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

### whatsapp.WhatsappContact

| Field | Type | Presence |
| --- | --- | --- |
| `name` | string | Unspecified |
| `phone` | string | Unspecified |
| `vcard` | string | Unspecified |

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

### whatsapp.WhatsappDisappearing

| Field | Type | Presence |
| --- | --- | --- |
| `edit_on_next` | boolean | Unspecified |
| `replace_on_next` | boolean | Unspecified |
| `timer` | string | Unspecified |

### whatsapp.WhatsappFormOption

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Unspecified |
| `title` | string | Unspecified |

### whatsapp.WhatsappFormStep

| Field | Type | Presence |
| --- | --- | --- |
| `allow_custom` | boolean | Unspecified |
| `id` | string | Unspecified |
| `label` | string | Unspecified |
| `multiple` | boolean | Unspecified |
| `options` | Array of `whatsapp.WhatsappFormOption` | Unspecified |

### whatsapp.WhatsappInteractiveForm

| Field | Type | Presence |
| --- | --- | --- |
| `steps` | Array of `whatsapp.WhatsappFormStep` | Unspecified |

### whatsapp.WhatsappInteractiveMessage

| Field | Type | Presence |
| --- | --- | --- |
| `actions` | Array of `whatsapp.WhatsappAction` | Unspecified |
| `button_text` | string | Unspecified |
| `cards` | Array of `whatsapp.WhatsappCarouselCard` | Unspecified |
| `footer` | string | Unspecified |
| `form` | `whatsapp.WhatsappInteractiveForm` | Unspecified |
| `sections` | Array of `whatsapp.WhatsappListSection` | Unspecified |
| `text` | string | Unspecified |
| `title` | string | Unspecified |
| `type` | string | Unspecified |

### whatsapp.WhatsappInteractiveReply

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Unspecified |
| `name` | string | Unspecified |
| `params` | object | Unspecified |
| `title` | string | Unspecified |
| `type` | string | Unspecified |
| `version` | integer | Unspecified |

### whatsapp.WhatsappListRow

| Field | Type | Presence |
| --- | --- | --- |
| `description` | string | Unspecified |
| `id` | string | Unspecified |
| `title` | string | Unspecified |

### whatsapp.WhatsappListSection

| Field | Type | Presence |
| --- | --- | --- |
| `rows` | Array of `whatsapp.WhatsappListRow` | Unspecified |
| `title` | string | Unspecified |

### whatsapp.WhatsappLocation

| Field | Type | Presence |
| --- | --- | --- |
| `address` | string | Unspecified |
| `latitude` | number | Unspecified |
| `longitude` | number | Unspecified |
| `name` | string | Unspecified |
| `url` | string | Unspecified |

### whatsapp.WhatsappMessage

| Field | Type | Presence |
| --- | --- | --- |
| `action` | `whatsapp.WhatsappActionMessage` | Unspecified |
| `ads` | `whatsapp.WhatsappMessageAds` | Unspecified |
| `attachment` | `whatsapp.WhatsappAttachment` | Unspecified |
| `chat` | `whatsapp.WhatsappChat` | Unspecified |
| `contact` | `whatsapp.WhatsappContact` | Unspecified |
| `debug` | `whatsapp.WhatsappMessageDebug` | Unspecified |
| `disappearing` | `whatsapp.WhatsappDisappearing` | Unspecified |
| `edited` | boolean | Unspecified |
| `exceptions` | Array of string | Unspecified |
| `expiresat` | integer | Unspecified |
| `forwarded` | boolean | Unspecified |
| `forwardingscore` | integer | Unspecified |
| `fromhistory` | boolean | Unspecified |
| `frominternal` | boolean | Unspecified |
| `fromme` | boolean | Unspecified |
| `id` | string | Unspecified |
| `inaibotmessage` | boolean | Unspecified |
| `info` | JSON value | Unspecified |
| `inforwarded` | boolean | Unspecified |
| `inreaction` | boolean | Unspecified |
| `inreply` | string | Unspecified |
| `interactive` | `whatsapp.WhatsappInteractiveMessage` | Unspecified |
| `interactive_reply` | `whatsapp.WhatsappInteractiveReply` | Unspecified |
| `invideonote` | boolean | Unspecified |
| `location` | `whatsapp.WhatsappLocation` | Unspecified |
| `participant` | `whatsapp.WhatsappChat` | Unspecified |
| `pin` | `whatsapp.WhatsappPin` | Unspecified |
| `poll` | `whatsapp.WhatsappPoll` | Unspecified |
| `status` | `whatsapp.WhatsappMessageStatus` | Unspecified |
| `synopsis` | string | Unspecified |
| `text` | string | Unspecified |
| `timestamp` | string | Unspecified |
| `trackid` | string | Unspecified |
| `type` | `whatsapp.WhatsappMessageType` | Unspecified |
| `url` | `whatsapp.WhatsappMessageUrl` | Unspecified |
| `whatsmeowid` | string | Unspecified |
| `wid` | string | Unspecified |

### whatsapp.WhatsappMessageAds

| Field | Type | Presence |
| --- | --- | --- |
| `app` | string | Unspecified |
| `id` | string | Unspecified |
| `sourceid` | string | Unspecified |
| `sourceurl` | string | Unspecified |
| `thumbnail` | `whatsapp.WhatsappMessageThumbnail` | Unspecified |
| `title` | string | Unspecified |
| `type` | string | Unspecified |

### whatsapp.WhatsappMessageDebug

| Field | Type | Presence |
| --- | --- | --- |
| `event` | string | Unspecified |
| `info` | JSON value | Unspecified |
| `reason` | string | Unspecified |

### whatsapp.WhatsappMessageStatus

string

### whatsapp.WhatsappMessageThumbnail

| Field | Type | Presence |
| --- | --- | --- |
| `data` | string | Unspecified |
| `mime` | string | Unspecified |
| `urlprefix` | string | Unspecified |

### whatsapp.WhatsappMessageType

integer

### whatsapp.WhatsappMessageUrl

| Field | Type | Presence |
| --- | --- | --- |
| `description` | string | Unspecified |
| `reference` | string | Unspecified |
| `thumbnail` | `whatsapp.WhatsappMessageThumbnail` | Unspecified |
| `title` | string | Unspecified |

### whatsapp.WhatsappPin

| Field | Type | Presence |
| --- | --- | --- |
| `action` | string | Unspecified |
| `duration` | integer | Unspecified |
| `expiresat` | string | Unspecified |
| `messageid` | string | Unspecified |

### whatsapp.WhatsappPoll

| Field | Type | Presence |
| --- | --- | --- |
| `options` | Array of string | Unspecified |
| `question` | string | Unspecified |
| `selections` | integer | Unspecified |
