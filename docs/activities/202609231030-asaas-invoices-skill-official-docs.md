# Skill asaas-invoices 0.5.0 — documentação oficial, descrição vs serviço municipal — 2026-09-23

## Pedido

O usuário reportou, a partir do teste leigo no tablet (pedido de NFS-e de
R$ 1 para Hugo Castro de Deco), que os detalhes de serviço "caso não
especificados, são autopreenchidos", que isso "deve estar na skill", e pediu:
verificar na documentação oficial da API Asaas, deixar o link oficial na
skill para o agente se virar com o usuário final e reportar problemas ou
necessidade de atualização.

## Verificação na documentação oficial (2026-09-23)

Páginas consultadas: [guia de emissão](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico),
[referência Agendar nota fiscal](https://docs.asaas.com/reference/agendar-nota-fiscal)
(PT e EN), [FAQ de Notas Fiscais](https://docs.asaas.com/docs/faq-de-notas-fiscais),
[Notas fiscais — introdução](https://docs.asaas.com/docs/notas-fiscais),
[configuração fiscal](https://docs.asaas.com/docs/configurar-informacoes-fiscais),
[assinaturas](https://docs.asaas.com/docs/emitir-notas-fiscais-automaticamente-para-assinaturas),
[Cancelamento](https://docs.asaas.com/reference/cancelar-uma-nota-fiscal) e o
[índice llms.txt](https://docs.asaas.com/llms.txt).

O que a documentação **afirma**:

- A narrativa do guia e da referência pede `municipalServiceId` **ou**
  `municipalServiceCode` ("obrigatório enviar um ou outro"), conforme a
  disponibilidade da lista municipal; Portal Nacional exige código manual.
- No OpenAPI (`InvoiceSaveRequestDTO`), a lista `required` é:
  `serviceDescription, observations, value, deductions, effectiveDate,
  municipalServiceName, taxes` — `municipalServiceId`/`municipalServiceCode`
  **não** aparecem como obrigatórios.
- Único autopreenchimento documentado: `municipalServiceName`, quando omitido,
  usa `municipalServiceCode` como identificação.
- Emissão automática de **assinaturas** é fluxo próprio
  (`invoiceSettings` por assinatura); não é default de nota avulsa.

O que a documentação **não afirma** (limite honesto): que a omissão dos campos
de serviço faz o provedor preencher código/ISS a partir do cadastro de serviços
da conta, nem que `serviceDescription` (obrigatória no schema) seja
preenchida automaticamente. A alegação de autopreenchimento **não pôde ser
confirmada** na documentação. A regra operacional da conta (emitir sem os
campos municipais; recusa tratada com o motivo real do provedor) permanece;
a primeira emissão real confirmará o comportamento em produção.

## Mudanças na skill (0.4.1 → 0.5.0)

- `SKILL.md`: nova seção "Fonte oficial e atualização" com links para
  `llms.txt`, guias e referências (agendamento, listagem, cancelamento) e
  regra de reporte ao time (divergência, limite, mudança de contrato, recusa
  da prefeitura) sem expor dados sensíveis; nova seção "Serviço cadastrado
  versus descrição da nota" separando `serviceDescription` (descrição
  impressa, obrigatória no schema) de `municipalServiceId`/`Code`
  (enquadramento municipal, omitidos por regra da conta), com conduta para
  usuário leigo: propor descrição inequívoca do histórico para confirmação ou
  perguntar "qual foi o serviço prestado" em linguagem simples — nunca pedir
  código; remoção do fragmento solto "na conta."; cancelamento documentado
  como ferramenta existente quando disponível, com status honestos.
- `references/invoices-cancel.md` (novo): contrato de `asaas_invoices_cancel`
  (recusas `already_canceled`, `cancellation_in_progress`,
  `cancellation_denied`, `not_cancellable`; sucesso com
  `cancellationRequested`/`canceled`/`cancellationIsFinal`; eventos oficiais).
- `references/invoices-create.md`, `services-list.md`, `invoices-list.md`:
  mesma separação descrição × enquadramento; nota de honestidade sobre o
  OpenAPI × narrativa; Portal Nacional conforme orientação oficial.
- `release.json` 0.5.0; `skill-card.md` e `agents/openai.yaml` atualizados.
- `catalog/upstream-v2.json`: descrição e `updatedAt`; `catalog/import-manifest.json`:
  `contentSha256` recalculado
  (`856105a8bdf42ffa6382d3bdf067916da8f98f9e200041ae0ae020714a52b741`).

## Compatibilidade com o plugin

- `AsaasPlugin.Tools.Fiscal.cs` mantém `required = [value, serviceDescription,
  effectiveDate]` — coerente com o OpenAPI e com a skill (descrição é campo
  da nota, não código municipal).
- Tool `asaas_invoices_cancel` (WIP no repositório genius) bate com o novo
  `references/invoices-cancel.md` (razões, campos e mensagens).
- Suíte do plugin no genius: 89/89 verde na sessão (build local).

## Validação

- `scripts/validate.py`: "Validated all 159 public skill packages."
- Nenhuma outra skill ou pacote afetado.

## Continuidade

- Para o agente do tablet receber a 0.5.0, o catálogo pinado no repositório
  genius (`scripts/update-skill-catalog.sh`) precisa ser atualizado na
  entrega que também levará `asaas_invoices_cancel` (pending na sessão).
- A emissão real de NFS-e de R$ 1 segue aguardando descrição verdadeira do
  serviço prestado (campo obrigatório do schema e do plugin).
