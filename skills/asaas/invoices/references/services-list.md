# Serviços municipais ASAAS

A ferramenta `asaas_services_list` consulta `/v3/fiscalInfo/services` — o
catálogo de serviços municipais que a prefeitura disponibiliza para a conta
de produção. Somente leitura (`writesPerformed: false`).

## Emitir nota não cria serviço — porque a emissão omite os campos municipais

No fluxo desta skill a emissão **não envia** `municipalServiceId` nem
`municipalServiceCode`, então um pedido de nota nunca produz cadastro novo.
A skill jamais inventa código. Se o catálogo não tem o que serve à nota, a
decisão é do usuário (outro serviço existente, ou o código correto com a
contabilidade).

A garantia vem da omissão, **não** de uma proteção do provedor. Testes
controlados em conta sandbox (2026-09-23) mostraram que, quando os campos
municipais **são** enviados, o agendamento tem efeito colateral real no
cadastro de serviços da conta:

- enviar só `municipalServiceCode` criou entrada nova, com o nome igual ao
  próprio código (ex.: `01.01.01`, sem o texto oficial do catálogo);
- reutilizar um `municipalServiceName` existente com outro código alterou a
  associação **retroativamente**, inclusive para notas já agendadas;
- a identidade do cadastro é o **nome**, não o código: dois nomes distintos
  com o mesmo código aparecem como dois registros no painel.

Por isso a regra operacional de omitir é também uma proteção do cadastro, e
não apenas uma conveniência. Entradas criadas assim só se removem pelo painel.

## Criação a pedido explícito do usuário

Criar serviço é ato separado e legítimo **quando o usuário pede isso
diretamente**. A API pública do ASAAS, porém, expõe apenas a leitura deste
catálogo — não há `POST`/`PUT`/`DELETE` de serviço municipal (`POST` nesta
rota respondeu HTTP 404 no teste de 2026-09-23). Nesse caso, oriente o painel
(**Notas Fiscais › Configurações › Serviços › Adicionar Serviço**) e ofereça
listar os serviços existentes antes, para evitar duplicatas. Não trate o
pedido como proibido, e não simule a criação.

**Não use agendamento de nota como atalho de cadastro.** Ele até produz
entrada nova (ver seção anterior), mas emite um documento fiscal real, não
permite definir ISS de forma confiável e deixa resíduo removível só pelo
painel. Não é uma API de criação disfarçada.

Também não há endpoint público para **editar, excluir, definir padrão ou
ativar/desativar** serviço: essas ações existem apenas no painel. Não
prometa fazê-las por ferramenta.

## Argumentos

| Argumento | Tipo | Padrão | Regras |
| --- | --- | --- | --- |
| `description` | string | (nenhum) | Filtro por nome/código do serviço (ex.: `1.01`, `sistemas`); até 80 caracteres. Casa **qualquer trecho**, não só o prefixo: `07.` traz também `01.07.01` e `04.07.01`. |
| `limit` | inteiro | `10` | Entre 1 e 30. |
| `offset` | inteiro | `0` | Não negativo. Ver a armadilha de paginação abaixo. |

## Paginação: `offset` funciona como número de página

Testes de 2026-09-23 mostraram que o deslocamento real é `offset × limit`,
não o índice do primeiro elemento:

- `limit=1&offset=5` e `limit=5&offset=1` devolveram **o mesmo item**;
- com `limit=100`, as páginas `0`, `1`, `2` e `3` cobriram os 338 itens
  (100+100+100+38) e `offset=4` veio vazio;
- por isso `limit=5&offset=100` retorna lista vazia com `hasMore: false`,
  apesar de `totalCount: 338`.

Somar `offset += limit`, o padrão usual, **pula a maior parte do catálogo e
encerra sem erro**. Avance de 1 em 1 e pare quando `hasMore` for `false`. Se
um serviço parecer ausente, suspeite da paginação antes de afirmar que não
existe — e prefira o filtro `description` a varrer páginas.

Comportamento observado neste endpoint; confirme antes de assumir o mesmo em
outros. O plugin pode normalizar isso: a regra acima descreve a API crua.

## Resultado de sucesso

`provider: "asaas"`, `environment: "production"`, `note` (lembrete: emitir
nota nunca cria serviço nem especifica um), `query`, `totalCount`,
`hasNext`, `services[]` e `writesPerformed: false`.

Cada serviço traz: `id`, `description` (código + nome, até 200 caracteres) e
`issTax`. O `id` só vira `municipalServiceId` na emissão quando o usuário
escolher explicitamente aquele serviço para a nota; no fluxo normal desta
conta a emissão não envia os campos municipais.

Detalhes observados nos campos (sandbox, 2026-09-23):

- `id` é chave interna sequencial, **sem relação com o código fiscal** (não
  o derive nem o adivinhe a partir do código).
- `description` traz `NN.NN.NN - Texto.` — é este valor **exato** que deve ir
  em `municipalServiceName` quando o usuário escolher o serviço. Nunca monte
  o nome à mão.
- `issTax` é alíquota de referência do catálogo e veio `0.0` em todos os
  itens da conta testada: não a apresente como a tributação real da nota.
- `municipalServiceId` **sozinho é recusado** no agendamento (HTTP 400,
  `invalid_action`: "O campo municipalServiceName deve ser informado"),
  mesmo com id válido. Quando for usar o id, envie o par id + nome.

**Catálogo ≠ cadastro da conta.** Este endpoint lista o que a prefeitura
disponibiliza (centenas de itens); a tela **Notas Fiscais › Configurações ›
Serviços** mostra apenas os serviços salvos da conta, que é outro conjunto.
Não descreva um como se fosse o outro ao responder o usuário.

## Contas do Portal Nacional

Contas que emitem pelo Portal Nacional não recebem a lista municipal pela
API. Nesse cenário a consulta falha com erro do provedor (ex.: "código de
serviços municipais não habilitado") — não é falha sua. A orientação oficial
([guia](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico)) é
obter o código no Portal Nacional ou com a contabilidade e usá-lo em
`municipalServiceCode` quando um serviço específico for necessário. Na regra
operacional desta conta a emissão segue sem os campos municipais — os
detalhes do serviço são auto preenchidos pelo cadastro; se o provedor
recusar, apresente o motivo real e reporte à equipe. Nunca adivinhe código.

## Códigos de falha

| Código | Ação |
| --- | --- |
| `asaas_services_invalid_arguments` | Corrija filtros; nada foi chamado. |
| `asaas_services_unexpected` | Resposta fora do formato; tente uma vez. |
| `asaas_provider_unavailable` | Pode ser conta sem lista municipal (Portal Nacional) — trate com o usuário, não repita em loop. |
| Demais (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_timeout`, `asaas_transport_failed`) | Fluxo padrão das skills ASAAS. |
