# Extension presence and Do not disturb

The presence of an extension is the native Asterisk state of that extension, keyed by
its GUID (never by its number). It is the same on every voice node. Public explanation:
<https://wiki.sufficit.com.br/Sufficit/Telephony/presenca-ramal.html>.

## Read and change

- Read: `GET /telephony/endpoint/presence?contextId=<company guid>&id=<extension guid>`.
- Change: `PUT /telephony/endpoint/presence` with
  `{ "contextId", "endPointId", "state", "subtype"?, "message"? }`.
  - The server writes the change on every voice node.
  - 200 means every node applied it.
  - 502 returns the per-node result. Retry the same request.
- Access: the extension's own user, or whoever holds the company's telephony
  entitlement. Another company's extension answers 404.
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
| **DND** tag, "Não perturbe ativo" | Presence `dnd` (or PBX Do not disturb) is set; queues skip it | Read the presence; ask the user to switch back to available, or set `available` with the company's confirmation |
| **DND?** tag, "Não perturbe provável · n recusas" | The phone/app answered busy while free; usually the app's own Do not disturb (e.g. MicroSIP) | Ask the user to turn off Do not disturb **in the phone or app**. The API cannot change it, and setting presence does not affect the app |
| "Indisponível" | Presence `unavailable`; queues skip it | Same as DND |
| "Ausente · note", "Ocupado · note", "Ausência prolongada" | Away states; queues still offer calls | Not the cause of a queue not ringing |

While an app keeps its own Do not disturb, queues wait the queue's
"Espera após ramal ocupado" (default 10 s) before offering again, so other agents
keep receiving calls. Recommend the Sufficit app status or the PBX Do not disturb
instead of the app's local Do not disturb: then the PBX knows, and the panel shows
**DND** (confirmed).

## Limits

- Legacy SIP extension cards are keyed by number, so presence is not shown on them.
  The likely DND (busy-while-idle) still is.
- Planned, not available yet: the Sufficit Phone status changing presence by
  itself, feature codes for Do not disturb, and colleagues seeing presence on BLF
  keys.
