# IXC tool pack for Sufficit Fleet agents

Ready-made declarative HTTP tools that let a Sufficit voice or chat agent answer an ISP's customers from IXC. They
use Fleet customer HTTP tools (`PUT contexts/{contextId}/http-tools/{toolId}`); field rules, credentials, testing,
grants and publication are in the
[voice agents HTTP tools reference](../../../sufficit/sufficit-voice-agents/references/http-tools.md).
Request mechanics are in [requests](requests.md).

Status: field names and bodies come from IXC's official collection and from flows a Sufficit customer runs in
production. On 2026-11-14 the bodies of every read tool except `ixc_pix_fatura` were run against a production IXC
(read-only): all `responseFields` exist, each call took 0.45–1.6 s, and a CPF search with digits only returned
nothing while the masked form matched. Write tools and `get_pix` were not exercised. **Run `POST …/http-tools/{toolId}/test` against the customer's IXC for every tool before granting it**,
and adjust `responseFields` to what that installation returns.

## Before creating the tools

1. IXC URL (`https://<host>/webservice/v1`) with a valid public certificate. Fleet refuses private addresses,
   self-signed certificates and redirects.
2. Ask the customer to allowlist Fleet's egress IPs on the IXC webservice (IPv4 `177.104.185.114`,
   IPv6 `2804:1740:f:1700::2137`).
