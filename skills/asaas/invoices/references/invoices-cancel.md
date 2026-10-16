# Cancellation of the invoice ASAAS

The `asaas_invoices_cancel` tool requests cancellation of a NFS-e in the production account via `POST /v3/invoices/{id}/cancel` ([official reference](https://docs.asaas.com/reference/cancelar-uma-nota-fiscal)). It just cancels: never issues and never changes invoice data.

## Prerequisites (in this order)

1. The user explicitly asked to cancel (cancel, cancel, undo).
2. The target is an id `inv_...` obtained from `asaas_invoices_list` — never a number read on invoice paper, never a guess.
3. The tool consults the invoice before writing: refuses when there is nothing to cancel, and the approval card shows what will be cancelled.
4. Explicit approval in conversation: cancellation is irreversible.

## Arguments

| Argument | Type | Mandatory | Rules |
| --- | --- | --- | --- |
| `invoice` | string | yes | Invoice Id ASAAS (`inv_...`), according to `asaas_invoices_list`. |

## Refusals (no write performed)

`canceled: false` with `writesPerformed: false` is refusal, not error. No POST happened.

| `reason` | Cause | Conduct |
| --- | --- | --- |
| `already_canceled` | The bill's already canceled. | Inform the user; nothing to do. |
| `cancellation_in_progress` | Cancellation is already in processing. | Wait for the result; do not repeat. |
| `cancellation_denied` | The city has already denied this cancellation. | Explain it's up to the city. |
| `not_cancellable` | Status does not allow to cancel (e.g. `ERROR`). | Inform the user of the actual status. |

## Success result

| Field | Value |
| --- | --- |
| `cancellationRequested` | `true` — the request has been accepted by ASAAS. |
| `canceled` | `true` only if the status returned is `CANCELED`. |
| `cancellationIsFinal` | `true` only with `CANCELED`. |
| `cancellationIsAsync` | `true` when it's not final yet. |
| `previousStatus` | Invoice status before request. |
| `invoice` | Sanitized invoice projection (without URLs/check code). |

Compulsory honesty: `PROCESSING_CANCELLATION` means "accepted request, municipality processing" — don't say the invoice has been cancelled. The city may deny (`CANCELLATION_DENIED`) and not every municipality allows automatic cancellation by integration (option `supportsCancellation` in municipal settings). Official flow events: `INVOICE_PROCESSING_CANCELLATION`, `INVOICE_CANCELED`, `INVOICE_CANCELLATION_DENIED`. To confirm later, see the invoice and report the actual status.

## Failure codes

| Code | Action |
| --- | --- |
| `asaas_invoices_cancel_invalid_arguments` | Absent/invalid id; nothing was called. |
| `asaas_invoices_cancel_not_found` | Id does not exist: list the invoices (`asaas_invoices_list`) and use the returned id. |
| `asaas_invoices_cancel_rejected` | Provider refused (message brings code+description). |
| `asaas_invoices_cancel_unexpected` | Strange response: refer to the invoice before repeating. |
| `asaas_timeout` | See the invoice before repeating. |
| Other failures (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_provider_unavailable`, `asaas_transport_failed`) | Standard flow of ASAAS skills. |
