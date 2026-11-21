# Verify SIP credentials for a customer interconnection

In **Telefonia → Interconexões**, enter the **Host**, **Usuário SIP** and
**Segredo** with the customer's REGISTER authentication mode. Click
**Testar registro SIP** before saving. The receipt checks credentials through a
REGISTER without Contact. The server's active bindings are unchanged.

1. Resolve the customer's `contextId` and verify the applicable telephony
   entitlement and interconnection ownership. Follow the
   [customer-write guard](../../sufficit-api/references/customer-write-context.md).
2. Check the deployed contract. Use
   `POST /Telephony/interconnection/registration-test` with `contextId`,
   `interconnectionId`, `host`, `username` and `password`. Use the zero UUID
   for a new draft. Omit `node` and use optional `port` and `transport` for
   the public registrar. Defaults are UDP/5060 or 5061 when using TLS.
3. Use the password supplied by the customer through the private HTTPS
   input or editor. Keep it out of prompts, diagnostics and transcripts.
   The synchronous POST and async status GET are excluded from generated
   MCP tools.
4. Report `CredentialsConfirmed` only when the registrar accepts an
   authenticated request. `CredentialsNotVerified` means it accepted the
   query without asking for credentials. A rejected query can also mean the
   carrier does not support authentication without Contact. Check the SIP code
   and `history` and report the observed result.

A legacy client that passes `node` explicitly invokes the temporary-contact
flow and its existing authorization rules. Use the credential check for
new tests. The [carrier onboarding workflow](carrier-sip-line-onboarding.md)
covers the node, contact, call routing and activation of the permanent line.

## Optional asynchronous mode

Verify that the deployed API supports `async=true` before using it. Send
the same POST with `?async=true` and a new UUID in `Idempotency-Key`. The
first response is `202 Accepted` with `Location` and `Retry-After: 1`.
Read that location or use
`GET /Telephony/interconnection/registration-test/{id}?contextId=…`.

- `202` returns the current `history`. `200` means the run ended and returns
  the full history and SIP outcome in `result`. Check `result.status`
  before reporting whether the credentials were verified.
- Reuse the same key after an uncertain response. It identifies one run for
  that user and customer for 10 minutes, including across API instances.
  Changing the interconnection, node, registrar, port, transport or username returns `409` for
  the same key. Generate a new key only for a deliberate new test, such as
  after changing credentials. The API does not compare passwords on replay.
- An interrupted executor becomes `Interrupted` on the next status check
  after 30 seconds. Check the receipt before a new attempt. A `503` may indicate that the
  shared store or execution capacity is temporarily unavailable.
- An authenticated `/ws` connection receives
  `InterconnectionRegistrationTestChanged` for the job owner. The SignalR
  event carries `jobId`, `revision`, and `status`. Fetch `Location` for the
  actual result and use the same GET to reconcile after disconnects, missing
  events or out-of-order notifications.
