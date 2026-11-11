# Device auto-provisioning (phones and intercoms by MAC)

Device provisioning is not extension creation. Creating an extension
([provisioning.md](provisioning.md)) produces SIP credentials; device
provisioning lets a physical phone or softphone download a configuration file
that already carries those credentials. Use this reference when a request
mentions provisionamento/autoprovisionamento, MAC, TFTP, "servidor de
provisionamento", a phone model (Intelbras TIP 125i, Grandstream, Cisco) or a
Linphone QR code.

## Server

- Public host: `provisioning.sufficit.com.br`. The same service runs on the
  three *-apps nodes; the public name resolves to one of them.
- Transports, all serving the same generated file:
  - TFTP: UDP 69.
  - HTTP: port 80.
  - HTTPS: port 443 and port 26511 (both with a valid public certificate).
- Device downloads use **no authentication**. The file is generated at request
  time from the registered MAC, so it carries the extension secret.

## Paths by model

The device appends its own MAC (12 hex digits, no separators). Ask only for the
base path; never ask the technician to type the MAC into the path.

| Model (catalog) | Requested file | Path field to configure |
|-----------------|----------------|-------------------------|
| Intelbras TIP125i (registered as "TIP 125") | `intelbras/tip125i/<MAC>.xml` | `intelbras/tip125i/` |
| GrandStream V1 | `grandstream/v1/cfg<mac>.xml` | `grandstream/v1/` |
| Cisco SEP | `SEP<MAC>.cnf.xml` (TFTP root) | server only |
| Linphone softphone | `/linphone/configuration` (installation, not MAC) | QR code / link |

Read the live list with `GET /api/management/v1/catalog/models` before claiming
a model is unsupported. Requests for generic files such as `tip125system.xml`
answer 204; that is normal and not a failure.

Answering "which values do I put in the device" for a TIP 125i: protocol HTTPS,
server `provisioning.sufficit.com.br` (port 443 is the default; 26511 also
works), path `intelbras/tip125i/`, authentication none. HTTP on 80 and TFTP
on 69 are valid alternatives. Port 26511 is not required. If the device has a
separate port field, fill it consistently with the protocol chosen.

## Management API (provisioning target of the authenticated helper)

All calls are scoped by customer context; an absent device in another
customer's scope returns 404, which is not proof that the MAC is unknown.

- `GET /api/management/v1/devices?search=<MAC or extension digits>&take=20`
  (optional `context_id`, `vendor`, `model`, `enabled`). Summary includes
  `contextId`, `extensionId`, `extensionNumber`, `enabled`, `lastRequestAt`,
  `lastDelivered`.
- `GET /api/management/v1/devices/{MAC}`: vendor, model, displayName and the
  properties `context_id`, `extension_id`, `extension_number`, `enabled`,
  `match`. Secret properties are never returned.
- `GET /api/management/v1/diagnostics/requests?mac=<MAC>&take=20`: download
  attempts of registered devices with `requestedFile`, `client` (device public
  IP), `transport` (`tftp`/`http`/`https`), `outcome`, `detail`, `matched`,
  `delivered`, `timestamp` (UTC). Filters: `mac`, `client=<IP>`,
  `outcome=<slug>`, `transport=<tftp|http|https>`, `since=<UTC ISO time>`,
  `delivered`. Add `unregistered=true` to see requests with no registered
  device (unknown MAC, wrong path, static files). Rows written before
  2026-11-11 18:20 UTC have no transport/outcome.
- `GET /api/management/v1/diagnostics/summary?window_hours=24`: totals.
- `GET /api/management/v1/discoveries?window_hours=24`: physical MACs that
  requested a file but are not registered, and Linphone installations without
  an extension. Use it when the technician does not know the MAC.
