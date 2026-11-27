# Support bridge (customer's local network)

Use the bridge when a device (phone, ONT, router, ATA, PBX) is only reachable
inside the customer's local network. The customer runs a small portable program
on a computer of that network. By default the session is **full network**: you
reach every private network that computer reaches, through any adapter, including
devices behind internal routers/NAT. Every session is audited, limited in time
and closes by itself.

**Do not ask the customer for IPs.** Discover them through the bridge and the
provisioning records. Ask the customer only what cannot be discovered (for
example which extension a phone must use, or the go-ahead).

## 1. Check what we already know

Before talking about the bridge, look up the customer's devices and extensions
in provisioning (by customer, extension or MAC) when the provisioning tools are
available. Note model, MAC and last known IP: they tell you what to look for.

## 2. Agree with the customer

One message: a program will be downloaded, a code pasted, the window kept open
during the support; closing it ends the access at any time. Wait for the go-ahead.

## 3. Open the session

Call `http_support_bridge_open` with `label` (e.g. `Telefone IP - conversa <id>`),
`customer_reference` (`hermes:<conversation id>`) and `minutes` (60 by default,
at most 240). **Leave `target` empty** (full network). Fill `target` only when you
must restrict the session to a single known IP.

The answer has `sessionId`, `expiresAt`, `bridgeCode` and `agentCode`.

- `bridgeCode` goes to the customer.
- `agentCode` is yours. **Never** send it to the customer, a group, a note,
  memory or a summary: it gives access to the customer's network.

## 4. Send the customer the link and the code

Public reply, in plain words:

1. Download: `https://storage.googleapis.com/suff-public/sufficit-bridge/sufficit-bridge.exe`
   (no installation, no administrator rights).
2. Open it, paste the code `<bridgeCode>` and press Enter.
3. Keep the window open; closing it ends the access.

If SmartScreen warns: *Mais informações → Executar assim mesmo*. Never ask the
customer to disable antivirus or firewall.

## 5. Connect from your shell

```bash
cd /tmp && curl -fsSLo sufficit-bridge https://storage.googleapis.com/suff-public/sufficit-bridge/sufficit-bridge-linux-amd64 \
  && chmod +x sufficit-bridge && ./sufficit-bridge --version   # 1.2.0 or newer for full network
read -r SUFFICIT_BRIDGE_AGENT_CODE   # paste agentCode (keeps it out of history)
export SUFFICIT_BRIDGE_AGENT_CODE
./sufficit-bridge agent -socks 127.0.0.1:1080 -api 127.0.0.1:8081 > /tmp/bridge-agent.log 2>&1 &
unset SUFFICIT_BRIDGE_AGENT_CODE
```

When the customer says the window shows *Conectado*, inspect the network through
the local API (it answers from the customer's computer):

```bash
curl -sS -m 20 http://127.0.0.1:8081/info        # adapters, MACs, gateways, networks to scan
curl -sS -m 20 http://127.0.0.1:8081/neighbors   # ARP table (IP + MAC)
curl -sS -m 300 http://127.0.0.1:8081/scan       # scans the networks of all active adapters
curl -sS -m 300 'http://127.0.0.1:8081/scan?cidr=192.168.0.0/24,10.0.0.0/24&ports=80,443,5060'
```

`/scan` with no `cidr` covers the recognisable networks of every active adapter.
Devices behind NAT/another router are in other subnets: use the gateways and
adapter networks from `/info`, the provisioning data and common ranges
(`192.168.0.0/24`, `192.168.1.0/24`, `10.0.0.0/24`…) as extra `cidr`. Limits: 4096
addresses and 32 ports per scan. Each host comes with open ports, MAC and HTTP
title/server: identify the device by MAC vendor prefix, model in the title and
the provisioning MAC. A `502 ponte indisponível` means the customer's program is
not connected yet: wait for the customer, do not loop.

Then reach the device through the SOCKS proxy (private addresses only):

```bash
curl -sS -m 15 --socks5-hostname 127.0.0.1:1080 -I http://<device-ip>/
OPENSSL_CONF=/tmp/openssl_legacy.cnf curl -k -sS -m 15 --socks5-hostname 127.0.0.1:1080 -I https://<device-ip>/
```

Follow the normal flow: read before writing, minimal change, read back.

## 6. Update our records

If the device is missing or outdated in provisioning (IP, MAC, model, extension),
create or update it with the provisioning tools so the next support already has
it. Record only device data, never passwords in notes.

## 7. Close

1. `http_support_bridge_close` with the `sessionId`;
2. stop the local agent (`kill %1` or the PID) and delete `/tmp/sufficit-bridge`,
   the log and any cookies;
3. tell the customer the access is closed and they can delete the program.

Report "connected through the bridge" only after a real reply from the device
through the proxy. Escalate to N2 only if the tool fails or the device does not
answer through the bridge.
