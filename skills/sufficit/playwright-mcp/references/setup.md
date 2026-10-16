# Playwright MCP registration in Genius

Genius supports custom MCP servers without plugin or configuration file editing. Since 2026-09-28, the agent registers servers directly by calling `mcp_server_add` — the tables below (`Campos do cadastro`) map directly to the JSON call arguments: `Nome`→`name`, `Transporte`→ `transport`, `Comando`→`command`, `Argumentos`→`arguments` (array), `Variáveis de ambiente`→`environment` (object), `Endpoint`→`endpoint`. Example for desktop isolated mode:

```json
{
  "name": "playwright",
  "transport": "stdio",
  "command": "npx",
  "arguments": ["-y", "@playwright/mcp@<pinned-version>", "--headless"],
  "environment": { "NPM_CONFIG_LOGLEVEL": "silent" }
}
```

After calling `mcp_server_add`, check out `connected`/`error` on return — do not report success merely because the call raised no exception. To enable, disable or remove a server already registered (by the user or yourself before), use `mcp_server_set_enabled` (`server`, `enabled`) and `mcp_server_remove` (`server`) — `server` accepts the id or name.

If these three tools are not in your list, this version of Genius precedes this functionality: only in this case guide the manual registration in Extensions → Catalog → Add custom server using the same fields in the tables below.

