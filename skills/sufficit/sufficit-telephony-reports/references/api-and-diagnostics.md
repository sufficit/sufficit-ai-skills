# Contrato e diagnóstico

Contrato observado em 05/11/2026. Consulte o catálogo em execução e o
[guia mantido em sufficit-endpoints](https://github.com/sufficit/sufficit-endpoints/blob/main/docs/USAGE-TELEPHONY-REPORTS.md)
para mudanças. O contrato compartilhado fica em sufficit-base, o motor em
sufficit-standard, o transporte em sufficit-client e a superfície em sufficit-blazor.

| Modelo | Conteúdo | Filtros opcionais |
| --- | --- | --- |
| `billed-calls` | Chamadas tarifadas e valores cobrados | Nenhum |
| `billed-by-operator` | Tarifadas por atendente | `dids`, `filter` |
| `outbound-calls` | Chamadas de saída | `dids`, `filter` |
| `outbound-by-operator` | Saídas por atendente | `dids`, `filter` |
| `lost-calls` | Chamadas perdidas | `dids`, `filter` |
| `operators` | Atendimento por operador | `dids`, `filter` |
| `calls-by-hour` | Entradas agrupadas por hora | `dids`, `filter` |
| `billed-by-did` | Tarifadas por DID | Nenhum |
| `usage-by-extension` | Uso por ramal e direção | `discardSeconds` |

Limites iniciais: 31 dias, exceto `calls-by-hour` (48 horas); quatro execuções
simultâneas por instância; 100.000 linhas (erro em vez de truncamento);
até 100 DIDs de 40 caracteres, texto de 200 caracteres. Tags opcionais de telas
legadas não são expostas nesse contrato. Não suponha que contagem de linhas
seja contagem de chamadas em modelos agrupados: use os totais do modelo.

`billed-calls` retorna `Registros`, `Segundos` e `Valor (R$)` nos totais.
A soma monetária usa a coluna `Custo`, preservando sua precisão. Tempos são
segundos; para apresentar duração, converta sem modificar o arquivo original.
A aba `Resumo` contém contexto, intervalo UTC, fuso, instante de geração,
totais e observações. O nome amigável do cliente pode ser obtido pela busca
que resolveu o contexto; não o confunda com o GUID presente na aba.

## Diagnóstico proporcional

- **401/403:** diferencie credencial ausente/expirada de permissão por contexto.
  Não altere concessões como parte da geração do relatório.
- **400:** confira modelo, período, segundos, fuso e capacidades de filtro.
- **429/504:** respeite limite/timeout. Se for necessário reduzir o período,
  informe isso; não apresente o intervalo menor como o relatório completo pedido.
- **500 na exportação:** registre a mensagem sem conteúdo sensível. Quando há
  acesso operacional autorizado, examine o erro interno e as dependências da
  aplicação instalada. JSON sem Excel pode ajudar a isolar o problema, mas é
  outra execução; não afirme que é o mesmo snapshot da tentativa que falhou.
- **502 durante publicação:** verifique se houve reinício ou troca de versão
  antes de repetir; não atribua automaticamente o erro à consulta.

### Regressão EPPlus observada

O teste operacional de 05/11/2026 encontrou
`MissingMethodException: ExcelWorksheet.get_Dimension()`: Standard compilado
contra EPPlus 7.1.2 e API publicada com EPPlus 8.7.2 devido a dependência `*`.
Foi corrigido alinhando a dependência da API ao renderer e testando geração real
com `includeSpreadsheet=true`, abertura do XLSX e comparação com JSON.
Essas versões são evidência histórica, não uma ordem permanente para downgrade.
Verifique a compatibilidade das versões atuais antes de corrigir.

Se a tarefa incluir implementação/publicação, siga os AGENTS.md dos repositórios.
Teste o candidato com as bibliotecas reais de runtime; preserve correções de
segurança e catálogo já publicadas e confirme os hashes após a instalação.
A geração ordinária de um relatório não autoriza deploy ou troca de DLLs.

A rota antiga `/Reports` tem relatórios agregados de gestores e não substitui
`/Telephony/Reports` por cliente. Não use a rota antiga para contornar uma negativa
de autorização. A existência da API nova não comprova que telas legadas foram
removidas nem que todos os modelos já tiveram paridade operacional validada.
