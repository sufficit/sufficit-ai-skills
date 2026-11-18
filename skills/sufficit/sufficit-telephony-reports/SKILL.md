---
name: sufficit-telephony-reports
description: "Direct customers to Sufficit portal telephony reports with customer and period prefilled, and generate reports through the corporate API. Use for ligacoes tarifadas, gasto desde a ultima recarga de tarifado ou 0800, restricted report spreadsheets, and Excel exports."
metadata:
  version: "1.4.0"
  author: "Sufficit"
---

# Relatórios de telefonia Sufficit

## Acesso do cliente pelo portal

Quando o pedido é dar ao cliente acesso a ligações tarifadas, indique o
[Relatório de ligações tarifadas no portal Sufficit](https://blazor.sufficit.com.br/pages/reports/telephony?model=billed-calls).
Use esse link também quando o gestor já enviou uma planilha e o cliente recebe
um pedido de autorização ao abrir o arquivo.

Use os dados já confirmados na conversa. Envie de preferência o link com
`contextid` e o período preenchidos. Se já houver um cliente selecionado,
reaproveite esse contexto. Se houver apenas o nome da empresa, descubra a
consulta autorizada de clientes em `/Sales/Clients` e resolva seu `contextid`.
Peça uma identificação reconhecível somente se houver ambiguidade entre
clientes. Aproveite os filtros confirmados mesmo quando faltar outro campo.

O cliente entra com a conta Sufficit. Com `load=true`, o portal abre a consulta
automaticamente após confirmar o contexto. Para refazer um resultado já exibido,
clique em **Carregar relatório**. Se o link estiver incompleto, indique quais
campos o cliente precisa escolher antes de carregar.
Se o próprio portal indicar erro de autorização, confira o contexto e o acesso
`phonecalls` com o gestor responsável. Alterar o compartilhamento de uma
planilha ou gerar outro arquivo exige pedido específico.

### Consumo antes de uma nova recarga

Preserve o período explícito já informado. Se o cliente pedir os gastos antes
de uma nova recarga de tarifado ou 0800 e nenhum outro período tiver sido
combinado, use a última recarga efetivada até o momento da consulta.

1. Reaproveite o registro da última recarga quando a conversa já confirmar
   a empresa e o instante do crédito. Se faltar essa informação, descubra
   `GET /Telephony/Billing/Recharges` com `sufficit_api_search` e consulte
   o histórico autorizado para o `contextId` com `sufficit_api_call`.
2. Use o `timestamp` da compra de crédito mais recente efetivada até a hora
   atual para aquele contexto. Desconsidere recargas futuras ou pendentes,
   a validade do crédito e as datas da fatura ou do pagamento. O histórico
   retorna compras de crédito do cliente. Use evidência de serviço quando
   houver mais de um ciclo aplicável ou quando o pedido exigir isolar um 0800.
   O modelo `billed-calls` cobre o cliente e não aceita filtro por DID.
3. Se o histórico não estiver disponível ou não confirmar a última recarga,
   explique a lacuna e use o link com o contexto conhecido. Peça apenas a
   informação que faltar para preencher o período com segurança.

### Montar o link

Use `model=billed-calls`, `contextid`, `start` e `end` (datas `yyyy-MM-dd`),
`starttime` e `endtime` (`HH:mm:ss`) e `offset` (minutos). No intervalo de
recarga, converta o horário UTC do crédito e o instante atual para o fuso do
relatório antes de preencher datas e horários. Use Brasília (`offset=-180`)
quando nenhum outro fuso tiver sido informado. Preserve a hora efetiva da
recarga e informe o período e o fuso junto ao link. O fim é inclusivo.
Inclua `load=true` quando modelo, cliente e datas estiverem confirmados. Com
datas completas, o portal usa `00:00:00` e `23:59:59` se as horas forem omitidas.

Exemplo com contexto fictício para um mês completo:

```text
https://blazor.sufficit.com.br/pages/reports/telephony?model=billed-calls&contextid=11111111-1111-1111-1111-111111111111&start=2026-10-01&end=2026-10-31&offset=-180&load=true
```

Use um link por período solicitado, mesmo para vigências longas. Os modelos
de relatório aceitam o intervalo completo. O limite de datas do histórico de
chamadas pertence àquela página. Em caso de HTTP 504, preserve o período
original e consulte o diagnóstico da API antes de tentar novamente.

## Geração e exportação por solicitação

Gere o relatório solicitado pela API, valide o resultado e entregue o arquivo
ou a análise pedida. O motor funciona sem sessão ou processo do site WebForms.

## Descoberta e acesso

Prefira as ferramentas conectadas da API. No Genius, descubra operações com
`sufficit_api_search` e execute com `sufficit_api_call`; pesquise também em inglês
(`telephony reports`, `billed calls`, `catalog`). Use o esquema da ferramenta
para os argumentos, sem inventar um nome de tool a partir de uma rota HTTP.

O endereço público é `https://endpoints.sufficit.com.br`. As operações verificadas
incluem `GET /Telephony/Reports/Catalog`, a fila `/Telephony/Reports/Jobs` e a
geração síncrona em `POST /Telephony/Reports/{model}`.
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

Envie somente os filtros que o modelo oferece. Quando o catálogo retornar
`supportsBackgroundJobs: true` e as operações estiverem disponíveis, prefira a
fila para gerar e acompanhar o relatório pelo ID. Reaproveite a execução
existente com os mesmos filtros, inclusive após interrupção do acompanhamento.
Leia o [contrato da fila](references/api-and-diagnostics.md#geração-em-segundo-plano)
para consultar o estado, obter o resultado ou pedir uma nova geração.

A rota síncrona devolve o mesmo contrato de resultado. Use-a quando a fila
não estiver disponível e não houver execução já aceita. Configure o cliente
HTTP para comportar a espera da API (por exemplo, 200 segundos para o prazo
de geração de 180 segundos).

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

## Talk to Sufficit

Report to Sufficit, as a support thread, what still fails after reading the state and retrying once, a capability you
need that is missing, or a question the API cannot answer: `POST /Support/Threads` with the same credential, `source:
"skill:sufficit-telephony-reports"`. Once per session, also read the threads waiting for the company
(`GET /Support/Threads?contextId={contextId}&waitingFor=customer`) and act on them within this skill's rules. Full
contract: skill [`sufficit-support`](https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/sufficit/sufficit-support).
