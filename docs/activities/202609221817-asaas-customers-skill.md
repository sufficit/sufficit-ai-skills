# Skill pública de clientes ASAAS — 2026-09-22

## Objetivo

Publicar no catálogo v2 a orientação de consulta de clientes da conta de
produção do ASAAS, fechando o segundo domínio aprovado (cobranças →
clientes). A ferramenta executável `asaas_customers_list` vive no plugin
`plugins/asaas` do Genius; toda a orientação vive nesta skill pública em
`skills/asaas/customers`.

## Estado inicial

O espelho estava em `a656e38` (import `asaas/payments`, 157 pacotes). O
usuário aprovou clientes como segundo domínio, somente leitura, no regime de
acumulação sem release público.

## Alterações

- Criado `skills/asaas/customers` na versão 0.1.0 com `SKILL.md`, referência
  de contrato, cartão, metadados de interface, `release.json` e licença MIT-0.
- `SKILL.md` orienta a jornada de clientes: pedido leigo comum (quem são meus
  clientes, buscar por nome), descoberta de `asaas_customers_list`, tradução
  de `personType` para linguagem simples, busca por nome sem alterar o texto,
  paginação honesta com `offset`/`hasNext`, limites explícitos (telefone,
  endereço e observações não entram no contexto; documento chega mascarado) e
  conduta quando a ferramenta não existe.
- `references/customers-list.md` documenta os argumentos (nome ≤ 80,
  limit 1–30, offset ≥ 0), os campos sanitizados de sucesso e os 11 códigos
  de falha com a ação esperada de cada um.
- README, catálogo v2 e manifesto atualizados para 158 pacotes, com digest
  SHA-256 do novo pacote (`391b9e35…61881`).

## Decisões

- Documento mascarado nos 3 últimos dígitos: o modelo pode ecoar uma dica de
  identificação (`***705`) sem nunca segurar o CPF/CNPJ completo; documentos
  curtos chegam como `***`.
- Leitura antes de escrita mantida: cadastrar/editar/remover cliente fica
  para depois, com piso de aprovação.
- Resultado marcado como conteúdo não confiável (`ReturnsUntrustedContent`),
  alinhado ao contrato de cobranças.

## Validação

- `python3 scripts/validate.py`: 158 pacotes aprovados.
- `python3 -m json.tool` nos catálogos: aprovado.

## Continuidade

Esta entrega cobre somente leitura de clientes. Escritas (criar cobrança,
cadastrar cliente) exigem revisão de aprovação antes de entrar. O build do
app segue o regime de acumulação (versionCode crescente, instalação local no
tablet, sem canal público) até o usuário pedir o release.
