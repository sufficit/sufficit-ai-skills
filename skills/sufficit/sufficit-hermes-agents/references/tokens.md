# Agent API tokens

Access tokens that let an agent (or integrations acting for them) call the
API. The deployed OpenAPI is the authority on issuance, scope and rotation.

## Policy

1. A token identifies one agent in one account: never share a token between
   agents or accounts, and never reuse a user's token for another purpose.
2. Issue only when the use case needs programmatic access; a human attendant
   who only uses the panel does not need one.
3. Treat the token as a secret at least as sensitive as a password: deliver it
   once, never echo it into logs, chats, summaries or committed files.
4. Delivering a token to a third party (another company, an external address)
   is a separate decision that only the authorizing user can make explicitly
   in text; issuing it does not authorize sending it.
5. Prefer rotation over long-lived tokens: discover the rotate/revoke
   operations and what each does to the previous token before using them.

## Flow

1. Read the agent's current token state when the API exposes it (existence,
   creation date — not the value).
2. Discover the issuance operation (search terms: `token`, `access token`,
   `api token`, `chatwoot token`).
3. Issue the token scoped to the confirmed agent and account; verify by an
   independent read that the agent has a token (existence only).
4. Deliver through the authorized channel; record account, agent and date
   without the value.
5. On suspicion of leakage: rotate or revoke first, report after — and say
   which operations the deployed API actually offered.

## Offboarding

Removing or suspending the agent does not necessarily revoke tokens: discover
the revoke operation and run it explicitly, then verify by reading the token
state again.
