# Atualização da skill de relatórios de telefonia

A versão 1.4.0 documenta links do portal com cliente, modelo, período e carregamento automático, além do fluxo de geração e recuperação assíncrona pela API. O diagnóstico orienta a refazer snapshots anteriores à correção da coluna Tipo quando apresentarem UNKNOWN para destinos fixos e móveis.

As instruções seguem o contrato publicado em 18/11/2026 e a validação de uma nova geração em produção, incluindo o Excel. Os exemplos usam contexto fictício. A exportação usa o mesmo snapshot da consulta.

[Skill de relatórios de telefonia](../../skills/sufficit/sufficit-telephony-reports/SKILL.md).

## Integração e publicação

A versão 1.4.0 passou no CI do espelho em `d9373aa`. A sincronização manual
integrou a mesma revisão na main do Genius em `2b1266d4` e confirmou a revisão
publicada. A verificação final encontrou as worktrees integradas e os
temporários da entrega já removidos. Worktrees de outras tarefas foram preservadas.

[Workflow de publicação do catálogo](https://github.com/sufficit/sufficit-ai-genius/actions/runs/44411734389).
