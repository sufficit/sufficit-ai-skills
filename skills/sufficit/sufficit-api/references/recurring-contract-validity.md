# Recurring contract validity and monthly periods

Read this before renewing a monthly service, changing its end date, or correcting
an active recurring contract that appears expired. Discover the deployed API
operation and read its schema; the field names below explain business semantics,
not a route or permission to migrate or cancel a service.

## Separate the contract from its periods

- Native contract `end` (`Contract.End`): the contractual stop of the service.
  A recurring service agreed for an indefinite term keeps this null. Filling it
  with the latest monthly expiry caps all subsequent coverage, even when the
  contract is Active and automation appears enabled.
- Period `periodStart` / `periodEnd`: finite boundaries of one monthly competence.
  Ends are exclusive: the next period starts at the preceding period's end.
  They do not establish that the whole contract ends on that date.
- `nextDueDate`, the customer's preferred day and posting date: billing schedule
  information. None is a value to copy into the contract's `end`.
- Recurrence configuration and settlement: independent choices. Recurring does
  not mean postpaid, and prepaid does not mean a service stops after each payment.
  Read the saved recurrence, including `billing.recurrence.v1` when present;
  absent optional metadata does not establish that a legacy-adopted monthly
  agreement is one-off. Changing catalog defaults does not update that agreement.

Example: an indefinite native monthly service has `end: null`, with the current
period `[03/11/2026, 03/12/2026)` and the next `[03/12/2026, 03/01/2027)`.
Do not save `end: 03/12/2026` to show that November was renewed. That would limit
the contract at December's boundary rather than describe the November purchase.
For prepaid billing, the current period's debit belongs to its start; recording
an end or repeating a renewal does not reconcile an existing charge.

## Choose the owner and intended change

Read the contract, latest history, periods and linked financial operations before
writing. Use customer comments and the manager's agreement to distinguish an
indefinite recurring service, an explicitly fixed-term recurring agreement,
a real cancellation/pause and a one-off purchase.

- Native recurring service: let its recurrence produce periods. Investigate a
  missing period or debit separately. Do not extend `end` by a month, run the
  legacy renewal writer, recreate a purchase or mark a payment to bypass a cap.
- LegacySales service: the legacy service row's `end` may be the current purchased
  coverage, mirrored into its contract projection. Follow the
  [legacy renewal flow](sales.md#renewing-a-legacy-monthly-service). Do not clear
  every legacy `end`, reinterpret its projection as a native indefinite contract,
  or migrate it merely because the manager said “renew”.
- A genuinely fixed-term recurring service retains its agreed contract end.
  Explicit cancellation and documented pauses remain effective. This rule does
  not authorize bulk removal of end dates from recurring or historical services.

## Correct an unintended native contract cap

When correction is authorized and the indefinite agreement is confirmed, use the
supported contract writer to remove only the erroneous contractual end. Preserve
source, identity, price, recurring interval, settlement, preferred day, resources
and already purchased periods. Include the current revision/concurrency fields
required by the discovered schema. Do not change monthly period ends to null or
issue another debit for the competence already charged.

Read independently after saving: the contract has no end; the existing competence
and its single linked debit remain intact; the next competence can exist beyond
the former cap; recurrence remains enabled and balances have not changed. A
future `nextDueDate`, Active status or a successful save alone does not prove this.
If the write response is ambiguous, inspect state/history before retrying.
Engineering maintenance outside this API skill follows the repository provider,
transactional history and global replay/commission checks described in
[service reconciliation](service-reconciliation.md#audit-evidence-and-completion).
