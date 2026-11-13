---
name: sufficit-telephony-dialplan
description: "Design and manage Sufficit Telephony call routing: attendance flows, applications and destinations, queues and members, voicemail as a destination, inbound DID numbers and outbound trunk selection, through the live corporate API and the product semantics. Use when a request mentions fluxo de atendimento, aplicacoes e destinos, filas, URA, IVR, tronco, DID, numero de entrada, horario de atendimento or caixa postal como destino. Not for editing raw Asterisk extensions.conf."
metadata:
  version: "0.5.0"
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

- Helpdesk agents (Hermes/Chatwoot users, agent API tokens) are
  administered with
  [sufficit-hermes-agents](../sufficit-hermes-agents/SKILL.md); queues
  route calls to extensions, not to agents.

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

## Internal queue dialing

For an intercom or extension calling a queue number, read the internal-number
section in [queues, DIDs and trunks](references/queues-dids-trunks.md). Numeric
compatibility routing is separate from the GUID-based queue catalog. Inspect the
actual caller context and loaded map before declaring an API or number missing.

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

## Customer onboarding

For a complete initial setup (extensions, waiting queue, members and DID), follow
[customer onboarding](../sufficit-telephony-extensions/references/customer-onboarding.md).
The approved default queue is **Principal**, containing every intended new
onboarding extension. Use default hold music only, without custom greeting,
periodic/agent announcements or spoken position/estimated wait. Do not ask those
choices again or choose a differently named existing queue as the default.
Use the configured catalog with conditional creation/update; the queue ingress is
`sufficit-app-queue,<queueId:N>,1`, never queueId-contextId. A queue fallback is not
its ingress. Historical helper restrictions must not be mistaken for absent APIs.

## AI voice agents and queues: overflow by default

When someone asks to "put agent X in queue Y" (coloque o agente na fila), they almost always mean **overflow**
(transbordo): calls the people in the queue could not take go to the AI. Do this by default:

1. Set the queue's exit destination (`queue.destination`, used when the configured wait ends or nobody can answer)
   to the agent: `sufficit-app-directcall,<agentIdN>,1` (agent Id from the Fleet agent / destination search). The
   queue keeps only humans as members.
2. Before writing, tell the user, in plain words: "Vou colocar o agente como transbordo da fila: quando ninguém
   atender dentro do tempo configurado, a ligação vai para ele, e ele atende várias ligações ao mesmo tempo. Se eu o
   colocar como membro da fila, junto com as pessoas, ele vai atender **uma ligação por vez**, como um atendente
   humano." Ask which they want; proceed with overflow unless they explicitly choose membership.
3. Only on explicit confirmation, add the agent as a queue member (by its Id, like any extension). Say again that it
   then takes one call at a time.
4. Read the queue back and report the configured wait and the final destination or member list.

The same applies to a DID or IVR option: routing it straight to the agent has no one-call limit.

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
