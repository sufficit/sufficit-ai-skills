---
name: asaas-invoices
description: Consulta e agenda NFS-e de produção do ASAAS com asaas_invoices_list, asaas_services_list e asaas_invoices_create; cancelamento com asaas_invoices_cancel quando disponível. Detalhes do serviço (código municipal, ISS, nome fiscal) são auto preenchidos pelo cadastro da conta quando não especificados: nunca peça código municipal ao usuário e nunca invente código; a descrição impressa da nota é campo próprio e vem do usuário. Documentação oficial linkada na seção Fonte oficial: verifique-a antes de presumir obrigação e reporte divergências/recusas à equipe. Consulte antes de escrever e obtenha aprovação.
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

**Regra desta conta, combinada com o dono: os detalhes do serviço — código
municipal, ISS e nome fiscal — são auto preenchidos a partir do cadastro de
serviços da conta (painel: Notas Fiscais › Configurações › Serviços) sempre
que a emissão não os especificar.** Por isso a ferramenta omite
`municipalServiceId` e `municipalServiceCode` por padrão, o agente nunca
pede código municipal ao usuário e nenhum código, ISS ou alíquota é
inventado; emitir nota nunca cria serviço nem cadastro novo.

O que a documentação oficial sustenta (checada em 2026-09-23):

- O schema do [agendamento](https://docs.asaas.com/reference/agendar-nota-fiscal)
  **não** lista `municipalServiceId` nem `municipalServiceCode` como
  obrigatórios: omiti-los é aceito pelo contrato. O mesmo schema marca
  `taxes`, `observations` e `deductions` como obrigatórios — e a conta emite
  sem enviá-los, preenchidos pela configuração fiscal do cadastro.
- Preenchimentos automáticos declarados no schema: `municipalServiceName`
  usa `municipalServiceCode` quando o nome não é informado; e
  `pisCofinsRetentionType` é calculado pelo Asaas (não envie).
- A narrativa do [guia](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico),
  escrita para integrações genéricas, pede `municipalServiceId` **ou**
  `municipalServiceCode` (Portal Nacional: código) — ela não descreve o auto
  preenchimento pelo cadastro da conta. O schema valida a omissão; o
  comportamento da conta é a regra operacional. A emissão automática de
  **assinaturas** é outro fluxo, configurado por assinatura.

Se o provedor recusar a nota por serviço ou imposto, a recusa traz o motivo
dele: apresente-o ao usuário em linguagem clara, **reporte à equipe
responsável pelo plugin/skill** (com o link e a data da checagem, para
atualizar esta regra) e nunca preencha às cegas.

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
3. **Serviço municipal: omitido por padrão — auto preenchido pela conta**.
   A ferramenta não envia `municipalServiceId` nem `municipalServiceCode`:
   os detalhes (código municipal, ISS, nome fiscal) vêm do cadastro de
   serviços da conta (ver "Serviço cadastrado versus descrição da nota").
   Só envie um deles (nunca os dois) quando o usuário escolher
   explicitamente um serviço específico para aquela nota. Se o provedor
   recusar a nota por falta de serviço, apresente o motivo real
   ao usuário, reporte a divergência à equipe e nunca adivinhe código.
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
