# IXC administration

Company and system administration: company and branches, IXC users (including the API user itself), user ↔
branch/warehouse links, SMTP, logs, HR/payroll (colaboradores), reports that return files, and global
configuration. Use it to resolve ids (`filial`, `usuarios`, `funcionarios`), to audit who did what, and to set up
the integration user. Shared mechanics are in [request mechanics](requests.md); `cidade`/`uf` CRUD is with the
customer tables in [customers](customers.md); stock reports' context is in [inventory and sales](inventory-sales.md).

Sensitive-data rules for this module (stricter than elsewhere):
- Never print, log or relay `usuarios.senha`, `usuarios.acesso_token`, `smtp.senha`, `filial` certificate/NFS-e
  credentials (`nfe_certificado`, `nfe_email_senha`, `nfse_senha_acesso`, `token`, `nfse_client_secret`, `nfce_csc`),
  `configuracao_geral` secrets (`client_secret`, `firebase_secret`, `senha_*`) or `configuracao_mvno` credentials.
  Drop those keys from every response before showing or storing it.
- `funcionarios` and `funcionarios_arquivos` hold employees' personal data (CPF, RG, PIS, bank account, PIX key,
  salary, dependants). Return only the fields the task needs (name, id, active, sector).
- Writes here change who can log in, what they can see, and how the company invoices. Confirm every write; prefer
  doing user/permission changes in the IXC UI.

## Tables

### `empresa` — company (Empresa)
Operations: list / insert / update / delete. Top-level legal entity; branches hang from it.
Fields in the collection: `razao` (REQ, company name), `logomarca`, `logo_docs`, `logo_recibo`, `logo_autenticacao_tv`,
`sped_indicador_natureza_pessoa_juridica`. n8n lists an unmapped action `retornar_logo_app` on this resource.

### `filial` — branch (Filiais)
Operations: list / insert / update / delete. Almost every record carries `filial_id`/`id_filial`; the branch sets the
CNPJ, fiscal configuration (NF-e/NFS-e/NFC-e), Anatel data and contact details used on invoices and messages.
| Field | Meaning | Notes |
|---|---|---|
| `id` | branch id | used as `filial_id` / `id_filial` everywhere |
| `ativo` | active | |
| `id_empresa` | company | → `empresa` |
| `razao`, `fantasia`, `tipo_pessoa`, `cnpj`, `ie`, `im`, `cnae` | legal identity | |
| `ato_anatel`, `sici_numero_fistel`, `rt` | telecom regulatory data | |
| `cidade`, `bairro`, `endereco`, `numero`, `cep`, `complemento`, `latitude`, `longitude` | address | `cidade` → `cidade` |
| `telefone`, `telefone1`, `whatsapp`, `email`, `email_suporte`, `site` | contacts shown to customers | |
| `nfe_*`, `nfse_*`, `nfce_*`, `opcao_simples`, `rt_especial` | fiscal configuration | contains secrets, never expose |
| `contador_*` | accountant | |
Updating a branch can break invoice issuing; do not change fiscal fields through the API.

