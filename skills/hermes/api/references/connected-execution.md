# Connected execution when a Hermes tool is missing

Use this when a plugin lacks an operation or attachment parameter. Missing wrappers
are a discovery problem, not proof that the account cannot perform the operation.

1. Discover the exact tool through the host catalog and inspect its schema. Use it
   if it covers the operation. A skill explains procedures; loading it does not
   itself execute an API call or make a new tool available.
2. Identify the configured Hermes host. Genius production uses
   `https://chatwoot.sufficit.com.br`; do not substitute a development host or the
   upstream `servers` value from Swagger. Fetch `/api` and
   `/swagger/swagger.json` using available HTTP, browser read or shell tools.
   Search locally for the needed operation and resolve its request-body schemas.
3. Discover the connected Identity Vault tools. Inspect metadata for
   `personal/hermes/production/api-token` in the current user's personal vault.
   A missing environment variable says nothing about this entry. A prior successful
   `hermes_connection_test` already proves the plugin resolved this credential.
4. Prefer a host HTTP/secret bridge that resolves the Vault reference at execution
   time without returning the value to the conversation. Inspect the actual tool
   schema: `vault:` is not automatically supported in arbitrary headers or shell.
   When no such bridge exists, use the available authorized Vault resolution tool
   according to its contract. Identity's `vault_resolve` requires `name` and
   `confirmPlaintext: true` and returns plaintext; do not describe that path as
   secret-free. Respect the host's disclosure/confirmation policy. Keep the value
   out of replies, logs, files committed to Git, command-line literals and URLs.
   Where tool orchestration can retain the result in memory, pass it directly to
   the HTTP client without printing it. Do not ask the user to paste a stored token.
5. Call the discovered profile operation with `Authorization: Bearer <resolved
   token>` against the configured host. Use its account memberships and the
   contact's inbox/channel evidence for subsequent calls. Do not reuse the
   Sufficit API bearer as a Hermes credential or forward auth across hosts.
6. Execute the authorized operation with the discovered contract, then read its
   result. After an ambiguous write response, reconcile state before retrying;
   never create another attendance or send another message just because a call timed out.

## Shell host matters

Inspect shell help/platform before executing a script. Genius's Windows shell uses
`cmd.exe`: `env | grep` and bare `Get-ChildItem` do not run there. Invoke PowerShell
explicitly, e.g. `powershell.exe -NoProfile -NonInteractive -Command "$PSVersionTable.PSVersion"`,
or use `pwsh` only after checking availability. Prefer a script file for complex
quoting. An interpreter error means the command did not run; correct the interpreter
before judging network access. Never probe by printing all environment values.

## Evidence required for a blocker

Report the attempted step and the actual response: document fetch failure, missing
Vault entry, resolution denied, authenticated HTTP 401/403, invalid payload, or no
available executor capable of using the credential. Try the relevant supported
alternative before concluding; do not cycle broad catalog queries indefinitely.
A 401/403 is not permission to change identity or bypass access controls. If the
host truly cannot resolve/pass a stored credential, say which bridge is absent,
not that the user has no token. Preserve completed resource IDs and pending steps.
