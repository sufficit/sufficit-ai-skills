# Teste de conexão ASAAS

A ferramenta `asaas_connection_test` não aceita argumentos. Ela resolve
`personal/asaas/production/api-key` no Vault pessoal, injeta a chave apenas no
cabeçalho `access_token` de uma requisição feita pelo host confiável e nunca
devolve a chave, o corpo do provedor ou dados da conta.

## Resultado de sucesso

| Campo | Valor |
| --- | --- |
| `connected` | `true` |
| `authenticated` | `true` |
| `provider` | `asaas` |
| `environment` | `production` |
| `check` | `myAccount/status` |
| `method` | `GET` |
| `httpStatus` | `200` |
| `credentialReference` | `personal/asaas/production/api-key` |
| `writesPerformed` | `false` |

Informe ao usuário, em linguagem simples, que a conta está conectada e que o
teste não alterou nada na conta.

## Códigos de falha

| Código | Significado | Ação |
| --- | --- | --- |
| `asaas_vault_sign_in_required` | O usuário não está autenticado no Sufficit Identity. | Peça para entrar na conta Sufficit e repita o teste. |
| `asaas_key_missing` | A entrada ainda não existe ou está vazia no Vault. | Prepare `personal/asaas/production/api-key` com a tela segura de Vault e repita depois de o usuário salvar a chave. |
| `asaas_key_invalid` | A chave salva tem formato inválido para autenticação HTTP. | Peça ao usuário para gerar uma nova chave no painel do ASAAS e salvar na mesma entrada do Vault. |
| `asaas_credential_rejected` | O ASAAS rejeitou a chave (HTTP 401/403). | A chave está errada ou foi revogada; peça uma chave válida, salve no Vault e repita uma única vez. |
| `asaas_provider_unavailable` | O ASAAS respondeu, mas não concluiu o teste. | Falha do provedor; informe o usuário e, se marcada repetível, refaça o teste após uma espera. |
| `asaas_transport_failed` | A API de produção não foi alcançada. | Problema de rede; verifique a conexão e repita. |
| `asaas_timeout` | O teste excedeu o tempo limite. | Repita uma vez; se persistir, trate como indisponibilidade. |
| `asaas_vault_timeout` | O acesso ao Vault excedeu o tempo limite. | Repita uma vez; se persistir, trate como indisponibilidade do Identity. |
| `asaas_vault_unavailable` | O Vault não pôde ser acessado. | Indisponibilidade do Identity; tente novamente depois. |

Falhas marcadas como repetíveis no resultado podem ser tentadas de novo com
parcimônia: uma nova tentativa, aguardando um instante. Falhas não repetíveis
exigem uma ação do usuário antes de qualquer nova chamada.

Nunca use uma operação de escrita — criar cobrança, pagamento, cliente ou
qualquer alteração — para diagnosticar a conexão.
