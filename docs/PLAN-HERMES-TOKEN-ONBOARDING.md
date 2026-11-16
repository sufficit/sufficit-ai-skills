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
