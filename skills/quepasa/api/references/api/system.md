# Health, capabilities, audit and jobs

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `GET /api/v5/audit`

List HTTP API audit entries.

- Unversioned alias `GET /api/audit` when canonical aliases are enabled.
- Access. System administrator.
- Request. Query filters and pagination.
- HTTP 200. `AuditPage`.

### `GET /api/v5/capabilities`

Inspect features and directives for the authenticated principal.

- Unversioned alias `GET /api/capabilities` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. No request parameters.
- HTTP 200. `Capabilities`.

### `GET /api/v5/health`

Read the compatibility health report.

- Unversioned alias `GET /api/health` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. An authorized request can expose additional diagnostics.
- HTTP 200. `api.HealthResponse`.

### `GET /api/v5/jobs`

List visible background jobs.

- Unversioned alias `GET /api/jobs` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Query filters and pagination.
- HTTP 200. `JobPage`.

### `GET /api/v5/jobs/{id}`

Read a background job by ID.

- Unversioned alias `GET /api/jobs/{id}` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Path id.
- HTTP 200. `Job`.

### `GET /api/v5/livez`

Probe process liveness.

- Unversioned alias `GET /api/livez` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. No request parameters.
- HTTP 200. `Probe`.

### `GET /api/v5/readyz`

Probe readiness to accept traffic.

- Unversioned alias `GET /api/readyz` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. Check both HTTP status and status field.
- HTTP 200. `Probe`.

### `GET /api/v5/startupz`

Probe completion of gateway startup.

- Unversioned alias `GET /api/startupz` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. Check both HTTP status and status field.
- HTTP 200. `Probe`.

### `GET /api/v5/system/environment`

Read the public environment preview.

- Unversioned alias `GET /api/system/environment` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. No request parameters.
- HTTP 200. `api.EnvironmentResponse`.

### `GET /api/v5/system/health`

Read gateway health and the installed version.

- Unversioned alias `GET /api/system/health` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. An authorized request can expose additional diagnostics.
- HTTP 200. `api.HealthResponse`.

### `GET /api/v5/system/version`

Read the installed QuePasa version.

- Unversioned alias `GET /api/system/version` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. No request parameters.
- HTTP 200. `Version`.

### `HEAD /api/v5/health`

Check the compatibility health endpoint without a response body.

- Unversioned alias `HEAD /api/health` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. No request parameters.
- HTTP 200. Empty body.

### `HEAD /api/v5/system/health`

Check gateway health without a response body.

- Unversioned alias `HEAD /api/system/health` when canonical aliases are enabled.
- Access. Public. Some routes expose additional fields to an authenticated caller.
- Request. No request parameters.
- HTTP 200. Empty body.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### AuditPage

| Field | Type | Presence |
| --- | --- | --- |
| `items` | Array of `AuditRecord` or null | Required |
| `nextCursor` | string | Required |

### AuditRecord

| Field | Type | Presence |
| --- | --- | --- |
| `ID` | string | Required |
| `Actor` | string | Required |
| `Method` | string | Required |
| `Route` | string | Required |
| `Status` | string | Required |
| `Action` | string | Required |
| `Target` | string | Required |
| `timestamp` | date-time | Required |

### Capabilities

| Field | Type | Presence |
| --- | --- | --- |
| `apiVersion` | string | Required |
| `features` | Array of string | Required |
| `directives` | Array of string | Required |

### Job

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Required |
| `type` | string | Required |
| `status` | string | Required |
| `createdAt` | date-time | Required |
| `updatedAt` | date-time | Required |

### JobPage

| Field | Type | Presence |
| --- | --- | --- |
| `items` | Array of `Job` or null | Required |
| `nextCursor` | string | Required |

### Probe

| Field | Type | Presence |
| --- | --- | --- |
| `status` | string | Required |

### Version

| Field | Type | Presence |
| --- | --- | --- |
| `version` | string | Required |

### api.EnvironmentResponse

| Field | Type | Presence |
| --- | --- | --- |
| `debug` | Array of string | Unspecified |
| `preview` | `environment.EnvironmentSettingsPreview` | Unspecified |
| `settings` | `environment.EnvironmentSettings` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### api.HealthResponse

