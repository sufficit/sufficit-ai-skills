# IXC network / provisioning

Radius logins (PPPoE, Hotspot, IP x MAC, VLAN, IPoE), online status, sessions and traffic, trust unblock, session
disconnect, fiber ONU/OLT and the "authorize ONU" flow, transmitters/POPs, IP pools, speed plans, Radius NAS and
reply attributes, ACS/TR-069, InMap (fiber map, technical viability), the VoIP platform and MVNO mobile lines. Use
this file for any "is the customer's internet up / why is it down / what is their signal" question. Request shapes,
the `ixcsoft: listar` header, `grid_param` and error handling are in [request mechanics](requests.md). Contract
status and blocking live in `cliente_contrato` ([customers](customers.md)); invoices in [financial](financial.md).

Safety rules for this module:
- **Never display passwords or secrets.** `radusuarios.senha`, `senha_router1/2`, `senha_rede_sem_fio*`,
  `senha_wpa2aes`, `radpop_radio.senha`/`senha_anm`, `senha_onu_cliente`, `voip_sippeers.secret`,
  `radauth_nas.secret`, `auth_usuarios.senha`, `linha_mvno.senha` come back in clear text in listings. Drop them
  from anything you show or log. When an update needs the full record (see the PUT warning in
  [request mechanics](requests.md)), pass the stored value back unchanged without echoing it.
- **Actions that change the end customer's service** (marked ⚠ below): disconnect, MAC clear, trust unblock,
  editing `radusuarios`/`radpop_radio_cliente_fibra`, any ONU/OLT button (write, reset, reboot, delete,
  credentials), ACS Wi-Fi push, SIP block/unblock, MVNO line status. Confirm with the user first, state what the
  customer will experience (connection drop, reboot, lost configuration), and never run them in loops or bulk.

## Tables

### `radusuarios` — Radius login / internet access account (Login)
Operations: list / insert / update / delete. One record per access credential; a contract can have several. This is
the source for "is the customer online", IP, MAC, plan and last connection.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | login id | used by `desconectar_clientes`, `radusuarios_25452`, `radusuarios_consumo*.id_login`, `radpop_radio_cliente_fibra.id_login` |
| `login` | PPPoE/Hotspot user name | REQ, max 50; matches `radacct.username` |
| `senha` | login password | **secret, never show**; `senha_md5` S/N = stored as MD5 (default N) |
| `ativo` | login enabled | REQ, `S`=Sim, `N`=Não. `N` blocks authentication entirely |
| `online` | current Radius status | `S`=online, `N`=offline, `SS`=Sem status (never seen / unknown). Updated by IXC from Radius accounting, not real time |
| `id_cliente` | customer | REQ → `cliente` |
| `id_contrato` | contract | → `cliente_contrato` |
| `id_grupo` | speed plan | REQ → `view_radgrupos_vd_contratos_produtos` (i.e. `radgrupos`) |
| `autenticacao` | auth type | REQ, default `L`. `L`=PPPoE, `H`=Hotspot, `M`=IP x MAC, `V`=VLAN, `D`=IPoE, `I`=Integração, `E`=Externa |
| `tipo_conexao_mapa` | access medium | REQ. `58`=5.8 GHz, `24`=2.4 GHz, `F`=Fibra, `L`=Cabo, `A`=ADSL, `LTE`=LTE, `LDD`=Link dedicado |
| `ip` / `pd_ipv6` / `framed_pd_ipv6` | assigned IPv4 / delegated / framed IPv6 | |
| `mac` | MAC learned or bound | cleared by `radusuarios_25452` |
| `ultima_conexao_inicial` / `ultima_conexao_final` | start / end of the last session | `YYYY-MM-DD HH:MM:SS`; `0000-00-00 00:00:00` = never |
| `tempo_conectado`, `tempo_conexao` | connected time counters | seconds (inferred) |
| `motivo_desconexao`, `count_desconexao` | last disconnect reason (Radius terminate cause) / count | |
| `login_simultaneo` | simultaneous sessions allowed | REQ, default 1 |
| `auto_preencher_ip`, `fixar_ip`, `relacionar_ip_ao_login` | IP learning/pinning | REQ, `H`=Configuração padrão, `S`=Sempre, `N`=Nunca. Same codes for `auto_preencher_mac`, `relacionar_mac_ao_login`, `relacionar_concentrador_ao_login` and the `*_ipv6` variants |
| `autenticacao_por_mac` | MAC check | REQ, default `P`. `N`=Não, `S`=Sim, `P`=Padrão, `MK`=Mikrotik, `UN`=UBNT, `WP`=WPA2-AES (Postman comments use `H` for "Não") |
| `tipo_vinculo_plano` | how the plan is bound | REQ, `D`=Padrão, `C`=Contrato, `P`=Pré-pago, `G`=Grátis |
| `franquia_maximo`, `franquia_consumo`, `franquia_consumo_up`, `franquia_atingida` | data cap, usage, cap reached | `franquia_atingida` S/N |
| `download_atual`, `upload_atual` | current rates reported by IXC | |
| `id_concentrador` / `concentrador` / `ip_concentrador` / `interface` | NAS | → `nas` / `mk_interfaces` |
| `pool_radius`, `id_radgrupos_pools`, `id_rad_dns` | pools / DNS | → `radpool`, `radgrupos_pools`, `rad_dns` |
| `vlan`, `vlan_ip_rede`, `service_tag_vlan`, `mtu` | VLAN/IPoE params | required for `V`/`D`/`I`/`E` inserts |
| `id_transmissor`, `interface_transmissao(_fibra)`, `id_caixa_ftth`, `ftth_porta`, `onu_mac`, `id_hardware`, `tipo_equipamento` | physical path | → `radpop_radio`, `radpop_radio_porta(_fibra)`, `rad_caixa_ftth`, `rad_hardware`; `tipo_equipamento` `C`=Comodato, `P`=Próprio |
| `endereco_padrao_cliente` | address source | REQ, `S`=Padrão cliente, `N`=Manual, `C`=Padrão contrato |
| `ssid_router_wifi(_5ghz)` | Wi-Fi SSIDs | passwords in `senha_rede_sem_fio*` are secrets |
| `onu_compartilhada`, `franquia_atingida`, `cliente_tem_a_senha`, `autenticacao_wps`, `autenticacao_mac` | flags | S/N |
| `id_filial` | branch | read-only → `filial` |

