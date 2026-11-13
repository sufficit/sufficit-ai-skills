# Telephony credit purchases and commitments

## Interpret the business request

At Sufficit, **“lançar saldo” means buying telephony credit**. The same applies to
“colocar saldo” or “adicionar crédito para ligações”. Do not ask whether this
means recording a financial receipt or granting a promotional benefit. An explicit
request for a different product or a bonus has its own workflow; do not override it.

Financial receipts are recorded exclusively by the integration systems. Agents do
not register receipts, mark payments received or manufacture financial credit to
fund a purchase. A financial debit produced by an authorized service purchase is
part of that purchase, not a manual receipt.

| Requested outcome | Effect |
|---|---|
| “Lançar R$ X de saldo” | One telephony credit purchase, with its commercial service, financial debit/funding and delivered call credit. |
| “Firmar comprometimento de R$ X por mês” | Agreement only: amount, cycle and anniversary. No purchase, debit, call credit or automatic renewal is implied. |
| “Comprar R$ X automaticamente todo mês” | Explicit recurring purchase with agreed amount and calendar; retain past purchases and receipts. |
| Correct a previous purchase | Audited correction of the identified original operation; no compensating duplicate service. |

A credit's validity is separate from its purchase frequency. The current ordinary
one-off purchase flow grants six months of validity; that does not establish a
six-month purchase cycle or authorize monthly purchases. A tariff such as BRL/min
prices consumption; it is not the purchase amount or monthly commitment.

## Make one credit purchase

1. Resolve the customer by GUID and read existing services/purchases and the
   financial and call balances separately. Match the requested resource: ordinary
   outbound and toll-free/0800 credit must not be silently substituted. A billed
   0800 number or a confirmed commitment is not evidence of a delivered top-up.
2. Discover the live purchase operation and inspect its body and authority headers.
   The known ordinary one-off writer is `POST /Sales/CallCreditPurchase`; it
   coordinates funding and creation of the corresponding service. Do not replace
   it with independent writes to the balance, a generic credits wallet, or a
   second service-creation call. If the requested resource is unsupported by the
   discovered writer, report that concrete limitation rather than buying another
   kind of credit.
3. Determine the amount from the request. Use the requested instant or the current
   instant for a purchase requested now, keeping UTC on the wire. Do not backdate
   to an old service's end or infer the amount from a commitment, tariff, balance
   or last purchase. Resolve only materially missing customer/amount/resource data.
4. Keep one `operationId` and the same payload for this purchase. The current
   writer also requires `cutoverId` and the commercial authority headers. Obtain
   them through the [commercial session flow](sales.md#renewing-a-legacy-monthly-service),
   not from the user. Supply headers as headers. On authority/revision conflict,
   read fresh state and reconcile before another write; never change operation
   identity to escape a conflict.
5. Follow the live writer's payer/funding policy. Do not set `allowWithoutBalance`
   merely because the caller is a manager; purchasing without balance requires
   an explicit authorized exception. Do not invent a payment or financial bonus.
   The ordinary writer needs a previous tariffed service. If it reports that the
   customer has none, inspect the supported initial-service creation flow; do not
   create a dummy predecessor or copy another customer's service.
6. After the write, independently verify the operation/service identity, amount,
   dates, financial debit/funding and delivery of the telephony credit. An accepted
   command, positive financial balance or a commercial service alone does not
   prove call credit was delivered. Report a pending/failed leg accurately.

After a timeout or uncertain response, inspect the same operation and its receipts
before retrying. Do not issue another purchase, create a replacement service or
apply direct call-balance changes to compensate for an unverified result. A second
purchase is a separate business effect and needs a separate request.

## Record a commitment without buying credit

Discover `GET /Telephony/Billing/Commitment` and
`POST /Telephony/Billing/Commitment/Confirm` in the deployed OpenAPI. Read the
customer's agreement before writing; Confirm can edit an existing agreement, so
an existing different agreement must be reconciled with the requested change.
If the requested agreement already exists, verify it rather than confirming again.

Confirm accepts a manual agreement without a detected draft: `contextId`, positive
`minimumAmount`, `cycleMonths` from 1 to 12 (default 1), and explicit
`anniversaryUtc` for creation/reactivation without a draft. No draft or recharge
history needs to be manufactured. A discarded draft remains a conflict. A missing
anniversary preserves the current anchor only when editing an active agreement.

The commitment flow permits `manager`, `salesmanager` and `administrator`;
confirmation requires an identified approver and records an audit. A refusal does
not authorize granting roles or using another identity. Verify the saved amount,
cycle and anniversary by GET; use Confirmed/Assessment for independent agreement
and cycle evidence. Check the separate `Commitment/Preference` when 0800 credit
participation is relevant; do not change it implicitly.

A commitment alone never authorizes a purchase or recurring service. For explicit
automatic purchases, discover the deployed recurring-credit flow and check the
existing contract's source, recurrence, funding and next cycle. Do not turn a
one-off service into recurring merely to show the commitment in service history.
If the required recurring configuration is not exposed, report that limitation;
do not synthesize future purchases or backfill a series of services.

For historical settlement without new call credit, billing pauses or mismatched
financial dates, read [service reconciliation](service-reconciliation.md). A
matched debit alone does not prove that credit was delivered.

## Advance renewal for a paid customer without call balance

Owner rule (12/11/2026). When a customer has already paid, the call balance is at or
below zero and the financial balance is positive:

1. Renew the most recent fixed recurring services in advance, on the customer's
   preferred-day calendar. Use whole cycles with no proration, charge or bonus. Never
   debit an already paid competence again.
2. Put the remaining financial balance into call credit on the tariffed service, but
   only when the tariffed recharges have always had the same value. Buy whole
   recharges of that value.
3. If the recharge values differ, or the leftover is not a whole multiple of that
   value, do not choose an amount. Warn the manager with the balance, the past
   values and the services already renewed.

For a tariffed service that is already monthly (a commitment with automatic
renewal), the leftover becomes an **extra recharge** on the same contract. The
monthly schedule, periods and commitment stay unchanged. Each extra recharge is
listed in the contract parameter `billing.extra-call-credits.v1` (id, amount,
start, expiration). The services table then shows a second value line: "Neste
ciclo: R$ X do compromisso + R$ Y a mais". The engineering command is
`EFSalesProvider.PurchaseExtraRecurringCallCredit`. If the deployed API does not
expose an equivalent writer, report that limitation; do not convert the service to
a one-off purchase or create a second tariffed service to get around it.

The extra purchase is funded from the shared balance and posted on the Brasília
civil day. It is delivered by the same funded outbox as the monthly cycle.
Delivery can be refused while the posting date is still in the future. In that
case, resume the same suspended event after it becomes due; never issue a new
purchase. Verify the financial debit, the delivered credit and the call balance
independently.

## Preserve service history

Keep original purchase IDs, values, timestamps, delivered credits and financial
receipts. Credit exhaustion or expiry does not authorize rewriting a past purchase.
Do not alter old periods to represent a new purchase, split one purchase into
monthly services, migrate the customer or enable automation as a side effect.

A requested correction uses the supported audited writer and concurrency controls
for the identified operation. Verify commercial history, its financial effect and
call credit afterward. Do not delete history, write SQL or create unrelated bonus,
receipt or service entries to make the displayed balances agree.
