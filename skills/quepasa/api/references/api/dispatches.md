# Dispatches and dead letters

QuePasa 5.26.1125.1212, canonical API v5.

## Operations

### `DELETE /api/v5/dispatches`

Read or mutate a dispatch configuration by transport.

- Unversioned alias `DELETE /api/dispatches` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token. Select type webhook or rabbitmq, then use that transport's request fields.
- HTTP 200. `api.WebhookResponse` or `api.RabbitMQResponse`.

### `DELETE /api/v5/dispatches/rabbitmq`

Read, create or delete RabbitMQ configurations.

- Unversioned alias `DELETE /api/dispatches/rabbitmq` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token and RabbitMQ configuration or identifiers for mutations.
- HTTP 200. `api.RabbitMQResponse`.

### `DELETE /api/v5/dispatches/webhooks`

Read, create or delete webhook configurations.

- Unversioned alias `DELETE /api/dispatches/webhooks` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token and webhook URL or configuration for mutations.
- HTTP 200. `api.WebhookResponse`.

### `DELETE /api/v5/dlq/{id}`

Delete a dead-letter delivery.

- Unversioned alias `DELETE /api/dlq/{id}` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path id.
- HTTP 200. `DLQDeleted`.

### `GET /api/v5/dispatches`

Read or mutate a dispatch configuration by transport.

- Unversioned alias `GET /api/dispatches` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token. Select type webhook or rabbitmq, then use that transport's request fields.
- HTTP 200. `api.WebhookResponse` or `api.RabbitMQResponse`.

### `GET /api/v5/dispatches/rabbitmq`

Read, create or delete RabbitMQ configurations.

- Unversioned alias `GET /api/dispatches/rabbitmq` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token and RabbitMQ configuration or identifiers for mutations.
- HTTP 200. `api.RabbitMQResponse`.

### `GET /api/v5/dispatches/webhooks`

Read, create or delete webhook configurations.

- Unversioned alias `GET /api/dispatches/webhooks` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token and webhook URL or configuration for mutations.
- HTTP 200. `api.WebhookResponse`.

### `GET /api/v5/dlq`

List dead-letter webhook deliveries.

- Unversioned alias `GET /api/dlq` when canonical aliases are enabled.
- Access. System administrator.
- Request. Query cursor and page size.
- HTTP 200. `DLQPage`.

### `GET /api/v5/dlq/{id}`

Inspect a dead-letter delivery.

- Unversioned alias `GET /api/dlq/{id}` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path id. The payload can contain message data.
- HTTP 200. `DLQEntry`.

### `POST /api/v5/dispatches`

Read or mutate a dispatch configuration by transport.

- Unversioned alias `POST /api/dispatches` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token. Select type webhook or rabbitmq, then use that transport's request fields.
- HTTP 200. `api.WebhookResponse` or `api.RabbitMQResponse`.

### `POST /api/v5/dispatches/rabbitmq`

Read, create or delete RabbitMQ configurations.

- Unversioned alias `POST /api/dispatches/rabbitmq` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token and RabbitMQ configuration or identifiers for mutations.
- HTTP 200. `api.RabbitMQResponse`.

### `POST /api/v5/dispatches/webhooks`

Read, create or delete webhook configurations.

- Unversioned alias `POST /api/dispatches/webhooks` when canonical aliases are enabled.
- Access. Authenticated. Resource-specific ownership and directives still apply.
- Request. Session token and webhook URL or configuration for mutations.
- HTTP 200. `api.WebhookResponse`.

### `POST /api/v5/dlq/{id}/retry`

Retry dispatch of a dead-letter delivery.

- Unversioned alias `POST /api/dlq/{id}/retry` when canonical aliases are enabled.
- Access. System administrator.
- Request. Path id.
- HTTP 200. `DLQRetried`.

## JSON schemas

The field names below use their wire casing. An explicit null is separate from an omitted property.

### DLQDeleted

