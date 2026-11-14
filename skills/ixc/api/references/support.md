# IXC support (atendimentos and ordens de serviço)

Tickets (`su_ticket`, "Atendimento"), their interactions, files and transfers; service orders (`su_oss_chamado`,
"Ordem de serviço") with every workflow button, the finishing wizard (products, comodato, services, files), the
support registries (subjects, departments, sectors, teams, events, canned answers, diagnostics, print models) and
the workflow engine (`wfl_*`). Use this file to read a customer's support history, open a ticket or OS, or move an
OS through its life cycle. Request shapes, auth, `ixcsoft: listar`, `grid_param` and error handling are in
[request mechanics](requests.md); customers, contracts and logins are in [customers](customers.md); stock,
products and comodato equipment in [inventory and sales](inventory-sales.md); users and permissions in
[administration](administration.md).

Before working with OS: the IXC wiki recommends removing the **"Filtrar setor"** and **"Filtrar funcionário"**
restrictions from the API user (Configurações → Usuários). With them on, listings silently return only the OS of
the user's own sector/employee and actions on other OS fail.

Every write here is visible to the ISP's support staff, and several actions notify the technician or the end
customer, move stock or create billable items. Confirm with the user before any insert, update or action; never
delete without an explicit request for that exact record.

## Tables

### `su_ticket` — support ticket (Atendimento)
Operations: list / insert / update (`PUT /su_ticket/<id>`, send the full record) / delete. One table for both
customer tickets (`tipo=C`) and tickets about the ISP's own structure (`tipo=E`). Status changes are normally done
by inserting an interaction in `su_mensagens` (see Actions), not by editing `su_status`.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | ticket id | autoincrement, never send on insert |
| `tipo` | ticket kind | **REQ**. `C`=Cliente, `E`=Estrutura própria (then `id_estrutura` is required) |
| `protocolo` | protocol number shown to the customer | max 20; get one from `gerar_protocolo_atendimento` before inserting |
| `id_cliente` | customer | → `cliente`. Required in the Postman insert (also for `tipo=E`) |
| `id_login` | internet login (PPPoE/IPoE) | → `radusuarios` (optional) |
| `id_contrato` | contract | → `cliente_contrato` (optional) |
| `id_filial` | branch | → `filial` (optional) |
| `id_assunto` | subject | → `su_oss_assunto` (same registry as OS; `finalidade` AT/AM). Postman marks it required, the catalog does not; send it whenever known |
| `id_circuito` | circuit | only when circuits are enabled; auto-fills customer/login/contract |
| `id_estrutura` | own structure | → `estrutura`, for `tipo=E` |
| `titulo` | title | **REQ**, max 200 |
| `menssagem` | opening description | **REQ**. Note IXC's spelling with **double s** (`menssagem`); `mensagem` is ignored here |
| `id_ticket_setor` | department | **REQ**, → `su_ticket_setor` (not `empresa_setor`) |
| `prioridade` | priority | **REQ**. `B`=Baixa, `M`=Normal, `A`=Alta, `C`=Crítica. Normal is **`M`** here (OS uses `N`) |
| `su_status` | ticket status | **REQ**. `N`=Novo, `P`=Pendente, `EP`=Em progresso, `S`=Solucionado, `C`=Cancelado. Insert with `N` |
| `melhor_horario_reserva` | customer's preferred period | `M`=Manhã, `T`=Tarde, `N`=Noite, `Q`=Qualquer (default) |
| `data_reservada` | reserved date | max 10 (date) |
| `data_criacao`, `data_ultima_alteracao` | created / last changed | set by IXC; sort by `su_ticket.data_criacao desc` for history |
| `origem_endereco` | where the address comes from | `C`=Cliente, `L`=Login, `CC`=Contrato, `M`=Manual (default) |
| `origem_endereco_estrutura` | address source for `tipo=E` | `E`=Estrutura (default), `M`=Manual |
| `endereco`, `latitude`, `longitude` | address / coordinates | lat/long read-only |
| `id_responsavel_tecnico` | responsible employee | → `funcionarios` |
| `id_usuarios` | IXC user (operator) | → `usuarios` |
| `id_resposta` | canned answer used | → `su_oss_respostas` |
| `id_wfl_processo` | workflow process | → `wfl_processo` |
| `id_evento_status_processo` | complementary status | → `su_evento_status` |
| `id_canal_atendimento` | service channel | → `su_canal_atendimento` |
| `id_su_diagnostico` | diagnosis | → `su_diagnostico` |
| `id_ticket_origem` | origin | `I`=Interna (default), `H`=Hotsite |
| `interacao_pendente` | who owes the next interaction | `E`=Externa, `I`=Interna, `N`=Nenhuma (default), `A`=Ambos |
| `status` | internal flag | default `T` (meaning undocumented) |
| `mensagens_nao_lida_cli` / `_sup` | unread counters (customer / support) | default `0` |
| `finalizar_atendimento` | close flag | default `N` |
| `origem_cadastro` | record origin | default `P` |
| `cliente_fone`, `cliente_telefone_celular`, `cliente_whatsapp`, `cliente_email`, … | customer contact snapshot | read-only copies from `cliente` |
| `atualizar_cliente`, `atualizar_login` | update customer/login coordinates | checkbox, default `S` |

Relations: `id_cliente` → `cliente`, `id_login` → `radusuarios`, `id_contrato` → `cliente_contrato`, `id_assunto` →
`su_oss_assunto`, `id_ticket_setor` → `su_ticket_setor`, `id_responsavel_tecnico` → `funcionarios`. An OS opened
from a ticket carries `su_oss_chamado.id_ticket`.

List a customer's tickets (newest first):
```json
{ "qtype": "su_ticket.id_cliente", "query": "<id_cliente>", "oper": "=", "page": "1", "rp": "20",
  "sortname": "su_ticket.data_criacao", "sortorder": "desc" }
```
Read `id`, `su_status`, `data_criacao`, `titulo`, `menssagem`, `protocolo`. Open tickets only: add
`grid_param` `[{"TB":"su_ticket.su_status","OP":"IN","P":"N,P,EP"}]` (or three separate `!=` filters if `IN` is
not accepted on the installation).

