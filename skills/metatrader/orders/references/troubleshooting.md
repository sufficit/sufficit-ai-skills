# Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `initialize` → `(-10005, 'IPC timeout')` | Terminal not logged in, still recompiling/updating, different display/user, or broker demanding a password change | Check the terminal journal; log in first; wait for startup; same `DISPLAY` for terminal and Python |
| Journal: `master password must be changed` | Broker (XP) requires changing the initial password | User changes it in the broker app, updates the Vault entry, retry |
| Generic MT5 reads `login.ini` but never connects | Server unknown to the generic build | Install the broker's own MT5 |
| Journal: `Service is not available` | Broker server side issue or off-hours maintenance | Wait and retry later; not a password problem |
| `cannot load config` | Broken quoting of `/config:` path | Pass `'/config:C:\login.ini'` as one argument |
| Shell exits 143 | `pkill -f terminal64.exe` killed its own command | Use a separate script with `pgrep` |
| Vault resolve fails with outdated credentials | Session authentication expired | Ask the user to renew the environment authentication; do not loop `mcp_refresh` |
| `order_check` → `No money` | No balance | Expected before a deposit |

Also review the broker's access notifications with the user: successful logins from the
cloud environment show its IP and time (convert to the user's time zone).
