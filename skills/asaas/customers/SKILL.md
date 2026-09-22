---
name: asaas-customers
description: Consulta, busca e cadastra clientes na conta de produção do ASAAS (nome, e-mail, tipo de pessoa, CNPJ completo ou CPF nos 3 primeiros dígitos) pelas ferramentas asaas_customers_list e asaas_customers_create do Sufficit AI Genius. Consultas são somente leitura; cadastro exige confirmação do usuário e sempre verifica duplicatas antes de escrever.
---

# Clientes ASAAS de produção

Use esta orientação quando o usuário pedir para ver, listar, buscar, conferir
ou **cadastrar** clientes no ASAAS.

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
`/v3/customers` com filtros opcionais de nome, e-mail e documento (CPF/CNPJ)
e paginação. É somente leitura: não cria, altera nem remove cliente nenhum.

Considere o resultado confiável somente quando indicar `provider: "asaas"`,
`environment: "production"` e `writesPerformed: false`. Em caso de falha, siga
[references/customers-list.md](references/customers-list.md).

Traduza `personType` para linguagem simples: FISICA = pessoa física,
JURIDICA = empresa. O documento segue a política de identificação: um CNPJ
(empresa) chega completo e formatado (ex.: `27.506.088/7001-24`), porque é
dado público de registro; um CPF chega limitado aos 3 primeiros dígitos
(ex.: `390.***.***-**`) — nunca tente adivinhar ou completar o número.
Para contas grandes, percorra as páginas com `offset` enquanto `hasNext` for verdadeiro;
não prometa "todos" de uma vez, o limite por página é 30.

## Cadastro de cliente novo — consultar antes de escrever

Só cadastre quando o usuário **pedir explicitamente** o cadastro (ex.: "cadastra
um cliente novo"). Antes de qualquer escrita, a própria ferramenta consulta se
o cliente já existe — e você deve conduzir a conversa no mesmo espírito:

1. **Recolha os dados essenciais**: nome completo e, se o usuário tiver,
   CPF/CNPJ e e-mail. Não peça mais que isso e nunca invente dados.
2. **Deixe a ferramenta deduplicar**: `asaas_customers_create` consulta por
   documento, e-mail e nome antes de escrever.
   - Documento que já existe: a ferramenta **recusa sempre** e devolve o
     candidato existente. Use o cliente existente; não insistir.
   - E-mail ou nome parecido: a ferramenta recusa com os candidatos e pede
     confirmação. Só repita com `confirmedDistinct: true` depois que o
     **usuário** confirmar que é um cliente diferente.
3. **Aguarde o card de aprovação**: o cadastro é uma escrita real na conta de
   produção e exige aprovação explícita na conversa. Nunca prometa o cadastro
   como automático.
4. **Reporte com honestidade**: em sucesso, o resultado traz o cliente criado
   com o documento sob a política de identificação (CNPJ completo; CPF nos 3
   primeiros dígitos). Em timeout, consulte se o cadastro aconteceu antes
   de tentar de novo — a própria mensagem da falha orienta isso.

Detalhes completos de argumentos, recusas e códigos de falha:
[references/customers-create.md](references/customers-create.md).

## Limites honestos

- As respostas trazem id, nome, tipo de pessoa, e-mail e documento (CNPJ
  completo; CPF nos 3 primeiros dígitos).
  Telefone, endereço, observações e referências externas não entram no
  contexto do modelo. Se o usuário precisar desses dados, oriente o painel
  do ASAAS.
- O cadastro envia apenas nome, CPF/CNPJ e e-mail — endereço, telefone e
  outros campos ficam para o painel do ASAAS.
- Não há como editar ou remover cliente por aqui. Se o usuário pedir,
  explique o limite e ofereça o painel.

## Quando a ferramenta não existe

Se `asaas_customers_list` ou `asaas_customers_create` não estiverem
disponíveis, o plugin ASAAS está desabilitado ou esta versão do Genius ainda
não as oferece. Oriente o usuário a ativar o plugin ASAAS nas extensões do
Genius ou atualizar o aplicativo. Não contorne a ausência chamando a API por
shell, script ou outra ferramenta: a chave de produção não pode transitar
pelo prompt.
