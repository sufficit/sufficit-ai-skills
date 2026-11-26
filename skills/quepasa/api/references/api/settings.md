# Gateway settings

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `DELETE /api/v5/settings/oauth`

Clear OAuth provider overrides.

- Unversioned alias `DELETE /api/settings/oauth` when canonical aliases are enabled.
- Access. System administrator.
- Request. No request parameters.
- HTTP 200. `OAuthSettings`.

### `DELETE /api/v5/settings/rate-limits`

Read, set or reset the global rate policy.

- Unversioned alias `DELETE /api/settings/rate-limits` when canonical aliases are enabled.
- Access. System administrator.
- Request. PUT accepts a JSON policy patch. DELETE restores inherited policy.
- HTTP 200. `RateLimits`.

### `DELETE /api/v5/settings/rate-limits/sessions/{sessionID}`

Read, set or reset a session rate-policy override.

- Unversioned alias `DELETE /api/settings/rate-limits/sessions/{sessionID}` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path sessionID. PUT accepts a JSON policy patch.
- HTTP 200. `RateLimits`.

### `DELETE /api/v5/settings/runtime-limits`

Read, set or restore global runtime limits.

- Unversioned alias `DELETE /api/settings/runtime-limits` when canonical aliases are enabled.
- Access. System administrator.
- Request. PUT accepts api.RuntimeLimitsRequest JSON.
- Request schemas. `api.RuntimeLimitsRequest`.
- HTTP 200. `api.runtimeLimitsResponse`.

### `DELETE /api/v5/settings/scoped`

Delete a scoped setting.

- Unversioned alias `DELETE /api/settings/scoped` when canonical aliases are enabled.
- Access. System administrator.
- Request. Query key, contextid and userid.
- HTTP 200. `DeletedSetting`.

### `GET /api/v5/settings`

Read current gateway configuration.

- Unversioned alias `GET /api/settings` when canonical aliases are enabled.
- Access. System administrator.
- Request. No request parameters.
- HTTP 200. `GatewaySettings`.

### `GET /api/v5/settings/cable`

Read Cable connection policy.

- Unversioned alias `GET /api/settings/cable` when canonical aliases are enabled.
- Access. System administrator.
- Request. No request parameters.
- HTTP 200. `CableSettings`.

### `GET /api/v5/settings/oauth`

Read configured OAuth providers and overrides.

- Unversioned alias `GET /api/settings/oauth` when canonical aliases are enabled.
- Access. System administrator.
- Request. No request parameters.
- HTTP 200. `OAuthSettings`.

### `GET /api/v5/settings/preferences`

Read preference definitions and effective values.

- Unversioned alias `GET /api/settings/preferences` when canonical aliases are enabled.
- Access. System administrator.
- Request. No request parameters.
- HTTP 200. `Preferences`.

### `GET /api/v5/settings/rate-limits`

Read, set or reset the global rate policy.

- Unversioned alias `GET /api/settings/rate-limits` when canonical aliases are enabled.
- Access. System administrator.
- Request. PUT accepts a JSON policy patch. DELETE restores inherited policy.
- HTTP 200. `RateLimits`.

### `GET /api/v5/settings/rate-limits/sessions/{sessionID}`

Read, set or reset a session rate-policy override.

- Unversioned alias `GET /api/settings/rate-limits/sessions/{sessionID}` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path sessionID. PUT accepts a JSON policy patch.
- HTTP 200. `RateLimits`.

### `GET /api/v5/settings/restart`

Read gateway restart status.

- Unversioned alias `GET /api/settings/restart` when canonical aliases are enabled.
- Access. System administrator.
- Request. No request parameters.
- HTTP 200. `Restart`.

### `GET /api/v5/settings/runtime-limits`

Read, set or restore global runtime limits.

- Unversioned alias `GET /api/settings/runtime-limits` when canonical aliases are enabled.
- Access. System administrator.
- Request. PUT accepts api.RuntimeLimitsRequest JSON.
- Request schemas. `api.RuntimeLimitsRequest`.
- HTTP 200. `api.runtimeLimitsResponse`.

### `GET /api/v5/settings/scoped`

List settings in the selected scope.

- Unversioned alias `GET /api/settings/scoped` when canonical aliases are enabled.
- Access. System administrator.
- Request. Query contextid and userid.
- HTTP 200. `ScopedSettings`.

### `POST /api/v5/settings/oauth/test`

Test configured OAuth discovery.

- Unversioned alias `POST /api/settings/oauth/test` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON provider settings or provider identifier.
- HTTP 200. `OAuthTest`.

