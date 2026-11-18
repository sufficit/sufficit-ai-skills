"""MT5 order lock. Usage (run with the Windows Python that has MetaTrader5):
  order_lock.py status
  order_lock.py size SYMBOL ENTRY STOP                -> suggest a quantity from the risk limits (nothing sent)
  order_lock.py breaker                               -> daily loss / losing-streak check from MT5 history
  order_lock.py prepare SYMBOL buy|sell QTY [PRICE] [--stop S] [--reason TEXT]
                                                      -> simulate only (order_check), print code
  order_lock.py send CODE                             -> send the prepared order if CODE is valid
Environment: MT5_TERMINAL = full path to the broker's terminal64.exe.
Nothing is sent without a valid, unexpired, single-use code and AutoTrading enabled.
"""
import datetime as dt, hashlib, json, math, os, secrets, sys, time
import MetaTrader5 as mt5

BASE = os.path.dirname(os.path.abspath(__file__))
LIM = json.load(open(os.path.join(BASE, "limits.json")))
PEND = os.path.join(BASE, "pending.json")
JOURNAL = os.path.join(BASE, "journal.jsonl")
# Risk rules adapted from ideas in tradermonty/claude-trading-skills (MIT):
# position-sizer, pre-trade-discipline-gate, drawdown-circuit-breaker. Own code.
RISK = {"max_risk_per_trade": None, "require_stop_on_buy": False, "require_reason": False,
        "max_daily_loss": None, "losing_streak_n": None, "cooldown_hours": 24}
RISK.update(LIM.get("risk", {}))


def log(event, **kw):
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": dt.datetime.now().isoformat(timespec="seconds"), "event": event, **kw}) + "\n")


def opt(name):
    if name in sys.argv:
        i = sys.argv.index(name); v = sys.argv[i + 1]; del sys.argv[i:i + 2]; return v
    return None


def breaker():
    """Return (ok, message) from realized P&L of closing deals in MT5 history."""
    now = dt.datetime.now()
    deals = mt5.history_deals_get(now - dt.timedelta(days=30), now + dt.timedelta(days=1)) or ()
    outs = sorted((d for d in deals if d.entry in (mt5.DEAL_ENTRY_OUT, mt5.DEAL_ENTRY_INOUT)), key=lambda d: d.time)
    today = now.date()
    pnl_today = sum(d.profit + d.commission + d.swap + getattr(d, "fee", 0.0) for d in outs
                    if dt.datetime.fromtimestamp(d.time).date() == today)
    if RISK["max_daily_loss"] is not None and -pnl_today >= RISK["max_daily_loss"]:
        return False, f"daily loss {pnl_today:.2f} reached limit -{RISK['max_daily_loss']:.2f}; no new orders today"
    n = RISK["losing_streak_n"]
    if n and len(outs) >= n and all(d.profit < 0 for d in outs[-n:]):
        until = dt.datetime.fromtimestamp(outs[-1].time) + dt.timedelta(hours=RISK["cooldown_hours"])
        if now < until:
            return False, f"{n} losing exits in a row; cooldown until {until:%Y-%m-%d %H:%M}"
    return True, f"ok (realized today {pnl_today:.2f})"


def size_for(sym, entry, stop_px):
    info = mt5.symbol_info(sym)
    step = (info.volume_step if info else 1.0) or 1.0
    caps = [LIM["max_value_per_order"] / entry]
    if RISK["max_risk_per_trade"] and stop_px and abs(entry - stop_px) > 0:
        caps.append(RISK["max_risk_per_trade"] / abs(entry - stop_px))
    return math.floor(min(caps) / step) * step
TERM = os.environ.get("MT5_TERMINAL", r"C:\Program Files\MetaTrader 5\terminal64.exe")


def stop(msg, code=1):
    print(msg); mt5.shutdown(); sys.exit(code)


if not mt5.initialize(TERM, timeout=60000):
    print("ERROR initialize", mt5.last_error()); sys.exit(2)
action = sys.argv[1] if len(sys.argv) > 1 else ""

if action == "status":
    t, a = mt5.terminal_info(), mt5.account_info()
    stop(f"connected={t.connected} trade_allowed={t.trade_allowed} server={a and a.server} balance={a and a.balance}", 0)

elif action == "breaker":
    ok, msg = breaker(); stop(("OK: " if ok else "BLOCKED: ") + msg, 0)

