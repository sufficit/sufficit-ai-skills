# HTTP tools

Base `https://fleet.sufficit.com.br/api/fleet/v1`, personal Fleet token of a human user of your company. Confirm
fields in the live OpenAPI. Agents and system users cannot create, change or test tools.

## Credential

`POST credentials?contextId={contextId}`

```json
{ "id": null, "expectedRevision": null, "name": "IXC API", "integration": "ixc", "kind": "basic",
  "description": "Usuário de API do IXC", "fields": { "username": "<IXC user id>", "password": "<IXC token>" } }
```

Kinds: `basic` (fields `username`, `password`), `token` (field `token`), `fields` (up to 16 named fields). Values are
never returned. To rotate, send the same `id` with the current `expectedRevision` and new `fields`.

## Tool definition

`PUT contexts/{contextId}/http-tools/{toolId}` (new `toolId` Guid, `expectedRevision: null` to create; to edit, send
the `revision` you read).

| Field | Rule |
|---|---|
| `name` | `a-z`, digits, `_`; 3–48 characters; what the agent sees (prefixed `http_` on voice) |
| `description` | what it does and when to use it, up to 1000 characters; the agent decides from this |
| `method` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| `baseUrl` | `https://` host and optional base path; no user, query or fragment |
| `pathTemplate` | appended path; `{{param}}` is URL-encoded |
| `query` | object name → template |
| `headers` | object of non-secret headers; `Authorization`, `Cookie`, `Host` and similar are refused |
| `body` | JSON template (not for GET/DELETE). A string that is exactly `"{{param}}"` becomes the typed value |
| `parameters` | up to 20: `{ name, type: string|number|integer|boolean, description, required, enum?, maxLength? }` |
| `credentialId` + `auth` | `{ kind: none }`, `{ kind: basic, field, passwordField }`, `{ kind: bearer, field }`, `{ kind: header, name, field }`, `{ kind: query, name, field }` — `field` names a credential field |
| `responseFields` | dotted paths kept from a JSON response (arrays are mapped); empty keeps everything |
| `timeoutSeconds` | 1–10 |
| `effect` | `read` or `write` |
| `enabled` | turn off without deleting |

Rules enforced by Fleet:

- Only public HTTPS addresses. Private, local and internal networks and redirects are refused.
- Parameters are data: they cannot change host, method or headers. Unknown or mistyped parameters are refused
  (`400` with the parameter name).
- Responses are cut to the selected fields and to 8 KB. Up to 60 calls per minute per tool.
- Every call is audited (tool, agent, status, duration), without the request or response content.

## Test, grant, publish

- `POST contexts/{contextId}/http-tools/{toolId}/test` `{ "parameters": { … } }` →
  `{ status, success, body, truncated, durationMs }`. `status: 0` means the call did not reach your system (network
  refused or timeout); `body` says why.
- `PUT agents/{agentId}/http-tools` `{ "tools": [ { "toolId": "…", "allowWrite": false } ] }` replaces the agent's
  list. `GET` reads it.
- Voice agents: run `POST agents/{agentId}/voice/publish` after granting, changing or revoking tools.
- `DELETE contexts/{contextId}/http-tools/{toolId}` only after removing it from every agent.

## Example: IXC customer lookup by CPF/CNPJ (read)

```json
{
  "name": "ixc_buscar_cliente",
  "description": "Busca o cliente no IXC pelo CPF ou CNPJ informado pela pessoa. Use antes de falar de contrato ou fatura.",
  "method": "POST",
  "baseUrl": "https://<seu-ixc>/webservice/v1",
  "pathTemplate": "/cliente",
  "headers": { "ixcsoft": "listar" },
  "body": { "qtype": "cliente.cnpj_cpf", "query": "{{documento}}", "oper": "=", "page": "1", "rp": "5" },
  "parameters": [ { "name": "documento", "type": "string", "description": "CPF ou CNPJ, com ou sem pontuação, como a pessoa disse", "maxLength": 18 } ],
  "credentialId": "<id da credencial IXC>",
  "auth": { "kind": "basic", "field": "username", "passwordField": "password" },
  "responseFields": [ "total", "registros.id", "registros.razao", "registros.ativo" ],
  "timeoutSeconds": 8,
  "effect": "read",
  "enabled": true,
  "expectedRevision": null
}
```

IXC searches are `POST` with header `ixcsoft: listar`; other tables follow the same pattern (`/cliente_contrato`,
`/fn_areceber`, `/su_oss_chamado`). Check the format of `query` (punctuation, zeros) with `test` before granting the
tool. A tool that opens a ticket uses `effect: "write"`, no `ixcsoft` header, and is granted with `allowWrite: true`.