| Field | Type | Presence |
| --- | --- | --- |
| `deleted` | boolean | Required |
| `id` | string | Required |

### DLQEntry

| Field | Type | Presence |
| --- | --- | --- |
| `id` | string | Required |
| `session_token` | string | Required |
| `webhook_id` | string | Required |
| `destination` | string | Optional |
| `message_id` | string | Optional |
| `error` | string | Required |
| `attempt` | integer | Required |
| `created_at` | date-time | Required |
| `expires_at` | date-time | Required |
| `payload` | JSON value | Optional |
| `payload_stored` | boolean | Required |
| `payload_oversized` | boolean | Optional |

### DLQPage

| Field | Type | Presence |
| --- | --- | --- |
| `items` | Array of `DLQEntry` or null | Required |
| `nextCursor` | string | Required |

### DLQRetried

| Field | Type | Presence |
| --- | --- | --- |
| `retried` | boolean | Required |
| `id` | string | Required |

### api.RabbitMQResponse

| Field | Type | Presence |
| --- | --- | --- |
| `affected` | integer | Unspecified |
| `debug` | Array of string | Unspecified |
| `rabbitmq` | Array of `models.QpRabbitMQConfig` | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |

### api.WebhookResponse

| Field | Type | Presence |
| --- | --- | --- |
| `affected` | integer | Unspecified |
| `debug` | Array of string | Unspecified |
| `status` | string | Unspecified |
| `success` | boolean | Unspecified |
| `webhooks` | Array of `models.QpWebhook` | Unspecified |

### models.QpRabbitMQConfig

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `call_policy` | `whatsapp.NullableCallPolicy` | Unspecified |
| `connection_string` | string | Unspecified |
| `deliveryreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `direct` | `whatsapp.WhatsappBoolean` | Unspecified |
| `exchange_name` | string | Unspecified |
| `extra` | JSON value | Unspecified |
| `failure` | string | Unspecified |
| `forwardinternal` | boolean | Unspecified |
| `groups` | `whatsapp.WhatsappBoolean` | Unspecified |
| `historysyncdays` | integer | Unspecified |
| `messages` | `whatsapp.WhatsappBoolean` | Unspecified |
| `presence` | string | Unspecified |
| `queue_history` | string | Unspecified |
| `readreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `readupdate` | `whatsapp.WhatsappBoolean` | Unspecified |
| `routing_key` | string | Unspecified |
| `success` | string | Unspecified |
| `timestamp` | string | Unspecified |
| `trackid` | string | Unspecified |
| `voipmode` | `whatsapp.VoIPMode` | Unspecified |

### models.QpWebhook

| Field | Type | Presence |
| --- | --- | --- |
| `broadcasts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `call_policy` | `whatsapp.NullableCallPolicy` | Unspecified |
| `deliveryreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `direct` | `whatsapp.WhatsappBoolean` | Unspecified |
| `extra` | JSON value | Unspecified |
| `failure` | string | Unspecified |
| `forwardinternal` | boolean | Unspecified |
| `groups` | `whatsapp.WhatsappBoolean` | Unspecified |
| `historysyncdays` | integer | Unspecified |
| `messages` | `whatsapp.WhatsappBoolean` | Unspecified |
| `presence` | string | Unspecified |
| `readreceipts` | `whatsapp.WhatsappBoolean` | Unspecified |
| `readupdate` | `whatsapp.WhatsappBoolean` | Unspecified |
| `success` | string | Unspecified |
| `timestamp` | string | Unspecified |
| `trackid` | string | Unspecified |
| `url` | string | Unspecified |
| `voipmode` | `whatsapp.VoIPMode` | Unspecified |

### whatsapp.CallPolicy

integer

### whatsapp.NullableCallPolicy

| Field | Type | Presence |
| --- | --- | --- |
| `policy` | `whatsapp.CallPolicy` | Unspecified |
| `valid` | boolean | Unspecified |

### whatsapp.VoIPMode

string

### whatsapp.WhatsappBoolean

integer
