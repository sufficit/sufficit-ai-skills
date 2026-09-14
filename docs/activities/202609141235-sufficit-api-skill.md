# Skill genérica da Sufficit API — 2026-09-14

## Objetivo

Adicionar ao catálogo público uma skill genérica para agentes de gestores
operarem a API corporativa com a identidade já conectada no Genius. O primeiro
recorte cobre gestão central de créditos, vales e contatos.

## Estado inicial

O repositório estava limpo, sincronizado com `origin/main` e continha 153 skills,
três delas Sufficit. O Genius já oferecia `sufficit_api_search` e
`sufficit_api_call`, mas não havia skill de domínio ensinando o uso operacional,
os limites financeiros ou a gestão segura de contatos.

## Alterações

- Criado `skills/sufficit/sufficit-api` na versão 1.0.0, com `SKILL.md`, licença
  MIT-0, metadados de interface, release e cartão de catálogo.
- A entrada principal exige descoberta pelo OpenAPI vivo, usa a credencial fora
  do prompt, diferencia 401/403/409/422 e manda verificar toda escrita por uma
  leitura independente.
- `references/credits.md` documenta consulta de produtos, recursos, carteiras,
  movimentos, recargas e vales, conversão exata de unidades e publicação/
  desativação de campanhas.
- `references/contacts.md` documenta busca por contexto/GUID, atributos
  conhecidos, criação, atualização pontual, importância e exclusão permanente.
- README, catálogo v2 e manifesto foram atualizados para 154 skills e quatro
  pacotes Sufficit, com digest SHA-256 do novo pacote.

## Decisões

- `sufficit-api` permanece genérica e recebe novos domínios por referências sob
  demanda; não replica todo o Swagger.
- OpenAPI implantado prevalece sobre caminhos memorizados. As referências
  preservam apenas semântica e invariantes que mudam decisões do agente.
- A skill não cria autorização permanente: escritas dependem do pedido atual e
  continuam sujeitas às funções da conta no servidor.
- A API gerencial não permite crédito manual, exclusão de movimento,
  transferência ou conversão. O agente não procura atalhos no banco.
- Exclusão de contato exige alvo conferido e ciência da irreversibilidade; a
  marcação de importante não é removida automaticamente para contornar proteção.

## Validação

- `quick_validate.py skills/sufficit/sufficit-api`: aprovado.
- `python3 scripts/validate.py`: 154 pacotes aprovados, incluindo links e digest.
- Os exemplos JSON foram desserializados com sucesso.
- Doze operações mencionadas nas referências foram comparadas com o OpenAPI v2
  vivo de `endpoints.sufficit.com.br` e todas existem.
- `python3 -m json.tool` nos dois manifestos e `git diff --check`: aprovados.

A primeira versão da checagem adicional manteve query strings nos caminhos e
produziu três falsos negativos; após normalizar o trecho posterior a `?`, a
comparação passou. Não houve divergência de API.

## Limites e continuidade

Esta entrega ensina somente créditos/vales e contatos. Operações de produto,
contratos, boletos, telefonia e outros domínios devem ganhar referências próprias
quando forem priorizadas e conferidas no OpenAPI vigente. A publicação no catálogo
do Genius é disparada pelo workflow após `main` receber uma revisão válida.