Minimal insert (write; creates a ticket the ISP staff will see):
```json
{ "tipo": "C", "id_cliente": "<id_cliente>", "titulo": "<short title>", "id_ticket_setor": "<id_su_ticket_setor>",
  "prioridade": "M", "menssagem": "<description>", "su_status": "N",
  "protocolo": "<from gerar_protocolo_atendimento>", "id_assunto": "<id_su_oss_assunto>",
  "id_login": "<id_radusuarios>", "id_contrato": "<id_cliente_contrato>", "id_filial": "<id_filial>",
  "melhor_horario_reserva": "Q" }
```
The Postman insert lists every column with empty strings; empty optional fields can be omitted on insert (but not
on `PUT`, see [request mechanics](requests.md)).

### `su_mensagens` — ticket interactions (Mensagens / Interagir)
Operations: list / insert / update / delete. Each row is one interaction on a ticket; inserting one is also how
the "Interagir" buttons change the ticket status (see Actions).

| Field | Meaning | Values / notes |
|---|---|---|
| `id_ticket` | ticket | **REQ**, → `su_ticket` |
| `id_cliente` | customer | **REQ** in Postman |
| `mensagem` | interaction text | **REQ** (single s here) |
| `mensagem_ticket` | ticket text | **REQ** in Postman (sent together with `mensagem`) |
| `su_status` | ticket status after this interaction | **REQ**. `N`, `P`, `EP`, `S`, `C` (same codes as `su_ticket.su_status`) |
| `visibilidade_mensagens` | visibility | **REQ**; Postman example `P` (likely Pública vs internal; other codes undocumented, inferred) |
| `existe_pendencia_externa` | external pending flag | **REQ**; Postman example `E` (codes undocumented) |
| `id_resposta` | canned answer | → `su_oss_respostas` |
| `id_evento_status` | complementary status event | → `su_evento_status` (inferred) |
| `id_su_diagnostico` | diagnosis | → `su_diagnostico` |
| `operador`, `data`, `titulo`, `assunto_ticket` | operator, date, title, subject | optional |

List: `qtype: su_mensagens.id_ticket`, `oper: =`, sort `su_mensagens.id desc`.

### `su_ticket_arquivos` — ticket attachments (Arquivos do atendimento)
Operations: list (`qtype: su_ticket_arquivos.id_ticket`) / insert / delete. Insert is **multipart form-data**, not
JSON: fields `descricao`, `local_arquivo` (the file), `id_ticket`. Download with `su_ticket_arquivos_28010`.

### `su_transf_atendimento` — ticket transfer history (Movimentações/Histórico)
Operations: list only (`qtype: su_transf_atendimento.id`, `rp` 100 in Postman). One row per department transfer;
filter by the ticket field to audit a ticket's path. New rows come from `su_transf_atendimento_26466`.

### `su_oss_chamado` — service order (Ordem de serviço, OS)
Operations: list / insert / update (`PUT /su_oss_chamado/<id>`, full record) / delete. `tipo=C` for customer OS,
`tipo=E` for the ISP's own structure. After insert, move the OS with the action endpoints below; do not edit
`status` directly.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | OS id | autoincrement |
| `tipo` | OS kind | **REQ** (Postman). `C`=Cliente (default), `E`=Estrutura própria (then `id_estrutura` and `origem_endereco_estrutura` required) |
| `id_assunto` | subject | **REQ**, → `su_oss_assunto`. The subject drives SLA, default answer, print layout and what the finishing wizard demands |
| `id_cliente` | customer | → `cliente`; required for `tipo=C` |
| `id_filial` | branch | **REQ**, → `filial` |
| `id_login` | login | → `radusuarios` |
| `id_contrato_kit` | contract | → `cliente_contrato` (the contract field is named `id_contrato_kit`, not `id_contrato`) |
| `id_ticket` | originating ticket | → `su_ticket`, read-only |
| `protocolo` | protocol | max 20; `gerar_protocolo_ordem_servico` |
| `origem_endereco` | address source | **REQ**. `C`=Cliente, `L`=Login, `CC`=Contrato, `M`=Manual (default) |
| `origem_endereco_estrutura` | address source for `tipo=E` | `E`=Estrutura (default), `M`=Manual |
| `prioridade` | priority | **REQ**. `B`=Baixa, `N`=Normal (default), `A`=Alta, `C`=Crítica. The Postman example sends `"1"`; use the catalog letters |
| `melhor_horario_agenda` | preferred period | `M`=Manhã, `T`=Tarde, `N`=Noite, `Q`=Qualquer (default) |
| `setor` | sector responsible | **REQ**, → **`empresa_setor`** (not `su_ticket_setor`) |
| `id_tecnico` | technician | → `funcionarios` |
| `mensagem` | OS description | max 10000 (single s) |
| `mensagem_resposta` | closing answer text | max 400 |
| `status` | OS status | **REQ**. `A`=Aberta, `AN`=Análise, `EN`=Encaminhada, `AS`=Assumida, `AG`=Agendada, `DS`=Deslocamento, `EX`=Execução, `F`=Finalizada, `RAG`=Aguardando agendamento. Insert with `A` |
| `id_su_diagnostico` | diagnosis | → `su_diagnostico` |
| `id_wfl_param_os`, `id_wfl_tarefa` | workflow config / current task | → `wfl_parametro_oss`, `wfl_tarefa` |
| `origem_os_aberta` | why it was opened | `M`=Manual, `P`=Processo, `CRM`=Cobrança, `CC`=Cancelamento de contrato |
| `origem_cadastro` | record origin | `P`, `SV` (Service mobile app, inferred) |
| `status_conexao` | login online? | `S`=Online, `N`=Offline (computed) |
| `status_assinatura` | customer signature | `A`=Pendente (default), `F`=Assinada |
| `status_pesquisa_satisfacao` | satisfaction survey | `1`=Enviado, `2`=Respondida, `3`=Expirada |
| `gera_comissao` | generates technician commission | `S` (default) / `N` |
| `liberado` | released | `1`=Sim (default), `2`=Não |
| `impresso` | printed | `S` / `N` (default) |
| `id_atendente` | attendant | REQ in the catalog, filled by IXC from the API user |
| `data_abertura`, `data_inicio`, `data_hora_analise`, `data_hora_encaminhado`, `data_hora_assumido`, `data_hora_execucao`, `data_final`, `data_fechamento` | life-cycle timestamps | read-only, set by the actions |
| `data_agenda`, `data_agenda_final` | scheduled window | read-only; set by `su_oss_chamado_reagendar` |
| `data_reservada`, `data_prazo_limite`, `data_prev_final`, `data_reagendar` | reserved date, deadline, expected end, reschedule date | |
| `id_cidade`, `bairro`, `endereco`, `complemento`, `referencia`, `id_condominio`, `bloco`, `apartamento`, `latitude`, `longitude` | service address (manual origin) | |
| `regiao_manutencao`, `ids_login_regiao_manutencao` | maintenance region / affected logins | see `su_oss_chamado_regiao_manutencao_radusuarios` |
| `status_sla`, `justificativa_sla_atrasado` | SLA status / late justification | |
| `valor_total`, `valor_outras_despesas`, `valor_unit_comissao`, `valor_total_comissao` | totals and commission | money |

