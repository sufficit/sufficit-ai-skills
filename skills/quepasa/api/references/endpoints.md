# Referência de rotas do QuePasa

Fonte: especificação Swagger do QuePasa versão `5.26.0922.1322` (55 caminhos) e
as rotas canônicas v5 conferidas no código-fonte e no gateway em produção
(versão `5.26.0929.1644`). Os valores entre `<…>` são exemplos; nenhum token,
chave ou número real aparece aqui.

## Convenções

- Base: `$QUEPASA_URL`. Duas superfícies coexistem:
  - **v5 canônica**: `$QUEPASA_URL/api/v5/...` — preferida.
  - **legada (v4)**: `$QUEPASA_URL/api/...`, `$QUEPASA_URL/api/v4/...` e
    também na raiz (`$QUEPASA_URL/...`). É a que o Swagger descreve.
- Autenticação por sessão: cabeçalho `X-QUEPASA-TOKEN` (na v5 também aceito como
  `?token=` ou `"token"` no corpo — prefira sempre o cabeçalho, para o token não
  ir parar em log de URL).
- Chave de usuário: `X-QUEPASA-USERKEY`, só para rotas de conta/sessões
  (`/api/v5/sessions`). Vê várias sessões; ver alertas no SKILL.md.
- Na v5, parâmetros comuns são aceitos por cabeçalho, query ou corpo:

| Parâmetro | Cabeçalho | Query | Corpo |
| --- | --- | --- | --- |
| token | `X-QUEPASA-TOKEN` | `token` | `token` |
| grupo | `X-QUEPASA-GROUPID` | `groupid`, `groupId`, `group_jid` | `groupid`, `groupId`, `group_jid` |
| mensagem | `X-QUEPASA-MESSAGEID` | `messageid`, `id` | `messageid`, `messageId`, `id` |
| chat | `X-QUEPASA-CHATID` | `chatid`, `chatId` | `chatid`, `chatId` |

- Resposta padrão: `{"success": bool, "status": "texto", ...}`. `success:false`
  é falha mesmo com HTTP 200.

## Superfície v5 (canônica)

### Sistema (público, sem token)

| Método | Rota | Uso |
| --- | --- | --- |
| `GET` | `/api/v5/system/version` | versão em execução |
| `GET` | `/api/v5/health` | saúde |

### Mensagens

| Método | Rota | Uso |
| --- | --- | --- |
| `POST` | `/api/v5/messages` | enviar (`chatid`, `text`, `trackid`, `inreply`, `url`, `content`, `fileName`, `poll`, `location`, `contact`, `sticker`, `link`) |
| `GET` | `/api/v5/messages` | histórico em cache; filtros `messageid`, `chatid`, `type`, `category`, `search`, `fromme`, `fromhistory`, `trackid`, `timestamp`, `page`, `limit` (padrão 50, máx. 500) |
| `POST` | `/api/v5/messages/get` | uma mensagem por `messageid` |
| `PATCH` | `/api/v5/messages` | editar texto (`messageid`, `text`) |
| `DELETE` | `/api/v5/messages` | revogar (`messageid`) |
| `POST` | `/api/v5/messages/retry` | redisparar a mensagem para webhooks/filas |
| `POST` / `DELETE` | `/api/v5/messages/react` | reagir / remover reação (`chatid`, `messageid`, `emoji`, `fromme`) |
| `POST` | `/api/v5/messages/links` | cartão de link clicável (`chatid`, `url`, `text`, `title`, `description`) |
| `POST` | `/api/v5/messages/actions` | botões experimentais (1 a 3); WhatsApp Web mostra só aviso |
| `POST` | `/api/v5/messages/lid/direct` | texto direto para um `…@lid` (teste) |

### Grupos

