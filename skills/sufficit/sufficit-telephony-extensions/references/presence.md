# Extension presence and Do not disturb

The presence of an extension is the native Asterisk state of each of its devices, keyed
by the extension GUID (never by its number): `<guid>` PJSIP phone/app, `wss-<guid>`
Chrome extension, numeric title for legacy SIP. It is the same on every voice node. Public explanation:
<https://wiki.sufficit.com.br/Sufficit/Telephony/presenca-ramal.html>.

## Read and change

- Read: `GET /telephony/endpoint/presence?contextId=<company guid>&id=<extension guid>`.
- Change: `PUT /telephony/endpoint/presence` with
  `{ "contextId", "endPointId", "state", "subtype"?, "message"?, "device"? }`
  (`device`: `pjsip`, `webrtc` or `sip`; only per-device extensions use it).
  - The server writes the change on every voice node.
  - 200 means every node applied it.
  - 502 returns the per-node result. Retry the same request.
- Access: the extension's own user, or whoever holds the company's telephony
  entitlement. Another company's extension answers 404.
- Mode (extension record option "Presença por aparelho"): `unified` (default; every
  change applies to all devices) or `device`. Read it in the `mode` field of the GET;
  change it with `PUT /telephony/endpoint/presencemode` `{ "contextId", "endPointId", "mode" }`
  (extension management access, audited). Switching to unified aligns every device to
  the phone's state (or the Chrome extension's when the phone has none).
- The GET also returns `devices[]` (state of each device).
- Discover the operation in the deployed OpenAPI; it is the authority on field names.

| `state` | Use for | Queues |
|---|---|---|
| `available` | available | offered |
| `chat` | available, eager to talk | offered |
| `away` | away; `subtype: "busy"` = "Ocupado" | offered (for now) |
| `xa` | extended away (vacation, leave) | offered (for now) |
| `dnd` | Do not disturb | **not offered** |
| `unavailable` | offline | **not offered** |
| `not_set` | clear the state (no subtype/message) | offered |

- `message`: up to 140 characters, e.g. "Almoço, volto 14h".
- `subtype`: up to 40 characters.
- The response field `offerable` is `false` for `dnd` and `unavailable`.

Change one extension per call, confirm company and extension first, then read the
state back and report it. Never set `dnd`/`unavailable` on someone else's extension
without the requester confirming it: queues stop offering calls to it.

## "The queue does not ring" / "the extension does not receive calls"

Check the extension card on the telephony panel first:

| Card | Meaning | What to do |
|---|---|---|
| **DND** tag, "Não perturbe ativo" | Presence `dnd` (or PBX Do not disturb) is set on that device; queues and direct calls skip that device (unified: every device) | Read the presence; ask the user to switch back to available, or set `available` with the company's confirmation |
| **DND?** tag, "Não perturbe provável · n recusas" | The phone/app answered busy while free; usually the app's own Do not disturb (e.g. MicroSIP) | Ask the user to turn off Do not disturb **in the phone or app**. The API cannot change it, and setting presence does not affect the app |
| "Indisponível" | Presence `unavailable`; queues skip it | Same as DND |
| "Ausente · note", "Ocupado · note", "Ausência prolongada" | Away states; queues still offer calls | Not the cause of a queue not ringing |

While an app keeps its own Do not disturb, queues wait the queue's
"Espera após ramal ocupado" (default 10 s) before offering again, so other agents
keep receiving calls. Recommend the status of the Sufficit apps (Sufficit Phone,
Chrome extension) instead of a third-party app's local Do not disturb: then the PBX
knows, and the panel shows **DND** (confirmed). There are no dial codes for presence.

## Per device

- The panel shows one card per device type of the extension (phone/app, Chrome
  extension "WebRTC", legacy SIP); the voice node is a detail on the card.
- Per-device extension with DND only on the Chrome extension: the phone keeps ringing,
  by design. If the customer expects one "Do not disturb" for everything, switch the
  extension back to unified.
- With every device in DND or offline, a direct call ends as unavailable. There is no
  voicemail or forwarding on the extension: mailboxes and follow-me ("siga-me") are
  separate applications in the dialplan.
- Internal extension-to-extension calls still ring a DND device; only queues and direct
  calls filter by presence.

## Limits

- Legacy SIP presence uses the numeric title key; it is shown on the `SIP/<number>` card.
- Available: the Chrome extension (2.23.0+) stores its status as presence on every line
  (Disponível → available, Ocupado → dnd, Offline → unavailable); from 2.23.1 it names
  the `webrtc` device, so per-device extensions change only the browser.
- Planned: the Sufficit Phone desktop status (code ready, release pending). Deferred: colleagues seeing presence on BLF keys.
- There are no dial (feature) codes for presence, by decision.