List a customer's OS: `qtype: su_oss_chamado.id_cliente`, `oper: =`, sort `su_oss_chamado.id desc`; open ones:
`grid_param` `[{"TB":"su_oss_chamado.status","OP":"!=","P":"F"}]`.

Minimal customer OS insert (write; appears in the technicians' queue and may notify them):
```json
{ "tipo": "C", "id_assunto": "<id_su_oss_assunto>", "id_cliente": "<id_cliente>", "id_filial": "<id_filial>",
  "id_contrato_kit": "<id_cliente_contrato>", "id_login": "<id_radusuarios>", "origem_endereco": "M",
  "prioridade": "N", "melhor_horario_agenda": "Q", "setor": "<id_empresa_setor>", "mensagem": "<description>",
  "status": "A", "protocolo": "<from gerar_protocolo_ordem_servico>" }
```
With `origem_endereco` `C`/`L`/`CC` IXC copies the address from customer/login/contract; with `M` send the
address fields if the technician needs them.

### `su_oss_chamado_mensagem` — OS interactions / history (Mensagens OS)
Operations: list (`qtype: su_oss_chamado_mensagem.id_chamado`) / insert / update / delete. Also the "Registrar
mensagem" action (same endpoint, see Actions).

| Field | Meaning | Values / notes |
|---|---|---|
| `id_chamado` | OS | **REQ**, → `su_oss_chamado` |
| `id_evento` | event | **REQ**, → `su_oss_evento` |
| `mensagem` | text | **REQ** |
| `status` | OS status recorded with the message | **REQ**; OS status codes (`A`, `AN`, …) |
| `tipo_cobranca` | charge type of the interaction | **REQ**; Postman `NENHUM` (no charge). Other values undocumented; anything else may bill the customer (inferred) |
| `finaliza_processo` | ends the workflow process | **REQ**, `S`/`N` |
| `id_resposta` | canned answer | → `su_oss_respostas` |
| `id_tecnico`, `id_equipe` | technician / team | → `funcionarios`, `su_equipe` |
| `data_inicio`, `data_final`, `data` | work window / date | |
| `id_evento_status`, `id_proxima_tarefa` | complementary status / next workflow task | |
| `latitude`, `longitude`, `gps_time` | technician location | |

### `su_oss_chamado_arquivos` — OS attachments (Arquivos)
Operations: list (`qtype: su_oss_chamado_arquivos.id_oss_chamado`) / insert / delete. Insert is **multipart
form-data**: `descricao`, `local_arquivo` (file), `id_oss_chamado`, `classificacao_arquivo`. View with
`visualizar_arquivo_os`. The wizard variant is `su_oss_chamado_arquivos_wiz` (same fields).

### `su_oss_mov_produto` — products and assets used on the OS (Produtos)
Operations: list / insert / update / delete. Stock movement attached to an OS. The **search prefix is
`movimento_produtos`**, not the endpoint name: `qtype: movimento_produtos.id_oss_chamado`. Product lines:
`grid_param` on `movimento_produtos.id_produto >= 1`; asset (patrimônio) lines: `movimento_produtos.id_patrimonio >= 1`.

| Field | Meaning | Values / notes |
|---|---|---|
| `id_oss_chamado` | OS | **REQ** |
| `id_produto` | product | **REQ**, → `produtos` |
| `id_patrimonio`, `numero_patrimonial`, `patrimonio` | asset id / asset tag | **REQ** for asset lines |
| `data` | movement date | **REQ**, format **`DD/MM/YYYY`** in Postman (not ISO) |
| `id_unidade`, `unidade_sigla`, `fator_conversao` | unit, unit symbol (`UND`), conversion factor | **REQ** |
| `id_almox` | warehouse the item leaves | **REQ**, → `almox` |
| `qtde_saida` | quantity | **REQ** |
| `valor_unitario`, `valor_total` | unit / total price | **REQ**, money; may end up billed to the customer (see risk) |
| `pdesconto`, `vdesconto`, `pcomissao` | discount %, discount value, commission % | |
| `id_classificacao_tributaria` | tax classification | **REQ**, → `cnf_classificacao_tributaria` |
| `tipo` | product kind | **REQ**. `C`=Comércio, `S`=Serviço, `F`=Fabricação, `M`=Matéria prima, `P`=Patrimônio, `O`=Consumo |
| `estoque` | controls stock | **REQ**, `S`/`N` |
| `numero_serie`, `garantia_oss`, `id_terceiro_oss`, `id_su_oss_kit_equipamento`, `id_pedido_os`, `id_saida` | serial, warranty, third party, kit, sale order, stock exit | |

Risk: moves stock out of the warehouse; depending on the subject (`su_oss_assunto.id_tipo_doc_pedido`,
`id_cond_pag_produto`, `fat_somente_finalizada`) items become an OS sale order (`pedido_os` / `vd_saida_fat_os`)
billed to the customer (inferred from the subject fields).

### `su_oss_mov_comodato_wiz` — equipment lent to the customer through the OS (Comodato)
Operations: list / insert / update / delete. Same `movimento_produtos` prefix; listing filters
`movimento_produtos.status_comodato = E`. Fields as `su_oss_mov_produto` plus: `id_contrato` (**REQ**, contract
receiving the equipment), `filial_id` (**REQ**), `id_login`, `mac`, `status_comodato` (**REQ**, `E` in all
examples; meaning "entregue/em comodato", inferred), `status_patrimonio`, `tipo_produto`. For asset lines
`id_patrimonio`, `patrimonio`, `numero_patrimonial`, `status_patrimonio`, `mac` and `tipo_produto` are required
(Postman: "if not sent, it stays hidden in the interface"). Postman edits product-type comodato rows with
`PUT /su_oss_mov_produto/<id>` and asset rows with `PUT /su_oss_mov_comodato_wiz/<id>`; deletes likewise.
Note: the Postman comodato listing `grid_param` is malformed (`"OP":"=", ">=":"1"`); write it as
`{"TB":"movimento_produtos.id_produto","OP":">=","P":"1"}`.
Risk: links equipment to the contract and moves stock; affects later return/charge of the equipment.

### `su_oss_mov_servico_wiz` — services charged on the OS (Serviços)
Operations: list (`qtype: movimento_produtos.id_oss_chamado`) / insert / update / delete.
Insert fields (Postman comments): `id_oss_chamado` **REQ**, `descricao` **REQ** (service description), `data`
**REQ** (`DD/MM/YYYY`), `id_unidade` **REQ** (→ `produtos_unidades`), `qtde_saida` **REQ**, `valor_unitario`
**REQ**, `valor_total` **REQ**, `id_terceiro_oss` (supplier), hidden fields from the product registry:
`id_produto` (→ `produtos`), `id_classificacao_tributaria` **REQ**, `tipo` **REQ** (`S` for services; codes as
above), `estoque` **REQ** `S`/`N`, `filial_id`, `unidade_sigla` (`SER`), `fator_conversao` **REQ**,
`garantia_oss` `N`, `tipo_produto` default `S`.
Risk: **charges money** — a service line with a value is billed to the customer per the subject's
`id_tipo_doc_servico` / `id_cond_pag_servico` (inferred). Confirm value and customer agreement first.

### `su_oss_chamado_regiao_manutencao_radusuarios` — logins affected by a maintenance OS (Logins afetados)
Operations: list / insert / delete. Insert (all required): `id_radusuarios` (→ `radusuarios`), `id_su_oss_chamado`,
`id_su_oss_chamado_regiao_manutencao`. Used for outage/maintenance-region OS; subjects with
`conceder_desconto_login_regiao_manutencao=S` may grant those logins a discount (billing impact, inferred).

### `su_oss_assunto` — subjects for tickets and OS (Assunto)
Operations: list / insert / update / delete. Read it to pick `id_assunto` and to know what finishing an OS will
demand. Insert requires `assunto`, `ativo`, `layout_impressao`, `numero_de_vias`, `exige_comodato_finalizar_os`,
`exige_produto_finalizar_os`, `tipo_comissao` (plus `quantidade_equipamentos` / `quantidade_produtos` when the
matching `exige_*` is `S`); the catalog also marks `considerar_sla` and `metas_horas_abertura_ticket` required.

| Field | Meaning | Values / notes |
|---|---|---|
| `assunto` | subject name | **REQ**, max 100 |
| `ativo` | active | `S`/`N` |
| `tipo` | applies to | `C`=Cliente, `E`=Estrutura, `A`=Ambos (default) |
| `finalidade` | used by | `OS`=Ordem de serviço, `AT`=Atendimento, `AM`=Ambos (default). Filter on it when picking a subject |
| `endereco_padrao` | default address source | `C`, `L` (default), `CC`, `M`, `E` |
| `prioridade_padrao` | default priority | `B`, `N` (default), `A`, `C` |
| `setor_su_oss_chamado` | default OS sector | → `empresa_setor` |
| `id_processo`, `obrigar_processo_atendimento` | workflow process / force it | → `wfl_processo`; `S`/`N` |
| `contrato_obrigatorio`, `login_obrigatorio` | contract / login required on the OS | `S`/`N` |
| `permite_abrir_cliente_atraso` | allow OS for customers in arrears | `S`, `N`, `P`=Padrão |
| `id_resposta_padrao`, `id_resposta_padrao_finalizacao` | default answers (open / close) | → `su_oss_respostas` |
| `exige_fotos_finalizacao_os` + `quantidade_fotos_finalizacao_os` | photos required to finish | `S`/`N`, count |
| `exige_comodato_finalizar_os` + `quantidade_equipamentos` | comodato required to finish | |
| `exige_produto_finalizar_os` + `quantidade_produtos` | products required to finish | |
| `diagnostico_obrigatorio_finalizacao_os`, `equipe_obrigatoria_finalizacao_os` | diagnosis / team required to finish | |
| `localizacao_obrigatoria_cliente_finalizacao_os`, `localizacao_obrigatoria_login_finalizacao_os` | location required to finish | |
| `wiz_comodato`, `wiz_produtos`, `wiz_mensalidade`, `wiz_autorizar_ONU`, `wiz_localizacao`, `wiz_arquivos`, `wiz_resumo_os`, `wiz_servico` | finishing-wizard tabs | `M`=Mostrar, `E`=Esconder |
| `wiz_assinatura_obrig`, `habilita_assinatura_cliente`, `integracao_assinatura_digital` | signature | |
| `considerar_sla` | SLA counted from | `AB`=Abertura (default), `AG`=Agendamento |
| `meta_horas_abertura`, `meta_horas_agendamento`, `metas_horas_abertura_ticket` | SLA hours | default `72.0` |
| `sla_apenas_dias_uteis` | business days only | `S`, `N`, `P`=Padrão |
| `validar_choque_horarios_agendamento_os` | block overlapping schedules | `S`/`N` |
| `tipo_comissao`, `valor_comissao` | commission | `F`=Fixa, `H`=Por hora |
| `id_tipo_doc_*`, `id_cond_pag_*`, `fat_somente_finalizada`, `tipo_cobranca` (default `NENHUM`), `id_vendedor_faturamento` | how OS products/services/comodato are invoiced | `fat_somente_finalizada=S` invoices only finished OS |
| `layout_impressao` | built-in print layout | `1`=Assistência Internet Rádio, `2`=Assistência Fibra, `3`=Instalação Rádio, `4`=Instalação Fibra, `5`=Serviço de Manutenção, `6`=Chamado Técnico, `7`=OS simples, `8`=OS Simples Modelo 2, `9`=Assistência Modelo 2, `10`=OS Instalação Modelo 2, `11`=Instalação Rádio Modelo 2, `12`=OS fibra |
| `su_oss_modelo_impressao`, `numero_de_vias`, `modelo_email` | custom print model, copies, e-mail model | → `su_oss_modelo_impressao` |
| `mostra_hotsite`, `mostrar_no_service` | visible in hotsite / Service app | |
| `wiz_service_mobile_enviar_sms_deslocamento` | notify customer when technician is on the way | `N`=Não notificar, `S`=Por SMS (default), `O`=WhatsApp (Opa Suite) — **messages the end customer** on `DS` |
| `id_checklist`, `id_feedback`, `mostrar_checklist_analise_risco` (`i`/`F`/`N`) | checklist, satisfaction survey, risk checklist | |

### `su_ticket_setor` — ticket departments (Departamento do atendimento)
Operations: list / insert / update / delete. Source of `su_ticket.id_ticket_setor` and of
`su_transf_atendimento_26466` department ids. In the Postman collection it sits under "Folha de pagamento →
Cadastros → Departamentos". Fields: `setor` (**REQ**, name), `ordem` (**REQ**, sort, default 10), `ativo`
(**REQ** in Postman, `S`/`N`), `email`, `presta_atendimento` (provides support), `mostra_hotsite`,
`exige_vinculo_produto` (checkboxes, default `S`).

### `empresa_setor` — company sectors (Setor)
Operations: list / insert / update / delete. Source of `su_oss_chamado.setor`, `su_diagnostico.id_setor`,
`su_oss_respostas.setor`, `su_oss_assunto.setor_su_oss_chamado`. Fields: `setor` (**REQ**), `ativo` (**REQ**,
`S`/`N`), `id_depto` (→ `su_ticket_setor`, the department this sector belongs to), `cor`, `recebe_telegram_setor`
(default `N`), `token_bot_telegram_setor`, `empresa_setor_chatid_telegram` (Telegram notification of the sector;
the bot token is a secret, never echo it).

### Other registries

| Table | Purpose (UI label) | Operations | Key fields |
|---|---|---|---|
| `su_diagnostico` | diagnoses for tickets/OS (Diagnóstico de suporte) | list / insert / update / delete | `descricao` **REQ** (max 150), `ativo` **REQ** `S`/`N`, `id_setor` → `empresa_setor` |
| `su_equipe` | technician teams (Equipe) | list / insert / update / delete | `descricao` **REQ** (max 100), `ativo` `S`/`N` |
| `funcionarios_equipes` | team members (Colaboradores da Equipe) | list / insert / update / delete | all required: `id_equipe` → `su_equipe`, `id_funcionario` → `funcionarios`, `percentual_comissao` (e.g. `1.0`) |
| `su_oss_evento` | OS event types (Cadastro de eventos) | list / insert / update / delete | `descricao` **REQ**. Source of `id_evento` in OS actions/messages |
| `su_oss_respostas` | canned answers (Resposta) | list / insert / update / delete | `titulo` **REQ**, `resposta` **REQ**, `ativo` **REQ**, `su_status` **REQ** (ticket status it applies: `N`, `P`, `EP` default, `S`, `C`), `interacao_pendente` **REQ** (`E`, `I` default, `N`, `A`), `setor` → `empresa_setor`, `id_evento_status_processo` → `su_evento_status` |
| `su_oss_modelo_impressao` | custom OS print models (OS modelos) | list / insert / update / delete | both required: `nome` (max 150), `texto` (HTML template); `os_teste_impressao` → `su_oss_chamado` |

### Workflow (`wfl_*`, Configurações → Processos)

| Table | Purpose | Operations | Key fields |
|---|---|---|---|
| `wfl_processo` | workflow process (Processo) | list / insert / update / delete | **REQ**: `id_depto` (→ `su_ticket_setor`, inferred), `descricao`, `ativo` `S`/`N`; `ultima_atualizacao`, `operador_ultima_atualizacao` |
| `wfl_tarefa` | process task (Tarefa) | list (`qtype: wfl_tarefa.id_processo`, sort `wfl_tarefa.id asc`) / insert / update / delete | **REQ**: `id_processo`, `id_setor`, `descricao`, `sequencia`, `id_proxima_tarefa`. Others: `prazo_minutos`, `ativo`, `permite_finalizar` `S`/`N`, `finaliza_processo` `S`/`N`, `gera_comissao` (example `ROS`, codes undocumented), `origem_prioridade_os` (example `OS`), `decisao` `S`/`N` (decision task), `obrigatorio` `S`/`N`, `id_tarefa_anterior` |
| `wfl_interacoes` | automatic interactions fired by a task (Interação) | list (`qtype: wfl_interacoes.id_tarefa`) / insert / update / delete | `id_tarefa`, `id_wfl_param_os`, `id_email`, `id_sms`, `su_status_evento`, `ativa_contrato` `S`/`N` (**activates the contract**), `destinatario_email` (example `C`), `email_destino`, `dispara_proxima` `S`/`N`, `gatilho` (example `Conclusao`), `ativo`. Postman sends insert/edit to `/wfl_tarefa` — a collection error; use `/wfl_interacoes` (inferred) |
| `wfl_parametro_oss` | OS auto-open configuration (Configurações ordem de serviço) | list / insert / update / delete | `descricao`, `id_assunto` → `su_oss_assunto`, `id_setor`, `id_tecnico`, `prioridade` (example `N`), `processo` (example `NE`, codes undocumented), `id_wfl_processo`, duplicate rules `abre_duplicada_cliente`, `abre_duplicada_contrato`, `abre_duplicada_areceber`, `considera_contrato_inativo`, `considera_contrato_negativado`, `considera_finalizada` (`S`/`N`). Postman shows an `IXC_Session` cookie on this request; it is a browser artifact, use normal Basic auth |

Workflow registries change how every future ticket/OS behaves (emails, SMS, contract activation). Treat any
write to them as an admin change and get explicit confirmation.

## Actions

All are `POST` to `/<action>` with a JSON body and **no** `ixcsoft` header unless stated. `id_chamado` is the OS id
(`su_oss_chamado.id`). Common optional fields: `id_evento` (→ `su_oss_evento`), `id_resposta` (→
`su_oss_respostas`), `mensagem` (text recorded in the OS history), `data` (action date; empty = now, inferred),
`latitude` / `longitude` / `gps_time` (technician location, mobile app). Each action records an
`su_oss_chamado_mensagem` row and updates `su_oss_chamado.status` and the matching timestamp. Check the response
`type`; a refusal (wrong current status, missing wizard requirement, restricted user) comes back as HTTP 200
`type: error`.

### `gerar_protocolo_atendimento` — reserve a ticket protocol number
`POST /gerar_protocolo_atendimento`, empty body. Returns the next protocol for a ticket; put it in
`su_ticket.protocolo`. Response shape is not documented in the collection: log the raw response once and read the
number from it. Effect: write (consumes a sequence number, nothing else). Low risk.

### `gerar_protocolo_ordem_servico` — reserve an OS protocol number
`POST /gerar_protocolo_ordem_servico`, empty body. Same as above for `su_oss_chamado.protocolo`. Low risk.

### `su_mensagens` "Interagir" buttons — change ticket status with an interaction
`POST /su_mensagens` with `id_ticket`, `id_cliente`, `mensagem`, `mensagem_ticket`, `visibilidade_mensagens`,
`existe_pendencia_externa`, optional `id_resposta`, `id_evento_status`, `id_su_diagnostico`, and `su_status`:
`N` (Novo), `P` (Pendente), `EP` (Em progresso), `S` (Solucionado — closes), `C` (Cancelado — cancels).
Effect: write. `S`/`C` end the ticket; public interactions are visible to the end customer in the hotsite/app and
may notify them (inferred). Confirm text and status with the user.

### `su_transf_atendimento_26466` — transfer a ticket to another department ("Transferir atendimento")
`POST /su_transf_atendimento_26466`. Body: `id_atendimento` (ticket id, `su_ticket.id`), `data_transferencia`
(`DD/MM/AAAA hh:mm:ss`), `id_departamento_origem`, `id_departamento_destino` (both → `su_ticket_setor`),
`id_responsavel_tecnico` (→ `funcionarios`). Effect: write; changes the ticket's department/owner and adds a
`su_transf_atendimento` row. Medium risk (ticket leaves the current queue).

### `su_ticket_arquivos_28010` — download a ticket attachment ("Visualizar arquivo do atendimento")
`GET /su_ticket_arquivos_28010`, body `{ "id": "<su_ticket_arquivos.id>" }`. Effect: read (returns the file).

### `visualizar_arquivo_os` — download an OS attachment ("Visualizar arquivo da O.S")
`GET /visualizar_arquivo_os`, header `ixcsoft: listar`, body `{ "id": "<su_oss_chamado_arquivos.id>" }`. Read.

### `su_oss_chamado_analisar` — put an OS in analysis ("Analisar", status `AN`)
Body: `id_chamado`, `id_setor`, `id_tecnico`, `mensagem`, `data_inicio`, `data_final`, `status: "AN"`, `data`,
`id_evento`, location fields. Effect: write (status change). Low risk.

### `su_oss_chamado_alterar_setor` — forward an OS ("Encaminhar" / "Encaminhar (alterar setor)", status `EN`)
Body: `id_chamado`, `id_setor` (→ `empresa_setor`), `id_tecnico`, `id_assunto` (may change the subject),
`mensagem`, `status: "EN"`, `data`, `id_evento`, location. Effect: write; moves the OS to another sector and/or
technician (the technician gets it in their queue/app). Both Postman entries are the same call.

### `su_oss_chamado_32982` — technician assumes the OS ("Assumir", status `AS`, inferred)
`POST /su_oss_chamado_32982`, body `{ "id_chamado": "<id>" }` (the OS being assumed). The API user's employee
becomes the one handling it (inferred). Effect: write.

### `su_oss_chamado_reagendar` — schedule or reschedule ("Agendar" `AG` / "Reagendar" `RAG`)
Body: `id_chamado`, `data_agendamento`, `data_agendamento_final` (scheduled window; format not documented, use the
installation's `DD/MM/YYYY HH:MM:SS` convention, inferred), `id_resposta`, `mensagem`, `id_tecnico`, `id_equipe`
(→ `su_equipe`), `status` (`AG` for Agendar; Postman uses `RAG` for Reagendar), `data`, `id_evento`,
`id_compromisso` (agenda entry), location. Effect: write; fills `data_agenda` / `data_agenda_final`, books the
technician's agenda. The subject may reject overlapping times (`validar_choque_horarios_agendamento_os`). Tell the
user the customer will expect a visit in that window. IXC's n8n node also lists `su_oss_chamado_reagendar_28895`
(no parameters documented).

### `su_oss_chamado_reagendamento` — mark for rescheduling ("Marcar para reagendamento", status `RAG`)
Body: `id_chamado`, `id_resposta`, `mensagem`, `status: "RAG"` (Aguardando agendamento), `data`, `id_evento`,
`id_compromisso`, location, `id_setor` (sector that must reschedule), `id_tecnico`. Effect: write; clears the visit
from the current schedule (inferred) and returns the OS to the scheduling queue.

### `su_oss_chamado_mensagem` — record a message on the OS ("Registrar mensagem")
`POST /su_oss_chamado_mensagem`, fields as the table above (`id_chamado`, `id_evento`, `mensagem`, `status`,
`tipo_cobranca`, `finaliza_processo`, optional `id_tecnico`, `id_equipe`, `data_inicio`, `data_final`,
`id_evento_status`, `id_proxima_tarefa`, location). With a different `status` it also moves the OS (e.g. `DS`
Deslocamento, which can SMS/WhatsApp the customer per the subject; inferred — no dedicated `DS` action exists in
the collection). Keep `tipo_cobranca: "NENHUM"` unless the user asked to charge. Effect: write.

### `su_oss_chamado_executar` — start execution ("Executar", status `EX`)
Body: `id_chamado`, `data_inicio`, `data_final`, `id_resposta`, `mensagem`, `id_tecnico`, `id_equipe`,
`gera_comissao`, `status: "EX"`, `data`, `id_evento`, `id_su_diagnostico`, `justificativa_sla_atrasado`,
`id_evento_status`, location, and the workflow fields (below). Effect: write.

### `su_oss_chamado_fechar` — finish the OS ("Finalizar" / "Finalizar com tarefa", status `F`)
Body, OS part: `id_chamado`, `data_inicio`, `data_final`, `id_resposta`, `mensagem`, `id_tecnico`, `id_equipe`,
`gera_comissao` / `gera_comissao_aux` (`S`/`N`, technician commission), `status: "F"`, `data`, `id_evento`,
`id_su_diagnostico` (required when the subject demands a diagnosis), `justificativa_sla_atrasado` (when past SLA),
location (required when the subject demands it).
Workflow part (must match `wfl_tarefa` of the OS's process; leave empty for OS without process): `id_processo`,
`id_tarefa_atual`, `eh_tarefa_decisao` (current task is a decision), `sequencia_atual`, `proxima_sequencia_forcada`,
`finaliza_processo_aux`, `id_evento_status`, `id_proxima_tarefa`, `id_proxima_tarefa_aux`.
Effect: write, **hard to undo** (only `su_oss_chamado_reabrir`). Can trigger workflow interactions (e-mail/SMS to
the customer, contract activation via `wfl_interacoes.ativa_contrato`), commission, invoicing of OS products and
services (`fat_somente_finalizada`) and the satisfaction survey. Fails if the subject's wizard requirements (photos,
comodato, products, team, diagnosis, location, signature) are not met — run the wizard recipe first. IXC's n8n
node also exposes `su_oss_chamado_fechar_wiz_29956`, `enviar_wifi_acs`, `sincronizar_dispositivo_acs` (wizard
close / ACS Wi-Fi push / device sync; parameters undocumented, do not call blind).

### `su_oss_chamado_reabrir` — reopen a finished OS ("Reabrir", status `A`)
Two shapes in the collection, both with header **`ixcsoft: listar`**:
- `POST /su_oss_chamado_reabrir`, body `{ "id_chamado": "<id>", "status": "A", "mensagem": "<reason>",
  "id_operador": "", "data": "", "id_evento": "", "id": "", "id_tecnico": "" }`.
- `POST /su_oss_chamado_reabrir/<id_chamado>`, body with `"id": "<id>"` instead of `id_chamado`.
Required: OS id, `status` must be `A`, `mensagem`. Effect: write; reopens SLA and the technician queue.

### Print and e-mail
| Endpoint | What it does | Body | Effect |
|---|---|---|---|
| `GET /imprimir_jato_laser_os` | print the OS, standard inkjet/laser model ("Jato de Tinta/Laser") | `{ "id": "<OS id>" }` | read (returns printable document; may set `impresso=S`, inferred) |
| `GET /imprimir_jato_tinta_com_historico` | print the OS with its history | `{ "id": "<OS id>" }` | read |
| `GET /su_oss_chamado_22873` | print with the subject's custom model ("Do modelo de OS", `su_oss_modelo_impressao`) | `{ "id": "<OS id>" }` | read |
| `GET /botao_rel_23367` | **e-mail the OS to the technician** ("Enviar e-mail ao técnico") | `{ "id": "<OS id>" }` | sends an e-mail; confirm first |

Other OS/ticket endpoints listed only in IXC's n8n node, with no documented parameters (do not call without
testing on a non-production record): `botao_ajax_30002`, `botao_rel_30001` (OS); `su_ticket_26468`,
`su_ticket_26885`, `su_ticket_26886`, `su_mensagens_cliente`, `buscar_endereco_completo_26307` (ticket);
`su_transf_atendimento_26521`; `retornar_deptos_contrato`, `retornar_deptos_usuario`, `retornar_usuarios_depto`
(department lookups, read); `su_oss_mov_comodato_wiz_novo`, `baixar_comodato_23441` (comodato return — stock);
`su_oss_chamado_transf_automatica_29446` / `_29447` (automatic stock transfer).

## Recipes

### Customer support history
1. Find the customer (`cliente`, see [customers](customers.md)) → `id_cliente`.
2. `su_ticket` list by `su_ticket.id_cliente`, sort `su_ticket.data_criacao desc`, `rp` 10–20; read `id`,
   `su_status`, `data_criacao`, `titulo`, `menssagem`, `protocolo`.
3. Details of one ticket: `su_mensagens` by `su_mensagens.id_ticket`; transfers: `su_transf_atendimento`.
4. Service orders: `su_oss_chamado` by `su_oss_chamado.id_cliente`, sort `id desc`; history via
   `su_oss_chamado_mensagem` by `id_chamado`. Translate status codes for the user (`F` = finished, `AG` = scheduled
   with `data_agenda`).

### Open a ticket (write, confirm first)
1. Pick the department: `su_ticket_setor` list, `ativo=S`. Pick the subject: `su_oss_assunto` with `ativo=S` and
   `finalidade` `AT` or `AM`.
2. Optional: `id_contrato` / `id_login` / `id_filial` from the customer's contract and login.
3. `POST /gerar_protocolo_atendimento` → protocol.
4. `POST /su_ticket` with the minimal insert above (`tipo C`, `prioridade M`, `su_status N`, `menssagem`
   double s). Check `type: success`, keep `id`, give the user the protocol.

### Open an OS (write, confirm first)
1. Subject: `su_oss_assunto` with `finalidade` `OS`/`AM`, `ativo=S`; note `setor_su_oss_chamado`,
   `contrato_obrigatorio`, `login_obrigatorio`, `permite_abrir_cliente_atraso`.
2. Sector: the subject's `setor_su_oss_chamado` or an `empresa_setor` chosen by the user (required).
3. Contract (`id_contrato_kit`) and login if the subject demands them; `id_filial` (required).
4. `POST /gerar_protocolo_ordem_servico` (optional) → `protocolo`.
5. `POST /su_oss_chamado` with the minimal insert (`status A`, `origem_endereco M` or `C`/`L`/`CC`).
   An "arrears" or "duplicate OS" error comes from subject / `wfl_parametro_oss` rules; relay it.

### Move an OS through its life cycle
`A` → `su_oss_chamado_analisar` (`AN`) → `su_oss_chamado_alterar_setor` (`EN`, to sector/technician) →
`su_oss_chamado_32982` (`AS`, assume) → `su_oss_chamado_reagendar` (`AG`, schedule) → `su_oss_chamado_mensagem`
with `DS` (on the way, inferred) → `su_oss_chamado_executar` (`EX`) → wizard → `su_oss_chamado_fechar` (`F`).
Not every installation uses every step; IXC accepts skipping (e.g. `A` → `AG` → `F`) unless a workflow process
enforces the order. Can't make the visit: `su_oss_chamado_reagendamento` (`RAG`). Wrongly closed:
`su_oss_chamado_reabrir`.

### Finish an OS through the wizard (ordered; writes, confirm values and charges first)
Order follows the subject's wizard tabs (`wiz_comodato`, `wiz_produtos`, `wiz_localizacao`, `wiz_arquivos`,
`wiz_servico`, `wiz_resumo_os`); the API does not enforce the order, `su_oss_chamado_fechar` only checks the
result (inferred).
1. Read the OS (`su_oss_chamado` by `id`) and its subject (`su_oss_assunto` by `id_assunto`): note
   `exige_fotos_finalizacao_os`/`quantidade_fotos_finalizacao_os`, `exige_comodato_finalizar_os`/
   `quantidade_equipamentos`, `exige_produto_finalizar_os`/`quantidade_produtos`,
   `diagnostico_obrigatorio_finalizacao_os`, `equipe_obrigatoria_finalizacao_os`, `localizacao_obrigatoria_*`,
   `wiz_assinatura_obrig`.