Relations: `id_cliente` → `cliente`, `id_contrato` → `cliente_contrato`, `id_grupo` → `radgrupos`, `id_integracao` →
`radintegracao`, `lte_id` → `radacessoslte`, `id_df_projeto` → `df_projeto`, `id_reserva_rede_neutra` →
`reserva_rede_neutra`, `id_condominio` → `cliente_condominio`.

Listing examples:
```json
{"qtype":"radusuarios.id_contrato","query":"<id_contrato>","oper":"=","page":"1","rp":"20","sortname":"radusuarios.id","sortorder":"desc"}
{"qtype":"radusuarios.login","query":"<login>","oper":"=","page":"1","rp":"1"}
{"qtype":"radusuarios.autenticacao","query":"L","oper":"=","page":"1","rp":"20"}
```
Insert minimum (Postman, "todos os campos são obrigatórios"): `autenticacao`, `tipo_conexao_mapa`, `id_cliente`,
`id_contrato`, `id_grupo`, `login`, `senha_md5`, `senha` (not for IPoE/Integração/Externa), `login_simultaneo`,
`ativo`, `auto_preencher_ip`, `fixar_ip`, `relacionar_ip_ao_login`, `autenticacao_por_mac`, `auto_preencher_mac`,
`relacionar_mac_ao_login`, `tipo_vinculo_plano`; Hotspot adds `ip`; IP x MAC adds `ip`, `mac`; VLAN/IPoE/
Integração/Externa add `id_concentrador`, `interface`, `vlan`, `vlan_ip_rede` (Integração also `id_integracao`).
⚠ Insert/update/delete change the customer's ability to authenticate. Changing `id_grupo` changes their speed;
`ativo=N` cuts access.

### `radusuarios_consumo`, `radusuarios_consumo_d`, `radusuarios_consumo_m` — traffic usage (Consumo / Diário / Mensal)
Operations: list / insert / update / delete (insert/update/delete only for data correction; normally written by
IXC). Raw, daily and monthly aggregates per login.

| Field | Meaning | Values / notes |
|---|---|---|
| `id_login` | login | → `radusuarios.id` |
| `data` | period date | insert format `DD/MM/AAAA hh:mm:ss` |
| `consumo` | download | bytes |
| `consumo_upload` | upload | bytes |

Example: `{"qtype":"radusuarios_consumo_m.id_login","query":"<id_login>","oper":"=","page":"1","rp":"12","sortname":"radusuarios_consumo_m.id","sortorder":"desc"}`.

### `radacct` — Radius session history (Conexões Radius)
Operations: list only. One row per accounting session; use for "when did it drop / how long / which IP or MAC".

| Field | Meaning |
|---|---|
| `radacctid` | session row id (sort by this, desc) |
| `username` | login (= `radusuarios.login`) |
| `callingstationid` | customer MAC |
| `framedipaddress` / `framedipv6prefix` / `delegatedipv6prefix` | assigned addresses |
| `nasipaddress` | concentrador (NAS) IP |
| `calledstationid` | service name, e.g. `PPPoE_1` (Hotspot/PPPoE) |
| `acctstarttime` / `acctstoptime` | session start / end (`YYYY-MM-DD HH:MM:SS`; empty stop = still open) |
| `acctsessiontime` | duration, seconds |
| `acctinputoctets` / `acctoutputoctets` | bytes in / out (NAS perspective) |
| `acctterminatecause` | disconnect reason (e.g. `User-Request`, `Lost-Carrier`, `Admin-Reset` — standard Radius values, inferred) |
| `acctsessionid`, `acctuniqueid`, `groupname`, `nasportid`, `acctupdatetime` | technical |

Official example (sessions of one IP on one day):
```json
{"qtype":"radacct.framedipaddress","query":"172.16.0.23","oper":"=","page":"1","rp":"1000",
 "sortname":"radacct.radacctid","sortorder":"desc",
 "grid_param":"[{\"TB\":\"radacct.acctstarttime\",\"OP\":\">=\",\"P\":\"2020-11-13 00:00:00\"},{\"TB\":\"radacct.acctstarttime\",\"OP\":\"<=\",\"P\":\"2020-11-13 23:59:59\"}]"}
```
For a customer, filter by login: `"qtype":"radacct.username","query":"<login>"`, `rp` 10–50, `radacctid desc`.
`radacct` is large; always filter by `username`/IP and a date range.

