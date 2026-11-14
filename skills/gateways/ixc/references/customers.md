# IXC customers, contracts, CRM and customer-facing integrations

This file covers customer records (`cliente`), service contracts (`cliente_contrato`) and their buttons (activation,
block/unblock, temporary release, cancellation, etc.), sale plans (`vd_contratos`), contract products, discounts and
add-ons, comodato equipment, CRM (leads, prospects, negotiations), suppliers and salespeople, location lookups,
TV/SVA logins, and the buttons that message the end customer (SMS, omnichannel, push). Use it to find a customer and
their contracts, or to change contract and access status. Shared mechanics (auth, `ixcsoft: listar`, search body,
`grid_param`, error shape) are in [request mechanics](requests.md); this file does not repeat them.

Sources: official IXC Postman collection "API - IXC Provedor", the field catalog of the IXC wiki, and IXC's official
n8n node. Anything not stated in those sources is marked "(inferred)".

**Safety.** Every insert, update, delete and every "botão" here is a write in the customer's production ERP. Confirm
with the user before any write, and never delete unless the user explicitly asks. These markers flag the effects:
- **[ACCESS]** blocks, unblocks or changes the subscriber's internet access.
- **[MONEY]** creates, cancels or changes receivables (invoices) or prices.
- **[MESSAGES CUSTOMER]** sends something to the end customer.
- **[CANCELS]** is irreversible or hard to undo.

**Date format in this module.** The Postman insert and update examples send dates as `DD/MM/YYYY` (for example
`"data": "18/06/2024"`), and a contract record read back for a button shows `"data_ativacao": "28/09/2026"`.
Timestamps look like `2026-10-02 12:12:24`. For writes, use the format the same record has when you read it.

## Tables

