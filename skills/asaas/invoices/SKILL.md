---
name: asaas-invoices
description: "Query and schedule production ASAAS NFS-e invoices with asaas_invoices_list, asaas_services_list, and asaas_invoices_create; cancel with asaas_invoices_cancel when available. Omit municipal service fields by default so account configuration supplies them. Never ask the user for a municipal code or invent one. Invoice descriptions come from the user. Municipal fields can create service entries or change existing invoice associations. Consult official documentation before assuming requirements, report discrepancies, query before writing, and obtain approval."
---

# ASAAS production service invoices

Use when the user asks to issue, schedule, view, check, or cancel ASAAS service invoices (NFS-e). Use plain language with the user. Query existing records and configuration rather than asking for IDs or codes you can retrieve.

## Official sources and updates

- Complete index, including future changes: [official Asaas API documentation](https://docs.asaas.com/llms.txt).
- Tax workflow: [invoice introduction](https://docs.asaas.com/docs/notas-fiscais) and [issuing NFS-e](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico).
- Contracts for [scheduling (`POST /v3/invoices`)](https://docs.asaas.com/reference/agendar-nota-fiscal), [listing invoices](https://docs.asaas.com/reference/listar-notas-fiscais), and [cancellation](https://docs.asaas.com/reference/cancelar-uma-nota-fiscal).
- Documentation changes. Check both the guide and endpoint schema/errors before treating a field as required or assuming an account default. For discrepancies, tool limitations, contract changes, municipal rejection, or missing tax data, tell the user what was and was not done and why. Report the issue to the plugin/skill maintainers for an update. Never expose the key, full CPF, or sensitive data in that report, and do not bypass the plugin with manual requests.

## Verified account queries: HTTP 200

On 2026-09-23, two real production queries returned HTTP 200 without scheduling invoices or modifying records:

| Operation | Purpose | Confirmed limitation |
| --- | --- | --- |
| `GET /v3/myAccount/commercialInfo` | Identify the account holder and query commercial details. | Does not identify the default invoice service. |
| `GET /v3/fiscalInfo/` | Query existing account tax configuration. | Did not return registered services or the default service ID. |

`serviceProvisionCityDefaultType` represents the default city of service provision, not the default service. HTTP 200 from these queries does not prove automatic completion of fields omitted when scheduling.

See [references/account-reads.md](references/account-reads.md) for contracts, useful fields, sources, and limitations. These are verified API capabilities; documenting them does not add tools to the plugin. Use corresponding tools only when available. Do not invent tool names or bypass missing tools with manual authenticated requests.

## Credential

- Tools resolve `personal/asaas/production/api-key` in the user's Sufficit Identity Vault.
- Never request the key in chat or put it in arguments, commands, or files. Handle `asaas_key_missing` and `asaas_vault_sign_in_required` through the same secure Vault screen flow as the other ASAAS skills.

## Registered service versus invoice description

`serviceDescription` is the description printed on the invoice. `municipalServiceId`/`municipalServiceCode` identify the municipal service classification. The former does not automatically become the latter.

The account owner's operational rule is that service details (municipal code, ISS, and tax name) are filled from the account service registration when omitted. The dashboard path is `Notas Fiscais › Configurações › Serviços`. Therefore, omit `municipalServiceId` and `municipalServiceCode` by default. Never ask the user for a municipal code or invent a code, ISS, or tax rate. Do not create a service or registration as part of issuing an invoice.

Official documentation checked on 2026-09-23 establishes the following:

- The [scheduling schema](https://docs.asaas.com/reference/agendar-nota-fiscal) does not require `municipalServiceId` or `municipalServiceCode`, so omission is accepted by the contract. It marks `taxes`, `observations`, and `deductions` as required, although this account issues invoices without sending them, using its registered tax configuration.
- Documented automatic values: `municipalServiceName` uses `municipalServiceCode` when the name is absent; Asaas calculates `pisCofinsRetentionType` (do not send it).
- The [guide](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico), intended for generic integrations, asks for `municipalServiceId` or `municipalServiceCode` (code for National Portal accounts). It does not describe account-based automatic completion. The schema permits omission; the account behavior is the operational rule. Automatic subscription invoicing is a separate flow configured per subscription.

If the provider rejects an invoice because of its service or tax details, present the actual reason in plain language. Report it to the plugin/skill maintainers with the source link and check date so this rule can be updated. Never fill fields blindly.

To reduce the user's burden, query invoice history and existing records. If one description is unambiguous and relevant to the current service, propose it with the amount, recipient, and date, and obtain confirmation before the write approval card. A previous description is only a reference; it does not prove that the same service was provided now. If evidence is missing or several choices exist, ask what service was provided without requesting a technical code. Never use a fictional "test service" description for a real tax transaction.

If the user explicitly chooses a specific municipal service, use `municipalServiceId` (if available) or `municipalServiceCode` (validated), never both. New registration requires an explicit request.

### Proven municipal-field side effects (sandbox, 2026-09-23)

Controlled sandbox experiments showed that scheduling an invoice can modify service registration. This reinforces omission as the default; it does not authorize unrestricted use of these fields.

- Service registration identity is `municipalServiceName`, not the code. Different names create separate dashboard entries even with the same municipal code.
- Sending only `municipalServiceCode` creates a new entry named after that code, such as `01.01.01`, without the official description.
- Reusing an existing name with a different code retroactively changes associations: queries for previously scheduled invoices with that name returned the new code.
- `municipalServiceId` alone is rejected even when the ID exists: HTTP 400, `invalid_action`, literal message "O campo municipalServiceName deve ser informado". The ID and name must be supplied together.
- The sandbox does not validate codes against the catalog. The nonexistent code `99.99.99` was accepted, scheduled, and authorized with an invoice number and documents. HTTP 200 there does not prove that a municipality would accept it.

When the user chooses a specific service, prefer `municipalServiceId` + `municipalServiceName`, using the exact `description` returned by `asaas_services_list`. Never construct a name manually or send only the code; these produced divergent test-account entries, removable only through the dashboard.

## Query invoices

`asaas_invoices_list` makes a fixed read-only `GET` request to `/v3/invoices`, with optional customer, charge, status, date-range filters and pagination. Each invoice includes its recipient: `customer` contains the resolved `id`, `name`, `personType`, and `document` (full formatted CNPJ, first three CPF digits). An unresolved customer remains an ID on the invoice and appears in `unresolvedCustomerIds`. Query `asaas_customers_list` before identifying that recipient.

Explain statuses plainly: SCHEDULED = scheduled, SYNCHRONIZED = sent to the municipality, AUTHORIZED = issued, CANCELED = canceled, ERROR = failed. Full contract: [references/invoices-list.md](references/invoices-list.md).

## Issue a new invoice: query before writing

Issue only when explicitly requested. `asaas_invoices_create` schedules the NFS-e and enforces these protections:

1. Exactly one origin: charge (`payment`), installment plan (`installment`), or customer (`customer`, standalone invoice). Resolve `pay_...` for a charge or `cus_...` for a customer before writing.
2. Automatic deduplication: a charge with an existing invoice is always rejected. The same customer + amount + date is rejected until the user confirms (`confirmedDistinct`). Rejection is not a failure; present the existing invoice.
3. Municipal service fields are omitted by default; the account supplies the municipal code, ISS, and tax name. Send only one of `municipalServiceId` or `municipalServiceCode` when the user explicitly chooses a specific service. If the provider rejects missing service details, present the actual reason, report the discrepancy, and never guess a code.
4. Explicit approval: issuance writes to production and displays an approval card in the conversation.
5. Accurate processing status: scheduling starts the flow, but municipal authorization is asynchronous. Say "invoice scheduled; issuance is being processed", not that authorization is immediate. Query by ID to confirm the later status.

Details: [references/invoices-create.md](references/invoices-create.md).

## Query municipal services

`asaas_services_list` reads the service catalog (`GET /v3/fiscalInfo/services`) with optional description filtering. Its result reinforces the rule that issuing an invoice must not create a service. Use it to inspect and discuss services, including duplicates; do not populate issuance fields on your own. National Portal accounts do not receive this list through the API. Official guidance is to obtain and validate the service code with the National Portal or the accountant before using it. Missing results do not authorize guessing. See [references/services-list.md](references/services-list.md).

Two distinctions matter:

- The municipal catalog is not the account's registered-service list. The endpoint returns hundreds of municipal items; `Notas Fiscais › Configurações › Serviços` displays only account registrations. Do not present one as the other.
- Observed `offset` behavior was a page number, not an item index: displacement was `offset × limit`. Adding `offset += limit` skips most entries and can end without error, with an empty list and `hasMore: false`. Increment by 1 and stop when `hasMore` is `false`. Investigate pagination before concluding that a service is missing.

## Requests to register a service

Treat an explicit request to register a new service as legitimate. However, the public ASAAS API offers only service listing, not creation, editing, or deletion.

1. Explain that registration is allowed but cannot be automated through this API.
2. Direct the user to `Notas Fiscais › Configurações › Serviços › Adicionar Serviço` in the ASAAS dashboard (municipal code, ISS, and description).
3. Help with available operations: list services to find possible duplicates and, after the user registers the service, use it for issuance.

Never invent a creation endpoint or claim to have created a service. Do not use invoice scheduling as a registration shortcut: it issues a real tax document, cannot reliably set ISS, and leaves entries removable only through the dashboard.

## Limits

- Responses exclude PDF/XML and verification codes. Use the ASAAS dashboard for the documents.
- Invoice updates and early issuance are unavailable here; direct the user to the dashboard.
- If `asaas_invoices_cancel` is available, it reads the invoice first, requires explicit approval, and reports the actual status. `PROCESSING_CANCELLATION` does not mean canceled; the municipality can reject it (`CANCELLATION_DENIED`). See [references/invoices-cancel.md](references/invoices-cancel.md). Without the tool, explain the limitation and direct the user to the dashboard.
- `taxes` follow account configuration; the tool does not send custom rates.

## Tools unavailable

If invoice tools are unavailable, the ASAAS plugin is disabled or the Genius version does not provide them yet. Ask the user to enable the plugin or update the application. Do not bypass it through a shell or script: the production key must not enter the prompt.
