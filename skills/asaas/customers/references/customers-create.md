# Client Registration ASAAS

The `asaas_customers_create` tool registers a new customer in the production account. It requires explicit approval in the conversation (approval card) and executes the rule consult before writing in code: before POST it consults `/v3/customers` per document, email and name, and refuses to write when it finds duplicates. The `personal/asaas/production/api-key` key exits the direct Vault to the `access_token` header; the answer arrives sanitized with the document under the identification policy (CNPJ complete; CPF in the first 3 digits).

## When to use

Only when the user explicitly asked to register a new client. Do not offer the registration on your own initiative and never register as a side effect of another task.

## Arguments

| Argument | Type | Mandatory | Rules |
| --- | --- | --- | --- |
| `name` | string | yes | Client name; 1 to 80 characters. |
| `cpfCnpj` | string | no | CPF (11 digits) or CNPJ (14 digits); punctuation is ignored. |
| `email` | string | no | E-mail; up to 64 characters. |
| `confirmedDistinct` | boolean | no | `true` only when the user has confirmed that the name/e-mail collision is another client. Never overrides a document match. |

Sending to the provider takes only `name`, `cpfCnpj` (digits) and `email` — nothing more. Address, telephone and supplement are for the ASAAS panel.

## Refusals (no write performed)

The result with `created: false` and `writesPerformed: false` is a refusal, not an error. No POST happened.

| `reason` | Cause | Conduct |
| --- | --- | --- |
| `duplicate_document` | There is already a client with the informed CPF/CNPJ. | Use the existing client returned in `existingCustomer`. Do not repeat creation with `confirmedDistinct`. |
| `possible_duplicate` | E-mail collision or name without confirmation. | Introduce candidates (`dedupMatches`) and ask the user. Only repeat with `confirmedDistinct: true` if it confirms that it is another client. |

## Success result

| Field | Value |
| --- | --- |
| `created` | `true` |
| `writesPerformed` | `true` |
| `customer` | Client created sanitized (`id`, `name`, `personType`, `email`, `document` under the identification policy) |
| `dedupPerformed` | `true` — the duplicate query ran before writing |
| `credentialReference` | `personal/asaas/production/api-key` |

## Failure codes

| Code | Meaning | Action |
| --- | --- | --- |
| `asaas_customers_create_invalid_arguments` | Empty/long name, document out of 11/14 digits, long email. | Correct arguments and repeat; nothing has been called. |
| `asaas_customers_create_rejected` | ASAAS refused registration (e.g. invalid CPF). | The message brings code and description of the provider; correct with the user and try again. |
| `asaas_customers_create_unexpected` | Creation confirmed, but response in unexpected format. | See the client list to confirm the actual status. |
| `asaas_timeout` | Time limit exceeded. | See if the client has been created before repeating; writing may have happened. |
| `asaas_credential_rejected` | Key rejected (401/403). | Ask valid key and save in Vault. |
| `asaas_provider_unavailable` / `asaas_transport_failed` / `asaas_vault_*` | Shared failures of other ASAAS tools. | Follow the same conduct as the consultation. |

## Recommended flow

```
user requests registration
        │
        ▼
asaas_customers_create (name, cpfCnpj?, email?)
        │
        ├─ duplicate_document ──► use the existing customer
        ├─ possible_duplicate ──► ask the user
        │                              └─ confirmed? retry with confirmedDistinct=true
        └─ approval card ──► created:true ──► report with document (full CNPJ / first 3 CPF digits)
```

Never bypass a refusal by calling API another way; refusal is the tool protecting the production account from duplicates.
