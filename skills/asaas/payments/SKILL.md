---
name: asaas-payments
description: Lista e consulta cobranças da conta de produção do ASAAS (pagamentos, faturas, vencidas, recebidas) pela ferramenta asaas_payments_list do Sufficit AI Genius. Use quando o usuário pedir para ver, conferir ou somar cobranças do ASAAS; somente leitura, sem criar ou alterar nada.
---

# Cobranças ASAAS de produção

Use esta orientação quando o usuário pedir para ver, conferir, listar ou somar
cobranças, pagamentos, faturas ou valores vencidos do ASAAS.

## Credencial

- A ferramenta resolve sozinha a chave em `personal/asaas/production/api-key`
  no Vault pessoal do Sufficit Identity.
- Nunca peça a chave na conversa e nunca a inclua em argumentos, comandos ou
  arquivos.
- Se o resultado indicar `asaas_key_missing`, prepare exatamente essa entrada
  com a ferramenta de preparo de Vault do Genius (`vault_prepare_entry`) e
  entregue a tela segura para o usuário colar e salvar. Se indicar
  `asaas_vault_sign_in_required`, peça para entrar na conta Sufficit.

## Consulta de cobranças

Descubra e use `asaas_payments_list`. Ela executa um `GET` fixo em
`/v3/payments` com filtro opcional de situação e paginação. É somente leitura:
não cria, altera nem estorna cobrança nenhuma.

Considere o resultado confiável somente quando indicar `provider: "asaas"`,
`environment: "production"` e `writesPerformed: false`. Em caso de falha, siga
[references/payments-list.md](references/payments-list.md).

Traduza as situações para linguagem simples: PENDING = aguardando pagamento,
RECEIVED = recebida, CONFIRMED = recebida e confirmada, OVERDUE = vencida,
REFUNDED = estornada. Para somar ou contar, use os valores retornados — nunca
invente números. Se o usuário pedir "todas", percorra as páginas com
`offset` enquanto `hasNext` for verdadeiro; não tente burlar o limite de 30
por página.

## Limites honestos

- O resultado traz o identificador do cliente (`customer`), mas não o nome,
  CPF/CNPJ, e-mail ou telefone: esses dados não entram no contexto do modelo.
  Se o usuário perguntar quem pagou, diga com naturalidade que a identificação
  do cliente ainda não está disponível na integração.
- Não há como criar, editar ou estornar cobrança por aqui. Se o usuário
  pedir, explique que por enquanto a integração é de consulta e ofereça o
  painel do ASAAS.

## Quando a ferramenta não existe

Se `asaas_payments_list` não estiver disponível, o plugin ASAAS está
desabilitado ou esta versão do Genius ainda não o oferece. Oriente o usuário a
ativar o plugin ASAAS nas extensões do Genius ou atualizar o aplicativo. Não
contorne a ausência chamando a API por shell, script ou outra ferramenta: a
chave de produção não pode transitar pelo prompt.
