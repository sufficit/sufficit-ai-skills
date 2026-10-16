# Client list ASAAS

The `asaas_customers_list` tool consults `/v3/customers` in the production account by injecting the `personal/asaas/production/api-key` key only into the `access_token` header. The result only contains projected and sanitized fields: telephones, addresses, observations and external references do not enter the model context. The document follows the identification policy: CNPJ arrives complete and formatted (e.g. public register `27.506.088/7001-24`); CPF arrives limited to the first 3 digits (e.g. `390.***.***-**`).

## Arguments

| Argument | Type | Default | Rules |
| --- | --- | --- | --- |
| `name` | string | (None) | Optional; matches customers whose name contains the text. Up to 80 characters; empty is ignored. |
| `limit` | integer | `10` | Between 1 and 30; higher values are reduced to 30. |
| `offset` | integer | `0` | Not negative, limited to 100,000; use to scroll pages. |

## Success result

| Field | Value |
| --- | --- |
| `provider` | `asaas` |
| `environment` | `production` |
| `query` | `{ name, limit, offset, returned }` — what was ordered and how many items came |
| `totalCount` | Total customers matching the filter in ASAAS |
| `hasNext` | `true` when there is next page |
| `customers[]` | sanitized items |
| `writesPerformed` | `false` |
| `credentialReference` | `personal/asaas/production/api-key` |

Each item of `customers[]` brings, when it exists in the provider: `id`, `name` (truncated to 80 characters), `personType`, `email` and `document` (CNPJ complete and formatted; CPF in the first 3 digits; other formats arrive as `***`). Absent fields arrive as `null`.

## Types of person

| Value | User Reading |
| --- | --- |
| `FISICA` | Individual. |
| `JURIDICA` | Company (legal person). |

## Failure codes

| Code | Meaning | Action |
| --- | --- | --- |
| `asaas_customers_invalid_arguments` | `name` above 80 characters, invalid `limit`/`offset`. | Correct arguments and repeat; nothing was called in the provider. |
| `asaas_customers_unexpected` | The body of ASAAS did not come in the expected format. | Inform the user and try again; if it persists, treat it as unavailable. |
| `asaas_vault_sign_in_required` | User not logged in to Sufficit Identity. | Ask to enter the Sufficit account and repeat. |
| `asaas_key_missing` | Missing or empty Vault entry. | Prepare `personal/asaas/production/api-key` with the safe screen and repeat after saving. |
| `asaas_key_invalid` | Invalid format key. | Ask for a new key in the ASAAS panel and save in the same input. |
| `asaas_credential_rejected` | The ASAAS rejected the key (401/403). | Ask for a valid key, save to Vault and try once. |
| `asaas_provider_unavailable` | ASAAS responded but did not complete the query. | If marked retryable, retry after a brief wait. |
| `asaas_transport_failed` | Unreachable API. | Check the network and repeat. |
| `asaas_timeout` | Time limit exceeded. | Repeat once. |
| `asaas_vault_timeout` | Vault exceeded the time limit. | Repeat once. |
| `asaas_vault_unavailable` | Vault inaccessible. | Try again later. |

Retryable failures admit a new attempt after a brief wait; the others require user or provider action before insisting. Never use a writing operation to diagnose the query.

## Search by name in practice

If the user gives a name, pass on `name` without changing; the match is by containment in the provider. Without a name filter, list the first page and offer to proceed with `offset` as long as `hasNext` is true until you exhaust `totalCount` or the user request. The document is for the user to confirm which client it is — in the case of CPF, never try to deduce the full number from the first 3 digits.
