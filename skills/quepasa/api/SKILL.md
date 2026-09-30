---
name: quepasa-api
description: Usa a API HTTP do QuePasa (gateway WhatsApp em Go) do jeito certo — enviar texto e mídia, administrar grupos (criar, participantes, nome, descrição, convites e pedidos de entrada), baixar mídia e contatos compartilhados, consultar histórico e configurar/interpretar webhooks — com o token da sessão (X-QUEPASA-TOKEN) e nunca a chave de usuário fora do seu escopo. Use quando o pedido envolver QuePasa, WhatsApp via gateway, grupos de WhatsApp, webhooks de mensagem ou integração Hermes/Chatwoot com QuePasa.
metadata:
  version: "0.1.0"
---

# QuePasa API

O QuePasa expõe uma sessão de WhatsApp (um número) por token. Esta skill ensina
as rotas que funcionam em produção, a autenticação correta e as armadilhas já
vividas. A referência completa das rotas está em
[references/endpoints.md](references/endpoints.md) e o formato do webhook em
[references/webhook-payload.md](references/webhook-payload.md).

## Endereço e credenciais

- `QUEPASA_URL` é a URL base do gateway (sem barra final). Nunca invente outra;
  use a configurada no ambiente do agente.
- `GET $QUEPASA_URL/api/v5/system/version` e `GET /api/v5/health` são públicos:
  use-os para confirmar que o gateway responde e qual versão está no ar.
- **Token da sessão** — cabeçalho `X-QUEPASA-TOKEN: <token>`. Identifica um
  número. É a credencial padrão para tudo: enviar, grupos, mídia, webhook.
- **Chave de usuário** — cabeçalho `X-QUEPASA-USERKEY: <chave>`. Enxerga
  **várias sessões** (de vários números/clientes) e `GET /api/v5/sessions`
  devolve inclusive os tokens delas. É poderosa: use-a apenas para a finalidade
  e a sessão para a qual foi entregue, nunca para ler, enviar ou alterar outras
  sessões, e nunca para "descobrir" o token de outra pessoa.
- Nunca mostre token ou chave em resposta, log, comando ecoado, arquivo,
  issue ou mensagem. Ao citar, mascare (`abcd…`). Não cole a lista de sessões
  crua na conversa.

## Regras de leitura das respostas

- Toda resposta tem `success` (bool) e `status` (texto). **`success: false` é
  falha mesmo com HTTP 200** — leia `status` e reporte o motivo real.
- 401 = token ausente/inválido para a rota; 404 = rota inexistente (confira o
  prefixo); 405 = método errado (ex.: `GET /api/v5/groups/get`, que é `POST`).
- Envio bem-sucedido traz `message.id`: guarde-o para responder (`inreply`),
  reagir, editar ou revogar.

## Identificadores (JID)

- Pessoa: `<dígitos com DDI>@s.whatsapp.net` (ex.: `5511999999999@s.whatsapp.net`).
- Grupo: `<id>@g.us`.
- LID (identificador opaco novo do WhatsApp): `<número>@lid`. Converta com
  `GET /api/v5/contacts/identifier?phone=…` ou `?lid=…` quando precisar.

## Enviar mensagem

`POST $QUEPASA_URL/api/v5/messages` com `X-QUEPASA-TOKEN`:

```json
{ "chatid": "<jid>", "text": "Olá!", "trackid": "meu-sistema", "inreply": "<id opcional>" }
```

- `chatid` é o grupo (`…@g.us`) ou a pessoa (`…@s.whatsapp.net`).
- `trackid` identifica o sistema que enviou; o webhook devolve esse valor e
  permite ignorar o próprio eco (evita loop de bot).
- Arquivo: mesmo endpoint com `url` (o servidor baixa) ou `content`
  (`data:<mime>;base64,…`) e `fileName`; ver campos `poll`, `location`,
  `contact`, `sticker`, `link` na referência.
- Confirme `success: true` antes de dizer ao usuário que foi enviado.

## Administrar grupos

Todas com `X-QUEPASA-TOKEN`; a sessão precisa ser admin do grupo para alterar.
O grupo vai em `?groupid=<jid@g.us>` e/ou no corpo como `group_jid`.

