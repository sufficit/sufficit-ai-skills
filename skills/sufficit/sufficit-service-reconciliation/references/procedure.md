# Procedimento e verificação

## Manifesto

Usar plano/manifesto por contexto e etapa, com IDs, versão esperada, fonte, ação,
data/hora pretendida, invariantes e resultado independente. Registrar antes a
sequência completa; não avançar pelo número de operações executadas.

Priorizar comandos já existentes. Na manutenção EFData, procurar no código e na
versão instalada os comandos `ReconcileHistoricalPurchaseCalendar`,
`ExtendSnapshotPurchaseHistory`, `ReconcileInheritedReceiptProjection` e comandos
de cancelamento. Cada um tem pré-condições próprias; nomes não são rotas de API.
Nenhum deles autoriza SQL direto em contratos ou relaxar histórico inconsistente.
A revisão histórica deve respeitar CycleDay; versões antigas usavam DueDay para
ambos e podem deslocar uma competência por um dia. Se o comando não suportar a
âncora correta, registrar bloqueio técnico e corrigir com validação proporcional.

## Captura para o verificador

O diretório contém arquivos JSON produzidos pela leitura real:

- `contracts.json`, `customers.json`, `periods.json`, `renewals.json` e
  `original-purchases.json`;
- `ledger-<customer-guid>.json`: extrato completo com Id,Timestamp,Value,Kind,
  Description,Document,Active; campos extras de versão são preservados;
- `financial-assessment.json`: avaliação **das classes da UI**, lista de
  `{ContractId, Entries:[{Id,Start,End,Amount,Documents,State}]}`.

Não produzir `Entries` recalculando datas para coincidir com o esperado. Usar
`ServiceHistoryAssociation`, `ServiceReconciliation` e `ServiceFinancialAssessment`
do runtime avaliado, incluindo predecessores e compras consolidadas.

```bash
python3 scripts/check_continuity.py \
  --capture /caminho/after --baseline /caminho/before \
  --contract GUID_DO_SERVICO --since 2022-05-27 \
  --as-of 2026-11-14T18:00:00-03:00 \
  --report /caminho/relatorio-novo.json
```

`--since` delimita o bloco cuja continuidade foi comprovada por evidência; não
é filtro para esconder lacunas desconhecidas. Registrar o motivo de excluir
história anterior. O verificador não modifica captura, serviço nem banco e recusa
sobrescrever relatório. Exit0 significa apenas que os checks listados passaram;
exit2 indica divergência/dado indisponível. Repassar os demais gates da skill.

Para correção exclusivamente de competência, os extratos e recibos devem ser
idênticos. Uma manutenção financeira autorizada exige outro manifesto de
alterações e comparação específica; não passar uma baseline nova para disfarçar
mudanças da operação. O saldo atual sozinho não substitui a comparação integral.

## Relatório de entrega

Informar o que mudou, qual era a fonte, verificações realizadas, limites e link do
cliente. Distinguir código enviado à main, runtime instalado e dados realmente
alterados. Uma skill publicada no catálogo não prova instalação/ativação no Genius;
confirmar instalação no ambiente que a utilizará.

A próxima data deve corresponder a uma cobertura projetada real e não pode
preceder GenerateFrom da agenda nativa. Uma data no dia preferencial correto,
mas em outro mês, também é divergência. Compras legadas já reservadas e entregas
agendadas não são a próxima renovação nativa a gerar.
