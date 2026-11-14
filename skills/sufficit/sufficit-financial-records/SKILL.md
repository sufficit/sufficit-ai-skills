---
name: sufficit-financial-records
description: "Write, review and query the text of Sufficit financial ledger records (customer statement lines in fina_financial_records): the description shown to people and the machine document. Applies the house convention of correct Portuguese with fixed delimiters (: ; [competência] {referência} (ORIGEM) · Rótulo: valor) so lines stay readable and can be filtered with regex. Use when creating or correcting a credit, debit, bonus, transfer, refund or commission line, when designing a new ledger producer in code, when a description is vague (\"Pagamento de comissões: 1 período(s)\"), and when searching the statement by origin, competence or reference. Use for descricao de lancamento, extrato financeiro, registro financeiro, padrao de descricao, filtrar extrato, regex no extrato."
metadata:
  version: "1.0.0"
  author: "Sufficit"
---

# Sufficit financial records

A ledger row has two text fields for two readers:

- `description` (max 250): **people and regex filters**. Correct Portuguese built with fixed
  delimiters.
- `document` (max 300): **code**. Machine keys `PREFIX:id[:PREFIX:id]` used for joins, idempotency
  and reconciliation (`SERVICO:<id>`, `COMISSAO:<payout>`, `ASAAS:<pay_id>`, `IDBOLETO:<id>`,
  `CENTRODECUSTO:<id>:TRANSFERENCIA:<id>`).

Never put an identifier in the description when the document can carry it, and never use the
description as a key.

## The description grammar

```
<Ação>[: <item>[; <item>]...][ · <Rótulo>: <valor>]...
item := <objeto>[ [<competência>]][ {<referência>}][ (<ORIGEM>)]
```

| Piece | Use | Example |
|---|---|---|
| `Ação` | what happened, sentence case, with accents | `Pagamento de comissões` |
| `: ` | ends the action (first colon only) | `Pagamento de comissões: ...` |
| `; ` | separates items; never a comma, because titles contain commas | `TRONCO DE ENTRADA [10/2026] (A LTDA); TRONCO FLEXIVEL+ [11/2026] (B LTDA)` |
| `[MM/AAAA]` | competence in the São Paulo calendar; several inside with `; ` | `[10/2026; 11/2026]` |
| `{...}` | reference to another record or document | `{débito #213863}`, `{NFS-e 1101}` |
| `(NOME)` | **origin**, the last parentheses of the item: the counterpart (customer, payer, representative) with its registry title, frozen at write time | `(FORMATTA NEGÓCIOS LTDA)` |
| ` · Rótulo: valor` | extra attribute at the end | `· DID: 552125978975` |

Rules:

1. Always name the **origin** when another party exists (commission, transfer, payment made for
   someone else, bonus granted because of a customer).
2. Remove `; [ ] { } ( )` from the free text before embedding it (`;` → `,`), otherwise the
   regex breaks.
3. No trailing period. Write money (`R$ 1.234,56`) only if a second amount is needed; the value is
   in the `value` column.
4. Within 250 characters, drop whole items and end with `; +N outro(s)`. Never cut a name.
5. Do not change formats that code parses: `Ativação do serviço - TÍTULO[ · DID: ...]` and the
   transfer `(CONTRAPARTE)`. The [convention reference](references/convention.md) lists every
   current producer.

Good: `Pagamento de comissões: Suporte e assessoria do Chatwoot, n8n e API do WhatsApp [10/2026] (FORMATTA NEGÓCIOS LTDA)`
Bad: `Pagamento de comissões: 1 período(s)` (no service, no competence, no origin)

## Writing or changing a row

- **New lines** come from the domain flow (payment, transfer, payout, bonus) through the
  transactional writer. In code, build the text with a pure, tested formatter, as
  `CommissionPayoutDescription.Build` in `sufficit-standard` does.
- **Correcting an existing line** is a financial write. Use only
  `FinancialLedgerMySqlTransactionalWriter.Update`, with the expected version (`updated_at`) and an
  idempotent operation key. Keep value, date, document, authorship and active state. Compare the
  statement and balance before and after, and record an activity. Never `UPDATE` the table directly.
- Show the proposed text and get confirmation before writing to a customer's statement.

## Querying

Filter the description with regex, and join through the document:

```sql
SELECT code, movement_at, value, description FROM fina_financial_records
WHERE kind = 'cmrb - comissao' AND description REGEXP '\\(FORMATTA[^()]*\\)';      -- by origin

SELECT code, description FROM fina_financial_records
WHERE description REGEXP '\\[[^]]*10/2026[^]]*\\]';                                -- by competence
```

More patterns and the producer table: [convention reference](references/convention.md).
Canonical source: `sufficit-standard/docs/USAGE-FINANCIAL-RECORD-DESCRIPTIONS.md`.
