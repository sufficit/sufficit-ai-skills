# Financial record description convention: reference

Canonical copy: `sufficit-standard/docs/USAGE-FINANCIAL-RECORD-DESCRIPTIONS.md`.

## Regex for each piece

| Piece | Regex (PCRE / .NET) |
|---|---|
| action | `^(?<acao>[^:]+): ` |
| items | split on `; (?![^\[]*\])` (does not split inside `[ ]`) |
| competences | `\[(?<comp>\d{2}/\d{4}(?:; \d{2}/\d{4})*)\]` |
| reference | `\{(?<ref>[^}]+)\}` |
| origin | `\((?<origem>[^()]+)\)(?=;\| ·\|$)` |
| attribute | ` · (?<rotulo>[^:]+): (?<valor>[^·]+)` |
| whole commission item | `(?<servico>[^:;\[]+?) \[(?<comp>[^\]]+)\] \((?<origem>[^()]+)\)` |

MariaDB `REGEXP` uses PCRE: double the backslashes in SQL string literals (`'\\('`).

## Current producers

| `kind` | Description | `document` |
|---|---|---|
| `ativ - ativacao` | `Ativação do serviço - TÍTULO[ · DID: 552125978975]` | `SERVICO:<serviço ou período>` |
| `cmrb - comissao` (payout) | `Pagamento de comissões: SERVIÇO [10/2026] (CLIENTE); ...` | `COMISSAO:<payout>` |
| `cmrb - comissao` (legacy, before 2026-10-06) | `Recebimento de comissão por ativação de serviço: TÍTULO (CLIENTE)` | `SERVICO:<serviço>` |
| `trns`/`trne - transferencia` | `(CONTRAPARTE)` | `CENTRODECUSTO:<origem>:TRANSFERENCIA:<id>` |
| `rect - recarga ted` | `PIX Asaas - serviço avulso: OBJETO {débito #213863}` | `ASAAS:<pay_id>` |
| `recc - recarga cartao` | `Pagamento recorrente no cartão — serviços de outubro/2026` | `ASAAS:<pay_id>` |
| `recb - recarga boleto` | `Recarga por Boleto Bancário` | `IDBOLETO:<id>` |
| `bons - bonus` | `Bônus substituído por gratuidade na primeira competência do serviço` | `BONUS:SERVICO:<id>:PRIMEIRA` |

Formats that code parses, which must not change without changing their readers:

- `Ativação do serviço - ` prefix: the service name for commission payouts and the history enrichment.
- Legacy commission ` (CLIENTE)` suffix: kept by `CommissionDescription` on rewrites.
- Transfer `(NOME)`: checked by the transfer metadata audit.

Older rows still contain free text (`BONUS`, `(débito 213863)`). New rows follow the grammar.

## Examples

```
Pagamento de comissões: TRONCO DE ENTRADA [10/2026] (BRUNNAS CONFECCOES LTDA)
Pagamento de comissões: TRONCO FLEXIVEL+ [10/2026; 11/2026] (GF NET LTDA); TRONCO FLEXIVEL+ [11/2026] (LOPES TELECOM LTDA)
Bônus por cobrança indevida: Suporte in loco terceirizado [10/2026] {débito #212345} (CLIENTE LTDA)
Estorno de PIX enviado por chave {débito #214000} (EMILLY CAROLINE DA SILVA JULIAO)
```
