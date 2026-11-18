# Acesso do cliente ao relatório de ligações tarifadas

O pedido veio de um cliente que recebeu uma planilha com acesso restrito.
A skill `sufficit-telephony-reports` 1.2.0 passou a orientar o Genius a indicar
o [relatório de ligações tarifadas no portal](https://blazor.sufficit.com.br/pages/reports/telephony?model=billed-calls)
quando o objetivo é a consulta pelo cliente. A instrução inclui seleção da
empresa, período e carregamento, com personalização do link quando o contexto
e o período forem conhecidos. A exportação continua disponível sob pedido.

A URL em produção respondeu HTTP 302 para o login da Sufficit. O filtro
`model=billed-calls` e os parâmetros de contexto e período foram conferidos
no código do Blazor e no teste que documenta a montagem do link. A consulta com
a conta do cliente ficou fora da validação e depende do acesso dessa conta
à empresa.

Foram aprovados o validador dos 195 pacotes, os checks de índice, versões e
cobertura Markdown, os 70 testes do repositório e `git diff --check`.
A versão e o digest do pacote foram atualizados no catálogo. A adoção em
sessões com uma cópia instalada do Genius depende da atualização dessa cópia.
