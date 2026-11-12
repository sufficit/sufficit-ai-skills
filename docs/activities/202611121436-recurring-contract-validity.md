# Contrato recorrente: término contratual e fim da competência

Concluído em 12/11/2026 por solicitação do mantenedor: outro agente havia tratado
a renovação mensal como extensão do término de um contrato nativo recorrente.

## Entrega

Skill `sufficit-api` elevada de 1.0.39 para 1.0.40, com entrada visível antes do
fluxo de renovação e referência dedicada
[recurring-contract-validity](../../skills/sufficit/sufficit-api/references/recurring-contract-validity.md).
As referências de vendas e conciliação levam à mesma orientação.

Acordo nativo recorrente por prazo indeterminado usa `Contract.End = null`;
o fim finito de cada competência pertence a `ContractPeriod.PeriodEnd`.
Próximo vencimento e classificação pré-paga não encerram a contratação.
Exemplo: competência `[03/11, 03/12)` e próxima `[03/12, 03/01)` sem término
contratual em 03/12. Preservam-se prazos determinados explícitos, cancelamentos,
pausas e a semântica de projeção LegacySales; não há autorização para limpeza em
massa de datas nem migração implícita.

O caso motivador foi corrigido pelo `EFSalesProvider`, fora da operação desta
skill de API: retirada somente do término indevido, histórico transacional,
nenhuma nova renovação ou movimentação financeira. Contrato, períodos, histórico,
saldo, replay global e comissões foram relidos. A documentação e o AGENTS.md do
EFData também receberam a regra. Evidências operacionais privadas em
`/mnt/workspaces/sufficit/tmp/recurring-contract-end-20261112/`.

## Validação e distribuição

- `skill-creator/scripts/quick_validate.py`: pacote válido.
- `scripts/validate.py`: 185 pacotes aprovados em snapshot isolado de HEAD com
  somente esta mudança sobreposta. Isso preserva a alteração paralela em
  `clear-technical-writing/SKILL.md`, cujo conteúdo não integra esta entrega.
- `scripts/catalog_versions.py --check` e `build_skill_index.py --check`: aprovados
  nesse mesmo snapshot. Release, versão do catálogo e digest do pacote atualizados.
- Revisão das decisões: contrato nativo indefinido, prazo determinado explícito,
  projeção LegacySales e competência mensal finita permanecem distintos.
- `git diff --check` sem erros. Cobertura Markdown validada após indexação.

Nenhuma lógica de produto alterada e nenhum deploy executado. Commit/push do
pacote não substitui sincronização do catálogo Genius nem comprova atualização
de uma versão já fixada em outro agente. O plano concluído foi convertido nesta
atividade; não há checkpoints pendentes deste escopo.
