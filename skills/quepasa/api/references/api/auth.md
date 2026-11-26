# Authentication and accounts

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `DELETE /api/v5/auth/contexts`

Remove a context access grant.

- Unversioned alias `DELETE /api/auth/contexts` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Provide contextid in query or JSON.
- HTTP 200. `Removed`.

### `DELETE /api/v5/auth/contexts/members`

Remove a context member.

- Unversioned alias `DELETE /api/auth/contexts/members` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Context identifier and target member.
- HTTP 200. `Removed`.

### `DELETE /api/v5/auth/contexts/owned`

Remove an owned context.

- Unversioned alias `DELETE /api/auth/contexts/owned` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Context identifier.
- HTTP 200. `Removed`.

### `DELETE /api/v5/users/{id}`

Delete a user by ID.

- Unversioned alias `DELETE /api/users/{id}` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path id.
- HTTP 200. `ResultID`.

### `DELETE /api/v5/users/{id}/apikey`

Revoke the current managed user API key.

- Unversioned alias `DELETE /api/users/{id}/apikey` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path id.
- HTTP 200. `Revoked`.

### `GET /api/v5/auth/account`

Read account identity and session count.

- Unversioned alias `GET /api/auth/account` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. No request body.
- HTTP 200. `Account`.

### `GET /api/v5/auth/config`

Read login and onboarding options.

- Unversioned alias `GET /api/auth/config` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. No request parameters.
- HTTP 200. `LoginConfig`.

### `GET /api/v5/auth/contexts`

List visible context access grants.

- Unversioned alias `GET /api/auth/contexts` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. No request body.
- HTTP 200. `ContextItems`.

### `GET /api/v5/auth/contexts/owned`

List contexts owned by the caller.

- Unversioned alias `GET /api/auth/contexts/owned` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. No request parameters.
- HTTP 200. `OwnedContexts`.

### `GET /api/v5/auth/contexts/sessions`

List sessions shared with the caller through contexts.

- Unversioned alias `GET /api/auth/contexts/sessions` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Query context filters.
- HTTP 200. `ContextSessionItems`.

### `GET /api/v5/auth/session`

Read the authenticated identity and directives.

- Unversioned alias `GET /api/auth/session` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Bearer token or supported user key.
- HTTP 200. `AuthSession`.

### `GET /api/v5/users`

List users visible to the caller.

- Unversioned alias `GET /api/users` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. No request parameters.
- HTTP 200. `Users`.

### `PATCH /api/v5/auth/contexts`

Create or update a context access grant.

- Unversioned alias `PATCH /api/auth/contexts` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. JSON context and grant fields. Requires context management permission.
- HTTP 200. `ContextItem`.

### `PATCH /api/v5/users/{id}/role`

Set a user role.

- Unversioned alias `PATCH /api/users/{id}/role` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path id and JSON role.
- HTTP 200. `UserRole`.

### `POST /api/v5/auth/contexts`

Create or update a context access grant.

- Unversioned alias `POST /api/auth/contexts` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. JSON context and grant fields. Requires context management permission.
- HTTP 200. `ContextItem`.

### `POST /api/v5/auth/contexts/members`

Add or update a context member.

- Unversioned alias `POST /api/auth/contexts/members` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. JSON context identifier, target user and role.
- HTTP 200. `ContextItem`.

### `POST /api/v5/auth/login`

Exchange login credentials for a JWT.

- Unversioned alias `POST /api/auth/login` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. Form fields email and password. Success sets the HttpOnly jwt cookie.
- HTTP 200. `LoginResult`.

### `POST /api/v5/auth/oauth/exchange`

Exchange an OAuth provider token for a QuePasa JWT.

- Unversioned alias `POST /api/auth/oauth/exchange` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. Use Authorization: Bearer with a token issued by the configured identity provider.
- HTTP 200. `OAuthExchange`.

### `POST /api/v5/auth/setup`

Create the initial account through public bootstrap.

- Unversioned alias `POST /api/auth/setup` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. JSON account credentials. Bootstrap policy applies.
- HTTP 200. `ResultID`.

### `POST /api/v5/users`

Create a QuePasa user.

- Unversioned alias `POST /api/users` when canonical aliases are enabled.
- Access. System administrator.
- Request. JSON account credentials and role.
- HTTP 200. `User`.

### `POST /api/v5/users/{id}/apikey`

Issue a managed user API key.

- Unversioned alias `POST /api/users/{id}/apikey` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path id. Treat the one-time response as a secret.
- HTTP 200. `APIKey`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### APIKey

| Field | Type | Presence |
| --- | --- | --- |
| `apikey` | string | Required |
| `header` | string | Required |
| `warning` | string | Required |

### Account

| Field | Type | Presence |
| --- | --- | --- |
| `user` | `AccountUser` | Required |
| `serverCount` | integer | Required |
| `version` | string | Required |
| `relaxedSessions` | boolean | Required |

### AccountUser

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Required |
| `username` | string | Required |
| `role` | string | Required |
| `timestamp` | date-time | Optional |
| `ui` | string | Optional |
| `apikey_rotated_at` | date-time | Optional |

### AuthSession

| Field | Type | Presence |
| --- | --- | --- |
| `user` | `AuthUser` | Required |
| `directives` | Array of string | Required |
| `version` | string | Required |
| `oauthClaims` | object | Optional |
| `oauthSubject` | string | Optional |
| `oauthResourceAuthenticated` | boolean | Optional |
| `claims` | Array of `Claim` | Optional |

### AuthUser

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Required |
| `username` | string | Required |
| `email` | string | Required |
| `role` | string | Required |
| `avatarUrl` | string | Optional |

### Branding