| Field | Type | Presence |
| --- | --- | --- |
| `assignedHost` | string | Unspecified |
| `commandAvailable` | boolean | Unspecified |
| `connection_health` | `whatsapp.ConnectionHealth` | Unspecified |
| `debug` | Array of string | Unspecified |
| `diagnostic` | `models.QpConnectionDiagnostic` | Unspecified |
| `items` | Array of `api.HealthResponseItem` | Unspecified |
| `managedHere` | boolean | Unspecified |
| `metaCoexistence` | boolean | Unspecified |
| `runtimeHost` | string | Unspecified |
| `runtimeLeaseExpiresAt` | string | Unspecified |
| `runtimeObservedAt` | string | Unspecified |
| `runtimeOwnership` | string | Unspecified |
| `runtimeRemote` | boolean | Unspecified |
| `runtimeStale` | boolean | Unspecified |
| `runtimeState` | string | Unspecified |
| `servingHost` | string | Unspecified |
| `state` | `whatsapp.WhatsappConnectionState` | Unspecified |
| `stats` | `api.HealthStats` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `timestamp` | string | Unspecified |
| `uptime` | object | Unspecified |
| `version` | string | Unspecified |
| `wid` | string | Unspecified |

### api.HealthResponseItem

| Field | Type | Presence |
| --- | --- | --- |
| `assignedHost` | string | Unspecified |
| `commandAvailable` | boolean | Unspecified |
| `connection_health` | `whatsapp.ConnectionHealth` | Unspecified |
| `diagnostic` | `models.QpConnectionDiagnostic` | Unspecified |
| `managedHere` | boolean | Unspecified |
| `metaCoexistence` | boolean | Unspecified |
| `runtimeHost` | string | Unspecified |
| `runtimeLeaseExpiresAt` | string | Unspecified |
| `runtimeObservedAt` | string | Unspecified |
| `runtimeOwnership` | string | Unspecified |
| `runtimeRemote` | boolean | Unspecified |
| `runtimeStale` | boolean | Unspecified |
| `servingHost` | string | Unspecified |
| `state` | `whatsapp.WhatsappConnectionState` | Unspecified |
| `state_code` | integer | Unspecified |
| `token` | string | Unspecified |
| `wid` | string | Unspecified |

### api.HealthStats

| Field | Type | Presence |
| --- | --- | --- |
| `healthy` | integer | Unspecified |
| `percentage` | number | Unspecified |
| `total` | integer | Unspecified |
| `unhealthy` | integer | Unspecified |

### environment.APISettings

| Field | Type | Presence |
| --- | --- | --- |
| `allow_ownerless_sessions` | boolean | Unspecified |
| `allowed_origins` | Array of string | Unspecified |
| `default_version` | string | Unspecified |
| `jwt_cookie_secure` | boolean | Unspecified |
| `jwt_ttl_minutes` | integer | Unspecified |
| `outbound_send_timeout_ms` | integer | Unspecified |
| `password` | string | Unspecified |
| `prefix` | string | Unspecified |
| `profile_picture_cache_seconds` | integer | Unspecified |
| `relaxed_sessions` | boolean | Unspecified |
| `signing_secret` | string | Unspecified |
| `timeout` | integer | Unspecified |
| `use_ssl_websocket` | boolean | Unspecified |
| `user` | string | Unspecified |
| `webhook_timeout` | integer | Unspecified |

### environment.AuthorizationSettings

| Field | Type | Presence |
| --- | --- | --- |
| `bootstrap_contexts` | string | Unspecified |
| `bootstrap_password_file` | string | Unspecified |
| `bootstrap_role` | string | Unspecified |
| `bootstrap_user` | string | Unspecified |

### environment.BrandingSettings

| Field | Type | Presence |
| --- | --- | --- |
| `accentColor` | string | Unspecified |
| `avatar_url_template` | string | Unspecified |
| `companyName` | string | Unspecified |
| `companyUrl` | string | Unspecified |
| `company_logo_url` | string | Unspecified |
| `context_avatar_url_template` | string | Unspecified |
| `favicon` | string | Unspecified |
| `logo` | string | Unspecified |
| `primaryColor` | string | Unspecified |
| `secondaryColor` | string | Unspecified |
| `title` | string | Unspecified |

### environment.CableBackplaneSettings

| Field | Type | Presence |
| --- | --- | --- |
| `cluster_size` | integer | Unspecified |
| `enabled` | boolean | Unspecified |

### environment.CacheSettings

| Field | Type | Presence |
| --- | --- | --- |
| `backend` | string | Unspecified |
| `disk_path` | string | Unspecified |
| `hot_window_days` | integer | Unspecified |
| `init_fallback` | boolean | Unspecified |

### environment.CallsSettings

