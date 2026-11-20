---
name: meta-business
description: "Operate Sufficit assets on Meta (Facebook) Business Suite and Business Manager: businesses, ad accounts, pages, people and permissions. Use to grant or revoke a person's access to an ad account, invite or remove business users, resolve which ad account actually has spend, diagnose 'user cannot be added to business' and permission-save failures, and to set up system users with tokens for API-first operation. Prefers Graph API over clicking the Meta UI; the browser is the fallback. Version 1.0.0."
metadata:
  version: "1.0.0"
---

# Meta Business (Business Suite / Business Manager)

Grant and manage access to Sufficit's Meta assets with the Graph API first and the
browser only as fallback. Most breakage seen in the wild is UI automation failing
on overlays and tooltips while a documented API call existed all along.

## Decision order

1. **Read state via Graph API** before asking anyone anything. Which businesses
   exist, which ad accounts they hold and which one has spend are facts, not
   user questions.
2. **Mutate via Graph API** when the authenticated context allows it (invite a
   user, assign an ad account with tasks, promote to admin).
3. **System user + token** when person invites are refused by Meta or when
   operating headless (`business_management` scope, token kept in the Vault).
4. **Browser UI (Genius extension)** only for what the API genuinely cannot do,
   and after reading state with `browser_get_page`. Use the element `reference`,
   never positional `nth-of-type` selectors; every click that changes state must
   carry `wait_for_text`/`wait_for_selector`.

Escalation rule: after 2–3 failed UI attempts on the same step, stop clicking and
return to the API/catalog search. The UI is the fallback, not the default.

## Reading state (facts, never questions)

- `GET /me/businesses` — businesses the token can see (id, name, verification).
- `GET /{business-id}/owned_ad_accounts` and `GET /{business-id}/client_ad_accounts`
  — ad accounts per business with `account_status`.
- `GET /act_{ad-account-id}/insights?fields=spend&date_preset=maximum` — which
  account actually has spend ("a que já veiculou anúncios"). An account with zero
  spend everywhere is not the historical one, regardless of what the UI lists first.
- `GET /{business-id}/business_users` — current people and their roles.
- `GET /act_{id}/assigned_users` — who is on the ad account today.

## Granting a person access

1. Resolve the target ad account and the wanted task level with the requester.
   Tasks on ad accounts: `MANAGE` (full), `ADVERTISE` (create/edit campaigns —
   the usual "gerenciar campanhas"), `ANALYZE` (read-only).
2. Ensure the person is in the business:
   `POST /{business-id}/business_users` with `email` and `role` (`EMPLOYEE` for
   partial access; `ADMIN` for full). This replaces the whole "Convidar pessoas"
   4-step dialog.
3. Assign the asset: `POST /act_{ad-account-id}/assigned_users` with
   `user` (business user id or email-scoped id) and `tasks=["ADVERTISE", ...]`.
4. Verify by reading `assigned_users` back; never trust the invite screen.
5. The invited person must accept by email; the accept step is theirs.

## System user track (when person invites fail)

Meta refuses some person invites for account-state reasons no admin can fix
("O usuário não pode ser adicionado à empresa"). The durable route for a company
that needs to operate its own assets:

1. Admin creates a system user in Business Settings → System Users
   (`POST /{business-id}/system_users`, admin-only, or in the UI once).
2. Grant assets to the system user (`assigned_users` with tasks, same as above).
3. Generate a token with `business_management` (+ `ads_management` as needed):
   `POST /{system-user-id}/access_tokens`. Store it in the Sufficit Vault
   (`vault_save`); never paste it in chat.
4. From then on, grants like the above run over this token without any person's
   personal account being the bottleneck.

## Error taxonomy

| Graph/UI error | Meaning | Next step |
| --- | --- | --- |
| `(#10) Application does not have permission` | token lacks scope | use system-user token or extend scopes |
| `(#100) nonnumeric ID` or `invalid target | wrong id type (ad account needs `act_` prefix, business user needs scoped id | re-read state, resolve the right id |
| "O usuário não pode ser adicionado à empresa" | Meta-side block on that person's account | do not retry the same invite; switch to another email or the system-user track |
| "Houve um problema ao salvar suas alterações" (UI) | session/permission save failure | re-read, then prefer API; a different browser won't fix a Graph refusal |
| `(#2901) permission denied on asset` | actor lacks the task on that asset | escalate to a business admin or system user |
| 2FA / biometric / "chave de acesso" prompts | owner-only device verification | stop; the account owner completes it. Never automate, never request the code as a tool input |

## Hard limits

- Never automate password recovery or enter another person's password.
- Never bypass 2FA/biometric; wait for the account owner.
- Tokens only in the Vault; never in the conversation, URL or logs.
- Never call an endpoint from memory without confirming it on the live version —
  check the Graph API version in use and prefer `GET` dry-runs before writes.
