---
name: meta-business
description: "Manage Sufficit's Meta Business Suite assets and permissions, including Instagram content and insights access, ad account roles, business users, and system users. Use the authenticated Meta Graph API when its contract covers the exact asset and operation. Use targeted Business Suite evidence otherwise."
metadata:
  version: "1.1.0"
---

# Meta Business (Business Suite / Business Manager)

## Choose the route for the asset

1. Identify the person, asset type, exact account, and requested access. Check the last confirmed state
   and keep any alternative the requester already authorized.
2. Use Graph API when an authenticated Meta tool or client exposes a verified operation for that asset.
   Check the service, Graph version, operation and credential scope before calling. Fleet and Sufficit
   API tools only cover their own services. A catalog match or a loaded skill establishes discovery,
   while a usable route requires the authenticated contract.
3. Use the Business Suite agent tab when the Meta API route is unavailable. Read the current tab
   before navigating. Use the element reference and verify any change with evidence from that same
   tab. A selected tab, an already-present result or a successful scroll receipt leaves the
   permission unverified.
4. Record an exhausted route with the concrete result and what must change to make a retry useful.
   After a failed full-page read, use a targeted read such as the person's asset details instead of
   fetching the same page again. When both routes are exhausted, use the authorized fallback or
   report the specific missing evidence. Resume there on a short follow-up such as “faça”.

## Instagram content and insights

- Keep the business role and the Instagram asset permission distinct. To confirm access, look for
  evidence that links the person, the specific Instagram account and the requested capabilities.
  A name in the page text and full control over the business are insufficient evidence for the
  effective permissions of a specific Instagram asset.
- With a verified Meta API route, read the exact asset assignment before any change and read it
  again afterward. Verify the provider's operation and permission names for Instagram. The
  `act_` route and ad-account tasks below belong to ad accounts.
- In Business Suite, inspect the person's assigned assets or the Instagram asset's person details.
  Use the row or card for the matched person and the exact handle. A name-only accessibility match
  does not identify the row's permissions, and `browser_find` matches actionable controls. When
  another structured read can resolve the ambiguity, pick the specific row, details control or
  container. Mark the task complete only with the linked permission evidence.
- If the requester authorized an insights export and assignment cannot be verified, switch to the
  export once its actual operation is available. Preserve the requested time range or post count
  and metrics. Report any unavailable metrics or blocked export with the precise reason.

## Read business and ad account state

- `GET /me/businesses` — businesses the token can see (id, name, verification).
- `GET /{business-id}/owned_ad_accounts` and `GET /{business-id}/client_ad_accounts`
  — ad accounts per business with `account_status`.
- `GET /act_{ad-account-id}/insights?fields=spend&date_preset=maximum` — which
  account actually has spend ("a que já veiculou anúncios"). An account with zero
  spend everywhere is not the historical one, regardless of what the UI lists first.
- `GET /{business-id}/business_users` — current people and their roles.
- `GET /act_{id}/assigned_users` — who is on the ad account today.

## Grant access to an ad account

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

## System user track when person invites fail

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
