# Armadilhas, com sintoma e causa

## webhook-app-de-outro-business
`POST /{waba|page}/subscribed_apps` com token de um app de **outro** business devolve
`{"success":true}`, o app aparece em `subscribed_apps`, dá até para gravar
`override_callback_uri` — **e nenhum evento é entregue**. Só o app do business dono do ativo
(ou com o ativo compartilhado como cliente) recebe.
Diagnóstico: `GET /{asset}/subscribed_apps` **com o token de página/WABA do app que você quer
conferir**; com token de outro app a resposta só mostra a inscrição dele mesmo.

## verificação de rede não é o problema (quase nunca)
Antes de culpar MTU/firewall: os GET de verificação da Meta são pequenos e passam; POST de
evento é maior. Prove com `POST` de 4 KB de fora e `tcpdump` filtrando as faixas da Meta
(`2a03:2880::/32`, `31.13/16`, `157.240/16`). Se não há conexão de entrada, o problema é do lado deles.

## Login for Business x scope clássico
App tipo Business tem Login for Business e o diálogo recusa `scope`:
"Este app precisa pelo menos de uma supported permission". Use `config_id`.

## FedCM no Chrome Android ignora o config_id
No Android, o SDK entra pelo login federado do Chrome (`dialog_source=fedcm`, `scope=openid`)
e descarta o `config_id`. Contorno: Chrome > Configurações > Configurações de sites >
**Login de terceiros** > "Bloquear solicitações". Aí volta o diálogo normal. Desfaça depois.

## Coexistência (SMB)
`GET /{phone}?fields=is_on_biz_app` = `true` significa número no app WhatsApp Business com a
Cloud API acoplada. `POST /{phone}/register` responde
`Register endpoint is not available for SMB businesses`, e envio dá `133010`. Só religa
refazendo o cadastro de coexistência no celular que tem o app.

## Número de teste da Meta
Vem no caso de uso WhatsApp ("Etapa 1. Experimente"). Pode estar sem registro: `POST /{phone}/register`
com qualquer PIN resolve. Só envia para destinatários cadastrados na UI (a Meta manda um código
de 5 dígitos por WhatsApp ao número). `141006` no WABA de teste bloqueia só conversa iniciada
pela empresa; resposta dentro da janela funciona.

## Send API do Messenger
`messaging_type: MESSAGE_TAG` + `tag: ACCOUNT_UPDATE` dentro da janela de 24h → `(#100) Invalid parameter`.
Dentro da janela o correto é `messaging_type: RESPONSE`.

## Acesso padrão limita a quem tem papel no app
Com acesso padrão, o app só troca mensagem com quem é admin/dev/tester dele. Para gravar o
vídeo, use uma conta com papel no app como "cliente".

## Upload de screencast
Arrastar e soltar por script mostra "screencast carregado" mas pode não salvar. Use o seletor
real de arquivos. No Android, o Chrome só lê `/sdcard` com permissão de armazenamento concedida
(`pm grant ... READ_EXTERNAL_STORAGE`); sem ela a Meta responde "Couldn't load the image".

## "0 de 1 chamada de API obrigatória"
Não é formulário faltando: é o contador da Meta, que leva até 24h. Faça a chamada com token do
app novo e espere.

## Aba descartada no Android
Ao abrir a janela de consentimento, o Android pode descartar a aba de trás por memória; ao
voltar, a resposta do login se perde e o fluxo reinicia. Refaça o login (a segunda vez é rápida,
"você já vinculou").

## Três travas escondidas no fim do envio
- `pages_messaging`: além do texto de reprodução, há um seletor "Selecione uma Página"; o item só conclui com a Página escolhida.
- Com todas as permissões em "Editar", a seção "Uso permitido" continua sem marca até clicar "Avançar" dentro dela.
- O diálogo final tem uma caixa de aceite dos Termos da Plataforma; sem marcar, o botão "Enviar" do diálogo fica desabilitado e o clique não faz nada.