### `radgrupos` — speed plans (Planos de velocidade)
Operations: list / insert / update / delete. The plan a login uses (`radusuarios.id_grupo`).

| Field | Meaning | Values / notes |
|---|---|---|
| `grupo` | plan name (Radius group) | REQ |
| `tipo` | product type | REQ, `I`=Internet, `T`=Telefonia, `S`=Serviço/Produto |
| `id_produto` | product | REQ → `produtos` |
| `download` / `upload` (+ `_busrt`, `_busrt_th`, `_busrt_time`), `garantia_*`, `prioridade` (1–8) | normal profile | `qos_ativo` S/N (if S, fill download/upload) |
| `red_*` / `id_plano_reduzir` / `horas_reduzido` | reduced profile | `red_ativo` S/N |
| `tur_*` / `id_plano_turbinar` / `horas_turbinado` | boosted profile | `tur_ativo` S/N |
| `alteracao_velocidade` | allow speed change by routine | REQ; wiki `P`=Sim, `C`=Não; Postman uses `S`/`N` |
| `ativo_normal`, `horas_normal` | scheduled return to normal | REQ S/N; hours 0–23 comma separated |
| `franquia_mensal`, `tipo_franquia`, `id_plano_franquia` | data cap | REQ; `tipo_franquia` `M`=Mês atual, `U`=Últimos 30 dias, `P`=Período vencimento do contrato |
| `reduzir_dias_atraso`, `id_plano_atraso` | plan when payment is late | → `radgrupos` |
| `id_pool`, `id_rad_dns`, `address_list(_ipv6)` | pools/DNS/address list | → `radgrupos_pools`, `rad_dns` |
| `sici_tecnologia` | Anatel SICI tech | REQ, `A`=xDSL, `B`=Cable Modem, `C`=Spread Spectrum (Wi-Fi), `D`=FWA, `E`=SeAC, … (full list in wiki) |
| `dici_tipo_conexao_mapa` | DICI medium | same codes as `radusuarios.tipo_conexao_mapa` |
| `tipo_integracao_neutra`, `operador_neutro` | neutral network | `ixcsoft`, `fibrasil` → `operadores_neutros` |
| `type_band_control` | `l2` / `l3` | |

⚠ Editing a plan changes the speed of every login on it.

### `radgrupos_pools` — IP pools (Pool IP)
Operations: list / insert / update / delete. Filter by `radgrupos_pools.tipo`.

| Field | Meaning | Values / notes |
|---|---|---|
| `descricao` | name | REQ |
| `tipo` | pool kind | `RAD`=Radius, `CON`=Concentrador IPv4, `CONV6`=Concentrador IPv6, `DUALSTACK`=Concentrador Dual Stack |
| `nome` | IPv4 pool name on the concentrator | REQ for `CON`/`DUALSTACK` |
| `nomepoolipv6` | IPv6 pool name | REQ for `CONV6`/`DUALSTACK` |
| `id_rad_pool` | Radius pool | REQ for `RAD` → `radpool` |

### `radpop` — POPs / transmission points (POP - Pontos de transmissão)
Operations: list / insert / update / delete. Required on insert: `pop` (name), `id_cidade` → `cidade`.
Other: `id_projeto` → `df_projeto`, address fields, `latitude`/`longitude`, `abertura` (`R`=Repetidor, `PA`=Ponto de
acesso), `tp_estacao` (`P`=Própria, `T`=Terceiro, `N`=Nuvem, `V`=Virtual), `numestacao_anatel`, `id_fornecedor` →
`fornecedor`, `sn_enlace_proprio`/`sn_enlace_contratado`/`sn_enlace_satelite` S/N.

### `radpop_radio` — transmitters: OLTs and radios (Transmissores)
Operations: list / insert / update / delete. The OLT id here is the `id_olt`/`id_transmissor` used everywhere in the
fiber flow.

| Field | Meaning | Values / notes |
|---|---|---|
| `descricao` | name | REQ |
| `fabricante_modelo` | vendor/driver | REQ. `U`=Radio Ubiquiti, `M`=Radio Mikrotik, `I`=Radio Intelbras (disc.), `O`=OLT Overtek Epon, `FH`=OLT Fiberhome (ANM/UNM), `DC`=Datacom, `HW`=Huawei, `ZTE`, `NK`=Nokia, `PK`=Parks, `FK`/`FKG`=Furukawa (disc.), `INB`=Intelbras Gpon, `DIG`=Digistar, `FBT`=Fiberhome (sem ANM/UNM), `FKWGL`=Furukawa Lightdrive, `VSOL`, `RAISE`=Raisecom, `CIAEPON`/`CIAGPON`=Cianet, `ZYXEL`, `UFIBER`=Ubiquiti Ufiber, `FB6001`=Fiberhome AN6001, `FKC`=Furukawa (Conscius), `ZTEC610`, `VSOLGPON`, `PHYHOME`, `INTELBRASG16`, `2FLEX`, `INTELBRASEPON`, `TPLINK`, `SMARTOLT`, `OLTNEUTRA`=Rede Neutra, `TH`=Think. Required fields vary by vendor |
| `id_pop` | POP | REQ → `radpop` |
| `ip`, `login`, `senha`, `porta_ssh`, `porta_telnet`, `httpd_port`, `porta_api`, `timeout` | management access | REQ ip/login/senha; **`senha` secret** |
| `ativo` | enabled | REQ S/N |
| `usa_vpn` | via VPN | REQ, `1`=Sim, `0`=Não (Postman sends `N`) |
| `busca_potencia` | poll ONU power | REQ S/N |
| `perfil_fibra_padrao`, `perfil_neutro_bridge`, `perfil_neutro_router` | default ONU profiles | → `radpop_radio_cliente_fibra_perfil` |
| `conexoes_ultima`, `conexoes_ulltima_data`, `fwversion`, `uptime`, `cpu_load`, `total_memory`, `free_memory`, `temperatura`, `voltagem`, `modelo` | monitoring snapshot | read |
| `id_prov_snmp`, `id_padrao_cores`, `id_servidor_unms`, `id_pv_grupo_backup`, `operador_neutro` | relations | → `prov_snmp`, `df_padrao_cores`, `integracoes_redes`, `pv_grupo_backup`, `operadores_neutros` |

