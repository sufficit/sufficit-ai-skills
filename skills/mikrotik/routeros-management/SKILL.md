---
name: routeros-management
description: Administra MikroTik RouterOS v7 e CHR com CLI, SSH e REST; diagnostica interfaces, IP, DHCP, DNS, roteamento, firewall, NAT, VPN, Wi-Fi, serviços, scripts, backup e atualizações, com mudança controlada e validação. Use quando o usuário mencionar MikroTik, RouterOS, WinBox, CHR, /ip, /interface ou /system.
---

# Operação MikroTik RouterOS v7

Escopo: RouterOS **7.x**; antes de aplicar sintaxe, confirme versão, arquitetura, pacotes e recursos disponíveis (`/system/resource/print`, `/system/package/print`, `/system/device-mode/print`). RouterOS v6 tem menus e comportamentos diferentes: não execute receitas v7 às cegas. Este documento ensina operação; **não fornece conexão, credenciais ou autorização** para administrar dispositivo algum.

## Contrato de operação

1. Identifique dispositivo, ambiente, interface de administração, acesso fora de banda, janela e objetivo. Leia o estado primeiro; não assuma nomes de interfaces, WAN/LAN, endereços ou fábrica padrão. Não execute em equipamento de terceiros sem autorização.
2. Proponha mudança mínima com inventário do estado anterior, comandos exatos, impacto, dependências, verificação e reversão. Peça confirmação explícita para alterar roteadores de produção, principalmente acesso, firewall, rotas, VPN, reset, upgrade ou reboot; não trate leitura como consentimento para escrita.
3. Antes de mudanças de conectividade: preserve sessão alternativa/OOB, exporte configuração **sem `show-sensitive`**, faça backup binário criptografado com senha armazenada fora do chat quando viável, e estabeleça recuperação testável. Export texto não inclui todas as credenciais/chaves/certificados; backup binário é específico do dispositivo e versão. Não copie artefatos sensíveis para logs ou repositórios.
4. Na CLI interativa WinBox/SSH use Safe Mode (Ctrl+X ou F4), altere em passos pequenos e teste o acesso antes de sair com Ctrl+X para confirmar. Ctrl+D desfaz. Safe Mode **não é transação universal**: a sessão precisa continuar viva, outras sessões podem interferir e o histórico tem limite; REST/API e scripts não herdam automaticamente o Safe Mode de uma sessão. Para automação remota, prefira alteração em fases, watchdog/rollback independente testado e acesso OOB. Nunca assuma que `/undo` desfaz todo tipo de operação.
5. Confira estado observado contra objetivo, sem revelar segredos. Se houve perda de conectividade, **pare** e use o plano de recuperação; não dispare comandos repetidos. Registre o que foi alterado e o que não foi verificado.

## CLI não é Linux

SSH abre a CLI do RouterOS, **não bash**: não use `ls`, `apt`, `iptables`, `systemctl`, redirecionamento ou pipes. Caminhos como `/ip/address/print`, `/interface/print`, `/system/resource/print` são menus/comandos; scripts `.rsc` têm sintaxe própria. Exemplos de leitura:

```routeros
/system/identity/print
/system/resource/print
/interface/print detail
/ip/address/print detail
/ip/route/print detail
/ip/firewall/filter/print detail
/ip/firewall/nat/print detail
/log/print where topics~"error"
```

