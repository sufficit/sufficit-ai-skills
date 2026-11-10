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
5. Retrieve `documentUrl` from the same issuance record and verify the PDF as
   described below before delivery.
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


## Retrieve and inspect the PDF

Prefer the ready PDF returned through the issued record's `documentUrl`. Discover
its live operation before calling it. A provider payment page (`ProviderHtmlUrl`)
is HTML, not the delivery document: do not print or reconvert it as a substitute.
The legacy `Finance/BankSlip/Download` operation historically converted that HTML;
updated deployments stream the same provider PDF as `public/finance/bankslips`.
Check the deployed contract rather than assuming the repair is installed. These
routes stream a provider document; a Sufficit filename or branding does not prove
that Sufficit rendered the PDF.

Open the downloaded file in an available PDF viewer or render its pages and
inspect them before claiming the document is ready to send. Verify legibility,
layout and the payer, amount and due date against the same issuance record. MIME,
PDF signature, byte size and successful save validate transport, not visual
correctness. Multiple pages alone do not establish a defect. If visual inspection
is unavailable, state that limitation instead of claiming it passed.

For a broken file, reread the existing boleto and obtain its ready PDF; preserve
the issuance ID and idempotency key. A layout defect does not justify reissuing,
switching providers or creating another charge. If the alternative document also
fails, report the document failure and retain the valid issuance for recovery.

`documentUrl` requires public access enabled under the current contract. A bearer
token on a legacy anonymous Download alias does not bypass that policy. Do not
enable public access implicitly to work around a missing private document route;
report the actual policy restriction when it prevents delivery.
