# Emissão (agendamento) de nota fiscal ASAAS

A ferramenta `asaas_invoices_create` agenda uma NFS-e nova na conta de
produção via `POST /v3/invoices`. Ela exige aprovação explícita na conversa e
executa **consultar antes de escrever em código**: deduplica por cobrança e
por cliente+valor+data antes do POST, e só aceita serviço municipal
existente.

## Pré-requisitos (nesta ordem)

1. O usuário pediu explicitamente a nota.
2. A origem é conhecida: `payment` (cobrança), `installment` (parcelamento)
   ou `customer` (nota avulsa) — **exatamente uma**.
3. O serviço foi escolhido com o usuário: `municipalServiceId` do catálogo
   (`asaas_services_list`) **ou** `municipalServiceCode` informado pelo
   usuário (Portal Nacional) — **exatamente um**.

## Argumentos

| Argumento | Tipo | Obrigatório | Regras |
| --- | --- | --- | --- |
| `customer` / `payment` / `installment` | string | exatamente um | Ids ASAAS (`cus_...`, `pay_...`). |
| `value` | number | sim | Valor total em reais; entre 0,01 e 999.999.999,99. |
| `serviceDescription` | string | sim | Descrição impressa na nota; 1 a 200 caracteres. |
| `effectiveDate` | string | sim | Data de emissão AAAA-MM-DD. |
| `municipalServiceId` | string | um dos dois | Id do catálogo municipal. |
| `municipalServiceCode` | string | um dos dois | Código dado pelo usuário (Portal Nacional). |
| `municipalServiceName` | string | não | Nome do serviço; até 80 caracteres. |
| `observations` | string | não | Observações impressas; até 200 caracteres. |
| `confirmedDistinct` | boolean | não | `true` só após o usuário confirmar colisão cliente+valor+data como nota distinta. |

Impostos não são enviados: `taxes` segue a configuração fiscal da conta.

## Recusas (escrita não realizada)

Resultado com `scheduled: false` e `writesPerformed: false` é recusa, não
erro. Nenhum POST aconteceu.

| `reason` | Causa | Conduta |
| --- | --- | --- |
| `duplicate_payment` | A cobrança já tem nota fiscal. | Use a nota existente devolvida. Nunca insista, nem com `confirmedDistinct`. |
| `possible_duplicate` | Mesmo cliente, valor e data de nota existente. | Apresente a nota existente; só repita com `confirmedDistinct: true` se o usuário confirmar que é outra nota. |

## Resultado de sucesso

| Campo | Valor |
| --- | --- |
| `scheduled` | `true` |
| `writesPerformed` | `true` |
| `emissionIsAsync` | `true` — agendar inicia o fluxo; autorização vem depois |
| `invoice` | Nota sanitizada (`id`, `status` SCHEDULED, `value`, `effectiveDate`, ids vinculados; sem URLs) |
| `dedupPerformed` | `true` |

**Sempre reporte honestamente**: "nota agendada; a emissão está em
processamento pela prefeitura". Autorização se confirma consultando o status
depois (AUTHORIZED).

## Códigos de falha

| Código | Ação |
| --- | --- |
| `asaas_invoices_create_invalid_arguments` | Origem ausente/duplicada, serviço ausente/duplicado, valor/datas inválidos. Corrija; nada foi chamado. |
| `asaas_invoices_create_rejected` | Provedor recusou (mensagem traz código+descrição, ex.: serviço municipal inválido). Corrija com o usuário. |
| `asaas_invoices_create_unexpected` | Agendou mas a resposta veio estranha; consulte a lista de notas para confirmar. |
| `asaas_timeout` | **Consulte se a nota foi criada antes de repetir.** |
| Demais (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_provider_unavailable`, `asaas_transport_failed`) | Fluxo padrão das skills ASAAS. |

## Fluxo recomendado

```
usuário pede a nota
        │
        ▼
descobrir origem (payment/installment/customer) e serviço
(histórico de notas + catálogo municipal — JAMAIS criar serviço)
        │
        ▼
asaas_invoices_create (origem, valor, descrição, data, serviço)
        │
        ├─ duplicate_payment ──► use a nota existente
        ├─ possible_duplicate ──► confirme com o usuário
        │                             └─ confirmou? confirmedDistinct=true
        └─ card de aprovação ──► scheduled:true ──► "agendada, emissão em processamento"
```
