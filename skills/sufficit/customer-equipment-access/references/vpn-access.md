# Customer VPN access (Linux, NetworkManager)

Use only when the device does not answer on its direct address.

## Read the customer's VPN data

Customers often send a screenshot of their own VPN client: server, type (PPTP,
L2TP/IPsec, OpenVPN, WireGuard), user and password. Read it with OCR; if OCR
fails, open the image and read it visually. A masked password (dots) is **not**
a password — ask for it in the conversation, never in a group.

## Create a route-only profile

One profile per customer, routing only the device address:

```bash
nmcli connection add type vpn con-name "cust-<name>" vpn-type pptp \
  vpn.data "gateway=<vpn-server>, user=<user>, require-mppe=yes, refuse-eap=yes" \
  ipv4.never-default yes ipv4.ignore-auto-routes yes ipv4.routes "<device-ip>/32"
nmcli connection modify "cust-<name>" vpn.secrets "password=<password>"   # from the conversation, not echoed
nmcli connection up "cust-<name>"
```

- `gateway` belongs inside `vpn.data`, not as an nmcli property.
- Never let the VPN become the default route and never change the system
  default/route table by hand.
- PPTP needs the `network-manager-pptp` plugin and GRE allowed outbound.

## Prove the tunnel

Before saying "VPN connected", read back all three:

1. `nmcli -t -f NAME,STATE connection show --active | grep cust-<name>` → activated;
2. `ip route get <device-ip>` → goes through the `ppp`/`tun` interface;
3. the device answers through it.

`Connection activation failed: Unknown reason` usually means wrong password,
blocked GRE or an unsupported encryption setting. Retry once after checking
them; do not loop.

## Clean up

`nmcli connection down "cust-<name>"` when finished, and delete the profile
(`nmcli connection delete`) unless the customer agreed to keep access. Never
store the VPN password anywhere else.
