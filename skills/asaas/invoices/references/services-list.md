# Serviços municipais ASAAS

A ferramenta `asaas_services_list` consulta `/v3/fiscalInfo/services` — o
catálogo de serviços municipais que a prefeitura disponibiliza para a conta
de produção. Somente leitura (`writesPerformed: false`).

## Emitir nota nunca cria serviço

A emissão sempre se vincula a um serviço já cadastrado: a skill jamais cria um
serviço como efeito colateral de um pedido de nota, e jamais inventa código.
Se o catálogo não tem o que serve à nota, a decisão é do usuário (outro
serviço existente, ou o código correto com a contabilidade).

## Criação a pedido explícito do usuário

Criar serviço é ato separado e legítimo **quando o usuário pede isso
diretamente**. A API pública do ASAAS, porém, expõe apenas a leitura deste
catálogo — não há `POST`/`PUT`/`DELETE` de serviço municipal. Nesse caso,
oriente o painel (**Notas Fiscais › Configurações › Serviços › Adicionar
Serviço**) e ofereça listar os serviços existentes antes, para evitar
duplicatas. Não trate o pedido como proibido, e não simule a criação.

## Argumentos

| Argumento | Tipo | Padrão | Regras |
| --- | --- | --- | --- |
| `description` | string | (nenhum) | Filtro por nome/código do serviço (ex.: `1.01`, `sistemas`); até 80 caracteres. |
| `limit` | inteiro | `10` | Entre 1 e 30. |
| `offset` | inteiro | `0` | Não negativo. |

## Resultado de sucesso

`provider: "asaas"`, `environment: "production"`, `note` (lembrete: emitir
nota nunca cria serviço nem especifica um), `query`, `totalCount`,
`hasNext`, `services[]` e `writesPerformed: false`.

Cada serviço traz: `id`, `description` (código + nome, até 200 caracteres) e
`issTax`. O `id` só vira `municipalServiceId` na emissão quando o usuário
escolher explicitamente aquele serviço para a nota; no fluxo normal desta
conta a emissão não envia os campos municipais.

## Contas do Portal Nacional

Contas que emitem pelo Portal Nacional não recebem a lista municipal pela
API. Nesse cenário a consulta falha com erro do provedor (ex.: "código de
serviços municipais não habilitado") — não é falha sua. A orientação oficial
([guia](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico)) é
obter o código no Portal Nacional ou com a contabilidade e usá-lo em
`municipalServiceCode` quando um serviço específico for necessário. Na regra
operacional desta conta a emissão segue sem os campos municipais; se o
provedor recusar, apresente o motivo real e reporte à equipe. Nunca adivinhe
código.

## Códigos de falha

| Código | Ação |
| --- | --- |
| `asaas_services_invalid_arguments` | Corrija filtros; nada foi chamado. |
| `asaas_services_unexpected` | Resposta fora do formato; tente uma vez. |
| `asaas_provider_unavailable` | Pode ser conta sem lista municipal (Portal Nacional) — trate com o usuário, não repita em loop. |
| Demais (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_timeout`, `asaas_transport_failed`) | Fluxo padrão das skills ASAAS. |