### `radpop_radio_cliente_fibra` — fiber customer / ONU (Cliente Fibra)
Operations: list / insert / update / delete. One row per ONU. All ONU buttons take this record's `id`.

| Field | Meaning | Values / notes |
|---|---|---|
| `id` | ONU record id | body `id` of every ONU button |
| `nome` | ONU name | REQ |
| `id_transmissor` | OLT | REQ → `radpop_radio` |
| `id_contrato` | contract | → `cliente_contrato` (main lookup key) |
| `id_login` | login | → `radusuarios` |
| `mac` | ONU serial / MAC (GPON SN on most vendors) | |
| `sinal_rx` / `sinal_tx` | optical power received / transmitted, dBm | `data_sinal` = when read; refresh with `botao_rel_22991` |
| `temperatura`, `voltagem`, `distancia_onu` | ONU telemetry | |
| `causa_ultima_queda` | last drop cause reported by the OLT (e.g. dying-gasp / LOS, vendor text) | there is no separate `status` field; use this, `data_sinal` and `radusuarios.online` |
| `id_perfil` | ONU profile | → `radpop_radio_cliente_fibra_perfil` |
| `ponid`, `slotno`, `ponno`, `onu_numero`, `gemport`, `service_port`, `vlan`, `vlan_pppoe`/`_dhcp`/`_tr69`/`_iptv`/`_voip`/`_outros` | OLT position and service VLANs | |
| `tipo_operacao` | `B`=Bridge, `R`=Router (PPPoE) | |
| `tipo_autenticacao`, `onu_tipo`, `versao`, `senorid` | provisioning details | |
| `id_caixa_ftth`, `porta_ftth`, `id_projeto` | splitter box / port / map project | → `rad_caixa_ftth`, `df_projeto` |
| `id_radpop_radio_porta` | PON interface | read-only → `radpop_radio_porta_fibra` |
| `ip_gerencia`, `login_onu_cliente`, `senha_onu_cliente`, `porta_telnet_onu_cliente`, `porta_web_onu_cliente`, `perfil_onu_cliente`, `script_onu_cliente` | ONU management | **`senha_onu_cliente` secret** |
| `radpop_estrutura` | own infrastructure (not a customer) | REQ, S/N |
| `onu_rede_neutra` | neutral network ONU | read-only S/N |
| `id_hardware`, `id_ramal` | → `rad_hardware`, `voip_sippeers` | |
| address fields, `latitude`/`longitude`, `id_condominio` | location | |

Customer check (used in production): `{"qtype":"radpop_radio_cliente_fibra.id_contrato","query":"<id_contrato>","oper":"=","page":"1","rp":"5","sortname":"radpop_radio_cliente_fibra.id","sortorder":"desc"}`
→ take `registros[0]` (newest ONU). ⚠ Insert/update/delete change the OLT inventory; most changes only reach the OLT
when a "Gravar" button is pressed, but treat every edit as service-affecting.

### `radpop_radio_cliente_fibra_perfil` — ONU provisioning profiles (Perfis cliente fibra)
Operations: list / insert / update / delete. All fields REQ: `fabricante_modelo` (OLT driver codes, same family as
`radpop_radio.fabricante_modelo`, e.g. `SMARTOLT`, `HW`, `ZTE`, `FH`), `nome`, `comando` (script template with
placeholders like `#pon_id#`). The `id` becomes `radpop_radio_cliente_fibra.id_perfil`.

### `fh_onu_nao_autorizadas` — ONUs seen by the OLT but not authorized (ONU não autorizada)
Operations: list. Fields: `Chassi`, `slotno`, `ponno`, `mac` (serial), `dt` (seen at), `id_pop`, `id_olt` →
`radpop_radio`. List per OLT with only `grid_param`:
```json
{"grid_param":"[{\"TB\":\"id_olt\",\"OP\":\"=\",\"P\":\"<id_olt>\"}]"}
```
(the generic `qtype: fh_onu_nao_autorizadas.id` listing also works).

