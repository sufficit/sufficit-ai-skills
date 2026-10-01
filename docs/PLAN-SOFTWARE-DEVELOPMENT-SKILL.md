# Software-development: migração e instalação vinculada

Objetivo: tornar sufficit-ai-skills a fonte canônica, melhorar o fluxo e instalar
no Codex uma skill versionada com conferência explícita de atualizações.

## Checkpoints
1. [completed] Inspecionar origem, catálogo, convenções e descoberta do Codex.
2. [in_progress] Criar pacote 1.0.0 e melhorar instruções; integrar catálogo/digest.
3. [pending] Implementar instalação vinculada, backup e conferência local/remota; testar isoladamente.
4. [pending] Validar pacote e CI público; publicar revisão na main canônica.
5. [pending] Migrar instalação real com backup, conferir atualização e descoberta no Codex; registrar entrega.

## Decisões e limites
- Origem: /home/hugodeco/.codex/skills/software-development; preservar conteúdo antigo em backup fora da descoberta.
- Destino canônico: skills/sufficit/software-development, release.json e metadata.version 1.0.0.
- Symlink no CODEX_HOME/skills aponta ao checkout canônico, não a worktree temporária.
- Check remoto por uso: consulta versão/digest, sem pull/instalação automática nem timer permanente.
- Estado local e recibos ficam fora do pacote versionado; falha de rede é resultado desconhecido, nunca atualizado.
- Usuário pediu migração, aperfeiçoamento e reinstalação; não alterar outras skills nem configurar outros agentes.
- CI público usa ubuntu-latest. Instalação ligada usa helper próprio porque o instalador oficial faz cópias desconectadas.

## Aceite e validação
- Skill válida, versionada e incluída no manifesto com digest verificável.
- Plano sempre em docs/PLAN-*.md, progresso atualizado e validação baseada em evidência.
- Instalação preserva original, é idempotente, recusa fonte alterada e links inesperados.
- Check distingue current/update-available/modified/unavailable; compara pacote, não apenas HEAD global.
- Testes sem rede para instalação, atualização disponível, fonte modificada e falha remota.
- Conferência real da instalação e descoberta no Codex após publicação.
