# Traps, with symptom and cause

## Webhook for an app from another business

`POST /{waba|page}/subscribed_apps` with token from another business app returns `{"success":true}`, the app appears in `subscribed_apps`, gives even to record `override_callback_uri` — and no event is delivered. Only the business app owner of the asset (or with the asset shared as a client) receives. Diagnosis: `GET /{asset}/subscribed_apps` with the page token/WABA of the app you want to check out; with token from another app the answer only shows its own registration.

## override of webhook gives `(#200) Permissions error`

`POST /{waba}/subscribed_apps` with `override_callback_uri` (or `webhook_configuration` in number) refusal with `#200` even with `business_management`, WABA with full access and verification of the working destination — and the registration without override goes true anyway (the event goes to the default callback of the app). Cause found: Token owner system user did not have paper on the app (only "install app" when generating token is not enough). Business settings → Apps → the app → Assign people → the system user → Manage app. After that the same token records the override. `POST /{app}/assigned_users` does not exist in API: only by interface. Similar report (other cause: WABA in client portfolio): chatwoot do-ai #568.

## network verification is not the problem (almost never)

Before blaming MTU/firewall: GET verification Meta are small and pass; Event POST is bigger. Prove with `POST` of 4 KB of the outside and `tcpdump` filtering Meta network ranges (`2a03:2880::/32`, `31.13/16`, `157.240/16`). If there's no input connection, the problem is on their side.

## Login for Business x Classic Scope

Business App type has Login for Business and the dialogue refuses `scope`: "This app needs at least a supported permission". Use `config_id`.

## FedCM on Chrome Android ignores config_id

On Android, SDK enters the federated Chrome login (`dialog_source=fedcm`, `scope=openid`) and discards the `config_id`. Workaround: Chrome > Settings > Website Settings > Third-party Login > "Block Requests". Then comes the normal dialogue. Undo it later.

## Coexistence (SMB)

`GET /{phone}?fields=is_on_biz_app` = `true` means number in the WhatsApp app Business with Cloud API coupled. `POST /{phone}/register` answers `Register endpoint is not available for SMB businesses`, and submits `133010`. He just reconnects by retracing the coexistence record on his mobile phone that has the app.

## Meta test number

It comes in case of use WhatsApp ("Step 1. Try"). You can be unregistered: `POST /{phone}/register` with any PIN solves. Only sends to registered recipients in UI (Meta sends a 5-digit code by WhatsApp to the number). `141006` in WABA test only blocks conversation started by the company; response inside the window works.

## Messenger API

Send `messaging_type: MESSAGE_TAG` + `tag: ACCOUNT_UPDATE` within the 24h window → `(#100) Invalid parameter`. Inside the window the correct one is `messaging_type: RESPONSE`.

## Standard access limits to those who have a role in the app

With default access, the app only exchanges message with who is admin/dev/tester of it. To record the video, use an account with an app role as a "client".

## Screencast Upload

Drag and drop by script shows "screencast loaded" but may not save. Use the actual file selector. On Android, Chrome only reads `/sdcard` with granted storage permission (`pm grant ... READ_EXTERNAL_STORAGE`); without it the Meta answers "Couldn't load the image".

## "0 of 1 call of API mandatory"

Not missing form: is the Meta counter, which takes up to 24h. Make the call with token from the new app and wait.

## Tab discarded on Android

When opening the consent window, Android can discard the back tab by memory; on return, the login response is lost and the flow restarts. Retrace login (the second time is fast, "you have already linked").

## Three locks hidden at the end of the submission
- `pages_messaging`: In addition to the reproduction instructions, there is a selector "Select a Page"; the item only concludes with the chosen Page.
- With all permissions in "Edit", the "Use Allowed" section continues unmarked until you click "Next" inside it.
- The final dialog has an acceptance box of the Platform Terms; without checking it, the "Send" button of the dialog is disabled and the click does nothing.
