# IXC request mechanics

Every IXC Provedor installation exposes the same REST webservice. Each table (the IXC docs call them
"formulários") is a resource under one base URL. This file covers the request shapes shared by every table; the
module references list the tables, fields and actions.

Sources: the official Postman collection "API - IXC Provedor" (published by IXCSoft's API support), the official
wiki (`https://wikiapiprovedor.ixcsoft.com.br/`, one page per form with fields and allowed values) and the support
wiki pages "Configuração Webservice" and "Erros comuns API". Items marked *(observed)* come from Sufficit
production flows. The mechanics in this file (POST and GET search, `grid_param` with `IN` and `BE`, empty-result
shape, error shapes, 401) were checked read-only against a production IXC on 2026-11-14; *(inferred)* items are not documented and must be confirmed with a read before relying on them.

## Base URL and authentication

- Base: `https://<customer-ixc-host>/webservice/v1`. The host is the customer's own IXC server. There is no
  central IXC cloud API; never guess a host. Opening `https://<host>/webservice/v1` in a browser shows whether the
  API module is enabled.
- Auth: HTTP Basic. User name = the numeric id of the IXC user, password = that user's token:
  `Authorization: Basic base64("<userId>:<token>")`.
- The token is created in **Configurações do sistema → Usuários → Novo**, with **Permite acesso ao webservice**
  checked; IXC generates it when the user is saved. Webservice permissions and logs work exactly like a logged-in
  user: the user's group decides which forms it can list, insert, edit or delete. See
  [administration](administration.md#api-user-setup) for a least-privilege setup.
- Many installations restrict access by source IP. If calls time out or are refused, the caller's public IP must be
  allowlisted by the customer.
- Send `Content-Type: application/json`.

## Operations

| Operation | Method | Path | Header | Body |
|---|---|---|---|---|
| List / search | `GET` with a JSON body (official) or `POST` *(observed, works)* | `/<table>` | `ixcsoft: listar` | search object |
| Insert | `POST` | `/<table>` | none | record fields; every required field of the form |
| Update | `PUT` | `/<table>/<id>` | none | **all** fields of the record, not only the changed ones |
| Delete | `DELETE` | `/<table>/<id>` | none | none |
| Action ("botão", wizard, report) | per action (`POST`, `PUT` or `GET`) | `/<action_name>` | per action | small JSON, see each module |

- The `ixcsoft: listar` header turns a request into a search. A `POST` search without it **inserts a record**
  built from the search fields (or fails validation). Check this header first when a call behaves unexpectedly.
  Several official action examples also carry `ixcsoft: listar`; follow each module's documented headers.
- Many HTTP clients drop the body of a `GET`. Prefer `POST` + `ixcsoft: listar` from tools that cannot send a GET
  body (Fleet HTTP tools, n8n, Typebot).
- Update: IXC documents that a `PUT` must contain every field, even unchanged ones. Read the record first
  (search by `<table>.id`), change the fields you need on the returned object and send the whole object back to
  `/<table>/<id>`. Omitted fields can be blanked.
- Insert: fill every field marked required in the form (module references and the official wiki list them). The
  `id` field is auto-increment; never send it on insert.
- Delete is destructive. Do not delete unless the user explicitly asked for that exact record to be removed and
  confirmed it. Prefer the documented cancel/inactivate action of the module.

## Search body

```json
{
  "qtype": "cliente.cnpj_cpf",
  "query": "123.456.789-09",
  "oper": "=",
  "page": "1",
  "rp": "20",
  "sortname": "cliente.id",
  "sortorder": "desc"
}
```

| Field | Meaning |
|---|---|
| `qtype` | field to filter, `<table>.<field>` (table prefix required) |
| `query` | value to compare, always a string |
| `oper` | operator (table below) |
| `page` | page number, from `1` |
| `rp` | rows per page. Keep small (1–50) for interactive work; thousands are slow and may time out |
| `sortname` / `sortorder` | sort field (`<table>.<field>`) and `asc` / `desc` |
| `grid_param` | extra AND filters as a **JSON-encoded string** (below) |

Operators (official list):

| `oper` / `OP` | Meaning | Rule |
|---|---|---|
| `=` `!=` | equal / different | |
| `>` `<` `>=` `<=` | comparisons | numbers and dates |
| `L` / `NL` | contains / does not contain | text (SQL `LIKE`) |
| `IN` / `NI` | in / not in a comma-separated list (`"1,3,5"`) | numbers (official rule). On text codes it works for some fields (`cliente_contrato.status_internet IN CA,CM,FA`) and breaks on others (`fn_areceber.status`); prefer `!=` chains or `=` for text |
| `BE` / `NBE` | between / not between `P` and `P2` | needs both bounds; only inside `grid_param` |

To list a whole table, use `"qtype": "<table>.id", "query": "1", "oper": ">="` (or `"0"` with `>`) and page.
The official examples also use `"query": ""` with a `grid_param`, so the main filter is ignored when empty.

### Several filters (`grid_param`)

`grid_param` is a string containing a JSON array of `{ "TB": "<table>.<field>", "OP": "<oper>", "P": "<value>" }`
(plus `"P2"` for `BE`/`NBE`). All conditions are ANDed with the main `qtype` filter.

```json
{
  "qtype": "fn_areceber.id_cliente",
  "query": "<id_cliente>",
  "oper": "=",
  "page": "1",
  "rp": "20",
  "sortname": "fn_areceber.data_vencimento",
  "sortorder": "asc",
  "grid_param": "[{\"TB\":\"fn_areceber.status\",\"OP\":\"=\",\"P\":\"A\"},{\"TB\":\"fn_areceber.liberado\",\"OP\":\"=\",\"P\":\"S\"}]"
}
```

Escape the inner quotes. A raw array instead of a string is ignored or rejected depending on the version.

Common official filters, all as `grid_param` entries:

| Need | Table | Filter |
|---|---|---|
| active customers | `cliente` | `cliente.ativo = S` |
| registered in a month | `cliente` | `cliente.data_cadastro BE 01/04/2016 … 30/04/2016` |
| contracts activated in a month | `cliente_contrato` | `cliente_contrato.data_ativacao BE <first> … <last>` |
| blocked contracts | `cliente_contrato` | `cliente_contrato.status_internet IN CA,CM` (see [customers](customers.md)) |
| open, released invoices | `fn_areceber` | `fn_areceber.status = A` and `fn_areceber.liberado = S` |
| hidden invoices | `fn_areceber` | `fn_areceber.liberado = N` |
| open tickets of a customer | `su_ticket` | main `su_ticket.id_cliente = <id>`, `su_ticket.su_status = N` |
| open service orders | `su_oss_chamado` | `su_oss_chamado.status = A` (`AG` scheduled, `F` finished) |
| active and online logins | `radusuarios` | `radusuarios.online = S` and `radusuarios.ativo = S` |
| login by MAC | `radusuarios` | `radusuarios.mac = AA:BB:CC:DD:EE:FF` |
| sessions by date | `radacct` | `radacct.acctstarttime BE 2023-12-18 00:00:00 … 2023-12-18 23:59:59` |
| changes made to one record | `ixc_logs` | main `ixc_logs.id_tabela = <id>`, `ixc_logs.tabela = radusuarios` |

## Responses

- Search: `{ "page": "1", "total": "37", "registros": [ { … } ] }`. `total` counts the whole filter, not the page.
  Every value is a string. No match → `total: "0"` and no or empty `registros`.
- Insert: `{ "type": "success", "message": "…", "id": "<new id>" }`.
- Update, delete and actions: `{ "type": "success", "message": "…" }`; some actions add fields (see modules).
- **Errors usually come back as HTTP 200** with `{ "type": "error", "message": "…" }`. Always check `type` before
  reading `registros` or `id`; never report an error as "no records" or "done". `message` is Portuguese and may
  contain HTML (`<br />`); relay the real reason in plain words.
- A filter IXC cannot process can return HTTP 200 with a **non-JSON** body such as "Ocorreu um erro ao processar.
  Contate o suporte IXC Soft." Treat a non-JSON 200 as an error of the request (usually the filter), not as data.
- HTTP status codes (official "Erros comuns API"):
  - `401 Authorization Required` — the user's token changed or the user was deleted (or webservice access is off).
    The body is an nginx HTML page, not JSON.
  - `404 Not Found` from nginx — the server lacks `try_files $uri $uri /webservice/index.php?$query_string;`;
    a customer-side fix. A 404 on one table only means a wrong table or action name.
  - `400 Bad Request` — `http://` used where the server requires `https://`.
  - Timeouts — large `rp`, `L` filters on big tables or an overloaded server; reduce the page and filter on ids.

## Value formats

- Dates in records: `YYYY-MM-DD`; date-times `YYYY-MM-DD HH:MM:SS` (server local time, normally
  `America/Sao_Paulo`). Empty dates may appear as `0000-00-00`.
- Dates in filters: the official examples use `DD/MM/YYYY` for date fields (`data_cadastro`, `data_vencimento`,
  `data_ativacao`) and `YYYY-MM-DD HH:MM:SS` for date-time fields (`radacct.acctstarttime`). If a date filter
  returns nothing unexpectedly, try the other format.
- Dates in insert/update bodies: the official examples mostly send `DD/MM/YYYY` (as the UI does). When you update
  a record you just read, send the dates back in the format the read returned unless the module says otherwise,
  and read the record again to confirm the stored value.
- Booleans: `"S"` (sim) / `"N"` (não).
- Money: decimal with a dot, as a string (`"99.90"`).
- `cliente.cnpj_cpf` is stored **with punctuation**: CPF `000.000.000-00`, CNPJ `00.000.000/0000-00`. Mask what
  the person typed or said before an `=` search (11 digits → CPF mask, 14 digits → CNPJ mask). Checked on a
  production IXC: the digits-only search finds nothing.
- Phones (`telefone_celular`, `fone`, `whatsapp`) are free text, usually `(DD) 9XXXX-XXXX` *(observed)*. Search with
  the same mask; when unsure, use `L` with the last 8 digits and confirm the match with a second datum.
- Field names keep IXC's spelling, including typos: `su_ticket.menssagem`, table `sub_grupo_produdos`.
- Ids are numeric strings. Relations are named `id_<table>` (`id_cliente`, `id_contrato`, `id_login`, `id_filial`).
- Opaque names such as `cliente_contrato_15464` or `botaoAjax_22282` are IXC's internal button ids. They are
  stable across installations of the same IXC version but can change between versions; the module references say
  what each one does.

## Volume

- IXC runs on the customer's own server: avoid loops of thousands of calls, page bulk reads with `rp` 100–500 and
  pause between pages.
- Never pull an entire table to answer a question about one customer; filter on the server.

## Example with curl

```bash
# IXC_URL=https://ixc.example.com.br/webservice/v1
# IXC_AUTH=$(printf '%s' "$IXC_USER_ID:$IXC_TOKEN" | base64 -w0)
curl -sS -X POST "$IXC_URL/cliente" \
  -H "Authorization: Basic $IXC_AUTH" -H "Content-Type: application/json" -H "ixcsoft: listar" \
  -d '{"qtype":"cliente.cnpj_cpf","query":"123.456.789-09","oper":"=","page":"1","rp":"1"}'
```

Never echo `IXC_AUTH` or the token; keep them in environment variables or a credential reference.