| Field | Type | Presence |
| --- | --- | --- |
| `ended_display_seconds` | integer | Unspecified |
| `history_limit` | integer | Unspecified |
| `history_retention_seconds` | integer | Unspecified |
| `media_failure_timeout_seconds` | integer | Unspecified |
| `media_initial_timeout_seconds` | integer | Unspecified |
| `media_relay_reconnect_attempts` | integer | Unspecified |

### environment.ConnectivitySettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `interval_seconds` | integer | Unspecified |
| `timeout_seconds` | integer | Unspecified |

### environment.DLQSettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `max_entries` | integer | Unspecified |
| `max_payload_bytes` | integer | Unspecified |
| `retention_hours` | integer | Unspecified |
| `store_payload` | boolean | Unspecified |

### environment.DashboardSettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `prefix` | string | Unspecified |

### environment.DatabaseOutageSendSettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `store_path` | string | Unspecified |

### environment.DatabaseSettings

| Field | Type | Presence |
| --- | --- | --- |
| `database` | string | Unspecified |
| `driver` | string | Unspecified |
| `host` | string | Unspecified |
| `password` | string | Unspecified |
| `port` | string | Unspecified |
| `ssl_mode` | string | Unspecified |
| `user` | string | Unspecified |

### environment.EnvironmentSettings

| Field | Type | Presence |
| --- | --- | --- |
| `api` | `environment.APISettings` | Unspecified |
| `authorization` | `environment.AuthorizationSettings` | Unspecified |
| `branding` | `environment.BrandingSettings` | Unspecified |
| `cableBackplane` | `environment.CableBackplaneSettings` | Unspecified |
| `cache` | `environment.CacheSettings` | Unspecified |
| `calls` | `environment.CallsSettings` | Unspecified |
| `connectivity` | `environment.ConnectivitySettings` | Unspecified |
| `database` | `environment.DatabaseSettings` | Unspecified |
| `databaseOutageSend` | `environment.DatabaseOutageSendSettings` | Unspecified |
| `dlq` | `environment.DLQSettings` | Unspecified |
| `form` | `environment.FormSettings` | Unspecified |
| `general` | `environment.GeneralSettings` | Unspecified |
| `mcp` | `environment.MCPSettings` | Unspecified |
| `messages` | `environment.MessageSettings` | Unspecified |
| `metrics` | `environment.MetricsSettings` | Unspecified |
| `oauth` | `environment.OAuthSettings` | Unspecified |
| `outboundRetry` | `environment.OutboundRetrySettings` | Unspecified |
| `rabbitMQ` | `environment.RabbitMQSettings` | Unspecified |
| `redis` | `environment.RedisSettings` | Unspecified |
| `security` | `environment.SecuritySettings` | Unspecified |
| `sessionRouting` | `environment.SessionRoutingSettings` | Unspecified |
| `sessionSnapshot` | `environment.SessionSnapshotSettings` | Unspecified |
| `sipproxy` | `environment.SIPProxySettings` | Unspecified |
| `swagger` | `environment.SwaggerSettings` | Unspecified |
| `webServer` | `environment.WebServerSettings` | Unspecified |
| `whatsApp` | `environment.WhatsAppSettings` | Unspecified |
| `whatsFuck` | `environment.WhatsFuckSettings` | Unspecified |

### environment.EnvironmentSettingsPreview

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | string | Unspecified |
| `calls` | string | Unspecified |
| `db_log_level` | string | Unspecified |
| `default_api_version` | string | Unspecified |
| `delivery_receipts` | string | Unspecified |
| `groups` | string | Unspecified |
| `history_sync` | string | Unspecified |
| `log_level` | string | Unspecified |
| `presence` | string | Unspecified |
| `read_receipts` | string | Unspecified |
| `read_update` | string | Unspecified |
| `rerequest_from_phone` | string | Unspecified |
| `retry_message_store` | string | Unspecified |
| `wakeup_duration` | string | Unspecified |
| `wakeup_hour` | string | Unspecified |

### environment.FormSettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `prefix` | string | Unspecified |

### environment.GeneralSettings

