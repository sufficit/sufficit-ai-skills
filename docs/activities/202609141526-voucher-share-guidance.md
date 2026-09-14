# Orientação para compartilhamento de vale no Checkout

Data: 2026-09-14 15:26 America/Sao_Paulo.

## Entrega

A skill `sufficit-api` foi atualizada para a versão 1.0.2. O agente agora distingue
o resgate gerencial imediato da entrega de um vale avulso por link ao cliente.

O fluxo novo ensina a usar `POST /Finance/Credits/Vouchers/{id}/Share` somente em
vale vigente e previamente vinculado a `Contact.id` e produto. A resposta
`voucherId`, `url` e `expiresUtc` é apresentada de forma humanizada, sem tratar o
token portador como dado comum de log ou diagnóstico.

## Decisões de segurança e negócio

- Gerar ou copiar o link não aplica o benefício; a confirmação ocorre no Checkout.
- O agente não abre nem aplica o link durante a verificação, pois isso seria uma
  mutação financeira real.
- Vales globais ou sem produto não são silenciosamente adaptados. Como a oferta é
  imutável, um novo vale vinculado exige autorização explícita.
- Resposta incerta do `Share` não autoriza duplicar a campanha; a repetição usa o
  mesmo GUID.
- Pedidos ambíguos entre “conceder agora” e “entregar por link” são esclarecidos
  antes da escrita, evitando que o cliente receba um link já consumido.

## Validação

- `quick_validate.py`: pacote individual aprovado.
- `python3 scripts/validate.py`: 154 pacotes públicos e digest SHA-256 aprovados.
- Os dois catálogos passaram em `json.tool`; `git diff --check` não encontrou
  erros de whitespace.

A sincronização do Genius permanece responsabilidade do workflow acionado após
atualização válida da `main`.
