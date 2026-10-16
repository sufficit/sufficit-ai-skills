---
name: asaas-customers
description: "Query, search, and register customers in the ASAAS production account using asaas_customers_list and asaas_customers_create in Sufficit AI Genius. Exposes name, email, person type, full CNPJ, or only the first three CPF digits. Queries are read-only; registration requires user confirmation and checks duplicates before writing."
---

# ASAAS production customers

Use when the user asks to view, list, search, check, or register ASAAS customers.

## Credential

- The tool resolves `personal/asaas/production/api-key` in the user's Sufficit Identity Vault.
- Never request the key in the conversation or include it in arguments, commands, or files.
- For `asaas_key_missing`, prepare this exact entry with `vault_prepare_entry` and provide the secure screen for the user to paste and save the key. For `asaas_vault_sign_in_required`, ask the user to sign in to their Sufficit account.

## Query customers

Discover and use `asaas_customers_list`. It makes a fixed `GET` request to `/v3/customers`, with optional name, email, CPF/CNPJ filters and pagination. It is read-only: no customer is created, modified, or removed.

Trust the result only when it reports `provider: "asaas"`, `environment: "production"`, and `writesPerformed: false`. Follow [references/customers-list.md](references/customers-list.md) for failures.

Explain `personType` in plain language: FISICA = individual, JURIDICA = company. Under the identification policy, a company CNPJ is returned in full and formatted (for example, `27.506.088/7001-24`) as public registration data. A CPF is limited to its first three digits (for example, `390.***.***-**`); never infer or complete the remaining digits. For large accounts, paginate with `offset` while `hasNext` is true. Do not promise all results in one call; the limit is 30 per page.

## Register a customer: query before writing

Register only when the user explicitly requests it, such as "register a new customer". The tool checks whether the customer exists before writing. Follow the same approach in the conversation:

1. Collect essential data: full name and, if available, CPF/CNPJ and email. Do not request more or invent values.
2. Let `asaas_customers_create` check duplicates by document, email, and name.
   - An existing document always causes rejection and returns the existing candidate. Use that customer; do not insist.
   - A matching email or similar name returns candidates and requests confirmation. Retry with `confirmedDistinct: true` only after the user confirms that this is a different customer.
3. Wait for the approval card. Registration writes to the production account and requires explicit approval in the conversation. Do not promise automatic registration.
4. Report the actual result. Success includes the created customer with the identification policy applied (full CNPJ, first three CPF digits). After a timeout, check whether creation succeeded before retrying; the failure message provides guidance.

Arguments, refusals, and failure codes: [references/customers-create.md](references/customers-create.md).

## Limits

- Results include ID, name, person type, email, and document under the identification policy. Phone, address, invoices, and external references do not enter the model context. Direct the user to the ASAAS dashboard for those fields.
- Creation sends only name, CPF/CNPJ, and email. Address, phone, and other fields require the dashboard.
- Editing and removing customers are unavailable here; explain the limitation and direct the user to the dashboard.

## Tool unavailable

If `asaas_customers_list` or `asaas_customers_create` is unavailable, the ASAAS plugin is disabled or this Genius version does not provide it yet. Ask the user to enable the plugin in Genius extensions or update the application. Do not bypass it through a shell, script, or another tool: the production key must not enter the prompt.