2. Comodato equipment: `POST /su_oss_mov_comodato_wiz` per device (`id_oss_chamado`, `id_contrato`, `id_produto`
   or `id_patrimonio` + `patrimonio` + `numero_patrimonial` + `mac`, `id_almox`, `filial_id`, `data` DD/MM/YYYY,
   unit fields, `status_comodato: "E"`). Verify with the `su_oss_mov_comodato_wiz` listing.
3. Products consumed: `POST /su_oss_mov_produto` per item (warehouse, quantity, value). Values may be billed.
4. Services charged: `POST /su_oss_mov_servico_wiz` per service (only if the user confirmed the charge).
5. Photos/files: `POST /su_oss_chamado_arquivos_wiz` (form-data `id_oss_chamado`, `descricao`, `local_arquivo`,
   `classificacao_arquivo`), as many as `quantidade_fotos_finalizacao_os`; check with the `_wiz` listing
   (`qtype: su_oss_chamado_arquivos.id_oss_chamado`).
6. Logins affected (maintenance OS only): `su_oss_chamado_regiao_manutencao_radusuarios`.
7. `POST /su_oss_chamado_fechar` with `status: "F"`, `mensagem`, `id_tecnico`, `id_equipe`, `id_su_diagnostico`,
   `data_inicio`/`data_final`, location, and the workflow fields if the OS has `id_wfl_tarefa`
   (read `wfl_tarefa` by `id_processo` to fill `id_tarefa_atual`, `sequencia_atual`, `id_proxima_tarefa`).
8. Confirm with `su_oss_chamado` by `id` that `status = F` and `data_fechamento` is set.

### Transfer a ticket to another department
1. `su_ticket` by `id` → current `id_ticket_setor`.
2. Destination from `su_ticket_setor`; optional responsible employee from `funcionarios`.
3. `POST /su_transf_atendimento_26466` with origin, destination, `data_transferencia` `DD/MM/AAAA hh:mm:ss`.
4. Optionally add a `su_mensagens` interaction explaining the transfer.
