"""MT5 order lock. Usage (run with the Windows Python that has MetaTrader5):
  order_lock.py status
  order_lock.py prepare SYMBOL buy|sell QTY [PRICE]   -> simulate only (order_check), print code
  order_lock.py send CODE                             -> send the prepared order if CODE is valid
Environment: MT5_TERMINAL = full path to the broker's terminal64.exe.
Nothing is sent without a valid, unexpired, single-use code and AutoTrading enabled.
"""
import hashlib, json, os, secrets, sys, time
import MetaTrader5 as mt5

BASE = os.path.dirname(os.path.abspath(__file__))
LIM = json.load(open(os.path.join(BASE, "limits.json")))
PEND = os.path.join(BASE, "pending.json")
TERM = os.environ.get("MT5_TERMINAL", r"C:\Program Files\MetaTrader 5\terminal64.exe")


def stop(msg, code=1):
    print(msg); mt5.shutdown(); sys.exit(code)


if not mt5.initialize(TERM, timeout=60000):
    print("ERROR initialize", mt5.last_error()); sys.exit(2)
action = sys.argv[1] if len(sys.argv) > 1 else ""

if action == "status":
    t, a = mt5.terminal_info(), mt5.account_info()
    stop(f"connected={t.connected} trade_allowed={t.trade_allowed} server={a and a.server} balance={a and a.balance}", 0)

elif action == "prepare":
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
    req = {"symbol": sym, "volume": qty, "price": ref,
           "action": mt5.TRADE_ACTION_PENDING if price else mt5.TRADE_ACTION_DEAL,
           "type": (mt5.ORDER_TYPE_BUY_LIMIT if buy else mt5.ORDER_TYPE_SELL_LIMIT) if price
                   else (mt5.ORDER_TYPE_BUY if buy else mt5.ORDER_TYPE_SELL),
           "type_time": mt5.ORDER_TIME_DAY, "type_filling": mt5.ORDER_FILLING_RETURN,
           "comment": "genius"}
    chk = mt5.order_check(req)
    code = secrets.token_hex(3).upper()
    with open(PEND, "w") as f:
        json.dump({"req": req, "code_sha256": hashlib.sha256(code.encode()).hexdigest(),
                   "expires": time.time() + LIM["confirmation_seconds"]}, f)
    print(f"SUMMARY: {side} {qty:g} {sym} {'limit' if price else 'market ~'} {ref:.2f} | value ~ {value:.2f}")
    print("SIMULATION (order_check):", None if chk is None else (chk.retcode, chk.comment), mt5.last_error())
    print("CONFIRMATION CODE:", code, f"(valid {LIM['confirmation_seconds']} s)")
    stop("NOTHING WAS SENT", 0)

elif action == "send":
    if not os.path.exists(PEND): stop("BLOCKED: no prepared order")
    p = json.load(open(PEND)); os.remove(PEND)  # single use
    if len(sys.argv) < 3 or hashlib.sha256(sys.argv[2].upper().encode()).hexdigest() != p["code_sha256"]:
        stop("BLOCKED: invalid confirmation code")
    if time.time() > p["expires"]: stop("BLOCKED: confirmation expired, prepare again")
    if not mt5.terminal_info().trade_allowed: stop("BLOCKED: AutoTrading is disabled in the terminal")
    r = mt5.order_send(p["req"])
    print("RESULT:", None if r is None else r._asdict(), mt5.last_error())
    stop("END", 0)
else:
    stop(__doc__)
