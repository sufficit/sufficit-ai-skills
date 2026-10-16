---
name: asaas-connection
description: "Securely connect and test the ASAAS production account using the key stored in the user's Sufficit Identity Vault and the asaas_connection_test tool in Sufficit AI Genius. Use when the user asks to connect, continue, check, or test ASAAS. The test is read-only and creates no charge, payment, or customer."
---

# ASAAS production connection

Use this guidance when the user asks to connect, continue, verify, or test the real ASAAS account.

## Credential

- The canonical reference is `personal/asaas/production/api-key` in the user's Sufficit Identity Vault.
- Never ask the user to paste the key into the conversation. Never include it in tool arguments, commands, scripts, or files. Never display headers, tokens, the provider response body, or account data.
- If the entry is missing, use the Genius Vault preparation tool (`vault_prepare_entry`) to prepare exactly this reference. Give the user the secure screen to paste and save the key. Once the user says it is saved, test the connection without asking for the secret again.

## Connection test

Discover and use `asaas_connection_test`. This tool resolves the key inside the trusted host, makes a single `GET https://api.asaas.com/v3/myAccount/status` request, and neither follows redirects nor reads the response body. It creates no charge, payment, or customer and does not modify the account.

Consider the test complete only when the result reports `connected: true`, `authenticated: true`, HTTP 200, and `writesPerformed: false`. Report this in plain language.

On failure, identify the returned code and follow [references/connection-test.md](references/connection-test.md). Do not try another endpoint, automatically retry non-retryable failures, or perform a financial operation to "confirm" connectivity.

## Tool unavailable

If `asaas_connection_test` is unavailable, the ASAAS plugin is disabled or this version of Genius does not provide it yet. Ask the user to enable the ASAAS plugin in Genius extensions or update the application. Do not bypass the tool by calling the ASAAS API through a shell, script, or another tool: the production key must not enter the prompt.
