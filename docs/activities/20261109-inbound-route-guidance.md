# Inbound route lookup guidance

The agent attempted `GET /Telephony/DID` and an invented `/Telephony/Route`, then reported it could not read the inbound route. The supported `POST /Telephony/DID/Search` returned HTTP 200 using the same agent credential.

Updated `sufficit-api` to 1.0.27. The telephony reference now distinguishes DID configuration from destination catalogs, SIP registration and call history; documents the read-only search method; resolves direct-call endpoint GUIDs to extension titles; and requires actual failure evidence before reporting access unavailable.

Bound the same guidance as a focused private skill through the existing Fleet command, without installing the entire business API reference into every support turn. Binding ID: `ddd0385b-9425-4d07-95ae-308260fe58fe`. Read-back confirmed all four bindings in the effective session instructions. Active sessions retain their previous snapshots.

## Plain-language retest

The first isolated test (`93578429-f030-444f-ad50-5a74f58e69c6`) was invalid: a shell-only tool policy and an abbreviated prompt omitted the operational helper instructions available in the real mission. It reported missing tools; this is not evidence that the updated production workflow is inaccessible.

Repeated in isolated session `7f74d4a1-f8ee-49a0-af58-3fe2188f1009` with the original preset and full original mission context/history, replacing only the initial skill snapshot. The original user request is exactly `confira as rotas`. No expected DID mapping was supplied. Tool discovery is enabled as in ordinary support. Explicit test instructions forbid configuration changes, Fleet operations, group/workspace updates and messages. The retest completed. Inspected actual tool results: `POST /Telephony/DID/Search` and the context endpoint list both returned HTTP 200. The agent resolved each direct-call GUID against the returned endpoint IDs and correctly reported `(21) 2284-6230 → 0004016001` and `(21) 3899-2804 → 0004016002`. It did not ask the operator for an API path or say the inbound route was unreadable.

The test passes the requested route-reading outcome, not the entire narrative: the final reply also incorrectly described calls before 14:28 as occurring after the report. Distinct registration IPs also do not independently prove distinct physical devices. Those claims are not used as route validation evidence. The configured DID mapping does not prove the executed route or resolve the original ringing complaint.

All 185 packages passed repository validation; skill-creator validation and whitespace checks passed. No production telephony configuration or WhatsApp message was changed by the test.
