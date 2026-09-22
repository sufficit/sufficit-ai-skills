# Identificação de cliente nas notas e política de documento — 2026-09-22

## Objetivo

Duas correções de produto aprovadas pelo usuário no ciclo do tablet:

1. **"Para quem foi emitida"**: a listagem de notas trazia só o id do cliente
   (`cus_...`); o agente respondia os dados da nota sem saber o recebedor.
2. **Política de documento**: CNPJ (pessoa jurídica) é dado público de
   registro e chega **completo e formatado**; CPF (pessoa física) fica
   limitado aos **3 primeiros dígitos** (antes: `***` + 3 últimos).

## Alterações

- `skills/asaas/customers` → **0.3.0**: SKILL.md, `references/customers-list.md`
  e `references/customers-create.md` descrevem a política de identificação
  (CNPJ completo; CPF nos 3 primeiros dígitos; outros formatos `***`) e mantêm
  a proibição de deduzir o CPF completo.
- `skills/asaas/invoices` → **0.2.0**: SKILL.md e `references/invoices-list.md`
  documentam o `customer` resolvido em cada nota (`id`, `name`, `personType`,
  `document`) e o `unresolvedCustomerIds` + `guidance` quando a resolução não
  é possível — nunca afirmar o recebedor a partir de id não resolvido.
- `catalog/upstream-v2.json`: descrições das duas skills atualizadas;
  `catalog/import-manifest.json`: digests SHA-256 recalculados (customers
  `b2cdc41d…`, invoices `e3483517…`).

## Decisões

- CNPJ aberto por ser registro público; CPF parcial nos 3 primeiros dígitos
  (os que identificam a região fiscal) — decisão do usuário, espelhada na
  ferramenta do plugin (`MaskDocument`).
- A resolução de cliente acontece na própria ferramenta de listagem (leitura
  extra por id distinto, cap 30/página); a skill só ensina a ler o que já vem.

## Validação

- `python3 scripts/validate.py`: 159 pacotes aprovados.
- `python3 -m json.tool` nos dois catálogos: aprovado.

## Continuidade

O plugin do Genius (`plugins/asaas`) implementa a mesma política na mesma
entrega; o pin do catálogo no repositório do produto é atualizado em seguida
(`scripts/update-skill-catalog.sh`).
