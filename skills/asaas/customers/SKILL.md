---
name: asaas-customers
description: "Query, search, register, and update customers in the ASAAS production account using asaas_customers_list, asaas_customers_create, and asaas_customers_update in Sufficit AI Genius. Exposes name, email, person type, full CNPJ, or only the first three CPF digits. Queries are read-only; registration and updates require user confirmation. Registers the address the prefeitura requires on an NFS-e."
---

# ASAAS production customers

Use when the user asks to view, list, search, check, register, or update ASAAS customers.

## Credential

- The tool resolves `personal/asaas/production/api-key` in the user's Sufficit Identity Vault.
- Never request the key in the conversation or include it in arguments, commands, or files.
- For `asaas_key_missing`, prepare this exact entry with `vault_prepare_entry` and provide the secure screen for the user to paste and save the key. For `asaas_vault_sign_in_required`, ask the user to sign in to their Sufficit account.

## Query customers

Discover and use `asaas_customers_list`. It makes a fixed `GET` request to `/v3/customers`, with optional name, email, CPF/CNPJ filters and pagination. It is read-only: no customer is created, modified, or removed.

Trust the result only when it reports `provider: "asaas"`, `environment: "production"`, and `writesPerformed: false`. Follow [references/customers-list.md](references/customers-list.md) for failures.

Explain `personType` in plain language: FISICA = individual, JURIDICA = company. Under the identification policy, a company CNPJ is returned in full and formatted (for example, `27.506.088/7001-24`) as public registration data. A CPF is limited to its first three digits (for example, `390.***.***-**`); never infer or complete the remaining digits. For large accounts, paginate with `offset` while `hasNext` is true. Do not promise all results in one call; the limit is 100 per page. `addressComplete` and `addressMissing` say whether the address is enough to issue an NFS-e.

## Register a customer: query before writing

Register only when the user explicitly requests it, such as "register a new customer". The tool checks whether the customer exists before writing. Follow the same approach in the conversation:

1. Collect essential data: full name and, if available, CPF/CNPJ and email. When an invoice will be issued, also collect the street, number, neighborhood, and CEP: the prefeitura rejects an NFS-e for a customer without them. Never invent values.
2. Let `asaas_customers_create` check duplicates by document, email, and name.
   - An existing document always causes rejection and returns the existing candidate. Use that customer; do not insist.
   - A matching email or similar name returns candidates and requests confirmation. Retry with `confirmedDistinct: true` only after the user confirms that this is a different customer.
3. Wait for the approval card. Registration writes to the production account and requires explicit approval in the conversation. Do not promise automatic registration.
4. Report the actual result. Success includes the created customer with the identification policy applied (full CNPJ, first three CPF digits). After a timeout, check whether creation succeeded before retrying; the failure message provides guidance.

Arguments, refusals, and failure codes: [references/customers-create.md](references/customers-create.md).

## Update a customer

When the user asks to fix or complete a registration, or after a `customer_address_incomplete` refusal or a prefeitura rejection, use `asaas_customers_update` with the `cus_...` id from `asaas_customers_list`. It sends only the fields provided, requires the approval card, and never changes the name or CPF/CNPJ. See [references/customers-update.md](references/customers-update.md).

## Limits

- Results include ID, name, person type, email, document under the identification policy, and which address fields are missing. Phone, address values, invoices, and external references do not enter the model context. Direct the user to the ASAAS dashboard to read those values.
- Changing the name or CPF/CNPJ, clearing a field, and removing customers are unavailable here; explain the limitation and direct the user to the dashboard.

## Tool unavailable

Search the capability catalog before saying a tool is missing. If `asaas_customers_list`, `asaas_customers_create`, or `asaas_customers_update` is unavailable after that, the ASAAS plugin is disabled or this Genius version does not provide it yet. Ask the user to enable the plugin in Genius extensions or update the application. Do not bypass it through a shell, script, or another tool: the production key must not enter the prompt.
