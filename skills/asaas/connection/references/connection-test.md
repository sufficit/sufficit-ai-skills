# Connection test ASAAS

The `asaas_connection_test` tool does not accept arguments. It resolves `personal/asaas/production/api-key` in personal Vault, injects the key only into the `access_token` header of a request made by the trusted host and never returns the key, the provider response body or account data.

## Success result

| Field | Value |
| --- | --- |
| `connected` | `true` |
| `authenticated` | `true` |
| `provider` | `asaas` |
| `environment` | `production` |
| `check` | `myAccount/status` |
| `method` | `GET` |
| `httpStatus` | `200` |
| `credentialReference` | `personal/asaas/production/api-key` |
| `writesPerformed` | `false` |

Inform the user, in simple language, that the account is connected and that the test has not changed anything in the account.

## Failure codes

| Code | Meaning | Action |
| --- | --- | --- |
| `asaas_vault_sign_in_required` | The user is not logged into Sufficit Identity. | Ask to enter the Sufficit account and repeat the test. |
| `asaas_key_missing` | Entry does not yet exist or is empty in Vault. | Prepare `personal/asaas/production/api-key` with Vault safe screen and repeat after the user saves the key. |
| `asaas_key_invalid` | The saved key has invalid format for HTTP authentication. | Ask the user to generate a new key in the ASAAS panel and save to the same Vault input. |
| `asaas_credential_rejected` | ASAAS rejected the key (HTTP 401/403). | The key is wrong or has been revoked; ask for a valid key, save to Vault and repeat once. |
| `asaas_provider_unavailable` | ASAAS responded, but did not complete the test. | Provider failure; inform the user and, if checked retryable, retest after a wait. |
| `asaas_transport_failed` | The production API was not achieved. | Network problem; check the connection and repeat. |
| `asaas_timeout` | The test exceeded the time limit. | Repeat once; if it persists, treat as unavailability. |
| `asaas_vault_timeout` | Access to Vault exceeded the time limit. | Repeat once; if persistent, treat as unavailability of Identity. |
| `asaas_vault_unavailable` | Vault couldn't be accessed. | Unavailability of Identity; try again later. |

Failures marked as retryable in the result can be attempted again with parsimony: a new attempt, waiting for an instant. Non-retryable failures require user action before any new call.

Never use a writing operation — create billing, payment, customer or any change — to diagnose the connection.