`print` mostra números de linha **temporários**: não os use em scripts. `[find ...]` pode retornar zero ou vários IDs; confirme cardinalidade antes de `set/remove`. Use seletores exatos de `name`/`comment` e identifique a propriedade real; IDs `*HEX` podem mudar. Não faça `remove [find]`, `remove [find dynamic=no]` ou limpeza por regex ampla. Marque apenas objetos que a automação possui e reconcilie um por vez. Reexecute scripts apenas depois de confirmar idempotência. Para sintaxe desconhecida, consulte ajuda `?` no menu, versão e [referência oficial](https://manual.mikrotik.com/docs/CLI%20Reference/); não invente propriedades.

## Acesso e interfaces de gestão

Prefira SSH com chave ou HTTPS com certificado validado, usuário de menor privilégio e firewall/listas de endereços de gestão; segmente gestão por VLAN/VPN. REST é exposto pelo serviço `www-ssl` (ou `www` sem TLS, não recomendado), em `/rest/` no RouterOS v7; não confunda REST com a **API binária** (`api`/`api-ssl`, portas usualmente 8728/8729). Restrinja `/ip/service`, `/tool/mac-server`, WinBox e neighbor discovery à rede de gestão. Não habilite `www`, API sem TLS ou login com senha vazia para facilitar automação; não use `curl -k`, tokens em argumentos de shell ou export `show-sensitive` em logs. Faça inventário de regras atuais antes de restringir serviços.

REST: `GET /rest/ip/address` lista; `PUT /rest/ip/address` **cria**, `PATCH /rest/ip/address/*ID` atualiza, `DELETE` remove; `POST /rest/<menu>/print` consulta com argumentos/proplist e `POST /rest/<menu>/<command>` executa comandos. `.id` é o identificador interno, não número de linha. Comandos de ação (`reboot`, `reset-configuration`, etc.) não são GET; trate POST como potencialmente mutante. Use cliente HTTPS com verificação de certificado, segredo fora de URL/log, timeout e registro redigido. REST não é transacional: compare antes/depois e execute rollback explícito se necessário.

## Mapa de operação (inspecione antes de configurar)

| Área | Inventário inicial | Cuidados e verificação |
| --- | --- | --- |
| Links/VLAN/bridge/Wi-Fi | `/interface/print detail`, `/interface/bridge/print`, `/interface/bridge/port/print`, `/interface/vlan/print`, menus `wifi`/`wireless` existentes | VLAN filtering, PVID e bridge CPU podem derrubar gestão; Wi-Fi depende de hardware, pacotes e versão. Teste SSID/autenticação e caminho de gestão. |
| IPv4/IPv6, DHCP, DNS | `/ip/address/print`, `/ipv6/address/print`, `/ip/dhcp-server/print`, `/ip/dhcp-client/print`, `/ip/dns/print` | Verifique pools, leases, gateway, RA/DHCPv6 e resolução de clientes; não abra recursão DNS para Internet. |
| Rotas e protocolos | `/ip/route/print detail`, `/routing/table/print`, menus `/routing` disponíveis | Confirme tabela/VRF, next-hop, distância, políticas, BGP/OSPF e rota de retorno da gestão; teste failover de ponta a ponta. |
| Firewall/NAT | `/ip/firewall/filter/print detail`, `/ip/firewall/nat/print detail`, `/ipv6/firewall/filter/print detail` | Regras em ordem; `input` protege roteador, `forward` trânsito; IPv6 tem firewall separado. Preserve established/related e exceção de gestão antes do drop. NAT depende de conntrack; teste ambos os sentidos. |
| VPN/túneis | `/interface/wireguard/print`, `/ip/ipsec/peer/print`, `/ppp/active/print` conforme pacotes | Confirme peers, Allowed Address, rotas, MTU, DNS, firewall e handshake; nunca exponha chave privada, PSK ou credenciais. |
| Contas/serviços/certificados | `/user/print`, `/ip/service/print`, `/certificate/print` | Menor privilégio, TLS válido, origem restrita, rotação coordenada; não remova único acesso administrativo. |
| Observabilidade | `/log/print`, `/tool/ping`, `/tool/traceroute`, `/interface/monitor-traffic`, `/tool/torch` | Cuidado com tráfego sensível e captura; monitoração pode consumir recursos. Compare baseline e erro antes/depois. |
| Backup/upgrade | `/system/package/print`, `/system/routerboard/print`, `/file/print` | Planeje versão, arquitetura, espaço, compatibilidade, reboot, rollback e acesso físico; não atualize firmware/RouterBOOT automaticamente. |
| Scripts/automação | `/system/script/print detail`, `/system/scheduler/print detail` | Scripting não é shell; políticas/permissões importam. Não execute snippets não auditados, imports ou downloads remotos. |

## Firewall: sequência e escopo

Regras filter são avaliadas de cima para baixo; exceções devem vir antes do drop. `action=log` e ações de address-list podem continuar avaliação. `fasttrack-connection` pode contornar mangle/filas: avalie policy routing e QoS antes de ativar. Para port forwarding, verifique `dstnat` **e** permissão de `forward`, IP do destino, retorno e hairpin se aplicável; publicar serviço aumenta superfície de ataque. Nunca substitua conjunto de regras por template genérico nem misture `/ip/firewall` com `/ipv6/firewall`. Use comentários exclusivos da sua automação e confira a posição de cada regra antes e depois.

## Plano de mudança reutilizável

```text
Alvo e autorização: identidade, versão, ambiente, proprietário, janela
Estado atual: saídas relevantes (redigidas), rota de gestão, acesso alternativo
Objetivo e riscos: interfaces/endereços/fluxos impactados
Pré-condições: versão/pacotes, backup/export, OOB, rollback testado
Mudança: comandos específicos, em passos menores, com seletores únicos
Verificação: estado, conexão existente + conexão nova, clientes e monitoramento
Reversão: comandos para o estado anterior, gatilho, responsável e prazo
Resultado: aplicado/parcial/não aplicado, evidências sem segredos
```

## Fontes e proveniência técnica

Adaptado e ampliado de [tikoci/routeros-skills (MIT, revisão fixa)](https://github.com/tikoci/routeros-skills/tree/c9802a8713927a6851f5540efe93b95f2b0637b8), especialmente `routeros-fundamentals`, `routeros-firewall` e `routeros-scripting`; atribuição e licença acompanham este pacote. Consulte sempre a documentação vigente da MikroTik para versão e menu reais: [manual](https://manual.mikrotik.com/docs/introduction/), [Configuration Management/Safe Mode](https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management), [REST API](https://help.mikrotik.com/docs/spaces/ROS/pages/47579162/REST+API), [Firewall](https://help.mikrotik.com/docs/display/ROS/Filter). As páginas antigas `help.mikrotik.com` estão congeladas; priorize o manual novo quando houver divergência.