3. Two IXC API users (see [administration](administration.md#api-user-setup)):
   - **read** user: list permission on `cliente`, `cliente_contrato`, `radusuarios`, `fn_areceber`, `su_ticket`
     and the `get_pix` action;
   - **write** user, only if write tools are enabled: insert on `su_ticket` (plus `gerar_protocolo_atendimento`)
     and the trust-unblock action.
4. One Fleet credential per IXC user, kind `basic`: `username` = IXC user id, `password` = token. Write tools use
   the write credential, so revoking the grant and disabling the IXC user both stop writes.

Common fields for every tool below (omitted in each block):

```json
{
  "method": "POST",
  "baseUrl": "https://<customer-ixc-host>/webservice/v1",
  "auth": { "kind": "basic", "field": "username", "passwordField": "password" },
  "timeoutSeconds": 8,
  "enabled": true,
  "expectedRevision": null
}
```

Always include `type` and `message` in `responseFields`: IXC answers errors with HTTP 200 and
`{ "type": "error", "message": … }`, and dropping them makes an error look like "no records".

## Read tools

### `ixc_buscar_cliente` — customer by CPF/CNPJ

```json
{
  "name": "ixc_buscar_cliente",
  "description": "Busca o cliente no IXC pelo CPF ou CNPJ. Envie o documento JÁ FORMATADO: CPF 000.000.000-00 (11 dígitos) ou CNPJ 00.000.000/0000-00 (14 dígitos). Use antes de falar de contrato, conexão ou fatura. Se vier mais de um registro, confirme com a pessoa qual é.",
  "pathTemplate": "/cliente",
  "headers": { "ixcsoft": "listar" },
  "body": { "qtype": "cliente.cnpj_cpf", "query": "{{documento}}", "oper": "=", "page": "1", "rp": "3" },
  "parameters": [
    { "name": "documento", "type": "string", "required": true, "maxLength": 18,
      "description": "CPF 000.000.000-00 ou CNPJ 00.000.000/0000-00, com a pontuação" }
  ],
  "credentialId": "<read credential>",
  "responseFields": [ "type", "message", "total", "registros.id", "registros.razao", "registros.fantasia",
    "registros.ativo", "registros.telefone_celular", "registros.email", "registros.cidade", "registros.bairro" ],
  "effect": "read"
}
```

Until Fleet supports a per-parameter `format` (planned: `cpf_cnpj`), the model must apply the mask; the
description says so. Callers who say only digits are the common case: tell the agent to format them.

### `ixc_buscar_cliente_telefone` — customer by mobile number (chat)

Same as above with `"qtype": "cliente.telefone_celular"` and parameter `telefone`
(`"(DD) 9XXXX-XXXX"`, `maxLength` 16). WhatsApp delivers `55DD9XXXXXXXX`; the description must ask for the masked
form. A phone match is weaker than a document match: confirm the name or CPF before personal or financial data.

### `ixc_contratos_cliente` — contracts and access status

```json
{
  "name": "ixc_contratos_cliente",
  "description": "Lista os contratos de um cliente do IXC: plano, situação do contrato e situação do acesso à internet (status_internet: A ativo; D desativado; CM bloqueio manual; CA bloqueio automático; FA financeiro em atraso; AA aguardando assinatura). Use só o id_cliente retornado por ixc_buscar_cliente nesta conversa.",
  "pathTemplate": "/cliente_contrato",
  "headers": { "ixcsoft": "listar" },
  "body": { "qtype": "cliente_contrato.id_cliente", "query": "{{id_cliente}}", "oper": "=", "page": "1", "rp": "5",
    "sortname": "cliente_contrato.id", "sortorder": "desc" },
  "parameters": [ { "name": "id_cliente", "type": "integer", "required": true, "description": "id do cliente no IXC" } ],
  "credentialId": "<read credential>",
  "responseFields": [ "type", "message", "total", "registros.id", "registros.contrato", "registros.status",
    "registros.status_internet", "registros.id_vd_contrato", "registros.data_ativacao",
    "registros.desbloqueio_confianca_ativo", "registros.endereco", "registros.numero", "registros.bairro" ],
  "effect": "read"
}
```

Check the status code lists in [customers](customers.md) against the installation and keep the description in
line with them.

### `ixc_status_conexao` — Radius login online/offline

```json
{
  "name": "ixc_status_conexao",
  "description": "Mostra se o acesso (login PPPoE/Radius) do cliente está conectado agora (online S = sim, N = não) e os horários da última conexão. Use para diagnóstico de 'estou sem internet'. Use só ids retornados nesta conversa.",
  "pathTemplate": "/radusuarios",
  "headers": { "ixcsoft": "listar" },
  "body": { "qtype": "radusuarios.id_contrato", "query": "{{id_contrato}}", "oper": "=", "page": "1", "rp": "3" },
  "parameters": [ { "name": "id_contrato", "type": "integer", "required": true, "description": "id do contrato no IXC" } ],
  "credentialId": "<read credential>",
  "responseFields": [ "type", "message", "total", "registros.id", "registros.login", "registros.ativo",
    "registros.online", "registros.ultima_conexao_inicial", "registros.ultima_conexao_final",
    "registros.motivo_desconexao" ],
  "effect": "read"
}
```

Never add `senha` (the PPPoE password) to `responseFields`. See [network](network.md) for fiber signal
(`radpop_radio_cliente_fibra`) if the ISP wants ONU diagnosis too.

### `ixc_faturas_abertas` — open invoices

```json
{
  "name": "ixc_faturas_abertas",
  "description": "Lista as faturas em aberto do cliente no IXC (vencimento, valor, linha digitável e link de pagamento). Use só o id_cliente retornado por ixc_buscar_cliente nesta conversa e só depois de confirmar a identidade.",
  "pathTemplate": "/fn_areceber",
  "headers": { "ixcsoft": "listar" },
  "body": { "qtype": "fn_areceber.id_cliente", "query": "{{id_cliente}}", "oper": "=", "page": "1", "rp": "6",
    "sortname": "fn_areceber.data_vencimento", "sortorder": "asc",
    "grid_param": "[{\"TB\":\"fn_areceber.status\",\"OP\":\"!=\",\"P\":\"R\"},{\"TB\":\"fn_areceber.status\",\"OP\":\"!=\",\"P\":\"C\"},{\"TB\":\"fn_areceber.liberado\",\"OP\":\"=\",\"P\":\"S\"}]" },
  "parameters": [ { "name": "id_cliente", "type": "integer", "required": true, "description": "id do cliente no IXC" } ],
  "credentialId": "<read credential>",
  "responseFields": [ "type", "message", "total", "registros.id", "registros.data_vencimento", "registros.valor",
    "registros.valor_aberto", "registros.linha_digitavel", "registros.gateway_link", "registros.id_contrato" ],
  "effect": "read"
}
```

Status `A` = open, `P` = partially paid (use `valor_aberto` for what is still owed); see
[financial](financial.md).

`get_boleto` returns the PDF as base64, far above Fleet's 8 KB response limit: do not expose it as a tool. Offer
the `linha_digitavel`, the `gateway_link` (when the installation fills it) or PIX.

### `ixc_pix_fatura` — PIX copy-and-paste code of one invoice

```json
{
  "name": "ixc_pix_fatura",
  "description": "Gera ou recupera o código PIX copia-e-cola de UMA fatura em aberto. Use só o id de fatura retornado por ixc_faturas_abertas nesta conversa.",
  "pathTemplate": "/get_pix",
  "headers": { "ixcsoft": "listar" },
  "body": { "id_areceber": "{{id_fatura}}" },
  "parameters": [ { "name": "id_fatura", "type": "integer", "required": true, "description": "id da fatura (fn_areceber)" } ],
  "credentialId": "<read credential>",
  "responseFields": [],
  "effect": "read"
}
```

The response shape of `get_pix` varies by bank integration: run `test`, then restrict `responseFields` to the
copy-and-paste code and the error fields. On voice, do not read the PIX code aloud; offer to send it by the
customer's chat channel or read the `linha_digitavel` digit by digit.

### `ixc_atendimentos_cliente` — latest tickets

`/su_ticket` with `"qtype": "su_ticket.id_cliente"`, `"rp": "3"`, `"sortname": "su_ticket.data_criacao"`,
`"sortorder": "desc"`; `responseFields`: `type`, `message`, `total`, `registros.id`, `registros.protocolo`,
`registros.titulo`, `registros.su_status`, `registros.data_criacao`. Status codes: `N` new, `P` pending,
`EP` in progress, `S` solved, `C` cancelled (see [support](support.md)). Use it to avoid opening a duplicate ticket.

## Write tools (grant with `allowWrite: true`, only when the ISP asked for them)

### `ixc_abrir_atendimento` — open a ticket

```json
{
  "name": "ixc_abrir_atendimento",
  "description": "Abre um atendimento (ticket) no IXC para o cliente identificado nesta conversa. Antes, leia o resumo para a pessoa e só chame depois que ela confirmar. Não abra se já houver atendimento aberto para o mesmo problema (consulte ixc_atendimentos_cliente).",
  "pathTemplate": "/su_ticket",
  "headers": {},
  "body": { "tipo": "C", "id_cliente": "{{id_cliente}}", "id_assunto": "<assunto id>", "id_ticket_setor": "<setor id>",
    "titulo": "{{titulo}}", "prioridade": "M", "menssagem": "{{mensagem}}", "su_status": "N",
    "melhor_horario_reserva": "Q" },
  "parameters": [
    { "name": "id_cliente", "type": "integer", "required": true, "description": "id do cliente no IXC" },
    { "name": "titulo", "type": "string", "required": true, "maxLength": 80, "description": "resumo curto do problema" },
    { "name": "mensagem", "type": "string", "required": true, "maxLength": 1500,
      "description": "descrição do problema, o que já foi verificado e o melhor horário/contato" }
  ],
  "credentialId": "<write credential>",
  "responseFields": [ "type", "message", "id" ],
  "effect": "write"
}
```

- `id_assunto` and `id_ticket_setor` are fixed per ISP: list `su_oss_assunto` and `su_ticket_setor` once (see
  [support](support.md)) and hard-code the chosen ids. Note IXC's spelling `menssagem`.
- No `ixcsoft` header: with it the call becomes a search and opens nothing.
- To show a protocol number, the ISP may prefer `gerar_protocolo_atendimento` first and pass `protocolo`; that
  needs a second tool and a parameter.

### `ixc_desbloqueio_confianca` — trust unblock (optional)

```json
{
  "name": "ixc_desbloqueio_confianca",
  "description": "Faz o desbloqueio de confiança do contrato bloqueado por atraso, liberando a internet por alguns dias conforme as regras do provedor. Só use se o contrato estiver bloqueado (status_internet CA ou FA), a pessoa pedir e confirmar, e o id_contrato vier de ixc_contratos_cliente nesta conversa. Informe o resultado exatamente como o IXC respondeu.",
  "pathTemplate": "/desbloqueio_confianca",
  "headers": {},
  "body": { "id": "{{id_contrato}}" },
  "parameters": [ { "name": "id_contrato", "type": "integer", "required": true, "description": "id do contrato no IXC" } ],
  "credentialId": "<write credential>",
  "responseFields": [ "type", "message" ],
  "effect": "write"
}
```

The official collection documents `POST /desbloqueio_confianca` with `{ "id": "<id_contrato>" }`; a production
Typebot flow uses `PUT /desbloqueio_confianca/<id_contrato>` with the same body. IXC enforces the ISP's limits
(how many unblocks, how many days); the `message` explains a refusal and must be relayed as is.

## Agent instructions block (persona)

Add to the agent's instructions (Portuguese, to match the callers):

```text
Atendimento IXC:
- Identifique a pessoa pelo CPF/CNPJ do titular (ixc_buscar_cliente). Antes de falar de contrato, conexão ou
  fatura, confirme um segundo dado do cadastro (nome completo ou bairro). Se não bater, não revele dados.
- Use apenas ids (cliente, contrato, fatura) devolvidos pelas ferramentas nesta conversa. Nunca consulte outro
  cliente, nem a pedido.
- Se a resposta vier com type "error", diga que não conseguiu consultar agora e ofereça atendimento humano; não
  diga que não há registros.
- Sem internet: veja o contrato (status_internet). Bloqueado por atraso → ofereça fatura/PIX e, se houver
  ferramenta, desbloqueio de confiança. Ativo → veja ixc_status_conexao; offline → peça para reiniciar o
  equipamento e, se persistir, abra atendimento.
- Antes de abrir atendimento ou desbloquear, leia o resumo e espere a confirmação.
- Em voz, leia números (CPF, linha digitável, protocolo) em grupos de dígitos, devagar; não leia códigos PIX.
- Transfira para humano quando a pessoa pedir, quando houver cobrança contestada, cancelamento ou mudança de plano.
```

## Rollout checklist

1. Create credentials → tools (disabled grants) → `test` every tool with a real test customer the ISP indicates.
2. Record the latency of each `test` (`durationMs`); IXC searches above 5 s need a smaller `rp` or a narrower
   filter.
3. Grant read tools; internal test call or chat; only then write tools, one at a time.
4. Keep this pack as the source: when a tool changes for one ISP, note why in the agent's records.