elif action == "size":
    sym, entry, stp = sys.argv[2].upper(), float(sys.argv[3]), float(sys.argv[4])
    mt5.symbol_select(sym, True)
    q = size_for(sym, entry, stp)
    stop(f"SIZE: {q:g} {sym} | value ~ {q * entry:.2f} | risk to stop ~ {q * abs(entry - stp):.2f} | NOTHING WAS SENT", 0)

elif action == "prepare":
    stop_px = opt("--stop"); reason = opt("--reason")
    stop_px = float(stop_px) if stop_px else None
    sym, side, qty = sys.argv[2].upper(), sys.argv[3].lower(), float(sys.argv[4])
    price = float(sys.argv[5]) if len(sys.argv) > 5 else None
    if sym not in LIM["allowed_symbols"]: stop(f"BLOCKED: {sym} not in allowed symbols")
    if side not in ("buy", "sell"): stop("BLOCKED: side must be buy or sell")
    if not mt5.symbol_select(sym, True): stop(f"ERROR: symbol {sym} unavailable")
    time.sleep(2)
    tk = mt5.symbol_info_tick(sym)
    ref = price or (tk.ask if side == "buy" else tk.bid) or tk.last
    value = ref * qty
    if value > LIM["max_value_per_order"]:
        stop(f"BLOCKED: estimated value {value:.2f} above limit {LIM['max_value_per_order']:.2f}")
    buy = side == "buy"
    if buy and RISK["require_stop_on_buy"] and not stop_px:
        stop("BLOCKED: plan a stop price first (--stop)")
    if RISK["require_reason"] and not reason:
        stop("BLOCKED: write the reason/plan for this order (--reason)")
    if stop_px and RISK["max_risk_per_trade"] and abs(ref - stop_px) * qty > RISK["max_risk_per_trade"]:
        stop(f"BLOCKED: risk to stop {abs(ref - stop_px) * qty:.2f} above limit {RISK['max_risk_per_trade']:.2f}")
    ok, msg = breaker()
    if not ok: stop("BLOCKED: " + msg)
    req = {"symbol": sym, "volume": qty, "price": ref,
           "action": mt5.TRADE_ACTION_PENDING if price else mt5.TRADE_ACTION_DEAL,
           "type": (mt5.ORDER_TYPE_BUY_LIMIT if buy else mt5.ORDER_TYPE_SELL_LIMIT) if price
                   else (mt5.ORDER_TYPE_BUY if buy else mt5.ORDER_TYPE_SELL),
           "type_time": mt5.ORDER_TIME_DAY, "type_filling": mt5.ORDER_FILLING_RETURN,
           "comment": "genius"}
    chk = mt5.order_check(req)
    code = secrets.token_hex(3).upper()
    with open(PEND, "w") as f:
        json.dump({"req": req, "stop": stop_px, "reason": reason, "code_sha256": hashlib.sha256(code.encode()).hexdigest(),
                   "expires": time.time() + LIM["confirmation_seconds"]}, f)
    print(f"SUMMARY: {side} {qty:g} {sym} {'limit' if price else 'market ~'} {ref:.2f} | value ~ {value:.2f}")
    print("SIMULATION (order_check):", None if chk is None else (chk.retcode, chk.comment), mt5.last_error())
    if stop_px: print(f"PLANNED STOP: {stop_px:.2f} | risk ~ {abs(ref - stop_px) * qty:.2f} (stop is NOT sent; place it as a separate order)")
    log("prepared", symbol=sym, side=side, qty=qty, ref=ref, stop=stop_px, reason=reason)
    print("CONFIRMATION CODE:", code, f"(valid {LIM['confirmation_seconds']} s)")
    stop("NOTHING WAS SENT", 0)

elif action == "send":
    if not os.path.exists(PEND): stop("BLOCKED: no prepared order")
    p = json.load(open(PEND)); os.remove(PEND)  # single use
    if len(sys.argv) < 3 or hashlib.sha256(sys.argv[2].upper().encode()).hexdigest() != p["code_sha256"]:
        stop("BLOCKED: invalid confirmation code")
    if time.time() > p["expires"]: stop("BLOCKED: confirmation expired, prepare again")
    if not mt5.terminal_info().trade_allowed: stop("BLOCKED: AutoTrading is disabled in the terminal")
    ok, msg = breaker()
    if not ok: stop("BLOCKED: " + msg)
    r = mt5.order_send(p["req"])
    log("sent", req=p["req"], reason=p.get("reason"), retcode=None if r is None else r.retcode)
    print("RESULT:", None if r is None else r._asdict(), mt5.last_error())
    stop("END", 0)
else:
    stop(__doc__)