### Other network tables
| Table | Purpose (UI label) | Ops | Key fields / notes |
|---|---|---|---|
| `radpop_olt_slot` | OLT slots (Interface slot) | L/I/U/D | REQ `id_transmissor` → `radpop_radio`, `numero_slot`, `portas`; `descricao` |
| `radpop_radio_porta_fibra` | PON interfaces (Interface Fibra) | L/I/U/D | REQ `id_pop_radio` (OLT), `id_slot`, `numero_pon`; `interface`, `fabricante`, `potencia_pon`, `potencia_limite`, `vlan_*`. Official listing uses `qtype: radpop_radio_porta.id` (table alias quirk) |
| `radpop_radio_cliente` | radio (wireless) customers (Cliente rádio) | L/I/U/D | REQ `id_pop_radio` → `radpop_radio`, `id_pop_radio_porta` → `radpop_radio_porta`, `mac`; `id_radusuarios` → `radusuarios`; telemetry `sinal`, `ccq`, `tx`, `rx`, `noise`, `signal_to_noise`, `distance`, `uptime`, `lastip`, `airmax_*` |
| `radpop_radio_cliente_fibra_historico` | ONU power history (Histórico de potenciação) | L/D | filter by ONU id (field name not in sources; inspect a row), sort `id desc` |
| `radpop_ocorrencias` | transmitter incidents/solutions (Ocorrências/Soluções) | L/I/U/D | REQ `transmissor` (Postman: → `radpop_radio`; wiki: → `radpop`), `data` `DD/MM/AAAA`, `problema`; `solucao` |
| `radauth_nas` | authorized concentrators / Radius clients (Concentradores autorizados) | L/I/U/D | `shortname` (description), `nasname` (IP), `secret` (**secret**), `ports` (default 1814), `type`, `server`, `community`, `description`. ⚠ wrong values break authentication for every customer on that NAS |
| `auth_usuarios` | equipment access users (Usuários auth) | L/I/U/D | `descricao`, `login`, `senha` (**secret**), `opcao` `ssh`/`winbox`, `grupo_usuarios` `full`/`read`/`write` |
| `radgroupreply` | Radius reply attributes per group (Resposta de grupo) | L/I/U/D | REQ `groupname`, `attribute`, `op` (default `=`), `value`; `prio`, `id_plano` → `radgrupos` (read-only) |
| `radusergroup` | plan x login mapping (Planos x Logins) | L/D | `id_usuario` → `radusuarios`, `username`, `groupname`, `priority` (default 1). Maintained by IXC; don't edit |
| `rad_hardware` | equipment models | L | `tipo` `R`=Rádio, `F`=Fibra, `hardware`, `ativo` S/N |
| `acs_device_grid` | ACS / TR-069 devices (Dispositivos acs) | L | listing uses `qtype: acs_device.id`; device id is the input of `botaoAjax_30774` |

### InMap (fiber map) — `df_*`, `rad_caixa_ftth`, `elemento_arquivos`
| Table | Purpose (UI label) | Ops | Key fields / notes |
|---|---|---|---|
| `df_projeto` | map project (Projetos) | L/I/U/D | REQ `nome`, `latitude`, `longitude`, `zoom` (16), `status` `A`=Ativo/`I`=Inativo; `id_filial`, `cor_mapa` |
| `df_elemento` | map elements; filter `df_elemento.tipo` | L/I/U/D | `tipo`: `CA`=Caixa de emenda, `CS`=Caixa subterrânea, `CB`=Cabo, `PT`=Poste, `AR`=Região de cobertura, `RN`=Região de rede neutra (the Postman insert example for RN sends `AR`; use `RN`). REQ `id_projeto` → `df_projeto`, `id_tipo_elemento` → `df_tipo_elemento`, `descricao`, `observacao`, `preco_unidade`; optional `latitude`/`longitude`, `codigo_identificador` (box style, CA), `comprimento` + `ativo` (CB), `total_caixas` + `ativo` (RN) |
| `df_tipo_elemento` | element types | L | id for `id_tipo_elemento` |
| `df_elemento_coordenada` | element coordinates (paths of cables/regions) | L | filter by element |
| `rad_caixa_ftth` | service boxes / splitters, CTO (Caixas de atendimento) | L/I/U/D | REQ `descricao`, `id_projeto`, `id_transmissor` → `radpop_radio`, `codigo_estilo_caixa` (color code: `7eTTWpDR` Azul, `1Pr4jX4X` Verde, `8PbLzK3P` Amarela, `9S83YSCh` Branca, `5T4gmUHG` Vermelha, `752EWQuj` Laranja, `3HHYsgRp` Cinza, `50r7nh0u` Preta (padrão), `ASydas32` Roxa, `a8sFy8ff` Rosa, `AssUd3h7` Marrom, `AhsuSS1u` Azul claro, `LIgAKPfY` Azul escuro, `YveVV4Ka` Lilás, `H63QbvyX` Limão, `w5bHIgOc` Verde escuro); `tipo` `P`=Própria/`N`=Neutra/`A`=Ambas, `id_interface` → `radpop_radio_porta_fibra`, `id_tecnologia` → `rad_caixa_ftth_tecnologia`, `capacidade`, `status` `A`/`I`, address, `id_cidade` |
| `elemento_arquivos` | images attached to boxes/elements | L/I/D | insert is **multipart form-data**: `descricao`, `local_arquivo` (file), `id_elemento`, `tabela` |

