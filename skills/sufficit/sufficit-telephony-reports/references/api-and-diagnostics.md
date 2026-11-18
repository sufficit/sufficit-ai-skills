# Contrato e diagnóstico

Contrato da fila verificado em produção em 18/11/2026. Consulte o catálogo em execução e o
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

O catálogo usa `maximumHours: 0` para indicar que o modelo aceita qualquer
duração válida, inclusive em `calls-by-hour`. A rota síncrona aceita quatro execuções
simultâneas por instância. A geração aceita até 100.000 linhas (excesso gera erro), até 100 DIDs de
40 caracteres e texto de até 200 caracteres. Tags opcionais de telas
legadas não são expostas nesse contrato. Não suponha que contagem de linhas
seja contagem de chamadas em modelos agrupados: use os totais do modelo.

`billed-calls` retorna `Registros`, `Segundos` e `Valor (R$)` nos totais.
A soma monetária usa a coluna `Custo`, preservando sua precisão. Tempos são
segundos; para apresentar duração, converta sem modificar o arquivo original.
A aba `Resumo` contém contexto, intervalo UTC, fuso, instante de geração,
totais e observações. O nome amigável do cliente pode ser obtido pela busca
que resolveu o contexto; não o confunda com o GUID presente na aba.

## Geração em segundo plano

As rotas abaixo têm o prefixo `/Telephony/Reports/Jobs` e usam a autorização do
mesmo solicitante para o cliente. Use o mesmo modelo, intervalo, fuso e corpo,
inclusive o valor de `includeSpreadsheet`, para localizar a execução.

| Método e caminho | Quando usar |
| --- | --- |
| `POST /{model}/lookup` | Recuperar uma execução existente. HTTP 404 indica que nenhum pedido foi encontrado para esses filtros. |
| `POST /{model}` | Iniciar ou reutilizar uma execução. HTTP 202 devolve o ID e o endereço de status. |
| `GET /{id}?contextId=…` | Ler `Queued`, `Running`, `Completed`, `Failed` ou `Canceled`. |
| `GET /{id}/result?contextId=…` | Após `Completed`, ler o snapshot com o Excel, quando solicitado. |
| `DELETE /{id}?contextId=…` | Cancelar uma execução pendente a pedido do usuário e conferir o estado devolvido. |

Consulte o status em intervalos moderados e respeite `Retry-After`.
No portal, o evento autenticado `TelephonyReportJobChanged` do SignalR avisa
que o status mudou. O evento contém o ID; o resultado continua na API.
Em caso de falha ou cancelamento, informe o estado e a mensagem disponível.
Para refazer um snapshot concluído a pedido do usuário, envie
`POST /{model}?replaceCompleted={id}` com os mesmos filtros. Resultados
concluídos são mantidos por um dia.

### Coluna Tipo em ligações tarifadas

O relatório classifica pelo número em E.164 compacto. Se um resultado antigo
mostrar `UNKNOWN` para destinos fixos e móveis reconhecíveis, gere um snapshot
novo e confira `generatedAt` e a distribuição de `Tipo` no JSON e no XLSX.
`UNKNOWN` pode ser válido para um destino que o classificador não reconhece.

## Diagnóstico proporcional

- **401/403:** diferencie credencial ausente/expirada de permissão por contexto.
  Não altere concessões como parte da geração do relatório.
- **400:** confira modelo, período, segundos, fuso e capacidades de filtro.
- **429:** aguarde o prazo indicado em `Retry-After`.
- **504:** registre o tempo limite e identifique se a resposta veio da API ou
  do gateway. Se o início do job ficou sem resposta, consulte o `lookup`
  antes de iniciar outra geração. Preserve o período e o link original.
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
