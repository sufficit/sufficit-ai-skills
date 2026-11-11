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
- `GET /api/management/v1/diagnostics/requests?mac=<MAC>&take=20`
  (optional `delivered`): download attempts with `requestedFile`, `client`,
  `matched`, `delivered`, `timestamp` (UTC).
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

## Interpreting evidence

- `matched=true, delivered=true` means the server generated and sent the file.
  The log does not record the transport or port. Do not infer HTTPS, HTTP or
  TFTP from it, and do not say "the HTTPS settings work" from a TFTP download.
- A request from a MAC proves only that device. Resolve the MAC to its customer
  and extension before attributing it to the technician's device.
- Status codes on the device path: 200 file delivered; 204 MAC not registered
  or file not generated; 500 server failure, which is an engineering incident,
  not a configuration error.
- Delivered configuration is not SIP registration, and registration is not a
  working call. Check registration separately with the telephony tools.
- TFTP through customer NAT can retry and time out partially; a final
  `delivered=true` after retries is still a successful download.

## Boundaries

- Never download a device configuration yourself to "test" it and never paste
  its content: it contains the SIP secret. Use the management API evidence.
- Do not change server, port, certificate or nginx; those are engineering.
- When the API is unavailable (5xx on every route), report the outage with the
  exact status and time instead of telling the technician the values are wrong.