### VoIP platform
| Table | Purpose (UI label) | Ops | Key fields / notes |
|---|---|---|---|
| `voip_sippeers` | customer SIP lines / extensions (Ramal SIP - Clientes) | L/I/U/D | REQ `id_contrato` → `cliente_contrato`, `id_integracao` (VoIP integration id in IXC), `ativo` S/N, `use_area_code` S/N, `tipo_linha_sip` `N`=Normal, `P`=Portabilidade entrada, `S`=Portabilidade saída; `name` (extension), `secret` (**secret**), `callerid` (binagem), `tarifa` → `tarifas_grupos`, `id_plano_sip` → `planos_voip`, `id_perfis_voip` → `perfis_voip`, `calllimit`; registration snapshot `fullcontact`, `ipaddr`, `port`, `regseconds`, `useragent`. Hidden fields `tipo_linha_sip`, `recharge_settings` (`N`), `dia_fechamento` (`0`) must be sent or the insert returns "Erro ao processar". Platform-specific fields per integration: Flux (`id_subscriber_integration`, `id_sip`), Magnus Billing (`plano_magnus`, `accountcode`), SaperX (`saperx_*`: `saperx_tipo` 1=Pré-pago/0=Pós-pago, `sapex_plano_tipo` scm/stfc/customroute, LC/LDN/LDI/VC1-3 flags 1/0), Zeus (`plano_zeus`, `grupo_plano_zeus`, `tech_prefix_zeus` 1111/2222/5555/7777/0, `bloquear_ligacoes_*_zeus` S/N), Summit (`summit_bid_type` TERMINAL/TRUNK, `plano_summit`, `categoria_summit`), Sippulse (`sippulse_*`, `ddd`, `ddi`), VSC (`vsc_*`, `billing` C/D/L). ⚠ insert/edit provisions on the external platform and affects billing |
| `planos_voip` | VoIP plans | L/I/U/D | REQ `descricao`, `id_plataforma` |
| `tarifas_grupos` | call rate plans (Plano de tarifas) | L/I/U/D | REQ `nome`, `id_produto_ligacoes` → `produtos`; `ddd`, `ddi`, `dt_ini_vigencia`/`dt_fin_vigencia` `DD/MM/AAAA`, franchise `id_produto_franquia`, `franquia_valor`, `franquia_tempo_segundos`, `id_tarifa_franquia` → `tarifas`. ⚠ money |
| `cdr` | call detail records (Registros de chamadas) | L/I/U/D | `id_sip` (line), `clid` (extension), `calldate` `YYYY-MM-DD hh:mm:ss`, `src`, `dst` (dialed), `destino` (normalized), `duration` (total s), `billsec` (billed s), `id_tarifa`, `tp_chamada`, `custo` (buy), `valor_user` (sell), `tarifado` S/N, `lastapp` (`Dial`/`Hangup`/`Set`), `disposition` (`ANSWERED` — Postman shows `ANSWERE` —, `BUSY`, `NO ANSWER`, `FAILED`), `importado` S/N, `id_fatura`, `recordingfile`, `did`, `uniqueid`. Read only in practice; edits change billing |
| `visualizar_range_numeros` | registered number ranges (Range) | L | listing of number blocks (`range_terminais_lista`) |

### MVNO (mobile)
| Table | Purpose (UI label) | Ops | Key fields / notes |
|---|---|---|---|
| `linha_mvno` | mobile lines (Assinantes) | L/I/U/D | REQ `id_integracao` → `configuracao_mvno` (MVNA: TGN, TIP, Telecall, Americanet, EAI, Surf, Contel, brazmovel, playmovel, tatelecom, Bora, Unifique), `id_contrato` → `cliente_contrato`, `esim` S/N, `portabilidade` S/N, `api` (`A`=Na API e no IXC, `I`=Apenas no IXC); `id_prod_ixc_mvno` → `produtos_ixc_mvno`, `simcard` (ICCID), `ddd_telefone`, `numero_telefone`, `msisdn`, `status_linha` (`A`=Ativo, `BR`=Bloqueio roubo, `BP`=Bloqueio perda, `BA`=Bloqueio parcial, `I`=Inativo, `BI`=Bloqueio uso indevido, `BT`=Bloqueio total, `C`=Cancelada, `AA`=Aguardando ativação), `status_portabilidade` (`A`=Aguardando, `R`=Recusado, `CO`=Concluído, `CA`=Cancelado), `tipo_numero` (1=Normal, 2=Gold, 3=DID Móvel, 4=M2M, 5=M2M Especial, 6=Teste, 7=QA), `dia_recorrencia`, `link_esim`, `operadora_origem` → `operadoras_linha_mvno`, `login`/`senha` (**secret**). ⚠ with `api=A` inserts/edits are pushed to the carrier: activating, blocking or cancelling a real phone line |
| `produtos_ixc_mvno` | IXC product ↔ MVNO plan mapping | L/I/U/D | REQ `id_plano_integracao` (→ `planos_mvno`), `id_produto_ixc` → `produtos`, `tipo_referencia` (`C`=Contrato, `A`=Assinatura; Postman also shows `S`/`N`), `ativo` S/N; `id_integracao` → `configuracao_mvno` (when C), `id_assinatura_integracao` (when A) |
| `configuracao_mvno` | MVNO integration config | — | holds carrier credentials (`token`, `client_secret`); never read for display |

## Actions

All actions: no `ixcsoft` header, JSON body, response `{"type":"success"|"error","message":"…"}` (check `type`;
HTTP 200 on errors). Some buttons return script text or HTML in `message` (inferred for "Visualizar script").

