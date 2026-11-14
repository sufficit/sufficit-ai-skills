# IXC inventory, purchasing and sales

Stock (almoxarifados, balances, transfers, material requests, patrimony), product catalog, purchasing
(requisição → pedido → compra/entrada), sales and invoices (vd_saida), fleet, and the "products of a technician /
of a contract" flows. Use it for "what equipment does technician X hold", "is product Y in stock", "issue/print the
sale invoice", "move a router to another warehouse". Shared mechanics (auth, `ixcsoft: listar`, search body,
errors) are in [request mechanics](requests.md); contracts and plans are in [customers](customers.md), receivables
in [financial](financial.md), service orders in [support](support.md).

Notes for this module:
- Insert/update examples in the official collection send dates as `DD/MM/YYYY` (UI format), e.g. `"data": "20/06/2024"`;
  listings return `YYYY-MM-DD`. Send the format the examples show for each table.
- Quantities and conversion factors are decimals with many places (`"qtde": "1.00000"`, `"fator_conversao": "1.000000000"`).
- Several listings use a **different table prefix** in `qtype` than the endpoint name (marked "prefix" below), e.g.
  `vd_saida_produtos` filters on `movimento_produtos.*`, `vd_pedido_venda` on `pedido.*`,
  `estoque_min_max_almox` on `estoque_min_max.*`. Use the prefix shown, not the endpoint name.
- Most writes here move stock or create fiscal/financial documents. Confirm every write with the user; never delete
  without an explicit request for that record.

## Tables

### Stock and warehouses

#### `almox` — warehouse / stock location (Almoxarifado)
Operations: list / insert / update / delete. A warehouse can be a physical stock room or a technician's van/personal
stock (technicians are linked to warehouses through `almox_usuario`, see [administration](administration.md)).
| Field | Meaning | Values / notes |
|---|---|---|
| `id` | warehouse id | |
| `descricao` | name | REQ, max 150 |
| `id_filial` | branch | REQ → `filial` |
| `ativo` | active | REQ `S`/`N` |
| `requisitar_preferencialmente_de` | default warehouse to request material from | → `almox` (via `requisitar_preferencialmente_de_almox`) |
Insert example (all fields required): `{"descricao":"<nome>","id_filial":"1","ativo":"S","requisitar_preferencialmente_de":"1"}`.

#### `estoque_produtos_almox_filial` — stock balance per product/warehouse/branch (Saldos por almoxarifado / Meu estoque)
Operations: list only (read view). This is the answer to "how many of X are in warehouse Y".
| Field | Meaning | Values / notes |
|---|---|---|
| `id_produto` / `produto_descricao` | product | → `produtos` |
| `id_almox` / `almox_descricao` / `almox_ativo` | warehouse, name, active `S`/`N` | → `almox` |
| `id_filial` | branch | → `filial` |
| `saldo` | balance in the product unit | decimal string |
| `produto_unidade` | unit | |
| `produto_controla_estoque` | product controls stock | `S`/`N` |
| `produto_tipo`, `produto_ativo`, `produto_preco_base`, `produto_pcomissao`, `produto_id_class_fiscal` | product attributes copied into the view | |
Example: `{"qtype":"estoque_produtos_almox_filial.id_almox","query":"<id_almox>","oper":"=","page":"1","rp":"100"}`.

#### `estoque_min_max_almox` — min/max stock per product and warehouse (Estoque mínimo e máximo)
Operations: list / insert / update / delete. **Prefix:** `qtype` uses `estoque_min_max.<field>`.
Fields: `id_produto` → `produtos`; `id_almox` → `almox`; `qtd_min`, `qtd_max` (decimals); `requisitar_mutiplo_de`
[sic] = fixed reorder quantity ("Quantidade fixa"); `status` = hidden field (example `"0"`).

#### `patrimonio` — serialized asset / patrimony item (Patrimônios)
Operations: list (the collection documents only listing). Each row is one physical unit (router, ONU, tool) with
its own patrimony number; used by `id_patrimonio` in transfers, comodato (loan to customer) and structures.
Filter by `patrimonio.id`. Field catalog not in the wiki extract; inspect a returned record before filtering on
other fields. The IXC n8n node also exposes an unmapped action `validate_mac` on this resource (no body documented).

#### `estrutura` — structure / site (Estrutura)
Operations: list / insert / update / delete. A physical site (POP, tower, cabinet, office) that holds patrimony and
consumed products.
| Field | Meaning | Values / notes |
|---|---|---|
| `descricao` | name | REQ, max 200 |
| `id_filial` | branch | → `filial` (REQ in the Postman example) |
| `id_cidade` | city | REQ → `cidade` |
| `ativo` | active | REQ, default `S` |
| `cep`, `endereco`, `numero`, `complemento`, `bairro`, `referencia`, `observacao`, `latitude`, `longitude` | address/location | |
| `id_planejamento_analitico` | accounting account | read-only |

