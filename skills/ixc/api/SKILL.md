---
name: ixc-api
description: "Call the IXC Provedor (IXCSoft ISP management ERP) REST webservice correctly for every module — customers, contracts and plans, receivables (boleto, PIX, renegotiation), payables, tickets and service orders, Radius logins, connection status, trust unblock, fiber ONU/OLT, inventory, purchasing, sales, CRM, VoIP and administration — with Basic auth (user id + token), the ixcsoft: listar search header, grid_param filters and safe write rules. Also ships a tested-pattern tool pack for Sufficit Fleet voice and chat agents. Use when a request involves IXC, IXCSoft, IXC Provedor, webservice/v1 or an ISP's customer, contract, invoice, ticket, OS or login data."
metadata:
  version: "1.0.1"
---

# IXC Provedor API

IXC Provedor is the ERP many Brazilian ISPs run on their own server. Its REST webservice exposes each form
("formulário") as a table under `https://<isp-host>/webservice/v1/<table>`, plus "button" actions for things a user
clicks in the UI (unblock, disconnect, print boleto, close an OS). This skill teaches the shared mechanics, the
tables and actions of each module, and the safety rules for acting on an ISP's live system.

## Start here

1. Read [request mechanics](references/requests.md): auth, search body, operators, `grid_param`, update and error
   rules. Every module reference assumes it.
2. Open the module reference for the task:

| Task | Reference |
|---|---|
| Customers, contracts, contract buttons (activate, block, release, plan change, cancel), sale plans, leads/CRM, cities, files, SMS/push to the customer, credit check, TV/SVA | [customers](references/customers.md) |
| Receivables (`fn_areceber`), boleto (`get_boleto`), PIX (`get_pix`), receipts, cancellation, renegotiation, payables, accounting, billing wallets, fiscal | [financial](references/financial.md) |
| Tickets (`su_ticket`), protocols, service orders (`su_oss_chamado`) and their actions, subjects, sectors, teams, workflows | [support](references/support.md) |
| Radius logins (`radusuarios`), online status, consumption, disconnect, clear MAC, trust unblock, fiber ONU/OLT, POPs, IP pools, ACS, InMap, VoIP, MVNO | [network](references/network.md) |
| Stock, assets, transfers, products, purchasing, sales and invoices out, fleet | [inventory and sales](references/inventory-sales.md) |
| Company, branches, users and API users, logs, HR, reports | [administration](references/administration.md) |
| Ready tools and persona for Sufficit Fleet voice/chat agents | [Fleet tool pack](references/fleet-tools.md) |

3. Confirm field names against the customer's installation with a small read (`rp` 1) before relying on them.
   IXC versions differ; the official per-form wiki is `https://wikiapiprovedor.ixcsoft.com.br/`.

## Credentials

- You need the ISP's IXC host, an IXC user id and that user's webservice token. Auth is
  `Authorization: Basic base64("<userId>:<token>")`.
- Use the credential the environment provides (Sufficit Identity Vault entry, Fleet credential reference,
  environment variable). Never ask a person to paste a token into a chat, never print, log or commit it, and mask
  it (`abcd…`) when you must refer to it.
- The token carries the IXC user's permissions. Prefer a dedicated read-only user for lookups and a separate user
  for writes ([administration](references/administration.md#api-user-setup)).

## Safety rules

The webservice acts on the ISP's production system: its customers' internet access, invoices and books.

- **Read freely within the task; confirm before every write.** Before an insert, update or action, state what
  will change (table or action, record id, customer) and wait for the user's confirmation. A confirmation covers
  that one operation.
- **Never delete** unless the user explicitly asks to delete that exact record. Prefer the module's cancel or
  inactivate action.
- **Updates replace the record.** Read it, change the fields on the returned object and send all fields back.
- Treat these as high impact and say so before asking for confirmation: blocking, releasing or cancelling a
  contract; disconnecting a login; ONU authorization or removal; trust unblock; cancelling, receiving or
  renegotiating invoices; sending SMS, e-mail, push or WhatsApp to the end customer; changing a plan or price.
- **Errors arrive as HTTP 200** with `{ "type": "error", "message": … }`. Check `type` on every response; never
  report an error as "no records" or "done".
- **Personal data.** Fetch only the fields the task needs, never dump `registros` wholesale into a chat, never
  reveal passwords (`radusuarios.senha`, hotspot or Wi-Fi passwords) and never discuss one customer's data with
  another person. When serving an end customer, confirm identity (document + a second datum) first.
- **Load.** IXC runs on the ISP's server: filter on the server, keep `rp` small, page bulk reads and pause
  between pages.

## Quick reference

```json
POST /webservice/v1/cliente            header ixcsoft: listar
{ "qtype": "cliente.cnpj_cpf", "query": "123.456.789-09", "oper": "=", "page": "1", "rp": "1" }

POST /webservice/v1/fn_areceber        header ixcsoft: listar
{ "qtype": "fn_areceber.id_cliente", "query": "<id_cliente>", "oper": "=", "page": "1", "rp": "10",
  "sortname": "fn_areceber.data_vencimento", "sortorder": "asc",
  "grid_param": "[{\"TB\":\"fn_areceber.status\",\"OP\":\"=\",\"P\":\"A\"}]" }

POST /webservice/v1/su_ticket          no ixcsoft header (insert)
{ "tipo": "C", "id_cliente": "<id>", "id_assunto": "<id>", "titulo": "…", "menssagem": "…", "su_status": "N" }
```

- CPF/CNPJ are stored with punctuation (`000.000.000-00`, `00.000.000/0000-00`); mask before searching.
- Booleans are `S`/`N`; record dates `YYYY-MM-DD`; filter dates usually `DD/MM/YYYY`; every value is a string.
- Search without `ixcsoft: listar` = insert. Insert with that header = search.

## Support

Questions, gaps or errors in this skill go to Sufficit through the
[support skill](../../sufficit/sufficit-support/SKILL.md). Changes are recorded in [CHANGELOG](CHANGELOG.md).
