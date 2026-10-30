# MetaTrader 5 own-account orders skill

Added `metatrader5-orders` 0.1.0 under `skills/metatrader/orders` (generic, not company-specific). It records what was learned while
connecting MetaTrader 5 under Wine (Linux cloud executor) to a real XP Investimentos account
(`XPMT5-PRD`) with the password kept only in the Sufficit Identity Vault.

## Content

- Setup for Windows and for Wine 64-bit + Xvfb + 64-bit embeddable Python, offline wheels.
- Broker-specific MT5 build requirement, `login.ini` first login and secret hygiene.
- Two-layer order lock: terminal AutoTrading off and `order_lock.py` with symbol/value limits
  and a single-use, expiring confirmation code per order.
- Validation without a demo account and a troubleshooting table.

## Validation

- Lock validated live: symbol outside list, value above limit, send without prepare and wrong
  code were refused; a valid fractional order was only simulated (`No money`, zero balance).
  No order was sent.
- Repository validation and skill index check passed. The Markdown coverage failure on
  `docs/PLAN-HUMAN-NOTIFICATIONS.md` already existed on `main` and is unrelated.

Living guide: to be updated as real orders are placed and new lessons appear.
