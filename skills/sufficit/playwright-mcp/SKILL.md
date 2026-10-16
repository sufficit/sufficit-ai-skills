---
name: playwright-mcp
description: "Configure and use Playwright MCP as an optional Sufficit AI Genius browser automation path, with isolated --headless mode or --extension bridge mode. Desktop uses local stdio; mobile/tablet requires http to a hosted server. Manage registration directly with mcp_server_add, mcp_server_set_enabled, and mcp_server_remove. Use for Playwright, MCP Bridge, isolated scraping, or capabilities missing from native browser_* tools, such as network/console capture, PDF, multiple tabs, file upload, or accessibility snapshots."
---

# Playwright MCP and Playwright MCP Bridge

Genius already accesses the user's browser through its native force-installed MV3 extension: `browser_navigate`, `browser_get_page`, `browser_find`, `browser_click`, and `browser_type` (see `TOOLS-BROWSER.md`). This is the default path and needs no registration.

Playwright MCP is a second, optional path. Its `mcp__<server-name>__*` tools add a structured accessibility tree, simultaneous tabs, file upload, network/console capture, PDF export, and drag-and-drop.

Registration is self-service. Since 2026-09-28, agents can add, enable, disable, and remove MCP servers through `mcp_server_add`, `mcp_server_set_enabled`, and `mcp_server_remove`. When the user asks to connect Playwright, call `mcp_server_add` with the values in [references/setup.md](references/setup.md). Do not send the user through the registration UI unless those management tools are absent, typically in an older Genius build.

## Navigation modes

1. Isolated/headless (`--headless`): a separate Playwright process without the user's logins. It serves a similar purpose to Genius's internal `CdpBrowserToolset` (PuppeteerSharp, currently disabled by default), with richer tools. Use it for scraping or automated checks that must not touch real user tabs or sessions.
2. Browser bridge (`--extension`): attaches to a real Chrome/Edge desktop tab through the Chrome Web Store extension named "Playwright Extension" (manifest name: "Playwright MCP Bridge"). See [references/setup.md](references/setup.md). Use this alternative only when the task needs a capability absent from native `browser_*`. It always controls a desktop browser; Chrome mobile has no such extension, so this cannot bridge to the tablet or phone's own Chrome.

## Desktop and mobile transports

Genius mobile rejects MCP `stdio` connections with `MCP stdio is unavailable on mobile; use HTTP`.

- Desktop: register `stdio` with command `npx`. Genius starts Playwright locally on demand; no extra infrastructure is required.
- Mobile/tablet: there is no local process to start. Run Playwright MCP persistently on an always-on host (desktop, notebook, or Sufficit server) using `--port`, and register its address through `http`. See [references/setup.md](references/setup.md) for the live-validated endpoint and network-exposure precautions: the server has no built-in authentication.

## Determine connection state

- A `mcp__<server-name>__*` tool in the available tool list means the server is registered, connected, and ready. Do not ask for unnecessary reconnection.
- Missing tools can mean an unregistered or disabled server or a connection failure, such as missing Node/`npx`. Follow registration guidance rather than invoking Playwright through a shell on the user's behalf.
- A connected MCP server does not prove the browser extension is installed. The first bridge call can hang or fail if the extension is missing or has not been clicked in the target tab. Relay the tool's actual instructions rather than guessing; see [references/setup.md](references/setup.md).

## Missing tools

1. If `mcp_server_add` exists but no `mcp__playwright*__*` tool exists, register Playwright yourself using [references/setup.md](references/setup.md). Do not ask the user to navigate a registration screen. Check `connected`/`error` before reporting success.
2. If `mcp_server_add` itself is missing, the Genius build predates MCP self-management. Only then direct the user to the literal UI path `Genius → Extensões → Catálogo → Adicionar servidor personalizado`, using the same setup values, or suggest updating Genius.

Do not invent flags, run `npx` outside Genius to test on the user's behalf, or silently substitute native `browser_*` when Playwright is required. Explain the missing capability.

## Prefer the native browser when sufficient

Native `browser_*` is the default way to act in the real user browser: force-installed, no registration, and no additional extension. Use the Playwright bridge only for capabilities it adds. Use `--headless` for isolated scraping/checks that must not touch the user's real session.

## Reference

[references/setup.md](references/setup.md) covers exact registration fields, Node/`npx`, Windows, version pinning, clean stdout, hosted mobile HTTP endpoints, network security, the Chrome Web Store extension, and troubleshooting.
