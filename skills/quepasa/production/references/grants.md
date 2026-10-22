# Grants per task

An agent does not get these by default. Each one is granted by the operator, scoped to the task, and should be revoked when no longer needed.

If a task needs a grant you do not hold, stop and name the missing grant. Never borrow another system's credential, never read a secret you were not given, and never widen your own access.

| Task | Minimum grant |
| --- | --- |
| Public health and version | None |
| Health, logs and events of one session | That session's token (`X-QUEPASA-TOKEN`) |
| Re-pair, restart, enable or disable one session | That session's token, plus a request from the number's owner or an operator |
| List sessions of one owner | Userkey of that owner, used only for that owner's sessions |
| DLQ list, inspect, retry or delete; `/metrics` | Masterkey or an admin identity (operator-level) |
| Read pods, logs and events in `quepasa-prod` | Kubernetes read role on the namespace: `get`, `list` and `watch` on pods, deployments and events, plus `pods/log` |
| Run a read-only command inside a pod (e.g. `redis-cli`, a Galera status query) | `pods/exec` in `quepasa-prod`, with read-only use declared |
| Pause/restore the witness, scale or patch app Deployments (rollout, rollback) | Kubernetes write role on deployments in `quepasa-prod`, granted for the maintenance window |
| Import an image into the nodes | Node-level access to containerd on the three app nodes (operator only) |
| Galera bootstrap or any destructive database action | Operator only. Never delegated to an agent. |

## How to ask

Name the task, the grant you need, its scope (one session, or one namespace) and how long you need it. For example: "To read the logs of the pod that owns the Fleet session, I need read access to pods and logs in `quepasa-prod` for this diagnosis."
