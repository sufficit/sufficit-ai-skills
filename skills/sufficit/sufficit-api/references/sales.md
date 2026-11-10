# Sales representatives

For “lançar saldo”, tariffed credit purchases, monthly commitments and their service
history, read [the telephony credit workflow](telephony-credit.md). A credit purchase,
a commitment and an automatic purchase schedule are distinct operations.

Representatives are contacts identified by GUID. Discover the routes in the live OpenAPI by `representative customers`, `representative list` or `representatives` before calling.

## Customer portfolio

`GET /Sales/Representative/Customers?representativeId=...` returns the representative's own row first and then every customer with a service commissioned to it, with `title`, `balance`, `commitment`, `activeServices` and `entries` (inbound numbers). The portfolio also keeps former customers whose commissioned services ended; they come with `activeServices = 0`.

Always narrow the request instead of reading the whole list:

- `onlyActive=true`: only customers with at least one service active now;
- `filter`: customer title fragment or exact customer GUID;
- `skip` and `take`: pages ordered by title;
- `includeRepresentative=false`: omits the representative's own row.

The `X-Total-Count` response header carries the filtered total before paging. To count the active portfolio, call with `onlyActive=true&includeRepresentative=false&take=1` and read the header; to list it, page with `take` of up to 100 and keep going while rows remain. Never sum `activeServices` from a truncated answer.

The representative itself may read its own portfolio; managers and administrators may read any.

## Which count to use

- Active portfolio: `Representative/Customers` with `onlyActive=true` (header `X-Total-Count`). This is the official count of a representative's active customers.
- `GET /Sales/Representative/List` (management only) counts every customer ever commissioned, including former ones.
- `GET /Sales/Representatives/ById` shows `customers` and `commissionedCustomers` from the commission program registry. A representative whose portfolio was not yet registered there shows `0`; this is not the size of its customer base.

## Customer contact data