### `desconectar_clientes` — disconnect a login's current session (Desconectar Login) ⚠
`POST /desconectar_clientes`, body `{"id": "<radusuarios.id>"}`. Same as UI Provedor → Logins → Editar →
Desconectar. IXC sends a Radius disconnect/CoA to the concentrator; the customer's connection drops and the router
re-authenticates (normally back in seconds if the login and contract are OK). Effect: write, network access.
- Which id: the official collection and IXC's n8n node attach this action to resource `radusuarios` with field `id`,
  which in IXC buttons is the record id, so send **`radusuarios.id`**. A Sufficit customer flow sends the login
  text (`registros[0].login`) instead; that is unverified. Prefer the numeric id; if it returns `type: error`, report
  the message rather than retrying blindly with the other form, and only try the login text if the user accepts.
- Use it after changing plan/IP/MAC so the new settings apply, or to force a reconnect. Never in bulk.

### `radusuarios_25452` — clear the login's bound MAC (Limpar MAC) ⚠
`POST /radusuarios_25452`, official body `{"get_id": "<radusuarios.id>"}` (n8n node also uses `get_id`). A
Sufficit flow sends `{"id": …}`; if that returns error, use `get_id`. Effect: write; clears `radusuarios.mac` so the
next device to connect is learned (needed after a router/ONU swap when `relacionar_mac_ao_login` pins the MAC).
Usually followed by `desconectar_clientes`.

### Other `radusuarios` buttons
`atualiza_wifi` (likely pushes Wi-Fi SSID/password to the CPE, inferred) and `botao_rel_24730` (a report) exist in
IXC's n8n node with no body documented. Do not call without a confirmed body.

### `desbloqueio_confianca` — trust unblock of a contract (Desbloqueio confiança) ⚠
Official form: `POST /desbloqueio_confianca`, body `{"id": "<id_contrato>"}` (Postman comment: "ID do Contrato").
Same as Contrato → Status de Acesso → Desbloqueio confiança. Releases a contract blocked for late payment for a
period without payment ("in trust"). Effect: write, network access (restores the end customer's internet) and
collections policy.
- Sufficit flows also sent it as `PUT /desbloqueio_confianca` with the body and as `PUT /desbloqueio_confianca/<id>`
  with `{"id": <id_contrato>}`; prefer the documented POST.
- IXC enforces per-contract rules configured in the installation (how many days, how often): `cliente_contrato.desbloqueio_confianca`
  (`S`=Habilitado, `N`=Desabilitado, `P`=Padrão), `desbloqueio_confianca_ativo` (S/N, currently in a trust unblock),
  `restricao_auto_desbloqueio` (S/N) with `motivo_restricao_auto_desbloq`, `dt_ult_des_bloq_conf` (last use). A refusal
  comes back as `type: error` with the reason (limit reached, not allowed); relay it, never loop.
- Afterwards read the contract (`status_internet` should leave `CA`/`CM`/`FA`) and the login (`online`). If the
  customer stays offline, `desconectar_clientes` forces re-authentication.

### Fiber ONU buttons (all bodies use the `radpop_radio_cliente_fibra.id`)
| Endpoint | UI button | Body | Effect / risk |
|---|---|---|---|
| `botao_gravar_dispositivo_22408` | Integração OLT → Gravar no dispositivo | `{"id": "<id_cliente_fibra>"}` | ⚠ writes the ONU config (profile, VLANs, service-port) to the **OLT**; completes authorization |
| `radpop_radio_cliente_fibra_22407` | Integração OLT → Visualizar Script | `{"id": …}` | read; returns the OLT script that would be applied |
| `botao_excluir_dispositivo_22434` | Integração OLT → Excluir dispositivo | `{"id": …}` | ⚠ destructive: removes the ONU from the OLT; customer loses service until re-authorized |
| `radpop_radio_cliente_fibra_24700` | Integração ONU → Gravar na ONU | `{"id": …}` | ⚠ writes configuration into the ONU itself (WAN/Wi-Fi), may restart services |
| `radpop_radio_cliente_fibra_22952` | Integração ONU → Alterar credenciais do dispositivo | `{"id": …}` | ⚠ changes the ONU management credentials |
| `radpop_radio_cliente_fibra_24699` | Integração ONU → Resetar ONU | `{"id": …}` | ⚠ destructive: factory reset; customer offline until re-provisioned |
| `radpop_radio_cliente_fibra_24701` | Integração ONU → Visualizar script ONU | `{"id": …}` | read |
| `radpop_radio_cliente_fibra_26379` | Integração ONU → Reboot ONU | `{"id": …}` | ⚠ reboots the ONU (a few minutes offline) |
| `radpop_radio_cliente_fibra_28120` | Integração ONU → Libera acesso web | `{"id": …}` | ⚠ enables remote web access to the ONU |
| `botao_rel_22991` | Potência / Resumo ONU | `{"id": …}` | read on the OLT; returns current power/summary and refreshes `sinal_rx`/`sinal_tx`/`data_sinal` (inferred). Safe diagnostic |
| `sincronizar_olt_22397` | Sincronizar ONU | `{"transmissor": "<id_olt>"}` | write (inventory): syncs the OLT's ONU list into IXC; heavy on big OLTs |
| `radpop_radio_cliente_fibra_28571`, `radpop_radio_cliente_fibra_29661` | unmapped | unknown | do not call |

### `fh_onu_nao_autorizadas_22396` — authorize a pending ONU (Autorizar ONU) ⚠
`POST /fh_onu_nao_autorizadas_22396`, body `{"get_id": "<fh_onu_nao_autorizadas.id>"}`. Creates the fiber customer
record for that ONU (the `id_cliente_fibra` used in the next steps). Effect: write. `autorizar_onu` and
`select_id_olt` also appear in IXC's n8n node as unmapped helpers; use the documented `_22396` flow.

### `botaoAjax_30774` — push Wi-Fi data to the device via ACS (Enviar dados acs wifi) ⚠
`POST /botaoAjax_30774`, body `{"id": "<id>"}` (ACS device id from `acs_device_grid`, inferred). Sends SSID/password
to the CPE over TR-069; Wi-Fi clients disconnect and must reconnect.

### `viabilidade_tecnica` — technical viability (Viabilidade técnica)
`POST /viabilidade_tecnica`. Two forms: by address `{"endereco","numero","bairro","cidade","estado" (REQ, UF
sigla),"cep"}` or by point `{"latitude": "-16.302805", "longitude": "-39.024840"}` (both REQ). Read. Requires the
InMap module and the "Autoviabilidade" feature enabled; otherwise returns an error. Use for "do you serve my
address?" pre-sales.

### `consultar_regiao_manutencao` — is a point inside a maintenance region (Consultar Região de Manutenção)
`POST /consultar_regiao_manutencao`, body `{"latitude": "…", "longitude": "…"}` (both REQ). Read. Use to tell a
customer that an outage is a known maintenance in their area.

### `bloquear_desbloquear_sip` — block / unblock a SIP line ⚠
`POST /bloquear_desbloquear_sip`, body `{"get_id": "<voip_sippeers.id>"}`. Toggles the line state (read the line
first to know which way it goes). Affects the customer's phone service. `chamada_ura` and
`retornar_funcionario_ramal` exist on `voip_sippeers` in the n8n node, unmapped; do not call.

### `rfn_bloqueio_cliente_comodatos_21558` — contracts report with loaned equipment (Relatórios contratos, Comodatos)
`POST /rfn_bloqueio_cliente_comodatos_21558` with `ixcsoft: listar` and the report filter object (`contrato`,
`status`, `tipo_conexao_mapa`, `desbloqueio_confianca_ativo`, `status_comodato`, date ranges…; `T` = todos). Read,
heavy; narrow filters.

## Recipes

1. **Is the customer's internet up?** `cliente` by CPF → `cliente_contrato` by `id_cliente` (check `status_internet`:
   `A` ok, `CM`/`CA` blocked, `FA` overdue) → `radusuarios` by `id_contrato` (`ativo`, `online`, `ip`,
   `ultima_conexao_inicial/final`, `motivo_desconexao`) → if fiber, `radpop_radio_cliente_fibra` by `id_contrato`,
   `sort id desc`, take `registros[0]` and read `sinal_rx` (typical GPON healthy range about -8 to -27 dBm,
   inferred) and `causa_ultima_queda`; optionally `botao_rel_22991` for a fresh reading.
