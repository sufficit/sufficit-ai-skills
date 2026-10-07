# Desempenho com sessões simultâneas

Objetivo: incorporar regras de renderização Blazor na skill e reduzir trabalho redundante no Genius, preservando streaming por eventos, histórico, confirmações duráveis e recuperação.

1. [EM ANDAMENTO] Atualizar skill de desenvolvimento: parâmetros imutáveis, ShouldRender, IsFixed e diagnóstico antes de throttling; validar pacote.
2. [PENDENTE] Implementar streaming por alterações com snapshot inicial e compatibilidade; preservar mensagens anteriores.
3. [PENDENTE] Isolar mensagens em componentes e restringir renderizações aos dados afetados.
4. [PENDENTE] Direcionar notificações de chat/diretório aos componentes correspondentes.
5. [PENDENTE] Tratar persistência separadamente: coalescer saves e persistir somente sessões alteradas com migração segura.
6. [PENDENTE] Validar concorrência 1/3/5, histórico grande, durabilidade, cancelamento e recuperação; CI completo.
7. [PENDENTE] Documentar atividades, publicar entregas revisáveis e atualizar estado final.

Restrições: sem timer de renderização 100ms; sem perder delta/histórico; valores em cascata fixos apenas quando realmente invariáveis; callbacks/idioma/expiração continuam atualizando mensagens; nenhuma alteração em dados de produção ou reinício automático.
Validação: skills/scripts/validate.py e quick_validate; testes de streaming, renderização e persistência com regressão antes/depois; bash scripts/ci-local.sh.
Bloqueios: nenhum.
