# WhatsApp calls by SIP for customer numbers

Scenario: a platform handling only WhatsApp calls (SIP to your PBX) for customers whose messaging remains with another provider. Everything below has been confirmed in production.

## Checklist (all at once)

1. Live mode app with `whatsapp_business_management` and `whatsapp_business_messaging` in advanced access.
2. Tech Provider onboarding completed in case of use WhatsApp (if not the customer sees "<app> cannot integrate customers at the moment").
3. Business Login Config: General variation, user token, permissions `business_management`, `whatsapp_business_management`, `whatsapp_business_messaging`. The variation "Cadastro incorporado" (Embedded Signup) serves to register new number; number that is already with another provider appears "Unqualified".
4. The customer shares WABA with the app owner business (business settings → WhatsApp Accounts → Partners → Assign partner). The customer login alone gives only user permission: Meta marks the app as `BLOCKED` to SIP and does not send the INVITE (the caller sees "calling", the PABX does not see anything).
5. SIP server recorded in the number with the app itself token (`POST /{phone_id}/settings` → `calling.sip.servers`). SIP servers are per app.
6. Server with TLS (valid certificate), firewall allowing Meta network ranges, and a destination that rings.

Customer business verification (`141010`, `LIMITED` error) did not prevent calls.

## Diagnosis

- `GET /{phone_id}?fields=health_status` → entity `APP`, field `can_receive_call_sip` (not `can_send_message`).
  - `141011` in APP → missing item 4 (or permission of messages).
  - `138025` → missing item 5 for this app.
- Health delay: after item 4 the call was already working and health still showed `BLOCKED`. Confirm with a real call.
- Compare with a client that works: `client_whatsapp_business_accounts` of your business, `GET /{waba}/subscribed_apps` and the health of his number.
- Asterisk: `pjsip set logger pcap /tmp/x.pcap` saves SIP decrypted without a console; the `pjsip set logger host <network-range>` filter does not filter in some versions (record everything — quickly turn off).

## Separate calls from messaging

If you need to sign up for the app in the client's WABA, leave the WABA webhook of the app without fields (`DELETE /{app}/subscriptions?object=whatsapp_business_account&fields=messages,calls`): the registration is only as an authorization and no customer message reaches you.

## Browser login

- Chrome with FedCM turns `FB.login` into `dialog_source=fedcm&scope=openid` and loses `config_id` → "app not available". Open the OAuth (`/dialog/oauth?client_id&config_id&response_type=code&override_default_response_type=true&redirect_uri&state`) dialog in your own window and receive the code on a return page of the same domain.
- SDK JS domains and redirect URIs are app-only and editable by UI.
- "App not available" soon after publication is usually propagation: test with an account that has no role in the app.