- `PUT /api/management/v1/devices/{MAC}` registers or updates a device:
  `{"vendor","model","displayName","description","properties":{"context_id",
  "extension_id","extension_number","enabled":"true"}}`. Properties are merged,
  not replaced. This is a business write: do it only when an authorized person
  asked for that MAC and that extension, after confirming the extension belongs
  to the same customer and no other device is linked to it. Follow the
  existing naming (Intelbras / "TIP 125", displayName = full extension number)
  and re-read the device afterwards. Never move a MAC already linked to
  another customer; report it instead.

## Acting for the technician

When a technician installs or configures a device, do the provisioning work
for them instead of asking them to operate the server:

1. **Find the device.** Ask for nothing you can read. List what appeared
   recently: `GET .../discoveries?window_hours=24` (unregistered MACs with
   model, public IP, first/last seen and request count) and
   `GET .../diagnostics/requests?unregistered=true&since=<UTC>&take=50`.
   Correlate by the time the technician says they configured it and by the
   site's public IP (the `client` of the customer's other devices, or the
   address its registered SIP extensions come from). Several candidates or no
   candidate: show what you saw (model, MAC, IP, time) and ask which one, or
   ask for the MAC on the label. Never pick one by guess.
   MACs made of zeros or other obvious placeholders (`000000000000`,
   `0000000000AA`) are test requests, not devices: mention them only as such.
2. **Register it** (authorized business write, see the PUT contract above):
   resolve the target extension through the EndPoints API of the same
   customer (GUID, full number), confirm no other device is linked to that
   extension and the MAC is not linked to another customer, PUT, re-read.
3. **Ask for one action only:** reboot the device or force provisioning.
4. **Verify:** `GET .../diagnostics/requests?mac=<MAC>&since=<UTC>` and report
   transport, outcome and time. Then check the SIP registration of the
   extension separately. Report each step as verified or not verified.

## Diagnosing failures

Read the requests for the MAC, then for the site IP (`client=<IP>` with and
without `unregistered=true`) in the window of the test. Map what you see:

| Evidence | Meaning | Next step |
|----------|---------|-----------|
| No request at all from the device or site IP | The device is not reaching the server: wrong server name, protocol/port, path field empty, provisioning disabled on the device, DNS or firewall at the site | Ask for the exact values on the device screen and compare with the table above; HTTPS 443 is the safest choice |
| `outcome=no-model` | Path does not match any model (typo, wrong folder or file name; letter case does not matter) | Show the `requestedFile` received next to the expected pattern |
| `outcome=device-unresolved` | MAC not registered, disabled or without extension | Register or fix the link (Acting for the technician, step 2) |
| `outcome=policy-blocked` | Credentials withheld: the device came from a network outside the one learned for it (`detail`) | Do not change the policy yourself; report MAC, old and new IP to an administrator |
| `outcome=credential-error` / `credential-missing` | The extension secret could not be read | Check the extension exists and is enabled; otherwise engineering |
| `outcome=empty` | The model produced no document | Engineering |
| `outcome=delivered` then `transfer-failed` (tftp) | File generated but the device never acknowledged it, typically NAT/firewall on UDP | Switch the device to HTTPS 443 |
| `outcome=delivered` over http/https, extension not registered | Provisioning worked; the problem is SIP registration | Diagnose registration (credentials, network), not provisioning |
| Many `static`/204 rows for generic files (e.g. `tip125system.xml`) | Normal model housekeeping | Ignore |
| 5xx on device or management routes | Server failure | Report status and time; engineering |

General rules:

- A request from a MAC proves only that device; resolve MAC to customer and
  extension before attributing it to the technician's device.
- `delivered=true` alone, on rows without `transport`, says nothing about the
  protocol or port the device used.
- Delivered configuration is not SIP registration, and registration is not a
  working call. Check each separately.
- Times in the API are UTC; convert to Brasília when talking to people.

## Boundaries

- Never download a device configuration yourself to "test" it and never paste
  its content: it contains the SIP secret. Use the management API evidence.
- Do not change server, port, certificate or nginx; those are engineering.
- When the API is unavailable (5xx on every route), report the outage with the
  exact status and time instead of telling the technician the values are wrong.
