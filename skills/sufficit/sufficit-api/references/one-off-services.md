# One-off work: validity and billing

A service performed once has a commercial validity instant: start and end are
equal. This is not “no validity”. Preserve the verified execution instant and
its available precision; never substitute payment date or invent a future end,
month of coverage or approximate work time. Read customer comments and purchase
history before resolving the instant; ask only if the business fact is missing.

Keep these decisions separate:

| Fact | Persisted meaning |
| --- | --- |
| Execution validity | `Start == End` for instantaneous performed work |
| No future purchases | `billing.recurrence.v1=false` |
| Separate charge | `billing.chargeMode=standalone`, when requested |
| Shared consolidated charge | `billing.chargeMode=unified`, when explicitly agreed |
| Posting time | Prepaid/postpaid is independent of recurrence and charge grouping |
| Paid | Confirmed receipt evidence, never inferred from status or zero-length validity |

Setting non-recurrence does not set separate billing. Read and verify both. A
recurring subscription can also have separate billing; do not treat standalone
as the recurrence flag. Do not universally force separate billing for every
non-recurring service if the customer agreed to consolidation.

This rule concerns performed work. Tariffed top-ups, prepaid resources and other
products with their own coverage/credit validity keep those contracts; a one-time
purchase does not erase the resource's useful lifetime.

Discover the deployed commercial read/write operations in OpenAPI. Read the current
contract, keep its original identities and use the commercial writer so history
is recorded transactionally. Preserve existing debit/payment receipts, price,
customer and purchase snapshots; do not recreate an obligation or payment while
correcting dates or billing grouping. Financial receipt creation remains the
integration's responsibility under this skill.

If equal start/end is rejected, report the deployed validation error. Do not
bypass it by inventing one day/month of service, direct SQL or silently omitting
the end. The engineering fix belongs to the commercial provider. An internal
accounting period may need a positive envelope or preserve issued historical
dates; do not present that period as execution duration or rewrite immutable
purchase evidence to match a new display.

After writing, reread validity, recurrence, charge grouping, renewal and next due
date. Verify requested changes and preserved financial receipts independently.
One-off labels do not prove completion/payment for unrelated services. Explain
any concrete failure without claiming the state was changed.

Maintainer clarification: 11November2026, after a one-off support job appeared
as a monthly prorated service, then incorrectly as validity “not applicable”.
Correct interpretation: an execution instant with equal bounds, no renewal,
and the separately requested billing grouping. API documentation contract:
https://github.com/sufficit/sufficit-endpoints/blob/main/docs/ONE-OFF-SERVICES.md.
