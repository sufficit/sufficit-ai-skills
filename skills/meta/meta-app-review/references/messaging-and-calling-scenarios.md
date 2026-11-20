# Scenarios: message + calls × only calls

A platform can use the same Meta app for two products:

1. Full service (WhatsApp messages + calls): The app receives messages via webhook and calls by SIP (or by API).
2. Voice only: The app only delivers calls by SIP to a PABX. Here are two types of customer:
   - 2a — Messenger with another provider: WABA continues with his message provider; you only answer calls and cannot receive messages.
   - 2b — voice only: the customer does not use messaging anywhere.

## By scenario

| | 1. Messages + Calls | 2a. Voice only, messages in competitor | 2b. Voice only |
|---|---|---|---|
| Login Config (see below) | Embedded Signup | General + user token | Embedded Signup (new) or General (existing) |
| WABA shared with app business | automatic Embedded Signup | customer assigns you as partner | automatic (new) / manual (existing) |
| Message webhook | on, pointing to the platform | off | off |
| SIP in number, recorded with the app token | yes | Yeah. | yes |

In scenario 2a, without partner sharing, Meta marks the app as `BLOCKED` for SIP (`141011`) and does not deliver the call. See [SIP calling](whatsapp-calling-sip.md).

In 2b the number still needs to be in Cloud API (`CONNECTED`, approved name, registered with `POST /{phone_id}/register`). Messages that arrive at this number are not routed anywhere; agree on this behavior with the customer.

## A scenario login config

Create a Facebook configuration Login for Business by scenario, even if two stay the same for Meta — you can track who entered where and change one scenario without affecting the other:

| Scene | Difference | Token | Assets/product |
|---|---|---|---|
| 1. Messages + Calls | WhatsApp Embedded Signup | system user, expiration Never | WhatsApp accounts; product only WhatsApp Cloud API |
| 2a. Voice only, messages in competitor | General | user (act on behalf of client) | none; permissions `business_management`, `whatsapp_business_management`, `whatsapp_business_messaging` |
| 2b. Voice only | WhatsApp Embedded Signup | system user, expiration Never | WhatsApp accounts; product only WhatsApp Cloud API |

Traps when creating in the dashboard (Facebook login for Business → Settings → Create):

- mark "WhatsApp Cloud API" can tag "API Marketing Messages" together — uncheck;
- standard expiration of token is 60 days; choose Never to avoid reauthorization;
- the embedded registry shows already active numbers in another provider as "Unqualified" — for them use General config (2a) and partner sharing;
- editing an existing configuration stops at the product step; to see the rest, create another.

## Webhook is app, not client

WABA webhook fields (`messages`, `calls`) are valid for all WABAs in which the app is registered.

An app only works when every client in scenario 1 is a messenger client from the platform itself (does not use another system) — receiving his messages is the goal. The only rule applies to 2a: before connecting `messages` to the app, each WABA customer with concurrent messaging needs to be

1. Unsubscribed from the app (`DELETE /{waba}/subscribed_apps`) — for SIP what releases the call is partner sharing; confirm with a call that registration is not required; or
2. subscribed with `override_callback_uri` pointing to a receiver that only confirms and discards.

Without this, the messages of a customer whose messaging is handled by a competitor reach your platform.

Safer pattern (adopted in Sufficit): The app's default callback points to a receiver that only responds to verification and discards (200 without reading the body), and each WABA of messenger client receives `override_callback_uri` for the platform. Thus, any WABA registered without override — voice-only client, new client, test account — never delivers messages to anyone. To save override the token system user must have a role in the app (see [traps](pitfalls.md), `#200`). Register on voice onboarding if the client is 2a or 2b.

If you can't guarantee this rule, use two apps in the same business (one voice only, no WABA webhook fields); each needs its own approvals, SDK domains and configs.
