# Sessions and pairing

QuePasa 5.26.1125.1212, canonical API v5.

## Behaviors

- Read configured flags from `session` in `POST /sessions/get`. A JSON `null` means inherit, `false` explicitly disables, and `true` explicitly enables. Keep those three values distinct. The per-option effective fields, when present, report the resolved policy.
- The read names `readReceipts` and `deliveryReceipts` become lowercase `readreceipts` and `deliveryreceipts` in `PATCH /sessions`. To set only groups, send `{"groups":true}`. Omit all unrelated keys. For ordinary pointer-backed Boolean fields such as groups, use numeric `0` to clear the override. JSON `null` is treated as omission in that patch. The call policy has its own presence and null semantics.
- `POST /session/option` accepts the option name in JSON, query, or `X-QUEPASA-OPTION`. Ordinary tri-state flags cycle unset → true → false → unset. The returned `value` is Boolean and cannot tell unset from false. Inspect `session.<field>`. The dedicated call policy cycles inherit → process → reject → ignore → inherit. Use the idempotent patch when the requested value is already known.
- The session reads include a temporary `server` alias for `session`. Prefer the canonical `session` key. Snapshot metadata can mark data from a fallback. Check it before treating a read as current. Session export bundles include linked-device credentials and should be handled as secrets.

### Read and set only the groups option

```bash
curl --fail-with-body --silent --show-error -X POST "$QUEPASA_API/sessions/get" \
  -H "X-QUEPASA-USERKEY: $QUEPASA_USER_KEY" \
  -H "X-QUEPASA-TOKEN: $QUEPASA_SESSION_TOKEN" | jq '.session.groups'
curl --fail-with-body --silent --show-error -X PATCH "$QUEPASA_API/sessions" \
  -H "X-QUEPASA-USERKEY: $QUEPASA_USER_KEY" \
  -H "X-QUEPASA-TOKEN: $QUEPASA_SESSION_TOKEN" \
  -H 'Content-Type: application/json' --data '{"groups":true}'
```

Read the flag with the first request again to verify the update. In JavaScript, use
`option === null` for inherited and `option === false` for explicitly disabled.

## Operations

### `DELETE /api/v5/sessions`

Delete the selected session.

- Unversioned alias `DELETE /api/sessions` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token. Deletion may return an empty body.
- HTTP 200. `models.QpResponse`.
- HTTP 204. Empty body.

### `GET /api/v5/session/events`

Read connection history for one session.

- Unversioned alias `GET /api/session/events` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Query id or session token, limit and cursor.
- HTTP 200. `api.SessionEventsResponse`.

### `GET /api/v5/session/export`

Export a portable linked-device bundle.

- Unversioned alias `GET /api/session/export` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token. Protect the response as credentials.
- HTTP 200. `SessionExport`.

### `GET /api/v5/session/paircode`

Get a phone pairing code.

- Unversioned alias `GET /api/session/paircode` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and phone query. Optional historysyncdays.
- HTTP 200. `Pairing`.

### `GET /api/v5/session/qrcode`

Get a QR code for a session.

- Unversioned alias `GET /api/session/qrcode` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and optional historysyncdays query.
- HTTP 200. `Pairing`.

### `GET /api/v5/sessions`

List visible sessions and the gateway version.

- Unversioned alias `GET /api/sessions` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Optional limit and cursor for the collection, or id to read one session.
- HTTP 200. `SessionList` or `SessionDetail`.

### `PATCH /api/v5/sessions`

Update only the session fields supplied.

- Unversioned alias `PATCH /api/sessions` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and JSON patch. See the session option rules and examples.
- Request schemas. `SessionPatch`.
- HTTP 200. `api.InformationResponse` or `SessionCompat`.

### `PATCH /api/v5/sessions/token`

Rename a session token.

- Unversioned alias `PATCH /api/sessions/token` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Current session token and JSON new_token (maximum 100 characters). References must use the returned token after success.
- HTTP 200. `SessionTokenRename`.

### `POST /api/v5/session/debug`

Toggle session debug mode.

- Unversioned alias `POST /api/session/debug` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token. This is a toggle.
- HTTP 200. `SessionDebug`.

### `POST /api/v5/session/disable`

Request that the selected session stop.

- Unversioned alias `POST /api/session/disable` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token.
- HTTP 200. `Result` or `models.QpResponse`.

### `POST /api/v5/session/disconnects/reset`

Reset stored disconnection statistics.

- Unversioned alias `POST /api/session/disconnects/reset` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token.
- HTTP 200. `DisconnectReset`.

### `POST /api/v5/session/enable`

