---
name: asaas-invoices
description: Emite e consulta notas fiscais de serviço (NFS-e) da conta de produção do ASAAS pelas ferramentas asaas_invoices_list, asaas_services_list e asaas_invoices_create do Sufficit AI Genius. Toda emissão é vinculada a um serviço JÁ EXISTENTE — emitir nota nunca cria serviço; criar serviço só a pedido explícito do usuário, e pelo painel, porque a API não oferece esse caminho. Consultar antes de escrever, sempre confirmar com o usuário.
---

# Notas fiscais de serviço ASAAS de produção

Use esta orientação quando o usuário pedir para emitir, agendar, ver ou
conferir notas fiscais (NFS-e) no ASAAS.

## Credencial

- As ferramentas resolvem sozinhas a chave em `personal/asaas/production/api-key`
  no Vault pessoal do Sufficit Identity.
- Nunca peça a chave na conversa e nunca a inclua em argumentos, comandos ou
  arquivos. Falhas `asaas_key_missing` e `asaas_vault_sign_in_required` seguem
  o mesmo fluxo das demais skills do ASAAS (tela segura de Vault).

## Regra de ouro: a nota nasce vinculada a um serviço existente

Uma nota fiscal de serviço **precisa** de um serviço. **Emitir nota nunca cria
serviço**: a emissão sempre se vincula a um serviço que já existe na conta —
jamais invente um serviço, jamais crie um como efeito colateral de um pedido
de nota. Criar um serviço novo é um ato separado, que só acontece quando o
usuário **pede isso explicitamente** (ver "Quando o usuário pede um serviço
novo"). Antes de qualquer emissão:

1. **Descubra o serviço padrão da conta**: consulte o histórico com
   `asaas_invoices_list` e veja qual `serviceDescription` a conta costuma
   emitir. Essa é a primeira pista do serviço padrão.
2. **Confirme no catálogo municipal**: use `asaas_services_list` (com filtro
   `description`, ex.: "1.01" ou "sistemas") para achar o serviço existente e
   seu `id`.
3. **Escolha com o usuário**: apresente o serviço encontrado (ou o padrão do
   histórico) e confirme. Se o usuário não disse nada sobre serviço,
   **pergunte** — nunca escolha sozinho na primeira vez, nunca invente código.
4. **Portal Nacional**: se o catálogo municipal não estiver disponível para a
   conta, o código do serviço vem do usuário (contabilidade/Portal Nacional).
   Nesse caso use `municipalServiceCode` informado por ele — e só por ele.

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
3. **Serviço obrigatório e existente**: `municipalServiceId` do catálogo OU
   `municipalServiceCode` dado pelo usuário — exatamente um, nunca ambos.
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
lembra: **emitir nota nunca cria serviço**. Use para escolher o serviço certo;
contas do Portal Nacional não têm lista e o código vem do usuário. Contrato em
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
- Não há cancelamento, atualização ou antecipação de nota por aqui. Se o
  usuário pedir, explique o limite e ofereça o painel.
- Impostos (`taxes`) seguem a configuração da conta; a ferramenta não envia
  alíquotas próprias.

## Quando a ferramenta não existe

Se as ferramentas de nota não estiverem disponíveis, o plugin ASAAS está
desabilitado ou esta versão do Genius ainda não as oferece. Oriente ativar o
plugin ou atualizar o aplicativo. Não contorne chamando a API por shell ou
script: a chave de produção não pode transitar pelo prompt.
