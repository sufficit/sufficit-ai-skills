# Customer WhatsApp number diagnostics

The support agent searched a customer WhatsApp number as a SIP endpoint/PSTN DID, then used the agent device's personal WhatsApp status/pairing tools. The pairing attempt failed. Those tools do not inspect a customer's existing gateway session.

## Operational findings and delivery

The requested Brazilian number resolves to a canonical WhatsApp WID without the mobile ninth digit. Current production health returned HTTP 200, `success=true`, `Ready`, fresh runtime ownership on `quepasa-prod-eveo`, calls processing enabled and VoIP `exclusive`. The live session's tenant context is empty.

A separate downstream telephony route does exist, is enabled and points to announcement 2592. It was found by the exact session credential linkage, not by assuming the phone or session-record GUID is the route key. Its customer context is present, which differs from the empty QuePasa session context. This discrepancy is evidence to investigate, not proof of the cause of failed calls.

An old database copy on eveo-data contains an obsolete UnVerified session. It was rejected as current-state evidence after checking timestamps and comparing with the actual Kubernetes production Galera/runtime and live public API. No historical record was changed.

Rafael's existing API credential gets a real HTTP 403 on the gateway route/context query. The exception identifies business context authorization; the generic `insufficient_scope` header does not establish missing OAuth scopes or justify reconnecting. No roles or entitlements were widened.

Provisioned a private credential for this exact session and a read-only diagnostic helper. Only the confirmed number aliases are accepted; output is whitelisted and credentials stay out of prompts, artifacts and replies. Optional verified customer-context configuration allows the helper to use the existing Sufficit API client for route reads; API refusals remain visible. It cannot pair, send, restart or change configuration. Its session token is a normal session credential, not a new gateway-enforced read-only role; the helper constrains the operations it exposes. No masterkey or owner-wide key was installed in the agent.

Updated `sufficit-api` to 1.0.28 with a WhatsApp voice gateway reference and `quepasa-production` to 0.1.1 with the reusable session-scoped helper. Updated Rafael's existing injected routing skill, preserving his four bindings.

## Verification

Live helper reads confirmed Ready and the separate route HTTP 403. An unprovisioned number is rejected. Both skill packages passed skill-creator validation; all 185 packages passed integrity validation. No production session, telephony route or customer message was changed.

Retest session `14150cf2-7011-47be-8840-2b8edc5d1b33` reuses the original WhatsApp mission/history and the user's gateway clarification with updated injected guidance. It allows read-only shell access and forbids pairing, sends, session controls and workspace changes. The retest completed. Its only tool call invoked the scoped helper; it correctly identified the canonical WhatsApp account, live Ready state, process/effective calls, exclusive VoIP mode, empty session context and the separate HTTP 403 route refusal. It did not invoke pairing or advise reconnection/token renewal.

This passes the requested resource-identification and live-session diagnostic outcome. It does not prove end-to-end calls or fix route authorization. The final answer still speculated about route/destination as the cause and asked for customer information even though the helper supplied a context hint; neither is treated as a verified diagnosis. Operator findings identify the existing route, while the agent's own gateway API permission remains a concrete limitation.

An earlier exploratory retest (`50713666-e210-40d7-814b-9b26043c97a0`) correctly read Ready but guessed the route identifier and recommended reconnecting for 403. The final guidance explicitly addresses both errors; that answer is not the acceptance result.
