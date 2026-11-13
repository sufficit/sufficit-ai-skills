---
name: sufficit-notifications
description: "Manage Sufficit notification contacts and event subscriptions through the corporate API: find, validate, create, block or remove contacts (e-mail, WhatsApp, SMS, Telegram), subscribe a contact to an event such as voicemail (caixa postal) or low balance, choose the delivery format (formatted text or JSON) per contact or per subscription, list and remove subscribers, and send an official test. Use for gestao de notificacoes, inscrever contato, contatos de notificacao, formato JSON da notificacao, quem recebe a caixa postal. Does not send free-form messages."
metadata:
  version: "1.0.3"
  author: "Sufficit"
---

# Sufficit notifications

A notification reaches a person when three things line up: a **contact** (channel +
destination, owned by a customer context), a **subscription** of that contact to an
**event** (optionally narrowed by a key, such as a mailbox), and a valid contact state.
This skill manages those records. Event producers (voicemail worker, balance alerts,
etc.) decide when to send; nothing here sends a message except the explicit test.

Front-end screens (Blazor), when the user prefers to do it by hand:
`/pages/notification/contactmanagement` (all contacts, managers),
`/pages/notification/mycontacts`, `/pages/notification/byevent`; the voicemail page
also has its own subscribe dialog and subscriber table.

## Access

Use the connected API tools: discover with `sufficit_api_search` and call with
`sufficit_api_call` (search in English: `notification contact`, `subscribers`,
`notification events`). Base URL `https://endpoints.sufficit.com.br`. The exact
operations, bodies and permissions are in the [API reference](references/api.md).
`POST /Notification/Subscribe` is hidden from the published OpenAPI; call the
documented route directly instead of concluding it does not exist.

Never print tokens. A valid token does not grant every customer: most operations
check the caller against the `contextId`; creating, editing, blocking and removing
contacts by id require manager or administrator. Do not grant roles or entitlements
to make a call pass; report the authorization gap.

## Workflow

1. **Resolve the customer** (`contextId`) and confirm homonyms. Do not switch customer
   on an empty result.
2. **Resolve the event** with `GET /Notification/Events` (id, title, subscribe method).
   Methods: `key` needs a key, `context` must not send one, `both` uses both. Never
   guess an event id from memory when the catalog is reachable.
3. **Resolve the key** when the event needs one (for voicemail it is the mailbox id,
   which must belong to the same customer). The API normalizes Guid keys and rejects
   legacy numbers; for other events read an existing subscription to confirm the format.
4. **Find or create the contact.** Search the customer's contacts first
   (`POST /Notification/Contact/Search`); reuse an existing one with the same channel
   and destination. Validate new destinations with `POST /Notification/Contact/Validate`.
5. **Subscribe** with `POST /Notification/Subscribe`, passing `contactId` for an
   existing contact, or `destination` + `channel` + `contextId` to create one.
6. **Read back** with `POST /Notification/Subscribers` and report what is now true.

## Contact state

- `cause` empty → valid, receives notifications.
- `cause = "pending"` → created by a subscription with a new destination; it does
  **not** receive anything until a manager clears `cause` (contact update). Say so
  explicitly instead of reporting the subscription as active.
- Any other `cause` → blocked (for example an opt-out or a bounced destination).
  Do not clear a block someone else set without the user's instruction.

## Delivery format

`format` is `TEXT` (default, human-readable per channel) or `JSON` (structured
document for automated consumers).

- `contact.format` is the contact default.
- `subscription.format` overrides it for one subscription; `null` inherits the contact.
- Effective format = subscription format, else contact format.

Use JSON only when the destination is an integration or the user asks for it; a person
reading WhatsApp should get text. Re-subscribing replaces the subscription row, so
always send the intended `format` (omit it only to inherit). Updating a contact also
replaces the record: read it first and send every field back, including `format`.

## Removing and testing

- Remove one subscription: `POST /Notification/Subscribers/Remove` (keeps the contact).
- Remove a contact: `DELETE /Notification/Contact?id=` deletes it **and all its
  subscriptions**. Confirm with the user before deleting.
- `POST /Notification/Test` sends one real simulated event to one existing contact.
  It is an outbound message: run it only when the user asked for a test, report
  `queued` as queued (not delivered), and do not retry an ambiguous result blindly.

## Proof

Report the read-back, not the request: contact id, channel, destination, cause, the
subscription (event, key, format) and the effective format. A 2xx without read-back,
a commit or a deploy is not proof that a person will receive the next notification.
