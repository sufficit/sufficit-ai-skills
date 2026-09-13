# Chamadas de API úteis (e as que contam como teste)

Todas com `appsecret_proof` quando o app exigir prova de segredo:
`proof = HMAC-SHA256(access_token, app_secret)`.

```bash
APP=<app_id>; SEC=<app_secret>; AT="$APP|$SEC"      # app token
proof(){ printf '%s' "$1" | openssl dgst -sha256 -hmac "$SEC" | sed 's/^.* //'; }
```

## Conferir token antes de qualquer coisa
```bash
curl -s "https://graph.facebook.com/v22.0/debug_token?input_token=$T&access_token=$AT"
```
Olhe `app_id`, `type`, `expires_at` e `granular_scopes[].target_ids`
(`null` = irrestrito; array = só aqueles ativos).

## Configurações do app (exige a chave "acesso da API às configurações")
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$APP" \
  --data-urlencode "app_domains=[\"exemplo.com.br\"]" \
  --data-urlencode "privacy_policy_url=https://exemplo.com.br/privacy" \
  --data-urlencode "access_token=$AT"
```

## Webhooks do app
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$APP/subscriptions" \
  --data-urlencode "object=whatsapp_business_account" \
  --data-urlencode "callback_url=https://host/webhooks/whatsapp" \
  --data-urlencode "fields=messages,calls" \
  --data-urlencode "verify_token=$VT" --data-urlencode "access_token=$AT"
```
`object=page` para Messenger. A Meta faz um GET de verificação: o endpoint tem que responder
200 com o `hub.challenge`.

## Inscrever o app no ativo
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$WABA/subscribed_apps" -d "access_token=$USER_OU_SU_TOKEN"
curl -s -X POST "https://graph.facebook.com/v22.0/$PAGE/subscribed_apps" \
  -d "subscribed_fields=messages,message_deliveries,message_reads,message_echoes" -d "access_token=$PAGE_TOKEN"
```

## Número de WhatsApp
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$PHONE/register" -d messaging_product=whatsapp -d pin=000000 -d "access_token=$T"
curl -s "https://graph.facebook.com/v22.0/$PHONE?fields=status,platform_type,is_on_biz_app,health_status&access_token=$T"
```
`health_status` diz exatamente o que bloqueia envio e chamada (por número, WABA, business e app).

## Chamadas que contam como teste, por permissão
| Permissão | Chamada |
|---|---|
| whatsapp_business_management | `GET /{waba}?fields=id,name` · `GET /{waba}/phone_numbers` · `GET /{waba}/message_templates` |
| whatsapp_business_messaging | `POST /{phone}/messages` (template ou resposta na janela) |
| business_management | `GET /me/businesses` |
| pages_show_list | `GET /me/accounts` |
| pages_manage_metadata | `POST /{page}/subscribed_apps` |
| pages_messaging | `POST /me/messages` com token de página |

Use **token do app que está sendo analisado**. O token temporário de 24h da tela
"Etapa 1. Experimente" serve.

## System user (token que não expira)
```bash
curl -s -X POST "https://graph.facebook.com/v22.0/$BUSINESS/system_users" -d "name=Integracao" -d "role=EMPLOYEE" -d "access_token=$ADMIN"
curl -s -X POST "https://graph.facebook.com/v22.0/$BUSINESS/access_token" \
  -d "scope=business_management,whatsapp_business_management,whatsapp_business_messaging" -d "access_token=$ADMIN"
```
Token de usuário morre quando a pessoa faz logout; system user não.
