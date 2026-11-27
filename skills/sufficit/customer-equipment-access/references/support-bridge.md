# Support bridge (device on the customer's LAN)

Use the bridge when the device is only reachable inside the customer's local
network (for example `192.168.1.1`) and has no working public IP or customer VPN.
The customer runs a small portable program on a Windows computer of that network;
you reach only the device IP you declared, for a limited time. Every session is
audited and closes by itself when it expires.

## 1. Agree with the customer first

Explain in one message what will happen and ask for the go-ahead: the customer
downloads a program, pastes a code, keeps the window open during the support and
can close it at any moment to end the access. Also ask for the **device IP on
their network** if it is not in the conversation (router/ONT is usually the
gateway: `ipconfig` → *Gateway padrão*). Do not open a session before the
customer agrees and the IP is known.

Only `10.0.0.0/8` and `192.168.0.0/16` IPv4 addresses are accepted, one device per
session. Another network or several devices: ask N2.

## 2. Open the session

Call `http_support_bridge_open` with:

- `label`: short description, e.g. `ONT - conversa <id>`;
- `customer_reference`: `hermes:<conversation id>`;
- `target`: the device IP;
- `minutes`: 60 by default; at most 240.

The answer has `sessionId`, `expiresAt`, `bridgeCode` and `agentCode`.

- `bridgeCode` goes to the customer.
- `agentCode` is yours. **Never** send it to the customer, a group, a note,
  memory or a summary: it gives access to the customer's network.

## 3. Send the customer the link and the code

Public reply in the customer's conversation, in plain words:

1. Download: `https://storage.googleapis.com/suff-public/sufficit-bridge/sufficit-bridge.exe`
   (no installation, no administrator rights needed).
2. Open it, paste the code `<bridgeCode>` and click **Conectar**.
3. Keep the window open; closing it ends the access.

If Windows SmartScreen warns, the customer chooses *Mais informações → Executar
assim mesmo*. Do not ask the customer to disable antivirus or firewall.

## 4. Connect from your shell

```bash
cd /tmp && curl -fsSLo sufficit-bridge https://storage.googleapis.com/suff-public/sufficit-bridge/sufficit-bridge-linux-amd64 \
  && chmod +x sufficit-bridge && ./sufficit-bridge --version
# keep the code out of the command line and history
read -r SUFFICIT_BRIDGE_AGENT_CODE   # paste agentCode
export SUFFICIT_BRIDGE_AGENT_CODE
./sufficit-bridge agent -socks 127.0.0.1:1080 > /tmp/bridge-agent.log 2>&1 &
unset SUFFICIT_BRIDGE_AGENT_CODE
```

Wait until the customer says the window shows *Conectado*, then reach the device
through the local proxy only:

```bash
curl -sS -m 15 --socks5-hostname 127.0.0.1:1080 -I http://<device-ip>/
OPENSSL_CONF=/tmp/openssl_legacy.cnf curl -k -sS -m 15 --socks5-hostname 127.0.0.1:1080 -I https://<device-ip>/
```

The proxy dials only the declared device; anything else is refused. A timeout
means the customer's program is not connected yet or the IP is wrong: confirm
with the customer, do not retry in a loop. From here follow the normal flow
(read before writing, minimal change, read back).

## 5. Close

When the work is done (or the customer asks to stop):

1. `http_support_bridge_close` with the `sessionId`;
2. stop the local agent (`kill %1` or the PID) and delete `/tmp/sufficit-bridge`,
   the log and any cookies;
3. tell the customer the access is closed and they can delete the program.

Report "connected through the bridge" only after a real reply from the device
through the proxy.