Transport depends on the device: desktop uses `stdio`; mobile/tablet requires `http` to a hosted server. See [mobile/tablet registration](#genius-mobiletablet-registration-by-http).

## Desktop: registration `stdio`

### Prerequisite: Node.js

`npx` comes with Node.js. Without Node installed on the host where Genius runs, the server process does not start (typical error when trying to connect: `spawn npx ENOENT`). In this case, guide the user to install Node.js LTS and reopen Genius before attempting again.

Windows: `.cmd` from `npx` is not resolved in the same way as an interactive shell when the process is created without invoking a shell. Use `npx.cmd` as command, not `npx`.

### Registration fields

| Field | Isolated/silent | Bridge |
| --- | --- | --- |
| Name | `playwright` | `playwright-bridge` |
| Transport | `stdio` | `stdio` |
| Command | `npx` (Windows: `npx.cmd`) | `npx` (Windows: `npx.cmd`) |
| Arguments | `-y`, `@playwright/mcp@<pinned-version>`, `--headless` | `-y`, `@playwright/mcp@<pinned-version>`, `--extension` |
| Environment variables | `NPM_CONFIG_LOGLEVEL=silent` | `NPM_CONFIG_LOGLEVEL=silent` |

Use different names for both entries: the tools are prefixed `mcp__playwright__*` and `mcp__playwright-bridge__*`, which makes it clear which one is being called. Before constructing the arguments, confirm the exact name of the flags in the installed version (`npx @playwright/mcp@<version> --help`) — they can change between package versions.

### Why pin the version instead of `@latest`

The `stdio` transport is JSON-RPC line-by-line over `stdout`: any extra text that the `npm`/`npx` writes to `stdout` (refresh notice, version resolution) corrupts the message frame and drops the connection at the first exchange. `@latest` makes `npx` see the npm registry at each start — slower and more likely to noise in `stdout`. A fixed version (`@0.x.y`) avoids this query and keeps the process quiet. `NPM_CONFIG_LOGLEVEL=silent` is the second noise protection layer.

Live validation on 2026-09-28 used `@playwright/mcp` 0.0.82, then the stable version. Check the current version with `npm view @playwright/mcp version`. Running the locally installed server without `npx`, the `initialize` handshake completed and `tools/list` returned 25 tools, compared with five native Genius `browser_*` tools. Additional capabilities included `browser_console_messages`, `browser_handle_dialog`, `browser_emulate_media`, `browser_evaluate`, `browser_file_upload`, and `browser_drop`. A real headless `browser_navigate` call to `github.com/sufficit` returned the expected result. No non-JSON-RPC lines appeared on `stdout`.

### Isolated x bridge — do not confuse the two

`--headless` starts an isolated Chromium that Playwright itself downloads and manages (the first run may take time because of the download) — no login, no cookies, no user history. `--extension` does not start any browser: the server expects the Chrome Web Store extension to connect to a tab that the user is already using, with its actual session.

## Genius mobile/tablet: registration by `http`

Why can't you copy the `stdio` registry from the desktop: Genius rejects `stdio` in mobile per design — there is no local process for the app to start inside Android/iOS. The Genius agent running on the tablet only sees Playwright if there is a Playwright server MCP already running persistently on some host always connected and reachable over the network — the user's desktop, a notebook, or a Sufficit server. This host starts the process with Node/`npx`; the tablet only connects to `http`.

### Start the server in `http`/SSE mode

In the host that will always stay on (e.g. `systemd`, or any process supervisor — it is not a command to run manually every time):

```bash
npx -y @playwright/mcp@<pinned-version> --headless --isolated \
  --port 8931 --host <internal-vpn-ip>
```

Live-validated in 2026-09-28: Up with `--port`, the process prints on the start (one time at the beginning — it is not continuous noise in the `stdout` of the protocol):

```
Listening on http://localhost:8931
Put this in your client config:
{
  "mcpServers": {
    "playwright": { "url": "http://localhost:8931/mcp" }
  }
}
For legacy SSE transport support, you can use the /sse endpoint instead.
```

I tested the full HTTP handshake against this endpoint (the same as `HttpClientTransport` Genius speaks — Streamable HTTP with fallback SSE, `AutoDetect`): `initialize` returned `Mcp-Session-Id` to the response header, `tools/list` brought the same 25 test tools by `stdio`, and a real `browser_navigate` against `github.com/sufficit` worked. The `/mcp` endpoint is the correct one for registration in Genius; `/sse` exists only as compatibility with older MCP clients.

### Registration fields in Genius mobile

| Field | Value |
| --- | --- |
| Name | `playwright` (or `playwright-bridge` if this host also has `--extension` — see below) |
| Transport | `http` |
| Endpoint | `http://<internal-vpn-ip>:8931/mcp` |

No command, no arguments, no environment variable — all of this has already been decided by the time of starting the process in the host. Genius mobile only needs URL. Via `mcp_server_add`, the call is only:

```json
{ "name": "playwright", "transport": "http", "endpoint": "http://<internal-vpn-ip>:8931/mcp" }
```

### Network access: no built-in authentication

Checked in the `--help` package: no token flag, bearer or password for `http` transport. Whoever reaches `<host>:<port>/mcp` over the network controls a real browser without asking for anything — including `browser_evaluate` (executes arbitrary JavaScript on the page) and `browser_file_upload`. `--allowed-hosts`/`--allowed-origins` restrict where the browser can navigate, not who can talk to the server — they are not access control to MCP.

Never bind on `0.0.0.0` on a network exposed to the internet or shared with those who should not have that control. Bind only on the host VPN/Tailscale interface (not `0.0.0.0` loose), and register on the tablet the IP of this VPN — not a public IP. Treat the full URL (host:port) as a password-equivalent secret: whoever has it controls that host's browser.

### Bridge mode (`--extension`) from mobile

If the host that runs the `--port` server also uses `--extension` (instead of `--headless`), the tablet can trigger the desktop browser of this host via Playwright MCP — but it remains the desktop browser that is controlled, never Chrome of the tablet itself (Chrome mobile does not run extensions). Make this clear to the user before setting up: "bridge on mobile" means "the tablet tells the computer to open and touch his browser", not "the tablet gets its own Playwright browser".

## Chrome Web Store Extension (bridge mode only)

1. The user installs the extension in the Chrome Web Store: `https://chromewebstore.google.com/detail/mmlmfjhmonkocbjadbfplnigmagldckm`. Two names, the same extension (referred to live in 2026-09-28): the store listing shows "Playwright Extension" — that's the name that appears in the page title and the "Add to Chrome" button. Once installed and connected, the Chrome warning bar itself ("this extension is debugging the browser") shows the internal name of the manifest: "Playwright MCP Bridge". If the user says he only found "Playwright Extension" in the store, it's the same thing — don't send for "MCP Bridge" again.
2. Unlike Genius's own extension (this is force-installed automatically by managed policy — see `TOOLS-BROWSER.md` in the `sufficit-ai-genius` repository), this extension does not connect on its own: the user needs to click on its icon in the tab he wants to share with each new tab the agent uses.
3. Without this click, the first bridge-side tool call (e.g. navigate) is pending or returns an error asking for the connection — it is not a problem in the registry of the MCP server itself.
4. Sign that it is working: the Chrome bar showing "'Playwright MCP Bridge' started debugging this browser" (or equivalent text in Portuguese) in the shared tab is the expected behavior, not a security alert or malicious extension signal — it is Chrome itself warning that an extension is with the API debugger attached to the tab, exactly the mechanism that allows bridge mode to work.

## Symptoms → causes → action

| Symptoms | Probable cause | What to do |
| --- | --- | --- |
| No `mcp__playwright*__*` tool in the list | Server not registered, disabled, or failed to connect | Check Extensions → Integrations → MCP the status/error of the server; if the error cites `spawn ... ENOENT`, Node/`npx` is missing in the PATH of the host running Genius |
| Tools present, but the call hangs or fails in bridge mode | Extension not installed, or installed but not clicked on target tab | Orient installation (link above) and icon click on the right tab |
| Tools present, but the call hangs or fails in mode `--headless` | First Chromium download from Playwright is still ongoing, or Chromium system dependencies are missing from the host (common on minimum Linux) | Wait for the first run to end; if you persist on Linux, there are missing system libraries that Chromium requires |
| Connection falls right after registration | `stdout` noise (version `@latest` without `NPM_CONFIG_LOGLEVEL`) corrupting the `stdio` frame | Switch to fixed version and add the environment variable from the table above |
| `stdio` register works on desktop but the same registration fails on Genius mobile | Mobile does not support `stdio` — expected error, not configuration failure | Register mobile by `http` against a `--port` server already running on host always connected (see mobile/tablet section above); never try `stdio` in mobile app |
| Genius mobile does not connect on `http` server | Server is not running, wrong port/IP, blocking firewall, or the server is bounded only in `localhost` of the other host (unreachable over the network) | Confirm that the process is active in the host, that `--host` is not `localhost`/`127.0.0.1` (needs to be the network interface/VPN), and that the port is released only to VPN — never open to the internet |

Network/spawn failures can be tried again with a moment of waiting. Failures that depend on user action (install Node, install extension, click icon) do not resolve by repeating the call — explain the missing step before trying again.
