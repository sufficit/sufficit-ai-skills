---
name: metatrader5-orders
description: "Set up MetaTrader 5 with the Python MetaTrader5 library (natively on Windows or under Wine on Linux), connect it to the user's own brokerage account with the password kept in the Sufficit Identity Vault, read quotes, and send orders only on the user's explicit, per-order confirmation behind a two-layer lock (terminal AutoTrading off plus value and symbol limits). Use when a user wants to operate their own account (for example XP Investimentos on B3) through Genius. Living guide, updated as lessons are learned."
---

# MetaTrader 5: own-account operations with an order lock

Use when a user asks to connect MetaTrader 5 (MT5) to their own brokerage account, read
market data through Python, or have Genius place orders for them. This skill covers only
the user's **own** account, at the user's own request. It is not investment advice: never
recommend assets, sizes or timing, and never trade on your own initiative.

## Ground rules

- **Read-only by default.** Connecting, reading the account and reading ticks/candles never
  sends orders. Say so to the user.
- **Orders only on explicit request, one at a time.** Each order is prepared, simulated
  with `order_check`, shown to the user with a one-time confirmation code, and sent only
  after the user repeats that code. Never batch, loop, or retry an order send.
- **No demo account is required**, but prefer one when the broker offers it. Without demo,
  validate the lock with orders that are refused or only simulated (see
  [references/order-lock.md](references/order-lock.md)).
- **Password lives only in the Vault.** Canonical reference:
  `personal/metatrader/<broker>/password` (for example `personal/metatrader/xp/password`).
  Never ask the user to paste it in chat. If missing, give the user the Vault creation
  link (`https://identity.sufficit.com.br/vault/new?name=metatrader%2F<broker>%2Fpassword`)
  or prepare the entry with `vault_prepare_entry`.
- **Never print the resolved secret, not even masked.** Write it straight to a file
  created under `umask 077`, check only its length, and delete every temporary copy
  (password file, `login.ini`) right after the terminal logs in. A masking attempt once
  failed and leaked a password into the conversation history; if that happens, tell the
  user immediately and recommend changing the broker password.
- The account login number is not a secret, but keep it out of public files.
- Report every step to the user in plain language, including failures.

## Workflow

1. **Environment.** Follow [references/setup.md](references/setup.md): Windows runs MT5
   and Python natively; Linux needs Wine 64-bit, a 64-bit Windows Python and Xvfb.
2. **Use the broker's own MT5 build.** The generic MetaQuotes terminal does not know
   broker servers (for XP: `XPMT5-PRD`). Install the broker installer into its own folder.
3. **First login** through a temporary `login.ini` (`/config:`), then delete it. Check the
   terminal journal for `authorized on <server>`.
4. **Read-only test with Python** (`mt5.initialize(<terminal path>)`, `account_info`,
   `symbol_info_tick`, `copy_rates_from_pos`).
5. **Install the order lock** ([references/order-lock.md](references/order-lock.md),
   script [scripts/order_lock.py](scripts/order_lock.py)) and validate it before any real
   order.
6. **Placing an order** (only when the user asks): `prepare` → show summary, estimated
   value, simulation result and code → user confirms with the code → temporarily enable
   AutoTrading → `send` → disable AutoTrading again → report the result (ticket, price,
   retcode).

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for `IPC timeout`
(-10005), `Service is not available`, master-password change prompts, Wine and pip issues.
