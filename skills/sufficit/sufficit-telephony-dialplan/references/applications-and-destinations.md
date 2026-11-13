# Applications and destinations

Concepts of the routing layer plus voicemail-drop semantics from the product
guides. The deployed API is the authority on names and values.

## Concepts

- **Application**: what happens in a flow step (play an announcement, route to
  a queue, drop into voicemail, transfer, hang up, check business hours).
- **Destination**: where the step hands the call — an extension, a queue, a
  voicemail box, an external number or another flow.
- A flow only routes well when each destination exists in the same company and
  is in the expected state; confirm before referencing.

## Voicemail as a destination

- The voicemail box takes a recorded message from the caller and forwards it to
  the notification contacts configured **on that box**.
- WhatsApp delivery is part of that flow when there is a valid recipient on that
  channel and the integration is enabled; the audio goes in the message and call
  details may arrive separately.
- One box may have several notification contacts; the receiving WhatsApp number
  is **not** deduced from the box name, extension or caller number.
- For a box to receive messages, the company needs the box enabled, a flow that
  actually routes calls to it and valid notification contacts. Routing a flow to
  voicemail without those does not deliver anything.
- Each recipient gets formatted text by default; JSON is an opt-in per contact or
  per subscription, meant for integrations. Managing those recipients (subscribe,
  remove, format, pending or blocked contacts) belongs to the `sufficit-notifications`
  skill; the subscription key is the box id.

## Editing a flow

1. Read the DID and its flow end to end; list each step's application and
   destination as they are, not as the requester expects.
2. Propose the minimal diff (which step, what changes, which destination) and
   only then apply it, one logical change per call.
3. Re-read and report the full resulting path; mention destinations that became
   dangling or duplicated, even when not part of the request.
4. For an unknown application or destination type, discover the semantics in the
   OpenAPI before using it; do not guess from the name.
