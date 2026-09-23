---
name: asaas-invoices
description: Consulta e agenda NFS-e de produção do ASAAS com asaas_invoices_list, asaas_services_list e asaas_invoices_create; cancelamento com asaas_invoices_cancel somente se disponível. Consulte documentação oficial para os campos fiscais, diferencie descrição da nota de código municipal, não invente serviço nem prometa preenchimento automático não comprovado. Consulte antes de escrever e obtenha aprovação.
---

# Notas fiscais de serviço ASAAS de produção

Use esta orientação quando o usuário pedir para emitir, agendar, ver,
conferir ou cancelar notas fiscais (NFS-e) no ASAAS. Fale com o usuário em
termos leigos; procure cadastro e configuração com ferramentas de leitura,
sem solicitar IDs/códigos que pode obter por conta própria.

## Fonte oficial e atualização

- Índice completo, inclusive alterações futuras: [documentação oficial da API
  Asaas](https://docs.asaas.com/llms.txt).
- Fluxo fiscal: [Introdução — Notas Fiscais](https://docs.asaas.com/docs/notas-fiscais)
  e [Emitindo NFS-e](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico).
- Contratos do [agendamento (`POST /v3/invoices`)](https://docs.asaas.com/reference/agendar-nota-fiscal),
  [listagem de notas](https://docs.asaas.com/reference/listar-notas-fiscais)
  e [cancelamento](https://docs.asaas.com/reference/cancelar-uma-nota-fiscal).
- A documentação evolui: antes de concluir que um campo é obrigatório ou
  presumir um padrão da conta, verifique o guia **e** o schema/erros do endpoint.
  Havendo divergência, limite da ferramenta, mudança de contrato, recusa da
  prefeitura ou informação fiscal ausente, diga ao usuário o que foi ou não
  feito, com o motivo, e reporte à equipe responsável pelo plugin/skill para
  atualização. Nunca exponha a chave, CPF integral nem dados sensíveis no
  relato; não contorne o plugin por requisição manual.

## Credencial

- As ferramentas resolvem sozinhas a chave em `personal/asaas/production/api-key`
  no Vault pessoal do Sufficit Identity.
- Nunca peça a chave na conversa e nunca a inclua em argumentos, comandos ou
  arquivos. Falhas `asaas_key_missing` e `asaas_vault_sign_in_required` seguem
  o mesmo fluxo das demais skills do ASAAS (tela segura de Vault).

## Serviço cadastrado versus descrição da nota

Há duas informações diferentes: `serviceDescription` é a **descrição impressa
na nota**; `municipalServiceId`/`municipalServiceCode` identificam o
**enquadramento municipal**. A primeira não vira automaticamente a segunda.

O [guia oficial](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico)
e a [referência do agendamento](https://docs.asaas.com/reference/agendar-nota-fiscal)
orientam enviar o `municipalServiceId` da lista municipal **ou** o
`municipalServiceCode` validado com prefeitura/contabilidade (Portal Nacional:
código). No OpenAPI, nenhum dos dois consta da lista `required` do schema,
mas **isso não prova preenchimento automático** quando ambos são omitidos.
O schema marca `serviceDescription` como obrigatório; só documenta fallback
de `municipalServiceName` para `municipalServiceCode` quando o nome é omitido.
A emissão automática de **assinaturas** é outro fluxo, configurado por
assinatura: não implica default para uma nota avulsa.

O usuário informa que, **na sua conta**, dados fiscais e serviços já estão
cadastrados no painel (Notas Fiscais › Configurações › Serviços). A ferramenta
atual deixa os campos municipais fora do POST por padrão: é uma **regra
operacional da conta, ainda não garantida pela documentação da API**. Não
chame isso de garantia do Asaas. Não invente código, ISS, alíquota nem
serviço; não crie novo cadastro como efeito colateral. Se a API recusar,
apresente a mensagem real e reporte a divergência à equipe para atualização.

Para não sobrecarregar o usuário leigo: consulte o histórico de notas e o
cadastro já disponível. Se houver **uma descrição inequívoca e pertinente**
à prestação atual, apresente-a ao usuário como proposta para a nota, com
valor, destinatário e data, e peça confirmação **antes** do card de escrita.
Uma descrição de cliente/serviço anterior é apenas referência: não prova que
o mesmo serviço foi prestado agora. Se houver opções ou não houver evidência,
pergunte *qual foi o serviço prestado*, sem pedir código técnico. Não use
"serviço de teste" como descrição fictícia de operação fiscal real.

Se o usuário escolher expressamente um serviço municipal específico,
`municipalServiceId` (se disponível) **ou** `municipalServiceCode` (código
validado), nunca ambos. Cadastro novo só em pedido explícito do usuário.

## Consulta de notas

`asaas_invoices_list` executa um `GET` fixo em `/v3/invoices` com filtros
opcionais (cliente, cobrança, status, período) e paginação. Somente leitura.
Cada nota já chega com **quem a recebeu**: o campo `customer` traz o cliente
resolvido (`id`, `name`, `personType`, `document` — CNPJ completo e formatado,
CPF nos 3 primeiros dígitos); se um cliente não pôde ser resolvido, o id vem
solto na nota e listado em `unresolvedCustomerIds`, com orientação para
consultar `asaas_customers_list` antes de afirmar quem recebeu.
Traduza status para linguagem simples: SCHEDULED = agendada, SYNCHRONIZED =
enviada à prefeitura, AUTHORIZED = emitida, CANCELED = cancelada, ERROR =
falhou. Contrato completo em
[references/invoices-list.md](references/invoices-list.md).

## Emissão de nota nova — consultar antes de escrever

Só emita quando o usuário **pedir explicitamente** a nota. A ferramenta
`asaas_invoices_create` agenda a NFS-e e protege a conta em código:

1. **Origem exatamente uma**: cobrança (`payment`), parcelamento
   (`installment`) ou cliente (`customer`, nota avulsa). Se o usuário falou de
   uma cobrança, descubra o `pay_...` antes; de um cliente, o `cus_...`.
2. **Deduplicação automática**: cobrança que já tem nota recusa sempre; mesma
   combinação de cliente + valor + data recusa até o usuário confirmar
   (`confirmedDistinct`). Recusa não é erro — apresente a nota existente.
3. **Serviço municipal: omitido por padrão**. A ferramenta não envia
   `municipalServiceId` nem `municipalServiceCode` — regra operacional desta
   conta (ver "Serviço cadastrado versus descrição da nota"). Só envie um
   deles (nunca os dois) quando o usuário escolher explicitamente um serviço
   específico para aquela nota. Se o provedor recusar a nota por falta de
   serviço, apresente o motivo real ao usuário, reporte a divergência à
   equipe e nunca adivinhe código.
4. **Aprovação explícita**: a emissão é escrita real na produção e mostra card
   de aprovação na conversa.
5. **Honestidade sobre o processamento**: agendar inicia o fluxo, mas a
   autorização pela prefeitura é assíncrona. Diga "nota agendada, a emissão
   foi para processamento" — nunca prometa autorização imediata. Para
   confirmar depois, consulte pelo id e veja o status.

Detalhes completos: [references/invoices-create.md](references/invoices-create.md).

## Consulta de serviços municipais

`asaas_services_list` lê o catálogo de serviços da conta
(`GET /v3/fiscalInfo/services`) com filtro opcional de descrição. O resultado
lembra: **emitir nota nunca cria serviço**. Use para **conferir e conversar**
sobre os serviços cadastrados (inclusive achar duplicatas) — não para
preencher campo de emissão por conta própria. Contas do Portal Nacional não
recebem a lista pela API; nesses casos a orientação oficial é obter e validar
o código do serviço com o Portal Nacional ou a contabilidade antes de usá-lo.
A ausência da lista não é falha sua e não autoriza adivinhar código. Contrato em
[references/services-list.md](references/services-list.md).

## Quando o usuário pede um serviço novo

Se — e somente se — o usuário pedir **explicitamente** para cadastrar um
serviço novo ("cadastra um serviço", "cria o serviço X"), trate como pedido
legítimo, não como desvio. Mas a API pública do ASAAS **não oferece** criação,
edição ou exclusão de serviço: o único endpoint fiscal de serviços é a
listagem. Então:

1. Não recuse o pedido como se fosse proibido — é permitido, só não é
   automatizável pela API.
2. Oriente o caminho real: painel do ASAAS em **Notas Fiscais › Configurações
   › Serviços › Adicionar Serviço** (código municipal, ISS e descrição).
3. Ofereça ajuda no que é automatizável: listar os serviços já cadastrados
   para conferir se o desejado já existe (evita duplicatas, comuns nessa tela)
   e, depois que o usuário cadastrar, usar o serviço na emissão.

Nunca invente um endpoint de criação nem finja ter criado um serviço.

## Limites honestos

- A resposta nunca traz PDF/XML nem código de verificação; para o documento
  em si, oriente o painel do ASAAS.
- Não há atualização nem antecipação de nota por aqui. Para esses casos,
  oriente o painel do ASAAS.
- Cancelamento: se a ferramenta `asaas_invoices_cancel` existir nesta versão
  do plugin, ela consulta a nota antes, exige aprovação explícita e reporta o
  status real — `PROCESSING_CANCELLATION` **não** é cancelada, e a prefeitura
  pode negar (`CANCELLATION_DENIED`). Contrato em
  [references/invoices-cancel.md](references/invoices-cancel.md). Sem a
  ferramenta, explique o limite e ofereça o painel.
- Impostos (`taxes`) seguem a configuração da conta; a ferramenta não envia
  alíquotas próprias.

## Quando a ferramenta não existe

Se as ferramentas de nota não estiverem disponíveis, o plugin ASAAS está
desabilitado ou esta versão do Genius ainda não as oferece. Oriente ativar o
plugin ou atualizar o aplicativo. Não contorne chamando a API por shell ou
script: a chave de produção não pode transitar pelo prompt.