| Método | Rota | Corpo / parâmetros |
| --- | --- | --- |
| `GET` | `/api/v5/groups` | lista os grupos da sessão |
| `POST` | `/api/v5/groups` | criar: `{"title": "…", "participants": ["<jid>"]}` |
| `POST` | `/api/v5/groups/get` | detalhes; `groupid` |
| `POST` | `/api/v5/groups/leave` | sair; `groupid` |
| `PUT` | `/api/v5/groups/name` | `{"group_jid": "…", "name": "…"}` |
| `PUT` | `/api/v5/groups/description` | `{"group_jid": "…", "topic": "…"}` |
| `PUT` | `/api/v5/groups/photo` | `{"group_jid": "…", "image_url": "…"}` ou `{"remove_img": true}` |
| `PUT` | `/api/v5/groups/permissions` | `groupid` + `{"members_can_send_messages": bool, "members_can_edit_group_settings": bool}` (omitido = inalterado) |
| `PUT` | `/api/v5/groups/participants` | `{"group_jid": "…", "action": "add"\|"remove"\|"promote"\|"demote", "participants": ["<jid>"]}` |
| `GET` | `/api/v5/groups/requests` | pedidos de entrada pendentes; `groupid` |
| `POST` | `/api/v5/groups/requests` | `{"group_jid": "…", "action": "approve"\|"reject", "participants": ["<jid>"]}` |
| `GET` / `POST` | `/api/v5/groups/invite` | link de convite atual → `url` |
| `DELETE` | `/api/v5/groups/invite` | revoga o link e devolve um novo |

Não existem na v5: `/api/v5/groups/getall`, `/api/v5/groups/create` (404) e
`GET /api/v5/groups/get` (405, é `POST`). Esses nomes são da superfície legada.

### Mídia

| Método | Rota | Uso |
| --- | --- | --- |
| `GET` | `/api/v5/media/messages?messageid=<id>` | binário da mídia (inclui vCard `text/x-vcard` de contato compartilhado) |
| `POST` | `/api/v5/media/messages/get` | idem com `messageid` no corpo |
| `GET` | `/api/v5/media/pictures/info?chatid=<jid>` | foto de perfil/grupo |

`/api/v5/download` não existe (404); o legado é `/api/download?messageid=…`.

### Chats e contatos

| Método | Rota | Uso |
| --- | --- | --- |
| `GET` | `/api/v5/chats` | conversas da sessão |
| `POST` | `/api/v5/chats/read`, `/api/v5/chats/unread` | marcar como lida/não lida (`chatid`) |
| `POST` | `/api/v5/chats/archive` | `{"chatid": "…", "archive": bool}` |
| `POST` | `/api/v5/chats/presence` | "digitando"/"gravando" (`chatid`, `type`, `duration`) |
| `GET` | `/api/v5/contacts` | contatos |
| `GET` | `/api/v5/contacts/identifier?phone=…` ou `?lid=…` | converter telefone ↔ LID |
| `POST` | `/api/v5/contacts/search` | `{"query": "…", "phone": "…"}` |
| `POST` | `/api/v5/contacts/get` | informações de usuário |
| `POST` | `/api/v5/contacts/availability` | quais números têm WhatsApp |
| `POST` / `DELETE` | `/api/v5/contacts/block` | bloquear / desbloquear (`wid`) |
| `POST` | `/api/v5/contacts/save` | salvar contato |

### Despachos (webhooks e filas)

| Método | Rota | Uso |
| --- | --- | --- |
| `GET` / `POST` / `DELETE` | `/api/v5/dispatches/webhooks` | webhooks da sessão |
| `GET` / `POST` / `DELETE` | `/api/v5/dispatches/rabbitmq` | filas RabbitMQ |

A forma usada em produção para webhook é a legada `POST /webhook` com o token
da sessão (corpo `url`, `forwardinternal`, `trackid`, `extra`). Não existe
`/api/v5/webhooks` nem `/api/v5/webhook`.

### Sessões (cuidado: afetam o número)

| Método | Rota | Uso |
| --- | --- | --- |
| `GET` | `/api/v5/sessions` | lista sessões visíveis à chave de usuário — **inclui tokens** |
| `POST` | `/api/v5/sessions/get` | uma sessão (token) |
| `PUT` | `/api/v5/session/name`, `/api/v5/session/photo` | perfil do número |
| `POST` | `/api/v5/session/restart`, `/enable`, `/disable`, `/pair`; `GET` `/qrcode`, `/paircode` | ciclo de vida — só com pedido explícito |
| `PATCH` / `DELETE` | `/api/v5/sessions` | alterar / apagar sessão — só com pedido explícito |

## Superfície legada (Swagger 5.26.0922.1322)

Rotas relativas a `$QUEPASA_URL` (também valem com `/api` e `/api/v4` na
frente). `*` = obrigatório. Todas usam `X-QUEPASA-TOKEN`, exceto onde indicado.
Exceções de prefixo: as linhas `/v5/...` só existem sob `/api` (ou seja,
`/api/v5/...`) e `/api/settings/...` já traz o prefixo. `/health` aceita
`X-QUEPASA-USER`/`X-QUEPASA-PASSWORD` opcionais; `/api/settings/runtime-limits`
é administrativa.

