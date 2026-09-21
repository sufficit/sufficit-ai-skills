# Chamadas do WhatsApp por SIP para números de clientes

Cenário: uma plataforma que só atende **chamadas** (SIP no seu PABX) de números WhatsApp de
clientes que mantêm a mensageria com outro provedor. Tudo abaixo foi confirmado em produção.

## Checklist (todos ao mesmo tempo)

1. App em modo **Live**, com `whatsapp_business_management` e `whatsapp_business_messaging`
   em acesso avançado.
2. Integração de **Provedor de Tecnologia** concluída no caso de uso WhatsApp
   (senão o cliente vê "<app> não pode integrar clientes no momento").
3. Config de Login para Empresas: variação **Geral**, **token de usuário**, permissões
   `business_management`, `whatsapp_business_management`, `whatsapp_business_messaging`.
   A variação "Cadastro incorporado" serve para **cadastrar número novo**; número que já está com
   outro provedor aparece "Não qualificado".
4. **O cliente compartilha a WABA com o business dono do app** (Configurações do negócio →
   Contas do WhatsApp → Parceiros → Atribuir parceiro). O login do cliente, sozinho, dá só
   permissão de usuário: a Meta marca o app como `BLOCKED` para SIP e **não envia o INVITE**
   (quem liga vê "chamando", o PABX não vê nada).
5. Servidor SIP gravado no número **com o token do próprio app**
   (`POST /{phone_id}/settings` → `calling.sip.servers`). Os servidores SIP são por app.
6. Servidor com TLS (certificado válido), firewall liberando as faixas da Meta e destino que toca.

A verificação do negócio do cliente (erro `141010`, `LIMITED`) **não** impediu as chamadas.

## Diagnóstico

- `GET /{phone_id}?fields=health_status` → entidade `APP`, campo **`can_receive_call_sip`**
  (não `can_send_message`).
  - `141011` no APP → falta o item 4 (ou a permissão de mensagens).
  - `138025` → falta o item 5 para este app.
- **A saúde atrasa**: depois do item 4 a chamada já funcionava e a saúde ainda mostrava `BLOCKED`.
  Confirme com ligação real.
- Compare com um cliente que funciona: `client_whatsapp_business_accounts` do seu business,
  `GET /{waba}/subscribed_apps` e a saúde do número dele.
- Asterisk: `pjsip set logger pcap /tmp/x.pcap` grava o SIP decifrado sem console; o filtro
  `pjsip set logger host <faixa>` não filtra em algumas versões (grava tudo — desligue logo).

## Separar chamadas de mensagens

Se for preciso inscrever o app na WABA do cliente, deixe o webhook de WABA do app **sem campos**
(`DELETE /{app}/subscriptions?object=whatsapp_business_account&fields=messages,calls`):
a inscrição fica só como autorização e nenhuma mensagem do cliente chega até você.

## Login no navegador

- Chrome com FedCM transforma `FB.login` em `dialog_source=fedcm&scope=openid` e perde o
  `config_id` → "app não disponível". Abra o diálogo OAuth
  (`/dialog/oauth?client_id&config_id&response_type=code&override_default_response_type=true&redirect_uri&state`)
  numa janela própria e receba o código numa página de retorno do mesmo domínio.
- Domínios do SDK JS e URIs de redirecionamento são **por app** e só editáveis pela UI.
- "App não disponível" logo depois de publicar costuma ser propagação: teste com conta sem papel no app.