#### `su_oss_mov_produto_estrutura` and `su_oss_mov_produto_estrutura_consumo` — products allocated to a structure
Both are views over `movimento_produtos` (stock movements); **prefix** `movimento_produtos.*` in `qtype`/`grid_param`.
- `su_oss_mov_produto_estrutura` — patrimony of the structure (Patrimônio). List with
  `qtype=movimento_produtos.id_estrutura` plus `grid_param` `imobilizado = S` and `patrimonio >= 1`.
- `su_oss_mov_produto_estrutura_consumo` — the same records seen as "Produto como patrimônio", and also "Outros
  produtos" (consumables) when filtered `imobilizado = N`.
Insert (write, **moves stock out of `id_almox` into the structure**). Required per the collection: `id_produto`,
`data` (`DD/MM/YYYY`), `id_unidade`, `id_almox`, `qtde_saida`, `valor_unitario`, `valor_total`,
`id_classificacao_tributaria`, `tipo` (`S` = outbound), `estoque` (`S`), `unidade_sigla`, `fator_conversao`,
`id_estrutura`, `imobilizado` (`S` = patrimony, `N` = other products); plus `patrimonio` (patrimony id) for the
patrimony variant. Optional links: `id_oss_chamado` (service order), `id_oss_mensagem`, `id_saida`, `descartado`.
The n8n node lists unmapped actions `baixar_produto_outro` and `descartar_produto` (discard) on the consumo resource;
no body is documented, do not call them without testing on a lab IXC.

### Transfers and material requests

#### `transf_almox_top` — transfer between warehouses, header (Transferência entre almoxarifados)
Operations: insert (documented); list fields from catalog. Immediate transfer (no confirmation step).
| Field | Meaning | Values / notes |
|---|---|---|
| `id_almox_saida` / `id_filial` | source warehouse / source branch | REQ → `almox` / `filial` |
| `id_almox_entrada` / `id_filial_entrada` | destination warehouse / destination branch | REQ |
| `data` | opening date | REQ, `DD/MM/YYYY` |
| `operador` | technician/operator of the operation | → `usuarios` (RO in catalog; Postman sends empty) |
| `obs` | note | REQ in the catalog |
| `documento`, `nf`, `id_saida` | generated document references | RO |

