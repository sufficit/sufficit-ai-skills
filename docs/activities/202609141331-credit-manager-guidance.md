# Orientação para concessão gerencial de créditos

Data: 2026-09-14 13:31 America/Sao_Paulo.

## Entrega

A skill `sufficit-api` foi atualizada para a versão 1.0.1. O agente agora aprende
que o contexto financeiro é `Contact.id`, resolve o destinatário por
`POST /Contact/Search`, publica o vale, resgata o mesmo vale na carteira e confirma
o benefício pela conta. O exemplo de Cloud Mobile inclui a conversão exata de
R$ 500 para `500000000000` unidades e separa benefício promocional de saldo pago.

O contrato distingue campos aceitos pelo pedido dos campos definidos pelo servidor
e proíbe escolher resultado ambíguo, duplicar vale após resposta incerta ou usar
outro contexto quando a carteira não existe.

## Validação

- Validador individual da skill: aprovado.
- Catálogo e manifesto: 154 pacotes públicos aprovados.
- JSON e whitespace: aprovados.

## Publicação

- Skill publicada em `main` na revisão `24ded8e`.
- Workflow de validação aprovado.
- Genius fixou essa revisão no commit `df3338a`, validou o contrato e publicou os
  catálogos v1 e v2 no armazenamento público.
- O workflow confirmou que a revisão publicada é exatamente `24ded8e`.
