---
name: routeros-management
description: "Administer MikroTik RouterOS v7 and CHR with CLI, SSH and REST; diagnose interfaces, IP, DHCP, DNS, routing, firewall, NAT, VPN, Wi-Fi, services, scripts, backup and updates, with controlled change and validation. Use when the user mentions MikroTik, RouterOS, WinBox, CHR, /ip, /interface or /system."
---

# Operation MikroTik RouterOS v7

Scope: RouterOS 7.x; before applying syntax, confirm version, architecture, packages and features available (`/system/resource/print`, `/system/package/print`, `/system/device-mode/print`). RouterOS v6 has different menus and behaviors: do not run v7 recipes blindly. This document teaches operation; does not provide connection, credentials or authorization to administer any device.

## Operation contract

1. Identify device, environment, administration interface, out-of-band access, window and target. Read state first; do not assume interface names, WAN/LAN assignments, addresses, or factory defaults. Do not perform on third party equipment without permission.
2. Propose minimal change with previous status inventory, exact commands, impact, dependencies, verification and reversal. Ask for explicit confirmation to change production routers, mainly access, firewall, routes, VPN, reset, upgrade or reboot; do not treat reading as written consent.
3. Before connectivity changes: Preserve alternative session/OOB, export configuration without `show-sensitive`, create an encrypted binary backup with password stored outside the chat when feasible, and establish testable recovery. Export text does not include all credentials/keys/certificates; binary backup is device-specific and version-specific. Do not copy sensitive artifacts for logs or repositories.
4. In CLI interactive WinBox/SSH use Safe Mode (Ctrl+X or F4), change in small steps and test access before leaving with Ctrl+X to confirm. Ctrl+D undoes. Safe Mode is not a universal transaction: the session must remain alive, other sessions may interfere and the history has limits; REST/API and scripts do not automatically inherit Safe Mode from a session. For remote automation, prefer phased changes, independent watchdog/rollback tested and OOB access. Never assume that `/undo` undoes all kinds of operation.
5. Check out observed state against objective, without revealing secrets. If connectivity has been lost, stop and use the recovery plan; do not fire repeated commands. Log what has been changed and what has not been verified.

## CLI is not Linux

SSH opens CLI of RouterOS, not Bash: do not use `ls`, `apt`, `iptables`, `systemctl`, redirect or pipe. Paths like `/ip/address/print`, `/interface/print`, `/system/resource/print` are menus/commands; scripts `.rsc` have their own syntax. Examples of reading:

```routeros
/system/identity/print
/system/resource/print
/interface/print detail
/ip/address/print detail
/ip/route/print detail
/ip/firewall/filter/print detail
/ip/firewall/nat/print detail
/log/print where topics~"error"
```

