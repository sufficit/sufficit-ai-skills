---
name: asaas-connection
description: Conecta e testa com segurança a conta de produção do ASAAS a partir da chave guardada no Vault pessoal do Sufficit Identity, usando a ferramenta asaas_connection_test do Sufficit AI Genius. Use quando o usuário pedir para conectar, continuar, verificar ou testar o ASAAS; o teste é somente leitura e não cria cobrança, pagamento ou cliente.
---

# Conexão ASAAS de produção

Use esta orientação quando o usuário pedir para conectar, continuar, verificar
ou testar a conta real do ASAAS.

## Credencial

- A referência canônica é `personal/asaas/production/api-key` no Vault pessoal
  do Sufficit Identity.
- Nunca peça que a chave seja colada na conversa, nunca a inclua em argumento
  de ferramenta, comando, script ou arquivo e nunca mostre cabeçalhos, token,
  corpo do provedor ou dados da conta.
- Se a entrada não existir, use a ferramenta de preparação de Vault do Genius
  (`vault_prepare_entry`) para preparar exatamente essa referência e entregue
  ao usuário a tela segura para colar e salvar a chave. Depois que ele disser
  que salvou, teste a conexão sem pedir o segredo novamente.

## Teste de conexão

Descubra e use `asaas_connection_test`. Essa ferramenta resolve a chave dentro
do host confiável, executa uma única requisição
`GET https://api.asaas.com/v3/myAccount/status` e não segue redirecionamentos
nem lê o corpo da resposta. Ela não cria cobrança, pagamento ou cliente e não
altera a conta.

Considere o teste concluído somente quando o resultado indicar
`connected: true`, `authenticated: true`, HTTP 200 e `writesPerformed: false`.
Informe isso em linguagem simples.

Em falha, identifique o código retornado e siga
[references/connection-test.md](references/connection-test.md). Não tente
outra rota, não repita automaticamente falhas não repetíveis e nunca realize
uma operação financeira para "confirmar" a conexão.

## Quando a ferramenta não existe

Se `asaas_connection_test` não estiver disponível, o plugin ASAAS está
desabilitado ou esta versão do Genius ainda não o oferece. Oriente o usuário a
ativar o plugin ASAAS nas extensões do Genius ou a atualizar o aplicativo. Não
contorne a ausência chamando a API do ASAAS por shell, script ou outra
ferramenta: a chave de produção não pode transitar pelo prompt.
