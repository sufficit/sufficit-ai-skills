---
name: asaas-invoices
description: Emite e consulta notas fiscais de serviço (NFS-e) da conta de produção do ASAAS pelas ferramentas asaas_invoices_list, asaas_services_list e asaas_invoices_create do Sufficit AI Genius. Ao emitir NÃO especifique o serviço — código municipal e ISS vêm do cadastro de serviços da conta; nunca peça código ao usuário só para emitir. Emitir nota nunca cria serviço; criar serviço só a pedido explícito do usuário, e pelo painel, porque a API não oferece esse caminho. Consultar antes de escrever, sempre confirmar com o usuário.
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

## Regra de ouro: o serviço vem do cadastro da conta, não da emissão

Dados fiscais — código municipal do serviço, alíquota de ISS, descrição
padrão — moram no **cadastro de serviços da conta** (no painel: Notas Fiscais
› Configurações › Serviços). A emissão apenas **usa** esse cadastro.

Por isso, ao emitir: **não especifique o serviço**. O contrato do provedor
(`InvoiceSaveRequestDTO`) **não exige** `municipalServiceId` nem
`municipalServiceCode`; omitindo os dois, o ASAAS aplica o serviço cadastrado
na conta. Consequências práticas:

- **Nunca peça um código de serviço ao usuário só para emitir uma nota.** Se
  você se pegou perguntando "qual o código municipal?", parou de seguir o
  cadastro da conta.
- **Nunca invente código.** Se o usuário não escolheu serviço, não envie
  nenhum dos dois campos.
- **Só envie o serviço quando o usuário escolher um específico**, dizendo
  explicitamente que aquela nota sai com outro serviço. Aí use
  `municipalServiceId` (do `asaas_services_list`) **ou**
  `municipalServiceCode` (o que o usuário informou) — nunca os dois juntos.
- **Emitir nota nunca cria serviço.** Criar é ato separado, só a pedido
  explícito (ver "Quando o usuário pede um serviço novo").

O histórico (`asaas_invoices_list`) e o catálogo (`asaas_services_list`)
servem para **conferir e conversar** sobre qual serviço a conta costuma usar —
não para preencher campo de emissão por conta própria.

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
3. **Serviço: não especifique**. Omita `municipalServiceId` e
   `municipalServiceCode` para que o serviço cadastrado na conta seja
   aplicado. Só envie um deles (nunca os dois) quando o usuário escolher
   explicitamente um serviço específico para aquela nota.
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
preencher campo de emissão: a nota sai sem serviço especificado. Contas do
Portal Nacional não recebem a lista, e isso **não impede emitir**: o cadastro
da conta continua valendo. Contrato em
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
