# Device auto-provisioning reference

sufficit-telephony-extensions 0.7.0 adds references/device-provisioning.md. The
existing provisioning.md covers extension creation only, so the support agent
had no basis to answer how a phone downloads its configuration.

Content verified against production on 2026-11-11: public host
provisioning.sufficit.com.br; TFTP UDP 69, HTTP 80, HTTPS 443 and 26511 with a
valid certificate; no device authentication; per-model paths (Intelbras TIP125i
intelbras/tip125i/<MAC>.xml, GrandStream, Cisco, Linphone); management API
routes for devices, download requests, summary, discoveries and device upsert.
It records that the access log has no transport/port, that a MAC request proves
only that device, status code meanings (200/204/500) and the rule never to
download or paste a device file (it carries the SIP secret).

No customer identifiers are included. Package digest/version updated in the
catalog; all 185 packages validated and Markdown coverage passed. The Fleet
support agent receives a short pointer in its bound diagnostic skill and a copy
of the reference in its executor workspace (40000-character budget kept).
