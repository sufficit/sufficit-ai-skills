# Período dos relatórios de telefonia

A skill `sufficit-telephony-reports` 1.3.1 orienta o Genius a incluir o período
completo em cada link de relatório, inclusive vigências longas. O catálogo da
API em produção informou `maximumHours: 0` para os nove modelos. O histórico de
chamadas mantém seu próprio limite. HTTP 504 indica tempo limite de processamento
ou comunicação e não muda o intervalo originalmente solicitado.

O validador dos 195 pacotes, a verificação de índices e versões, a cobertura
Markdown, os 70 testes e `git diff --check` passaram. A publicação no catálogo
do Genius ocorre por sincronização separada.
