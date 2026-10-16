# List of charges ASAAS

The `asaas_payments_list` tool consults `/v3/payments` in the production account by injecting the `personal/asaas/production/api-key` key only into the `access_token` header. The result only contains projected and sanitized fields: invoice URLs, personal documents, customer name and contacts do not enter the model context.

## Arguments

| Argument | Type | Default | Rules |
| --- | --- | --- | --- |
| `status` | string | (None) | Optional: `PENDING`, `RECEIVED`, `CONFIRMED`, `OVERDUE` or `REFUNDED`. Any other value is rejected before the call. |
| `limit` | integer | `10` | Between 1 and 30; higher values are reduced to 30. |
| `offset` | integer | `0` | Not negative, limited to 100,000; use to scroll pages. |

## Success result

| Field | Value |
| --- | --- |
| `provider` | `asaas` |
| `environment` | `production` |
| `query` | `{ status, limit, offset, returned }` — what was ordered and how many items came |
| `totalCount` | total charges matching the filter in ASAAS |
| `hasNext` | `true` when there is next page |
| `payments[]` | sanitized items |
| `writesPerformed` | `false` |
| `credentialReference` | `personal/asaas/production/api-key` |

Each item of `payments[]` brings when there are in the provider: `id`, `value`, `netValue`, `description` (truncated to 80 characters), `billingType`, `status`, `dueDate`, `paymentDate`, `installmentNumber`, `installmentCount`, `invoiceNumber` and `customer` (identifier only). Long texts are truncated with `…`; missing fields arrive as `null`.

## Situations

| Value | User Reading |
| --- | --- |
| `PENDING` | Waiting for payment. |
| `RECEIVED` | Received. |
| `CONFIRMED` | Received and confirmed. |
| `OVERDUE` | Overdue. |
| `REFUNDED` | Refunded. |

## Failure codes

| Code | Meaning | Action |
| --- | --- | --- |
| `asaas_payments_invalid_arguments` | Status out of list allowed, invalid `limit`/`offset`. | Correct arguments and repeat; nothing was called in the provider. |
| `asaas_payments_unexpected` | The body of ASAAS did not come in the expected format. | Inform the user and try again; if it persists, treat it as unavailable. |
| `asaas_vault_sign_in_required` | User not logged in to Sufficit Identity. | Ask to enter the Sufficit account and repeat. |
| `asaas_key_missing` | Missing or empty Vault entry. | Prepare `personal/asaas/production/api-key` with the safe screen and repeat after saving. |
| `asaas_key_invalid` | Invalid format key. | Ask for a new key in the ASAAS panel and save in the same input. |
| `asaas_credential_rejected` | The ASAAS rejected the key (401/403). | Ask for a valid key, save to Vault and try once. |
| `asaas_provider_unavailable` | ASAAS responded, but it didn't. | If marked retryable, retry after a brief wait. |
| `asaas_transport_failed` | Unreachable API. | Check the network and repeat. |
| `asaas_timeout` | Time limit exceeded. | Repeat once. |
| `asaas_vault_timeout` | Vault exceeded the time limit. | Repeat once. |
| `asaas_vault_unavailable` | Vault inaccessible. | Try again later. |

Retryable failures admit a new attempt after a brief wait; the others require user or provider action before insisting. Never use a writing operation to diagnose the query.

## Page in practice

Start without `offset`. If `hasNext` is `true` and the user wants more, ask for the next page with `offset` equal to the accumulated items already returned, until you exhaust `totalCount` or the user request. Don't promise "all" at once: the limit per page is 30.