#### `transf_almox_item` — item of a warehouse transfer
Operations: insert. **Inserting the item executes the transfer immediately** ("Após cadastrar, já é feito a
transferência"). Fields: `id_transf_almox` (header id from `transf_almox_top`), `id_produto`, `id_unidade`,
`unidade_sigla`, `qtde`, `fator_conversao`, `tipo_produto` (`C` = commerce product, `P` = patrimony in the
examples), `id_patrimonio` (empty for plain products; the patrimony id for serialized items).

#### `transf_automatica` / `transf_automatica_produtos` — transfer log (Registros de transferências)
Operations: list (read-only). Records transfers made automatically by the system (e.g. when a service order
consumes material, `id_oss_chamado` filled). **Prefix:** `transf_almox.*` for `transf_automatica`,
`transf_almox_item.*` for `transf_automatica_produtos`.
Header fields: `id`, `data`, `operador`, `id_almox_saida`, `id_filial`, `id_almox_entrada`, `id_filial_entrada`,
`documento`, `obs`, `id_oss_chamado`, `id_produto`, `origem`. Item fields: `id`, `id_produto`, `qtde`,
`id_patrimonio`, `fator_conversao`, `id_transf_almox`.

#### `requisicao_devolucao_material` — transfer with confirmation (Transferência com confirmação)
Operations: insert (documented), list. A transfer between two people's warehouses that the **receiving
colaborador must confirm** (typical for handing equipment between technicians).
| Field | Meaning | Values / notes |
|---|---|---|
| `id_funcionario` | sender colaborador | REQ → `funcionarios` |
| `id_almox_origem` / `id_filial_origem` | source warehouse / branch | REQ |
| `id_funcionario_destino` | receiving colaborador | REQ → `funcionarios` |
| `id_almox_destino` / `id_filial_destino` | destination warehouse / branch | REQ (destination list comes from `requisicao_transferencia_materal_almox_dest`) |
| `data` | creation date | `DD/MM/YYYY` |
| `data_confirmacao` | confirmation date | do not fill; set by the confirm button |
| `observacao` | note | |
| `status` | transfer status | `1`=Aberta (default on insert), `2`=Aguardando Confirmação, `3`=Confirmada, `4`=Cancelada |

#### `itens_requisicao_devolucao_material` — items of a transfer with confirmation
Operations: insert. Fields: `id_requisicao_devolucao_material` (transfer id), `id_produto`, `id_unidade`
(→ `produtos_unidades`), `qtd`, `fator_conversao`, `tipo_produto` (hidden; product type such as `P`), and
`id_patrimonio` when the item is a serialized asset.

#### `requisicao_material` / `requisicao_material_item` — material request from a technician (Requisição de material)
Operations: list / insert / update / delete for both. A technician asks a warehouse for material.
| Field (`requisicao_material`) | Meaning | Values / notes |
|---|---|---|
| `id_filial` | branch | REQ |
| `id_tecnico` | requesting colaborador | REQ → `funcionarios` |
| `id_almox` | warehouse | REQ → `almox` |
| `data` | date | REQ `DD/MM/YYYY` |
| `status` | status | `A`=Aberto, `P`=Parcial, `F`=Fechado, `C`=Cancelado |
| `tipo` | origin | `A`=Automática, `M`=Manual (default) |
| `id_mot_cancelamento` | cancellation reason | → `transf_mot_cancelamento` |
| `id_usuario_confirma`, `id_usuario_cancelamento`, `data_confirmacao`, `data_cancelamento` | audit | RO |
Item fields: `id_requisicao` (REQ), `id_produto` (REQ), `qtde` (REQ), `descricao`, `status`,
`saldo_almox_solicitante`, `id_usuario`. (The collection's "editar item" example body is a copy of the header body;
for item updates send the item's own fields.) n8n also lists an unmapped `requisicao_material_item_27795`.

### Products

#### `produtos` — product / service catalog (Produtos)
Operations: list / insert / update / delete. Covers physical goods, patrimony models **and billable services**
(plans' products), so be careful: changing a service product can change what contracts bill.
| Field | Meaning | Values / notes |
|---|---|---|
| `descricao` | name | REQ, max 200 |
| `ativo` | active | REQ `S`/`N` |
| `tipo` | product type | REQ: `C`=Comércio, `S`=Serviço, `F`=Fabricação, `M`=Matéria Prima, `P`=Patrimônio, `O`=Consumo |
| `controla_estoque` | controls stock | REQ `S`/`N` |
| `movimentacao` | used in | REQ: `C`=Compra, `V`=Venda, `A`=Ambos (default) |
| `id_sub_grupo` | subgroup | REQ → `sub_grupo_produdos` |
| `unidade` | base unit | REQ → `unidades` |
| `preco_base` | base price | REQ, money |
| `valor`, `valor_custo`, `custo_medio`, `custo_medio_total`, `saldo` | computed price/cost/balance | RO |
| `aceita_valor` | | REQ, must be `P` |
| `icms_issqn` | tax regime | `ICMS` (default), `ISSQN`, `NT`=Não tributado |
| `id_class_fiscal` / `id_class_fiscal_entrada` | tax classification (out / in) | → `cnf_classificacao_tributaria` (out REQ in Postman) |
| `ncm` | NCM code | REQ in Postman → `produtos_ncm` |
| `cod_classificacao_servico` | telecom service classification (NFCom/SPED) | e.g. `0100401` = Assinatura de serviços de comunicação multimídia |
| `iss_natureza_operacao` | ISS nature | `1`=Tributação no município … `6`=Exigibilidade suspensa por procedimento administrativo |
| `controle_impressao_etiqueta` | label printing key | `5`=Padrão, `4`=MAC, `3`=Núm. Série, `2`=Núm. Patrimônio IXC, `1`=Cód. Patrimônio IXC |
| `id_fr_faturamento_classificacoes` | franchise billing class | → `fr_faturamento_classificacoes` |
| `plataforma`, `tv_*`, `id_sva_*`, `produto_playhub` | TV/SVA integration of service products | e.g. `plataforma`: `watch`, `playhub`, `ministrav2`… |
| `mostra_valor_ecommerce`, `tipo_ecommerce`, `ecommerce_prioridade` | e-commerce | REQ in Postman: `P`, `P`, `1` |
| `id_conta_estoque/despesa/receita/comodato` | accounting accounts | → `planejamento_analitico` |
The full product body has ~150 fields (vehicle fields `chassi`, `renavan`… for dealers, `checkbox1..40`); for
updates read the record and send it back whole.

#### Minor product tables
| Table | Purpose (UI label) | Ops | Key fields |
|---|---|---|---|
| `produtos_unidades` | units a product can be moved in (Unidades por produto) | L/I/U/D | all REQ: `id_produto`, `id_unidade` → `unidades`, `fator_conversao`, `sigla`, `ativo` `S`/`N` |
| `unidades` | measure units (Unidades) | L/I/U/D | `descricao`, `sigla` (max 10), `codigo` |
| `grupo_produtos` | product group (Grupo de produtos) | L/I/U/D | `grupo`, `codigo_alternativo` (both required per Postman) |
| `sub_grupo_produdos` [sic, "produdos"] | product subgroup (Subgrupos de produtos) | L/I/U/D | REQ `id_grupo` → `grupo_produtos`, `sub_grupo`, `id_conta_estoque`, `id_conta_despesa`, `id_conta_receita2` → `planejamento_analitico`; `tipo_produto`: `veiculo`, `motos`, `caminhao`, `estofados`; `ecommerce` `S`/`N` |
| `fr_faturamento_classificacoes` | franchise billing classification of products (Classificação produtos franquia) | L/I/U/D | `descricao` REQ, catalog values `Brisa Music`, `Watch TV`, `Link`, `Celeti hub`; `porcentagem`; `ativo` REQ `S`/`N` |

### Purchasing (Entradas)

#### `requisicao_compra` / `requisicao_compra_itens` — purchase requisition (Requisição de compra)
Operations: L/I/U/D for both. Internal request to buy.
Header: `filial_id` REQ, `data` REQ, `descricao` REQ, `funcionario` REQ → `funcionarios`, `id_setor` → `empresa_setor`,
`necessito_ate` (needed by), `status` RO `A`=Aberta, `F`=Fechada, `C`=Cancelada; `status_liberacao_compra` RO
`S`=Liberada, `N`=Não liberada; `descricao_cancelamento`, `id_pedido_compra`.
Items: `id_requisicao` REQ, `id_produto` REQ, `id_unidade` REQ, `qtde` REQ, `descricao_produto`, `id_pedido`,
`id_requisicao_material_item` (link to a material request item).

#### `pedido_compra` / `pedido_compra_itens` — purchase order to a supplier (Pedido de compra)
Operations: L/I/U/D for both.
| Field | Meaning | Values / notes |
|---|---|---|
| `data` | date | REQ |
| `id_fornecedor` | supplier | REQ → `fornecedor` ([customers](customers.md)) |
| `id_condicoes_pagamento` | payment terms | REQ → `condicoes_pagamento` |
| `filial_id` | branch | → `filial` |
| `status` | status | RO: `A`=Aberto, `F`=Fechado, `C`=Cancelado |
| `status_liberado` | approval | `S`=Liberado, `N`=Não liberado |
| `tipo_desconto` / `valor_desconto` | discount type / value | `P`=Porcentagem, `V`=Valor |
| `tipo_frete` / `valor_frete` | freight | `E`=Emitente, `D`=Destinatário, `S`=Sem frete |
| `previsao_entrega`, `previsao_faturamento`, `data_liberacao` | dates | |
| `valor_total_produtos`, `valor_final` | totals | RO |
| `id_colaborador` | buyer | → `funcionarios` |
Items: `id_pedido_compra` REQ, `id_produto` REQ, `id_unidade` REQ, `quantidade` REQ, `valor_unitario` REQ,
`valor_total` REQ, `status` REQ (`A`), `tipo` REQ (`E` = entrada), `descricao_alt`, `observacao`, `id_entrada`,
`unidade_sigla`.

#### `entrada` — purchase / goods receipt (Compra)
Operations: L/I/U/D. The fiscal entry of a supplier invoice; with `gera_estoque=S` it adds stock.
| Field | Meaning | Values / notes |
|---|---|---|
| `tipo_documento` | document type | REQ → `tipo_documento` (example `201`) |
| `id_fornecedor` | supplier | → `fornecedor` |
| `condicoes_pagamento` | payment terms | → `condicoes_pagamento` |
| `filial_id` | branch | REQ |
| `data_emissao` / `data_entrada` | issue / entry dates | REQ in Postman |
| `status` | status | RO: `A`=Aberta, `F`=Finalizada, `C`=Cancelada, `E`=Emitida |
| `gera_estoque` | generates stock | REQ `S`/`N` |
| `nfe_emitida` | NF-e issued by us | REQ, default `N` |
| `tipo_frete` | freight | `P`=Emitente, `A`=Destinatário, `9`=Sem frete |
| `tipo_entrada_compra` | how it was entered | `XML`, `DFE`=DF-e, `MANUAL` |
| `tipo_calculo_tributacao` | tax calc | RO: `XML`, `XMLA`=XML com alterações, `SIST`=Automático, `MAN`=Manual |
| `numero_nf`, `serie`, `modelo_nf`, `nfe_chave`, `arquivo_xml` | invoice identification | `arquivo_xml` import auto-creates supplier/carrier |
| `valor_total`, `icms_*`, `ipi_valor`, `vpis`, `vcofins`, `cbs_*`, `ibs_*`, retained taxes | totals | RO, computed |
| `realizar_rateio_outras_despesas` | spread other expenses | `S`/`N` |

| Related table | Purpose | Notes |
|---|---|---|
| `entrada_pedido` | links a purchase (`id_entrada`) to a purchase order (`id_pedido`) (Pedido de compra interno) | L/I |
| `movimento_produtos` | stock movement lines; for purchases filter `movimento_produtos.id_entrada` | L/I/U/D. REQ on insert: `id_produto`, `id_unidade`, `id_almox`, `quantidade`, `valor_unitario`, `valor_total`, `estoque` (`S`), `id_entrada`, `tipo` (`E` = entrada, `S` = saída), `unidade_sigla`. Same table backs sales items and structure allocations. |
| `fn_movim_finan` | accounting entries (Lançamentos contábeis) of a purchase or sale; filter `fn_movim_finan.id_entrada` or `.id_saida` | L/I/U/D. REQ: `id_conta` → `planejamento_analitico`, `data`, `historico`, `filial_id`; `debito`/`credito` RO; `tipo_lanc` default `M`. Accounting write: confirm with the user. |

### Sales and outbound (Saídas)

#### `vd_saida` — sale / outbound fiscal document (Venda)
Operations: L/I/U/D. Every sale, comodato outbound, activation fee and the base of NF-e/NFS-e/NFCom documents.
| Field | Meaning | Values / notes |
|---|---|---|
| `id_cliente` | customer | REQ → `cliente` |
| `id_contrato` / `id_contrato_avulso` | linked contract | → `cliente_contrato` |
| `id_tipo_documento` | document type | REQ → `tipo_documento` (example `501`) |
| `id_condicao_pagamento` | payment terms | REQ → `condicoes_pagamento` |
| `filial_id` | branch | REQ |
| `id_comissionado` | seller receiving commission | REQ → `vendedor` |
| `data_emissao` / `data_saida` | dates | REQ `DD/MM/YYYY` |
| `status` | status | RO: `A`=Aberto, `F`=Finalizado, `C`=Cancelado, `D`=Denegada, `AP`=Aguardando processamento, `PE`=Processado com erro |
| `gera_estoque` | moves stock | REQ `S`/`N` |
| `previsao` | accounting regime | `N`=Competência (Previsão Não, default), `S`=Caixa (Previsão Sim) |
| `modalidade_frete` | freight | REQ: `0`=emitente, `1`=destinatário, `2`=terceiros, `9`=Sem frete |
| `cnpj_venda`, `razao_venda` | use customer CNPJ / name on the document | REQ `S`/`N` (default `S`) |
| `informar_local_entrega` | separate delivery address | REQ `S`/`N`; `*_entrega` fields when `S` |
| `indFinal` | final consumer | `1`=Sim, `0`=Não |
| `indPres` | buyer presence | `1`=Presencial, `2`=Internet, `3`=Teleatendimento, `4`=NFC-e entrega, `5`=presencial fora do estabelecimento, `9`=Outros, `0`=Não se aplica |
| `impresso` | printed | `N`/`S` |
| `criada_contrato_taxa_ativacao` | created by contract activation fee | `N`/`S` |
| `numero_nf`, `serie`, `modelo_nf`, `nfse_status` (default `NE`), `nfse_lote`, `nfse_prot` | fiscal number/status | RO/system |
| `valor_total` | total | RO |
| `ids_areceber`, `data_vencimento_areceber` | receivables generated on finalize | RO → `fn_areceber` |
| `id_transf_almox_top`, `id_filial_destino` | inter-branch transfer sale | |
| `avalista_1`, `avalista_2` | guarantors | → `cliente` |

#### `vd_saida_produtos` — items of a sale
Operations: L/I/U/D. **Prefix:** `movimento_produtos.*` (e.g. `movimento_produtos.id_saida`). REQ on insert:
`id_saida`, `id_produto`, `id_unidade`, `id_almox`, `quantidade`, `qtde_saida`, `valor_unitario`, `valor_total`,
`estoque` (`S`), `tipo` (`S`), `fator_conversao`, `unidade_sigla`, `movimento_cancelamento_venda` (must be `N`).

#### `vd_pedido_venda` — sales order (Pedido de venda)
Operations: L/I/U/D. **Prefix:** `pedido.*`.
Fields: `cliente` REQ → `cliente`; `forma_pagamento` REQ → `condicoes_pagamento`; `vendedor` REQ → `vendedor`;
`data`, `data_entrega` REQ; `status` REQ `6`=Novo (default), `2`=Em processo, `4`=Faturado; `modalidade_frete`
`9`/`2`/`1`/`0` (as in `vd_saida`); `id_vd_saida` RO (sale generated); `filial_id` REQ; `percentual_desconto`;
export fields (`incoterm`, `porto_*`, `companhia_maritima`…).

#### Service-order sales (catalog only)
| Table | Purpose | Key fields |
|---|---|---|
| `pedido_os` | sales order created from a service order (Pedido de venda via O.S.) | `id_oss_chamado`, `id_saida` RO, `id_cliente` REQ, `id_contrato`, `id_condicao_pagamento` REQ; `status_pedido_os` `A`=Aberto, `F`=Concluído, `C`=Cancelado; `status_fat_os` `N`=Novo, `F`=Faturado, `C`=Cancelado, `A`=Aguardando faturamento; `tipo_produtos` `PRO`, `SER`, `COM`=Comodato, `PAT`=Patrimônio |
| `vd_saida_fat_os` | O.S. orders pending invoicing (Pedidos O.S.) | `status` `A`/`F`/`C`; `status_fat_os` `1`=Faturado, `2`=Cancelado, `3`=Aguardando faturamento |

### Contract products

| Table | Purpose | Notes |
|---|---|---|
| `vd_contratos_produtos` | products of a sales plan (`id_vd_contrato`) or of a specific contract (`id_contrato`) | List by `vd_contratos_produtos.id_vd_contrato` = the plan id taken from the contract (`cliente_contrato.id_vd_contrato`), or by `vd_contratos_produtos.id_contrato` for products added to that contract only. Full CRUD is in [customers](customers.md). |
| `view_vd_contratos_produtos_gen` | read view: all products effectively billed on a contract (plan + contract-specific) | List by `view_vd_contratos_produtos_gen.cliente_contrato_id`. n8n also exposes button `api_get_produtos_contrato` with `{"id_contrato": "<id>"}` (Produtos por Contrato 2). |

### Fleet (Frota)

| Table | Purpose (UI label) | Ops | Key fields |
|---|---|---|---|
| `veiculos` | company vehicles (Veículos) | L/I/U/D | REQ `placa`, `descricao`, `oleo` (oil-change km), `tipo_rodado` (`01` Truck, `02` Toco, `03` Cavalo Mecânico, `04` VAN, `05` Utilitário, `06` Outros), `tipo_carroceria` (`00` n/a, `01` Aberta, `02` Fechada/Baú, `03` Granelera, `04` Porta Container, `05` Sider), `uf_veiculo` → `uf`; `renavam` REQ in catalog; `status` `A`=Sim (active), `I`=Não; `status_veiculos` `on`/`off` (tracker connected); `reastreador` [sic] = tracker id; `condutor_principal` → `funcionarios`; `categoria_veiculo` `MOTO`/`CARRO`/`CAMINHAO`; `combustivel_tipo` `GAS`, `ALCOOL`, `GASOLINA`, `DIESEL`, `ELETRICO`, `HIBRIDO` |
| `veiculos_despesas` | vehicle expenses (Despesas com veículos) | L/I/U/D | REQ `id_veiculo`, `tipo` (example `T`), `data`, `descricao` (catalog), `quantidade_litros`, `valor_litro`, `valor`, `kilometragem`; `id_condutor` → `funcionarios`; `gerar_contas_apagar` `S`/`N` (**default S: creates an accounts-payable entry**, `id_apagar`); `status_contas_apagar` `A`=A pagar, `F`=Pago, `P`=Parcial, `C`=Cancelado; `classificacao_infracao` `L`, `M`, `G`, `GR` (traffic fine severity) |
| `veiculos_tracker` | GPS tracker positions (Rastreadores de veículos / Logs de rastreamento) | L/I/U/D | REQ `rastreador` (tracker id, matches `veiculos.reastreador` / `funcionarios.rastreador`), `lastupdate` (`DD/MM/YYYY HH:MM:SS`); `latitude`, `longitude`, `speed`, `gps_time`. Insert is how a tracker integration pushes positions. |

## Actions

All take a small JSON body; none uses `ixcsoft: listar` unless stated. Opaque numeric suffixes (`_25738`, `_29158`)
are IXC form-button ids; they are stable names, not record ids.

### Patrimony and structures
#### `baixar_produto_imobilizado` — return a structure's patrimony item to my warehouse
`POST /baixar_produto_imobilizado`, body `{"get_id": "<id>"}` (the collection labels it "ID do Comodato": the
movement/allocation id of the patrimony, from `su_oss_mov_produto_estrutura`). Effect: write — removes the asset
from the structure (or comodato) and puts it back in the calling user's warehouse ("Patrimônio > Baixar > Meu
almoxarifado"). Stock only; no billing.
#### `baixar_produto_imobilizado_outro_almox` — return a patrimony item to another warehouse
`POST`, body `{"id": "<id da alocação/comodato>", "id_almox": "<receiving warehouse>"}`. Effect: write, stock only.
(n8n also lists an unmapped sibling `baixar_produto_outro_almox` without body.)

### Transfer with confirmation (`requisicao_devolucao_material`)
#### `requisicao_devolucao_material_29200` — helper used at step 1 of the flow
`POST`. The collection names it "1. Retornar os almoxarifados do usuário" (return the user's warehouses) but its
example body is a copy of a `transf_almox_item` body (`id_patrimonio`, `id_produto`, `id_unidade`, `unidade_sigla`,
`qtde`, `fator_conversao`, `id_transf_almox`, `tipo_produto`). Treat its real contract as **uncertain**; to find a
user's warehouses use `almox_usuario` instead (see recipe). Do not call it as a write.
#### `botaoAjax_29158` — send a transfer with confirmation for confirmation
`POST`, body `{"get_id": "<id requisicao_devolucao_material>"}`. Effect: write — status `1` Aberta → `2` Aguardando
Confirmação (inferred from the step name); the destination colaborador sees it to confirm.
#### `botaoAjax_29160` — confirm a transfer with confirmation
`POST`, body `{"get_id": "<id>"}`. Effect: write — status → `3` Confirmada; stock moves to the destination
warehouse. **Must be executed as the destination colaborador** ("é necessário o colaborador de destino"): the API
user must be the IXC user linked to `id_funcionario_destino`, otherwise IXC refuses.
Also in n8n, unmapped: `requisicao_devolucao_material_29115`, `botaoAjax_27931` (resource
`transf_almox_patrimonio_wizard`, a patrimony transfer wizard). No bodies documented.

### Material requests
#### `cancelar_requisicao_material` — cancel a material request
`PUT /cancelar_requisicao_material/<id_requisicao_material>`; the collection sends header `ixcsoft: listar` on it.
Body: `data_cancelamento` (`DD/MM/YYYY`), `id_mot_cancelamento` (→ `transf_mot_cancelamento`), `status` `C`,
`id_usuario_cancelamento` (→ `usuarios`), `tipo_cancelamento` `API` (default value). Effect: write, cancels.

### Purchasing buttons
| Endpoint | Method / body | Effect |
|---|---|---|
| `liberar_requisicao_compra` | `POST {"get_id": "<id requisicao_compra>"}` | write: approves a purchase requisition (`status_liberacao_compra` → `S`, inferred) |
| `requisicao_compra_cancelar` | `PUT /requisicao_compra_cancelar/<id>` `{"descricao_cancelamento": "<motivo>"}` | write: cancels a purchase requisition |
| `liberar_pedido` | `POST {"get_id": "<id pedido_compra>"}` | write: approves a purchase order (`status_liberado` → `S`, inferred) |
| `pedido_compra_cancelar` | `POST {"id": "<id>", "cancelamento_descricao": "<motivo>"}` | write: cancels a purchase order |
| `enviar_pedido_fornecedor` | `POST` (also documented as `GET`) `{"id": "<id pedido_compra>"}` | **external message**: e-mails the purchase order to the supplier. Confirm first. |
| `imprimir_pedido_compra` | `GET {"id": "<id>"}` | read: returns the printable purchase order (file/base64) |

### Sales buttons
#### `validar_finalizar_saida` — validate and finalize a sale
`GET` (with body) `{"id_saida": "<id vd_saida>", "carteira_cobranca": "<id fn_carteira_cobranca>", "nfe": "S|N"}`.
Effect: **write with billing and fiscal impact** — closes the sale (`status` `F`), moves stock if `gera_estoque=S`,
generates receivables (`fn_areceber`, boletos/PIX in the given billing wallet) and, with `nfe=S`, issues the fiscal
document to SEFAZ/city hall (effects inferred from the button name and the `vd_saida` fields; the collection gives
only the body). Hard to undo (requires cancelling the invoice and receivables). Always confirm items,
values, wallet and `nfe` with the user first.
#### `vd_saida_alterar` — reopen a sale
`PUT /vd_saida_alterar/<id_saida>`, body `{"status": "A", "aprova_desconto": "S|N", "previsao": "S|N|"}`
(`A`=Aberto, `F`=Fechado). Effect: write — reopens a finalized sale for editing; does not by itself cancel issued
invoices or receivables (inferred). Confirm first.
#### `faturar_pedido_os` — invoice a sales order created from a service order
`GET` (with body) `{"get_id": "<id pedido_os>"}`. Effect: **write, billing** — turns the O.S. order into a sale
(`vd_saida`) / charge (inferred). Confirm first.
#### Printing
| Endpoint | Body | Returns |
|---|---|---|
| `imprimir_venda` | `POST {"id": "<id vd_saida>"}` | sale receipt/document (file) |
| `imprimir_nota` | `POST {"id": "<id vd_saida>", "base64": "S"}` | the fiscal invoice (DANFE/NFS-e/NF 21-22) as base64 PDF |
| `vd_saida_25738` | `POST {"id": "<id vd_saida>", "base64": "S"}` | the sale printed with the installation's custom template (Imprimir modelo personalizado), base64 |
Read-only, but responses can be large; decode base64 to a file instead of printing it. Sending a document to the
end customer is a separate step and needs confirmation. Unmapped n8n `vd_saida` actions without documented body:
`vd_saida_24205`, `vd_saida_agrupamento`, `vd_saida_comodatos`; NF 21/22 print buttons `botao_rel_25740` /
`botao_rel_19314` (resource `rfn_md21`).

### Stock reports (`rcp_produtos_imprimir_*`)
`GET` with `ixcsoft: listar` and a filter body; **response is base64 (PDF)**, potentially heavy — always filter by
product, warehouse or branch. Details and body fields are in [administration → Reports](administration.md#reports).

## Recipes

### Products held by a technician
1. `POST /usuarios` (listar) `qtype=usuarios.funcionario`, `query=<id funcionarios>`, `oper==` → keep `usuarios.id`.
   (If you only have the name, list `funcionarios` with `funcionarios.funcionario` `L` first.)
2. `POST /almox_usuario` (listar) `qtype=almox_usuario.id_usuario`, `query=<usuarios.id>` → collect `id_almox`
   (`padrao_usuario=S` marks the default one).
3. For each warehouse: `POST /estoque_produtos_almox_filial` (listar) `qtype=estoque_produtos_almox_filial.id_almox`,
   `query=<id_almox>`. Report `produto_descricao` + `saldo`; ignore `saldo` 0 unless asked.
4. Serialized units: `POST /patrimonio` (listar) filtered per the installation's warehouse field (inspect a record
   first) to list individual serials/MACs.

### Products of a contract
1. Read the contract (`cliente_contrato`, see [customers](customers.md)) → `id_vd_contrato` (sales plan).
2. Plan products: `vd_contratos_produtos` `qtype=vd_contratos_produtos.id_vd_contrato`, `query=<id_vd_contrato>`.
3. Contract-specific products: `vd_contratos_produtos` `qtype=vd_contratos_produtos.id_contrato`, `query=<id contrato>`.
4. Or in one call: `view_vd_contratos_produtos_gen` `qtype=view_vd_contratos_produtos_gen.cliente_contrato_id`.

### Immediate transfer between warehouses
1. Confirm source, destination, products, quantities (and serials) with the user.
2. `POST /transf_almox_top` (no listar header) `{id_almox_saida, id_filial, id_almox_entrada, id_filial_entrada, data, obs}` → `id`.
3. Per item: `POST /transf_almox_item` `{id_transf_almox: <id>, id_produto, id_unidade, unidade_sigla, qtde,
   fator_conversao, tipo_produto, id_patrimonio}`. Each insert moves the stock immediately; check `type` on each
   response and stop at the first error.

### Transfer with confirmation (technician → technician), in order
1. Find both sides: `usuarios`/`funcionarios` ids and their warehouses via `almox_usuario` (do not rely on
   `requisicao_devolucao_material_29200`).
2. `POST /requisicao_devolucao_material` `{id_funcionario, id_almox_origem, id_filial_origem, id_funcionario_destino,
   id_almox_destino, id_filial_destino, data: "DD/MM/YYYY", data_confirmacao: "", observacao, status: "1"}` → `id`.
3. Per item: `POST /itens_requisicao_devolucao_material` `{id_requisicao_devolucao_material: <id>, id_produto,
   id_unidade, qtd, fator_conversao, tipo_produto}`; add `id_patrimonio` for serialized items.
4. `POST /botaoAjax_29158 {"get_id": "<id>"}` → status `2` Aguardando Confirmação.
5. `POST /botaoAjax_29160 {"get_id": "<id>"}` **with the destination colaborador's API user** → status `3`
   Confirmada, stock moved. If the agent's credential is not the destination user, stop after step 4 and tell the
   user the receiver must confirm in IXC.
6. Verify: list `requisicao_devolucao_material` by id (status `3`) and the destination balance.

### Is product X in stock?
`produtos` `qtype=produtos.descricao`, `oper=L` → `id`; then `estoque_produtos_almox_filial`
`qtype=estoque_produtos_almox_filial.id_produto`, `query=<id>` → sum `saldo` per warehouse (only `almox_ativo=S`).
Check `estoque_min_max_almox` (`estoque_min_max.id_produto`) to flag items below `qtd_min`.

### Sale with invoice (write, billing — confirm every step)
1. `POST /vd_saida` with the required header fields (status starts `A`) → `id`.
2. `POST /vd_saida_produtos` per item with `id_saida=<id>`.
3. Re-read `vd_saida` and show the total to the user.
4. `GET /validar_finalizar_saida {id_saida, carteira_cobranca, nfe}` → receivables (`ids_areceber`) and, with `nfe=S`,
   the fiscal document.
5. `POST /imprimir_nota {"id": "<id>", "base64": "S"}` → save the PDF; boleto/PIX of the receivables: [financial](financial.md).

### Purchase flow
`requisicao_compra` (+ itens) → `liberar_requisicao_compra` → `pedido_compra` (+ itens) → `liberar_pedido` →
optional `enviar_pedido_fornecedor` (e-mails the supplier) → on delivery `entrada` (+ `movimento_produtos` with
`id_entrada`, `gera_estoque=S`) and `entrada_pedido` to link it to the order.