### Ambiente

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/environment` | Get environment settings | — |

### Aplicação

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `POST` | `/account` | Manage user accounts | corpo: `password`, `username` |
| `POST` | `/spam` | Send spam messages | corpo: `chatId`, `text` |

### Bot

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/command` | Execute bot commands | query `action`* |

### Chat

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `POST` | `/chat/archive` | Archive or unarchive chat | corpo: `archive`, `chatid` |
| `GET` | `/chat/lists` | Manage WhatsApp lists on one conversation | query `chatid`*; corpo: `chatid`, `listid` |
| `POST` | `/chat/lists` | Manage WhatsApp lists on one conversation | query `chatid`*; corpo: `chatid`, `listid` |
| `DELETE` | `/chat/lists` | Manage WhatsApp lists on one conversation | query `chatid`*; corpo: `chatid`, `listid` |
| `POST` | `/chat/markread` | Mark chat as read | corpo: `chatid` |
| `POST` | `/chat/markunread` | Mark chat as unread | corpo: `chatid` |
| `POST` | `/chat/presence` | Control chat presence | corpo: `chatid`, `duration`, `type` |
| `GET` | `/lists` | Manage WhatsApp lists | corpo: `color`, `id`, `listid`, `name` |
| `PUT` | `/lists` | Manage WhatsApp lists | corpo: `color`, `id`, `listid`, `name` |
| `POST` | `/lists` | Manage WhatsApp lists | corpo: `color`, `id`, `listid`, `name` |
| `DELETE` | `/lists` | Manage WhatsApp lists | corpo: `color`, `id`, `listid`, `name` |

### Conexão

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/paircode` | Generate pairing code | query `phone`*; query `historysyncdays` |
| `GET` | `/scan` | Generate QR code | — |

### Configurações

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/api/settings/runtime-limits` | Read global runtime limits | — |
| `PUT` | `/api/settings/runtime-limits` | Replace global runtime limits | corpo: `overrides` |
| `DELETE` | `/api/settings/runtime-limits` | Restore inherited runtime limits | — |

### Contatos

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `POST` | `/contact/save` | Save contact | corpo: `firstname`, `fullname`, `phone`, `synctophone` |
| `POST` | `/contact/search` | Search contacts | corpo: `has_lid`, `has_title`, `phone`, `query` |
| `GET` | `/contacts` | Get contacts | — |
| `POST` | `/contacts/block` | Block contact | corpo: `wid` |
| `DELETE` | `/contacts/block` | Unblock contact | corpo: `wid` |
| `POST` | `/isonwhatsapp` | Check WhatsApp registration | corpo: `phones` |
| `GET` | `/useridentifier` | Get user identifier (LID) | query `phone`; query `lid` |
| `POST` | `/userinfo` | Get user information | corpo: `jids` |

### Envio

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `POST` | `/messages/lid/direct` | Send text directly to @lid | corpo: `chatid`, `inreply`, `text`, `trackid` |
| `POST` | `/send` | Send any type of message (text, streamed file, poll, base64 content, location, contact, sticker, link) | corpo: `chatId`, `contact`, `content`, `fileName`, `link`, `location`, `poll`, `sticker`, `text`, `url` |
| `POST` | `/senddocument` | Send document with forced document type | corpo: `chatId`, `content`, `fileName`, `text`, `url` |
| `POST` | `/v5/messages/actions` | Send an experimental WhatsApp action message | corpo: `actions`, `chatid`, `footer`, `id`, `text`, `title`, `trackid` |
| `POST` | `/v5/messages/links` | Send a cross-client clickable link card | corpo: `chatid`, `description`, `id`, `text`, `title`, `trackid`, `url` |

