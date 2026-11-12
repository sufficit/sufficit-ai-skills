# Service-history and financial reconciliation

Read this reference when asked to reconcile services, review inconsistent financial
history, restore missing services or review a portfolio. It supplements
[sales](sales.md) and [call-credit purchases](telephony-credit.md); it does not
provide database access or replace discovery of the deployed API.

## Establish the agreement and scope

Read customer observations/comments before deciding about renewal, price, cadence,
financial responsibility or cancellation. Corroborate with original purchases,
receipts, relevant Hermes conversations and available legacy evidence. An integrated
menu often connects to an ISP CRM; record the confirmed CRM name concisely in the
service's additional information, following the manager's model. A request to set
up an integration does not prove that it was technically completed.

Select currently effective contracts by status AND validity dates, separately from
customer commercial status. A manager's belief that current services are prepaid
does not reclassify expired historical agreements. Keep explicit later corrections
ahead of earlier instructions; do not blend superseded calendar proposals.

Credit expiry of up to six months is not a purchase cadence. Evidence of monthly
payments/comments can establish an agreed monthly service, but neither credit
expiry nor a special per-minute tariff establishes its amount or recurrence.

## Check separate financial effects

- Prepaid posts at coverage start; postpaid at coverage end. This classification
  does not itself require receipt of payment. Respect the deployed service-type
  funding policy; do not invent a universal positive-balance gate.
- A represented customer's funding transfer must occur strictly before the
  prepaid service debit, including its time. Verify both transfer legs and the
  debit identity; equal timestamps do not establish the required order. An ended
  current representative link does not erase historical funding obligations.
- Scheduled internal funding uses 05:59:00 GMT-3, before the ordinary 06:00
  activation. Apply this convention only when it keeps funding strictly earlier;
  preserve explicit real-payment timestamps and report historical/timezone cases
  that would require a different safe boundary. Do not postpone money already
  consumed by earlier debits merely to standardize the clock.
- For scheduled service entries with no explicit time, the manager's convention is 06:00
  in America/Sao_Paulo (convert to UTC for that date). This is not authority to
  rewrite timestamps of actual payments or move money into the future.
- Financial reconciliation and delivered call credit are separate. A matched
  debit is insufficient evidence of a top-up. If the manager explicitly chooses
  historical debt settlement without new credit, use the supported audited
  classification and verify existing balances; do not grant replacement credit.
- A missing/unidentified financial link is not proof that payment never arrived.
  Inspect the existing operation and integration receipt. Do not create receipts,
  mark a payment received or associate documents merely by matching amount/date.

“No boleto” comments require reviewing direct billing and the financial
responsible party together. Disable direct billing within the authorized scope;
establish the payer from evidence. Conditional instructions, barter and canceled
relationships are exceptions to investigate, not authority to invent a payer or
reactivate a former representative. A business successor is not automatically the
current responsible party for every former represented customer.

## Erroneous internal resource transfers

The manager's rule is that erroneous internal transfers can simply be removed,
including a compensating return that exists only because of those errors. Remove
the identified matching sides together and verify the expected balances. Do not
create a refund, reversal, replacement credit or customer audit entry merely to
keep these internal mistakes in the statement. No extra business audit or repeated
approval is required when this correction is already authorized.

Preserve the provenance and actual dates of movements originating in external
systems, such as banks and payment providers; internal-transfer cleanup does not
authorize deleting or fabricating those receipts. Keep backend-required technical
idempotency/concurrency controls, without adding financial statement entries.
This rule concerns internal transfers, not deletion of commercial contract history.

For a canceled customer, read the explicit cancellation date before touching
billing. Check the formal classification, active financial assignment and all
later transfers even if their net balance is zero. An exactly compensating return
does not by itself complete the reconciliation or justify a new service debit.

## Restore and correct without recreating history

For a recurring service with an unexpected end, read [contract validity versus
period ends](recurring-contract-validity.md). Correct only a proven unintended
native contract cap; keep monthly period ends and existing financial effects.
Do not bulk-clear legacy coverage, fixed terms or cancellations.

Restore missing historical services only with their original identities, prices,
coverage and status. Resolve a retired legacy label to the appropriate current
catalog item, not just a new display name. Preserve already consolidated/retired
rows and cancellation; restoration does not authorize activation or renewal.

For a billing pause, verify which periods were actually charged and whether a
compensating reversal exists. Use the supported audited correction of the
identified erroneous charge and its matching compensation together where possible;
preserve the real payment, legitimate periods and resulting balances. A pause alone
may not remove an already issued charge. Do not delete unrelated history or issue
an extra bonus to make the totals look correct. Report an unsupported correction
precisely rather than inventing an endpoint.

Customer preference, coverage boundary, period due date, financial posting instant
and external card-subscription schedule are distinct. Verify all affected views.
Preserve a confirmed external subscription when the manager explicitly requests
it; do not claim that changing service dates reprogrammed the card. A first free
period ends at the confirmed boundary, not an inferred full free month.

## Audit evidence and completion

Compare native immutable PostingDate receipts to actual linked ledger movements
independently of review/migration markers. For older receipts lacking PostingDate,
require proven period/identity/settlement evidence; original legacy emission may
legitimately differ from coverage dates. Never force today's preferred day onto
all past months or accept a value/date coincidence as document identity.

Report counts of corrected, explained and unresolved findings separately. A raw
alert count can include reviewed original emissions; do not call those pending
repairs or claim zero global alerts after only fixing one subset. Protect current
balances when considering future timestamps; record the deferred target and
re-evaluate it against fresh state rather than scheduling an automatic replay.

Use supported audited operations with concurrency and idempotency controls, then
independently verify contracts, periods, links, values, ledger and delivered credits.
For engineering-only maintenance outside this API skill, follow the repository's
provider/history policy and global commercial replay/commission checks. A point
repair is not a reason to add customer-specific permanent product methods.

A handoff records exact scope, latest decisions, already executed operation IDs,
private evidence paths, remaining decisions and delivery state. Do not rerun a
previous apply command or treat a saved memory as proof of a database update.
