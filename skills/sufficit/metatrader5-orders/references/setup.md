# Environment setup

## Windows (user's own PC)

- Install the broker's MT5 (for XP Investimentos: the XP installer from the MQL5 CDN,
  `https://download.mql5.com/cdn/web/xp.investimentos.cctvm/mt5/xpmt5setup.exe`).
- Install 64-bit Python and `pip install MetaTrader5`.
- Python must run under the same Windows user as the terminal.

## Linux / cloud (Wine)

Lessons from the first deployment:

- Use a **64-bit Wine** build (a portable `wine-*-amd64-wow64` tree works) with its own
  prefix: `WINEPREFIX=<dir>/prefix`, `WINEDEBUG=-all`.
- Run the terminal headless with **Xvfb** (`Xvfb :99 -screen 0 1280x800x24 &`,
  `DISPLAY=:99`). `xvfb-run` per command also works but keep one display for terminal and
  Python so IPC can attach.
- The official Python **32-bit installer fails** under a 64-bit-only Wine (`kernel32.dll`).
  Use the 64-bit embeddable package from NuGet
  (`https://www.nuget.org/api/v2/package/python/<version>`, extract `tools/` to
  `C:\Python312`).
- `pip` inside Wine may hang downloading. Download wheels on Linux from PyPI
  (`MetaTrader5` `cp312-win_amd64` and `numpy` `cp312-win_amd64`) and install offline:
  `wine C:\Python312\python.exe -m pip install --no-index --find-links <wheels> MetaTrader5`.
- First terminal start recompiles programs and may self-update for several minutes;
  give it time before attaching from Python.
- Shell commands that run longer than about 8 minutes may be killed by the environment;
  split work into background scripts.
- Never put the literal `terminal64.exe` in an inline `pkill -f` command: it matches and
  kills your own shell (exit 143). Put kill logic in a separate script and use
  `pgrep -f 'terminal64\.exe'` skipping `$$`.
- Terminal logs are UTF-16LE: `iconv -f UTF-16LE -t UTF-8 <logs>/<date>.log`.

## First login without typing the password

```bash
umask 077
# password file written by vault_resolve, never echoed
{ printf '[Common]\r\nLogin=<login>\r\nPassword='; tr -d '\r\n' < .pw;
  printf '\r\nServer=<server>\r\nKeepPrivate=1\r\n'; } > "$WINEPREFIX/drive_c/login.ini"
wine terminal64.exe '/config:C:\login.ini' &
sleep 80; rm -f "$WINEPREFIX/drive_c/login.ini" .pw
```

Quote the `/config:` argument as one token; a broken path gives `cannot load config`.

## Read-only Python test

```python
import MetaTrader5 as mt5
ok = mt5.initialize(r"C:\Program Files\<broker MT5 folder>\terminal64.exe", timeout=60000)
print(ok, mt5.last_error())
a = mt5.account_info(); print(a.login, a.server, a.balance, a.trade_allowed)
mt5.symbol_select("PETR4", True); print(mt5.symbol_info_tick("PETR4"))
mt5.shutdown()
```

On B3, fractional lots use the `F` suffix (`PETR4F`, 1 share minimum); standard lots are
usually 100 shares.
