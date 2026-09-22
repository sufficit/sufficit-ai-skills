---
name: asaas-customers
description: Lista e encontra clientes da conta de produção do ASAAS (nome, e-mail, documento mascarado) pela ferramenta asaas_customers_list do Sufficit AI Genius. Use quando o usuário pedir para ver, buscar ou conferir clientes cadastrados no ASAAS; somente leitura, sem criar ou alterar nada.
---

# Clientes ASAAS de produção

Use esta orientação quando o usuário pedir para ver, listar, buscar ou
conferir clientes, contatos ou pagadores cadastrados no ASAAS.

## Credencial

- A ferramenta resolve sozinha a chave em `personal/asaas/production/api-key`
  no Vault pessoal do Sufficit Identity.
- Nunca peça a chave na conversa e nunca a inclua em argumentos, comandos ou
  arquivos.
- Se o resultado indicar `asaas_key_missing`, prepare exatamente essa entrada
  com a ferramenta de preparo de Vault do Genius (`vault_prepare_entry`) e
  entregue a tela segura para o usuário colar e salvar. Se indicar
  `asaas_vault_sign_in_required`, peça para entrar na conta Sufficit.

## Consulta de clientes

Descubra e use `asaas_customers_list`. Ela executa um `GET` fixo em
`/v3/customers` com filtro opcional de nome e paginação. É somente leitura:
não cria, altera nem remove cliente nenhum.

Considere o resultado confiável somente quando indicar `provider: "asaas"`,
`environment: "production"` e `writesPerformed: false`. Em caso de falha, siga
[references/customers-list.md](references/customers-list.md).

Traduza `personType` para linguagem simples: FISICA = pessoa física,
JURIDICA = empresa. O documento chega sempre mascarado nos 3 últimos dígitos
(ex.: `***705`) — nunca tente adivinhar ou completar o número. Para contas
grandes, percorra as páginas com `offset` enquanto `hasNext` for verdadeiro;
não prometa "todos" de uma vez, o limite por página é 30.

## Limites honestos

- O resultado traz id, nome, tipo de pessoa, e-mail e documento mascarado.
  Telefone, endereço, observações e referências externas não entram no
  contexto do modelo. Se o usuário precisar desses dados, oriente o painel
  do ASAAS.
- Não há como criar, editar ou remover cliente por aqui. Se o usuário pedir,
  explique que por enquanto a integração é de consulta e ofereça o painel.

## Quando a ferramenta não existe

Se `asaas_customers_list` não estiver disponível, o plugin ASAAS está
desabilitado ou esta versão do Genius ainda não o oferece. Oriente o usuário
a ativar o plugin ASAAS nas extensões do Genius ou atualizar o aplicativo.
Não contorne a ausência chamando a API por shell, script ou outra ferramenta:
a chave de produção não pode transitar pelo prompt.
