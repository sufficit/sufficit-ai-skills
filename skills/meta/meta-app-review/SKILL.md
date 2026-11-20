---
name: meta-app-review
description: "Prepare Meta apps (WhatsApp, Messenger, Instagram) for App Review and operate Business Manager. Use to create or configure app in a portfolio, request advanced access to permissions like whatsapp_business_management, whatsapp_business_messaging, pages_messaging and business_management, record required screencasts, connect Page or WhatsApp Business account to a platform, or diagnose webhooks, Facebook Login for Business, WhatsApp numbers and Graph API errors in these streams."
metadata:
  version: "1.0.7"
---

# Meta App Review

Prepare a Meta app for review submission while avoiding misleading responses. Details are in `references/` and should be read only when the step requires.

## The rule that costs the most time

Much of what decides approval only exists in the interface, and Graph API returns `success` for operations that do not produce effect. Separate before automating:

| Only in the interface (developers.facebook.com) | By API |
|---|---|
| create, rename and link the app to a portfolio | Basic settings after connecting API access in Settings > Advanced |
| products, use cases and permissions | app webhooks (`POST /{app}/subscriptions`) |
| Facebook settings Login for Business (generate `config_id`) | subscribe the app to an asset (`POST /{ativo}/subscribed_apps`) |
| JavaScript SDK domains and redirect URIs | register number (`POST /{phone}/register`) |
| addressees of the test number | send messages, read templates, `debug_token` |
| become Tech Provider and send for analysis | system user tokens |

## Order that works

1. Business verified (`verification_status: verified`); without this there is no advanced access.
2. App and assets (WABA, Page) in the same business. Webhook is only delivered to the business app owner of the asset — see [traps](references/pitfalls.md).
3. Complete basic configuration: icon 1024x1024, privacy policy, terms, data deletion instructions, category. Reuse an already approved app when available.
4. Use cases and permissions, which begin in standard access ("Ready for testing").
5. Tech Provider. Meta itself warns that it is irreversible. Ask for explicit confirmation from the person responsible before accepting.
6. Allowed usage, per permission: description, screencast, test API call and acceptance.
7. Data processing and instructions for the analyst with a functional test account.
8. Send. After submission, editing and cancellation are unavailable.

Screen paths and content of each section: [approval flow](references/approval-workflow.md).

## Enable the submission button

"Send for analysis" is disabled as long as a permission shows "0 out of 1 call(s) of mandatory API(s)". Make a typical call of each permission with token from the analyzed app — writing when permission allows you to write — and wait: Meta informs up to 24 hours for the counter to reflect. Filling out the form again does not help. Calls for permission in [API calls](references/api-calls.md).

## Screencasts

- Show the actual flow of the product, from the user's point of view, with English subtitles that name the permission in use. The same video can meet multiple permissions.
- Cut footage where clicks leave the screen blank.
- Do not record third party personal data (conversation lists, contacts). If they show up, stop and delete the file.
- Attaching file to drag and drop via script may not save; use the actual file selector. Recipes in [interface automation](references/ui-automation.md).

## Mistakes that deceive

| Message | Real Cause |
|---|---|
| "This app needs at least a supported permission" | app with Facebook Login for Business: dialogue accepts `config_id`, not `scope` |
| "JSSDK option is not enabled" | enable "Entrar com o SDK do JavaScript" and register domain |
| "The domain of this URL is not included in the app domains" | strict mode enabled without URL in "valid OAuth redirecting URIs" |
| `(#10) Changing app settings through API calls has been disabled` | enable API access to Settings > Advanced |
| `(#100) Invalid parameter` when responding in Messenger | `MESSAGE_TAG` inside the 24h window; use `messaging_type: RESPONSE` |
| `(#133010) Account not registered` | Unregistered number in Cloud API or undone coexistence |
| `Register endpoint is not available for SMB businesses` | number in coexistence with WhatsApp app Business |
| `(#131030) Recipient phone number not in allowed list` | test number only sends to registered recipients |
| registered webhook and no event arrives | app from another business; only the owner of the asset receives |
| `141011` in APP (`can_receive_call_sip: BLOCKED`) | client did not share WABA with the app business |
| `138025` | SIP server not saved to the number with the token of this app |
| "<app> cannot integrate customers at the moment" | incomplete Tech Provider onboarding |
| "It seems that this app is not available" with `dialog_source=fedcm` | Chrome FedCM lost `config_id` |

Complete diagnosis in [traps](references/pitfalls.md). WhatsApp calls by SIP for customer numbers (who shares what, delayed health status, separate calls from messages): [SIP calling](references/whatsapp-calling-sip.md). An app for messages + calls and for voice only (clients with message in competitor or voice only), and the webhook rule for one app only: [messaging and calling scenarios](references/messaging-and-calling-scenarios.md).

## Security

- Analyst test credentials stay in restricted storage, never in conversation.
- Tech Provider, sending for analysis and data processing declarations are decisions of the app's controller: obtain confirmation beforehand.
- Do not change security of personal accounts, do not create PIN and do not link browsers to managed accounts when conducting the interface.
- Log the temporary changes made to record or test and undo them when finished.
