# Fiscal API reference (Sufficit endpoints)

Base URL `https://endpoints.sufficit.com.br` (every route also exists under `/v2`). JSON keys are
lowercase as shown. Managers and administrators only, with finance access to the customer.

## Catalog

`GET Finance/Fiscal/Services`

```json
[{ "key": "technical-support", "title": "Suporte técnico em informática", "code": "01.07.01",
   "name": "Suporte técnico em informática, inclusive …", "nbs": "1.1501.30.00", "operationindicator": "100301" }]
```

## Consolidation (received payments by invoice type)

`GET Finance/Fiscal/Receipts?contextId=<guid>&days=90`

- `taker`: Asaas customer (`customer`, `name`, `address`, `complete`, `synchronized`, `crm`).
- `blocker`: pt-BR reason that prevents issuing, when any.
- `groups[]`: `servicekey` (empty = not classified), `title`, `code`, `pending`, `pendingvalue`,
  `processing`, `issued`, `issuedvalue`.
- `lines[]`: one invoice to issue per receipt and invoice type.
  - `reference`: idempotency key to send when issuing.
  - `source`: `LEDGER` (financial record) or `ASAAS` (payment received at Asaas).
  - `timestamp`, `method`, `description`, `receiptvalue`, `value` (this line).
  - `servicekey`, `suggested` (service inferred by value), `services[]` (`contractid`, `title`,
    `category`, `value`), `payment` (`pay_…`).
  - `status`: `pending`, `processing`, `issued`, `failed`; `invoice` with `providerid`, `status`,
    `statusdescription` (provider reason), `number`, `pdf`.

Receipts come from the customer's ledger credits (checkout and bank slip items link the contracts) and
from payments received at Asaas without a ledger record; a provider payment is merged into an
unlinked ledger credit of the same amount within 3 days. The invoice type is the catalog category of
the paid contract (Suporte → technical-support; Telefonia, Atendimento, Hospedagem, Cloud Mobile →
licensing).

## Issue

`POST Finance/Fiscal/Issue`

```json
{ "contextid": "<guid>", "servicekey": "technical-support",
  "description": "Suporte e assessoria do Chatwoot, n8n e API do WhatsApp",
  "value": 750.00, "payment": "pay_…", "reference": "<line.reference>" }
```

Optional: `observations` (default "Referente ao pagamento de R$ … recebido." when bound to a payment),
`effectivedate` (default today in Brazil). Answer:

```json
{ "id": "<guid of the future imported document>", "provider": "ASAAS", "providerid": "inv_…",
  "status": "SCHEDULED", "value": 750.00, "payment": "pay_…", "servicecode": "01.07.01", "duplicate": false }
```

Errors: 400 invalid input (unknown `servicekey`, value, description); 422 business refusal with a pt-BR
`detail` (taker, payment of another customer, payment not received, value above the payment); 502 Asaas
refusal with the provider reason in `detail` and `code`.

## Follow-up

- `GET Finance/Fiscal/Invoices?contextId=<guid>`: latest invoices of the customer at Asaas.
- `GET Finance/Fiscal/Invoices/{providerId}?contextId=<guid>`: one invoice (404 when it belongs to
  another customer).
- `GET Finance/Fiscal/Takers/{contextId}` and `POST Finance/Fiscal/Takers/{contextId}/Sync`: taker at
  Asaas; sync copies the CRM address, and the CRM e-mail when Asaas has none.

## Decision queue

`GET Finance/Fiscal/Pending?days=30` (global finance access): `groups`, `customers` (per customer counts,
`dismissed`) and `lines` (each with `contextid` and `customer`; pending and failed first, oldest first, then
dismissed). Payments received only at Asaas are included (placed by imported invoices or by CPF/CNPJ).

`POST Finance/Fiscal/Dismiss` with `{ "contextid": "<guid>", "reference": "<line.reference>", "reason": "…" }`:
decides not to issue (answer `reason`, `userid`, `timestamp`). `DELETE Finance/Fiscal/Dismiss?contextId=&reference=`
puts it back (404 when it was not dismissed). A dismissed line issued later keeps the invoice status.

## Cancel

`POST Finance/Fiscal/Invoices/{providerId}/Cancel?contextId=<guid>`

```json
{ "reason": "Valor emitido errado; nova nota será emitida." }
```

Allowed for `SCHEDULED`, `SYNCHRONIZED`, `AUTHORIZED` and `CANCELLATION_DENIED`. Answer: the invoice
(`providerid`, `status` `CANCELED` or `PROCESSING_CANCELLATION`, …). Errors: 400 reason missing or
outside 5..500 characters; 422 with a pt-BR `detail` (invoice of another customer, already cancelled,
cancellation in progress, failed invoice); 502 Asaas refusal. The reason is kept in Sufficit's activity
log (Asaas has no reason field). The final state arrives by webhook.

## Import and synchronization (automatic)

Asaas webhooks (all NFS-e events) import authorized invoices with XML/PDF into the customer's
documents (Financeiro → Notas fiscais) and apply cancellations; a 15-minute reconciliation repairs
missed events. Administrators only:

- `GET Gateway/Asaas/Invoices/History?invoiceId=inv_…&limit=5`: processing history (`result`,
  `outcome`, e.g. `invoice_created`, `finance_entity_not_found`, `finance_entity_ambiguous`).
- `POST Gateway/Asaas/Invoices/Reprocess` with `["inv_…"]` (up to 50): requeue after fixing the CRM.