| Ação | Rota v5 |
| --- | --- |
| Listar grupos da sessão | `GET /api/v5/groups` |
| Criar | `POST /api/v5/groups` `{"title":"…","participants":["<jid>",…]}` |
| Detalhes | `POST /api/v5/groups/get?groupid=…` |
| Participantes | `PUT /api/v5/groups/participants` `{"group_jid":"…","action":"add\|remove\|promote\|demote","participants":[…]}` |
| Nome | `PUT /api/v5/groups/name` `{"group_jid":"…","name":"…"}` |
| Descrição | `PUT /api/v5/groups/description` `{"group_jid":"…","topic":"…"}` |
| Foto | `PUT /api/v5/groups/photo` `{"group_jid":"…","image_url":"…"}` ou `"remove_img":true` |
| Permissões | `PUT /api/v5/groups/permissions?groupid=…` `{"members_can_send_messages":bool,"members_can_edit_group_settings":bool}` |
| Link de convite | `GET /api/v5/groups/invite?groupid=…` → `url` |
| Revogar link | `DELETE /api/v5/groups/invite?groupid=…` (devolve o novo) |
| Pedidos de entrada | `GET /api/v5/groups/requests?groupid=…`; aprovar/recusar com `POST` `{"group_jid":"…","action":"approve\|reject","participants":[…]}` |
| Sair | `POST /api/v5/groups/leave?groupid=…` |

A superfície antiga (sem `v5`) continua ativa e usa outros nomes:
`GET /api/groups/getall`, `GET /api/groups/get?groupId=…`,
`POST /api/groups/create`. **Não misture**: `/api/v5/groups/getall` e
`/api/v5/groups/create` não existem (404).

### Convidar pessoas

Adicionar direto (`action: add`) pode falhar por privacidade do contato. O
padrão preferido é mandar o link de convite **no privado de cada pessoa**:

1. `GET /api/v5/groups/invite?groupid=<grupo>` → `url`.
2. Para cada pessoa, `POST /api/v5/messages` com `chatid` = `<dígitos>@s.whatsapp.net`
   e um texto curto com o link.
3. Se o grupo exigir aprovação, acompanhe `GET /api/v5/groups/requests` e
   aprove só quem foi convidado.

Nunca publique o link em grupo alheio ou canal público; revogue-o se vazar.

## Mídia, contatos compartilhados e histórico

- Baixar mídia de uma mensagem: `GET /api/v5/media/messages?messageid=<id>`
  devolve o binário com o `Content-Type` original. A rota antiga
  `/api/v5/download` **não existe** (404).
- Contato compartilhado (`type: "contact"`): o texto do webhook traz só o nome
  exibido; o vCard completo (`text/x-vcard`, com o telefone) vem pela mesma rota
  de mídia.
- Consultar mensagem/histórico: `GET /api/v5/messages?messageid=<id>` (aceita
  também `chatid`, `type`, `fromme`, `search`, `page`, `limit`); uma mensagem
  exata: `POST /api/v5/messages/get?messageid=<id>`.

## Webhooks

- Configure com o **token da sessão**: `POST $QUEPASA_URL/webhook` (legado,
  sem prefixo) com `{"url":"https://…","forwardinternal":false,"trackid":"…"}`;
  `GET /webhook` lista e `DELETE /webhook` remove. Não existe
  `/api/v5/webhooks`; o equivalente v5 é `/api/v5/dispatches/webhooks`.
- Campos úteis do payload: `id`, `chat.id`, `text`, `type`, `fromme`,
  `frominternal`, `fromhistory`, `timestamp`, `participant`, `attachment`,
  `wid`. Detalhes e tipos em
  [references/webhook-payload.md](references/webhook-payload.md).
- `wid` é o número da própria sessão (ex.: `<dígitos>:48@s.whatsapp.net`). Em
  grupo, uma menção `@<dígitos do wid>` no `text` é alguém falando com o bot.
- Ignore `fromme: true`/`frominternal: true` ao decidir responder, para não
  conversar consigo mesmo.

## Armadilhas (vividas em produção)

- **Reiniciar o serviço QuePasa derruba todas as sessões** por alguns instantes
  (todos os números, de todos os clientes). Nunca reinicie para "testar"; se for
  inevitável, é decisão humana em janela combinada.
- **Nunca teste com cópia de uma sessão real**: dois clientes com a mesma
  sessão fazem o WhatsApp derrubar o legítimo (`stream_replaced`). Use uma
  sessão de teste própria.
- `success: false` com HTTP 200 é erro — nunca relate sucesso sem
  `success: true`.
- Rota v5 com nome legado (`getall`, `create`, `download`) → 404; confira a
  tabela antes de tentar variações às cegas.
- Não crie, apague, pareie (`/session/pair`, QR code) nem desabilite sessões sem
  pedido explícito: isso afeta o número de produção de alguém.
- Não use a chave de usuário para contornar um 401 do token da sessão.