2. **Recent drops**: `radacct` with `qtype radacct.username = <login>`, `grid_param` on `acctstarttime >= <date>`,
   `sortname radacct.radacctid desc`, `rp 20`; report start/stop, `acctsessiontime`, `acctterminatecause`.
3. **Router swapped, customer can't connect** ⚠: confirm with user → `POST radusuarios_25452 {"get_id":"<id>"}` →
   `POST desconectar_clientes {"id":"<id>"}` → re-read `radusuarios` after ~1 min for `online=S` and the new `mac`.
4. **Blocked for late payment, customer promises to pay** ⚠: confirm with the user (this restores access before
   payment) → `POST desbloqueio_confianca {"id":"<id_contrato>"}` → on `success` re-read contract and login; on
   `error` relay the reason (limit/permission). See [financial](financial.md) for the boleto/PIX to send.
5. **Authorize a new ONU** (official order) ⚠:
   1. `radpop_radio` list → pick the OLT `id` (`id_transmissor`).
   2. `radpop_radio_cliente_fibra_perfil` list → pick the profile `id` (`id_perfil`).
   3. `fh_onu_nao_autorizadas` with `grid_param` `id_olt = <OLT id>` → find the ONU by `mac` (serial) → its `id`.
   4. `POST fh_onu_nao_autorizadas_22396 {"get_id":"<pending id>"}` → note the created fiber customer id.
   5. Read that `radpop_radio_cliente_fibra` record, set `id_perfil`, `id_transmissor`, plus `id_contrato`,
      `id_login`, `nome`, VLANs as needed, and `PUT /radpop_radio_cliente_fibra/<id>` with the full object.
   6. Optional: `radpop_radio_cliente_fibra_22407` to preview the script.
   7. `POST botao_gravar_dispositivo_22408 {"id":"<id_cliente_fibra>"}` to write to the OLT; then `botao_rel_22991`
      to confirm signal.
6. **Monthly usage**: `radusuarios_consumo_m` by `id_login`, sort `id desc`, `rp 12`; convert bytes to GB.
7. **Coverage check before sale**: `POST viabilidade_tecnica` with `estado` + `cep` (or lat/long) → if error mentions
   the module, the installation lacks InMap/Autoviabilidade; fall back to `df_elemento` `tipo=AR` regions only if the
   user wants a manual check.
8. **Outage near a customer**: `consultar_regiao_manutencao` with the login's or contract's `latitude`/`longitude`.