### `POST /api/v5/settings/restart`

Request a gateway restart.

- Unversioned alias `POST /api/settings/restart` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON restart mode.
- HTTP 200. `Restart`.

### `PUT /api/v5/settings`

Replace the global message configuration.

- Unversioned alias `PUT /api/settings` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON message configuration.
- HTTP 200. `MessageSettings`.

### `PUT /api/v5/settings/cable`

Update Cable connection policy.

- Unversioned alias `PUT /api/settings/cable` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON Cable settings.
- HTTP 200. `CableSettings`.

### `PUT /api/v5/settings/oauth`

Write OAuth provider overrides.

- Unversioned alias `PUT /api/settings/oauth` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON provider settings.
- HTTP 200. `OAuthSettings`.

### `PUT /api/v5/settings/preferences`

Set an environment preference.

- Unversioned alias `PUT /api/settings/preferences` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON key and value string for a supported preference.
- HTTP 200. `Setting`.

### `PUT /api/v5/settings/rate-limits`

Read, set or reset the global rate policy.

- Unversioned alias `PUT /api/settings/rate-limits` when canonical aliases are enabled.
- Access. System administrator.
- Request. PUT accepts a JSON policy patch. DELETE restores inherited policy.
- HTTP 200. `RateLimits`.

### `PUT /api/v5/settings/rate-limits/sessions/{sessionID}`

Read, set or reset a session rate-policy override.

- Unversioned alias `PUT /api/settings/rate-limits/sessions/{sessionID}` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path sessionID. PUT accepts a JSON policy patch.
- HTTP 200. `RateLimits`.

### `PUT /api/v5/settings/runtime-limits`

Read, set or restore global runtime limits.

- Unversioned alias `PUT /api/settings/runtime-limits` when canonical aliases are enabled.
- Access. System administrator.
- Request. PUT accepts api.RuntimeLimitsRequest JSON.
- Request schemas. `api.RuntimeLimitsRequest`.
- HTTP 200. `api.runtimeLimitsResponse`.

### `PUT /api/v5/settings/scoped`

Write a scoped setting.

- Unversioned alias `PUT /api/settings/scoped` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON key, value, contextid and userid.
- HTTP 200. `Setting`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### CablePolicy

| Field | Type | Presence |
| --- | --- | --- |
| `presence_disconnect_grace_seconds` | integer | Required |

### CableSettings

| Field | Type | Presence |
| --- | --- | --- |
| `effective` | `CablePolicy` | Required |
| `defaults` | `CablePolicy` | Required |
| `bounds` | `MinMax` | Required |
| `propagation_seconds` | integer | Required |

### DeletedSetting

| Field | Type | Presence |
| --- | --- | --- |
| `deleted` | boolean | Required |
| `key` | string | Required |
| `contextid` | string | Required |
| `userid` | string | Required |

### GatewaySettings

| Field | Type | Presence |
| --- | --- | --- |
| `env` | `MessageDefaults` | Required |
| `global` | `MessageSettings` | Required |

### MessageDefaults

| Field | Type | Presence |
| --- | --- | --- |
| `store_retention_days` | integer | Required |
| `dispatch_types` | string | Required |
| `profile_picture_cache_seconds` | integer | Required |

### MessageSettings

| Field | Type | Presence |
| --- | --- | --- |
| `store_retention_days` | integer | Optional |
| `dispatch_types` | string | Optional |
| `profile_picture_cache_seconds` | integer | Optional |

### MinMax

| Field | Type | Presence |
| --- | --- | --- |
| `min` | integer | Required |
| `max` | integer | Required |

### OAuthEffective

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Required |
| `provider_url` | string | Required |
| `client_id` | string | Required |
| `redirect_uri` | string | Required |
| `scopes` | Array of string or null | Required |
| `resource_url` | string | Required |
| `client_secret_configured` | boolean | Required |
| `auto_provision` | boolean | Required |
| `context_claim_mapping_enabled` | boolean | Required |
| `context_claim_names` | Array of string | Required |
| `context_claim_entry_pattern` | string | Required |
| `claim_role_mappings` | Map of string | Required |

### OAuthReadiness

| Field | Type | Presence |
| --- | --- | --- |
| `ready` | boolean | Required |
| `active` | boolean | Required |
| `missing` | Array of string | Required |

### OAuthSettings

| Field | Type | Presence |
| --- | --- | --- |
| `effective` | `OAuthEffective` | Required |
| `override_configured` | boolean | Required |
| `sources` | Map of string | Required |
| `status` | `OAuthReadiness` | Required |

