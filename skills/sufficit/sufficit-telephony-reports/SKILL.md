---
name: sufficit-telephony-reports
description: "Generate and deliver customer-scoped Sufficit telephony reports through the corporate API, including billed calls, operators, lost calls, hourly traffic and extension usage. Use for relatorio de chamadas tarifadas, exportacao Excel de telefonia, report verification, and reports requested while the legacy website is unavailable. Does not change tariffs, billing or call routing."
metadata:
  version: "1.0.0"
  author: "Sufficit"
---

# Relatórios de telefonia Sufficit

Gere o relatório solicitado pela API, valide o resultado e entregue o arquivo
ou a análise pedida. O motor funciona sem sessão ou processo do site WebForms.
A tela Blazor correspondente é `/pages/reports/telephony`, no cliente selecionado.

## Descoberta e acesso

Prefira as ferramentas conectadas da API. No Genius, descubra operações com
`sufficit_api_search` e execute com `sufficit_api_call`; pesquise também em inglês
(`telephony reports`, `billed calls`, `catalog`). Use o esquema da ferramenta
para os argumentos, sem inventar um nome de tool a partir de uma rota HTTP.

O endereço público é `https://endpoints.sufficit.com.br`. As operações verificadas
são `GET /Telephony/Reports/Catalog` e `POST /Telephony/Reports/{model}`.
Se o ambiente oferece execução HTTP autorizada, use apenas a credencial configurada
para a integração. Nunca imprima tokens nem os inclua em arquivos de relatório.
Não procure credenciais em históricos de outras sessões. Se não houver acesso
configurado, informe o bloqueio de autenticação; não fabrique um resultado.

O catálogo requer autenticação. A geração exige `PhoneCallsEntitlement`
(`phonecalls`) para o `contextId`, ou o acesso de gestor/administrador reconhecido
pela API. Um token válido não comprova autorização para qualquer cliente.
Não conceda entitlements ou roles para fazer um relatório passar.

## Resolver cliente, período e modelo

- Identifique o cliente pelo contexto selecionado ou pela busca autorizada.
  Confirme ambiguidades entre clientes homônimos. Não troque de cliente diante
  de resultado vazio, salvo quando o usuário permitiu escolher qualquer cliente.
- Para um exemplo de cliente livre, prefira um contexto autorizado com atividade
  conhecida. A geração do relatório continua pela API; não transforme uma
  solicitação de relatório em varredura do banco de produção.
- Obtenha o catálogo atual antes de gerar e respeite as capacidades anunciadas.
  A [referência de modelos](references/api-and-diagnostics.md) descreve a versão
  inicialmente validada, mas o catálogo em execução prevalece.
- Use o período pedido e explicite o fuso. Se faltar período e o contexto não
  permitir inferi-lo, pergunte. Para demonstração livre, um dia concluído é um
  padrão razoável: declare essa escolha. Não amplie silenciosamente a consulta.

## Gerar uma consulta completa

O corpo contém `contextId` não vazio, `start`, `end`, `offsetMinutes` e,
quando o usuário precisa do arquivo, `includeSpreadsheet: true`.
As datas ISO 8601 devem conter fuso e precisão de segundos; o fim é inclusivo.
Por exemplo, um dia em UTC-03 vai de `00:00:00-03:00` a `23:59:59-03:00`,
com `offsetMinutes: -180`. Não aplique a conversão de fuso duas vezes.
Colunas explicitamente marcadas UTC permanecem UTC, mesmo nesse relatório.

Não envie DIDs, texto ou descarte para modelos que não aceitam esses filtros.
Permita o tempo de geração: a versão validada tem timeout de 180 segundos;
clientes HTTP devem comportá-lo (por exemplo, 200 segundos).
A requisição é síncrona, cancelável e devolve um snapshot; não há job público
para polling, identificador de download ou dependência de afinidade entre hosts.

A resposta deve ser sucesso HTTP e um contrato de resultado válido. Confira
`schemaVersion`, `model`, `contextId`, intervalo e fuso contra a solicitação.
Ausência de resposta, timeout ou erro não significa zero chamadas. HTTP 429
pede respeito a `Retry-After`; não dispare várias gerações paralelas para contornar
limites. Não repita uma falha determinística sem corrigir sua causa.

## Validar e entregar

1. Confira `columns`, `rows`, `totals`, `notes` e `generatedAt`. As linhas seguem
   a ordem das colunas; identificadores e números telefônicos continuam texto.
   Some valores financeiros com decimal, nunca arredondando cada linha para
   centavos antes da soma. Some apenas colunas aditivas, não médias/percentuais.
2. Preserve avisos de tarifação pendente. Resultado sem linhas deve ser descrito
   como vazio para aquele cliente/período, não como falha nem como prova de que
   não houve chamadas de qualquer tipo.
3. Para Excel, decodifique `spreadsheetBase64` da mesma resposta. Ele é conteúdo
   base64, não uma URL. Verifique que o arquivo é um XLSX/ZIP válido, contém as
   planilhas de dados e `Resumo`, e que cliente, período, linhas e totais conferem
   com o JSON. Não gere uma segunda consulta só para exportar o mesmo snapshot.
4. Salve em diretório privado de artefatos, fora dos arquivos versionados. Entregue
   um link que a interface realmente consiga abrir, com cliente, período, fuso,
   contagem e totais relevantes. Um caminho no servidor não é automaticamente um
   anexo ou URL pública; use o mecanismo de anexos disponível ou um caminho local
   absoluto clicável quando essa for a interface suportada.
5. Se produzir CSV a partir do JSON, identifique-o como conversão local. A API
   validada oferece JSON e XLSX, sem PDF ou rota CSV anunciada.

Enviar aqui ao solicitante não autoriza enviar ao cliente por WhatsApp, e-mail
ou Chatwoot. Mensagens externas exigem instrução específica. Não inclua dados
reais de chamadas, tokens ou IDs de clientes em exemplos públicos desta skill.

## Falhas e comprovação

Para falhas de geração/exportação, leia o
[diagnóstico de API e Excel](references/api-and-diagnostics.md).
Uma consulta JSON bem-sucedida não comprova que Excel funciona. Health saudável,
commit ou push não comprovam instalação nem funcionamento da tela Blazor.
Distinga o relatório realmente gerado, a exportação validada e o estado de deploy.
