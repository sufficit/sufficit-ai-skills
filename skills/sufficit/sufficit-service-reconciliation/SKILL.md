---
name: sufficit-service-reconciliation
description: "Reconcile Sufficit customer service cycles and financial history: consolidation, false renewal gaps, preferred due days, prepaid posting, representative funding, cancellations and future charges. Use for revisar cliente, consolidar serviços, vigência, conciliação or cobrança de representante. Requires evidence and independent before/after validation; does not authorize new payments, call credit or unrelated code changes."
metadata:
  version: "1.0.0"
  author: "Sufficit"
---

# Reconciliação de serviços Sufficit

Concluir o caso pelo estado verificado do cliente, não por contagem de operações
executadas ou ausência de uma tag. Usar um manifesto de identidades e um plano
persistido por escopo; retomar dos resultados comprovados após interrupções.

## Antes de alterar

Ler observações/comentários e cancelamentos **antes** de renovar ou reconstruir
cobranças. Resolver cliente, representante, serviço e compras por GUID/documento.
Confrontar recibos originais, extratos dos dois responsáveis e histórico/Hermes
quando necessário. Título, valor e mês coincidentes não estabelecem vínculo.

Capturar contratos, períodos, compras/recibos originais, vínculos, classificação,
extratos completos e entregas financeiras pendentes. Separar fatos, hipótese e
decisão autorizada. Uma compra histórica, vigência ativa, pagamento bancário e
crédito na telefonia são quatro fatos diferentes.

## Corrigir a causa certa

- **Vigência:** recorrente nativo por prazo indeterminado mantém `End=null`.
  O fim de cada competência fica no período. Preservar teste, avulso, prazo fixo
  e cancelamento explícitos; não tornar todo contrato antigo pré-pago.
- **Calendário:** preferência/vencimento e início do ciclo são independentes.
  Ler o `CycleDay` explícito. Exemplo comprovado: pagamento26, cobertura27→27.
  Não inferir a competência histórica pelo mês UTC de emissão nem aplicar a
  preferência atual a anos inteiros com outro acordo.
- **Lacunas:** revisar a sequência efetivamente exibida pela UI, inclusive compras
  consolidadas e predecessores. Distinguir fim inclusivo legado, fim exclusivo
  nativo, instante com fuso e data civil. Um padrão28→27 pode ser uma lacuna de
  consolidação; exige recibos consecutivos e âncora, não basta ausência de pausa.
  Corrigir competência revisada pelo comando comercial, preservando datas e valores
  originais. Nunca esconder a linha vermelha ou somar um dia a todos os fins.
- **Futuro:** redatar um débito existente não desfaz sua emissão. Uma projeção não
  emitida deve ficar sem vínculo no extrato, com emissão durável agendada para o
  instante devido. Conferir consumidor, identidade, ordem, disponibilidade e replay
  antes de retirar qualquer linha. Não usar crédito/estorno/recarga para mascarar.
- **Responsável financeiro:** preservar vínculo histórico após cancelamento;
  “não enviar boleto” exige conferir cobrança direta e pagador comprovado. Ambos
  os lados do repasse antecedem estritamente o débito: no padrão ordinário,
  05:59 e06:00 Brasília. Descrição do repasse é `(CONTRAPARTE)` nos dois contextos.
  Mesmo horário com código menor não satisfaz essa regra.
- **Bancos:** EFí/ASAAS com fuso explícito usam esse fuso; sem fuso, assumir GMT−3
  conforme regra do mantenedor. Não converter uma data civil como se fosse UTC.
  Preservar recebimento real; registrar confirmação bancária na descrição somente
  quando o dia for diferente. Originais externos precisam de lastro preservado.

Antes de executar, ler [procedimento e limites](references/procedure.md).
Para detalhe operacional de competência/agenda, ler
[calendário e emissão](references/calendar-and-posting.md).

## Executar sem ampliar o caso

No ambiente API, descobrir rotas no OpenAPI com a skill `sufficit-api`; não usar
esta skill para contornar autenticação ou inventar endpoints. Em manutenção de
engenharia já autorizada, seguir AGENTS.md do repositório, providers comerciais,
gravador financeiro transacional, versões esperadas e chaves idempotentes.
Uma rejeição de domínio deve ser entendida; não remover guardas para aceitar dados.
Não criar método de produto ou alterar regra global apenas para resolver um dado.

Simular e verificar rollback antes do lote; manter exatamente uma etapa em
andamento. Usar cópia privada completa de DLLs em executores, sem symlink para o
runtime live: um deploy paralelo pode trocar dependências no meio da transação.
Após resposta ambígua, reler estado/recibo antes de repetir a mesma operação.

## Aceite obrigatório

1. Releitura independente dos mesmos IDs; conferir vigência, preferência, ciclo,
   próxima renovação, contratos associados e cobertura entre compras.
2. Comparar extratos completos, valores e saldos dos dois contextos. Explicar
   cada diferença autorizada; validar descrições e ordem dos repasses. Nenhum
   pagamento/recarga/estorno novo sem a decisão correspondente.
3. Conferir todas as projeções futuras e suas entregas duráveis, sem vínculo
   financeiro prematuro nem segunda cobrança do ciclo já emitido.
4. Avaliar as mesmas classes de associação/aviso/intervalos da UI. Tag sem aviso
   não prova continuidade, ordem financeira nem serviço operacional em uso.
5. Validar replay comercial e comissões após manutenção contratual. Saúde HTTP
   ou teste unitário sozinho não prova integridade dos contratos reais.
6. Registrar caso, evidência, operações aplicadas, exceções e limite do escopo.
   Só encerrar checkpoints comprovados. Não declarar a carteira inteira concluída.

Executar [o verificador somente leitura](scripts/check_continuity.py) sobre as
capturas e a avaliação produzida pelas classes reais da UI. Ele confere lacunas,
preferência/ciclo, futuros já emitidos e preservação do financeiro/recibos; **não**
substitui autorização, validação do consumidor, telefonia nem revisão de repasses.
Os exemplos e o formato estão em [procedimento](references/procedure.md).
