# Skill pública de conexão ASAAS — 2026-09-22

## Objetivo

Publicar no catálogo v2 a orientação completa de conexão da conta de produção
do ASAAS, separando responsabilidades do combo plugin + skill: todas as
ferramentas executáveis ficam no plugin `plugins/asaas` do Genius; toda a
orientação vive nesta skill pública em `skills/asaas`.

## Estado inicial

O espelho estava em `7e781b0` (import `images/svg-vectorization`, 155
pacotes). O plugin ASAAS já entregava `asaas_connection_test` com um
`SKILL.md` interno sem consumidor em runtime e fora do catálogo público.

## Alterações

- Criado `skills/asaas/connection` na versão 0.1.0 com `SKILL.md`, referência
  de contrato, cartão, metadados de interface, `release.json` e licença MIT-0.
- `SKILL.md` orienta a jornada completa: referência canônica do Vault
  (`personal/asaas/production/api-key`), preparo seguro da entrada quando
  ausente, teste somente leitura via `asaas_connection_test` e conduta quando
  a ferramenta não existe (plugin desabilitado ou Genius antigo).
- `references/connection-test.md` documenta os 9 campos do resultado de
  sucesso e os 9 códigos de falha com a ação esperada de cada um.
- README, catálogo v2 e manifesto atualizados para 156 pacotes, com digest
  SHA-256 do novo pacote (`cd382c03…fc4ab`).

## Decisões

- Coleção própria `skills/asaas` (não `sufficit`), conforme diretriz do
  usuário; author Sufficit, MIT-0, `sourceId` `sufficit-genius`.
- Skill sem scripts: a chave de produção não transita pelo prompt em hipótese
  alguma; scripts de skill rodariam via `shell_exec` sem canal do Vault e sem
  suporte no iOS. A capacidade executável com credencial permanece no plugin.
- A doutrina do documento interno do plugin foi preservada e ampliada na
  referência pública (falhas, repetibilidade, proibição de escrita para
  diagnóstico).

## Validação

- `python3 scripts/validate.py`: 156 pacotes aprovados (front matter, links,
  digests, cobertura total do manifesto).
- `python3 -m json.tool` nos dois catálogos e `git diff --check`: aprovados.

## Limites e continuidade

Esta entrega cobre apenas conexão/teste da conta. Recursos adicionais do
ASAAS (cobranças, clientes, assinaturas) exigem novas ferramentas no plugin e
referências próprias aqui, após revisão. A publicação no catálogo do Genius
ocorre via `scripts/update-skill-catalog.sh` + `scripts/publish-skill-catalog.sh`.
