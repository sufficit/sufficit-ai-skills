# Período da última recarga no relatório de ligações tarifadas

A skill `sufficit-telephony-reports` 1.3.0 prioriza o link autenticado com
empresa e período já confirmados na conversa. Quando o pedido é verificar
consumo antes de nova recarga de tarifado ou 0800, sem outro período explícito,
o início vem do último crédito efetivado e o fim é o momento da consulta.

O histórico autorizado `GET /Telephony/Billing/Recharges` retorna compras de
créditos do cliente com `timestamp` UTC. A orientação respeita essa abrangência:
pedidos relativos a um 0800 específico precisam de evidência que identifique o
serviço. O relatório `billed-calls` não aceita filtro por DID. Datas e horários
são convertidos para o fuso do relatório, com Brasília como padrão. Quando o
período supera 31 dias, os links cobrem a vigência em trechos consecutivos.

O contrato foi conferido no controlador e no histórico de recargas da API,
no guia de relatórios e na montagem do link no Blazor. Um caso sintético
verificou a exclusão de uma recarga futura, a conversão UTC que atravessa
a meia-noite e a divisão do intervalo longo. Os dois links direcionaram
ao login em produção. Não houve consulta autenticada a dados de cliente.

Foram aprovados o validador dos 195 pacotes, índice e versões do catálogo,
cobertura Markdown, os 70 testes do repositório e `git diff --check`.
O commit da skill habilita a sincronização automática do catálogo. A publicação
e o uso em sessões com uma versão já instalada exigem verificação própria.
