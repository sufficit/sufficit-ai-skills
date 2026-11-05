# Execução Sufficit/Hermes para pedidos leigos

Sessão de engenharia: 01a1acfc-ba97-7573-927c-d1b3df359815.
Evidência: exportação local da sessão c9e5f612-10d1-4b9d-97d9-ffdea69ccc12;
nenhum dado pessoal ou token da exportação foi copiado para este repositório público.

## Diagnóstico e correção

A execução emitiu o boleto, encontrou o grupo e comprovou autenticação Hermes,
mas terminou sem atendimento/anexo. Tentou comandos Unix e PowerShell diretamente
em CMD. As instruções atuais de hermes-api ainda proibiam o fallback de API no Genius.

- hermes-api 0.3.0: descoberta exata, API autenticada quando falta wrapper, metadados
  e resolução do Vault conforme contrato, contexto do shell Windows, atendimento,
  multipart/PDF e verificação independente do envio.
- sufficit-api 1.0.23: pedido leigo completo, descoberta antes de alegar incapacidade,
  fluxo de emissão/idempotência/documento e encaminhamento à skill Hermes.
- Catálogo, cartões, versões e digests atualizados. Nenhuma mudança de runtime.
- A API Sufficit continua com autenticação automática; a credencial Hermes é
  separada. A ausência de variável de ambiente não implica ausência no Vault.
- Não exigir nova autorização para etapas já expressamente pedidas; respeitar
  recusas reais do host e da API e explicar a etapa que efetivamente falhou.

## Evidências e validação

GET público de https://chatwoot.sufficit.com.br/swagger/swagger.json respondeu e
expôs profile, contatos/conversas, inboxes, criação de conversa e mensagens.
O Swagger não detalha attachments; o código local Hermes confirma que
MessagesController#create encaminha params a Messages::MessageBuilder, que lê
attachments e processa arquivos. Isto é evidência de implementação, não prova de
envio na instância da usuária. As instruções registram essa diferença.

Validação em worktree isolada com os 13 arquivos da entrega: 184 pacotes válidos,
índice atualizado, cobertura Markdown completa, 38 testes existentes aprovados,
git diff --check sem erro. quick_validate.py passou nas duas skills.
A primeira execução na árvore compartilhada falhou apenas por dois planos locais
fora da hierarquia, incluindo um de outra tarefa. O plano alheio foi preservado.

Revisão de cenários contra os contratos, sem simular uma execução por outro modelo:

| Cenário | Caminho exigido pelas instruções |
| --- | --- |
| Pedido leigo de boleto + atendimento + PDF | Resolver IDs, emitir uma vez, concluir e verificar as três etapas |
| Ferramenta Hermes ausente | Descobrir wrapper; ler OpenAPI e usar fallback autenticado |
| Variável HERMES ausente e conexão já bem-sucedida | Preservar evidência e localizar credencial no Vault |
| Comando PowerShell executado por CMD | Invocar interpretador explicitamente, sem inferir falha de acesso |
| Grupo e pessoa com nomes similares | Usar grupo, vínculo de inbox e contexto verificáveis |
| Boleto pronto e envio falha | Preservar ID; não emitir outra cobrança |
| Upload responde sem confirmação ou timeout | Ler mensagens/anexos antes de repetir escrita |
| HTTP 403 ou Vault negado | Bloqueio específico com evidência, sem troca de identidade |
| PDF retorna HTML | Resolver download real; não renomear HTML como PDF |

Nenhuma resolução de segredo, cobrança, atendimento ou mensagem real foi executada.
Os testes de repositório e a revisão de cenários não provam sucesso ponta a ponta
com o preset da usuária; isso exige uma nova execução autorizada no Genius.

## Distribuição

Commit/push direto na main conforme instrução do mantenedor. O CI de skills valida
os pacotes; o workflow skill-catalog-sync do Genius fixa a revisão e publica o
catálogo sem rebuild de binário. Resultado remoto será conferido nesta execução.