### `usuarios` — IXC system users (Usuários)
Operations: list / insert / update (no delete in the collection; deactivate with `status=I` in the UI). This is
also where the API credential lives: the Basic-auth user id is `usuarios.id`.
| Field | Meaning | Values / notes |
|---|---|---|
| `id` | user id (= API user id for webservice users) | |
| `nome`, `email` | name, login e-mail | REQ |
| `senha` | password | REQ on insert; **never expose**; update examples resend it (avoid user updates via API) |
| `id_grupo` | permission group | REQ → `usuarios_grupo`; permissions per form come from the group |
| `status` | active | `A`=Ativo, `I`=Inativo |
| `tipo_acesso` | where the user can log in | `A`=Ambos, `W`=Web, `M`=Mobile |
| `funcionario` | linked colaborador | → `funcionarios` (used to find a technician's user) |
| `acesso_webservice` | "Permite acesso ao webservice" | checkbox (`S`) |
| `acesso_token` | webservice token | RO, max 70, generated on save; **secret** |
| `language` | UI language | REQ `Pt-Br`, `En-Us`, `Es-Es` |
| `filtra_setor`, `filtra_funcionario`, `mostrar_os_sem_funcionario` | service-order visibility filters | `S`/`N`; defaults `N`, `N`, `S` |
| `filtra_departamento_ticket`, `filtra_funcionario_ticket`, `mostrar_ticket_sem_funcionario` | ticket visibility filters | `S`/`N` |
| `recebimentos_dia_atual`, `pagamentos_dia_atual`, `lancamentos_dia_atual` | restrict cash operations to today | REQ `S`/`N` |
| `desc_max_recebimento`, `desc_max_renegociacao`, `desc_max_monetario` | max discounts the user may give | decimals |
| `caixa_fn_receber`, `id_caixa`, `vendedor_padrao` | default cash account / seller | → `contas` / `vendedor` |
| `callcenter`, `user_callcenter` | call-center integration | e.g. `actioncall`, `belluno` |
| `permite_inutilizar_patrimonio`, `administrador_kanban`, `enviar_notificacao_backup`, `enviar_monitoramento_host` | misc permissions/notifications | |

### User ↔ branch / warehouse links
| Table | Purpose | Ops | Fields |
|---|---|---|---|
| `filial_usuario` | branches a user may operate (Filiais do usuário) | L/I/U/D | `usuario_id` → `usuarios`, `filial_id` → `filial`, `filial_padrao` `S`/`N` (default branch), `ativo` `S`/`N`. List with `qtype=filial_usuario.usuario_id`. |
| `almox_usuario` | warehouses a user holds/uses (Almoxarifados do usuário) | L/I/U/D | `id_usuario` → `usuarios`, `id_almox` → `almox`, `padrao_usuario` `S`/`N` (default). List with `qtype=almox_usuario.id_usuario`. This is how a technician's stock is found. |

### `smtp` — outgoing e-mail accounts (E-mail SMTP)
Operations: list / insert / update / delete. Used by invoices, O.S. e-mails, marketing.
Fields: `servidor_saida` REQ, `usuario` REQ, `senha` REQ (**secret**), `porta` REQ, `autenticacao` `S`/`N`,
`conexao_ssl` `S`=SSL, `T`=TLS, `N`=Nenhum (insecure), `codificacao_utf8` `S`/`N`, `forcar_codificacao`
`I`=ISO-8859-1, `U`=UTF-8, `A`=Automático, `remover_xmailer` `S`/`N`, `remetente`, `bcc_email`, `destino_envio`,
`limite_hora` (default 200), `limite_dia`, `responsavel_envio`, `assunto_envio` REQ, `texto_envio` REQ (HTML).
The collection's list example filters `wfl_processo.id` (copy error); use `smtp.id` (inferred).
Changing SMTP affects every e-mail the customer's IXC sends to subscribers.

### Logs (read-only)
| Table | Content (UI label) | Use |
|---|---|---|
| `ixc_logs` | user action log (Logs dos usuários): who changed which record | audit "who cancelled/changed X"; filter by id range or date, small `rp` |
| `log_tarefa_gateway` | payment-gateway task log (Logs gateway) | why a gateway charge/return failed |
| `crm_email_log` | e-mails sent (Logs de e-mails) | prove an invoice/notice e-mail was sent |
| `crm_sms_log` | SMS sent (Log SMS) | prove an SMS was sent |
| `log_backup` | IXC backup runs (Logs de backup) | backup health |
Field catalogs are not in the wiki extract: list one record (`rp=1`, `sortorder=desc`) to learn the field names
before filtering. These tables are large; never page through them without a filter.

### HR / payroll (Folha de pagamento)

#### `funcionarios` — colaboradores (employees, technicians, sellers)
Operations: list / insert / update / delete. Technicians in O.S. (`id_tecnico`, `id_funcionario`) point here.
| Field | Meaning | Values / notes |
|---|---|---|
| `funcionario` | name | REQ, max 100 |
| `ativo` | active | `S`/`N` |
| `filial_id` | branch | REQ |
| `usuario_id` | linked IXC user | → `usuarios` (the reverse link is `usuarios.funcionario`) |
| `id_departamento`, `id_setor_padrao` | sector | → `empresa_setor` |
| `id_funcao` | job role | → `fl_funcoes` |
| `cidade` | city | REQ → `cidade` |
| `id_conta` | accounting account | REQ → `planejamento_analitico` |
| `envia_email_os`, `envia_sms_os` | notify the colaborador of new O.S. | REQ `S`/`N` |
| `rastreador`, `rastreador_tipo`, `id_veiculo_padrao`, `cor_mapa` | tracking / map | `rastreador_tipo` `S`=Externo, `N`=Inmap Service |
| `mostrar_no_quadro_kanban`, `exibir_colaborador_inmap`, `maximo_os_dia` | scheduling | |
| `data_admissao`, `data_demissao` | dates | |
| `cpf_cnpj`, `pis_numero`, `ie_identidade`, `cnh_*`, `ctps_*`, `salario`, `banco`, `agencia`, `conta`, `chave_pix`, `dep_*`, `nome_mae`… | personal/payroll data | **personal data, do not expose** |
| `tipo_recebimento` | salary payment | `C`=Cheque, `B`=Transferência, `D`=Dinheiro, `P`=Pix |

| Table | Purpose | Ops | Notes |
|---|---|---|---|
| `funcionario_setores` | sectors of a colaborador (Setores) | L/I/U/D | `setor` → `empresa_setor`, `usuario` (id of the colaborador/user as in the example), `listar_agenda` `S`/`N`, `ativo` `S`/`N`. List with `qtype=funcionario_setores.usuario`. Sector membership drives O.S. visibility when `usuarios.filtra_setor=S`. |
| `funcionarios_arquivos` | files attached to a colaborador | L/I/D | insert is **multipart/form-data**: `descricao`, `arquivo` (file), `id_funcionario`, `tipo_doc` |
| `empresa_setor` | sectors/departments (Setor) — catalog only | | `setor` REQ, `ativo` `S`/`N`, `id_depto` → `su_ticket_setor` |
| `fl_adto_salario` | salary advance (Adiantamento de salários) | L/I/U/D | REQ `id_funcionario`, `descricao`, `data` (`DD/MM/YYYY`), `tipo_pagamento` (catalog: `Dinheiro`/`Cheque`; the Postman example sends `D`), `valor`, `conta_` → `contas` (cash account debited), `filial_id`. **Money write**: creates a cash outflow. |

### Global configuration (catalog only; not in the Postman collection)
| Table | Purpose | Notes |
|---|---|---|
| `configuracao_geral` | global settings of the subscriber portal/app (Central do Assinante), uploads, SMTP defaults, invoice display, card/PIX, push templates | Read-only for agents. Useful flags: `habilitar_web_services`, `ips_central_api` (allowed IPs for the portal API), `tipo_login` (`E`=e-mail+senha, `C`=CPF/CNPJ, `ID`=customer id), `bloquear_ip` `S`/`N`, `fatura_antecedencia` (days before due date an invoice shows, default 15), `pix_habilitar`, `pix_carteira`, `credit_card_*`, `manutencao` (portal in maintenance). Contains secrets. n8n exposes action `get_pix_parameter` (no body documented). |
| `configuracao_mvno` | MVNO (mobile) integration credentials | `mvna` (`TGN`, `TIP`, `Telecall`, `Americanet`, `EAI`, `Surf`, `Contel`, `brazmovel`, `playmovel`, `tatelecom`, `Bora`, `Unifique`), `ambiente` `P`=Produção/`H`=Homologação, `integracao` `A`=Brasil/`S`=Tá Telecom, `url`, `login`, `senha`, `token`, `client_id`, `client_secret` — **secrets**; see [network](network.md) for MVNO lines. |
| `central_bloqueio_ip` | IPs blocked after failed subscriber-portal logins | `ip`, `tentativas` (attempts), `bloqueado`, `data_hora`, `id_cliente` → `cliente`, `houve_bloqueio`. Use to answer "customer can't log into the Central do Assinante". Deleting a row to unblock is a write; confirm first. |

## Actions

### `visualizar_arquivo_funcionario` — download a colaborador's file
`GET` (body) with header `ixcsoft: listar`, body `{"id": "<id funcionarios_arquivos>"}`. Returns the file content
(read). Personal document: only fetch when the user explicitly asks for that file.

## Reports

Report endpoints (`rfn_*` = provider/financial reports, `rcp_*` = stock reports) run the same code as the IXC report
screens. They are read-only but **heavy**: they can scan whole tables and usually return a file (PDF/CSV) as
**base64** instead of JSON rows. Always narrow the filters, decode base64 to a file (`.pdf`) instead of printing it,
and expect long response times. Prefer the normal table listings when the question can be answered with rows.

### `rfn_cliente` — customer report (Relatório de clientes)
`GET`/`POST` with `ixcsoft: listar`, body in listing format, e.g.
`{"qtype":"cliente.filial_id","query":"<id_filial>","oper":"=","page":"1","rp":"1","sortname":"cliente.id","sortorder":"desc"}`.
Keep `rp` small.

### `rcp_produtos_imprimir_23072` and grouped variants — product/stock report (Relatório de produtos)
| Endpoint | Grouping |
|---|---|
| `rcp_produtos_imprimir_23072` | none |
| `rcp_produtos_imprimir_agrupado_filial_12688` | by branch |
| `rcp_produtos_imprimir_agrupado_grupo_12708` | by subgroup |
| `rcp_produtos_imprimir_agrupado_amox_22890` | by warehouse |
Method `GET` with `ixcsoft: listar`. Body: `id_produto` (→ `produtos`), `sub_grupo_produtos` (→ `sub_grupo_produdos`),
`almoxarifado` (→ `almox`), `id_filial`, `controla_estoque` `S`/`N`/`T`=todos, `tipo` (empty = all, `C`=comércio,
`O`=consumo, `F`=fabricação, `M`=matéria prima, `P`=patrimônio, `S`=serviço), `ativo` `S`/`N`/`T`, `estoque`
`POS`=positive, `NEG`=negative, `TD`=all, `numero_cest` `T`=all, `P`=filled, `V`=empty. Response: base64 PDF
("Retorno vem em base64, transforme para PDF").

### Stock inventory per colaborador (Relatório de Inventário de Estoque por Colaborador)
The collection documents it on `rcp_produtos_imprimir_23072` with body `id_produto`, `sub_grupo_produtos`,
`almoxarifado`, `id_filial`, `id_tecnico` (→ `funcionarios`), `ativo` `S`/`N`/`T`, `ordenar` `alfabetica`|`id`
("Imprimir agrupado por almoxarifado"). The IXC n8n node names the same report
`rcp_inventario_por_tecnico_imprimir_agrupado_almox_23941`; if the first path ignores `id_tecnico`, try that one.
For a quick answer, the "products held by a technician" recipe in [inventory and sales](inventory-sales.md) is lighter.

### `rfn_bloqueio_cliente_comodatos_21558` — contracts report, equipment on loan (Relatórios contratos — Comodatos)
`GET` with `ixcsoft: listar`. Lists contracts with their comodato (loaned equipment). The body is the full report
filter form (~90 keys, all strings): `contrato` / `status` / `ativo` / `tipo_pessoa` / `tipo_contrato` `T`=all,
date ranges `di`/`df` (registration), `diativacao`/`dfativacao`, `dt_bloqueio_inicial`/`final`,
`data_cancelamento_i`/`_f`, `di_comodato`/`df_comodato`, `id_filial`, `id_contrato`, `id_vd_contrato`,
`id_cidade`, `produto_id`, `subgrupo_id`, `status_comodato` (example `E`), `ordem` (example `P`), `mostra_consulta`
`N`. Send every key from the example with empty strings for unused filters. Very heavy without a date/branch filter.
(Listed in the network extract; documented here as a report.)

Other report/print endpoints elsewhere: `imprimir_nota`, `imprimir_venda`, `vd_saida_25738`, `imprimir_pedido_compra`
in [inventory and sales](inventory-sales.md); invoice/boleto prints in [financial](financial.md).

## API user setup

What the customer (IXC admin) does to give an integration access; agents never create users themselves.
1. **Configurações do sistema → Usuários → Novo** (Settings → Users → New).
2. Fill name, e-mail, a strong password, `status` Ativo, and the permission group (`id_grupo`).
3. Tick **"Permite acesso ao webservice"** (`acesso_webservice`). Save: IXC generates the **token**
   (`acesso_token`) on save. The credential is `<usuarios.id>:<token>` (see [request mechanics](requests.md)).
4. Permissions follow the **user's group** (per form: listar, inserir, editar, deletar, plus buttons). The IXC wiki
   suggests putting the API user in the administrator group; **do not**. Create a dedicated group per integration
   with least privilege: read on the tables it queries, write only on the forms it must change (e.g. `su_ticket`,
   `su_oss_chamado`), no access to users, branches, configuration or payroll.
5. One user per integration (never share with a person or another system), so `ixc_logs` shows who did what and the
   token can be revoked alone.
6. For O.S./ticket work, set `filtra_setor`, `filtra_funcionario`, `filtra_departamento_ticket`,
   `filtra_funcionario_ticket` to `N` and keep `mostrar_os_sem_funcionario` / `mostrar_ticket_sem_funcionario` `S`;
   otherwise listings silently return only the records of the user's sector/colaborador.
7. Link `filial_usuario` to every branch the integration must see; ask the customer to allowlist the integration's
   public IP if webservice access is IP-restricted.
8. Store the token in a secret store (Vault/credential reference), never in chat, code or tickets. To rotate,
   regenerate the token in the user form (inferred) and update the store.
If calls return HTTP 401, check steps 3 and 8; if they return an IXC permission error, check step 4.

## Recipes

### Resolve reference ids (pattern used in production at a Sufficit customer)
- Users: `POST /usuarios` (listar) `{"qtype":"usuarios.id","query":"0","oper":">","page":"1","rp":"200","sortname":"usuarios.id","sortorder":"asc"}`.
  Keep only `id`, `nome`, `email`, `status`, `funcionario`, `id_grupo`; **strip `senha` and `acesso_token`**.
- Branches: `POST /filial` (listar) `qtype=filial.id`, `query=0`, `oper=>` → keep `id`, `razao`, `fantasia`, `cnpj`,
  `ativo`, `cidade`; strip fiscal secrets.
- City/state of a record: `POST /cidade` (listar) `qtype=cidade.id`, `query=<id>`, `oper==` → `nome`, `uf`; then
  `POST /uf` (listar) `qtype=uf.id`, `query=<cidade.uf>` → state. Cache these small lookups for the session.

### Who did this? (audit)
Find the record id and the approximate time, then list `ixc_logs` newest first with a narrow filter (learn the field
names from one record), map the user id to `usuarios.nome`. Report user, time and action; no tokens.

### Find a technician's IXC user and branches
`funcionarios` by name (`funcionarios.funcionario`, `oper=L`) → `id`; `usuarios` with `qtype=usuarios.funcionario`
→ user id; `filial_usuario` and `almox_usuario` by that user id.

### Was the e-mail/SMS sent to the customer?
List `crm_email_log` / `crm_sms_log` newest first filtered by the destination or customer field (inspect one record
for names), small `rp`. Read-only; resending is a separate, confirmed action in another module.

### Subscriber can't log into the Central do Assinante
List `central_bloqueio_ip` by `central_bloqueio_ip.id_cliente` = customer id → blocked IPs and attempts; check
`configuracao_geral.tipo_login` for the login method expected. Unblocking (delete/update the row) only with explicit
confirmation.
