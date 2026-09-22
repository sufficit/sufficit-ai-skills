---
name: meta-app-review
description: Aprova apps da Meta (WhatsApp, Messenger, Instagram) na Análise do App e opera o Business Manager. Use para criar ou configurar app num portfólio, pedir acesso avançado a permissões como whatsapp_business_management, whatsapp_business_messaging, pages_messaging e business_management, gravar os screencasts exigidos, conectar Página ou conta do WhatsApp Business a uma plataforma, ou diagnosticar webhooks, Facebook Login for Business, números de WhatsApp e erros da Graph API nesses fluxos.
metadata:
  version: "1.0.5"
---

# Meta App Review

Levar um app da Meta até o envio para análise sem perder dias com respostas enganosas. Os
detalhes ficam em `references/` e devem ser lidos só quando o passo exigir.

## A regra que mais custa tempo

Boa parte do que decide a aprovação só existe na interface, e a Graph API devolve `success`
para operações que não produzem efeito. Separe antes de automatizar:

| Só na interface (developers.facebook.com) | Por API |
|---|---|
| criar, renomear e vincular o app a um portfólio | configurações básicas, depois de ligar o acesso por API em Configurações > Avançado |
| produtos, casos de uso e permissões | webhooks do app (`POST /{app}/subscriptions`) |
| configurações do Facebook Login for Business (geram o `config_id`) | inscrever o app no ativo (`POST /{ativo}/subscribed_apps`) |
| domínios do SDK de JavaScript e URIs de redirecionamento | registrar número (`POST /{phone}/register`) |
| destinatários do número de teste | enviar mensagens, ler templates, `debug_token` |
| tornar-se Tech Provider e enviar para análise | tokens de usuário do sistema |

## Ordem que funciona

1. Business verificado (`verification_status: verified`); sem isso não há acesso avançado.
2. App e ativos (WABA, Página) no mesmo business. Webhook só é entregue ao app do business
   dono do ativo — ver [armadilhas](references/armadilhas.md).
3. Configuração básica completa: ícone 1024x1024, política de privacidade, termos, instruções
   de exclusão de dados, categoria. Aproveite um app já aprovado quando houver.
4. Casos de uso e permissões, que começam em acesso padrão ("Pronto para teste").
5. **Tech Provider**. A própria Meta avisa que é irreversível. Peça confirmação explícita do
   responsável antes de aceitar.
6. **Uso permitido**, por permissão: descrição, screencast, chamada de API de teste e aceite.
7. **Tratamento de dados** e **instruções para o analista**, com uma conta de teste funcional.
8. Enviar. Depois de enviado não é possível editar nem cancelar.

Caminhos de tela e o conteúdo de cada seção: [fluxo de aprovação](references/fluxo-aprovacao.md).

## O que trava o botão de envio

"Enviar para análise" fica desabilitado enquanto uma permissão mostrar
**"0 de 1 chamada(s) de API obrigatória(s)"**. Faça uma chamada típica de cada permissão com
token do app analisado — de escrita quando a permissão permite escrever — e aguarde: a Meta
informa até 24 horas para o contador refletir. Repreencher o formulário não adianta.
Chamadas por permissão em [chamadas de API](references/chamadas-api.md).

## Screencasts

- Mostre o fluxo real do produto, do ponto de vista do usuário, com legendas em inglês que
  nomeiem a permissão em uso. Um mesmo vídeo pode atender várias permissões.
- Corte os trechos em que a tela fica vazia carregando.
- Não grave dados pessoais de terceiros (listas de conversas, contatos). Se aparecerem, pare e
  apague o arquivo.
- Anexar arquivo por arrastar e soltar via script pode não salvar; use o seletor de arquivos real.
  Receitas em [automação da interface](references/automacao-ui.md).

## Erros que enganam

| Mensagem | Causa real |
|---|---|
| "Este app precisa pelo menos de uma supported permission" | app com Facebook Login for Business: o diálogo aceita `config_id`, não `scope` |
| "A opção JSSDK não está ativada" | ligar "Entrar com o SDK do JavaScript" e cadastrar o domínio |
| "O domínio dessa URL não está incluído nos domínios do app" | modo estrito ligado sem a URL em "URIs de redirecionamento do OAuth válidos" |
| `(#10) Changing app settings through API calls has been disabled` | ligar o acesso por API em Configurações > Avançado |
| `(#100) Invalid parameter` ao responder no Messenger | `MESSAGE_TAG` dentro da janela de 24h; usar `messaging_type: RESPONSE` |
| `(#133010) Account not registered` | número sem registro na Cloud API ou coexistência desfeita |
| `Register endpoint is not available for SMB businesses` | número em coexistência com o app WhatsApp Business |
| `(#131030) Recipient phone number not in allowed list` | número de teste só envia a destinatários cadastrados |
| webhook inscrito e nenhum evento chega | app de outro business; só o dono do ativo recebe |
| `141011` no APP (`can_receive_call_sip: BLOCKED`) | cliente não compartilhou a WABA com o business do app |
| `138025` | servidor SIP não gravado no número com o token deste app |
| "<app> não pode integrar clientes no momento" | integração de Provedor de Tecnologia não concluída |
| "Parece que esse app não está disponível" com `dialog_source=fedcm` | FedCM do Chrome perdeu o `config_id` |

Diagnóstico completo em [armadilhas](references/armadilhas.md). Chamadas do WhatsApp por SIP para
números de clientes (quem compartilha o quê, saúde que atrasa, separar chamadas de mensagens):
[chamadas por SIP](references/whatsapp-calling-sip.md). Um app para mensagens + chamadas e para só voz
(clientes com mensageria em concorrente ou só voz), e a regra de webhook para um app só:
[cenários](references/cenarios-mensageria-chamadas.md).

## Segurança

- Credenciais de teste do analista ficam em armazenamento restrito, nunca na conversa.
- Tech Provider, envio para análise e declarações de tratamento de dados são decisões do
  responsável pelo app: confirme antes.
- Não altere segurança de contas pessoais, não crie PIN e não vincule navegadores a contas
  gerenciadas ao conduzir a interface.
- Registre as mudanças temporárias feitas para gravar ou testar e desfaça-as ao terminar.
