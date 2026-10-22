# Production architecture

Everything runs in the Kubernetes namespace `quepasa-prod` on Sufficit's private k3s cluster.

## Request path

```
client ──HTTPS──▶ quepasa.sufficit.com.br
                    ├─ Traefik route (eveo)            ┐
                    └─ quepasa-prod-edge HAProxy        ├─▶ quepasa-prod-router ─▶ app pod that owns the session
                       (castrum, apoint)                ┘
```

- The DNS name has records for more than one site. Any entry reaches the routers.
- **`quepasa-prod-router`** (3 replicas) looks up which app pod holds each session's lease in the database and forwards the request there.
- A request that reaches a pod that does not own the session gets `503 server not ready yet`. That is why clients must always use the public URL.
- The **Cable** websocket (`wss://…/cable`), used by Hermes/Chatwoot, lives in the memory of the owning pod.

## App pods

| Deployment | Node | Role |
| --- | --- | --- |
| `quepasa-prod-eveo` | eveo | Preferred host. Normally owns every session. |
| `quepasa-prod-castrum` | castrum | Failover |
| `quepasa-prod-apoint` | apoint | Failover |

All three Deployments share these settings:
- `replicas: 1` and `strategy: Recreate`. Two pods with the same host identity must never run at once.
- `imagePullPolicy: Never`. Images are imported into each node's containerd.
- Liveness, readiness and startup probes on `/api/v5/livez`, `/readyz` and `/startupz`.
- Labels `app=quepasa-prod` and `quepasa-node=<site>`.

## Witness

`quepasa-prod-witness` runs on a fourth node.
- **Failover:** after 3 failed liveness checks on the preferred pod, it moves that pod's sessions to a healthy one.
- **Failback:** when the preferred pod has been stable for 300 seconds, it moves the sessions back in batches of 5.

## Data

- **Galera `galera-prod`.** MariaDB, 3 members, local volumes. It holds the database `quepasa`: sessions, runtime leases and the WhatsApp device and key store. The key store is what makes a session usable, which is why copying this database is dangerous (see "Never do" #1 in SKILL.md).
- **Redis `redis-ha` + `redis-sentinel`.** Two data nodes and three Sentinels, AOF every second, no eviction. Holds the message cache, retry queues and the webhook dead-letter queue.

## Authentication

Credentials, from most to least power:

1. **Masterkey.** Everything, including admin routes. For the operator only.
2. **OAuth/OIDC.** Sufficit Identity; for people using the web panel.
3. **Userkey** (`X-QUEPASA-USERKEY`). Every session of one owner.
4. **Session token** (`X-QUEPASA-TOKEN`). One session (one number). The default for integrations and for agents.

Admin routes, such as the DLQ and the Prometheus `/metrics`, need the masterkey or an admin identity.

## Limits and queues

- **API rate limits:** about 600 requests/min, 240 mutations/min, 20 logins/min and 60 admin calls/min.
- **Webhook delivery:** up to 64 concurrent and 1024 pending callbacks; overflow goes to the DLQ.

## Observability

- **Logs:** `kubectl -n quepasa-prod logs deploy/<name>`. App log level is INFO, the WhatsApp library is at WARN, and per-request HTTP logs are off.
- **Metrics:** Prometheus at `/metrics` (admin only). Series include `quepasa_dispatch_*`, `quepasa_redis_message_*` and the WhatsApp risk metrics.
- **Monitoring gap:** at the time of writing, no scrape job or alert rule was installed for this deployment, and the legacy Zabbix check pointed at a retired host. Do not assume an alert would have fired; check directly.

## Test environment

The namespace `quepasa-multisite-test` is a separate copy with its own Galera and Redis, served at `quepasa-test.sufficit.com.br`. It is usually scaled to zero. Never point it at production data.