### `cliente` (Cliente, the customer record)
Operations: list, insert, update (`PUT /cliente/<id>`), delete. Start here for nearly every customer task. A
customer has 0..n contracts (`cliente_contrato.id_cliente`). Prospects use the same table with `crm = "S"` (see
`crm_canditados`).

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | customer id | auto-increment. Do not send it on insert. |
| `ativo` | active record | `S` Sim / `N` Não. **Required on insert.** This flag is about the record. Service status lives on the contract. |
| `tipo_pessoa` | person type | `F` Física (individual), `J` Jurídica (company), `E` Estrangeiro (foreigner). **Required.** |
| `razao` | name | The person's full name, or the company's legal name (razão social). **Required.** Always read this as "the customer name". |
| `fantasia` | trade name | Company trade name (nome fantasia). Usually empty for individuals. |
| `nome_social` | social name | optional |
| `cnpj_cpf` | CPF/CNPJ | **Stored with punctuation**: CPF `000.000.000-00`, CNPJ `00.000.000/0000-00` (Postman example `175.181.720-20`). Max 30 characters. Mask the value before searching with `=`. Required on insert per Postman. |
| `ie_identidade` | state registration (IE) or RG | |
| `contribuinte_icms` | ICMS taxpayer | `S` Sim, `N` Não, `I` Isento, `E` Excluído, plus the codes `1` `4` `5` `6` `15` (other countries' fiscal regimes). Postman marks it required (example `I`). |
| `tipo_assinante` | subscriber type | `1` Comercial/Industrial, `2` Poder Público, `3` Residencial/Pessoa física, `4` Público, `5` Semi-Público, `6` Outros. **Required.** |
| `tipo_cliente_scm` | fiscal customer class | `01` Comercial … `03` Residencial/PF … `99` Outros (full list in the catalog). Default `01`. |
| `id_tipo_cliente` | customer group | → `tipo_cliente` |
| `data_nascimento` | birth date, or company founding date | `DD/MM/YYYY` |
| `Sexo` | sex | Capital S. `F`, `M`, `NB`, `O`, `PNI` |
| `estado_civil` | marital status | `Casado`, `Solteiro`, `Divorciado`, `Viúvo` |
| `filial_id` | branch | → `filial`. Users can be restricted to the customers of certain branches. |
| `idx` | external id | integration key for other systems |
| `data_cadastro` | registration date | Filled automatically on insert. Keep the original value on update. |
| `ativo_serasa` | negativation active | `1` Sim, `2` Não. Read-only. |
| `cep`, `endereco`, `numero`, `bairro` | address | All **required on insert**. CEP is masked `00000-000`. |
| `complemento`, `referencia` | address extras | |
| `cidade` | city | **Numeric id** → `cidade.id`. **Required.** Never send a city name. |
| `uf` | state | **Numeric id** → `uf.id`. Read-only, derived from the city. |
| `tipo_localidade` | area type | `U` urbana / `R` rural. **Required.** |
| `moradia` | housing | `P` própria (owned) / `A` alugada (rented) |
| `id_condominio`, `bloco`, `apartamento` | building | → `cliente_condominio` |
| `latitude`, `longitude` | coordinates | read-only in the form |
| `*_cob` (`cep_cob`, `endereco_cob`, `cidade_cob`, …) | billing address | `cidade_cob` → `cidade.id` |
| `fone` | landline | max 20 characters, masked |
| `telefone_celular` | mobile | Free text with a mask. Usually `(DD) 9XXXX-XXXX`. Max 20 characters. |
| `whatsapp` | WhatsApp number | Same mask style as `telefone_celular`. Often empty, or the same number as the mobile. |
| `telefone_comercial`, `ramal` | work phone, extension | |
| `id_operadora_celular` | mobile carrier | → `operadora_telefonia` |
| `email` | main e-mail | max 256 characters |
| `hotsite_email`, `senha` | Central do Assinante login and password | The customer self-service portal login. Never read the password back or echo it. |
| `acesso_automatico_central`, `alterar_senha_primeiro_acesso` | portal behavior | `S`, `N`, `P` (Padrão = system default) |
| `crm` | is a prospect | `S` = still a prospect, not yet a customer. `N` = customer. |
| `status_prospeccao` | CRM stage | `C` Novo, `S` Sondagem, `A` Apresentando, `N` Negociando, `V` Vencemos (won), `P` Perdemos (lost), `AB` Abortamos, `SV` Sem viabilidade, `SP` Sem porta disponível |
| `crm_data_*` | date each CRM stage was reached | |
| `id_candato_tipo` (typo kept), `id_campanha`, `id_concorrente`, `id_perfil`, `id_segmento` | CRM classification | → `crm_tipo_candidato`, `crm_campanha`, `crm_concorrente`, `crm_perfil`, `segmento_crm` |
| `responsavel` | account owner | → `funcionarios` |
| `indicado_por` | referred by | → `cliente` |
| `id_vendedor` | salesperson | → `vendedor` |
| `participa_cobranca`, `participa_pre_cobranca`, `cob_envia_email`, `cob_envia_sms` | joins automated collection (and pre-collection) by e-mail or SMS | `S`/`N`. The full Postman insert body marks `cob_envia_email` and `cob_envia_sms` as required. |
| `regua_cobranca_considera`, `regua_cobranca_wpp`, `regua_cobranca_notificacao` | collection-cadence participation and its WhatsApp and notification channels | `S`, `N`, `P` |
| `grau_satisfacao` | satisfaction | `1` Nada … `5` Completamente satisfeito |
| `obs`, `alerta` | notes, and an alert shown to operators | |

Required on insert (Postman `//Obrigatório`): `ativo`, `tipo_pessoa`, `razao`, `cnpj_cpf`, `contribuinte_icms`,
`tipo_assinante`, `cep`, `endereco`, `numero`, `bairro`, `cidade`, `tipo_localidade`, `cob_envia_email`,
`cob_envia_sms`. Installations can add more required fields under **Parâmetros gerais**. If an insert fails, read the
`message`.

Update: the Postman comment says "É necessário trazer todos os campos" (send every field, even empty ones). List the
record by `cliente.id`, change the fields you need, and `PUT` the whole object back.

```json
{"qtype":"cliente.cnpj_cpf","query":"123.456.789-09","oper":"=","page":"1","rp":"1"}
{"qtype":"cliente.telefone_celular","query":"(11) 98765-4321","oper":"=","page":"1","rp":"5"}
```
Useful result fields: `registros[0].id`, `razao`, `email`, `telefone_celular`, `whatsapp`, `ativo`, `cidade`, `filial_id`.
More than one record can match a phone number; confirm which one with the CPF or the name.

### `cliente_contrato` (Contrato do cliente, the service contract)
Operations: list, insert, update (`PUT /cliente_contrato/<id>`, full record), delete. A contract is one subscription
(internet, phone, services or SVA). Its two status fields decide billing and access. **Change status with the
contract buttons (Actions below), not with a `PUT`.** The buttons also run IXC's side effects: RADIUS
disconnect, history entries and receivables.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | contract id | Use it as `id_contrato` everywhere. |
| `tipo` | service type | `I` Internet, `T` Telefonia, `S` Serviços, `SVA`. **Required.** |
| `id_cliente` | customer | → `cliente`. **Required.** |
| `id_vd_contrato` | sale plan | → `vd_contratos`. **Required.** This is "the plan". |
| `contrato` | contract description | Usually the plan name, e.g. `PLANO TESTE 10 MB`. **Required.** |
| `descricao_aux_plano_venda` | extra plan description | |
| `status` | contract status | `P` Pré-contrato (default), `A` Ativo, `I` Inativo (cancelled/deactivated), `N` Negativado (reported to credit bureaus), `D` Desistiu (gave up before activation) |
| `status_internet` | access status | `A` Ativo, `D` Desativado (default), `CM` Bloqueio Manual, `CA` Bloqueio Automático, `FA` Financeiro em atraso (overdue, warning stage), `AA` Aguardando Assinatura (waiting for signature) |
| `status_velocidade` | speed status | `N` Normal, `R` Reduzida (speed reduced for overdue payment) |
| `situacao_financeira_contrato` | financial situation | read-only, e.g. `R` |
| `data` | financial base date | **Required.** Billing is anchored on this date. |
| `data_ativacao` | activation date | Set by activation. |
| `data_assinatura` | signature date | read-only |
| `data_renovacao`, `data_expiracao`, `renovacao_automatica` | renewal, expiry, auto-renew | `renovacao_automatica` is `S`/`N` and **required**. |
| `fidelidade`, `desconto_fidelidade` | loyalty period in months, and the loyalty discount | |
| `pago_ate_data` | paid-up-to date | read-only |
| `motivo_inclusao` | why the contract was created | `I` Instalação, `U` Upgrade, `D` Downgrade, `M` Mudança de endereço (address change), `T` Mudança de tecnologia (technology change), `L` Mudança de titularidade (ownership transfer), `N` Negociação, `R` Reativação (reactivation) |
| `id_tipo_contrato` | billing type | → `cliente_contrato_tipo`. **Required.** |
| `id_modelo` | print model | → `cliente_contrato_modelo`. **Required.** |
| `id_filial` | branch | **Required.** |
| `id_tipo_documento` | invoice document type | → `tipo_documento`. **Required.** |
| `id_carteira_cobranca` | billing wallet | → `fn_carteira_cobranca`. **Required.** |
| `id_vendedor` | salesperson | → `vendedor`. **Required.** |
| `cc_previsao` | accounting regime | `P` default (parâmetros), `N` competência, `S` caixa, `M` manual. **Required.** |
| `tipo_cobranca` | how billing is sent | `P` default, `I` printed, `E` e-mail. **Required.** |
| `base_geracao_tipo_doc` | document basis | `P` default, `OPC` optional contract document, `PROD` product document. **Required.** |
| `bloqueio_automatico` | auto-block on overdue | `S`/`N`. **Required.** |
| `nao_bloquear_ate` | do not block until (date) | |
| `aviso_atraso` | overdue warning | `S`/`N`. **Required.** |
| `nao_avisar_ate` | do not warn until (date) | |
| `desbloqueio_confianca` | trust unblock allowed | `S` enabled, `N` disabled, `P` default |
| `desbloqueio_confianca_ativo` | trust unblock in use now | `S`/`N` |
| `restricao_auto_desbloqueio`, `motivo_restricao_auto_desbloq` | self-unblock restriction, and its reason | |
| `liberacao_bloqueio_manual` | "Forçar status acesso" | `S`, `N`, `P` |
| `liberacao_suspensao_parcial`, `nao_susp_parc_ate` | partial-suspension release | `H` enabled, `D` disabled, `P` default |
| `contrato_suspenso`, `data_inicial_suspensao`, `data_final_suspensao` | temporary suspension | `S`/`N` |
| `data_cancelamento`, `motivo_cancelamento`, `motivo_adicional`, `obs_cancelamento`, `origem_cancelamento` | cancellation | `motivo_cancelamento` → `fn_areceber_mot_cancelamento`. `motivo_adicional` → `fn_areceber_mot_cancelamento_adicional`. `origem_cancelamento` is `M` manual or `A` automático. |
| `data_negativacao`, `id_motivo_negativacao`, `protocolo_negativacao`, `obs_negativacao` | negativation | `id_motivo_negativacao` → `contrato_motivo_negativacao` |
| `data_desistencia`, `motivo_desistencia`, `obs_desistencia` | gave up | `motivo_desistencia` → `cliente_contrato_motivo_desistencia`. Production flows read `obs_desistencia`. |
| `data_acesso_desativado` | access deactivation date | read-only |
| `dt_ult_bloq_auto`, `dt_ult_bloq_manual`, `dt_ult_desbloq_auto`, `dt_ult_desbloq_manual`, `dt_ult_finan_atraso`, `dt_ult_des_bloq_conf`, `dt_ult_ativacao`, `dt_utl_negativacao`, `dt_ult_desiste` | last-event dates | All read-only. Useful for "when was it blocked?". |
| `taxa_instalacao`, `id_produto_ativ`, `id_tipo_doc_ativ`, `id_cond_pag_ativ`, `ativacao_numero_parcelas`, `ativacao_valor_parcela`, `ativacao_vencimentos` | activation (installation) fee and its installments | **[MONEY]** when activation generates them. |
| `id_contrato_principal` | parent contract | → `cliente_contrato` |
| `contrato_recorrencia`, `status_recorrencia` | recurring charge | `PIX` (Pix automático), `CREDIT` (credit card), `N` (none). Status: `AGUARDANDO_APROVACAO`, `APROVADA`, `REJEITADA`, `EXPIRADA`, `CANCELADA`. |
| `assinatura_digital`, `integracao_assinatura_digital`, `url_assinatura_digital`, `token_assinatura_digital`, `email_assinatura_digital`, `contato_assinatura_digital`, `testemunha_assinatura_digital` | digital signature | `S`, `N`, `P`. The URL and token are set by IXC Assina. |
| `endereco_padrao_cliente` | use the customer's address | Default `S`. Otherwise the contract has its own address fields (`endereco`, `cidade`, …, plus `*_novo` used for address changes). |
| `id_instalador` | installer | → `fornecedor` |
| `avalista_1`, `avalista_2` | guarantors | → `cliente` |
| `obs`, `obs_contrato`, `alerta_contrato` | notes | `obs` is HTML |

Required on insert (Postman): `tipo`, `id_cliente`, `id_vd_contrato`, `contrato`, `id_tipo_contrato`, `id_modelo`,
`id_filial`, `data`, `id_tipo_documento`, `id_carteira_cobranca`, `id_vendedor`, `cc_previsao`, `tipo_cobranca`,
`renovacao_automatica`, `base_geracao_tipo_doc`, `bloqueio_automatico`, `aviso_atraso`. A new contract starts as
`status=P` with `status_internet=D`. It does nothing until it is activated.

```json
{"qtype":"cliente_contrato.id_cliente","query":"<id_cliente>","oper":"=","page":"1","rp":"20",
 "sortname":"cliente_contrato.id","sortorder":"desc"}
```
Read `id`, `contrato`, `status`, `status_internet`, `status_velocidade`, `id_vd_contrato`, `data_ativacao`, and
`obs_desistencia` or `motivo_cancelamento` when the contract is not active. To list only active contracts, add
`grid_param` `[{"TB":"cliente_contrato.status","OP":"=","P":"A"}]`.

Reading the status pair:

| `status` | `status_internet` | Meaning |
|---|---|---|
| `A` | `A` | active, with access |
| `A` | `FA` | active, overdue warning (the subscriber may get a notice page) (inferred) |
| `A` | `CA` | active, blocked automatically for non-payment |
| `A` | `CM` | active, blocked manually by an operator |
| `A` | `AA` | active, waiting for the contract signature |
| `P` | `D` | pre-contract, not yet activated |
| `I` | `D` | inactive or cancelled |
| `N` | `CM` or `CA` | negativated and blocked (inferred) |
| `D` | `D` | customer gave up before activation (inferred) |

### `vd_contratos` (Planos de venda, the sale plans)
Operations: list, insert, update, delete. This is the plan catalog that `cliente_contrato.id_vd_contrato` points to.
Use it to show plan names, prices and loyalty terms.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | plan id | |
| `tipo` | service type | `I`, `T`, `S`, `SVA`. **Required.** |
| `nome` | plan name | **Required.** |
| `valor_contrato` | plan value | Money as a string. The billed amount comes from the products (`vd_contratos_produtos`). |
| `Ativo` / `ativo` | status | `S` active, `N` inactive. The Postman doc writes `Ativo`; the body uses `ativo`. |
| `id_tipo_documento`, `id_modelo`, `id_carteira_cobranca`, `id_vendedor`, `id_filial`, `comissao` | defaults copied to new contracts | |
| `id_cidade` | plan valid for this city | → `cidade` |
| `fidelidade` | default loyalty in months | |
| `id_tipo_doc_ativ`, `id_produto_ativ`, `id_cond_pag_ativ`, `id_vendedor_ativ` | activation-fee defaults | |
| `utilizar_desconto_ate_vencimento`, `utilizar_desconto_por_repeticao`, `utilizar_desconto_no_produto_plano` | discount modes | `S`/`N` |
| `base_geracao_por_tipo_doc` | document basis | `OPC`, `PROD`, `P` |
| `tel_franquia_segundos`, `tel_franquia_prefix` | phone allowance | for telephony plans |
| `limitar_n_logins`, `logins_simultaneos` | login limits | hidden fields |

### `vd_contratos_produtos` (Planos por contrato: products of a plan or a contract)
Operations: list, insert, update, delete. This one table holds the products of a **plan** template (filter
`id_vd_contrato`) and the products of a specific **contract** (filter `id_contrato`). Together they are what is
billed.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | row id | |
| `tipo` | product type | `I` internet, … **Required.** |
| `id_plano` | bandwidth or service plan | → `radgrupos` (inferred, see [network](network.md)). **Required.** |
| `id_produto` | product | → `produtos` |
| `descricao` | description | |
| `qtde`, `valor_unit` | quantity, unit price | Both **required**. **[MONEY]** if changed. |
| `id_vd_contrato` | plan template | set for plan rows |
| `id_contrato` | contract | Set for contract rows. **Required** on insert per Postman. |
| `valor_ate_vencimento` | price if paid by the due date | |
| `fixar_ip` | fixed IP | **Required.** `0` = no (inferred). |
| `tipo_desconto`, `desconto_percentual`, `valor_desconto_produto`, `repetir`, `qtde_repeticoes_desconto_produto` | product discount | |

Listings: `vd_contratos_produtos.id_vd_contrato = <plan id>` gives the plan products.
`vd_contratos_produtos.id_contrato = <contract id>` gives the contract products. The view
`view_vd_contratos_produtos_gen` (filter `view_vd_contratos_produtos_gen.cliente_contrato_id`) lists the generated
products per contract ("Produtos por Contrato 1").

### `cliente_contrato_tipo` (Tipo de cobrança, the billing type)
Operations: list, insert, update, delete. Sets pre/post-paid billing and the overdue thresholds that drive automatic
warnings and blocks.

| Field | Meaning | Values / notes |
|---|---|---|
| `tipo_contrato` | name | **Required.** |
| `tipo_pagamento` | prepaid or postpaid | `Pre` Pré-pago, `Pos` Pós-pago. **Required.** |
| `base_periodo_prestacao` | service-period basis | `V` due date, `C` contract date, `P` period. **Required.** |
| `id_condicoes_pagamento` | payment terms | → `condicoes_pagamento`. **Required.** |
| `avisar_dias` | days overdue before the warning (FA) | **Required.** |
| `bloquear_dias` | days overdue before the automatic block (CA) | **Required.** |
| `bloqueio_renegociado_n_dias` | days overdue before blocking renegotiated debt | default 3 |
| `periodo`, `qtd_periodos` | billing period | `D` day, `M` month, `A` year. Both **required**. |
| `parcela_cobrar_proporcional` | which installment carries the prorated amount | `0` none, `1` first, `2` second |
| `dias_proporcional_cob_mes`, `parcelas_cob_adicional`, `max_titulos_abertos_gerar_contrato`, `dias_carencia_pre` | proration and limits | |
| `ativo` | active | `S`/`N` |

### `cliente_contrato_modelo` (Modelos de contrato, the print models)
Operations: list, insert, update, delete. These are the HTML templates for the printed contract and its terms.
Fields: `status` (`A`/`I`), `nome` (**required**), `eh_modelo_termo` (`S` = this model is a term), `texto`,
`cabecalho`, `prazo`, `fidelidade`, `cliente_contrato_comodato`, `cliente_contrato_de_permanencia`,
`termo_personalizado` (all HTML), `imprimir_comodatos` (`C` comodatos, `L` checklist, `T` all), `imprimir_login_assinante`,
`imprimir_pppoe`, `imprimi_roteador` (`S`/`N`), `id_contrato_testes`.

### Contract sub-tables

| Table | Purpose | Operations and key fields |
|---|---|---|
| `cliente_contrato_descontos` | discounts on a contract product | List by `cliente_contrato_descontos.id_contrato`. Insert, update, delete. Fields: `id_contrato`, `id_vd_contrato_produtos` (the product row inside the contract), `descricao`, `valor`, `percentual`, `data_validade`. **[MONEY]** |
| `cliente_contrato_acrescimos` | surcharges on a contract product | Same fields as discounts. Postman's list example filters on `cliente_contrato_descontos.id_contrato`, which looks like a copy-paste slip; use `cliente_contrato_acrescimos.id_contrato` (inferred). **[MONEY]** |
| `cliente_contrato_servicos` (catalog form `cliente_contrato_desc_serv`) | additional services (`tipo_acres_desc = A`) and additional discounts (`D`) | List with `qtype` `cliente_contrato_servicos.tipo_acres_desc`, then filter `id_contrato` in `grid_param`. Required on insert: `id_produto`, `descricao`, `id_unidade`, `quantidade`, `valor_unitario`, `valor_total`, `repetir` (`V` a number of times, `S` always), `data`, `status` (`A`/`I`), `status_nf21` (`A`/`I`), `id_contrato`, `tipo_acres_desc`. Discounts also need `id_produto_contrato_vinc` (the product they discount). `tipo`: `I`, `T`, `S`, `M`, `SVA`, `TV`. **[MONEY]** recurring charges. |
| `cliente_contrato_historico` | contract and customer history log | List, insert, update, delete. Fields: `tipo` (free text, e.g. "Atualiza assinatura"), `data`, `historico`, `id_cliente` (all required), `id_contrato`. Good place for agents to leave an audit note (with confirmation). |
| `cliente_contrato_alt_plano` | log of plan changes made with the wizard | List only. Filter by `id_contrato`, or by a date range: `grid_param` `[{"TB":"cliente_contrato_alt_plano.data_hora_alteracao","OP":"BE","P":"2026-04-01 00:00:00","P2":"2026-04-30 23:59:59"}]` (`BE` = between, with `P2`). |
| `cliente_contrato_comodato` | equipment lent to the customer (comodato) | Products: list with `qtype` `movimento_produtos.id_produto`. Assets (patrimônio): `movimento_produtos.id_patrimonio`. Filter `grid_param` `movimento_produtos.status_comodato = E` (lent out) and add `id_contrato`. Insert needs `id_produto`, `data`, `id_unidade`, `id_almox`, `filial_id`, `qtde_saida`, `valor_unitario`, `valor_total`, `status_comodato` (`E`), `id_classificacao_tributaria`, `tipo` (`S` product / `E` asset), `estoque`, `unidade_sigla`, `fator_conversao`, `id_contrato`. Assets also need `id_patrimonio` and `numero_patrimonial`. This moves stock. See [inventory and sales](inventory-sales.md). |
| `cliente_contrato_assinatura_termo` | terms attached to a contract | List, insert, update, delete. Fields: `id_termo`, `assinado` (`S`/`N`), `id_cliente_contrato_modelo`, `id_contrato` (all required). `token_assinatura_digital` and `url_assinatura_digital` are required only with IXC Assina. |
| `cliente_contrato_produtos_reajuste_valor` | price-adjustment rule (reajuste) | List, insert, update, delete. Required: `descricao`, `percentual`, `status` (contract status filter `A`, `I`, `P`, `N`, `D`, `T` = all), `status_internet` (`A`, `D`, `CM`, `CA`, `FA`, `AA`, `T`), `tipo_servico` (`I`, `F` phone, `S`, `T`). Optional filters: date ranges, `mes_ativacao` (1–12), `id_filial`, `cliente`, `contrato`, `tipo_cobranca`, `carteira_cobranca`, `cidade`, `condominio`, `plano_venda`, `tipo_pessoa`. It only takes effect through `gerar_acrescimo_25243`. |
| `cliente_contrato_servicos_param` | default discount/surcharge parameters | catalog only: `tipo_da` (`D`/`A`), `tipo` (`V` value / `P` percent), `valor`, `percentual`, `repetir`, `acao_tipo` (`N` normal, `A` birthdays), `uf`, `cidade` |
| `voip_sippeers` | SIP extensions of a contract | Listed under Contratos (`voip_sippeers.id_contrato`). See [network](network.md). |
| `fn_areceber` (filter `id_contrato`) | the contract's invoices | Listed under Contratos with `grid_param` `liberado=S`, `status!=C`, `status!=R`. See [financial](financial.md). |

### `cliente_arquivos` (Arquivos do cliente/contrato, attached files)
Operations: list (filter `cliente_arquivos.id_cliente` or `cliente_arquivos.id_contrato`), insert, delete.
- Insert is **multipart form-data**, not JSON. Fields: `descricao` (the file's display name), `local_arquivo` (the
  file itself, with its exact name and extension), `id_cliente`, optional `id_contrato`, and `classificacao_arquivo`
  (default `P`).
- To download a file's content, use the `cliente_arquivo` action below (singular name).

### `cliente_condominio` (Condomínios, buildings)
Operations: list, insert, update, delete. Required: `condominio`, `endereco`, `numero`, `bairro`, `id_cidade` (→
`cidade`). Optional: `cnpj`, `cep`, `sindico`, `celular_sindico`, `data_cadastro`, `obs`, `quantidade_shafts`,
`bloco_unico`. Referenced by `cliente.id_condominio` and `cliente_contrato.id_condominio`.

### `tipo_cliente` (Tipos de clientes, customer groups)
Operations: list, insert, update, delete. Postman says all fields are required: `tipo_cliente` (name),
`tipo_assinante` (`1`–`6`, same codes as `cliente`), `contribuinte_icms` (`S`, `N`, `I`), `tipo_cliente_scm` (`01`–`99`).
Referenced by `cliente.id_tipo_cliente`.

### `cidade`, `uf`, `pais` (location lookups)
Operations: list and delete only. **Never delete these.** Look up ids before writing a customer.
- `cidade`: `id`, `nome`, `uf` (→ `uf.id`), `origem` (`N` nacional / `I` internacional), `cod_ibge`, `cod_siafi`,
  `regiao`. Find a city with `{"qtype":"cidade.nome","query":"Blumenau","oper":"=" }`, then check its `uf`, because
  many states have a city of the same name.
- `uf`: `id`, `nome`, `sigla` (e.g. `SC`), `cod_uf`, `regiao`, `id_pais` (→ `pais`), `cod_ibge`.
- `pais`: `id`, `nome`, `iso`, `iso3`, `codigo_pais`.
- `cliente.cidade`, `cliente.uf`, `cliente_condominio.id_cidade`, `vendedor.id_cidade` and `fornecedor.cidade` are
  numeric ids, never names.

### `fornecedor` (Fornecedores, suppliers)
Operations: list, insert, update, delete. Also used for installers (`cliente_contrato.id_instalador`). Required on
insert (these override the parameter settings): `ativo` (`S`/`N`), `tipo_pessoa` (`F`, `J`, `E`), `razao`, `data`
(`DD/MM/YYYY`), `cidade` (→ `cidade`). Other fields: `tipo` (→ `fornecedor_tipo`), `fantasia`, `cpf_cnpj` (**note
the field name differs from `cliente.cnpj_cpf`**), `ie_identidade`, `contribuinte_icms` (`S`, `N`, `I`), `id_conta` (→
`planejamento_analitico`), `representante`, `telefone`, `celular`, `email`, `site`, the address fields, and `obs`.

### `vendedor` (Vendedores, salespeople)
Operations: list, insert, update, delete. Required: `nome`, `comissao` (percent, e.g. `3.00`), `id_cidade`, `status`
(`A` active). Other fields: `comissao_perc_recebimento`, `comissao_v`, `telefone`, `celular`, `cnpj_cpf`, `ie_rg`,
`email`, `pipe_id_usuario` (Pipedrive). Referenced by the `id_vendedor` and `id_vendedor_ativ` fields of contracts and
plans.

### `contato` (Leads/Contatos, CRM leads)
Operations: list, insert, update, delete. Holds leads and contacts. A lead is not a `cliente` yet.
`contato.id_cliente` links a contact to an existing customer.

| Field | Meaning | Values / notes |
|---|---|---|
| `nome` | name | **Required.** |
| `data_cadastro` | registration date | **Required**, `DD/MM/YYYY`. |
| `fone_celular` | mobile | Postman marks it required. **At least one phone or the e-mail must be filled.** Postman's example is digits only (`49999999999`). |
| `fone_residencial`, `fone_comercial`, `fone_whatsapp`, `email`, `instagram`, `facebook`, `website` | contact channels | |
| `lead` | record kind | `S` Lead / `N` Contato |
| `principal` | primary contact of the customer | `S`/`N` |
| `ativo` | active | `S`/`N` |
| `id_cliente` | linked customer | → `cliente` |
| `tipo_pessoa`, `cnpj_cpf`, `razao`, `data_nascimento` | identity | |
| `id_filial` | branch | required in the catalog |
| `id_contato_tipo`, `id_candidato_tipo`, `id_campanha`, `id_concorrente`, `id_responsavel`, `id_segmento`, `id_perfil` | classification | → `contato_tipo`, `crm_tipo_candidato` (sales channel), `crm_campanha`, `crm_concorrente`, `funcionarios`, `segmento_crm`, `crm_perfil` |
| `id_vd_contrato` | plan of interest | → `vd_contratos` |
| `id_estagio`, `ordem_kanban` | kanban stage | → `crm_negociacoes_estagios` |
| `tipo_rede`, `status_viabilidade`, `caixa_mais_proxima`, `operador_neutro` | coverage (viability) | `tipo_rede`: `P` own network, `N` neutral network, `A` both |
| `origem`, `origem_source`, `origem_medium`, `origem_campaing` (typo kept), `external_id`, `external_system` | marketing attribution | read-only |
| `cep`, `endereco`, `numero`, `bairro`, `cidade` (→ `cidade`), `latitude`, `longitude`, `moradia`, `tipo_localidade` | address | |

### `crm_canditados` (Prospecções, prospects)
The table name keeps IXC's typo. Operations: list, insert, update, delete. Prospects are stored as customer-like
records with `crm = "S"`. The Postman list example filters with `qtype` `cliente.id`, which shows that the rows come from
the customer table. Required on insert: `razao`, `status_prospeccao` (the `cliente` codes above; Postman example
`N`), `tipo_pessoa`, `ativo` (`S`), `telefone_celular`, `cidade` (→ `cidade`), and `crm` (must be `S`). At least
one phone or the e-mail is required. Other fields: `id_vd_contrato_desejado`, `id_vendedor`,
`prospeccao_ultimo_contato`, `prospeccao_proximo_contato`, the viability fields, and `plano_negociacao_auto_viab`
(→ `crm_planos_negociacoes`). Prospect files use `cliente_arquivos` (same list, insert and delete as the customer's).

### `crm_negociacoes` (Negociações, deals)
Operations: list, insert, update, delete. Required on insert: `id_cliente` (customer or prospect), `descricao`,
`id_estagio` (→ `crm_negociacoes_estagios`), and `status`: `N` Negociando, `D` Perdemos (lost), `V` Vencemos (won).
The catalog also requires `id_filial`. Key fields: `id_plano_negocio` (→ `crm_planos_negociacoes`), `id_contato`,
`id_funil`, `id_responsavel`, `id_canal_origem`, `valor_mensal`, `valor_fixo`, `previsao_fechamento`, `substatus` (→
`crm_substatus`), `id_plano` (→ `vd_contratos`), `id_tipo_cobranca`, `id_modelo_contrato`, `id_contrato`
(read-only, filled when won). The automation flags `inserir_contrato`, `inserir_acesso`, `inserir_atendimento` and
`inserir_tarefa` (`S`) make "won" create a contract, a login, a ticket and a task. Access settings:
`autenticacao` (`L` PPPoE, `H` Hotspot, `M` IP x MAC, `V` VLan, `D` IPoE, `I` Integração, `E` Externa),
`tipo_conexao_mapa` (`F` fibra, `L` cabo, `A` ADSL, `58`, `24`), `login`, `senha`, `id_caixa_ftth`.
Scheduling: `prioridade` (`B`, `M`, `A`, `C`), `data_reservada`, `melhor_horario_reserva` (`M`, `T`, `N`, `Q`).
`status_reserva_rede_neutra`: `S`, `E`, `A`.

### `crm_planos_negociacoes` (Planos de negociações, deal templates)
Operations: list, insert, update, delete. Required: `descricao`, `velocidade`. The other fields mirror the
automation fields of `crm_negociacoes`: `id_plano`, `id_tipo_cobranca`, `id_modelo_contrato`, `fidelidade`,
`inserir_*`, `autenticacao`, `tipo_conexao_mapa`, `id_grupo`, `prioridade`, `id_assunto`, `id_wfl_processo`,
`menssagem`. Also `valor_mensal`, `valor_fixo`, `desconto_fidelidade`, `ativo`, `cor_mapa`, `ordem`.

### TV and SVA logins
`tv_usuarios` (Login TV): list, insert, update, delete. Delete works only if the integration allows it. One row is
one streaming/TV account linked to a contract. Common fields: `id_contrato`, `plataforma`, `connection_type_tv`
(`DTH`, `MMDS`, `SAT` free satellite, `IPTV`, `OTT`, `STR` streaming), `id_vd_contratos_produtos` (the contract
product that pays for it). The `plataforma` value selects the provider and its extra fields:

| `plataforma` | Extra fields |
|---|---|
| `apptec`, `minerva` | `account_id`, `id_login_plataforma` |
| `eiTv` | `usar_email_principal`, `login`, `senha`, `account_number`, `online` |
| `globoplay`, `telecineplay`, `watchespn` | only `connection_type_tv` |
| `hubNeo` | `account_id`, `usar_email_principal`, `login`, `senha` |
| `hubNeoDirectvGo` | `id_login_plataforma`, `account_number`, `online` |
| `ITTV`, `NxPlay` | `usar_email_principal`, `login`, `senha` |
| `ministra` | `login`, `senha`, `mac_devices`, `id_dealer`, `version`, `ip`, `online` |
| `ministrav2` | `api` (`A`), `login`, `senha`, `account_number`, `online` |
| `multTv` | `pin`, `login`, `senha`, `account_number`, `online` |
| `oletv` | `usar_email_principal`, `login`, `mac_devices`, `account_number`, `id_equipamentos`, `online` |
| `panaccess` | `id_integracao`, `account_id` |
| `playhub` | `api`, `login`, `senha`, `status_assinante_watch` |
| `SmartTUBE` | `account_id`, `pin`, `login`, `senha`, `status_assinante_watch`, `device_limit_id` |
| `watch` | `api` (`A`), `usar_email_principal`, `login`, `token_assinante_watch`, `status_assinante_watch` |
| `youCast` | `api`, `account_id`, `usar_email_principal`, `profile_name`, `pin`, `birthday`, `login`, `senha`, `status_assinante_watch`, `id_portal`, `mac_devices`, `id_dealer` |

`sva_usuarios` (Login SVA): list and insert. Fields: `id_contrato`, `id_integracao`, `id_produto_contrato`,
`usar_email` (`S` = use the customer's registration data), `user`, `senha`, `msisdn` (phone), `cnpj_cpf` (with dots
and hyphen), and `status_integracao` (`A` ativo, `B` bloqueado, `D` desativado). Never fill `user_id` or
`subscription_id`; the integration sets them. Postman has templates for Campsoft, GugoTv, Hexa, Music and Skeelo.
Creating a TV or SVA login provisions an account at the third-party provider (inferred), which may be billed by that
provider.

### `consulta_spc_serasa` (Consultas de CPF/CNPJ, credit checks)
List only (via the "Consulta de crédito" button). Fields: `id_cliente`, `data_hora_consulta`, `total_ocorrencias`,
`valor_total`, `tipo_consulta`, `id_lead`, `cnpj_cpf`, `intermediador`. The installation needs at least one credit
integration: Connect S.A, Crédito na Medida or SOAWebService. Listing reads past checks. In the UI the button runs a
new check, which the bureau may bill (inferred).

### Minor and lookup tables (from the IXC n8n node resource list and catalog relations)

| Table | Purpose |
|---|---|
| `cliente_contato` | contacts of a customer |
| `contato_tipo` | contact types (`descricao`, `cor_mapa`) |
| `crm_campanha` | marketing campaigns (`campanha`, `status` `S`/`N`, `data_inicio`, `data_termino`) |
| `crm_tipo_candidato` | sales channel (canal de vendas) |
| `crm_concorrente`, `crm_perfil`, `segmento_crm`, `crm_substatus` | CRM classifications |
| `crm_funil`, `crm_negociacoes_estagios` | sales funnels (`funil`, `tipo`) and their stages |
| `crm_negociacoes_produtos` | products of a deal |
| `crm_prospeccao_propostas` | proposals: `status` `criada`, `enviada`, `recusada`, `aceita`, `cancelada`, `finalizada`; `tipo_envio` `email` or WhatsApp. Sending a proposal **[MESSAGES CUSTOMER]**. |
| `crm_prospeccao_anotacoes` | prospect notes |
| `crm_emails`, `crm_modelo_email`, `crm_email_log`, `crm_sms_log` | CRM e-mails (`destinatarios`, `assunto`, `corpo`), templates, and the e-mail and SMS logs. Use the logs to check what was sent to a customer. |
| `crm_cobranca`, `crm_cobranca_historico` | collection management and its history (see [financial](financial.md)) |
| `indicacao_contrato` | referral source (`cliente_contrato.indicacao_contrato_id`) |
| `cliente_contrato_motivo_desistencia`, `fn_areceber_mot_cancelamento`, `fn_areceber_mot_cancelamento_adicional`, `contrato_motivo_negativacao`, `cliente_contrato_motivo_inclusao` | reason lookups for give-up, cancellation, negativation and inclusion. List them to get valid reason ids. |
| `cliente_contrato_indexadores` | price-adjustment indexes |
| `cidade_bairro` | neighborhoods |
| `cliente_envio_sms` | the SMS-sending form behind `botaoAjax_22282` |

## Actions

All of these are `POST` to `/<action>` with a JSON body and no `ixcsoft` header unless stated. The response is
`{"type":"success|error","message":…}`. Check `type`, and relay `message` when it is an error. The numeric suffixes
(`_15300`, `_23529`, …) are internal IXC button ids. They are opaque, stable names; the table below explains each
one.

### Contract status buttons

| Endpoint | UI label | Body | Effect |
|---|---|---|---|
| `cliente_contrato_ativar_cliente` | Status do contrato → **Ativar** | `{"id_contrato":"<id>"}` | Activates a pre-contract: `status` → `A` and `data_ativacao` is set. Access comes up. May generate the activation fee and the first invoices from the activation fields (inferred). Write. **[ACCESS] [MONEY]** |
| `desativar_cancelar_financeiro_nao_vencido` | Status → **Cancelar contrato e financeiro não vencido** | `{"id_contrato":"<id>","data_cancelamento":"DD/MM/YYYY","motivo_cancelamento":"<id fn_areceber_mot_cancelamento>","obs_cancelamento":"<text>"}` | Cancels the contract (`status` → `I`) and cancels its **not-yet-due** invoices. Overdue invoices stay open. Access is deactivated. **Destructive. [CANCELS] [MONEY] [ACCESS]** Only on the user's explicit request, with the reason confirmed. |
| `negativar_bloquear` | Status → **Negativar contrato e bloquear acesso** | `{"id":"<id_contrato>","id_cliente":"<id_cliente>"}` | Marks the contract negativated (`status` → `N`, reported to credit bureaus) **and blocks access**. **Destructive. [ACCESS] [CANCELS]** Legal and financial consequences for the customer. |
| `desistir_contrato` | Status → **Desistiu** | `{"id_contrato":"<id>","motivo_desistencia":"<id cliente_contrato_motivo_desistencia>","obs_desistencia":"<text>"}` | Records that the customer gave up (`status` → `D`). Fills `data_desistencia` and `obs_desistencia`. Used for contracts that were never activated (inferred). Write. **[CANCELS]** |

There is no documented "reactivate" or "change plan" button in the webservice. Reactivation and plan changes are
UI wizards. Plan changes leave a log in `cliente_contrato_alt_plano` (list only). New contracts created for these
reasons carry `motivo_inclusao` `R` (reactivation) or `U`/`D` (upgrade/downgrade). Doing either through the API means
inserting a new `cliente_contrato` and cancelling the old one. That has billing consequences, so do not attempt it
without the user and the ISP's procedure (inferred).

### Contract access buttons (status_internet and speed)

| Endpoint | UI label | Body | Effect |
|---|---|---|---|
| `cliente_contrato_15464` | Status acesso → **Liberar manualmente** (A) | `{"id_contrato":"<id>"}` | Sets `status_internet` → `A`. Manual unblock: access is restored regardless of overdue invoices. The automatic routine can block again on its next run unless the debt is settled or `nao_bloquear_ate` is set (inferred). **[ACCESS]** |
| `cliente_contrato_15300` | Status acesso → **Bloquear** (CM, Bloqueio manual) | `{"id_contrato":"<id>"}` | Sets `status_internet` → `CM`. The subscriber loses access, and active sessions are usually dropped (inferred). **[ACCESS]** |
| `cliente_contrato_15463` | Status acesso → **Avisar atraso** (FA, Financeiro em atraso) | `{"id_contrato":"<id>"}` | Sets `status_internet` → `FA`. This is the overdue-warning state, normally reached automatically after `avisar_dias`. The subscriber may be redirected to a warning page (inferred). **[ACCESS] [MESSAGES CUSTOMER]** (inferred) |
| `cliente_contrato_23529` | Status acesso → **Aguardando assinatura** (AA) | `{"id_contrato":"<id>"}` | Sets `status_internet` → `AA`. Access waits for the contract signature. **[ACCESS]** |
| `desbloqueio_confianca` | **Desbloqueio confiança** (trust unblock) | `{"id":"<id_contrato>"}` | A temporary trust unblock of an overdue-blocked contract. Fully documented in [network](network.md). **[ACCESS]** |
| `liberar_temporario_24722` | Ações → **Liberar temporariamente** | `{"get_id":"<id_contrato>"}` | Temporarily releases a blocked contract. Like the trust unblock, but started by an operator. The n8n node also exposes it as `cliente_contrato_btn_lib_temp_24722`. **[ACCESS]** |
| `suspender_temporario_29546` | Ações → **Suspender temporariamente** | The **full `cliente_contrato` record** (as read), including `id`; the Postman example has every field of the contract | Temporary suspension: `contrato_suspenso` → `S` for the period `data_inicial_suspensao`–`data_final_suspensao` (inferred from the fields). Access is cut and billing is affected for the period (inferred). Read the contract first and send it back with the suspension dates. **[ACCESS] [MONEY]** |
| `liberacao_reducao_contrato_29157` | Ações → **Liberação de redução de velocidade** | `{"get_id":"<id_contrato>"}` | Removes the speed reduction (`status_velocidade` `R` → `N`). **[ACCESS]** |

### Contract financial, print, comodato and signature buttons

| Endpoint | Body | Effect |
|---|---|---|
| `gerar_financeiro_contrato_15314` (Financeiro → **Gerar financeiro**) | `{"id_contrato":"<id>","tipo":"<billing type id>","id_cliente":"<id>","id_tipo_documento":"<id>"}` | Generates the contract's receivables (`fn_areceber` invoices). **[MONEY]** It can create duplicate charges. Check existing invoices first ([financial](financial.md)). |
| `cliente_contrato_imprimir_contrato_17678` (Imprimir → Contrato) | `{"id":"<id_contrato>"}` | Renders the printed contract from `cliente_contrato_modelo`. Read. |
| `botao_rel_28088` (Termos → Imprimir) | `{"id":"<id of cliente_contrato_assinatura_termo>"}` | Renders a term. Read. |
| `baixar_comodato_23069` (Comodato → Baixar → Outros almoxarifados) | `{"id":"<comodato row id>","id_almox":"<warehouse id>","id_almox_label":"<warehouse name>","id_filial_baixa":"<branch id>","id_filial_baixa_label":"<branch name>"}` | Returns lent equipment to a warehouse and closes the comodato. It works the same for products and assets. Write; moves stock. |
| `baixar_produto_imobilizado` | `{"get_id":"<comodato id>"}` | Patrimônio → Devolver → **Meu almoxarifado**: returns an asset to the user's own warehouse. Write. See [inventory and sales](inventory-sales.md). |
| `baixar_produto_imobilizado_outro_almox` | `{"id":"<comodato id>","id_almox":"<warehouse id>"}` | Returns an asset to another warehouse. Write. |
| `gerar_acrescimo_25243` (Reajuste de valor → **Gerar acréscimos**) | `{"id":"<id of cliente_contrato_produtos_reajuste_valor>"}` | Applies a price-adjustment rule. Every contract that matches the rule's filters gets the surcharge. **[MONEY]** A mass price change; confirm the scope with the user. |
| `gerar_documento_assinatura_digital` (Assinatura digital → Gerar novo documento) | `{"id_contrato":"<id>"}` | Creates a new IXC Assina signature document for the contract. Requires the **paid IXC Assina module**. Normally sends the signing link to the customer's e-mail or contact (inferred). Write. **[MESSAGES CUSTOMER]** (inferred) |
| `reenviar_link_assnatura_digital` (typo "assnatura" is the real name) | `{"id_contrato":"<id>"}` | Resends the signing link to the customer. Requires IXC Assina. **[MESSAGES CUSTOMER]** |

Contract-product helper actions seen only in the IXC n8n node (read):
- `cliente_contrato_retornar_produtos_contrato_28145`: `{"get_id":"<id_contrato>"}`, "Produtos por Contrato 1".
- `api_get_produtos_contrato`: `{"id_contrato":"<id>"}`, "Produtos por Contrato 2".

The listings `vd_contratos_produtos` and `view_vd_contratos_produtos_gen` usually serve the same purpose.

The financial buttons listed in the Contratos folder are documented in [financial](financial.md): `get_boleto` (PDF,
e-mail or SMS), `get_pix`, `fn_areceber_recebimentos_baixas_novo`, `fn_areceber_altera` and `relacionar_contrato`.

### Customer buttons

| Endpoint | Body | Effect |
|---|---|---|
| `botaoAjax_22282`, SMS mode (Cliente → Contato → **Enviar SMS**) | `{"tipo_envio_mensagem":"sms","celular":"(DD) 9XXXX-XXXX","id_gateway":"<SMS gateway id>","id_gateway_label":"<gateway name>","mensagem":"<text>","remetente":"<sender name, optional>","id_cliente":"<id>"}` | Sends an SMS **to the end customer** through a configured SMS gateway. It may cost money per message at the gateway. **[MESSAGES CUSTOMER]** Confirm the text and the number with the user. |
| `botaoAjax_22282`, omnichannel mode (**Enviar Omnichannel**) | `{"tipo_envio_mensagem":"omnichannel","celular":"<phone>","id_cliente":"<id>","msg_omnichannel":"<template id>","msg_omnichannel_label":"<template name>"}` | Sends a pre-registered omnichannel template (for example WhatsApp) to the customer. **[MESSAGES CUSTOMER]** |
| `botao_rel_26658` (**Enviar notificação push**) | `{"titulo":"<title>","mensagem":"<text>","id_cliente":"<id>"}` | Sends a push notification to the customer's app (the subscriber app). **[MESSAGES CUSTOMER]** |
| `cliente_arquivo` (Arquivos → **Visualizar**) | `{"id":"<cliente_arquivos.id>"}` | Returns the file content as base64. Read. |
| `consulta_spc_serasa` (Análise de crédito → Consulta de crédito; listing, `GET`/`POST`) | `ixcsoft: listar` + `{"qtype":"consulta_spc_serasa.id_cliente","query":"<id>","oper":"=", …}` | Lists the customer's credit checks. Read. |
| `imprimir_relatorio_inadimplencia` (`GET` in Postman) | `ixcsoft: listar` + `{"id":"<negativation id>"}` | Prints the credit-check (negativation) report. The Postman example sends an `IXC_Session` cookie, so it may need a UI session rather than the API token (inferred). Read. |
| `bloquear_desbloquear_sip` (Linha SIP → Bloquear/Desbloquear) | `{"get_id":"<SIP line id>"}` | Toggles the block on a customer's SIP phone line. **[ACCESS]** See [network](network.md). |

Label warning: the IXC docs swap the UI labels. The n8n node calls `botaoAjax_22282` "Enviar notificação push" and
`botao_rel_26658` "Enviar SMS", and the Postman folder screenshots are swapped too. Go by the body: `22282` takes
`celular` and `mensagem` (SMS or omnichannel); `26658` takes `titulo` and `mensagem` (push).

### CRM buttons

| Endpoint | Body | Effect |
|---|---|---|
| `PUT crm_negociacoes_simplificado/<id negociação>` (**Vencemos simplificado**) | `{"data_vencemos":"DD/MM/YYYY","id_responsavel":"<funcionarios id>","id_cliente":"<id>","id":"<id negociação>"}` | Marks the deal won. With the plan's `inserir_*` flags this can create the contract, login, ticket and task (inferred from the `crm_negociacoes` fields). Write. **[MONEY] [ACCESS]** (inferred) |
| `PUT crm_negociacoes_perdemos_data/<id>` (**Perdemos**) | `{"data_perdemos":"DD/MM/YYYY","id_responsavel":"<id>","id_cliente":"<id>","id":"<id negociação>"}` | Marks the deal lost. Write. |

### TV buttons

| Endpoint | Body | Effect |
|---|---|---|
| `ativar_usuario_playhub` | `{"get_id":"<tv_usuarios.id>"}` | Activates the PlayHub account at the provider. Write. Third-party billing (inferred). |
| `desativar_usuario_playhub` | `{"get_id":"<tv_usuarios.id>"}` | Deactivates the PlayHub account. Write. The customer loses the service. |

### Actions seen only in the IXC n8n node (undocumented)
The n8n node lists these without parameters or a mapping. Do not call them unless the user confirms how they work on
their IXC version:
- `assinar_contrato`, `assinar_termo`, `converter_cliente`, `contract_plans`
- `analise_credito`, `cliente_endereco_19479`, `diagnostico_cliente`, `listar_roteadores_do_cliente`
- `botao_Ajax_15343`, `botao_rel_20939`, `cliente_contrato_21517`, `liberacao_reducao_contrato_29154`
- `crm_negociacoes_29028`, `crm_negociacoes_29334`, `crm_canditados_23184`, `crm_canditados_27847`
- `botaoAjax_22264` and `imprimir_proposta` (proposals), `caixa_proxima_disponivel` (lead)

`viabilidade_tecnica` (viability check by address: `endereco`, `numero`, `bairro`, `cidade`, `estado`, `cep`) is
covered in [network](network.md) (inferred location).

## Recipes

1. **Identify the caller by CPF/CNPJ.** Strip the input to digits. Mask 11 digits as `000.000.000-00` and 14 digits
   as `00.000.000/0000-00`. List `cliente` with `qtype` `cliente.cnpj_cpf`, `oper` `=` and `rp` `1`. Check that
   `type` is not `error` and that `total` is greater than 0, then read `registros[0].id`, `razao`, `email` and
   `telefone_celular`.
2. **Identify the caller by phone.** Format the number as `(DD) 9XXXX-XXXX` (an 8-digit landline is
   `(DD) XXXX-XXXX`). List `cliente` with `cliente.telefone_celular` `=`, and if there is no match retry with
   `cliente.whatsapp` and `cliente.fone`. As a last resort use `L` with the last 8 digits. With several matches, ask
   for the CPF.
3. **Contract status for a customer.** List `cliente_contrato` by `id_cliente`. For each contract report
   `contrato`, `status` and `status_internet` using the code tables. For `D`, `I` or `N` add `obs_desistencia`,
   `obs_cancelamento` or `data_negativacao`. To get the plan name, look up `vd_contratos` by `id_vd_contrato`.
4. **"My internet is blocked."** Run recipe 3. If `status_internet` is `CA` or `FA`, list the open invoices
   ([financial](financial.md)) and send the boleto or PIX. If the customer asks for a release, use
   `desbloqueio_confianca` ([network](network.md)). Use `cliente_contrato_15464` only when an operator authorizes it.
   If `status_velocidade` is `R` after payment, `liberacao_reducao_contrato_29157` restores the speed. Confirm every
   step.
5. **New customer and contract.** Resolve `cidade` (and check its `uf`). Insert `cliente` with the required fields
   and get its `id`. Insert `cliente_contrato` with `id_cliente`, `id_vd_contrato`, the billing type, model, branch,
   document type, wallet and salesperson ids (list `vd_contratos`, `cliente_contrato_tipo` and
   `cliente_contrato_modelo` to choose them). Attach the products in `vd_contratos_produtos` if the plan does not add
   them. Activate with `cliente_contrato_ativar_cliente` only when the user says so (**[MONEY] [ACCESS]**).
6. **Cancel on request.** List the reason ids from `fn_areceber_mot_cancelamento`. Show the contract and its open
   invoices to the user, and get explicit confirmation. Call `desativar_cancelar_financeiro_nao_vencido` with the
   date, reason and note. Optionally add a `cliente_contrato_historico` entry.
7. **Message the customer.** Get `telefone_celular` from `cliente`. For SMS, get the gateway id from the user or the
   ISP config, then call `botaoAjax_22282` with `tipo_envio_mensagem` `sms`. For WhatsApp templates use `omnichannel`
   with `msg_omnichannel`. For app users, `botao_rel_26658`. Confirm the text first, and check `crm_sms_log` afterwards
   if delivery is in doubt.
8. **Equipment on loan.** List `cliente_contrato_comodato` with `grid_param` `movimento_produtos.status_comodato = E`
   plus the contract id. When the equipment comes back, `baixar_comodato_23069` returns it to a warehouse.
