# Emissão (agendamento) de nota fiscal ASAAS

A ferramenta `asaas_invoices_create` agenda uma NFS-e nova na conta de
produção via `POST /v3/invoices`. Ela exige aprovação explícita na conversa e
executa **consultar antes de escrever em código**: deduplica por cobrança e
por cliente+valor+data antes do POST.

## Pré-requisitos (nesta ordem)

1. O usuário pediu explicitamente a nota.
2. A origem é conhecida: `payment` (cobrança), `installment` (parcelamento)
   ou `customer` (nota avulsa) — **exatamente uma**.
3. O serviço municipal **não é enviado por padrão** — regra operacional desta
   conta (ver "Serviço cadastrado versus descrição da nota" no SKILL.md).
   Omita `municipalServiceId` e `municipalServiceCode`. Só envie um deles
   quando o usuário escolher explicitamente outro serviço para aquela nota.
   Se o provedor recusar a nota, apresente o motivo real ao usuário, reporte
   a divergência à equipe e nunca adivinhe código.

## Argumentos

| Argumento | Tipo | Obrigatório | Regras |
| --- | --- | --- | --- |
| `customer` / `payment` / `installment` | string | exatamente um | Ids ASAAS (`cus_...`, `pay_...`). |
| `value` | number | sim | Valor total em reais; entre 0,01 e 999.999.999,99. |
| `serviceDescription` | string | sim | Descrição impressa na nota; 1 a 200 caracteres. |
| `effectiveDate` | string | sim | Data de emissão AAAA-MM-DD. |
| `municipalServiceId` | string | **não** | Id do catálogo; só quando o usuário escolher um serviço específico. Nunca junto com `municipalServiceCode`. |
| `municipalServiceCode` | string | **não** | Código, só quando o usuário informar um explicitamente. Nunca junto com `municipalServiceId`. |
| `municipalServiceName` | string | não | Nome do serviço; até 80 caracteres. |
| `observations` | string | não | Observações impressas; até 200 caracteres. |
| `confirmedDistinct` | boolean | não | `true` só após o usuário confirmar colisão cliente+valor+data como nota distinta. |

Serviço e impostos: a emissão não envia `municipalServiceId`,
`municipalServiceCode` nem `taxes` — os detalhes do serviço são **auto
preenchidos pelo cadastro de serviços e pela configuração fiscal da conta**
quando não especificados (regra combinada com o dono). A documentação oficial
([guia](https://docs.asaas.com/docs/emitindo-notas-fiscais-de-servico) e
[referência do endpoint](https://docs.asaas.com/reference/agendar-nota-fiscal))
sustenta a omissão: o schema **não** lista `municipalServiceId`/
`municipalServiceCode` como obrigatórios e declara os preenchimentos
automáticos de `municipalServiceName` (usa o código) e de
`pisCofinsRetentionType` (calculado pelo Asaas); a narrativa do guia, para
integrações genéricas, pede id ou código sem descrever o auto preenchimento
pela conta. Enviar os dois campos de serviço ao mesmo tempo devolve
`asaas_invoices_create_invalid_arguments` sem nenhum POST, e nenhuma recusa se
preenche às cegas: apresente o motivo real do provedor e reporte à equipe.

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
| `asaas_invoices_create_invalid_arguments` | Origem ausente/duplicada, os dois campos de serviço ao mesmo tempo, valor/datas inválidos. Corrija; nada foi chamado. |
| `asaas_invoices_create_rejected` | Provedor recusou (mensagem traz código+descrição, ex.: serviço municipal inválido). Corrija com o usuário. |
| `asaas_invoices_create_unexpected` | Agendou mas a resposta veio estranha; consulte a lista de notas para confirmar. |
| `asaas_timeout` | **Consulte se a nota foi criada antes de repetir.** |
| Demais (`asaas_vault_*`, `asaas_credential_rejected`, `asaas_provider_unavailable`, `asaas_transport_failed`) | Fluxo padrão das skills ASAAS. |

## Fluxo recomendado

```
usuário pede a nota
        │
        ▼
descobrir origem (payment/installment/customer)
(a emissão NÃO especifica serviço — valores vêm do cadastro da conta)
        │
        ▼
asaas_invoices_create (origem, valor, descrição, data)
        │
        ├─ duplicate_payment ──► use a nota existente
        ├─ possible_duplicate ──► confirme com o usuário
        │                             └─ confirmou? confirmedDistinct=true
        └─ card de aprovação ──► scheduled:true ──► "agendada, emissão em processamento"
```