### Grupos

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `POST` | `/groups/create` | Create a new group | corpo: `participants`, `title` |
| `PUT` | `/groups/description` | Set group topic | corpo: `group_jid`, `topic` |
| `GET` | `/groups/get` | Get group information | query `groupId`* |
| `GET` | `/groups/getall` | Get all groups | — |
| `GET` | `/groups/invite` | Get group invite link | query `groupId`* |
| `DELETE` | `/groups/invite` | Revoke group invite link | query `groupId`* |
| `POST` | `/groups/leave` | Leave group | corpo: `chatId` |
| `PUT` | `/groups/name` | Set group name | corpo: `group_jid`, `name` |
| `PUT` | `/groups/participants` | Update group participants | corpo: `action`, `group_jid`, `participants` |
| `PUT` | `/groups/photo` | Set/Remove group photo | corpo: `group_jid`, `remove_img` |
| `GET` | `/groups/requests` | Handle group join requests | corpo: `action`, `group_jid`, `participants`; query `group_jid` |
| `POST` | `/groups/requests` | Handle group join requests | corpo: `action`, `group_jid`, `participants`; query `group_jid` |
| `GET` | `/invite` | Generate group invite link | query `chatid` |
| `GET` | `/invite/{chatid}` | Generate group invite link | path `chatid`; query `chatid` |
| `PUT` | `/v5/groups/permissions` | Update group permissions | header `X-QUEPASA-TOKEN`*; header `X-QUEPASA-GROUPID`*; corpo: `members_can_edit_group_settings`, `members_can_send_messages` |

### Mensagem

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `PUT` | `/edit` | Edit message | corpo: `content`, `messageId` |
| `GET` | `/message/{messageid}` | Get message | path `messageid`* |
| `DELETE` | `/message/{messageid}` | Revoke message | path `messageid`* |
| `POST` | `/messages/react` | Send message reaction | corpo: `chatid`, `emoji`, `fromme`, `messageid` |
| `DELETE` | `/messages/react` | Remove message reaction | corpo: `chatid`, `emoji`, `fromme`, `messageid` |
| `POST` | `/read` | Mark messages as read | corpo: JSON |
| `GET` | `/receive` | Receive messages | query `timestamp`; query `exceptions`; query `type`; query `category`; query `search`; query `fromme`; query `fromhistory`; query `chatid`; query `messageid`; query `trackid`; query `page`; query `limit` |
| `POST` | `/redispatch/{messageid}` | Re-dispatch message | path `messageid`* |

### Mídia

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/download` | Download media | query `messageid`; query `cache` |

### RabbitMQ

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/rabbitmq` | Manage RabbitMQ configurations | corpo: `connection_string`, `exchange`, `routing_key`; query `connection_string` |
| `POST` | `/rabbitmq` | Manage RabbitMQ configurations | corpo: `connection_string`, `exchange`, `routing_key`; query `connection_string` |
| `DELETE` | `/rabbitmq` | Manage RabbitMQ configurations | corpo: `connection_string`, `exchange`, `routing_key`; query `connection_string` |

### Restauração

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/restore` | Diagnose orphan WhatsApp sessions | — |
| `POST` | `/restore/auto` | Automatically restore one unambiguous orphan session | — |
| `POST` | `/restore/manual` | Manually restore one session link | corpo: `jid`, `token` |

### Saúde

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/health` | Health check with optional authentication | header `X-QUEPASA-USER`; header `X-QUEPASA-PASSWORD` |

### Sessão

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `PUT` | `/session/name` | Set session profile name | corpo: `name`, `token` |
| `PUT` | `/session/photo` | Set/Remove session profile photo | corpo: `content`, `image_url`, `remove_img`, `token` |

### Sessão (info)

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/info` | Get bot information | — |
| `POST` | `/info` | Create bot configuration | corpo: `broadcasts`, `calls`, `contextid`, `deliveryreceipts`, `devel`, `direct`, `groups`, `messages`, `presence`, `readreceipts`, `readupdate`, `sip_register_enabled`, `sip_register_password` |
| `DELETE` | `/info` | Delete bot information | — |
| `PATCH` | `/info` | Update bot information | corpo: `settings` |

### Status

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `POST` | `/status/publish` | Publish WhatsApp status | corpo: `attachment`, `text` |

### Webhooks

| Método | Rota | Resumo | Parâmetros |
| --- | --- | --- | --- |
| `GET` | `/webhook` | Manage webhook configurations | corpo: `bearer_token`, `failure_bearer_token`, `failure_method`, `failure_url`, `method`, `url` |
| `POST` | `/webhook` | Manage webhook configurations | corpo: `bearer_token`, `failure_bearer_token`, `failure_method`, `failure_url`, `method`, `url` |
| `DELETE` | `/webhook` | Manage webhook configurations | corpo: `bearer_token`, `failure_bearer_token`, `failure_method`, `failure_url`, `method`, `url` |
