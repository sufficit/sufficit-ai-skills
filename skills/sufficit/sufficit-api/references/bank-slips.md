# Boleto issuance and delivery

For "gere um boleto de R$150 para amanhã e envie no grupo do cliente", resolve the
customer and date from the request/session, then carry out every authorized outcome.
The user does not need to know providers, endpoint names, GUIDs or where credentials live.

1. Search the corporate API for `BankSlip`, payer readiness, issuance, status and
   document operations. Read each operation's schema, including referenced body
   definitions; a search result saying `[body required]` is not the body contract.
   Querying a guessed class name is not a substitute for reading the schema.
2. Resolve the customer context unambiguously. If Hermes provides a `contextid`,
   verify it against the Sufficit customer. Inspect existing charges and payer
   readiness. Use the configured provider unless the user requested another one.
   Do not start by registering an ASAAS customer just because the request says boleto.
3. Determine amount and due date, including year, using the current date/timezone
   and the user's wording. Resolve genuine ambiguity before issuing. Preserve
   existing issuance IDs from the session and check their state before creating.
   If prior charges make a duplicate or the claimed unpaid debt materially unclear,
   surface that specific ambiguity rather than issuing another charge blindly.
4. Issue once with the discovered required fields and an idempotency key when
   supported. Preserve that key for this logical issuance. `Requested` or
   `Processing` is pending, not failure: follow the documented status operation
   with bounded waits. `Ready` confirms issuance; a failed or uncertain result
   requires reading state before retrying, not switching providers automatically.
5. Retrieve the document URL from the same issuance record and verify the PDF.
   For a request to open an attendance/send a collection message, load `hermes-api`
   and follow its attendance/PDF reference. Hermes has its own OpenAPI and personal
   Vault credential; absence of Hermes routes in Sufficit's spec proves nothing
   about access to Hermes. Retain the boleto ID while completing delivery.
6. Verify each requested result independently: boleto ready, correct conversation
   created/reused, outgoing message and PDF attachment present, delivery state if
   exposed. Reuse the user's supplied message without inventing debt facts. Report
   partial completion precisely if a concrete attempted operation blocks progress.

Before claiming inability, discover the relevant tools, load their instructions,
inspect the service's live documentation and attempt the supported authenticated
operation. Missing a specialized tool is not itself a blocker. An actual permission
or credential rejection is; preserve completed work and explain that exact failure.
