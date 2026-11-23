# Remote commands and firmware evidence

## Authenticate a provisioning management request

Use the connected provisioning helper when available. For an interactive operator without a suitable provisioning session, use the public OAuth client `sufficit-telephony-provisioning-cli`. Start at the Sufficit Identity discovery document (`https://identity.sufficit.com.br/.well-known/openid-configuration`). POST form fields `client_id` and `scope=openid roles entitlements provisioning.manage` to its device authorization endpoint. Show the operator the returned verification link, user code and expiration. Keep the private device code with the polling client. At the token endpoint redeem it with the same client ID and `grant_type=urn:ietf:params:oauth:grant-type:device_code`, respecting the returned interval, pending approval and expiry.

Use the access token as a Bearer over HTTPS. The provisioning API expects a signed access token with audience `sufficit-provisioning`. A successful login alone proves only that Identity authenticated the operator. On 401 check expiry, issuer, audience and token format before requesting another login. Tokens issued for the chat host or temporary Identity Management capabilities serve different resources. On 403 inspect the operator's management permissions and customer scope. Keep bearer values, private device codes and SIP credentials out of chat, logs and activity records.

## Read diagnostics by MAC in Blazor

Open **Provisionamento → Dispositivos** (`/pages/provisioning/dashboard`) and find the exact MAC in the device table. Read **Diagnóstico** in that row. Each item with evidence shows its source and observation time in Brasília time.

| What the row shows | What it establishes |
| --- | --- |
| **Configuração** | The result of the latest configuration request, including transport when recorded. **Entregue sem credenciais** means the server delivered a sanitized configuration. |
| **Firmware** | The latest recognized GXP16xx HTTP(S) response tied to the phone's declared DevId. HTTP 200 is a complete response and HTTP 206 covers a range. This evidence describes the server response. |
| **Versão instalada** | A live PJSIP contact reported the model and version and matched the MAC, extension and customer. With only an HTTP User-Agent observation, the row shows **Versão informada**. |

For API reads, the scoped device list returns the configuration fields `lastRequestAt`, `lastDelivered`, `lastSanitized` and `lastConfigTransport`, plus `firmwareTransfer` when captured. To review individual firmware responses, use `GET /api/management/v1/diagnostics/requests?mac=<MAC>&outcome=firmware-http`. The screen assistant's `provisioning_summary_read` covers the currently loaded page.

**Sem registro** means the source has no matching event. The firmware collector starts with new requests at the known GXP16xx image paths and does not import old Nginx logs. A phone registered through chan_sip can have a version reported via HTTPS while the Blazor row still lacks live PJSIP evidence. For older transfers or paths outside the collector, use the log correlation described below.

## Ask the phone to act

1. Confirm the customer, linked extension, exact MAC and current SIP contact. Read `GET /api/management/v1/devices/commands?mac=<MAC>` on the provisioning API. A 200 with the command list validates read access. For read-only validation, stop here.
2. For an authorized action, check active calls before an operation that can interrupt service. POST to the same route using the catalog's **name**, e.g. `{"command":"check-sync","reason":"Apply updated device configuration"}`. Grandstream offers `check-sync` to fetch configuration and `reboot` to restart. Cisco SEP offers vendor-specific restart/reboot commands and requires a current PJSIP registration with its REGISTER Call-ID.
3. A response with `sent=true` records dispatch by the PBX. Follow the subsequent configuration request and SIP registration. After a timeout or an ambiguous response, check timestamps and device state before another command. When the desired version already appears on a live contact, the update is complete.

## GXP16xx firmware over HTTPS

- Bind the live model and software version to the intended MAC and customer. The catalog profile `GrandStream/V1` covers several devices. Enable firmware advisories only when the model is confirmed and its observed version compares below the approved version for that model. Clear the advisory when the device reports the target or a newer version. A download alone leaves installation unverified.
- For a confirmed compatible GXP16xx, verify the deployed image against the vendor release for its exact model. Enable the individual property `gxp1600_https_firmware` with string value `"true"` through the scoped device PUT. Preserve the current vendor, model, display name and description, send the changed property and re-read it. The renderer sets P6767 to 2 and P192 to `provisioning.sufficit.com.br:26511/static/grandstream/gxp1600`. Configuration delivery can continue over TFTP. Changing firmware transport does not require an extension technology change.
- Start with the per-MAC diagnosis. If it lacks a firmware event, use the serving node logs. For the firmware itself, correlate the exact GET path, time, HTTP status and bytes with the phone's User-Agent (model, SW version and DevId/MAC). On the validated port 26511 listener, requests appeared in the serving node's general Nginx access log, `/var/log/nginx/access.log`. Check the effective listener and relevant nodes. Multiple phones may share a public IP. A probe by curl confirms server availability only.
- Some phones append a stored prefix. On 404 inspect the exact requested URI. The deployed GXP1600 image is available both at `/static/grandstream/gxp1600/gxp1600fw.bin` and at `/static/grandstream/gxp1600/grandstream/v1/gxp1600fw.bin`. Verify the expected image digest at the failing path before retrying. Repeated HTTP 206 responses can be normal range downloads. Ringtone requests are separate files.
- Confirm installation from a fresh SIP registration with a live contact reporting the new version, or from a later device request showing the same DevId and new SW version. Record configuration delivery, firmware transfer and installed version separately. Treat a cached User-Agent on an expired contact as historical evidence.