Request that the selected session start.

- Unversioned alias `POST /api/session/enable` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token.
- HTTP 200. `Result` or `models.QpResponse`.

### `POST /api/v5/session/import`

Import a portable linked-device bundle.

- Unversioned alias `POST /api/session/import` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. JSON bundle and target token. Treat bundle fields as secrets.
- HTTP 200. `SessionImport`.

### `POST /api/v5/session/option`

Cycle the selected option to its next state.

- Unversioned alias `POST /api/session/option` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and option in the body, query or X-QUEPASA-OPTION. Use PATCH /sessions to set an explicit value.
- HTTP 200. `SessionToggle`.

### `POST /api/v5/session/pair`

Link a session using a QR code or phone code.

- Unversioned alias `POST /api/session/pair` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token. JSON method (qrcode or paircode), phone for paircode and optional historysyncdays. Use format=png for raw QR image bytes.
- HTTP 200. `Pairing` or binary.

### `POST /api/v5/session/restart`

Request that the selected session restart.

- Unversioned alias `POST /api/session/restart` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token.
- HTTP 200. `Result` or `models.QpResponse`.

### `POST /api/v5/sessions`

Create a persisted session configuration.

- Unversioned alias `POST /api/sessions` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Optional JSON configuration. Session creation and custom token depend on gateway policy.
- Request schemas. `api.InfoCreateRequest`.
- HTTP 201. `SessionCreated`.

### `POST /api/v5/sessions/get`

Read one session and its configured options.

- Unversioned alias `POST /api/sessions/get` when canonical aliases are enabled.
- Access. Authenticated with read access to the selected resource or session.
- Request. Session token. JSON token is also accepted.
- HTTP 200. `SessionDetail`.

### `POST /api/v5/sessions/search`

Search and paginate visible sessions.

- Unversioned alias `POST /api/sessions/search` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. JSON query, token, phone, state, page and limit.
- Request schemas. `SessionSearchRequest`.
- HTTP 200. `SessionSearch`.

### `PUT /api/v5/session/name`

Set the WhatsApp profile name.

- Unversioned alias `PUT /api/session/name` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and JSON name.
- HTTP 200. `SessionName`.

### `PUT /api/v5/session/photo`

Set or remove the WhatsApp profile photo.

- Unversioned alias `PUT /api/session/photo` when canonical aliases are enabled.
- Access. Authenticated with permission to modify the selected resource or session.
- Request. Session token and photo payload.
- HTTP 200. `PhotoResult`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### DisconnectReset

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `token` | string | Required |
| `reset_at` | date-time | Required |

### DisconnectStats

| Field | Type | Presence |
| --- | --- | --- |
| `total` | integer | Required |
| `recent` | integer | Required |
| `last_at` | date-time | Optional |
| `recent_times` | Array of date-time | Optional |
| `reset_at` | date-time | Optional |

### OutboundRateObservation

| Field | Type | Presence |
| --- | --- | --- |
| `available` | boolean | Required |
| `mode` | string | Required |
| `generation` | string | Required |
| `sampled_at` | date-time | Required |
| `last_exceeded_at` | date-time or null | Required |
| `max_delay_ms` | integer | Required |
| `decisions` | Array of `RateDecision` or null | Required |
| `buckets` | Array of `RateBucket` or null | Required |
| `policy` | `RatePolicy` | Required |

### Pairing

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `connected` | boolean | Optional |
| `token` | string | Optional |
| `wid` | string | Optional |
| `qrcode` | string | Optional |
| `rawcode` | string | Optional |
| `pairCode` | string | Optional |
| `formatted` | string | Optional |
| `method` | string | Optional |
| `format` | string | Optional |

### PhotoResult

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `pictureId` | string | Optional |

### RateBucket

| Field | Type | Presence |
| --- | --- | --- |
| `at` | integer | Required |
| `decisions` | Array of `RateDecision` or null | Required |

### RateDecision

| Field | Type | Presence |
| --- | --- | --- |
| `scope` | string | Required |
| `outcome` | string | Required |
| `count` | integer | Required |

### RatePolicy

| Field | Type | Presence |
| --- | --- | --- |
| `api_read_rpm` | integer | Required |
| `api_login_rpm` | integer | Required |
| `api_mutation_rpm` | integer | Required |
| `api_admin_rpm` | integer | Required |
| `outbound_observe_only` | boolean | Required |
| `outbound_enabled` | boolean | Required |
| `outbound_session_rpm` | integer | Required |
| `outbound_session_burst` | integer | Required |
| `outbound_recipient_rpm` | integer | Required |
| `outbound_recipient_burst` | integer | Required |
| `outbound_max_wait_ms` | integer | Required |

