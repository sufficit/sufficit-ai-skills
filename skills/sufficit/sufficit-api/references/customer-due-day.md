# Customer preferred payment day

For "dia preferencial", "dia de vencimento do cliente" or changing the
customer's preferred day each month, discover `PaymentPreferences` in the live
OpenAPI. The dedicated customer operation is independent of checkout availability
and monthly-service eligibility. Search `customer payment preferences` or the
exact path if a Portuguese search finds nothing.

## Read, change, verify

1. Resolve the customer's context GUID and discover `GET` and `POST
   `/Sales/Customers/{contextId}/PaymentPreferences`. Inspect the deployed schemas.
2. GET that customer's preference. The response is `{"contextId":"...",
   "dueDay":4}`; `dueDay: null` means no saved preference. Confirm the returned
   context matches the target. Do not infer the customer day from contract dates.
3. For day 09, POST `{"dueDay":9,"expectedDueDay":4}`, using the exact saved day
   from step 2 as `expectedDueDay`. Both fields must be explicitly present; use
   `expectedDueDay: null` when the read returned no preference. Days are integers
   1–31. Send `dueDay: null` only when the user requests clearing the preference.
4. GET again and verify the requested day before reporting success. On a network
   failure or unknown write outcome, read first: do not blindly resend. On 409
   `customer_payment_preference_changed`, reread and check the requested outcome;
   do not overwrite another operator's change with an obsolete expectation.

Known authorization: authenticated administrator/manager or scoped `clientadmin`
for writes; reading also accepts scoped `balanceview`. Internal service callers
need the corresponding context permission. A 403 is a concrete permission
refusal, not evidence that the preference is unsupported. A 404 means the contact
identity was not found. No eligible monthly contract or checkout activation is
required by this dedicated operation.

## Separate the effects

| Resource | Meaning | Effect of the preference-only operation |
| --- | --- | --- |
| Customer `DueDay` | Saved customer preference, 1–31 or null | Changed |
| Existing checkout link `dueDay` | Configured day of a billing group | Preserved |
| Contract `dueDay`, `start`, `nextDueDate` | Service coverage and recurring calendar | Preserved |
| Issued charge `dueDate` | Frozen date of an existing charge | Preserved |
| Customer `RenewalPolicy` | Whether renewal requires payment | Preserved; unrelated to preferred day |

Report that the **customer preference** was saved. Do not claim that all services
or existing checkout links now use that day. The saved link day takes precedence
over the proposed customer day when a consolidated link already exists; a
standalone group has its own configuration. If the user asks to align existing
billing as well, inspect and handle those requested resources separately.

`"An aligned schedule requires a reviewed correction before changing its dates."`
comes from the contract writer. It blocks the attempted calendar edit, not the
separate preference-only operation. Do not remove alignment metadata or repeatedly
resubmit date edits. Complete the authorized preference change when available and
report any separately requested calendar correction as its own outcome.

## Older deployments and checkout configuration

If `PaymentPreferences` is absent from the deployed OpenAPI, report the missing
operation. Do not invent routes. The historical consolidated `POST
/Sales/BillingCheckout/Link` with `contractId: null` writes both `Customer.DueDay`
and the link's configuration. It is appropriate for a requested billing-link
change; it is not a substitute for a preference-only request. In particular, do
not activate checkout, enable recurring card, alter payment methods or cancel a
card agreement to make a preference change possible. A contract GUID on that
route selects a standalone group and does not update the customer preference.

`GET /Sales/Customer?id=<customer GUID>` is a historical raw reader whose response
uses lowercase **`dueday`**; it is hidden from production OpenAPI in the reviewed
source. Its absence from search does not prove the preference does not exist.
Do not invent a `POST /Sales/Customer` or bypass tool discovery for hidden routes.
A 503 on `Customers/{contextId}/RenewalPolicy` describes only that unrelated call.

## Source evidence

- [Dedicated API and concurrency contract](https://github.com/sufficit/sufficit-endpoints/blob/152e7f9f8981e35a68bbe38d36d71236d787a662/docs/CUSTOMER-PAYMENT-PREFERENCES.md),
  [controller and authorization](https://github.com/sufficit/sufficit-endpoints/blob/152e7f9f8981e35a68bbe38d36d71236d787a662/src/Controllers/Sales/CustomerPaymentPreferencesController.cs),
  [customer-only transaction](https://github.com/sufficit/sufficit-endpoints/blob/152e7f9f8981e35a68bbe38d36d71236d787a662/src/Sales/CustomerPaymentPreferencesStore.cs).
- [Historical customer JSON field](https://github.com/sufficit/sufficit-base/blob/05c0023d88c07d1be94af918c5d9e2520aba29bd/src/Sales/Customer.cs),
  [checkout precedence and guards](https://github.com/sufficit/sufficit-endpoints/blob/a9b0bdcd8840522132f4f2f8da2f6e59b513706b/src/Sales/BillingCheckoutService.cs),
  [contract alignment guard](https://github.com/sufficit/sufficit-efdata/blob/74d30d6145175d3aa577dab8d3e67f8bd13c7299/src/Sales/EFSalesProvider.Recurring.cs).

Source reviewed on 2026-11-09. The deployed OpenAPI remains the calling contract;
repository publication alone does not establish deployment readiness.
