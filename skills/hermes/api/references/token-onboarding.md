# Connect your own Hermes account

Use when the personal Hermes credential is missing or invalid. First distinguish
missing metadata, an expired/revoked token (401), denied Vault access and insufficient
Hermes permissions (403). Do not replace a valid credential to solve a 403.

## Token page and personal scope

For the configured Genius production instance, the direct personal token page is
[Hermes — my access tokens](https://chatwoot.sufficit.com.br/app/profile/access-tokens).
Use the same path on the configured host for another instance; never send its token
to production. The current Hermes UI uses this separate page; on older versions
open [profile settings](https://chatwoot.sufficit.com.br/app/profile/settings) and
find **Token de acesso**. Verify the loaded UI before choosing a fallback. Local
Hermes source: `profile.routes.js`, `AccessTokensPage.vue` and
`accessTokens/AccessTokenOwnerView.vue` under dashboard settings/profile.

Use **personal** context, not the account-token/admin/installation section. Verify
that the signed-in Hermes user is the intended current user before saving. If the
identity cannot be established, ask which account to connect. Do not reuse another
operator's session, service credential, or the Sufficit API bearer.

## Prefer completing the authorized connection

When connecting the user's own Hermes account is authorized, use the host's
available browser tools to open that page in their existing session. Inspect the
actual schemas: an embedded browser and Chrome/Playwright may have different
cookie stores. Use the browser that actually holds the authorized session.

- If already signed in, retrieve an existing active personal token through the
  supported **show/reveal/copy** action. Do not choose **rotate/reset/revoke**.
  Newer Hermes lists tokens and reveals an existing one in a dialog; older Hermes
  may have a masked `access_token` field on the profile page. Follow the live UI.
- Prefer a secret-aware browser-to-Vault transfer or an executor that can retain
  the value in memory and call the discovered `vault_save` contract without
  printing it. Identity's personal destination is
  `personal/hermes/production/api-token`; omit shared `contextId`. Inspect the
  tool's actual naming convention, rather than adding `personal/` twice.
- Ordinary page snapshots, screenshots, clipboard reads and `browser_get_page`
  can disclose a revealed token into tool output. Do not reveal/copy into those
  tools and claim the transfer is secret-free. If the available tools cannot
  transfer the secret safely, use the guided path below instead of exposing it.
  Do not send the token in chat, URLs, shell literals, logs or committed files.
- Login, password, MFA or consent pages require the user to complete that step in
  the browser; give the direct link and the specific action needed. Do not claim
  the browser is signed in because another service is authenticated.
- If no active token exists, explain that creation is needed and obtain authority
  for creating one unless already included in the connection request. Never
  silently rotate an existing token to make it visible. Respect host approvals.

After saving, read Vault metadata (`vault_get_info`) and run
`hermes_connection_test`, or read the authenticated profile through the discovered
API. Metadata confirms storage; only a successful authenticated call confirms the
connection and available account memberships. Do not resolve plaintext just to
check storage. Resume the original authorized task using its saved resource IDs;
connecting alone does not authorize customer messages.

## Guided path when user interaction or safe transfer is needed

Discover `vault_prepare_entry` and call it with
`name: "hermes/production/api-token"` for the personal production credential. This
prepares a link, not a saved secret. Its `saved: false` describes this call, not
whether a credential was previously stored: `exists: true` and `status: Active`
indicate an existing entry. Do not tell the user their active entry is unsaved or
ask them to replace it for a hypothetical tutorial. Use `vault_get_info` when the
actual state matters. Present the exact returned URL as a clickable link; never
invent an Identity URL or replace it with just a secret path.

The reply must include both destinations and the actual remaining action, e.g.:

> Abra [seus tokens no Hermes](https://chatwoot.sufficit.com.br/app/profile/access-tokens)
> e entre na sua conta se for solicitado. Em um token pessoal ativo, use a opção de
> mostrar/copiar. Depois abra **Salvar no Vault** (usar aqui o link retornado pela
> ferramenta), cole o token e salve. Não cole o token neste chat. Avise quando salvar
> para eu conferir a conexão e continuar.

Adapt the words to the observed UI and blocker. If token creation is required,
say so rather than pretending every version has a token ready to copy. If Vault
link preparation fails, report that specific failure and retain the Hermes link;
do not label a fabricated or unavailable link as working. After the user's return,
verify metadata and authentication before proceeding. Preserve completed billing,
contact and conversation work; do not reissue a bill while reconnecting Hermes.
