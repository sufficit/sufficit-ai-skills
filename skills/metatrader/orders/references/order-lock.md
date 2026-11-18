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

## Layer 3: risk and discipline rules (optional, recommended)

Optional `risk` block in `limits.json` (all keys optional; `null`/`false` disables a rule):

```json
"risk": {
  "max_risk_per_trade": 20.0,
  "require_stop_on_buy": true,
  "require_reason": true,
  "max_daily_loss": 30.0,
  "losing_streak_n": 2,
  "cooldown_hours": 24
}
```

- `size SYMBOL ENTRY STOP`: suggests a quantity limited by `max_value_per_order` and by
  `max_risk_per_trade / |entry - stop|`, rounded down to the symbol's volume step
  (fixed-fractional sizing). Nothing is sent.
- `prepare ... --stop S --reason TEXT`: refuses a buy without a planned stop, an order
  without a written reason, or a risk to the stop above `max_risk_per_trade`. The stop is
  only planned; it is not sent with the order.
- `breaker`: reads realized P&L of closing deals in the MT5 history (last 30 days).
  Blocks new orders when today's realized loss reached `max_daily_loss`, or for
  `cooldown_hours` after `losing_streak_n` losing exits in a row (avoids revenge
  trades). `prepare` and `send` both run it.
- Each `prepared` and `sent` event is appended to `journal.jsonl` (with the reason), for
  later review of what was done and why.

These rules are recommendations the user configures; they never replace the user's
explicit confirmation and never authorize an order by themselves.

Credit: the ideas for this layer were adapted from the MIT-licensed
[tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills)
(`position-sizer`, `pre-trade-discipline-gate`, `drawdown-circuit-breaker`). The code here
is an independent, minimal implementation for MT5/B3; no code was copied.
