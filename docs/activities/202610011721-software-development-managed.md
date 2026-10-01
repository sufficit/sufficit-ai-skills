# Software-development 1.0.0 — migração e instalação vinculada

Concluído em 2026-10-01T17:21:55.553362-03:00.

## Entrega
- Fonte canônica: skills/sufficit/software-development, incluída nos 164 pacotes do catálogo.
- PR https://github.com/sufficit/sufficit-ai-skills/pull/6 integrado; revisão publicada 9028c8b4ae27fb1c69c0a94055f1b54a3159cef7.
- Versão 1.0.0 em release.json e metadata.version; digest 1aeb7e719af345e06a5cb7ed99c916fa8f3e62b73cc1bffe833a2aca98a0f93f.
- Codex instalado por symlink de /home/hugodeco/.codex/skills/software-development para /mnt/sufficit/sufficit-ai-skills/skills/sufficit/software-development.
- Original preservado em /home/hugodeco/.codex/skill-backups/software-development-20261001T202119Z-12d513df.
- Recibo em /home/hugodeco/.codex/skill-installations/software-development.json.

## Melhorias
Plano completo em docs/PLAN-*.md, checkpoints atuais e retomada sem repetir trabalho.
Investigação termina quando contrato, ponto de implementação e validação estão claros;
leituras adicionais respondem a incertezas identificadas. Falhas e cancelamentos exigem
classificação antes de repetir. A entrega separa implementação, teste, publicação e
comportamento observado. A skill não concede autorização para publicar ou comunicar
em nome do usuário por conta própria.

Conferência remota instruída no primeiro uso de cada sessão: compara versão/digest do
pacote na main por SHA imutável. Não executa pull nem instalação automática. Falha de
rede é unavailable, nunca current. O vínculo acompanha o checkout local; atualização
remota exige o procedimento documentado em references/installation.md.

## Evidências
- Nove testes isolados aprovados: instalação, migração e backup, idempotência,
  preservação de cópia/link, rejeição de fonte alterada, rollback, estados remotos,
  falha de rede e CLI. CI público executa a mesma suíte.
- scripts/validate.py aprovou os 164 pacotes; quick_validate.py aprovou a skill.
- CI do PR aprovado: https://github.com/sufficit/sufficit-ai-skills/actions/runs/36920840446.
- Instalação real retornou linked e check --remote retornou current para 1.0.0.
- codex app-server skills/list com forceReload encontrou exatamente uma skill
  software-development, scope user, enabled true, no caminho canônico do repositório.
- Backup original existe e o symlink resolve para a origem publicada.

## Limites
A conferência por sessão é uma instrução da skill, não um serviço permanente. Conversas
que já carregaram instruções antigas não são reescritas. A descoberta atual do Codex foi
verificada; nenhum outro perfil ou agente foi instalado e nenhum daemon foi adicionado.
