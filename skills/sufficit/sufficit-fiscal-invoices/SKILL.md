---
name: sufficit-fiscal-invoices
description: "Issue and consult service invoices (NFS-e) for Sufficit customers through the Sufficit API, without opening the Asaas panel: list a customer's received payments split by invoice type, see which invoices are pending, processing, issued or failed (with the provider reason), issue an invoice bound to the received payment, check the taker registration (address and e-mail copied from the CRM) and reprocess invoices after fixing the CRM. Use for emitir nota fiscal, NFS-e de cliente, notas a emitir, consolidacao fiscal, consultar nota, nota falhou, nota nao importou. Internal managers only."
metadata:
  version: "1.0.0"
  author: "Sufficit"
---

# Sufficit fiscal invoices (NFS-e)

Sufficit issues service invoices through its own API (`Finance/Fiscal`), which talks to
Asaas with the company credential. Managers never need the Asaas panel or a personal
Asaas key for a Sufficit customer: use this skill. The screen for the same work is
**Financeiro → Consolidação fiscal** (`https://blazor.sufficit.com.br/pages/finance/fiscal?contextid=<id>`).

The `asaas-invoices` skill is for an account owner's own Asaas account; do not use it for
Sufficit customers.

## Access

Use the connected API tools: discover with `sufficit_api_search` (search in English:
`fiscal receipts`, `fiscal issue`, `fiscal taker`) and call with `sufficit_api_call`. Base URL
`https://endpoints.sufficit.com.br`. Exact routes, bodies and answers are in the
[API reference](references/api.md).

Only internal managers and administrators can use these routes, and only for customers
they may access (finance entitlement on the `contextId`). Reprocessing is administrator
only. Do not grant roles or entitlements to make a call pass; report the gap.

## Rules

- **Issuing is a real tax document in production.** Before `POST Finance/Fiscal/Issue`,
  show the customer, the invoice type, the printed description, the value and the bound
  payment, and wait for an explicit confirmation ("pode emitir"). Querying needs none.
- **Invoice type comes only from the catalog** (`GET Finance/Fiscal/Services`): use its
  `servicekey`. Never send a municipal code, NBS or tax rate by hand and never invent a
  new service: at Asaas a new service name registers a new service. The catalog holds the
  official codes (today `licensing` 01.03.01 and `technical-support` 01.07.01 / NBS
  1.1501.30.00).
- **Use the consolidation line** from `GET Finance/Fiscal/Receipts`: send its `reference`,
  `payment` and `value`. The reference makes issuing idempotent: repeating it returns the
  existing invoice with `duplicate=true` instead of issuing another.
- **The CRM is the source of truth** for the taker's document, address and e-mail. If
  something is missing, fix the customer's contact in the CRM; issuing copies address and
  e-mail to Asaas when they are missing there. Never edit the customer only at Asaas.
- **Authorization is asynchronous.** A new invoice is `SCHEDULED`; the municipality
  authorizes it later and the Asaas webhook imports the XML/PDF automatically. Say
  "nota agendada; a autorização chega em seguida", never "emitida" before `AUTHORIZED`.
- Cancelling an invoice is not available in this API: tell the user it must be done in
  the Asaas panel and that the import follows automatically.

## Workflow: which invoices are pending

1. Resolve the customer (`contextId`) and confirm homonyms.
2. `GET Finance/Fiscal/Receipts?contextId=<id>&days=90` (30, 90, 180 or 365).
3. Report per group (`groups`): pending count and value, processing, issued. For pending
   lines give date, method, services, value and whether the service link is a
   `suggested` one (inferred by value; confirm with the user).
4. If `blocker` is present, explain it before anything else (see Troubleshooting).

## Workflow: issue an invoice

1. Take the pending (or `failed`) line from the receipts.
2. Unclassified line (`servicekey` empty): ask which type applies; never guess.
3. Propose the description: the paid services' titles, or what the user dictates.
4. Confirm with the user, then `POST Finance/Fiscal/Issue` with `contextid`, `servicekey`,
   `description`, `value`, `payment` and `reference` from the line.
5. Report `providerid` (`inv_...`) and the status. To follow up, read the line again in
   `Receipts` or `GET Finance/Fiscal/Invoices/{providerid}?contextId=<id>`.

## Troubleshooting

| Situation | Meaning and action |
| --- | --- |
| `blocker`: "Cliente sem CPF/CNPJ válido no cadastro." | Fill the document in the CRM contact. |
| `blocker`: "Cliente não cadastrado no Asaas." | The customer has no Asaas registration; it is not created automatically. Escalate. |
| `blocker`: "Há mais de um cadastro deste CPF/CNPJ no Asaas." | Duplicate at Asaas; unify there (escalate). |
| Address or e-mail incomplete | Complete the CRM contact (address with street, number, district, CEP; e-mail). Then `POST Finance/Fiscal/Takers/{contextId}/Sync` or simply issue. |
| HTTP 502 "O Asaas recusou a operação" | `detail` carries the Asaas reason after the colon (e.g. "E-mail do cliente incompleto."). Fix the cause and retry with the same reference. |
| Line `failed` | The municipality rejected it; the reason is in `invoice.statusdescription`. Fix and issue again (same reference). |
| Service with pending fields at Asaas | A new service type needs its "Código de tributação nacional" (e.g. 010701) set once in the Asaas panel by a manager: Notas Fiscais → Configurações → Serviços. The API cannot edit services. |
| Authorized at Asaas but missing in Sufficit | The import found no customer or two customers with the same CPF/CNPJ (`finance_entity_not_found` / `finance_entity_ambiguous` in `GET Gateway/Asaas/Invoices/History?invoiceId=`). Fix the CRM (unify, or mark the billing contact as important for finance), then an administrator runs `POST Gateway/Asaas/Invoices/Reprocess`. A 15-minute reconciliation also retries daily. |

## Output

Answer in plain Portuguese for a manager: customer, what is pending (count and value per
type), what was done, the invoice id and status, and the next step. Never show tokens,
full CPF numbers or raw payloads.
