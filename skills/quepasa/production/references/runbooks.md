# Production runbooks

Base URL: `https://quepasa.sufficit.com.br`. Namespace: `quepasa-prod`.

Before any procedure that changes something:
- confirm that someone allowed to decide asked for it;
- confirm you hold the grants listed in [grants.md](grants.md);
- note the current state, so you can say what changed.

After it, verify the result and report it with evidence.

## Session not ready

Use this when one number stopped sending or receiving.

1. **Read the state.** Call `GET /api/v5/health` with the session's `X-QUEPASA-TOKEN`. Healthy states are `Ready`, `Synchronizing` (inside its deadline) and `Stopped` (intentional); anything else is a fault.
2. **Read what the session itself recorded:**
   - `GET /api/v5/session/logs`
   - `GET /api/v5/session/events`
3. **Interpret the common states:**
   - **`UnPrepared`.** No connection object is attached yet. This is normal for a few seconds after a pod restart or a failover. If it persists, check that the owning pod is up and look at its logs.
   - **`UnVerified`, logged out, or `StreamReplaced` in the logs.** WhatsApp no longer accepts this device. `StreamReplaced` means another client connected with the same session. Find and stop that client before re-pairing, or the next pairing breaks again. The number then needs a [re-pair](#re-pair-a-session).
   - **Disconnected or reconnecting loops.** Look at the owning pod's logs. A pod-wide problem shows on many sessions at once; one session alone points to that account.
4. **If several sessions are affected,** check the pods, then [Galera](#galera) and [Redis](#redis).

## Re-pair a session

This needs the session token and a person with the phone in hand.

1. Make sure no other client runs this session (see "Never do" #1 in SKILL.md).
2. Get a QR code with `GET /api/v5/session/qrcode`, or a pairing code with `GET /api/v5/session/paircode?phone=<digits>`.
3. Deliver it privately to the phone's owner. Never post it in a group, because it grants the account. It expires quickly, so generate a fresh one if needed.
4. After the owner scans or enters it, poll `GET /api/v5/health` with the token until the state is `Ready`.
5. Send a test message only if the owner asked for one.

## Session control

All of these take the session token:

| Action | Call | Note |
| --- | --- | --- |
| Restart | `POST /api/v5/session/restart` | Reconnects the same device. Use it for a stuck session. |
| Disable | `POST /api/v5/session/disable` | Stops the session. The resulting `Stopped` state is healthy. |
| Enable | `POST /api/v5/session/enable` | Starts it again. |
| Reset disconnect counter | `POST /api/v5/session/disconnects/reset` | Only after the cause is fixed. |

Restarting or disabling interrupts that number's traffic, so only do it on request. Say which number and session (by id, never the token) you acted on.

## Webhook dead letters

When a receiver (Fleet, Chatwoot, n8n…) refuses or times out, QuePasa keeps the event in the DLQ. By default it keeps 168 hours, up to 10,000 entries, with payloads up to 1 MiB.

The DLQ routes are admin routes:

1. List the entries with `GET /api/v5/dlq`, and inspect one with `GET /api/v5/dlq/{id}`.
2. Fix the receiver first. Replaying into a receiver that is still broken just refills the queue.
3. Replay entries one by one with `POST /api/v5/dlq/{id}/retry`, or in small batches. Replays are not deduplicated by QuePasa, so a receiver without idempotency may process an event twice; say so before replaying.
4. Delete an entry with `DELETE /api/v5/dlq/{id}` only when it is confirmed useless.

## Pause and restore the witness

The witness moves sessions between pods by itself. Pause it during maintenance so it does not fight the change:

1. Record its replica count: `kubectl -n quepasa-prod get deploy quepasa-prod-witness -o jsonpath='{.spec.replicas}'`.
2. Pause it: `kubectl -n quepasa-prod scale deploy/quepasa-prod-witness --replicas=0`.
3. When the maintenance is over and the sessions are back, restore the recorded count. Never leave it paused: without it, a failed preferred pod keeps its sessions down.

## Roll out a new image

The order is fixed: **apoint, then castrum, then eveo last**, because eveo is the preferred host.

1. **Build the image.** Use an immutable tag `<feature>-<version>-<sha12>`. Production pulls nothing (`imagePullPolicy: Never`): the image must be imported into containerd on all three nodes before any pod uses it. Keep the current image imported too, for rollback.
2. **Save the rollback template.** Save each app Deployment's current spec (`kubectl -n quepasa-prod get deploy quepasa-prod-<site> -o yaml`), together with the list of sessions that are `Ready` now.
3. [Pause the witness.](#pause-and-restore-the-witness)
4. **Replace one site.** Change only the image of one Deployment. Run a server-side dry-run first (`kubectl patch … --dry-run=server`), then apply it. `Recreate` stops the old pod before the new one starts; expect about 4–6 seconds of `503` for that site's sessions.
5. **Validate before moving to the next site:**
   - the new pod is ready with zero restarts;
   - it runs the expected binary or version;
   - there are no fatal startup lines;
   - every session that was `Ready` before is `Ready` again.

   Galera deadlocks (`1213`) at startup are transient; repeated ones are not.
6. Repeat steps 4 and 5 for castrum, then for eveo.
7. Restore the witness. Check `/api/v5/system/version` and the dependent systems listed in SKILL.md.

## Roll back

1. Pause the witness.
2. Restore only the affected Deployment from its saved template. Its image is still imported on the node.
3. Confirm that its sessions return to `Ready`.
4. Restore the witness.
5. Report what was rolled back and why.

## Galera

There are three MariaDB members. QuePasa needs a Primary component to read and write sessions.

1. **Check the members:** `kubectl -n quepasa-prod get pods -l app=galera-prod`. On each member, run `SHOW STATUS LIKE 'wsrep_%'` and look at `wsrep_cluster_status` (`Primary`), `wsrep_local_state_comment` (`Synced`) and `wsrep_cluster_size` (`3`).
2. **One member down.** The other two keep quorum. Let it rejoin by itself (state transfer via mariabackup) and do not restart the healthy ones.
3. **Two members down, or no Primary.** Sessions stop. Escalate to the owner before any bootstrap. Bootstrapping the wrong member loses data.
4. **No backup.** No backup job for this cluster was found. Never delete a member's volume.

## Redis

`redis-ha` has two data nodes behind three Sentinels (master name `quepasa-prod`, quorum 2). QuePasa follows Sentinel, so a failover needs no restart.

1. **Find the master:** `kubectl -n quepasa-prod exec redis-sentinel-0 -- redis-cli -p 26379 SENTINEL get-master-addr-by-name quepasa-prod`.
2. **A data pod restarts.** Its init step asks the Sentinels who the master is, and the pod rejoins as a replica.
3. **Losing Redis loses the in-flight cache, retry queues and the DLQ,** not the sessions, which live in Galera. Check the DLQ before and after any Redis maintenance.