### Result

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |

### Session

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Optional |
| `token` | string | Required |
| `wid` | string | Required |
| `contextid` | string | Required |
| `host` | string | Required |
| `state` | string | Required |
| `stateCode` | integer | Required |
| `verified` | boolean | Required |
| `devel` | boolean | Required |
| `manually_stopped` | boolean | Required |
| `user` | string | Required |
| `user_id` | string | Optional |
| `timestamp` | date-time | Required |
| `startTime` | date-time | Required |
| `lastUpdate` | date-time | Required |
| `diagnostic` | `models.QpConnectionDiagnostic` or null | Required |
| `disconnect_stats` | `DisconnectStats` or null | Required |
| `uptimeSeconds` | integer | Required |
| `dispatchCount` | integer | Required |
| `webhookCount` | integer | Required |
| `rabbitmqCount` | integer | Required |
| `hasDispatching` | boolean | Required |
| `hasWebhooks` | boolean | Required |
| `hasRabbitMQ` | boolean | Required |
| `platform` | string | Required |
| `whatsappAccountType` | string | Required |
| `whatsappBusinessName` | string | Required |
| `whatsappPushName` | string | Required |
| `isBusiness` | boolean | Required |
| `listsSupported` | boolean | Required |
| `groups` | boolean or null | Required |
| `broadcasts` | boolean or null | Required |
| `readReceipts` | boolean or null | Required |
| `deliveryReceipts` | boolean or null | Required |
| `calls` | integer or null | Required |
| `calls_effective` | integer | Required |
| `calls_policy` | string | Required |
| `calls_source` | string | Required |
| `calls_locked` | boolean | Required |
| `messages` | boolean or null | Required |
| `messages_effective` | boolean | Required |
| `messages_source` | string | Required |
| `messages_locked` | boolean | Required |
| `server_message_policies` | Map of boolean | Required |
| `readupdate` | boolean or null | Required |
| `direct` | boolean or null | Required |
| `sip_register_enabled` | boolean or null | Required |
| `sip_register_password_set` | boolean | Required |
| `voip_mode` | string | Required |
| `presence` | string | Required |
| `presence_effective` | string | Required |
| `presence_source` | string | Required |
| `presence_locked` | boolean | Required |
| `server_presence` | string | Required |
| `store_retention_days` | integer or null | Optional |
| `dispatch_types` | string | Optional |
| `historysyncdays` | integer | Optional |
| `runtimeHost` | string | Optional |
| `runtimeStale` | boolean | Optional |
| `connection_health` | `whatsapp.ConnectionHealth` | Optional |
| `outbound_rate_observation` | `OutboundRateObservation` | Optional |

### SessionCompat

| Field | Type | Presence |
| --- | --- | --- |
| `session` | `Session` | Required |
| `server` | `Session` | Required |
| `_server` | string | Required |

### SessionCreated

`SessionCompat`

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `status` | string | Required |
| `diagnostic` | `models.QpConnectionDiagnostic` or null | Required |

### SessionDebug

`SessionCompat`

| Field | Type | Presence |
| --- | --- | --- |
| `devel` | boolean | Required |

### SessionDetail

`SessionCompat`

| Field | Type | Presence |
| --- | --- | --- |
| `dataSource` | string | Required |
| `degraded` | boolean | Required |
| `snapshotCapturedAt` | date-time | Optional |
| `snapshotExpiresAt` | date-time | Optional |

### SessionExport

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `result` | string | Required |
| `exportedAt` | date-time | Required |
| `wid` | string | Required |
| `token` | string | Required |
| `counts` | Map of integer | Required |
| `bundle` | `TransferBundle` | Required |

### SessionImport

`SessionCompat`

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `result` | string | Required |
| `imported` | Map of integer | Required |
| `started` | boolean | Required |

### SessionList

| Field | Type | Presence |
| --- | --- | --- |
| `servers` | Array of `Session` or null | Required |
| `total` | integer | Required |
| `version` | string | Required |
| `username` | string | Required |
| `databaseDriver` | string | Required |
| `cableBackplaneWarning` | boolean | Required |
| `serversViewMode` | string | Optional |
| `serversPageSize` | integer | Optional |
| `nextCursor` | string | Optional |
| `dataSource` | string | Required |
| `degraded` | boolean | Required |
| `snapshotCapturedAt` | date-time | Optional |
| `snapshotExpiresAt` | date-time | Optional |

### SessionName

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `name` | string | Required |

### SessionPatch