For the display name of a known customer/context GUID, follow [the contact-title lookup](contacts.md#resolve-a-customers-name-from-a-known-context-guid). An empty commercial customer record does not prove the contact is absent or legacy.

The portfolio returns aggregates only, never the customers' e-mail or phone. A representative's permission does not extend to its customers' records. Do not try to obtain them by passing a customer GUID as `contextId` or `contactId` to `POST /Contact/Search`; the server refuses it (`403`) and it is outside the authorised scope. When a campaign needs contact data, report that it requires an export authorised by Sufficit management.

## Customer preferred due day

For "dia preferencial" or a customer-wide payment-day change, follow [the customer due-day flow](customer-due-day.md) before editing contract dates. It identifies the dedicated customer preference writer, concurrency expectation, independent verification and the separate contract alignment guard.

## Initial zero-price period requested by a manager

For a new service, interpret “leave the value at0 initially” as free initial
coverage only until the customer's next preferred due date, followed by the
agreed normal price from that date onward. The free coverage ends the day before
the boundary. This is the default unless the manager explicitly specifies a
different arrangement; do not ask them to reconfirm this meaning. It does not
mean a permanently zero-priced service or a full free month from activation.

Read the saved preference and agreed recurring price. Ask only for a material
missing value, not for confirmation of the default. For example, activation on
9November with preferred day21 and monthly price30 means0 for9–20November and30
for cycles starting21November. For days29–31 absent in a month, use the last
valid day while preserving the original preferred day for later months.

Apply the initial waiver only to the first service period using an operation
supported by the live API, and keep the following periods at the agreed price.
Verify both periods and the next renewal. Do not create a separate financial
bonus, permanently set the recurring price to0, or post a future debit now. If
no deployed operation supports a period-scoped waiver, report that specific
limitation rather than inventing a route or broadening the discount.

## Monthly services: which system owns each service

Customers are moving from the legacy service manager to native contracts. Before acting, read the customer's contracts (`GET /Sales/Contract/Search`): `source` tells which system owns each one.

- **Native** contracts with automation on renew by themselves: the recurring automation opens each monthly period and debits it to the customer's balance. Nobody renews them by hand; a negative balance is how a debtor shows up. Do not try the legacy renewal below on them.
- **Legacy** contracts (`source` LegacySales) are still renewed by hand, one service at a time, until migrated. A renewal value such as `NotConfigured` describes the native automation, not whether the legacy renewal is allowed.
- A customer may have both sources. Handle each requested service separately. Neither an expired date nor an Active status selects the renewal engine. Native contracts with automation off require investigation of their native setup; do not send them through the legacy writer.

A request to renew does not authorize migration, enabling automation, marking payment or renewing other services. If two inbound services match a request for all inbound services, handle those two and report each result; leave unrelated service types untouched.

## Migrating a legacy service to the new system

One contract at a time, never in bulk. Migration is irreversible, so only do it when the user asked to migrate that customer's service, and confirm the contract and service type before calling.

1. Read the contract: `GET /Sales/Contract?id=<contractId>`. It must be `source` LegacySales, status Active and `automationEnabled` false; keep its `updatedAtUtc`.
2. Choose the native service type: `GET /Sales/ServiceCatalog`, never a retired item. If the contract already has a `catalogItemId`, use that one. When the right type is unclear, ask.
3. Migrate: `POST /Sales/Contract/{contractId}/AdoptNative` with `{"operationId": "<new GUID>", "catalogItemId": "...", "expectedUpdatedAtUtc": "<updatedAtUtc>", "reason": "<why>"}`. Reuse the same `operationId` to retry after an ambiguous failure. `409` means the contract changed or is not eligible: read it again.
4. Turn automation on so the next periods open by themselves: read `GET /Sales/Contract/Automation?id=<contractId>`, then `POST /Sales/Contract/Automation` with `{"contractId": "...", "enabled": true, "expectedEnabled": false}`.
5. Confirm by reading the contract again (`source` Native, automation on).

The current period stays as already charged; the new system charges the following ones. Managers holding `serviceupdate` for the customer may migrate; the same action is the "Migrar para o sistema novo" panel on the service page (`/pages/sales/services/item`).

## The manager's monthly routine (new system)

- Collections to follow up: `GET /Sales/ServiceCollections` (reference month, optional customer or responsible). Read-only.
- Record that the customer was contacted about a month: `POST /Sales/ServiceCollections/PeriodContact`; earlier contacts: `GET .../PeriodHistory` (a contact log, not a list of charges; empty is normal).
- Notices to send: `GET /Sales/ServiceCollections/Notices`, then `POST .../Notices/Sent` once the notice really went out, or `POST .../Notices/Cancel` with the reason. Genius never marks a notice as sent without confirmation that it was delivered.
- Payment links: per contract `GET|POST /Sales/ContractCheckout/Link`; consolidated `GET /Sales/BillingCheckout/Overview` and `POST /Sales/BillingCheckout/Link`.
- Prepaid plan changes: `POST /Sales/ServiceCollections/PlanPreview` (quote), then `PlanCommand`, then poll `PlanOperation`. Prepaid services only.
- Customer commercial status: `GET /Sales/Customers/{contextId}/Status`, change with `POST .../Status/Change` when the user confirms.
- Representative commission: released automatically after payment; `POST /Sales/Representatives/Release?customerId=` only anticipates it. It never charges or renews.

The same tasks exist in the Sufficit panel for users who prefer the screen: Gestão de serviços (`/pages/sales/services`), Cobranças dos serviços (`/pages/sales/services/collections`), Avisos de cobrança (`/pages/sales/services/collections/notices`) and Situação comercial do cliente (`/pages/sales/customer-status`).

## Renewing a legacy monthly service

Renewing creates the next monthly period and its charge, so only do it when the user explicitly asked to renew that customer and month.

These endpoints do not renew anything — do not use them for this:

- `ServiceCollections`, `PlanPreview`, `PlanCommand`: prepaid plan changes only. On a legacy service `PlanPreview` answers `409 plan_selection_conflict` because the service has no prepaid binding.
- `ServiceCollections/PeriodHistory` and `PeriodContact`: contact log.
- `Representatives/Release`: commission for periods already paid.
- `Customers/{contextId}/Status/Change`: commercial classification only.
The `Contract/RenewMonthly` and `RenewBilled` routes are a separate writer handoff for eligible legacy contracts. Their availability applies only to that route. `canRenew=false`, even with “A renovação deste serviço ainda não está habilitada no sistema novo”, does not establish that the legacy service is blocked. Use the legacy editor flow below when the contract is still LegacySales; do not try both handoff routes repeatedly or ask to migrate just to renew.

Renewal flow:

1. List the customer's services: `GET /Sales/Record/Search?contextId=<customer>&renewed=false`. Each row's `id` is the service id; check `description`, `value` and `end` against the request.
2. Read the authority: `GET /Sales/LegacyService/Session` returns `epoch`, `snapshotId` and `cutoverId`.
3. Open the service: `GET /Sales/LegacyService?id=<service id>` (the service id, never the customer id), passing in the call's `headers` argument `X-Sufficit-Sales-Epoch: <epoch>` and `X-Sufficit-Sales-Snapshot: <snapshotId>`. It returns `contractId`, `revision` and `service`. No `contractId` means the service is historical and cannot be renewed.
4. Renew: `POST /Sales/LegacyService` with the same headers and body `{"operationId": "<new GUID>", "cutoverId": "<cutoverId>", "action": "renew", "serviceId": "<service id>", "contractId": "<contractId>", "expectedRevision": <revision>}` (no `desired`). Keep the same `operationId` if you must retry after an ambiguous failure; the server replays the receipt.
5. Confirm with an independent read (step 1 or 3) that a new period exists, and report the services, values and new end date.

`409 "Commercial authority changed; reload before submitting."` means the request did not match the server's current authority; it is not proof of missing renewal capability or permission. Read Session again and supply BOTH headers in the tool's `headers` object (not in the JSON body or query), then reopen the service. On a changed cutover, reconstruct the command from that fresh editor state rather than patching an old command blindly. After an ambiguous write, inspect the state and preserve its operation ID/payload when replaying a receipt; never create a fresh renewal to compensate for an unknown outcome.

`"Service revision changed; reload before submitting."` requires reopening the service and checking whether the requested period already exists before writing again. If a fresh Session and correctly supplied headers still fail, stop and report the exact call and response; do not loop or waive the authority checks.

Current `sufficit_api_call` accepts `headers`. Inspect the available tool schema before claiming that it cannot send them. If an older installed client lacks this argument, report that specific limitation and point the operator to the Renovar button on the Sufficit service page; do not claim that the customer needs migration or that renewal itself is disabled.

### "customer_not_active" in ServiceCollections

`ServiceCollections` flags a legacy service `customer_not_active` when the customer's commercial status is not `Active`, including when it was never classified. The representative portfolio counts a customer as active by service dates instead, so both answers can disagree for the same customer. This flag does not block renewal; to fix it, read the status and, when the user confirms the customer is active, change it with `POST /Sales/Customers/{contextId}/Status/Change`.

### Representative's whole portfolio

There is no single call. List the active customers (`Representative/Customers` with `onlyActive=true&includeRepresentative=false`, paged), split native and legacy contracts, then renew only the legacy services per customer. Before renewing, show the user the list of customers, services and values to be renewed and get confirmation; then report each result, including failures.
