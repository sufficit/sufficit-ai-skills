# Hermes: conexão assistida e autônoma no tablet

## Objetivo e aceite
Corrigir a orientação de token ausente: oferecer o link direto do perfil Hermes e o link preparado pelo Vault; quando houver sessão pessoal autenticada e ferramentas adequadas, obter o token existente e salvá-lo no Vault sem expô-lo. Validar no tablet com o agente real, sem enviar mensagens a clientes.

## Checkpoints
1. Concluído — inspecionar contratos Hermes/Vault, distribuição das skills e controles do tablet.
2. Concluído — atualizar skills, referências, versões e catálogo; validar o repositório.
3. Em andamento — entregar via commit/push na main e verificar distribuição; testar no tablet, corrigindo falhas do escopo.
4. Pendente — registrar evidências finais e converter este plano em atividade se todo o aceite for comprovado.

## Restrições
Preservar alteração paralela em clear-technical-writing. Não registrar segredos, copiar credencial de outro usuário, rotacionar tokens ou enviar mensagens ao contato citado como teste. Login/MFA permanecem com o usuário quando necessários. Não confundir publicação com push nem teste estático com execução no tablet.

## Validação prevista
Validador/catalog/index/Markdown e testes existentes pertinentes; diff sem whitespace; sessão nova no tablet com recuperação do pacote e evidências de ferramentas/resposta; leitura de metadados Vault e teste de conexão quando o fluxo autônomo for executável.

## Descoberta
Tablet Lenovo HA1NP62H disponível via ADB. Fonte Hermes confirma rota pessoal /app/profile/access-tokens, fallback /app/profile/settings, contexto pessoal separado de conta e ação de revelar distinta de rotacionar. A skill hermes-api 0.3.0 não tinha onboarding de token ausente.

## Validação da implementação
hermes-api 0.4.0 com referência token-onboarding, roteamento no entrypoint/fallback e versões/digests/índice atualizados. quick_validate aprovado. Snapshot isolado /tmp/hermes-skills-validation-c7rxriei: 193 pacotes válidos, índice/versões/cobertura Markdown corretos, 60 testes aprovados. Árvore compartilhada tem digest divergente somente da alteração paralela preservada em clear-technical-writing. O snapshot foi inicializado como repositório Git para o inventário Markdown.

## Primeira execução no tablet
Genius 0.166.0-dev.42, preset Sufficit AI - Default, conversa nova 35120cde-1e96-4e01-a801-04b0c52c48b8. Pedido leigo de conectar a própria conta sem mensagens a clientes: hermes_connection_test teve sucesso; credencial já existe. Esse teste não cobre ausência de token. CI 43888102108 aprovado e sync 43888176969 iniciado. Revisão 0.4.1 também explicita conexão na descrição de descoberta e atualiza cartão/metadados de interface.

## Aceite incremental
- Página real no Chrome do tablet aberta e confirmada: /app/profile/access-tokens, contexto Meus tokens, ações Revelar/Editar/Rotacionar/Revogar. Nenhum segredo revelado.
- Sync 43888176969 concluiu e publicou 0.4.0 em GCS; sync 43888420241 da 0.4.1 em andamento.
- Sessão 888d6736-3898-4c3c-8a45-a53fd15c7f20, pergunta hipotética leiga sem alterar a conexão: FALHOU na primeira resposta. Exportação local /tmp/hermes-tablet-guidance-first.json comprova busca catalog que retornou hermes-api como install_required e descrição antiga; agente não fez o next_call de carregamento e respondeu sem os links. Não atribuir isso a falha do texto novo sem carregá-lo. Continuação solicita consulta à habilidade atualizada para verificar execução da orientação; depois repetir pedido leigo sem essa ajuda.

- Sync 43888420241 concluiu com sucesso; leitura independente do GCS confirma hermes-api 0.4.1 fixada em f83d1a5cc35f5df6ca5e3420145869cd699ff2fb.
- Continuação assistida na versão antiga também falhou: fez quatro buscas/listagens e não chamou catalog load apesar do next_call fornecido. Atualização do tablet para release estável 0.170.0 em andamento, APK verificado contra stable.json (SHA256 9e50b6eaf7d46bf0ab6127be349fc1259c39fa30a6d1650bea32190215c8ac27), instalação -r sem limpeza de dados.

## Correção orientada pelo tablet — 0.4.2
Genius 0.170.0 também não carregou espontaneamente a skill retornada como install_required. Solicitação técnica explícita de catalog load carregou a 0.4.1, mas a resposta ignorou a referência complementar e ainda disse não haver endereço direto; não preparou Vault. Correção: procedimento mínimo com link direto, nome exato de vault_prepare_entry e cópia de token ativo promovido ao SKILL.md. A referência fica para recuperação autônoma; descrição/tags incorporam termos leigos em português para descoberta. Esse teste foi assistido e falhou; não equivale a aceite espontâneo.

## Links confirmados e semântica de preparação — 0.4.3
Continuação da sessão 8a9d3bb0-7734-40c6-9d13-df2c206d3f95 no tablet: leu references/token-onboarding.md e chamou vault_prepare_entry com nome correto; retornou os dois links reais. Export /tmp/hermes-tablet-guided-links-041.json. Resultado de preparação: exists=true, status=Active, saved=false. O agente interpretou saved=false como entrada existente ainda não salva. A 0.4.3 distingue explicitamente preparação sem escrita de ausência de segredo; não pedir substituição em tutorial hipotético. Ainda pendente novo aceite após distribuição.