| Field | Type | Presence |
| --- | --- | --- |
| `groups` | boolean or integer | Optional |
| `broadcasts` | boolean or integer | Optional |
| `readreceipts` | boolean or integer | Optional |
| `deliveryreceipts` | boolean or integer | Optional |
| `messages` | boolean or integer | Optional |
| `readupdate` | boolean or integer | Optional |
| `direct` | boolean or integer | Optional |
| `sip_register_enabled` | boolean or integer | Optional |
| `calls` | boolean or integer or string or null | Optional |
| `username` | string | Optional |
| `devel` | boolean | Optional |
| `store_retention_days` | integer | Optional |
| `dispatch_types` | string | Optional |
| `historysyncdays` | integer | Optional |
| `contextid` | string | Optional |
| `host` | string | Optional |
| `sip_register_password` | string | Optional |
| `voip_mode` | string | Optional |
| `presence` | string | Optional |

### SessionSearch

| Field | Type | Presence |
| --- | --- | --- |
| `items` | Array of `Session` or null | Required |
| `total` | integer | Required |
| `page` | integer | Required |
| `limit` | integer | Required |
| `dataSource` | string | Required |
| `degraded` | boolean | Required |
| `snapshotCapturedAt` | date-time | Optional |
| `snapshotExpiresAt` | date-time | Optional |

### SessionSearchRequest

| Field | Type | Presence |
| --- | --- | --- |
| `query` | string | Optional |
| `token` | string | Optional |
| `phone` | string | Optional |
| `state` | string | Optional |
| `page` | integer | Optional |
| `limit` | integer | Optional |

### SessionToggle

`SessionCompat`

| Field | Type | Presence |
| --- | --- | --- |
| `option` | string | Required |
| `value` | boolean | Required |

### SessionTokenRename

`SessionCompat`

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `status` | string | Required |

### SessionTransferSnapshot

| Field | Type | Presence |
| --- | --- | --- |
| `token` | string | Optional |
| `wid` | string | Required |
| `verified` | boolean | Required |
| `devel` | boolean | Optional |
| `groups` | boolean or null | Optional |
| `broadcasts` | boolean or null | Optional |
| `readreceipts` | boolean or null | Optional |
| `deliveryreceipts` | boolean or null | Optional |
| `messages` | boolean or null | Optional |
| `readupdate` | boolean or null | Optional |
| `direct` | boolean or null | Optional |
| `sip_register_enabled` | boolean or null | Optional |
| `call_policy` | integer or null | Optional |
| `historysyncdays` | integer | Optional |
| `store_retention_days` | integer | Optional |
| `dispatch_types` | string | Optional |
| `contextid` | string | Optional |
| `sip_register_password` | string | Optional |
| `voipmode` | string | Optional |
| `presence` | string | Optional |

### SessionTransferTable

| Field | Type | Presence |
| --- | --- | --- |
| `name` | string | Required |
| `columns` | Array of string | Required |
| `rows` | Array of Array of `TransferCell` | Required |

### TransferBundle

| Field | Type | Presence |
| --- | --- | --- |
| `format` | string | Required |
| `version` | integer | Required |
| `created_at` | date-time | Required |
| `driver` | string | Optional |
| `session` | `SessionTransferSnapshot` | Required |
| `tables` | Array of `SessionTransferTable` | Required |
| `counts` | Map of integer | Required |

### TransferCell

| Field | Type | Presence |
| --- | --- | --- |
| `z` | boolean | Optional |
| `n` | number | Optional |
| `s` | string | Optional |
| `b` | string | Optional |

### api.InfoCreateRequest

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `calls` | `whatsapp.NullableCallPolicy` | Unspecified |
| `contextid` | string | Unspecified |
| `deliveryreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `devel` | boolean | Unspecified |
| `direct` | `whatsapp.WhatsappBoolean` | Unspecified |
| `groups` | `whatsapp.WhatsappBoolean` | Unspecified |
| `messages` | `whatsapp.WhatsappBoolean` | Unspecified |
| `presence` | string | Unspecified |
| `readreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `readupdate` | `whatsapp.WhatsappBoolean` | Unspecified |
| `sip_register_enabled` | `whatsapp.WhatsappBoolean` | Unspecified |
| `sip_register_password` | string | Unspecified |

### api.InformationResponse

| Field | Type | Presence |
| --- | --- | --- |
| `_server` | string | Unspecified |
| `connection_health` | `whatsapp.ConnectionHealth` | Unspecified |
| `debug` | Array of string | Unspecified |
| `diagnostic` | `models.QpConnectionDiagnostic` | Unspecified |
| `server` | `models.QpWhatsappSession` | Unspecified |
| `session` | `models.QpWhatsappSession` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `version` | string | Unspecified |

