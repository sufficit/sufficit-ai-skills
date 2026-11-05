---
name: sufficit-telephony-dialplan
description: "Design and manage Sufficit Telephony call routing: attendance flows, applications and destinations, queues and members, voicemail as a destination, inbound DID numbers and outbound trunk selection, through the live corporate API and the product semantics. Use when a request mentions fluxo de atendimento, aplicacoes e destinos, filas, URA, IVR, tronco, DID, numero de entrada, horario de atendimento or caixa postal como destino. Not for editing raw Asterisk extensions.conf."
metadata:
  version: "0.1.0"
---

# Sufficit Telephony: dialplan, applications and destinations

Operate the routing layer of Sufficit Telephony as the authenticated user: how an
inbound call travels from the DID through the attendance flow to a destination.
The deployed OpenAPI is the authority on paths, parameters and formats; this
skill adds the flow and the business semantics. Routes change between releases:
never assume a method, path or parameter from memory.

## Scope and boundaries

- Covers attendance flows (fluxos), the applications they run, their
  destinations, queues and members, voicemail **as a destination**, inbound DID
  numbers and outbound trunk behavior.
- Creating or changing extensions (ramais) and their preferences is
  [sufficit-telephony-extensions](../sufficit-telephony-extensions/SKILL.md).
- Attendant-style reads of call recordings and voicemail messages start at
  [sufficit-api](../sufficit-api/SKILL.md).
- Editing literal Asterisk `extensions.conf` in a repository is the
  `asterisk-dialplan` skill; this skill never edits raw dialplan files.

## Routing model

- Inbound: the call arrives at a **DID** (inbound number) and follows that
  number's **attendance flow**.
- A **flow** is an ordered sequence of steps; each step runs an **application**
  (announce, route to queue, drop to voicemail, transfer, etc.) and ends in a
  **destination** — an extension, a queue, a voicemail box, an external number
  or another flow.
- Destinations reference concrete resources: confirm the resource exists in the
  same company before referencing it. Relationships are GUIDs; names are
  presentation only.
- A **DID is the inbound number**, not a voicemail box: voicemail is a separate
  resource; never answer a voicemail question by listing DIDs.

## Operation flow

1. Resolve the target company explicitly and keep it selected for the whole
   task; never let a routing change touch another company.
2. Read the current routing before proposing changes: the DID, its flow, each
   step's application and destination, and the resources referenced.
3. Change one logical thing per call: a step, a destination, a queue membership.
   Do not reorder or rewrite unrelated steps while editing.
4. After each write, re-read the flow and report the resulting path
   (DID → flow → steps → destination) plus what was verified.
5. Removing or disabling a flow or destination changes live call handling:
   check what still references it (other flows, queues, voicemail notification)
   before removing, and report what was and was not verified.

## References

- Applications, destinations and voicemail drop semantics:
  [references/applications-and-destinations.md](references/applications-and-destinations.md).
- Queues, inbound DIDs and outbound trunks:
  [references/queues-dids-trunks.md](references/queues-dids-trunks.md).

## Validation

Verify every change by an independent read; present count and truncated flags
honestly (a truncated listing is not a total). When the deployed API does not
expose an operation this skill describes, follow the document, report the
limitation and do not invent a route or simulate success.

## Sources and provenance

Authored by Sufficit from the `Sufficit.Telephony` guides (wiki) — voicemail
notification, per-extension recording, individual trunk rules — and the corporate
API workflow. Release 0.1.0 teaches the flow; the exact routing calls must be
confirmed against the live OpenAPI on first real use and recorded in the
references in that same change.
