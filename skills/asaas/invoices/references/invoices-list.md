# List of invoices ASAAS

The `asaas_invoices_list` tool consults `/v3/invoices` in the production account by injecting the `personal/asaas/production/api-key` key only into the `access_token` header. It is read-only (`writesPerformed: false`). The projection never includes `pdfUrl`, `xmlUrl` or `validationCode` — for the issued document, direct the ASAAS panel.

## Arguments

| Argument | Type | Default | Rules |
| --- | --- | --- | --- |
| `customer` | string | (None) | Filter by client id (`cus_...`); up to 64 characters. |
| `payment` | string | (None) | Filter by the collection id (`pay_...`). |
| `status` | string | (None) | One between SCHEDULED, SYNCHRONIZED, AUTHORIZED, PROCESSING_CANCELLATION, CANCELED, CANCELLATION_DENIED, ERROR. |
| `effectiveDateGe` | string | (None) | Start of the period of issue (YYYY-MM-DD). |
| `effectiveDateLe` | string | (None) | End of period of issue (YYYY-MM-DD). |
| `limit` | integer | `10` | Between 1 and 30. |
| `offset` | integer | `0` | Not negative. |

## Success result

`provider: "asaas"`, `environment: "production"`, `query` (the request and `returned`), `totalCount`, `hasNext`, `invoices[]`, `writesPerformed: false`.

Each invoice brings: `id`, `status`, `statusDescription`, `type`, `number`, `serviceDescription` (up to 200 characters), `value`, `deductions`, `effectiveDate`, `observations`, `customer`, `payment`, `installment`.

The `customer` field brings the client solved by the tool (an extra customer id reading, no more than 30 per page): an object with `id`, `name`, `personType` and `document` — CNPJ complete and formatted (public record), CPF limited to the first 3 digits. When resolution is not possible (client removed, read failure), the invoice brings the provider's loose id and id appears in `unresolvedCustomerIds`, accompanied by `guidance` pointing to `asaas_customers_list`. Never state to whom the invoice was issued from an unsolved id.

## Status reading for user

| Status | Simple language |
| --- | --- |
| `SCHEDULED` | Scheduled — will be issued on the scheduled date. |
| `SYNCHRONIZED` | Sent to City Hall, awaiting permission. |
| `AUTHORIZED` | Issued (allowed). |
| `PROCESSING_CANCELLATION` | Cancellation in processing. |
| `CANCELED` | Canceled. |
| `CANCELLATION_DENIED` | Cancellation denied by the city. |
| `ERROR` | Issuance failed. |

## Failure codes

| Code | Action |
| --- | --- |
| `asaas_invoices_invalid_arguments` | Fix filters (status allowed, dates YYYY-MM-DD); nothing has been called. |
| `asaas_invoices_unexpected` | Response out of format; inform the user and try once. |
| `asaas_vault_sign_in_required` / `asaas_key_missing` / `asaas_key_invalid` / `asaas_credential_rejected` | Standard credential flow of ASAAS skills. |
| `asaas_provider_unavailable` / `asaas_transport_failed` / `asaas_timeout` / `asaas_vault_*` | Repeat as marked retryable. |

## Use to talk about account services

Without filters, the first page shows recent account invoices; the repeated `serviceDescription` shows what the account usually issues. Combine with `asaas_services_list` to check the registration — and remember that the description printed on the invoice is not the municipal framework: in this account the issue does not send the municipal fields (see SKILL.md, "Service registered versus invoice description").
