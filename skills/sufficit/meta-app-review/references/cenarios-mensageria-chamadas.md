# Cenários: mensageria + chamadas × só chamadas

Uma plataforma pode usar o mesmo app Meta para dois produtos:

1. **Atendimento completo** (mensagens do WhatsApp + ligações): o app recebe as mensagens por
   webhook e as ligações por SIP (ou pela API de chamadas).
2. **Só voz**: o app só entrega as ligações por SIP para um PABX. Aqui há dois tipos de cliente:
   - **2a — mensageria com outro fornecedor**: a WABA continua com o provedor de mensagens dele;
     você só atende as chamadas e **não pode** receber as mensagens.
   - **2b — só voz**: o cliente não usa mensageria em lugar nenhum.

## Por cenário

| | 1. Mensagens + chamadas | 2a. Só voz, mensagens em concorrente | 2b. Só voz |
|---|---|---|---|
| Config de login (ver abaixo) | cadastro incorporado | Geral + token de usuário | cadastro incorporado (novo) ou Geral (existente) |
| WABA compartilhada com o business do app | automático no cadastro incorporado | **o cliente atribui você como parceiro** | automático (novo) / manual (existente) |
| Webhook de mensagens | ligado, apontando para a plataforma | **desligado** | desligado |
| SIP no número, gravado com o token do app | sim | sim | sim |

No 2a, sem o compartilhamento de parceiro a Meta marca o app como `BLOCKED` para SIP
(`141011`) e não entrega a ligação — ver [chamadas por SIP](whatsapp-calling-sip.md).

No 2b o número ainda precisa estar na Cloud API (`CONNECTED`, nome aprovado, registrado com
`POST /{phone_id}/register`). Mensagens que chegarem nesse número ficam sem destino; combine isso
com o cliente.

## Uma config de login por cenário

Crie uma configuração de Facebook Login for Business por cenário, mesmo que duas fiquem iguais
para a Meta — dá para rastrear quem entrou por onde e mudar um cenário sem afetar o outro:

| Cenário | Variação | Token | Ativos / produto |
|---|---|---|---|
| 1. Mensagens + chamadas | Cadastro incorporado do WhatsApp | usuário do sistema, expiração **Nunca** | Contas do WhatsApp; produto só **WhatsApp Cloud API** |
| 2a. Só voz, mensagens em concorrente | Geral | **usuário** (age em nome do cliente) | nenhum; permissões `business_management`, `whatsapp_business_management`, `whatsapp_business_messaging` |
| 2b. Só voz | Cadastro incorporado do WhatsApp | usuário do sistema, expiração **Nunca** | Contas do WhatsApp; produto só **WhatsApp Cloud API** |

Armadilhas ao criar no painel (Login do Facebook para Empresas → Configurações → Criar):

- marcar "WhatsApp Cloud API" pode marcar junto "API de Mensagens de Marketing" — desmarque;
- a expiração padrão do token é 60 dias; escolha **Nunca** para não precisar reautorizar;
- o cadastro incorporado mostra números já ativos em outro provedor como "Não qualificado" — para
  eles use a config Geral (2a) e o compartilhamento de parceiro;
- a edição de uma config existente para no passo de produtos; para ver o resto, crie outra.

## Webhook é do app, não do cliente

Os campos de webhook de WABA (`messages`, `calls`) valem para **todas** as WABAs em que o app está
inscrito.

**Um app só funciona** quando todo cliente do cenário 1 é cliente de mensageria da própria
plataforma (não usa outro sistema) — receber as mensagens dele é o objetivo. A única regra é para
o **2a**: antes de ligar `messages` no app, cada WABA de cliente com mensageria em concorrente
precisa estar

1. **desinscrita** do app (`DELETE /{waba}/subscribed_apps`) — para SIP o que libera a chamada é o
   compartilhamento de parceiro; confirme com uma ligação que a inscrição não é necessária; **ou**
2. inscrita com `override_callback_uri` apontando para um receptor que só confirma e descarta.

Sem isso, as mensagens de um cliente cuja mensageria é de um concorrente chegam à sua plataforma.

**Padrão mais seguro (adotado na Sufficit):** o callback **padrão** do app aponta para um receptor
que só responde a verificação e descarta (200 sem ler o corpo), e cada WABA de cliente de
mensageria recebe `override_callback_uri` para a plataforma. Assim, qualquer WABA inscrita sem
override — cliente só de voz, cliente 2a novo, conta de teste — nunca entrega mensagens a ninguém.
Para gravar override o usuário do sistema do token precisa ter papel no app (ver
[armadilhas](armadilhas.md), `#200`).
Registre no onboarding de voz se o cliente é 2a ou 2b.

Se não der para garantir essa regra, use dois apps no mesmo business (um só de voz, sem campos
de webhook de WABA); cada um precisa das próprias aprovações, domínios do SDK e configs.