### OAuthTest

| Field | Type | Presence |
| --- | --- | --- |
| `checked_at` | date-time | Required |
| `latency_ms` | integer | Required |
| `issuer` | string | Required |
| `authorization_endpoint` | string | Required |
| `token_endpoint` | string | Required |
| `userinfo_endpoint` | string | Required |

### Preference

| Field | Type | Presence |
| --- | --- | --- |
| `key` | string | Required |
| `category` | string | Required |
| `label` | string | Required |
| `description` | string | Optional |
| `type` | string | Required |
| `restartRequired` | boolean | Required |
| `scoped` | boolean | Required |
| `environmentOverride` | boolean | Optional |

### Preferences

| Field | Type | Presence |
| --- | --- | --- |
| `catalog` | Array of `Preference` | Required |
| `environment` | Map of JSON value | Required |

### RateLimits

| Field | Type | Presence |
| --- | --- | --- |
| `scope` | string | Required |
| `revision` | integer | Required |
| `defaults` | `RatePolicy` | Required |
| `global` | `RatePolicy` | Required |
| `override` | `RateOverride` | Required |
| `effective` | `RatePolicy` | Required |
| `session` | `RateSession` | Optional |

### RateOverride

| Field | Type | Presence |
| --- | --- | --- |
| `api_read_rpm` | integer | Optional |
| `api_login_rpm` | integer | Optional |
| `api_mutation_rpm` | integer | Optional |
| `api_admin_rpm` | integer | Optional |
| `outbound_observe_only` | boolean | Optional |
| `outbound_enabled` | boolean | Optional |
| `outbound_session_rpm` | integer | Optional |
| `outbound_session_burst` | integer | Optional |
| `outbound_recipient_rpm` | integer | Optional |
| `outbound_recipient_burst` | integer | Optional |
| `outbound_max_wait_ms` | integer | Optional |

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

### RateSession

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Required |
| `token` | string | Required |

### Restart

| Field | Type | Presence |
| --- | --- | --- |
| `accepted` | boolean | Required |
| `already_running` | boolean | Required |
| `mode` | string | Required |
| `phase` | string | Required |
| `reason` | string | Optional |
| `wait_reason` | string | Optional |
| `started_at` | date-time | Optional |
| `deadline` | date-time | Optional |
| `remaining_seconds` | integer | Required |
| `active_calls` | integer | Required |
| `sessions_with_calls` | integer | Required |
| `unmapped_calls` | integer | Required |
| `pending_sessions` | integer | Required |
| `pending_outbound` | integer | Required |
| `pending_events` | integer | Required |
| `pending_handlers` | integer | Required |
| `pending_dispatch` | integer | Required |
| `quiesce_failures` | integer | Required |
| `last_error` | string | Optional |

### ScopedSettings

| Field | Type | Presence |
| --- | --- | --- |
| `contextid` | string | Required |
| `userid` | string | Required |
| `items` | Array of `Setting` or null | Required |

### Setting

| Field | Type | Presence |
| --- | --- | --- |
| `key` | string | Required |
| `value` | string | Required |
| `contextid` | string | Optional |
| `userid` | string | Optional |
| `created_at` | date-time | Required |
| `updated_at` | date-time | Required |

### api.RuntimeLimitsRequest

| Field | Type | Presence |
| --- | --- | --- |
| `overrides` | object | Unspecified |

### api.runtimeLimitsResponse

| Field | Type | Presence |
| --- | --- | --- |
| `result` | `runtimelimits.Response` | Unspecified |
| `success` | boolean | Unspecified |

### runtimelimits.Field

| Field | Type | Presence |
| --- | --- | --- |
| `activation` | string | Unspecified |
| `category` | string | Unspecified |
| `configured` | JSON value | Unspecified |
| `default` | JSON value | Unspecified |
| `effective` | JSON value | Unspecified |
| `environment` | string | Unspecified |
| `key` | string | Unspecified |
| `max` | integer | Unspecified |
| `min` | integer | Unspecified |
| `restart_required` | boolean | Unspecified |
| `source` | string | Unspecified |
| `type` | string | Unspecified |
| `unit` | string | Unspecified |

### runtimelimits.Response

| Field | Type | Presence |
| --- | --- | --- |
| `fields` | Array of `runtimelimits.Field` | Unspecified |
| `overrides` | object | Unspecified |
| `restart_required` | boolean | Unspecified |
| `revision` | integer | Unspecified |
