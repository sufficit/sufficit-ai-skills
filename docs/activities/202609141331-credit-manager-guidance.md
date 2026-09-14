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

Pendente de registro após push e sincronização do catálogo Genius.
