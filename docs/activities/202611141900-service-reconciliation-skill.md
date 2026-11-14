# Skill de reconciliação de serviços e aceite independente

O mantenedor solicitou em14/11/2026 um procedimento reutilizável após correções
repetidas que deixavam vencimento, competências, antecipações e intervalos sem
validação conjunta. Criada [sufficit-service-reconciliation](../../skills/sufficit/sufficit-service-reconciliation/SKILL.md), versão1.0.0.

O pacote distingue contrato/competência/vencimento/emissão, períodos inclusivos
legados versus exclusivos nativos, calendário histórico versus preferência atual,
repasse05:59/débito06:00, recibo externo e crédito de telefonia. Exige comentários,
identidades, snapshots, consumidor durável, rollback e releitura antes de fechar
um caso. Alterar somente a data de um lançamento futuro não desfaz sua emissão.

O verificador somente leitura recebe capturas completas antes/depois e entradas
calculadas pelas classes reais da UI. Confere continuidade no bloco comprovado,
calendário explícito, vínculos financeiros futuros, débitos por documento exato,
extratos/recibos preservados e campos originais das compras. Recusa dados ausentes,
fuso de as-of omitido e sobrescrita do relatório. Explicita os gates que não executa;
não é uma declaração de auditoria integral da carteira nem ferramenta de escrita.

13 testes adversos aprovados: uma lacuna com financeiro conciliado ainda falha;
redatar vínculo financeiro para o futuro falha; saldo igual com documento mudado
falha; datas originais/recibos não podem ser reescritos. Formato real `dueday` do
capture também foi validado. Validação estrutural da skill, versões e índice
aprovados. Catálogo e digests atualizados só para os pacotes desta tarefa.

A skill API passa a apontar esse procedimento, versão1.1.1. Instalação Codex por
symlink em `~/.codex/skills/sufficit-service-reconciliation`, conferida no disco.
Não declarar ativação no Genius: seu catálogo exige sincronização de revisão
imutável própria. Validação integral em snapshot de entrega isolado:191 pacotes, versões, índice
e cobertura Markdown aprovados, preservando alterações paralelas de outras
sessões.13 testes adversos aprovados no mesmo snapshot.

Evidência operacional privada:tmp/deoforte-historical-continuity-20261114/.
A verificação real inicial identificou56 lacunas e56 fronteiras fora da âncora
nos dois serviços selecionados; o caso operacional é documentado no EFData.

Resultado real:112 achados antes (56 lacunas/56 fronteiras) e0 após a revisão
das108 competências. Próxima renovação também é conferida contra a vigência
projetada e GenerateFrom; o dia preferencial correto sozinho não prova o mês.
