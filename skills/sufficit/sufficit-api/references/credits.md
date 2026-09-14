# Créditos e vales

## Limite do domínio

O Endpoints é a fonte de verdade de produto, carteira, saldo, recarga, benefício,
vale e ledger. O agente gerencial pode consultar esses dados, administrar vales e
aplicar um vale publicado a uma carteira conforme suas funções. Não existe rota
gerencial para apagar movimentos, transferir ou converter saldo, alterar saldo pago
ou confirmar pagamento. Recarga só vira saldo após recibo confirmado pelo Checkout.

Antes de qualquer chamada, pesquise no OpenAPI vivo por `credits`, `voucher`,
`rules`, `products`, `resources` ou `account`. As rotas abaixo descrevem o contrato atual e
servem para reconhecer o resultado da descoberta, não para dispensá-la.

## Consultas gerenciais

- `GET /Finance/Credits/Rules`: conversão de unidades, origem do `contextId` e
  operações que formam o fluxo gerencial.
- `GET /Finance/Credits/Products`: produtos e GUIDs disponíveis.
- `GET /Finance/Credits/Resources`: recursos cobrados e vínculo com produto.
- `GET /Finance/Credits/Account?contextId=...&productId=...`: carteira, capacidade
  de consumir, benefícios ativos, até 50 recargas e até 50 movimentos.
- `GET /Finance/Credits/Vouchers`: até 200 vales, inclusive desativados.

Resolva primeiro o produto pelo GUID retornado pela API. Nunca salve nome ou título
como chave. O `contextId` financeiro é exatamente o `id` GUID do contato; **não
existe outro identificador financeiro**. Quando o usuário nomear uma pessoa ou
empresa, use `POST /Contact/Search` com `titulo`, `cadastro`, `email` e `phone`.
Continue sem perguntar quando houver uma única correspondência inequívoca; se houver
mais de uma, apresente título e GUID para o usuário escolher. Conta ausente não é
saldo zero: significa que a carteira ainda não foi aberta após adesão ao serviço.

Valores de carteira e movimentos usam unidades inteiras de alta precisão:

```text
1 BRL = 1.000.000.000 unidades
valor em BRL = unidades / 1.000.000.000
```

Apresente BRL de forma humanizada, mas conserve as unidades originais quando uma
conferência financeira exigir precisão. `MoneyUnits` é saldo pago. Benefícios
promocionais permanecem separados. Movimentos conhecidos incluem `topup`, `usage`
e `redemption`; `UnchargedUnits` não é dívida.

## Publicar um vale

Use `POST /Finance/Credits/Vouchers` somente após obter produtos, recursos e vales
atuais e confirmar que não há campanha equivalente. A publicação cria uma oferta
imutável: não há edição nem exclusão. Uma correção exige desativar a oferta errada e
publicar outra com novo GUID.

O corpo `CreditVoucherIssueRequest` aceita os campos abaixo. `id`, `title`,
`startsUtc` e `endsUtc` são obrigatórios; os demais campos têm as regras descritas:

- `id`: UUID novo e único, gerado por fonte local confiável; nunca reutilizar.
- `title`: 1 a 120 caracteres, sem controles.
- `productId`: ausente para elegibilidade global ou GUID do produto.
- `resourceId`: opcional; quando presente, deve pertencer a `productId`.
- `contextId`: opcional; quando presente, limita a um contexto GUID.
- benefício: exatamente um entre `percentage` de 0 a 100, exclusivo de zero, ou
  `fixedUnits` positivo. Para valor fixo, converta BRL para unidades sem arredondar
  silenciosamente.
- `startsUtc` e `endsUtc`: ISO 8601 UTC; fim posterior ao início e ao momento atual.
- `durationDays`: 1 a 366; o benefício termina no menor prazo entre duração após o
  resgate e `endsUtc`.
- `maxRedemptions`: 1 a 100.000; `maxPerContext`: entre 1 e o limite total.
- `enabled`, `createdBy` e `createdUtc` não pertencem ao pedido: o servidor habilita
  a oferta e registra o ator e o instante autenticados.

Escopo global significa elegibilidade, não carteira compartilhada. Cada resgate
continua preso a um contexto e produto. Vale percentual de recurso não alcança os
outros recursos. Um uso é um resgate; leituras de consumo posteriores não gastam
novas utilizações.

Antes de publicar, resuma para o usuário: título, tipo/valor, produto, recurso,
contexto, validade, duração e limites. Se qualquer um desses dados materiais não
estiver determinado, peça-o. Depois da chamada, consulte a lista e confira o GUID e
os campos persistidos.

Exemplo de vale de R$ 500 para o Cloud Mobile, substituindo os GUIDs e datas após
consultar a API:

```json
{
  "id": "NOVO-GUID-DO-VALE",
  "title": "Crédito promocional Cloud Mobile",
  "productId": "bdd4e0f8-0900-4d90-924f-86e3a929eaa2",
  "resourceId": null,
  "contextId": "CONTACT-ID-DO-BENEFICIÁRIO",
  "percentage": 0,
  "fixedUnits": 500000000000,
  "startsUtc": "DATA-UTC-DE-INÍCIO",
  "endsUtc": "DATA-UTC-DE-FIM",
  "durationDays": 30,
  "maxRedemptions": 1,
  "maxPerContext": 1
}
```

Publicar apenas cria a oferta; não lança ainda o benefício na carteira.

## Aplicar crédito promocional

Quando o usuário pedir para **lançar, conceder ou aplicar** um crédito presente,
complete as duas escritas: publique o vale fixo e depois use
`POST /Finance/Credits/Vouchers/{id}/Redeem` com:

```json
{
  "contextId": "CONTACT-ID-DO-BENEFICIÁRIO",
  "productId": "GUID-DO-PRODUTO",
  "idempotencyKey": "chave-estável-desta-concessão"
}
```

Gere uma chave opaca e estável para a concessão e reutilize-a somente ao repetir a
mesma tentativa. Depois, consulte `GET /Finance/Credits/Account` e confirme o
benefício pelo `voucherId` e por `remainingUnits`. Não descreva `fixedUnits` como
saldo pago: ele é benefício promocional consumido antes de `MoneyUnits`.

Se o resgate informar carteira inexistente, não publique outro vale e não escolha
outro contexto. Informe que o contato ainda não aderiu ao produto ou que a carteira
não foi aberta. Em resposta ambígua, consulte conta e vales antes de repetir.

## Desativar um vale

`POST /Finance/Credits/Vouchers/{id}/Disable` impede novos resgates, mas não revoga
benefícios já concedidos. Não há reativação nessa API. Resolva o vale por GUID,
mostre o título e o estado atual e só execute quando o pedido identificar claramente
essa campanha. Resposta repetida para um vale já desativado é idempotente; valide a
lista depois da chamada.

Se o pedido for apagar vale, estornar recarga, alterar saldo pago, transferir crédito
ou revogar benefício já resgatado, explique que o contrato atual não oferece essa
operação. Não improvise com outro endpoint nem altere banco diretamente.
