---
name: asaas-connection
description: "Securely connect and test the ASAAS production account using the key stored in the user's Sufficit Identity Vault and the asaas_connection_test tool in Sufficit AI Genius. Use when the user asks to connect, continue, check, or test ASAAS. The test is read-only and creates no charge, payment, or customer."
---

# ASAAS production connection

Use this guidance when the user asks to connect, continue, verify, or test the real ASAAS account.

## Optional native plugin in Genius

Discover the required native tool first. If it is absent and `plugin_runtime` is
available, call `action: "list"`, then `action: "install", id: "sufficit.asaas"`
from the compatible official signed catalog. Re-query the tool catalog after
installation; the tools load on this device in the current session. Reuse an
already available plugin. A deliberately disabled plugin needs re-enabling through
Genius's plugin controls; preserve the user's setting. An older app without the
manager, or a catalog without a compatible package, needs an app update to install
native packages. Installation does not authorize
provider operations or moving the task to another computer.

## Credential

- The canonical reference is `personal/asaas/production/api-key` in the user's Sufficit Identity Vault.
- Never ask the user to paste the key into the conversation. Never include it in tool arguments, commands, scripts, or files. Never display headers, tokens, the provider response body, or account data.
- If the entry is missing, use the Genius Vault preparation tool (`vault_prepare_entry`) to prepare exactly this reference. Give the user the secure screen to paste and save the key. Once the user says it is saved, test the connection without asking for the secret again.

## Connection test

Discover and use `asaas_connection_test`. This tool resolves the key inside the trusted host, makes a single `GET https://api.asaas.com/v3/myAccount/status` request, and neither follows redirects nor reads the response body. It creates no charge, payment, or customer and does not modify the account.

Consider the test complete only when the result reports `connected: true`, `authenticated: true`, HTTP 200, and `writesPerformed: false`. Report this in plain language.

On failure, identify the returned code and follow [references/connection-test.md](references/connection-test.md). Do not try another endpoint, automatically retry non-retryable failures, or perform a financial operation to "confirm" connectivity.

## Tool unavailable

If `asaas_connection_test` remains unavailable after the native-plugin discovery above, report the installation/disabled-state failure and use the Genius plugin controls or application update as indicated. Do not bypass the tool by calling the ASAAS API through a shell, script, or another tool: the production key must not enter the prompt.
