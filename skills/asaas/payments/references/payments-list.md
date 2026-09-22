# Lista de cobranças ASAAS

A ferramenta `asaas_payments_list` consulta `/v3/payments` na conta de
produção, injetando a chave `personal/asaas/production/api-key` apenas no
cabeçalho `access_token`. O resultado só contém campos projetados e
sanitizados: URLs de fatura, documentos pessoais, nome e contatos do cliente
não entram no contexto do modelo.

## Argumentos

| Argumento | Tipo | Padrão | Regras |
| --- | --- | --- | --- |
| `status` | string | (nenhum) | Opcional: `PENDING`, `RECEIVED`, `CONFIRMED`, `OVERDUE` ou `REFUNDED`. Qualquer outro valor é rejeitado antes da chamada. |
| `limit` | inteiro | `10` | Entre 1 e 30; valores maiores são reduzidos a 30. |
| `offset` | inteiro | `0` | Não negativo, limitado a 100000; use para percorrer páginas. |

## Resultado de sucesso

| Campo | Valor |
| --- | --- |
| `provider` | `asaas` |
| `environment` | `production` |
| `query` | `{ status, limit, offset, returned }` — o que foi pedido e quantos itens vieram |
| `totalCount` | total de cobranças que casam com o filtro no ASAAS |
| `hasNext` | `true` quando existe próxima página |
| `payments[]` | itens sanitizados |
| `writesPerformed` | `false` |
| `credentialReference` | `personal/asaas/production/api-key` |

Cada item de `payments[]` traz, quando existem no provedor: `id`, `value`,
`netValue`, `description` (truncada em 80 caracteres), `billingType`,
`status`, `dueDate`, `paymentDate`, `installmentNumber`, `installmentCount`,
`invoiceNumber` e `customer` (apenas o identificador). Textos longos são
truncados com `…`; campos ausentes chegam como `null`.

## Situações (status)

| Valor | Leitura para o usuário |
| --- | --- |
| `PENDING` | Aguardando pagamento. |
| `RECEIVED` | Recebida. |
| `CONFIRMED` | Recebida e confirmada. |
| `OVERDUE` | Vencida (passou do vencimento sem pagamento). |
| `REFUNDED` | Estornada. |

## Códigos de falha

| Código | Significado | Ação |
| --- | --- | --- |
| `asaas_payments_invalid_arguments` | Status fora da lista permitida, `limit`/`offset` inválidos. | Corrija os argumentos e repita; nada foi chamado no provedor. |
| `asaas_payments_unexpected` | O corpo do ASAAS não veio no formato esperado. | Informe o usuário e tente de novo uma vez; se persistir, trate como indisponibilidade. |
| `asaas_vault_sign_in_required` | Usuário não autenticado no Sufficit Identity. | Peça para entrar na conta Sufficit e repita. |
| `asaas_key_missing` | Entrada do Vault ausente ou vazia. | Prepare `personal/asaas/production/api-key` com a tela segura e repita após salvar. |
| `asaas_key_invalid` | Chave com formato inválido. | Peça uma nova chave no painel do ASAAS e salve na mesma entrada. |
| `asaas_credential_rejected` | O ASAAS rejeitou a chave (401/403). | Peça uma chave válida, salve no Vault e tente uma única vez. |
| `asaas_provider_unavailable` | O ASAAS respondeu, mas não concluiu. | Se marcada repetível, refaça após uma espera. |
| `asaas_transport_failed` | API inalcançável. | Verifique a rede e repita. |
| `asaas_timeout` | Tempo limite excedido. | Repita uma vez. |
| `asaas_vault_timeout` | Vault excedeu o tempo limite. | Repita uma vez. |
| `asaas_vault_unavailable` | Vault inacessível. | Tente novamente depois. |

Falhas repetíveis admitem uma nova tentativa após breve espera; as demais
exigem ação do usuário ou do provedor antes de insistir. Nunca use uma
operação de escrita para diagnosticar a consulta.

## Páginação na prática

Comece sem `offset`. Se `hasNext` for `true` e o usuário quiser mais, peça a
próxima página com `offset` igual ao acumulado de itens já retornados, até
esgotar `totalCount` ou o pedido do usuário. Não prometa "todas" de uma vez: o
limite por página é 30.
