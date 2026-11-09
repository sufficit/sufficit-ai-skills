# Customer preferred payment day

Use this flow for "dia preferencial", "dia de vencimento do cliente" or changing
the customer's preferred day each month. Discover the live OpenAPI operations
before calling: search `BillingCheckout Link`, `billing checkout`, `customer due
day` and `preferred payment day`. An empty search for `RenewalPolicy` does not
establish that a customer preference is unavailable.

## Separate the requested effects

| Resource | Meaning | Known API surface |
| --- | --- | --- |
| Customer `DueDay` (JSON `dueday`) | Saved customer preference, integer 1–31 | Written by consolidated `POST /Sales/BillingCheckout/Link` |
| Billing checkout link `dueDay` | Due day for the configured billing group | `GET` and `POST /Sales/BillingCheckout/Link` |
| Contract `dueDay`, `start`, `nextDueDate` | Service coverage and recurring calendar | Contract operations; inspect each contract independently |
| Customer `RenewalPolicy` | Whether renewal requires payment | Separate policy; not a preferred-day writer |
| Issued charge `dueDate` | Frozen due date of an existing charge | Not rescheduled by saving the preference |

Do not replace a request for the general customer preference with edits to every
contract. A contract's explicit day can differ from the customer preference;
saving the preference does not rewrite its coverage, next cycle or historical
charges. For consolidated billing, the saved link day takes precedence over the
customer day proposed when there is no link; standalone billing uses its own group.
Do not describe contract-day precedence as a universal rule for all billing.

## Read, preserve, change, verify

1. Resolve the customer's context GUID. Discover `GET` and `POST
   /Sales/BillingCheckout/Link` and inspect their current schemas. Read the
   consolidated group with `contextId=<customer GUID>` and **no contractId**.
   A contract GUID selects a standalone group and does not update `Customer.DueDay`.
2. Retain the returned `enabled`, `recurringCardEnabled`,
   `preferredPaymentMethod` and `allowedPaymentMethods`. `availablePaymentMethods`
   is eligibility information, not a replacement for the saved allowed methods.
   This is a configuration write, not a one-field patch: omitted booleans or
   payment preference can change other settings. If the installed schema cannot
   preserve the current settings, report that limitation before writing.
3. For a request such as day 09, send integer `9` as `dueDay`, `contextId` as the
   customer GUID and `contractId: null`, preserving the settings read above. Do
   not send `nextDueDate`, enable billing or recurring card, or change payment
   methods merely to save the day.
4. Read the consolidated link again and verify the requested `dueDay` and the
   preserved settings. The successful consolidated configuration transaction
   saves both `Customer.DueDay` and the link day; its independent GET verifies
   the persisted link. A GET alone, before any write, may return an existing
   link's day or a proposed fallback and does not prove the raw customer value.
   Report "customer preference and consolidated billing day saved" only after
   the successful write and verification; distinguish any separately requested
   contract changes and their outcomes.

Payload illustration **only when the preceding GET returned these exact settings**
(enabled, recurring-card offering off, PIX and card allowed, no preferred method):

```json
{
  "contextId": "<resolved customer GUID>",
  "contractId": null,
  "enabled": true,
  "dueDay": 9,
  "recurringCardEnabled": false,
  "preferredPaymentMethod": null,
  "allowedPaymentMethods": [0, 1]
}
```

Never copy those configuration values as defaults. This operation configures the
link and customer preference; it does not itself issue a charge or collect payment.

## Concrete blockers and discovery limits

- The billing checkout feature and unified billing must already be enabled for
  this customer. `409 "Checkout consolidado ainda não está habilitado."` is a
  concrete configuration blocker. A GET `404` can mean no eligible service and
  no existing link. Do not activate checkout or create an arbitrary configuration
  as a workaround for a preference-only request.
- `recurringLocked=true` signals frozen card terms. A changed day is rejected with
  `"Encerre e reconcilie a autorização de cartão antes de alterar o vencimento."`.
  Report the required reconciliation; changing the preference does not authorize
  canceling a card agreement. Preserve any other validation failure as observed.
- `"An aligned schedule requires a reviewed correction before changing its dates."`
  comes from the contract writer. It blocks the attempted contract calendar edit;
  it does not prove that the separate customer preference write is forbidden.
  Do not remove alignment metadata or repeatedly resubmit date edits. If the user
  requested both effects, complete the authorized preference operation when
  available and report the contract correction separately.
- The known raw preference reader is `GET /Sales/Customer?id=<customer GUID>`,
  whose `Customer` response uses **`dueday`**. This controller is hidden from
  production OpenAPI in the reviewed source. Do not invent a `POST /Sales/Customer`
  or bypass tool discovery to call a hidden route. Its absence from search is not
  proof that the stored preference does not exist.
- A `503` on `Customers/{contextId}/RenewalPolicy` describes that call's
  availability. It says nothing about the due-day configuration route. If the
  actual billing operation is missing from deployed OpenAPI, report that specific
  discovery limitation rather than declaring that customers have no preference.

## Source evidence

Reviewed on 2026-11-09; these sources explain semantics, while the deployed
OpenAPI remains the calling contract:

- [Customer JSON field and range](https://github.com/sufficit/sufficit-base/blob/05c0023d88c07d1be94af918c5d9e2520aba29bd/src/Sales/Customer.cs).
- [Billing routes and management roles](https://github.com/sufficit/sufficit-endpoints/blob/a9b0bdcd8840522132f4f2f8da2f6e59b513706b/src/Controllers/Sales/BillingCheckoutController.cs),
  [request and response fields](https://github.com/sufficit/sufficit-endpoints/blob/a9b0bdcd8840522132f4f2f8da2f6e59b513706b/src/Sales/BillingCheckoutModels.cs),
  [Configure transaction, GetLink fallback and feature/card guards](https://github.com/sufficit/sufficit-endpoints/blob/a9b0bdcd8840522132f4f2f8da2f6e59b513706b/src/Sales/BillingCheckoutService.cs).
- [Hidden customer reader](https://github.com/sufficit/sufficit-endpoints/blob/a9b0bdcd8840522132f4f2f8da2f6e59b513706b/src/Controllers/Sales/CustomerController.cs),
  [renewal policy](https://github.com/sufficit/sufficit-base/blob/05c0023d88c07d1be94af918c5d9e2520aba29bd/src/Sales/CustomerRenewalPolicy.cs),
  [contract alignment guard](https://github.com/sufficit/sufficit-efdata/blob/74d30d6145175d3aa577dab8d3e67f8bd13c7299/src/Sales/EFSalesProvider.Recurring.cs).
