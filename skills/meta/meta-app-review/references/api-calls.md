# Useful API calls (and those that count as test)

All with `appsecret_proof` when the app requires app-secret proof: `proof = HMAC-SHA256(access_token, app_secret)`.

```bash
APP=<app_id>; SEC=<app_secret>; AT="$APP|$SEC"      # app token
proof(){ printf '%s' "$1" | openssl dgst -sha256 -hmac "$SEC" | sed 's/^.* //'; }
```

## Check token before anything
```bash
curl -s "https://graph.facebook.com/v22.0/debug_token?input_token=$T&access_token=$AT"
```
Look at `app_id`, `type`, `expires_at` and `granular_scopes[].target_ids` (`null` = unrestricted; array = only those assets).

## App settings (requires "API access to settings")
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$APP" \
  --data-urlencode "app_domains=[\"example.com\"]" \
  --data-urlencode "privacy_policy_url=https://example.com/privacy" \
  --data-urlencode "access_token=$AT"
```

## App webhooks
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$APP/subscriptions" \
  --data-urlencode "object=whatsapp_business_account" \
  --data-urlencode "callback_url=https://host/webhooks/whatsapp" \
  --data-urlencode "fields=messages,calls" \
  --data-urlencode "verify_token=$VT" --data-urlencode "access_token=$AT"
```
`object=page` to Messenger. Meta does a GET verification: the endpoint has to respond 200 with `hub.challenge`.

## Subscribe the app to an asset
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$WABA/subscribed_apps" -d "access_token=$USER_OR_SU_TOKEN"
curl -s -X POST "https://graph.facebook.com/v22.0/$PAGE/subscribed_apps" \
  -d "subscribed_fields=messages,message_deliveries,message_reads,message_echoes" -d "access_token=$PAGE_TOKEN"
```

## WhatsApp number
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$PHONE/register" -d messaging_product=whatsapp -d pin=000000 -d "access_token=$T"
curl -s "https://graph.facebook.com/v22.0/$PHONE?fields=status,platform_type,is_on_biz_app,health_status&access_token=$T"
```
`health_status` says exactly what blocks sending and calling (by number, WABA, business and app).

## Calls that count as a test, by permission
| Permission | Call |
|---|---|
| whatsapp_business_management | `GET /{waba}?fields=id,name` · `GET /{waba}/phone_numbers` · `GET /{waba}/message_templates` |
| whatsapp_business_messaging | `POST /{phone}/messages` (template or response in window) |
| business_management | `GET /me/businesses` |
| pages_show_list | `GET /me/accounts` |
| pages_manage_metadata | `POST /{page}/subscribed_apps` |
| pages_messaging | `POST /me/messages` with page token |

Use token from the app being analyzed. The 24h temporary token of the screen "Step 1. Try" fits.

## System user (token that does not expire)
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$BUSINESS/system_users" -d "name=Integration" -d "role=EMPLOYEE" -d "access_token=$ADMIN"
curl -s -X POST "https://graph.facebook.com/v22.0/$BUSINESS/access_token" \
  -d "scope=business_management,whatsapp_business_management,whatsapp_business_messaging" -d "access_token=$ADMIN"
```
User token dies when the person logouts; system user does not.
