# IXC financial

Receivables (contas a receber, the ISP customer's invoices/boletos/PIX), receipts and cancellations, renegotiation,
payables (contas a pagar), accounting entries, chart of accounts, billing wallets, payment terms, holidays and fiscal
classification. Use this file for anything about a customer's invoices, second copies of boletos, PIX copy-paste
codes, payments and debts. Shared request shapes (auth, `ixcsoft: listar`, `grid_param`, errors as HTTP 200) are in
[request mechanics](requests.md); customers and contracts are in [customers](customers.md).

**Books warning.** Every write in this module changes the ISP's accounting: receiving (baixa), cancelling,
estornar (reversal), editing value/due date, renegotiating and deleting titles alter the customer's receivables,
cash accounts and reports, and may trigger bank remittances (remessa), customer notifications, contract
unblocking/blocking rules and churn/default statistics. Read-only calls are `fn_areceber` listing, `get_pix`,
`get_boleto` with `tipo_boleto` `arquivo`/`dados` (and `atualiza_boleto: "N"` to avoid recalculating). Confirm
every write with the user, state the exact title id(s), value and date, and never delete without an explicit
request.

Date format: the Postman examples send `DD/MM/YYYY` on inserts/actions; listings return `YYYY-MM-DD`. Some
installations only filter dates in `YYYY-MM-DD` (official comment: "if the default date format does not filter,
use the American format, e.g. 2024-11-30"). Money in action bodies is sometimes Brazilian `0,20` (the UI format);
follow the example of each endpoint.

## Tables

### `fn_areceber` — receivable titles / invoices (Contas a receber)
Operations: list / insert / update / delete. The central table: one row per invoice/boleto/PIX charge of a
customer. Prefer `fn_areceber_altera` for edits (smaller body) and the action endpoints for receiving/cancelling;
plain `PUT /fn_areceber/<id>` needs the full record.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | title id ("id do boleto/fatura") | used by `get_boleto`, `get_pix`, all actions |
| `id_cliente` | customer | → `cliente.id`; REQ |
| `id_contrato` | contract that generated the title | → `cliente_contrato.id`; RO. `id_contrato_avulso` = one-off contract; `id_contrato_principal` |
| `filial_id` | branch | → `filial`; REQ |
| `id_conta` | revenue account (analytical chart) | → `planejamento_analitico.id`; REQ |
| `id_conta_class_finan_a` / `id_conta_class_finan` | financial class | → `planejamento_analitico_finan` |
| `id_carteira_cobranca` | billing wallet (bank/gateway config) | → `fn_carteira_cobranca.id` |
| `status` | title status | `A`=A receber (open), `R`=Recebido (paid), `P`=Parcial (partially paid), `C`=Cancelado |
| `liberado` | visible/released | default `S`. `N` hides the title (official note: must be `S` or the invoice stays hidden). Always filter `liberado = S` for customer-facing lists |
| `documento` | document number | free text |
| `data_emissao` / `data_vencimento` | issue / due date | REQ |
| `data_inicial` / `data_final` | service period covered by the invoice (inferred: billing period start/end) | RO in UI |
| `valor` | original amount | REQ |
| `valor_aberto` | amount still open | RO; use this, not `valor`, for "how much is owed" |
| `valor_recebido`, `pagamento_valor`, `pagamento_data` | received amount, last payment amount/date | RO |
| `valor_juros`, `valor_multas` | interest / fine charged | RO |
| `valor_cancelado`, `data_cancelamento`, `id_mot_cancelamento` | cancellation data | RO; → `fn_areceber_mot_cancelamento` |
| `previsao` | accounting regime | `N`=Competência (Previsão NÃO), `S`=Caixa (Previsão SIM), `M`=Manual; REQ |
| `tipo_recebimento` | payment method | `Boleto`, `Cheque`, `Cartão` (sent as `CartÃ£o` in some encodings), `Dinheiro`, `Depósito`, `Gateway`, `Débito` (débito em conta), `Fatura`, `ArrecadacaoRecebimento`, `Transferencia`, `Pix`; REQ |
| `nn_boleto` | nosso número of the boleto (official flow comment calls it "the boleto barcode") | RO |
| `linha_digitavel` | boleto typeable line (linha digitável) | RO, up to 200 chars; empty for non-boleto titles |
| `gateway_link` | payment-page link of the gateway (Efí, Juno, etc.) | RO; send this link to the end customer when present |
| `boleto` | boleto number | RO |
| `pix_txid` | PIX transaction id (official comment: "the PIX code of the boleto") | RO; the copy-paste string comes from `get_pix` |
| `tipo_cobranca_pix` | PIX charge type | `COM_VENCIMENTO`=Com vencimento, `IMEDIATA`=Imediata |
| `pix_txid_recorrente`, `pix_status_recorrente` | PIX Automático (recurring) | status `CRIADA`, `ATIVA`, `CONCLUIDA`, `EXPIRADA`, `REJEITADA`, `CANCELADA` |
| `recebido_via_pix` / `recebido_por_recorrencia` | paid by PIX / by card recurrence | `S`/`N` |
| `forma_recebimento` | how it was settled | `M`=manual, `R`=automatic (bank return/gateway) |
| `aguardando_confirmacao_pagamento` | awaiting payment confirmation | `S`/`N` |
| `conta_recebimento` | cash/bank account that received | → `contas` |
| `libera_periodo` | releases the period (unblock while open) (inferred) | `S`/`N` |
| `titulo_protestado`, `titulo_renegociado`, `titulo_importado`, `estornado`, `impresso`, `arquivo_remessa_baixado`, `parcelado_cartao` | flags | `S`/`N` |
| `id_renegociacao`, `id_renegociacao_novo`, `tipo_renegociacao` | renegotiation links (original → new) | |
| `tipo_cobranca` | delivery type | `P`=Padrão, `I`=Impresso, `E`=E-mail |
| `em_cobranca`, `etapa_envio_regua`, `status_cobranca_regua` | collection-rule (régua) state | etapa: `LP` Lembrete de pagamento, `CV` No vencimento, `AC` Aviso de cobrança, `IP` Informativo de pendência, `AP` Agendar pagamento, `CAP` Cobrança automática e presencial, `NC` Negativar clientes, `RCA` Recebimento, `CCA` Cancelamento, `RCB` Renegociação, `RN` Remover negativações; status `A` Aberta / `F` Finalizada |
| `status_billing_hub` | billing hub communication | `NC` Não comunicado, `EC` Em comunicação, `CS` Comunicado com sucesso, `CE` Comunicado com erro |
| `id_remessa`, `id_remessa_alteracao`, `motivo_alteracao` | bank remittance and change reason (CNAB code) | see `fn_areceber_altera` |
| `id_nf_gerada`, `id_nf_opcional2..4`, `id_nota_gerada*` | invoices (notas fiscais) generated | → `vd_saida` |
| `desconto_condicional_valor`, `validade_desconto_condicional` | conditional discount and its deadline | |
| `nparcela`, `numero_parcela_recorrente`, `parcela_proporcional` | installment info | |

Relations: `id_cliente` → `cliente`; `id_contrato` → `cliente_contrato`; `id_carteira_cobranca` →
`fn_carteira_cobranca`; `id_conta` → `planejamento_analitico`; `id_mot_cancelamento` → `fn_areceber_mot_cancelamento`;
`conta_recebimento` → `contas`; `id_saida` → `vd_saida`.

Insert REQ (Postman): `id_cliente`, `id_conta`, `filial_id`, `data_emissao`, `data_vencimento`, `valor`, `previsao`,
`tipo_recebimento`, `id_carteira_cobranca`, `liberado: "S"`. Inserting a title **creates a debt for the end customer**
and may register a boleto/PIX at the bank/gateway and notify the customer; only on explicit request.

Listing used in production (Sufficit): last 20 titles of a customer, newest first.
```json
{ "qtype": "fn_areceber.id_cliente", "query": "<id_cliente>", "oper": "=", "page": "1", "rp": "20",
  "sortname": "fn_areceber.id", "sortorder": "desc" }
```
Fields read: `id`, `nn_boleto`, `status`, `data_emissao`, `data_vencimento`, `data_inicial`, `data_final`, `valor`,
`linha_digitavel`, `gateway_link`, plus the response `total` (count of all titles for the filter).

Open titles only (official flow): `grid_param` with `fn_areceber.liberado = S` and status not received/cancelled.
The official example uses `{"TB":"fn_areceber.status","OP":"!=","P":"R","P2":"C"}` and a due-date range with
`"OP":"BE"` (between) and `P`/`P2`. The `P2` on `!=` is undocumented; the safe portable form is
`status IN A,P` or `status = A` (plus a second call for `P`), and checking `status` client-side.
```json
{ "qtype": "fn_areceber.id_cliente", "query": "<id_cliente>", "oper": "=", "page": "1", "rp": "50",
  "sortname": "fn_areceber.data_vencimento", "sortorder": "asc",
  "grid_param": "[{\"TB\":\"fn_areceber.liberado\",\"OP\":\"=\",\"P\":\"S\"},{\"TB\":\"fn_areceber.status\",\"OP\":\"IN\",\"P\":\"A,P\"}]" }
```
Overdue = `status` A/P and `data_vencimento` < today.

### `fn_areceber_altera` — edit a receivable (Alterar a receber)
Operations: list (`qtype` uses `fn_areceber.*`) / update `PUT /fn_areceber_altera/<id>` / delete. The UI "Alterar"
button; accepts only the editable subset. **Write** (changes due date, wallet, method; may generate a bank
remittance change).

| Field | Meaning | Values / notes |
|---|---|---|
| `documento`, `obs` | document, notes | |
| `data_emissao`, `data_vencimento` | dates | REQ |
| `id_carteira_cobranca` | wallet | REQ → `fn_carteira_cobranca` |
| `tipo_recebimento` | method | `Boleto`, `Cheque`, `Cartão`, `Dinheiro`, `Depósito`, `Gateway`, `Débito`, `Fatura`, `ArrecadacaoRecebimento`, `Pix` |
| `status` | `A` À receber, `R` Recebido, `P` Parcial, `C` Cancelado | do not change status here; use the actions |
| `aguardando_confirmacao_pagamento` | `S`/`N` | |
| `nn_boleto`, `pix_txid` | nosso número, PIX txid | |
| `libera_periodo` | `S`/`N`, REQ | |
| `liberado` | `S`/`N`; **must be `S`** or the invoice becomes hidden | |
| `titulo_protestado` | `S`/`N` | |
| `id_remessa_alteracao`, `motivo_alteracao` | remittance change and CNAB reason | e.g. `06` Alteração de Vencimento, `07` Concessão de desconto, `08` Cancelamento de desconto, `15` Dispensar cobrança de multa, `16` Alteração do valor de desconto, `17` Não conceder desconto (full list on `fn_areceber.motivo_alteracao`: also `03`,`04`,`05`,`09`–`14`,`18`–`24`,`30`,`31`,`33`–`35`,`40`–`46`,`49`) |

Send all fields (read the record first). Example body: `{"documento":"…","data_emissao":"19/06/2024",
"data_vencimento":"10/07/2024","id_carteira_cobranca":"1","obs":"…","tipo_recebimento":"Gateway","status":"A",
"aguardando_confirmacao_pagamento":"N","nn_boleto":"…","pix_txid":"","libera_periodo":"N","liberado":"S",
"titulo_protestado":"N","id_remessa_alteracao":"","motivo_alteracao":""}`. Delete here = deletes the title
(destructive).

### `fn_areceber_baixas` — receipts / payment settlements (Recebimentos)
Operations: list (`qtype` on `fn_movim_finan.*`, because each receipt is a financial movement) and delete
(`DELETE /fn_areceber_baixas/<id_recebimento>` = **estornar** the receipt, reopening the title).

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | receipt (movement) id | |
| `id_receber` | title | → `fn_areceber.id`; filter on it to see payments of one title |
| `data` | receipt date | |
| `credito` | amount credited | |
| `vdesconto` / `vacrescimo` / `descontos_adicionais` | discount / surcharge | |
| `valor_total_recebido`, `valor_liquido_recebido` | total / net received | |
| `historico`, `documento` | description, document | |
| `tipo_recebimento` | `D` Dinheiro, `H` Cheque, `C` Cartão de crédito, `CD` Cartão de Débito, `DP` Depósito, `P` Pix (EM DSV), `T` Transferência, `B` Boleto, `DC` Débito em conta | |
| `conta_` | cash/bank account | → `contas` |
| `id_lote_retorno` | bank return batch that settled it | |

### `fn_areceber_recebimentos` — cancel receivables (Cancelar recebíveis)
Operation used: `PUT /fn_areceber_recebimentos/<id_receber>` = UI "Cancelar Boletos" (see Actions). n8n also lists
list/insert/delete for this resource; only the cancel form is documented.

### `fn_areceber_mot_cancelamento` — cancellation reasons (Motivos de cancelamento)
Operations: list / insert / update / delete. Needed to cancel a title (`id_mot_cancelamento`). Also used by
contract cancellation.

| Field | Meaning | Values |
|---|---|---|
| `motivo` | reason text | REQ |
| `id_conta` | account for cancelled value | → `planejamento_analitico`; REQ |
| `ativo` | `S`/`N` | |
| `libera_periodo` | `S`/`N`, REQ | |
| `inadimplencia` | counts as default (inadimplência) | `S`/`N` |
| `nao_vencidos_inadimplencia` | not-yet-due titles count as default | `S`/`N` |
| `finalidade` | applies to | `C` Contrato, `F` Financeiro, `A` Ambos |
| `considerar_churn` | counts in churn | `S`/`N` |

### `fn_carteira_cobranca` — billing wallets (Carteira de cobrança)
Operations: list / insert / update / delete. Bank/gateway configuration behind boletos and PIX (bank agreement,
nosso número counters, interest/fine, gateway tokens). Read-only for agents; editing breaks billing. Contains
secrets (gateway tokens, PIX client secret, certificates) — never print them.

| Field | Meaning | Values / notes |
|---|---|---|
| `descricao` | name | REQ |
| `id_conta` | bank/cash account | → `contas`; REQ |
| `tipo_recebimento` | method | same list as `fn_areceber` (default `Boleto`) |
| `registrado` | registered boleto | `S`/`N`; REQ |
| `ativo` | `S`/`N`; REQ | |
| `filial_id` | branch | → `filial` |
| `lancamento_tarifa` | when the bank fee is posted | `L` Na data do pagamento, `C` Na data do crédito; REQ |
| `tipo_carteira` | `1` Simples, `2` Vinculada, `3` Caucionada, `4` Vendor, `5` ECR | |
| `jurop`, `jurov`, `jurop_mes`, `multap`, `multav` | interest/fine percent / value | used by `get_boleto` `juro`/`multa` and `calcula_juros_multa` |
| `desconto_p`, `desconto_v`, `desconto_condicional_*`, `desconto_proporcional` | discounts | |
| `dias_vencimento_fatura`, `dias_limite_pagamento_apos_vencimento` | days | defaults 1 / 90 |
| `gateway_nome` | gateway | e.g. `fortunus`=Efí, `widepay`, `boleto_facil`=Juno, `credi_sis`, `galaxPay`=Cel payments, `sicoobApi`, `sicrediApi`, … |
| `gera_pix_gateway`, `enviar_cobranca_pix_whatsapp` | PIX via gateway, send PIX by WhatsApp | `S`/`N` |
| `pix_gateway` | PIX provider | `GN` Efí, `MB` modobank, `SB` Sicoob, `ST` Santander, `BB` Banco do Brasil |
| `pix_modalidade` | `I` Imediata, `C` Cobrança | |
| `pix_ambiente` | `H` Homologação, `P` Produção | |
| `tipo_chave_pix` | `CPF_CNPJ`, `CELULAR`, `EMAIL`, `ALEATORIA`, `COPIA_E_COLA` | |
| `utiliza_pix_recorrente` | PIX Automático | `S`/`N` |
| `tipo_baixa` | how partial/over payment is handled | `D` Desconto, `P` Incluir na próxima fatura (contratos), `B` Baixa parcial |
| `pedido_baixa_automatico*`, `baixa_automatica*` | automatic write-off rules | insert REQ: `pedido_baixa_automatico_recorencia_cartao`, `filtra_inicio_nn` |

### `contas` — cash and bank accounts (Contas)
Operations: list / insert / update / delete. Where money lands (`conta_` in receipts/payments).

| Field | Meaning | Values |
|---|---|---|
| `conta` | name | REQ |
| `tipo_conta` | `C` Caixa, `B` Banco, `D` Dividendos | REQ |
| `data_abertura`, `saldo_abertura` | opening date / balance | date REQ |
| `id_planejamento` | analytical account | → `planejamento_analitico`; REQ |
| `filial_padrao` | default branch | → `filial`; REQ |
| `permitir_pag_saldo_negativo` | allow payment with negative balance | `S`/`N`; REQ |
| `ativo` | REQ | |
| `cod_banco`, `agencia(_dv)`, `numero_conta(_dv)`, `modalidade_conta` | bank data | modalidade `CONTA_CORRENTE` / `CONTA_PAGAMENTO` |
| `integration_name`, `integration_environment`, `integration_client_id/secret` | bank API integration (`modobank`) | env `H` Homologação / `P` Produção; secrets |

### `condicoes_pagamento` — payment terms (Condições de pagamento)
Operations: list / insert / update / delete. Required by the renegotiation wizard (`id_condicao_pagamento`).

| Field | Meaning | Values |
|---|---|---|
| `nome` | name | REQ |
| `ativo` | `S`/`N` | |
| `compra_venda` | applies to | `A` Ambas, `C` Entrada, `V` Saída; REQ |
| `ind_pag` | `1` A prazo, `0` À vista, `2` Outras | REQ |
| `n_parcelas` | number of installments | REQ |
| `com_entrada` | with down payment | `S`/`N`; REQ |
| `tipo` | schedule | `M` Mensal, `T` 30 em 30 dias, `P` Personalizado; REQ |
| `dia_fixo`, `periodicidade`, `vencimento_personalizado` | fixed day; `T` Trimestral `S` Semestral `A` Anual; custom days | |
| `desconto_max` | max discount % | REQ, default `0.00` |
| `baixa_primeira` | settle first installment immediately | `S`/`N` |

### `fn_apagar` — payables (Contas a pagar)
Operations: list / insert / update / delete. The ISP's own bills to suppliers (not end-customer debt).

| Field | Meaning | Values / notes |
|---|---|---|
| `id_fornecedor` | supplier | → `fornecedor`; REQ |
| `data_emissao`, `data_vencimento`, `valor` | REQ | |
| `id_contas` | paying cash/bank account | → `contas`; REQ |
| `id_conta` | expense account | → `planejamento_analitico` (Postman marks REQ) |
| `filial_id` | REQ | |
| `tipo_pagamento` | `Dinheiro`, `Boleto`, `Cheque`, `Cartão`, `Depósito`, `Débito`, `Transferencia`, `Pix`; REQ | |
| `tipo_pix`, `chave_pix`, `codigo_barras`, `id_dado_bancario` | how to pay | tipo_pix `CPF_CNPJ`, `CELULAR`, `EMAIL`, `ALEATORIA`, `COPIA_E_COLA` |
| `previsao` | `N` Competência, `S` Caixa, `M` Manual; REQ | |
| `status` | `A` A pagar, `F` Pago, `P` Parcial, `C` Cancelado | RO |
| `status_auditoria` | `A` Aprovado, `R` Reprovado, `C` Corrigido, `N` Não auditado | |
| `liberado` | must be `S` | |
| `valor_aberto`, `valor_pago`, `valor_total_pago`, `data_pagamento`, `valor_cancelado`, `data_cancelamento`, `id_mot_cancelamento` | RO | |
| `id_entrada` | purchase | → `entrada` |
| `eh_despesa_veiculo`, `id_despesa_veiculo` | vehicle expense | |
| centro de custo fields | `centro_custo_regra_criterio` `CE` Centro de custos / `CR` Critério de rateio | |

### `fn_apagar_arquivos` — payable attachments (Arquivos)
List by `fn_apagar_arquivos.id_apagar` (Postman omits the `listar` header; add it). Insert = multipart form-data
`arquivo`, `id_apagar`, `descricao`. `DELETE /fn_apagar_arquivos/<id_arquivo>`. Download: see Actions.

### `fn_movim_finan` — accounting entries (Lançamentos contábeis)
Operations: list / insert / update / delete. Every receipt, payment, transfer and manual entry is a movement.

| Field | Meaning | Values |
|---|---|---|
| `id_conta` | analytical account | → `planejamento_analitico`; REQ (Postman example uses a cash account id) |
| `data` | date | REQ |
| `debito` / `credito` | amounts | |
| `historico` | description | REQ |
| `tipo_lanc` | entry type | default `M` (manual); examples use `C` credit, `D` debit, `P` payment |
| `id_movim_finan` | parent movement | |
| `id_entrada` / `id_saida` | purchase / sale | |
| `filial_id` | REQ in catalog | |
| `registrado_por`, `atualizado_por` | users | RO |

`fn_movim_finan_credito` (Lançamentos a crédito) and `fn_movim_finan_debito` (Lançamentos a débito): same entity
filtered by side; list with `qtype` on `fn_movim_finan.*`; insert REQ `id_conta`, `data`, `historico` plus `credito`
(`tipo_lanc: "C"`) or `debito` (`tipo_lanc: "D"`), optional `id_movim_finan`, `documento`. Update/delete
`/<table>/<id>`. **Writes change account balances.**

### Planning / chart of accounts
| Table | Purpose (UI) | Key fields |
|---|---|---|
| `planejamento` | synthetic account (Planejamento gerencial / Conta contábil sintética) | `planejamento` REQ name; `tipo` REQ `A` Ativo, `P` Passivo, `R` Receitas, `D` Despesas, `C` Custo, `PT` Patrimônio; `subtipo` `CF` Custo fixo, `CV` Custo variável, `DF` Despesa fixa, `DV` Despesa variável, `DA` Depreciação/amortização; `nivel_superior` → `planejamento`; `cod_planejamento` |
| `planejamento_analitico` | analytical account (Planejamento gerencial analítico) — the `id_conta` of titles and entries | `id_planejamento` REQ → `planejamento`; `planejamento_analitico` REQ name; `ativo` REQ `S`/`N`; `previsao` `M` Manual, `S` Caixa, `N` Competência; `id_planejamento_analitico_finan` → class |
| `planejamento_analitico_finan` | financial class (Classe financeira analítica gerencial) — `id_conta_class_finan*` | `id_planejamento_finan` REQ; `planejamento_analitico` REQ name |

All three: list / insert / update / delete. Structural config; do not change without the ISP's accountant.

### `fn_feriados` — holidays (Feriados)
List / insert / update / delete. Fields: `descricao`, `data` (both REQ), `id_filial` → `filial`. Affects due-date
shifting and interest calculation.

### `cnf_classificacao_tributaria` — tax classification (Classificação tributária)
List / insert / update / delete. Tax rules applied to products/plans on invoice (NF) generation.

| Field | Meaning | Values |
|---|---|---|
| `descricao` | REQ | |
| `tipo_operacao` | `E` Entrada, `S` Saída | |
| `cf_tipo_tributacao` | `ICMS`, `ISSQN`, `NT` Não tributado | REQ |
| `cf_cfop`, `cf_cfop_f` | CFOP → `cnf_cfop`; `cf_ncm` → `produtos_ncm` | |
| `codigo_classificacao_sped` | SPED item class (e.g. `0101` telefonia, `0102` comunicação de dados, `0103` TV) | |
| `icms_regime` | `1` Simples Nacional, `2` Tributação Normal | |
| `icms_sn_stributaria`, `icms_sn_origem`, `modBC`, `cf_aliquota_icms`, … | ICMS | |
| `pis_*`, `cofins_*`, `cf_ipi_*`, `iss_*`, `irrf_*`, `csll_aliquota`, `p_fust`, `p_funttel` | other taxes | insert REQ: `descontar_icms_base_calculo`, `descontar_icms_base_calculo_cofins` (`S`/`N`), `irrf_tipo_retencao` (example `CX`) |

Fiscal config: never edit from an agent unless the ISP's accountant asked.

## Actions

### `get_boleto` — boleto PDF, invoice data, or send by e-mail/SMS (Imprimir boleto / Segunda via)
`POST /get_boleto` (no header). The official CPF flow uses `GET` with `ixcsoft: listar`; both are documented.

| Field | Meaning |
|---|---|
| `boletos` | title id(s) from `fn_areceber.id`, comma-separated (`"2233,3344"`) |
| `juro` | `S`/`N` — add interest for late payment |
| `multa` | `S`/`N` — add late fine |
| `atualiza_boleto` | default `S`; with `S`, an overdue boleto is recalculated (new due date/value with juro/multa, inferred) — the official flow says "always S". Sufficit production sends `N` to get the boleto exactly as issued |
| `tipo_boleto` | `arquivo` (default, PDF file), `dados` (invoice data, no file), `mail` (send by e-mail), `sms` (send by SMS) |
| `base64` | `S` returns the PDF base64-encoded, `N` returns binary (convert to PDF either way); used with `arquivo`/`dados` |
| `layout_impressao` | optional custom print layout id |

Production (Sufficit) body: `{"boletos":"<id>","juro":"N","multa":"N","atualiza_boleto":"N","tipo_boleto":"<type>"}`.

Response notes:
- `arquivo` + `base64: S`: a very large base64 string (hundreds of KB per boleto). Never print it to the chat or
  logs; decode to a `.pdf` file or forward as an attachment. Check for `{"type":"error"}` JSON before decoding.
- `dados`: structured boleto data; official note: works only when the title's `tipo_recebimento` is `Boleto`.
- `mail` / `sms`: **messages the end customer.** `mail` requires the e-mail templates configured in Configurações >
  Parâmetros > Parâmetros financeiro > Geral ("Servidor de e-mail boletos e faturas" / "… para vários boletos e
  faturas"); `sms` requires an SMS gateway and "SMS para envio de boletos"; SMS carries the boleto data, not the
  file. Confirm before sending.
- Effect: read (`arquivo`/`dados` with `atualiza_boleto: N`); `atualiza_boleto: S` may update the title (inferred);
  `mail`/`sms` = outbound customer message.

### `get_pix` — PIX copy-paste code of a title (Copiar código PIX)
`POST /get_pix` (official flow: `GET` + `ixcsoft: listar`), body `{"id_areceber":"<fn_areceber.id>"}`. Returns the
PIX data of the title (copy-paste "EMV" string and QR, inferred; inspect the actual keys). Works only when the
title's wallet generates PIX (`fn_carteira_cobranca.gera_pix_gateway`/`pix_gateway`). Effect: read (may create the
PIX charge at the provider on first call, inferred). Related: `get_pix_parameter` (n8n, unmapped) reads PIX
parameters of the installation.

### `fn_areceber_altera` (PUT) — edit title ("Alterar Boleto")
See table above. **Write**: changing `data_vencimento`/values of a registered boleto generates a remittance change;
keep `liberado: "S"`.

### `cancelar_financeiro` — cancel a title (Cancelar boleto)
`POST /cancelar_financeiro`, body `{"id":"<fn_areceber.id>","id_mot_cancelamento":"<id>","data_cancelamento":"DD/MM/YYYY"}`.
**Destructive write**: sets the title to `C`, removes the debt from the customer, may request bank write-off
(pedido de baixa) and counts in default/churn per the reason. Reversible only with `estornar_cancelamento`.

### `fn_areceber_recebimentos` (PUT) — cancel title with value ("Cancelar Boletos")
`PUT /fn_areceber_recebimentos/<id_receber>`. Body (official comments): `valor_cancelado` REQ (amount to cancel),
`id_cliente` REQ, `id_mot_cancelamento` REQ → `fn_areceber_mot_cancelamento`, `data_cancelamento` REQ, `obs`
optional, `status` REQ (`A` Aberto, `R` Recebido, `P` Parcial, `C` Cancelado), hidden fields copied from the title:
`data_emissao`, `data_vencimento`, `valor` (REQ), `cancelar_fatura`, `id_conta`, `documento`, `tipo_recebimento`,
`id_carteira_cobranca`, `id_saida`, `valor_recebido`, `valor_aberto`, `liberado` (recommended `S`, else hidden),
`libera_periodo`, `cancelamento_id_operador` → `usuarios`. **Destructive write**, same effects as
`cancelar_financeiro`; allows partial cancellation.

### `estornar_cancelamento` — undo a cancellation (Estornar boleto cancelado)
`DELETE /estornar_cancelamento`, body `{"get_id":"<fn_areceber.id>"}`. **Write**: reopens a cancelled title (debt
returns to the customer).

### `fn_areceber_recebimentos_baixas_novo` — receive a title manually (Receber boleto / baixa manual)
`POST /fn_areceber_recebimentos_baixas_novo`. Fields (empty in the official example; meanings from the
`fn_areceber_baixas` form): `filial_id`, `id_receber` (title id), `conta_` (cash/bank account → `contas`), `id_conta`
(analytical account), `tipo_recebimento` (`D`,`H`,`C`,`CD`,`DP`,`P`,`T`,`B`,`DC`), `data`, `documento`, `pdesconto` /
`vdesconto` (discount % / value), `id_motivo_desconto`, `pacrescimo` / `vacrescimo` (surcharge % / value),
`valor_parcela` (title amount), `credito`, `debito`, `valor_total_recebido`, `historico`, `tipo_r`, `previsao`,
`tipo_lanc` (last three undocumented; mirror the UI defaults — the payables equivalent uses `tipo_p: "T"`,
`tipo_lanc: "P"`). **Write that moves money in the books**: marks the title `R`/`P`, credits the account, may
unblock the customer's contract and request bank write-off. Only when the user confirms the payment really
happened. Undo: `DELETE /fn_areceber_baixas/<id_recebimento>`.

### `DELETE /fn_areceber_baixas/<id_recebimento>` — reverse a receipt (Estornar recebimento)
`id_recebimento` = `fn_areceber_baixas.id` (a `fn_movim_finan` id). **Destructive write**: the title goes back to
open/partial and the customer owes again (may trigger blocking by the collection rules).

### `fn_areceber_agrupamento` — list titles for invoice grouping (Agrupamento de faturas)
`POST /fn_areceber_agrupamento`, body `{"idCliente":"<id>","idContrato":"","limiteDiasBusca":"100","rp":"1000","page":"1"}`
(`idContrato` optional; `limiteDiasBusca` = number of days considered). Read: lists titles eligible to be grouped
into one invoice. Note camelCase parameters.

### `fn_areceber_26382` — unmapped receivable button (n8n only, no parameters documented). Do not call.

### Renegotiation wizard (ordered flow)
Renegotiation replaces open titles with new ones (new installments, interest/fine/discounts). **Write that rewrites
the customer's debt**: originals become renegotiated (`titulo_renegociado`), new titles are created, often with new
boletos sent. Run only on explicit request, showing the user totals before step 5.

1. `POST /renegociar_selecionados` body `{"get_id":"<id1>,<id2>"}` (fn_areceber ids). Opens a renegotiation with
   the selected titles; the response carries the renegotiation id (`fn_renegociacao_wiz.id`; inspect the response).
2. `PUT /fn_renegociacao_wiz/<id_renegociacao>` fill the wizard (edit only; official warning: this endpoint opens a
   renegotiation with or without titles, use it only to edit). REQ: `id_filial`, `id_conta` (revenue account),
   `id_cliente`, `data_emissao`, `previsao` (`S`/`N`/`M`), `id_carteira_cobranca`, `id_condicao_pagamento` →
   `condicoes_pagamento`, `contrato_renegociacao` (contract id), `valor_parcelas`, `valor_total`,
   `valor_renegociado`, `valor_total_pagar`, `status: "A"`, `finalizar: "N"`. Optional: `vendedor_renegociacao`,
   `data_vencimento` (first due date), `valor_acrescimos`, `valor_descontos` (`"0,00"` format), `acre_juros_multa`,
   `data_finalizada` (empty).
3. Adjust titles: `POST /adicionar_titulo_renegociacao` `{"id_renegociacao_aux":"<id_renegociacao>","get_id":"<fn_areceber.id>"}`;
   `POST /remover_titulo_renegociacao` `{"id_renegociacao":"<id_renegociacao>","get_id":"<fn_areceber.id>"}`
   (note the different key names).
4. `POST /calcula_juros_multa` `{"id_carteira_cobranca":"<id>","id_condicao_pagamento":"<id>","id":"<id_renegociacao>"}`
   recalculates interest/fine and installments. Run again after any add/remove.
5. Finalize: `PUT /fn_renegociacao_wiz/<id_renegociacao>` with the same body, `status: "A"` (keep),
   `data_finalizada: "<today DD/MM/YYYY>"`, `finalizar: "S"`. This generates the new titles.

### Payables buttons
| Endpoint | What it does | Effect |
|---|---|---|
| `POST /fn_apagar_pagamentos_baixas` and `POST /botao_pagar_26409` | pay a payable manually (Pagar / baixa manual). Same body: `id_pagar` (+`_label`), `filial`, `conta_` (paying account → `contas`, +`conta__label`), `tipo_pagamento` (example `D` Dinheiro), `chave_pix`, `cheque_*`, `id_conta_class_finan_a`, `id_conta`, `data`, `documento`, `pdesconto`/`vdesconto`, `pacrescimo`/`vacrescimo`, `valor_parcela`, `debito`, `valor_total_pago` (`"0,20"` format), `historico`, `tipo_p: "T"`, `tipo_lanc: "P"`, `filial_id`, `id_operador`. `botao_pagar_26409` is the newer button id of the same form (n8n: unmapped) | write, money out in books |
| `POST /botao_estornar_cancelamento_26200` `{"get_id":"<fn_apagar.id>"}` | undo cancellation of a payable (Estornar pagamento cancelado) | write |
| `DELETE /fn_apagar_baixas/<id_movim_finan>` | reverse a payment of a payable (Estornar pagamento) | destructive write |
| `POST /fn_apagar_auditoria` | audit a payable: `status` `A` Aprovado / `R` Reprovado / `C` Corrigido, `id_fn_apagar` REQ, `tipo` `I` Interno / `E` Externo, `motivo`, `operador`, `data_hora` | write (audit trail) |
| `POST /fn_apagar_arquivos_download` `{"id":"<id_arquivo>"}` | download a payable attachment (one Postman copy passes the payable id; use the file id) | read, binary |

### Fiscal reports
| Endpoint | What it does |
|---|---|
| `GET /botao_rel_19314` (`ixcsoft: listar`) | print NF modelo 21/22 (telecom invoices) for a period |
| `GET /botao_rel_25740` (`ixcsoft: listar`) | same report with the custom print layout |

Body (both): `id_filial`, `mes`, `ano`, `data_emissao`, `tipo_contrato` (example `X`), `produto`, `cidade`,
`tipo_pessoa` (`T`, inferred Todos), `modelo` (`T`), `finalidade` (`N`), `id_vd_inicial`/`id_vd_final` (sale id
range), `num_nf_inicial`/`num_nf_final`, `serie_nota`, `identificacao_estrutura` (`N`), `base_geracao_tipo_doc`
(`P`), `lucro_presumido` (`S`), `gerar_convenio_segundo_plano` (`S`, generate in background), `id_cliente`,
`id_mensagem`. Code meanings beyond the examples are undocumented. Read-only but heavy; restrict by `id_filial`,
month and customer.

## Recipes

### Open invoices by CPF/CNPJ → PIX copy-paste or linha digitável
1. Mask the document (`000.000.000-00` / `00.000.000/0000-00`), list `cliente` with
   `qtype: cliente.cnpj_cpf`, `oper: =`, `rp: 1`; take `id` (several matches → ask which). See [customers](customers.md).
2. List `fn_areceber` by `id_cliente` with `grid_param` `liberado = S` and `status IN A,P`, sorted by
   `fn_areceber.data_vencimento asc`. Check `type` for errors; `total: 0` → "no open invoices".
3. Present each title: `id`, `data_vencimento` (overdue?), `valor_aberto` (fallback `valor`), `data_inicial`–`data_final`.
4. For the chosen title:
   - PIX: `POST /get_pix {"id_areceber":"<id>"}` → copy-paste string. Empty/error → wallet has no PIX.
   - Boleto: use `linha_digitavel` from the listing; `gateway_link` if present is the payment page.
   - PDF: `get_boleto` `tipo_boleto: arquivo`, `base64: S`, save to file and send as attachment.
   For overdue titles the stored line/PIX may reflect the original due date; `atualiza_boleto: "S"` with
   `juro`/`multa` `S` gives an updated boleto (confirm with the ISP's policy).
5. Do not mark anything as paid; payment confirmation comes from the bank/gateway return.

### Last invoices of a customer (production pattern)
`fn_areceber` by `id_cliente`, `rp: 20`, `sortname: fn_areceber.id`, `sortorder: desc`; read `nn_boleto`, `status`,
`data_emissao`, `data_vencimento`, `data_inicial`, `data_final`, `valor`, `linha_digitavel`, `gateway_link` and
`total`. Then `get_boleto {"boletos":"<id>","juro":"N","multa":"N","atualiza_boleto":"N","tipo_boleto":"arquivo"}`
for the second copy.

### "I already paid" check
List `fn_areceber` by `id`; `status R` = paid (see `pagamento_data`, `valor_recebido`, `recebido_via_pix`).
`aguardando_confirmacao_pagamento: S` = waiting confirmation. Still `A`: list `fn_areceber_baixas` filtered by
`fn_areceber_baixas.id_receber` (empty = no receipt). Bank returns usually post D+1/D+2; do not do a manual baixa
without proof and explicit operator request.

### Send second copy by e-mail
Confirm the customer's e-mail in `cliente`, then `get_boleto` `{"boletos":"<id>","juro":"S","multa":"S","atualiza_boleto":"S","tipo_boleto":"mail"}`.
Messages the end customer; error = e-mail template not configured.

### Cancel a title (on explicit request)
List `fn_areceber_mot_cancelamento` (`ativo S`, `finalidade F`/`A`), confirm reason, title, value with the user,
then `cancelar_financeiro`. Undo: `estornar_cancelamento {"get_id":"<id>"}`.

### Change a due date
List `fn_areceber_altera` by `fn_areceber.id`, change `data_vencimento` on the returned object (keep `liberado: S`,
set `motivo_alteracao: "06"` when the wallet is registered and the ISP uses remittance changes), `PUT` the whole
object, then re-list to verify.

### Renegotiate overdue titles
Collect overdue ids (status A/P, past due) → steps 1–5 of the wizard; present `valor_total_pagar`, installments
(`condicoes_pagamento`) and first due date to the user before `finalizar: "S"`; afterwards list the customer's new
titles and send them (`get_boleto`).