### api.SessionEventsResponse

| Field | Type | Presence |
| --- | --- | --- |
| `active_restriction` | `models.QpConnectionDiagnostic` | Unspecified |
| `diagnostic` | `models.QpConnectionDiagnostic` | Unspecified |
| `events` | Array of `models.QpSessionEvent` | Unspecified |
| `next_cursor` | string | Unspecified |
| `session_id` | string | Unspecified |

### models.QpConnectionDiagnostic

| Field | Type | Presence |
| --- | --- | --- |
| `code` | string | Unspecified |
| `disconnect_cause` | string | Unspecified |
| `disconnect_details` | string | Unspecified |
| `force_manual_refresh` | boolean | Unspecified |
| `logout_reason` | string | Unspecified |
| `message` | string | Unspecified |
| `occurred_at` | string | Unspecified |
| `pair_code_retryable` | boolean | Unspecified |
| `pair_code_stage` | string | Unspecified |
| `requires_reauth` | boolean | Unspecified |
| `restriction_expires_at` | string | Unspecified |
| `restriction_type` | string | Unspecified |
| `suggested_action` | string | Unspecified |

### models.QpDispatching

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `call_policy` | `whatsapp.NullableCallPolicy` | Unspecified |
| `connection_string` | string | Unspecified |
| `deliveryreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `direct` | `whatsapp.WhatsappBoolean` | Unspecified |
| `extra` | JSON value | Unspecified |
| `failure` | string | Unspecified |
| `forwardinternal` | boolean | Unspecified |
| `groups` | `whatsapp.WhatsappBoolean` | Unspecified |
| `historysyncdays` | integer | Unspecified |
| `id` | string | Unspecified |
| `messages` | `whatsapp.WhatsappBoolean` | Unspecified |
| `owner_user_id` | string | Unspecified |
| `presence` | string | Unspecified |
| `readreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `readupdate` | `whatsapp.WhatsappBoolean` | Unspecified |
| `success` | string | Unspecified |
| `timestamp` | string | Unspecified |
| `trackid` | string | Unspecified |
| `type` | string | Unspecified |
| `voipmode` | `whatsapp.VoIPMode` | Unspecified |

### models.QpMetadata

Map of JSON value

### models.QpResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### models.QpSessionEvent

| Field | Type | Presence |
| --- | --- | --- |
| `diagnostic` | `models.QpConnectionDiagnostic` | Unspecified |
| `id` | string | Unspecified |
| `occurred_at` | string | Unspecified |
| `session_id` | string | Unspecified |
| `type` | string | Unspecified |

### models.QpTimestamps

| Field | Type | Presence |
| --- | --- | --- |
| `event` | string | Unspecified |
| `message` | string | Unspecified |
| `start` | string | Unspecified |
| `update` | string | Unspecified |

### models.QpWhatsappSession

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `call_policy` | `whatsapp.NullableCallPolicy` | Unspecified |
| `contextid` | string | Unspecified |
| `deliveryreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `devel` | boolean | Unspecified |
| `direct` | `whatsapp.WhatsappBoolean` | Unspecified |
| `dispatchTypes` | string | Unspecified |
| `dispatching` | Array of `models.QpDispatching` | Unspecified |
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
| `reconnect` | boolean | Unspecified |
| `sip_register_enabled` | `whatsapp.WhatsappBoolean` | Unspecified |
| `storeRetentionDays` | integer | Unspecified |
| `timestamp` | string | Unspecified |
| `timestamps` | `models.QpTimestamps` | Unspecified |
| `token` | string | Unspecified |
| `user` | string | Unspecified |
| `user_id` | string | Unspecified |
| `verified` | boolean | Unspecified |
| `voipmode` | `whatsapp.VoIPMode` | Unspecified |
| `wid` | string | Unspecified |

### whatsapp.CallPolicy

integer

### whatsapp.ConnectionHealth

| Field | Type | Presence |
| --- | --- | --- |
| `keepalive_failures` | integer | Unspecified |
| `observed_at` | string | Unspecified |
| `reason` | string | Unspecified |
| `send_failures` | integer | Unspecified |
| `status` | string | Unspecified |

### whatsapp.NullableCallPolicy

| Field | Type | Presence |
| --- | --- | --- |
| `policy` | `whatsapp.CallPolicy` | Unspecified |
| `valid` | boolean | Unspecified |

### whatsapp.VoIPMode

string

### whatsapp.WhatsappBoolean

integer
