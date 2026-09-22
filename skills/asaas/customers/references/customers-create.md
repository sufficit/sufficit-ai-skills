# Cadastro de cliente ASAAS

A ferramenta `asaas_customers_create` cadastra um cliente novo na conta de
produção. Ela exige aprovação explícita na conversa (card de aprovação) e
executa a regra **consultar antes de escrever em código**: antes do POST ela
consulta `/v3/customers` por documento, e-mail e nome, e se recusa a escrever
quando encontra duplicatas. A chave `personal/asaas/production/api-key` sai do
Vault direto para o cabeçalho `access_token`; a resposta chega sanitizada com
o documento mascarado nos 3 últimos dígitos.

## Quando usar

Somente quando o usuário pediu explicitamente para cadastrar um cliente novo.
Não ofereça o cadastro por iniciativa própria e nunca cadastre como efeito
colateral de outra tarefa.

## Argumentos

| Argumento | Tipo | Obrigatório | Regras |
| --- | --- | --- | --- |
| `name` | string | sim | Nome do cliente; 1 a 80 caracteres. |
| `cpfCnpj` | string | não | CPF (11 dígitos) ou CNPJ (14 dígitos); pontuação é ignorada. |
| `email` | string | não | E-mail; até 64 caracteres. |
| `confirmedDistinct` | boolean | não | `true` somente quando o usuário já confirmou que a colisão de nome/e-mail é outro cliente. Nunca sobreponde uma coincidência de documento. |

O envio ao provedor leva apenas `name`, `cpfCnpj` (dígitos) e `email` — nada
mais. Endereço, telefone e complemento ficam para o painel do ASAAS.

## Recusas (escrita não realizada)

O resultado com `created: false` e `writesPerformed: false` é uma recusa, não
um erro. Nenhum POST aconteceu.

| `reason` | Causa | Conduta |
| --- | --- | --- |
| `duplicate_document` | Já existe cliente com o CPF/CNPJ informado. | Use o cliente existente devolvido em `existingCustomer`. Não repita a criação, nem com `confirmedDistinct`. |
| `possible_duplicate` | Colisão de e-mail ou nome sem confirmação. | Apresente os candidatos (`dedupMatches`) e pergunte ao usuário. Só repita com `confirmedDistinct: true` se ele confirmar que é outro cliente. |

## Resultado de sucesso

| Campo | Valor |
| --- | --- |
| `created` | `true` |
| `writesPerformed` | `true` |
| `customer` | Cliente criado sanitizado (`id`, `name`, `personType`, `email`, `document` mascarado) |
| `dedupPerformed` | `true` — a consulta de duplicatas rodou antes da escrita |
| `credentialReference` | `personal/asaas/production/api-key` |

## Códigos de falha

| Código | Significado | Ação |
| --- | --- | --- |
| `asaas_customers_create_invalid_arguments` | Nome vazio/longo, documento fora de 11/14 dígitos, e-mail longo. | Corrija os argumentos e repita; nada foi chamado. |
| `asaas_customers_create_rejected` | O ASAAS recusou o cadastro (ex.: CPF inválido). | A mensagem traz código e descrição do provedor; corrija com o usuário e tente de novo. |
| `asaas_customers_create_unexpected` | Criação confirmada, mas resposta em formato inesperado. | Consulte a lista de clientes para confirmar o estado real. |
| `asaas_timeout` | Tempo limite excedido. | **Consulte se o cliente já foi criado antes de repetir**; a escrita pode ter acontecido. |
| `asaas_credential_rejected` | Chave rejeitada (401/403). | Peça chave válida e salve no Vault. |
| `asaas_provider_unavailable` / `asaas_transport_failed` / `asaas_vault_*` | Falhas compartilhadas das demais ferramentas ASAAS. | Siga a mesma conduta da consulta. |

## Fluxo recomendado

```
usuário pede cadastro
        │
        ▼
asaas_customers_create (name, cpfCnpj?, email?)
        │
        ├─ duplicate_document ──► use o cliente existente
        ├─ possible_duplicate ──► pergunte ao usuário
        │                              └─ confirmou? repita com confirmedDistinct=true
        └─ card de aprovação ──► created:true ──► reporte com documento mascarado
```

Nunca contorne uma recusa chamando a API por outro caminho; a recusa é a
ferramenta protegendo a conta de produção contra duplicatas.
