# Skills de escrita ASAAS — 2026-09-22

## Objetivo

Publicar no catálogo v2 a orientação da fase de escritas do ASAAS: cadastro
de clientes com deduplicação e emissão de notas fiscais de serviço sempre
vinculada a serviço municipal existente. Terceira e quarta skills do domínio
Asaas (connection, payments, customers, invoices), levando o espelho a 159
pacotes.

## Estado inicial

Espelho em `804ca70` (157→158 com asaas-customers 0.1.0 somente leitura). O
usuário aprovou a fase de escritas com um princípio explícito: **consultar se
já existe antes de escrever**; para nota fiscal, a nota nasce vinculada a um
serviço que **já existe** — "criar serviço novo" não é opção, e sem palavra
do usuário nenhuma entidade de apoio é criada.

## Alterações

- `skills/asaas/customers` promovido a **0.2.0**: SKILL.md ganhou a seção de
  cadastro (recolher nome/CPF/e-mail, deixar a ferramenta deduplicar, aguardar
  card de aprovação, reportar com honestidade) e nova referência
  `references/customers-create.md` com argumentos, recusas
  (`duplicate_document`, `possible_duplicate` + `confirmedDistinct`), resultado
  e códigos de falha (timeout manda consultar antes de repetir).
- Criado `skills/asaas/invoices` **0.1.0**: SKILL.md com a regra de ouro
  (descobrir serviço padrão pelo histórico → confirmar no catálogo municipal
  → escolher com o usuário; Portal Nacional usa código dado pelo usuário),
  três referências (`invoices-list`, `services-list`, `invoices-create`),
  cartão, metadados de interface, `release.json` e licença MIT-0.
- README, catálogo v2 e manifesto atualizados para 159 pacotes, com digests
  SHA-256 recalculados (customers `484ad6f8…e156`, invoices `6133f080…8764`).

## Decisões

- O princípio consult-before-write aparece nas duas skills como fluxo
  obrigatório e está garantido em código nas ferramentas (dedup antes do
  POST; recusas devolvem o candidato existente em vez de escrever).
- "Não existe criação de serviço" é dito explicitamente na skill e repetido
  no resultado de `asaas_services_list` (campo `note`).
- Emissão reportada como assíncrona: agendamento inicia o fluxo, autorização
  pela prefeitura vem depois — a skill proíbe prometer autorização imediata.
- Tag de customers mudou de `somente-leitura` para `cadastro`; invoices entra
  com tags `notas-fiscais`/`nfse`.

## Validação

- `python3 scripts/validate.py`: 159 pacotes aprovados.
- `python3 -m json.tool` nos dois catálogos: aprovado.

## Continuidade

As ferramentas correspondentes (`asaas_customers_create`, `asaas_invoices_list`,
`asaas_services_list`, `asaas_invoices_create`) estão no plugin do Genius
(suíte 70/70) e entram no próximo build de acumulação; o pin do catálogo será
atualizado no repositório do produto. Teste leigo de escrita em produção
depende de dados fornecidos pelo usuário.
