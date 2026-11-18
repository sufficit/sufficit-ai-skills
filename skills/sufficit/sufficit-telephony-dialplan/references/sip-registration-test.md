# Test a customer interconnection's SIP REGISTER

Use this workflow for **Telefonia → Interconexões → Testar registro SIP** or
for the equivalent API operation. The test sends a temporary SIP REGISTER
from a selected node. It leaves the draft unsaved and keeps calls, DIDs and
routes out of the operation. A separate test can verify INVITE or call delivery
when requested.

## Before sending REGISTER

1. Verify the customer's `contextId`, the interconnection's ownership and the
   effective telephony permission for that customer. Follow the
   [customer-write guard](../../sufficit-api/references/customer-write-context.md).
   A new draft uses the zero UUID for `interconnectionId` and requires its
   own authorization.
2. Confirm that the account uses REGISTER. Read the deployed OpenAPI and use
   `GET /Telephony/interconnection/registration-test/targets?contextId=…&interconnectionId=…`
   to check the available node and registrar tuples. The POST requires the
   exact authorized node, host, port, transport and SIP username for that
   customer and draft. HTTP `200 []` confirms the scoped lookup passed but
   returned no eligible destination. Check the matching
   `Telephony:RegistrationTests:Authorizations` entry and node inventory with
   the Sufficit configuration owner. A GET `403` means the context or
   interconnection is outside the allowed scope for this caller. A POST
   `403` can also indicate that the tuple or the exact username does not
   match. Target listings omit usernames and do not authorize every user on
   a listed host.
3. Confirm that the registrar accepts a separate contact for up to 30 seconds
   without replacing active contacts. Use an authorized account. For an
   externally managed interconnection, get this evidence from the customer's
   technical owner or their verified account configuration. Direct carrier
   confirmation is not a prerequisite for that operating model. Leave
   `AllowsIsolatedContact` unset or false until the behavior is verified.
   When the evidence is missing, stop before POST.
4. The POST and async status GET are excluded from the generated MCP tools.
   Use authorized HTTPS with a private secret input path or use the
   **Testar registro SIP** action in the interconnection editor. Keep the
   password out of prompts, chat, tool arguments recorded in transcripts,
   command-line arguments and diagnostics. If there is no secure route for
   the agent to use the credential, ask the authorized person to enter it in
   the editor. A test registration receipt alone does not attest to the
   preservation of other contacts. If proof is requested, compare independent
   before-and-after registrar evidence from the account owner.

## API response and timing

Send `POST /Telephony/interconnection/registration-test` with `contextId`,
`interconnectionId`, `node`, `host`, `port`, `transport`, `username` and
`password`. The synchronous mode is the default and returns a complete
result in one response. The API budgets 3 seconds to establish SSH and
10 seconds for the remote command. The probe budgets 2 seconds for DNS and
connection, 4 seconds for REGISTER including authentication, and 2 seconds
for withdrawal. A REGISTER timeout still leaves an independent withdrawal
attempt. The contact's 30-second expiry is a separate timer.

Report the node from the receipt. Use `history` in observation order for
UTC time, SIP challenge, authenticated attempt, final SIP code and cleanup.
An initial `401` or `407` is a challenge. `Registered` requires a 2xx
acceptance with the temporary contact confirmed for the short expiry.
Report rejection, timeout, and inability to confirm the contact using their
observed status. `cleanup=Unconfirmed` means withdrawal could not be verified,
even when REGISTER succeeded. `NotRequired` indicates that withdrawal was
unnecessary. Keep HTTP status, SIP status and cleanup status distinct.

## Optional asynchronous mode

Verify that the deployed API supports `async=true` before using it. Send
the same POST with `?async=true` and a new UUID in `Idempotency-Key`. The
first response is `202 Accepted` with `Location` and `Retry-After: 1`.
Read that location or use
`GET /Telephony/interconnection/registration-test/{id}?contextId=…`.

- `202` returns the current `history`. `200` means the run ended and returns
  the full history and SIP outcome in `result`. Check `result.status` and
  `result.cleanup` before reporting success.
- Reuse the same key after an uncertain response. It identifies one run for
  that user and customer for 10 minutes, including across API instances.
  Changing the interconnection, node, registrar, port, transport or username returns `409` for
  the same key. Generate a new key only for a deliberate new test, such as
  after changing credentials. The API does not compare passwords on replay.
- An interrupted executor becomes `Interrupted` on the next status check
  after 30 seconds. Report the uncertainty of withdrawal and check the
  receipt before starting a new attempt. A `503` may indicate that the
  shared store or execution capacity is temporarily unavailable.
- An authenticated `/ws` connection receives
  `InterconnectionRegistrationTestChanged` for the job owner. The SignalR
  event carries `jobId`, `revision`, and `status`. Fetch `Location` for the
  actual result and use the same GET to reconcile after disconnects, missing
  events or out-of-order notifications.

Endpoint source reference for the optional mode and WebSocket event: `d77d760`.
