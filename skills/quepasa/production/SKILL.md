---
name: quepasa-production
description: "Operate Sufficit's production QuePasa (WhatsApp gateway) on Kubernetes — check health, diagnose a session or a failed send, read logs and metrics, re-pair or restart a session, replay webhook dead letters, roll out or roll back a new image and handle Galera/Redis — with the grants each task needs and the rules that keep WhatsApp sessions from being corrupted. Use when the request is about the production QuePasa service itself (is it up, why a number stopped sending, deploy/rollback, failover), not just calling its API."
metadata:
  version: "0.1.0"
---

# QuePasa in production (Sufficit)

This skill covers **operating** the production QuePasa deployment. To call the API as a client (send, groups, media, webhooks), use the `quepasa-api` skill. Architecture details are in [references/architecture.md](references/architecture.md); step-by-step procedures are in [references/runbooks.md](references/runbooks.md); the access each task needs is in [references/grants.md](references/grants.md).

## Never do

1. **Never run two clients on the same WhatsApp session.** A second runtime (an old container or VM, a copied database, a test environment pointed at production data, a pod scaled up beside another) causes `StreamReplaced` and can corrupt the session's encryption keys. Then the number has to be paired again. Before booting any copy of the database, clear the device table (`whatsmeow_device`).
2. **Never re-apply the repository manifests blindly.** Images are swapped out-of-band; the manifest's image tag can be older than what runs. Patch only what you are changing, after a server-side dry-run.
3. **Never restart, scale or delete without an explicit request** from someone allowed to make that decision. Diagnosis is read-only by default.
4. **Never print secrets.** No masterkey, userkey, session token, database password or signing secret in replies, logs, commands you echo, files or tickets. Mask as `abcd…` when you must refer to one.
5. **Never use a userkey or the masterkey for something a session token can do.** The userkey sees every session of its owner; the masterkey sees everything.

## What runs where (summary)

- Kubernetes namespace **`quepasa-prod`** on the Sufficit k3s cluster.
- One app Deployment per site, each with `replicas: 1` and `strategy: Recreate`, pinned to its node: `quepasa-prod-eveo` (preferred host), `quepasa-prod-castrum`, `quepasa-prod-apoint`.
- **`quepasa-prod-router`** sends each request to the pod that owns the session lease.
- **`quepasa-prod-edge`** (HAProxy) and a Traefik route expose the public URL.
- **`quepasa-prod-witness`** moves sessions to a healthy pod when the preferred one fails, and moves them back after it is stable.
- **Galera** `galera-prod` (MariaDB, 3 members) holds the app tables and the WhatsApp key store.
- **Redis** (`redis-ha` with Sentinel, master name `quepasa-prod`) holds the message cache, retry queues and the webhook dead-letter queue (DLQ).
- Public URL: `https://quepasa.sufficit.com.br`. Never call a pod directly: a non-owner pod answers `503 server not ready yet`.

## First look: is it up?

Run these in order and stop at the first failure.

1. **Public endpoints** (no credential needed):
   - `GET https://quepasa.sufficit.com.br/api/v5/health`
   - `GET https://quepasa.sufficit.com.br/api/v5/system/version`

   A version answer proves the edge, the router and at least one app pod are serving.
2. **Workloads:** `kubectl -n quepasa-prod get deploy,pods -o wide`.
   - The three app pods should be `1/1` with no recent restarts.
   - The router, the edge and the witness should be up.
3. **One session:** call `GET /api/v5/health` with that session's `X-QUEPASA-TOKEN`.
   - Healthy states are `Ready`, `Synchronizing` (inside its deadline) and `Stopped` (intentional).
   - Any other state is a fault; see [runbooks](references/runbooks.md#session-not-ready).
4. **Logs of the pod that owns the session:** `kubectl -n quepasa-prod logs deploy/quepasa-prod-<site> --since=30m`. Look for `StreamReplaced`, logout, `UnVerified`, Galera `1213` deadlocks or Redis errors.

Report what you checked, what each check returned and the conclusion. If something failed, say exactly which check failed and how.

## A message did not go out

Work from the specific send outward:

1. **The API answer.** `success:false` is a failure even with HTTP 200; read its `status` text.
2. **The recipient.**
   - Wrong or outdated number (extra or missing digit 9, missing country code).
   - A `@lid` contact that must be resolved first (`GET /api/v5/contacts/identifier`).
   - The contact blocked the number.
3. **Scope of the failure.** If other chats on the same session are sending, the gateway is fine and the problem is that contact. If every chat on the session fails, check the session state. If every session fails, check the cluster.
4. **Webhook side.** Inbound events that the receiver refused go to the DLQ; see [runbooks](references/runbooks.md#webhook-dead-letters).

## Managing it

Each procedure needs the grants listed in [references/grants.md](references/grants.md). If you lack a grant, stop and say which one is missing; do not look for a way around it.

| Task | Procedure |
| --- | --- |
| Re-pair a number (QR or pairing code) | [runbooks › re-pair](references/runbooks.md#re-pair-a-session) |
| Restart / enable / disable one session | [runbooks › session control](references/runbooks.md#session-control) |
| Replay webhook dead letters | [runbooks › DLQ](references/runbooks.md#webhook-dead-letters) |
| Roll out a new image | [runbooks › rollout](references/runbooks.md#roll-out-a-new-image) |
| Roll back | [runbooks › rollback](references/runbooks.md#roll-back) |
| Pause/restore the witness | [runbooks › witness](references/runbooks.md#pause-and-restore-the-witness) |
| Galera member down / desynced | [runbooks › Galera](references/runbooks.md#galera) |
| Redis master failover | [runbooks › Redis](references/runbooks.md#redis) |

## Systems that depend on it

Tell their owners before maintenance and check them afterwards:

- **Sufficit Fleet.** WhatsApp groups and private chats use v5 messages, groups, presence and media. Inbound events reach Fleet through a webhook.
- **Sufficit AI Genius.** The WhatsApp tools use v5 and an OAuth exchange.
- **Hermes/Chatwoot `channel-quepasa`.** Inbound arrives through a per-inbox webhook, plus the Cable websocket, which lives only on the pod that owns the session.
- **Sufficit endpoints/Blazor and Asterisk routing.** These go through the Sufficit QuePasa gateway library. Asterisk WhatsApp routes reference session ids or tokens; trace a live call before "fixing" a mismatch.
