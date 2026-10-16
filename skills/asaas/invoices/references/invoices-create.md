# Issue (scheduled) of invoice ASAAS

The `asaas_invoices_create` tool schedules a new NFS-e in the production account via `POST /v3/invoices`. It requires explicit approval in the conversation and performs consult before writing in code: deduplicates per charge and per client+value+date before POST.

## Prerequisites (in this order)

1. The user explicitly asked for the invoice.
2. The origin is known: `payment` (charge), `installment` (installment plan) or `customer` (standalone invoice) — exactly one.
3. The municipal service is not sent by default — operating rule of this account (see "Service registered versus invoice description" in SKILL.md). Omit `municipalServiceId` and `municipalServiceCode`. Only send one of them when the user explicitly chooses another service for that invoice. If the provider refuses the invoice, present the actual reason to the user, report the divergence to the team and never guess code. Sending these fields changes the account service registration (creates entry or changes previous invoice association) — see "Side effect" below. The omission is what protects the record.

## Arguments

| Argument | Type | Mandatory | Rules |
| --- | --- | --- | --- |
| `customer` / `payment` / `installment` | string | exactly one | Ids ASAAS (`cus_...`, `pay_...`). |
| `value` | number | yes | Total amount in BRL; between 0.01 and 999,999,999.99. |
| `serviceDescription` | string | yes | Description printed on invoice; 1 to 200 characters. |
| `effectiveDate` | string | yes | Date of issue YYYY-MM-DD. |
| `municipalServiceId` | string | no | Catalog id; only when the user chooses a specific service. Never along with `municipalServiceCode`. Alone, it is rejected by the provider: also provide `municipalServiceName`. |
| `municipalServiceCode` | string | no | Code, only when the user explicitly reports one. Never along with `municipalServiceId`. Alone, it creates new entry into the register with the same name as the code. |
| `municipalServiceName` | string | no | Service name; up to 80 characters. It is the identity of the registration — use the exact `description` of `asaas_services_list`, never a hand-mounted name. |
| `observations` | string | no | Printed observations; up to 200 characters. |
| `confirmedDistinct` | boolean | no | `true` only after user confirms customer collision+value+date as distinct invoice. |

Service and taxes: The issue does not send `municipalServiceId`, `municipalServiceCode` or `taxes` — the service details are auto filled in by the service registration and by the tax configuration of the account when not specified (rule combined with the owner). The official documentation ([guide](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico) and [endpoint reference](https://docs.asaas.com/reference/agendar-nota-fiscal)] supports the omission: the schema does not list `municipalServiceId`/ `municipalServiceCode` as mandatory and declares the automatic fillings of `municipalServiceName` (uses the code) and `pisCofinsRetentionType` (calculated by Asaas); the guide narrative, for generic integrations, asks for id or code without describing the auto fill in by the account. Send the two service fields at the same time returns `asaas_invoices_create_invalid_arguments` without any POST, and no refusal fills in blind: present the provider's real motive and report to the team.

## Collateral effect of municipal fields (sandbox, 2026-09-23)

Schedule invoice is not neutral for account service registration. This reinforces the rule of omitting these fields; it is not permission to use them.

| Entry | Observed result |
| --- | --- |
| Only `municipalServiceCode` | Accepted. Creates a new entry with code-like name (e.g. `01.01.01`); `municipalServiceId` returns `null` even when the code exists in the catalog. |
| Only `municipalServiceId` | Refused — HTTP 400 `invalid_action`: "O campo municipalServiceName deve ser informado" (the municipalServiceName field is required), even with valid id. |
| `municipalServiceName` already existing + different code | Accepted, and the association changes retroactively: previous invoices with that name began to respond with the new code. |
| Nonexistent code (`99.99.99`) | Accepted, scheduled and authorized in the sandbox. API does not validate the code against the catalogue. |

Three practical consequences:

- The identity of the record is `municipalServiceName`, not the code. Different names have seen different records, even though the code matches.
- When the user chooses a service, prefer the `municipalServiceId` pair
  + `municipalServiceName` with the exact `description` of `asaas_services_list`. It's the only way that doesn't invent a name or create a divergent record.
- HTTP 200 does not prove tax acceptance. Sandbox authorized nonexistent code; in production who validates is the municipality, and the refusal appears later, in an asynchronous way.

Entries created by mistake can only be removed by the panel — and services with an authorized invoice are apparently not removable.

## Refusals (no write performed)

Result with `scheduled: false` and `writesPerformed: false` is refusal, not error. No POST happened.

| `reason` | Cause | Conduct |
| --- | --- | --- |
| `duplicate_payment` | The billing already has a tax bill. | Use the existing invoice returned. Never insist, not even with `confirmedDistinct`. |
| `possible_duplicate` | Same customer, value and date of existing invoice. | Present the existing invoice; only repeat with `confirmedDistinct: true` if the user confirms that it is another invoice. |

## Success result

| Field | Value |
| --- | --- |
| `scheduled` | `true` |
| `writesPerformed` | `true` |
| `emissionIsAsync` | `true` — Schedule starts the flow; authorization comes later |
| `invoice` | Sanitized invoice (`id`, `status` SCHEDULED, `value`, `effectiveDate`, linked ids; no URLs) |
| `dedupPerformed` | `true` |

Always report honestly: "scheduled invoice; the issue is in processing by the city." Authorization is confirmed by consulting the status later (AUTHORIZED).

## Failure codes

| Code | Action |
| --- | --- |
| `asaas_invoices_create_invalid_arguments` | Absent/duplicated origin, both service fields at the same time, invalid value/dates. Correct; nothing was called. |
| `asaas_invoices_create_rejected` | Provider refused (message brings code+description, e.g. invalid municipal service). Correct with the user. |
| `asaas_invoices_create_unexpected` | Scheduled but the answer came strange; refer to the list of invoices to confirm. |
| `asaas_timeout` | See if the invoice was created before repeating. |
| Other failures (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_provider_unavailable`, `asaas_transport_failed`) | Standard flow of ASAAS skills. |

## Recommended flow

```
user requests an invoice
        │
        ▼
resolve origin (payment/installment/customer)
(issuance does NOT specify a service; values come from account configuration)
        │
        ▼
asaas_invoices_create (origin, amount, description, date)
        │
        ├─ duplicate_payment ──► use the existing invoice
        ├─ possible_duplicate ──► confirm with the user
        │                             └─ confirmed? confirmedDistinct=true
        └─ approval card ──► scheduled:true ──► "scheduled; issuance is being processed"
```
