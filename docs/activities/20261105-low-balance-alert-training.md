# Telephony low-balance alert training

Updated `sufficit-api` from 1.0.21 to 1.0.22 instead of creating a competing skill.
The [workflow](../../skills/sufficit/sufficit-api/references/low-balance-alerts.md)
covers account resolution, existing alerts, consumption-based defaults, a usable
primary destination, supported writes, independent read-back and a final invitation
to change preferences. Catalog discovery, card, release and both digests agree.

The initial 20% of median recharge-cycle consumption is an explicit starter
heuristic selected for this workflow, not a pre-existing product guarantee.
Source inspection confirmed the call-balance event, BRL 50 fallback, strict
less-than threshold and deduplication per recharge/contact/key. It also found that
the Subscribe route is hidden from release OpenAPI; agents must discover an
available published writer or report that limitation. Generic credits wallets
must not be used as substitutes for telephony balance.

Reviewed eight fictional scenarios in the reference: calculated threshold,
existing alert, missing history, blocked WhatsApp with valid email, ambiguous
identity/missing recipient, uncertain write, already-low balance, and unavailable
API access. Arithmetic: median(180, 200, 220) × 20% = BRL 40. These are manual
instruction/decision checks, not a live-agent or production execution test.

Initial validation: all 184 packages, the generated index and skill quick validator
passed. The 38-test suite initially reported one Markdown coverage failure because
the temporary plan was not linked. After linking the temporary plan, all 38 tests and Markdown coverage passed.
The completed plan was then retired into this delivery record.

Delivery scope: skill source and catalog metadata only. No customer alert was
configured, no message was sent, and Genius installation/publication is not
established by this repository change. Commit and push follow local validation.
