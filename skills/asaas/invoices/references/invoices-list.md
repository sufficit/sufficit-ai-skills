# Lista de notas fiscais ASAAS

A ferramenta `asaas_invoices_list` consulta `/v3/invoices` na conta de
produção, injetando a chave `personal/asaas/production/api-key` apenas no
cabeçalho `access_token`. É somente leitura (`writesPerformed: false`). A
projeção **nunca** inclui `pdfUrl`, `xmlUrl` ou `validationCode` — para o
documento emitido, oriente o painel do ASAAS.

## Argumentos

| Argumento | Tipo | Padrão | Regras |
| --- | --- | --- | --- |
| `customer` | string | (nenhum) | Filtra pelo id do cliente (`cus_...`); até 64 caracteres. |
| `payment` | string | (nenhum) | Filtra pelo id da cobrança (`pay_...`). |
| `status` | string | (nenhum) | Um entre SCHEDULED, SYNCHRONIZED, AUTHORIZED, PROCESSING_CANCELLATION, CANCELED, CANCELLATION_DENIED, ERROR. |
| `effectiveDateGe` | string | (nenhum) | Início do período de emissão (AAAA-MM-DD). |
| `effectiveDateLe` | string | (nenhum) | Fim do período de emissão (AAAA-MM-DD). |
| `limit` | inteiro | `10` | Entre 1 e 30. |
| `offset` | inteiro | `0` | Não negativo. |

## Resultado de sucesso

`provider: "asaas"`, `environment: "production"`, `query` (o pedido e
`returned`), `totalCount`, `hasNext`, `invoices[]`, `writesPerformed: false`.

Cada nota traz: `id`, `status`, `statusDescription`, `type`, `number`,
`serviceDescription` (até 200 caracteres), `value`, `deductions`,
`effectiveDate`, `observations`, `customer`, `payment`, `installment`.

O campo `customer` traz o cliente **resolvido** pela ferramenta (uma leitura
extra por id distinto de cliente, no máximo 30 por página): um objeto com
`id`, `name`, `personType` e `document` — CNPJ completo e formatado
(registro público), CPF limitado aos 3 primeiros dígitos. Quando a resolução
não é possível (cliente removido, falha de leitura), a nota traz o id solto
do provedor e o id aparece em `unresolvedCustomerIds`, acompanhado de
`guidance` apontando para `asaas_customers_list`. Nunca afirme para quem a
nota foi emitida a partir de um id não resolvido.

## Leitura de status para o usuário

| Status | Linguagem simples |
| --- | --- |
| `SCHEDULED` | Agendada — vai ser emitida na data prevista. |
| `SYNCHRONIZED` | Enviada à prefeitura, aguardando autorização. |
| `AUTHORIZED` | Emitida (autorizada). |
| `PROCESSING_CANCELLATION` | Cancelamento em processamento. |
| `CANCELED` | Cancelada. |
| `CANCELLATION_DENIED` | Cancelamento negado pela prefeitura. |
| `ERROR` | Falhou a emissão. |

## Códigos de falha

| Código | Ação |
| --- | --- |
| `asaas_invoices_invalid_arguments` | Corrija filtros (status permitido, datas AAAA-MM-DD); nada foi chamado. |
| `asaas_invoices_unexpected` | Resposta fora do formato; informe o usuário e tente uma vez. |
| `asaas_vault_sign_in_required` / `asaas_key_missing` / `asaas_key_invalid` / `asaas_credential_rejected` | Fluxo de credencial padrão das skills ASAAS. |
| `asaas_provider_unavailable` / `asaas_transport_failed` / `asaas_timeout` / `asaas_vault_*` | Repita conforme marcado repetível. |

## Uso para descobrir o serviço padrão

Sem filtros, a primeira página mostra as notas recentes da conta; a
`serviceDescription` repetida indica o serviço padrão que a conta emite.
Combine com `asaas_services_list` para achar o `id` municipal antes de
qualquer emissão.
