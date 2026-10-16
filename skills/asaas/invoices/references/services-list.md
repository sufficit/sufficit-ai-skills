# Municipal services ASAAS

The `asaas_services_list` tool consults `/v3/fiscalInfo/services` — the municipal service catalogue that the city provides for the production account. Read-only (`writesPerformed: false`).

## Making an invoice does not create service — because the issue omits municipal fields

In the flow of this skill the issue does not send `municipalServiceId` or `municipalServiceCode`, so an invoice request never produces new registration. The skill never invents code. If the catalogue does not have what the invoice serves, the decision is of the user (another existing service, or the correct code with the accounting).

Guarantee comes from omission, not from provider protection. Controlled tests in sandbox account (2026-09-23) showed that when municipal fields are sent, scheduling has a real side effect on account service registration:

- send only `municipalServiceCode` created new entry with the same name as the code itself (e.g. `01.01.01` without the official text of the catalog);
- reuse an existing `municipalServiceName` with another code changed the association retroactively, including for already scheduled invoices;
- the identity of the registration is the name, not the code: two distinct names with the same code appear as two records in the panel.

Therefore, the operational rule of omitting is also a protection of registration, and not just a convenience. Entries created like this only remove through the panel.

## Creating on explicit user request

Creating service is a separate and legitimate act when the user asks for it directly. The public API of the ASAAS, however, exposes only the reading of this catalogue — there is no `POST`/`PUT`/`DELETE` of municipal service (`POST` on this route answered HTTP 404 in the test of 2026-09-23). In this case, guide the panel (`Notas Fiscais › Configurações › Serviços › Adicionar Serviço`) and offer to list existing services before, to avoid duplicates. Do not treat the application as prohibited, and do not simulate creation.

Do not use invoice scheduling as a registration shortcut. It even produces new input (see previous section), but emits a real tax document, does not allow to reliably define ISS and leaves residue removable only by the panel. It's not a disguised creation API.

There is also no public endpoint to edit, delete, set default or enable/disable service: these actions exist only in the panel. Don't promise to do it by tool.

## Arguments

| Argument | Type | Default | Rules |
| --- | --- | --- | --- |
| `description` | string | (None) | Filter by service name/code (e.g. `1.01`, `sistemas`); up to 80 characters. Matches any substring, not only the prefix: `07.` also brings `01.07.01` and `04.07.01`. |
| `limit` | integer | `10` | Between 1 and 30. |
| `offset` | integer | `0` | Not negative. See the pagination trap below. |

## Page: `offset` works as page number

Tests from 2026-09-23 showed that the real displacement is `offset × limit`, not the index of the first element:

- `limit=1&offset=5` and `limit=5&offset=1` returned the same item;
- with `limit=100`, pages `0`, `1`, `2` and `3` covered the 338 items (100+100+100+38) and `offset=4` came empty;
- therefore `limit=5&offset=100` returns empty list with `hasMore: false`, despite `totalCount: 338`.

Add `offset += limit`, the usual standard, skips most of the catalog and ends without error. Step forward from 1 to 1 and stop when `hasMore` for `false`. If a service appears absent, suspect pagination before claiming it does not exist — and prefer the `description` filter to scan pages.

Behavior observed in this endpoint; confirm before assuming the same in others. The plugin can normalize this: the above rule describes the raw API.

## Success result

`provider: "asaas"`, `environment: "production"`, `note` (remember: issuing invoice never creates service or specifies one), `query`, `totalCount`, `hasNext`, `services[]` and `writesPerformed: false`.

Each service brings: `id`, `description` (code + name, up to 200 characters) and `issTax`. `id` only turns `municipalServiceId` when the user explicitly chooses that service for the invoice; in the normal flow of this account the issue does not send the municipal fields.

Details observed in the fields (sandbox, 2026-09-23):

- `id` is a sequential internal key, unrelated to the tax code (do not derive or guess it from the code).
- `description` brings `NN.NN.NN - Texto.` — this is the exact value that should go on `municipalServiceName` when the user chooses the service. Never construct the name yourself.
- `issTax` is the catalog reference rate and came `0.0` on all items of the account tested: do not present it as the actual invoice tax rate.
- `municipalServiceId` alone is refused in scheduling (HTTP 400, `invalid_action`: "O campo municipalServiceName deve ser informado" (the municipalServiceName field is required)), even with valid id. When using id, send the id + name pair.

The municipal catalog is not the account’s registered-service list. This endpoint lists what the city provides (hundreds of items); the Tax Invoices screen › Settings › Services shows only the services saved from the account, which is another set. Do not describe one as being the other when answering the user.

## National Portal Accounts

Accounts issued by the National Portal do not receive the municipal list by API. In this scenario the query fails with provider error (e.g. "unenabled municipal service code") — it is not your fault. The official guidance ([Guide](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico)) is to obtain the code on the National Portal or with accounting and use it on `municipalServiceCode` when a specific service is needed. In the operational rule of this account the issue goes on without the municipal fields — the service details are auto filled by the registration; if the provider refuses, present the real reason and report to the team. Never guess code.

## Failure codes

| Code | Action |
| --- | --- |
| `asaas_services_invalid_arguments` | Fix filters; nothing has been called. |
| `asaas_services_unexpected` | Response out of format; try once. |
| `asaas_provider_unavailable` | Can be account without municipal list (Portal Nacional) — deal with the user, do not repeat in loop. |
| Other failures (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_timeout`, `asaas_transport_failed`) | Standard flow of ASAAS skills. |
