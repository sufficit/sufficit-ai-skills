# Serviços municipais ASAAS

A ferramenta `asaas_services_list` consulta `/v3/fiscalInfo/services` — o
catálogo de serviços municipais que a prefeitura disponibiliza para a conta
de produção. Somente leitura (`writesPerformed: false`).

## Não existe criação de serviço

O catálogo vem da prefeitura. Não há endpoint, botão ou fluxo para criar um
serviço — e a skill jamais deve tratar "criar serviço novo" como opção. Se o
catálogo não tem o que serve à nota, a decisão é do usuário (outro serviço
existente, ou o código correto com a contabilidade).

## Argumentos

| Argumento | Tipo | Padrão | Regras |
| --- | --- | --- | --- |
| `description` | string | (nenhum) | Filtro por nome/código do serviço (ex.: `1.01`, `sistemas`); até 80 caracteres. |
| `limit` | inteiro | `10` | Entre 1 e 30. |
| `offset` | inteiro | `0` | Não negativo. |

## Resultado de sucesso

`provider: "asaas"`, `environment: "production"`, `note` (lembrete de que não
existe criação de serviço), `query`, `totalCount`, `hasNext`, `services[]` e
`writesPerformed: false`.

Cada serviço traz: `id` (use como `municipalServiceId` na emissão),
`description` (código + nome, até 200 caracteres) e `issTax`.

## Contas do Portal Nacional

Contas que emitem pelo Portal Nacional não recebem a lista municipal. Nesse
cenário a consulta falha com erro do provedor (ex.: "código de serviços
municipais não habilitado") — não é falha sua. O caminho: pedir ao usuário o
`municipalServiceCode` (com a contabilidade ou no próprio Portal Nacional) e
usá-lo na emissão.

## Códigos de falha

| Código | Ação |
| --- | --- |
| `asaas_services_invalid_arguments` | Corrija filtros; nada foi chamado. |
| `asaas_services_unexpected` | Resposta fora do formato; tente uma vez. |
| `asaas_provider_unavailable` | Pode ser conta sem lista municipal (Portal Nacional) — trate com o usuário, não repita em loop. |
| Demais (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_timeout`, `asaas_transport_failed`) | Fluxo padrão das skills ASAAS. |
