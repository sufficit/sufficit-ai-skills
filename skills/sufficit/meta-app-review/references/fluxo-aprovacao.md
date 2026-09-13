# Fluxo completo de aprovação (caminhos de tela)

## 0. Pré-requisitos
- Business com `verification_status: verified` (`GET /{business}?fields=verification_status`).
- Uma pessoa com papel de **administradora** do app; só admin do portfólio vincula app a ele.
- App e ativo (WABA/Página) **no mesmo business** — ver armadilha do webhook.

## 1. Criar o app
`developers.facebook.com` > Criar app > caso de uso "Outro" > tipo **Business** > portfólio.
Não existe API para criar, renomear ou vincular app a portfólio.

## 2. Configurações do app
`Configurações > Básico`: ícone, política de privacidade, termos, site, e-mails, categoria,
URL de instruções de exclusão de dados.
`Configurações > Avançado`: ligar **"Permitir acesso da API às configurações do aplicativo"**.
Depois disso dá para gravar tudo por `POST /{app-id}` com app token.

## 3. Login do Facebook para Empresas (quando o app conecta ativos de terceiros)
`Login do Facebook para Empresas > Configurações`:
- **Entrar com o SDK do JavaScript** = Sim;
- **Domínios permitidos para o SDK do JavaScript**: uma entrada por domínio, com `https://` e barra final;
- **URIs de redirecionamento do OAuth válidos**: obrigatório quando "modo estrito" está ligado.

`Login do Facebook para Empresas > Configurações (lista) > Criar configuração`:
nome > variação **Geral** > **token de acesso do usuário** (com token de system user não se
escolhem ativos) > permissões. Gera o **`config_id`**, que é o parâmetro do diálogo.
`FB.login(cb, { config_id })`; `scope` clássico não funciona nesses apps.

## 4. Casos de uso e permissões
`Casos de uso > Personalizar > Permissões e recursos`. "Pronto para teste" = acesso padrão,
que só vale para quem tem papel no app. Permissões podem pertencer a mais de um caso de uso.

## 5. Tech Provider (irreversível)
Ao clicar em "Adicionar à análise do app" a Meta exige virar Tech Provider: verificação da
empresa + verificação de acesso + análise. **Confirme com o dono antes.** Depois de aceito,
as permissões exigidas pelos casos de uso entram sozinhas no envio.

## 6. Uso permitido (por permissão)
`Análise do app > Ir para o uso permitido > Começar`:
1. descrição do uso (o que faz, que valor dá, por que é necessária);
2. screencast;
3. chamada de API de teste (contador da Meta, até 24h);
4. aceite de conformidade.
`pages_messaging` pede também instruções de reprodução. `pages_manage_metadata` exige
`pages_show_list` no mesmo envio. `public_profile` e `email` só pedem o aceite.

## 7. Tratamento de dados
Operadores de dados (sim/não), controlador (razão social), país, pedidos de autoridades nos
últimos 12 meses, políticas aplicadas. São declarações legais: confirme com o responsável,
não copie no automático.

## 8. Instruções para o analista
URL do ambiente, conta de teste que funcione, passo a passo até a tela de cada permissão e
resposta a "Is Facebook Login integrated on this platform?".

## 9. Enviar
O botão só habilita com as cinco seções concluídas. Depois de enviado não dá para editar
nem cancelar enquanto estiver em análise.