| Field | Type | Presence |
| --- | --- | --- |
| `account_setup` | boolean | Unspecified |
| `app_title` | string | Unspecified |
| `attachment_protection_hours` | integer | Unspecified |
| `cache_days` | integer | Unspecified |
| `cache_length` | integer | Unspecified |
| `compatible_mime_as_audio` | boolean | Unspecified |
| `convert_png_to_jpg` | boolean | Unspecified |
| `convert_wave_to_ogg` | boolean | Unspecified |
| `force_audio_as_ptt` | boolean | Unspecified |
| `graceful_restart_timeout_seconds` | integer | Unspecified |
| `log_level` | string | Unspecified |
| `login_custom_css` | string | Unspecified |
| `login_font_awesome` | string | Unspecified |
| `login_footer` | string | Unspecified |
| `login_google_fonts` | string | Unspecified |
| `login_layout` | string | Unspecified |
| `login_logo` | string | Unspecified |
| `login_subtitle` | string | Unspecified |
| `login_warning` | string | Unspecified |
| `migrations` | string | Unspecified |
| `normalize_br_phone` | boolean | Unspecified |
| `server_host` | string | Unspecified |
| `synopsis_length` | integer | Unspecified |
| `testing` | boolean | Unspecified |

### environment.MCPSettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `path` | string | Unspecified |

### environment.MessageSettings

| Field | Type | Presence |
| --- | --- | --- |
| `dispatch_types` | Map of boolean | Unspecified |
| `retention_days` | integer | Unspecified |
| `send_burst` | integer | Unspecified |
| `send_max_wait_milliseconds` | integer | Unspecified |
| `send_rate_limit_enabled` | boolean | Unspecified |
| `send_rate_limit_observe_only` | boolean | Unspecified |
| `send_rate_per_minute` | integer | Unspecified |
| `send_recipient_burst` | integer | Unspecified |
| `send_recipient_per_minute` | integer | Unspecified |

### environment.MetricsSettings

| Field | Type | Presence |
| --- | --- | --- |
| `dashboard` | `environment.DashboardSettings` | Unspecified |
| `enabled` | boolean | Unspecified |
| `prefix` | string | Unspecified |

### environment.OAuthSettings

| Field | Type | Presence |
| --- | --- | --- |
| `auto_provision` | boolean | Unspecified |
| `claim_role_mappings` | Map of string | Unspecified |
| `client_id` | string | Unspecified |
| `client_secret` | string | Unspecified |
| `context_claim_entry_pattern` | string | Unspecified |
| `context_claim_mapping_enabled` | boolean | Unspecified |
| `context_claim_names` | Array of string | Unspecified |
| `enabled` | boolean | Unspecified |
| `provider_url` | string | Unspecified |
| `redirect_uri` | string | Unspecified |
| `resource_url` | string | Unspecified |
| `scopes` | Array of string | Unspecified |

### environment.OutboundRetrySettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |

### environment.RabbitMQSettings

| Field | Type | Presence |
| --- | --- | --- |
| `cache_backend` | string | Unspecified |
| `cache_disk_path` | string | Unspecified |
| `cache_length` | integer | Unspecified |
| `cache_queue_key` | string | Unspecified |

### environment.RedisSettings

| Field | Type | Presence |
| --- | --- | --- |
| `database` | integer | Unspecified |
| `dial_timeout_seconds` | integer | Unspecified |
| `host` | string | Unspecified |
| `key_prefix` | string | Unspecified |
| `max_retries` | integer | Unspecified |
| `password` | string | Unspecified |
| `pool_size` | integer | Unspecified |
| `port` | integer | Unspecified |
| `read_timeout_seconds` | integer | Unspecified |
| `sentinel_addresses` | Array of string | Unspecified |
| `sentinel_master` | string | Unspecified |
| `sentinel_password` | string | Unspecified |
| `username` | string | Unspecified |
| `write_timeout_seconds` | integer | Unspecified |

### environment.SIPProxySettings

| Field | Type | Presence |
| --- | --- | --- |
| `codecs` | string | Unspecified |
| `enable_transcoding` | boolean | Unspecified |
| `enabled` | boolean | Unspecified |
| `host` | string | Unspecified |
| `invite_allowed_ips` | string | Unspecified |
| `invite_rate_limit_rpm` | integer | Unspecified |
| `invite_timeout_seconds` | integer | Unspecified |
| `legacy_voip` | boolean | Unspecified |
| `local_port` | integer | Unspecified |
| `log_level` | string | Unspecified |
| `media_ports` | string | Unspecified |
| `port` | integer | Unspecified |
| `protocol` | string | Unspecified |
| `public_host` | string | Unspecified |
| `public_ip` | string | Unspecified |
| `register_default_expiry` | integer | Unspecified |
| `register_enabled` | boolean | Unspecified |
| `register_max_contacts` | integer | Unspecified |
| `register_max_expiry` | integer | Unspecified |
| `register_min_expiry` | integer | Unspecified |
| `register_rate_limit_rpm` | integer | Unspecified |
| `register_realm` | string | Unspecified |
| `register_require_password` | boolean | Unspecified |
| `register_wss_enabled` | boolean | Unspecified |
| `retries` | integer | Unspecified |
| `sdp_session_name` | string | Unspecified |
| `stun_server` | string | Unspecified |
| `timeout` | integer | Unspecified |
| `use_upnp` | boolean | Unspecified |
| `user_agent` | string | Unspecified |

