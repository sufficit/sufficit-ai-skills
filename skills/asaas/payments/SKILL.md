---
name: asaas-payments
description: "List and query charges in the ASAAS production account, including payments, invoices, overdue and received amounts, using asaas_payments_list in Sufficit AI Genius. Use when the user asks to view, check, or calculate totals for ASAAS charges. Read-only; does not create or modify anything."
---

# ASAAS production charges

Use this guidance when the user asks to view, check, list, or total ASAAS charges, payments, invoices, or overdue amounts.

## Credential

- The tool resolves the key at `personal/asaas/production/api-key` in the user's Sufficit Identity Vault.
- Never ask for the key in the conversation or include it in arguments, commands, or files.
- For `asaas_key_missing`, prepare exactly this entry with `vault_prepare_entry` and provide the secure screen for the user to paste and save the key. For `asaas_vault_sign_in_required`, ask the user to sign in to their Sufficit account.

## Query charges

Discover and use `asaas_payments_list`. It makes a fixed `GET` request to `/v3/payments` with optional status filtering and pagination. It is read-only: it does not create, modify, or refund charges.

Trust the result only when it reports `provider: "asaas"`, `environment: "production"`, and `writesPerformed: false`. On failure, follow [references/payments-list.md](references/payments-list.md).

Explain statuses in plain language: PENDING = awaiting payment, RECEIVED = received, CONFIRMED = received and confirmed, OVERDUE = overdue, REFUNDED = refunded. Calculate totals and counts from returned values; never invent numbers. If the user requests "all", paginate with `offset` while `hasNext` is true. Do not bypass the limit of 30 items per page.

## Limits

- Results include the customer identifier (`customer`), but not the name, CPF/CNPJ, email, or phone number; these fields do not enter the model context. If the user asks who paid, explain that customer identification is not yet available in this integration.
- This tool cannot create, edit, or refund charges. Explain this limitation and direct the user to the ASAAS dashboard when needed.

## Tool unavailable

If `asaas_payments_list` is unavailable, the ASAAS plugin is disabled or this version of Genius does not provide it yet. Ask the user to enable the plugin in Genius extensions or update the application. Do not bypass it through a shell, script, or another tool: the production key must not enter the prompt.
