# Cancelamento de nota fiscal ASAAS

A ferramenta `asaas_invoices_cancel` solicita o cancelamento de uma NFS-e na
conta de produção via `POST /v3/invoices/{id}/cancel`
([referência oficial](https://docs.asaas.com/reference/cancelar-uma-nota-fiscal)).
Ela só cancela: nunca emite e nunca altera dados da nota.

## Pré-requisitos (nesta ordem)

1. O usuário pediu **explicitamente** cancelar (cancelar, anular, desfazer).
2. O alvo é um id `inv_...` obtido de `asaas_invoices_list` — nunca um número
   lido no papel da nota, nunca um palpite.
3. A ferramenta consulta a nota **antes** de escrever: recusa quando não há
   nada a cancelar, e o card de aprovação mostra o que será cancelado.
4. Aprovação explícita na conversa: o cancelamento é **irreversível**.

## Argumentos

| Argumento | Tipo | Obrigatório | Regras |
| --- | --- | --- | --- |
| `invoice` | string | sim | Id ASAAS da nota (`inv_...`), conforme `asaas_invoices_list`. |

## Recusas (escrita não realizada)

`canceled: false` com `writesPerformed: false` é recusa, não erro. Nenhum
POST aconteceu.

| `reason` | Causa | Conduta |
| --- | --- | --- |
| `already_canceled` | A nota já está cancelada. | Informe o usuário; nada a fazer. |
| `cancellation_in_progress` | Cancelamento já está em processamento. | Aguarde o resultado; não repita. |
| `cancellation_denied` | A prefeitura já negou este cancelamento. | Explique que resolver depende da prefeitura. |
| `not_cancellable` | Estado não permite cancelar (ex.: `ERROR`). | Informe o status real ao usuário. |

## Resultado de sucesso

| Campo | Valor |
| --- | --- |
| `cancellationRequested` | `true` — o pedido foi aceito pelo ASAAS. |
| `canceled` | `true` **somente** se o status retornado for `CANCELED`. |
| `cancellationIsFinal` | `true` só com `CANCELED`. |
| `cancellationIsAsync` | `true` quando ainda não é final. |
| `previousStatus` | Status da nota antes do pedido. |
| `invoice` | Projeção sanitizada da nota (sem URLs/código de verificação). |

**Honestidade obrigatória**: `PROCESSING_CANCELLATION` significa "pedido
aceito, prefeitura processando" — não diga que a nota foi cancelada. A
prefeitura pode negar (`CANCELLATION_DENIED`) e nem todo município permite
cancelamento automático pela integração (opção `supportsCancellation` nas
configurações municipais). Eventos oficiais do fluxo:
`INVOICE_PROCESSING_CANCELLATION`, `INVOICE_CANCELED`,
`INVOICE_CANCELLATION_DENIED`. Para confirmar depois, consulte a nota e
reporte o status real.

## Códigos de falha

| Código | Ação |
| --- | --- |
| `asaas_invoices_cancel_invalid_arguments` | Id ausente/inválido; nada foi chamado. |
| `asaas_invoices_cancel_not_found` | Id não existe: liste as notas (`asaas_invoices_list`) e use o id retornado. |
| `asaas_invoices_cancel_rejected` | Provedor recusou (mensagem traz código+descrição). |
| `asaas_invoices_cancel_unexpected` | Resposta em formato estranho: consulte a nota antes de repetir. |
| `asaas_timeout` | **Consulte a nota antes de repetir.** |
| Demais (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_provider_unavailable`, `asaas_transport_failed`) | Fluxo padrão das skills ASAAS. |