| Field | Type | Presence |
| --- | --- | --- |
| `title` | string | Required |
| `logo` | string | Required |
| `favicon` | string | Required |
| `primaryColor` | string | Required |
| `secondaryColor` | string | Required |
| `accentColor` | string | Required |
| `companyName` | string | Required |
| `companyUrl` | string | Required |
| `companyLogoUrl` | string | Required |

### Claim

| Field | Type | Presence |
| --- | --- | --- |
| `type` | string | Required |
| `value` | string | Required |

### ContextGrant

| Field | Type | Presence |
| --- | --- | --- |
| `user_id` | string | Required |
| `username` | string | Required |
| `contextid` | string | Required |
| `label` | string | Optional |
| `role` | string | Required |
| `enabled` | boolean | Required |
| `avatarUrl` | string | Optional |
| `createdAt` | date-time | Optional |
| `updatedAt` | date-time | Optional |

### ContextItem

| Field | Type | Presence |
| --- | --- | --- |
| `item` | `ContextGrant` | Required |

### ContextItems

| Field | Type | Presence |
| --- | --- | --- |
| `items` | Array of `ContextGrant` or null | Required |

### ContextSessionItems

| Field | Type | Presence |
| --- | --- | --- |
| `items` | Array of `Session` or null | Required |
| `servers` | Array of `Session` or null | Required |
| `total` | integer | Required |
| `username` | string | Required |

### DisconnectStats

| Field | Type | Presence |
| --- | --- | --- |
| `total` | integer | Required |
| `recent` | integer | Required |
| `last_at` | date-time | Optional |
| `recent_times` | Array of date-time | Optional |
| `reset_at` | date-time | Optional |

### ListedUser

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Required |
| `username` | string | Required |
| `role` | string | Required |
| `account_type` | string | Required |
| `description` | string | Required |
| `timestamp` | date-time | Required |
| `is_self` | boolean | Required |
| `apikey_configured` | boolean | Required |
| `apikey_rotated_at` | date-time or null | Required |

### LoginConfig

| Field | Type | Presence |
| --- | --- | --- |
| `appTitle` | string | Required |
| `accountSetup` | boolean | Required |
| `accountRegistration` | boolean | Required |
| `version` | string | Required |
| `loginLogo` | string | Required |
| `loginSubtitle` | string | Required |
| `loginWarning` | string | Required |
| `loginFooter` | string | Required |
| `loginLayout` | string | Required |
| `customCss` | string | Required |
| `fontAwesome` | string | Required |
| `googleFonts` | string | Required |
| `sqliteMigrationAvailable` | boolean | Required |
| `oauth` | `OAuthLogin` | Required |
| `branding` | `Branding` | Required |

### LoginResult

| Field | Type | Presence |
| --- | --- | --- |
| `user` | `LoginUser` | Required |
| `version` | string | Required |

### LoginUser

| Field | Type | Presence |
| --- | --- | --- |
| `username` | string | Required |
| `email` | string | Required |

### OAuthExchange

| Field | Type | Presence |
| --- | --- | --- |
| `success` | boolean | Required |
| `token` | string | Required |
| `token_type` | string | Required |
| `expires_in` | integer | Required |
| `username` | string | Required |

### OAuthLogin

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Required |
| `loginUrl` | string | Required |

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

### OwnedContext

| Field | Type | Presence |
| --- | --- | --- |
| `contextid` | string | Required |
| `owner_id` | string | Required |
| `owner` | string | Required |
| `created_at` | date-time | Required |

### OwnedContexts

| Field | Type | Presence |
| --- | --- | --- |
| `items` | Array of `OwnedContext` or null | Required |

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

### Removed

| Field | Type | Presence |
| --- | --- | --- |
| `removed` | boolean | Required |
| `removed_access` | boolean | Optional |

### ResultID

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `id` | string | Required |
| `username` | string | Optional |
| `role` | string | Optional |

### Revoked

| Field | Type | Presence |
| --- | --- | --- |
| `revoked` | boolean | Required |

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

### User

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `id` | string | Required |
| `username` | string | Required |
| `role` | string | Required |
| `account_type` | string | Required |
| `description` | string | Optional |
| `apikey` | string | Optional |
| `apikey_generated` | boolean | Optional |
| `header` | string | Optional |
| `warning` | string | Optional |

### UserRole

| Field | Type | Presence |
| --- | --- | --- |
| `result` | string | Required |
| `id` | string | Required |
| `role` | string | Required |

### Users

| Field | Type | Presence |
| --- | --- | --- |
| `users` | Array of `ListedUser` or null | Required |

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

### whatsapp.ConnectionHealth

| Field | Type | Presence |
| --- | --- | --- |
| `keepalive_failures` | integer | Unspecified |
| `observed_at` | string | Unspecified |
| `reason` | string | Unspecified |
| `send_failures` | integer | Unspecified |
| `status` | string | Unspecified |

## Provider-defined routes

These registered passthrough routes are exempt from fixed QuePasa response schemas.
- `CONNECT /api/v5/auth/oauth/resource/*` (alias `CONNECT /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `DELETE /api/v5/auth/oauth/resource/*` (alias `DELETE /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `GET /api/v5/auth/oauth/resource/*` (alias `GET /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `HEAD /api/v5/auth/oauth/resource/*` (alias `HEAD /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `OPTIONS /api/v5/auth/oauth/resource/*` (alias `OPTIONS /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `PATCH /api/v5/auth/oauth/resource/*` (alias `PATCH /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `POST /api/v5/auth/oauth/resource/*` (alias `POST /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `PUT /api/v5/auth/oauth/resource/*` (alias `PUT /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
- `TRACE /api/v5/auth/oauth/resource/*` (alias `TRACE /api/auth/oauth/resource/*`). The OAuth resource proxy forwards requests to the configured upstream provider. The provider defines the suffix paths, supported methods, response status, content type and schema.