### environment.SecuritySettings

| Field | Type | Presence |
| --- | --- | --- |
| `dispatch_max_concurrent_callbacks` | integer | Unspecified |
| `dispatch_max_pending_callbacks` | integer | Unspecified |
| `max_json_body_bytes` | integer | Unspecified |
| `max_multipart_body_bytes` | integer | Unspecified |
| `outbound_allowed_private_hosts` | Array of string | Unspecified |
| `outbound_dial_timeout_seconds` | integer | Unspecified |
| `outbound_keepalive_seconds` | integer | Unspecified |
| `outbound_max_redirects` | integer | Unspecified |
| `outbound_response_max_bytes` | integer | Unspecified |
| `outbound_timeout_seconds` | integer | Unspecified |
| `rate_limit_admin_rpm` | integer | Unspecified |
| `rate_limit_login_rpm` | integer | Unspecified |
| `rate_limit_mutation_rpm` | integer | Unspecified |
| `rate_limit_rpm` | integer | Unspecified |
| `webhook_require_safe_egress` | boolean | Unspecified |

### environment.SessionRoutingSettings

| Field | Type | Presence |
| --- | --- | --- |
| `cache_ttl_ms` | integer | Unspecified |
| `dial_timeout_ms` | integer | Unspecified |
| `enabled` | boolean | Unspecified |
| `json_probe_bytes` | integer | Unspecified |
| `max_replay_bytes` | integer | Unspecified |
| `request_timeout_ms` | integer | Unspecified |
| `resolve_timeout_ms` | integer | Unspecified |
| `response_header_timeout_ms` | integer | Unspecified |
| `url_template` | string | Unspecified |

### environment.SessionSnapshotSettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `max_age_seconds` | integer | Unspecified |

### environment.SwaggerSettings

| Field | Type | Presence |
| --- | --- | --- |
| `enabled` | boolean | Unspecified |
| `prefix` | string | Unspecified |

### environment.WebServerSettings

| Field | Type | Presence |
| --- | --- | --- |
| `base_url` | string | Unspecified |
| `default_app` | string | Unspecified |
| `dev_frontend` | boolean | Unspecified |
| `frontend_dev_port` | string | Unspecified |
| `frontend_host` | string | Unspecified |
| `host` | string | Unspecified |
| `idle_timeout_seconds` | integer | Unspecified |
| `logs` | boolean | Unspecified |
| `max_header_bytes` | integer | Unspecified |
| `port` | integer | Unspecified |
| `read_header_timeout_seconds` | integer | Unspecified |
| `read_timeout_seconds` | integer | Unspecified |
| `shutdown_timeout_seconds` | integer | Unspecified |
| `write_timeout_seconds` | integer | Unspecified |

### environment.WhatsAppSettings

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | `whatsapp.WhatsappBooleanExtended` | Unspecified |
| `calls` | `whatsapp.WhatsappBooleanExtended` | Unspecified |
| `delivery_receipts` | `whatsapp.WhatsappBooleanExtended` | Unspecified |
| `groups` | `whatsapp.WhatsappBooleanExtended` | Unspecified |
| `history_sync_days` | integer | Unspecified |
| `messages` | `whatsapp.WhatsappBooleanExtended` | Unspecified |
| `presence` | string | Unspecified |
| `read_receipts` | `whatsapp.WhatsappBooleanExtended` | Unspecified |
| `read_update` | `whatsapp.WhatsappBooleanExtended` | Unspecified |
| `wakeup_duration` | integer | Unspecified |
| `wakeup_hour` | string | Unspecified |

### environment.WhatsFuckSettings

| Field | Type | Presence |
| --- | --- | --- |
| `dispatch_unhandled` | boolean | Unspecified |
| `whatsfuck_db_log_level` | string | Unspecified |
| `whatsfuck_log_level` | string | Unspecified |
| `whatsfuck_profile_picture_timeout_seconds` | integer | Unspecified |
| `whatsfuck_rerequest_from_phone` | boolean | Unspecified |
| `whatsfuck_use_retry_message_store` | boolean | Unspecified |

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

### whatsapp.WhatsappBooleanExtended

integer

### whatsapp.WhatsappConnectionState

integer
