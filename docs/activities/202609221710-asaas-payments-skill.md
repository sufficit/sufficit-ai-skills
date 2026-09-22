# Skill pública de cobranças ASAAS — 2026-09-22

## Objetivo

Publicar no catálogo v2 a orientação de consulta de cobranças da conta de
produção do ASAAS, seguindo o combo já validado: a ferramenta executável
`asaas_payments_list` vive no plugin `plugins/asaas` do Genius; toda a
orientação vive nesta skill pública em `skills/asaas/payments`.

## Estado inicial

O espelho estava em `229be1b` (import `asaas/connection`, 156 pacotes). O
plugin ainda oferecia apenas `asaas_connection_test`; o usuário aprovou a
ampliação começando por cobranças, somente leitura.

## Alterações

- Criado `skills/asaas/payments` na versão 0.1.0 com `SKILL.md`, referência de
  contrato, cartão, metadados de interface, `release.json` e licença MIT-0.
- `SKILL.md` orienta a jornada de cobranças: pedido leigo comum (vencidas,
  recebidas, faturas), descoberta de `asaas_payments_list`, tradução das
  situações para linguagem simples, paginação honesta com `offset`/`hasNext`,
  limites explícitos (dados do cliente não entram no contexto) e conduta
  quando a ferramenta não existe.
- `references/payments-list.md` documenta os argumentos (status permitido,
  limit 1–30, offset ≥ 0), os campos sanitizados de sucesso e os 11 códigos
  de falha com a ação esperada de cada um.
- README, catálogo v2 e manifesto atualizados para 157 pacotes, com digest
  SHA-256 do novo pacote (`29a5f6a7…8ff5e2a`).

## Decisões

- Leitura antes de escrita: cobranças começam como consulta; criar/estornar
  cobrança fica para depois, com piso de aprovação por ser ato financeiro
  irreversível.
- O resultado da tool é marcado como conteúdo não confiável
  (`ReturnsUntrustedContent` no plugin) e a skill instrui a tratar os campos
  como dados do provedor, nunca como instruções.
- Sem repetição de código: nenhum script na skill; a execução com credencial
  permanece exclusivamente no plugin (iOS incluso).

## Validação

- `python3 scripts/validate.py`: 157 pacotes aprovados.
- `python3 -m json.tool` nos catálogos: aprovado.

## Limites e continuidade

Esta entrega cobre somente leitura de cobranças. O próximo domínio aprovado é
clientes (leitura); escritas (criar cobrança, cadastrar cliente) exigem
revisão de aprovação antes de entrar. A publicação no catálogo do Genius
ocorre via `scripts/update-skill-catalog.sh` + `scripts/publish-skill-catalog.sh`.
