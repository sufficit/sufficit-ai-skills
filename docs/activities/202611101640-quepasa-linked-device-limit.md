# QuePasa linked-device limit in call diagnostics

A customer QuePasa session (Linkweb Telecom, +55 71 9735-8658) was `Ready` with calls enabled. Calls placed from WhatsApp Web reached the PBX; calls placed from phones showed "Chamando…", rang only on the customer's physical phone and left no call event in the owning pod. Messages from the same phones did reach the session, and the same caller phone reached another QuePasa number.

The account had five companion devices besides the phone (IDs 4, 6, 7, 8 and a Meta coexistence device `:99@hosted`). WhatsApp delivers calls to at most four companions; above that, call notifications reach them unpredictably.

## Delivery

- `sufficit-endpoints` `2343ac5`: the WhatsApp diagnostic, and therefore the telephony check-up, reports `quepasa_linked_devices_count` as `Error` above four companions with the device list; position is the rank among companions. Deployed to eveo-apps, castrum-apps and apoint-apps.
- `sufficit-api` 1.0.35: [WhatsApp gateway reference](../../skills/sufficit/sufficit-api/references/whatsapp-gateway.md) explains the limit, symptom and customer action.
- `quepasa-production` 0.1.2: [runbook for calls missing on a ready session](../../skills/quepasa/production/references/runbooks.md#calls-missing-on-a-ready-session).

No customer session, device or route was changed.