`print` shows temporary line numbers: do not use them in scripts. `[find ...]` can return zero or multiple IDs; confirm cardinality before `set/remove`. Use `name`/`comment` exact selectors and identify the real property; `*HEX` IDs can change. Do not do `remove [find]`, `remove [find dynamic=no]` or wide regex cleaning. Mark only objects that automation has and reconcile one at a time. Reexecute scripts only after confirming idempotency. For unknown syntax, see `?` help in menu, version and [official reference](https://manual.mikrotik.com/docs/CLI%20Reference/); do not invent properties.

## Access and management interfaces

Prefer SSH with key or HTTPS with validated certificate, user of lesser privilege and firewall/management address lists; segment management through VLAN/VPN. REST is exposed by the `www-ssl` service (or `www` without TLS, not recommended), in `/rest/` in RouterOS v7; do not confuse REST with the binary API (`api`/`api-ssl`, ports usually 8728/8729). Restrict `/ip/service`, `/tool/mac-server`, WinBox and neighbor discovery to the management network. Do not enable `www`, API without TLS or login with empty password to facilitate automation; do not use `curl -k`, tokens in shell arguments or export `show-sensitive` in logs. Inventory current rules before restricting services.

REST: `GET /rest/ip/address` list; `PUT /rest/ip/address` creates, `PATCH /rest/ip/address/*ID` update, `DELETE` removes; `POST /rest/<menu>/print` query with arguments/proplist and `POST /rest/<menu>/<command>` executes commands. `.id` is the internal identifier, not the line number. Action commands (`reboot`, `reset-configuration`, etc.) are not GET; treat POST as potentially state-changing. Use HTTPS client with certificate verification, secret outside URL/log, timeout and redacted logging. REST is not transactional: compare before/after and run explicit rollback if necessary.

## Operation Map (inspect before setting up)

| Area | Initial Inventory | Care and verification |
| --- | --- | --- |
| Links/VLAN/bridge/Wi-Fi | `/interface/print detail`, `/interface/bridge/print`, `/interface/bridge/port/print`, `/interface/vlan/print`, existing `wifi`/`wireless` menus | VLAN filtering, PVID and bridge CPU can disrupt management access; Wi-Fi depends on hardware, packages and version. Test SSID/authentication and management path. |
| IPv4/IPv6, DHCP, DNS | `/ip/address/print`, `/ipv6/address/print`, `/ip/dhcp-server/print`, `/ip/dhcp-client/print`, `/ip/dns/print` | Check pools, leases, gateway, RA/DHCPv6 and customer resolution; do not open DNS recursion for Internet. |
| Routes and protocols | `/ip/route/print detail`, `/routing/table/print`, `/routing` menus available | Confirm table/VRF, next-hop, distance, policies, BGP/OSPF and management return route; fail-over test from end to end. |
| Firewall/NAT | `/ip/firewall/filter/print detail`, `/ip/firewall/nat/print detail`, `/ipv6/firewall/filter/print detail` | Rules in order; `input` protects router, `forward` traffic; IPv6 has separate firewall. Preserve established/related and management exception before drop. NAT depends on conntrack; test both directions. |
| VPN/tunnels | `/interface/wireguard/print`, `/ip/ipsec/peer/print`, `/ppp/active/print` according to packages | Confirm peer, Allowed Address, Routes, MTU, DNS, firewall and handshake; never expose private key, PSK or credentials. |
| Accounts/services/certificates | `/user/print`, `/ip/service/print`, `/certificate/print` | Less privilege, valid TLS, restricted origin, coordinated rotation; do not remove only administrative access. |
| Observability | `/log/print`, `/tool/ping`, `/tool/traceroute`, `/interface/monitor-traffic`, `/tool/torch` | Beware of sensitive traffic and capture; monitoring can consume resources. Compare baseline and error before/after. |
| Backup/upgrade | `/system/package/print`, `/system/routerboard/print`, `/file/print` | Plan version, architecture, space, compatibility, reboot, rollback and physical access; do not update firmware/RouterBOOT automatically. |
| Scripts/automation | `/system/script/print detail`, `/system/scheduler/print detail` | Scripting is not shell; policies/permissions matter. Do not perform unaudited snippets, imports or remote downloads. |

## Firewall: sequence and scope

Filter rules are evaluated from top to bottom; exceptions should come before drop. `action=log` and address-list actions can continue evaluation. `fasttrack-connection` can bypass mangle/queues: evaluate policy routing and QoS before activating. For port forwarding, check `dstnat` and permission from `forward`, IP of destination, return and hairpin if applicable; publish service increases attack surface. Never replace rules by generic template or mix `/ip/firewall` with `/ipv6/firewall`. Use unique comments from your automation and check the position of each rule before and after.

## Reusable change plan

```text
Target and authorization: identity, version, environment, owner, maintenance window
Current state: relevant redacted output, management route, alternate access
Objective and risks: affected interfaces, addresses, and flows
Prerequisites: version/packages, backup/export, OOB, tested rollback
Change: exact commands, small steps, unique selectors
Verification: state, existing and new connections, clients, monitoring
Rollback: commands restoring previous state, trigger, owner, deadline
Result: applied/partial/not applied, evidence without secrets
```

## Sources and technical provenance

Adapted and expanded from [tikoci/routeros-skills (MIT, pinned revision)](https://github.com/tikoci/routeros-skills/tree/c9802a8713927a6851f5540efe93b95f2b0637b8), especially `routeros-fundamentals`, `routeros-firewall`, and `routeros-scripting`. Attribution and license are included in this package. Consult current MikroTik documentation for the actual version and menu: [manual](https://manual.mikrotik.com/docs/introduction/), [Configuration Management/Safe Mode](https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management), [REST API](https://help.mikrotik.com/docs/spaces/ROS/pages/47579162/REST+API), and [Firewall](https://help.mikrotik.com/docs/display/ROS/Filter). The old `help.mikrotik.com` pages are frozen; prefer the new manual when they disagree.
