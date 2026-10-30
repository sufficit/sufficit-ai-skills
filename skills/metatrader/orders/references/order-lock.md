# Order lock

Two independent layers. Both must be open for an order to reach the broker.

## Layer 1: terminal AutoTrading off

Disable automated trading in the terminal configuration (`Config/common.ini`, section
`[Experts]`, `Enabled=0`; keep a backup). Confirm from Python:
`mt5.terminal_info().trade_allowed == False`. With this off, `order_send` is refused by
the terminal even if a script tries. Enable it only for the moment of an order the user
confirmed, then disable again.

## Layer 2: limits and per-order confirmation

[`../scripts/order_lock.py`](../scripts/order_lock.py) reads `limits.json` next to it:

```json
{
  "allowed_symbols": ["PETR4", "PETR4F", "VALE3", "VALE3F", "BOVA11", "BOVA11F"],
  "max_value_per_order": 200.0,
  "confirmation_seconds": 300
}
```

- `prepare SYMBOL buy|sell QTY [PRICE]`: refuses symbols outside the list and estimated
  values above the limit, runs `order_check` (simulation, nothing sent), stores the
  pending request with only the hash of a random 6-hex code, prints summary and code.
- `send CODE`: consumes the pending order once; refuses a missing, wrong or expired code
  and refuses when AutoTrading is off; otherwise calls `order_send` and prints the result.

Agree the limits with the user and change them only on the user's request.

## Validation without a demo account

Run, and expect every line to be refused or only simulated:

1. AutoTrading status → `trade_allowed=False`.
2. `prepare` a symbol outside the list → `BLOCKED`.
3. `prepare` above the value limit → `BLOCKED`.
4. `send` with nothing prepared → `BLOCKED`.
5. `prepare` a valid fractional order → simulation only (with zero balance the broker
   answers `No money`, which is expected).
6. `send` with a wrong code → `BLOCKED`; the pending file must be gone afterwards.

Report each result to the user. Only then offer real orders, small, after a deposit.
