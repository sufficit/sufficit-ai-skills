# Notification API reference

Verified against `sufficit-endpoints` and `sufficit-base` on 2026-11-13. The live
OpenAPI prevails for field details; this file records behavior that is not obvious
from the schema. JSON property names are lowercase as shown.

## Operations

| Operation | Purpose | Authorization |
|---|---|---|
| `GET /Notification/Events` | Event catalog: `id`, `title`, `description`, `method`, `icon` | public |
| `POST /Notification/Contact/Search` | Contacts by `contextid`, `channel`, `destination`/`filter` text, `valid` | authenticated; non-managers must send a `contextid` they can access |
| `GET /Notification/Contact?id=` | One contact | manager/administrator |
| `POST /Notification/Contact` | Create (`id` empty) or replace a contact | manager/administrator |
| `DELETE /Notification/Contact?id=` | Delete a contact **and all its subscriptions** | manager/administrator |
| `POST /Notification/Contact/Validate` | Normalize/validate `destination` + `channel`; `valid` is the normalized destination, `message` explains a block | public |
| `GET /Notification/Contact/IsValid`, `GetCause` | Block check by `destination` (+ `channel`) | manager/administrator |
| `POST /Notification/Subscribe` | Subscribe a contact (hidden from OpenAPI) | see warning below |
| `POST /Notification/Subscribers` | Subscribers (`contact` + `subscription`) of `eventid`, optional `contextid`, `keys`, `channel`, `valid` | authenticated; non-managers must send an accessible `contextid` |
| `POST /Notification/Subscribers/Remove` | Remove one subscription (`eventid`, `key`, `contactid`) | authenticated; context checked |
| `POST /Notification/Test` | Send one simulated event to one valid contact (`eventid`, `contextid`, `contactid`) | authenticated; both contexts checked |

## Bodies

Contact:

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "contextid": "<customer context id>",
  "channel": "WHATSAPP",
  "destination": "5521999990000",
  "extra": "optional note, max 200",
  "priority": 0,
  "format": "TEXT",
  "cause": null
}
```

Channels: `EMAIL`, `SMS`, `WHATSAPP`, `TELEGRAM`, `PUSH` (plus `UNKNOWN` = detect on
validation). `POST /Notification/Contact` with an empty `id` reuses an existing contact
with the same context, channel and destination (updating `cause`, `extra`, `priority`,
`format`); with an `id` it replaces the whole record, so send every field back.

Subscribe:

```json
{
  "eventid": "<event id from /Notification/Events>",
  "key": "<required when method is key or both; omit otherwise>",
  "contextid": "<customer context id>",
  "contactid": "<existing contact id>",
  "format": "JSON"
}
```

Instead of `contactid`, send `destination` and `channel` (and `contextid`): the API
validates them, reuses a matching contact or creates one with `cause = "pending"`.
`format` omitted or `null` means "inherit the contact format". A second subscribe for
the same event, key and contact replaces the row, including `format`.

Subscriber (response item):

```json
{
  "contact": { "id": "...", "channel": "WHATSAPP", "destination": "...", "format": "TEXT" },
  "subscription": { "eventid": "...", "key": "...", "contactid": "...", "contextid": "...", "format": "JSON" }
}
```

`format` is omitted from JSON when it is the default (`TEXT` on a contact, `null` on a
subscription); treat a missing value accordingly.

## Event keys

- Voicemail (`MailBoxNEvent`, id `69f367ab-c465-4f29-991f-b31b0b8e0760`): key is the
  mailbox id as 32 hex characters **without hyphens** (Guid "N"). The worker matches the
  key literally; a hyphenated id is accepted but never fires.
- Queue events: key is the native queue id; the API normalizes it to Guid "N" and
  rejects legacy extension numbers.
- Other events: check `method` in the catalog and an existing subscription of the same
  event before inventing a key format.

## Delivery

Voicemail notifications: valid contacts only (`cause` empty), channels e-mail, SMS,
WhatsApp, Telegram and push. `TEXT` sends the per-channel formatted message with the
audio attached where the channel supports it; `JSON` sends the voicemail JSON document
(event, message, context, mailbox, call, parameters) with the same audio.

## Warning: unauthenticated subscribe

As verified on 2026-11-13, `POST /Notification/Subscribe` has no `[Authorize]` and does
not check the caller against `contextid`. New destinations stay `pending` and do not
receive notifications, which limits exposure, but an existing valid `contactid` can be
subscribed to other keys of its own context. Do not rely on this endpoint to enforce
permissions: confirm the user's authority over the customer before subscribing.
