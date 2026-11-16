# Hermes: orientação de token e Vault validada no tablet

## Objetivo e aceite
Corrigir a orientação de token ausente: oferecer o link direto do perfil Hermes e o link preparado pelo Vault; quando houver sessão pessoal autenticada e ferramentas adequadas, obter o token existente e salvá-lo no Vault sem expô-lo. Validar no tablet com o agente real, sem enviar mensagens a clientes.

## Checkpoints
1. Concluído — inspecionar contratos Hermes/Vault, distribuição das skills e controles do tablet.
2. Concluído — atualizar skills, referências, versões e catálogo; validar o repositório.
3. Concluído — entregar via commit/push na main e verificar distribuição; testar no tablet, corrigindo falhas do escopo.
4. Concluído — evidências e limitações registradas; plano convertido nesta atividade após aceite do fluxo assistido no tablet.

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

Metadados independentes de vault_get_info confirmaram entrada pessoal Active com updatedAtUtc ainda de 03/11, sem rotação ou nova gravação nos testes. A leitura não resolveu o valor.

## Aceite final — 0.4.3
- CI 43890435247 e sincronização Genius 43890509554 aprovados; GCS confirmou versão 0.4.3 e origem 973bef32a0fb2f2ab0efec97d1e8ea98e8e2673b.
- Tablet atualizado por substituição para Genius 0.170.0/build1003514, com firstInstallTime preservado. O APK correspondeu ao SHA256 do manifesto oficial. Após encerramento da conversa ociosa, processo 3241 foi identificado antes de reiniciar somente o aplicativo para renovar o catálogo.
- Sessão 6127caa4-e19f-41c0-bf48-220e40a86403: skill_list comprovou hermes-api 0.4.3 habilitada, Source fixada em 973bef32; pergunta leiga após preparação técnica retornou links Hermes/Vault, Revelar/Copiar de token ativo e interpretação correta de exists=true/saved=false. Export local /tmp/hermes-tablet-final-043.json.
- Sessão nova 8b1bdaa4-c4a4-4f40-9efa-8ab1ba2bbc19, mesmo preset padrão, sem instrução técnica de carregamento: “Nao sei onde copiar meu token do Hermes nem onde salvar para conectar. Me manda os links e explica como fazer, sem trocar minha chave atual.” PASSOU: catalog search → catalog load hermes-api → descoberta Vault → vault_prepare_entry com nome correto. Resposta apresentou os dois links reais, Meus tokens/Revelar/Copiar, cópia de token ativo, estado da entrada existente e aviso sobre substituição. Export local /tmp/hermes-tablet-unassisted-final-043.json; conferidos os URLs da resposta contra o retorno da ferramenta e a página real.
- Metadados do Vault antes/depois: Active e mesma data de atualização de 03/11. Nenhuma chamada vault_save, vault_resolve ou envio de mensagem nos testes finais. Nenhum token revelado. Teste inicial de conexão real respondeu HTTP200/connected/authenticated, writesPerformed=false.

## Limites comprovados
O aceite cobre orientação leiga e conexão com credencial existente, não um onboarding com Vault realmente vazio nem envio ao contato mencionado no relato. A obtenção automática de um token novo pelo agente não foi exercitada: o navegador nativo Android inspecionado oferece navegação/leitura/clique/digitação, sem ponte verificada que transfira um segredo diretamente ao Vault. A skill dá preferência a essa ponte quando existir e mantém o fluxo assistido validado quando ela não estiver disponível; nenhuma nova ponte de runtime foi implementada. O carregamento/atualização inicial da skill e do aplicativo foi preparação do ambiente; a última pergunta de negócio ocorreu em conversa nova e sem instruções técnicas. As falhas anteriores foram preservadas como evidência histórica, superadas pelo aceite final deste fluxo.

## Validação e entrega
193 pacotes validados, índice/versões/cobertura Markdown consistentes e 60 testes existentes aprovados no snapshot isolado da entrega. quick_validate de hermes-api aprovado. A alteração paralela em clear-technical-writing foi preservada e não entrou nos commits. Commits de implementação enviados diretamente à main: 0ebb8ab, f83d1a5, 36d1c03 e 973bef3.

CI da versão final: https://github.com/sufficit/sufficit-ai-skills/actions/runs/43890435247
Publicação conferida do catálogo: https://github.com/sufficit/sufficit-ai-genius/actions/runs/43890509554

O plano foi convertido após a conclusão dos checkpoints autorizados; o fluxo automático condicionado à disponibilidade de uma ponte de segredos permanece como orientação, sem alegação de implementação ou teste ponta a ponta dessa ponte. Exports brutos permanecem fora do repositório público.
