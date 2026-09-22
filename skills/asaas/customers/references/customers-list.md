# Lista de clientes ASAAS

A ferramenta `asaas_customers_list` consulta `/v3/customers` na conta de
produção, injetando a chave `personal/asaas/production/api-key` apenas no
cabeçalho `access_token`. O resultado só contém campos projetados e
sanitizados: telefones, endereços, observações e referências externas não
entram no contexto do modelo. O documento segue a política de identificação:
CNPJ chega completo e formatado (registro público, ex. `27.506.088/7001-24`);
CPF chega limitado aos 3 primeiros dígitos (ex. `390.***.***-**`).

## Argumentos

| Argumento | Tipo | Padrão | Regras |
| --- | --- | --- | --- |
| `name` | string | (nenhum) | Opcional; casa com clientes cujo nome contém o texto. Até 80 caracteres; vazio é ignorado. |
| `limit` | inteiro | `10` | Entre 1 e 30; valores maiores são reduzidos a 30. |
| `offset` | inteiro | `0` | Não negativo, limitado a 100000; use para percorrer páginas. |

## Resultado de sucesso

| Campo | Valor |
| --- | --- |
| `provider` | `asaas` |
| `environment` | `production` |
| `query` | `{ name, limit, offset, returned }` — o que foi pedido e quantos itens vieram |
| `totalCount` | total de clientes que casam com o filtro no ASAAS |
| `hasNext` | `true` quando existe próxima página |
| `customers[]` | itens sanitizados |
| `writesPerformed` | `false` |
| `credentialReference` | `personal/asaas/production/api-key` |

Cada item de `customers[]` traz, quando existe no provedor: `id`, `name`
(truncado em 80 caracteres), `personType`, `email` e `document` (CNPJ
completo e formatado; CPF nos 3 primeiros dígitos; outros formatos chegam
como `***`). Campos
ausentes chegam como `null`.

## Tipos de pessoa

| Valor | Leitura para o usuário |
| --- | --- |
| `FISICA` | Pessoa física. |
| `JURIDICA` | Empresa (pessoa jurídica). |

## Códigos de falha

| Código | Significado | Ação |
| --- | --- | --- |
| `asaas_customers_invalid_arguments` | `name` acima de 80 caracteres, `limit`/`offset` inválidos. | Corrija os argumentos e repita; nada foi chamado no provedor. |
| `asaas_customers_unexpected` | O corpo do ASAAS não veio no formato esperado. | Informe o usuário e tente de novo uma vez; se persistir, trate como indisponibilidade. |
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

## Busca por nome na prática

Se o usuário der um nome, repasse em `name` sem alterar; a correspondência é
por contenção no provedor. Sem nome, liste a primeira página e ofereça
avançar com `offset` enquanto `hasNext` for verdadeiro, até esgotar
`totalCount` ou o pedido do usuário. O documento serve para o usuário
confirmar qual cliente é — no caso de CPF, nunca tente deduzir o número
completo a partir dos 3 primeiros dígitos.
