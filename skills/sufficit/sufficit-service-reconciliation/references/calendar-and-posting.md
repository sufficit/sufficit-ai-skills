# Calendário, datas e emissão

## Quatro eixos

| Eixo | Exemplo | Conferência |
|---|---|---|
| Contrato recorrente | sem término | Não usar fim mensal como End |
| Competência |27/10–27/11, fim exclusivo | Seguir CycleDay comprovado |
| Vencimento preferencial |26/10 | Não substituir início/fim por26 |
| Emissão financeira |27/10 06:00 Brasília | Repasse05:59; não comprova pagamento |

Datas civis em DTOs podem vir com `Z` por convenção de serialização; isso não as
transforma em instantes. Não subtrair3h dessas datas. Instantes de banco/ledger
exigem offset/fuso. Preservar os dois valores quando uma leitura SQL divergir da
leitura do provider, até esclarecer o tipo da coluna e a sessão.

Uma compra histórica28/09→27/10 não deve automaticamente virar28/09→28/10.
No caso comprovado por recibos e sucessor27/11, com ciclo27 e vencimento26, a
competência revisada é27/09→27/10. Guardar essa competência nos campos de revisão,
sem sobrescrever Start/End/Amount originais. Uma mudança de calendário antiga
ou uma pausa real pode interromper o bloco: não atravessar essa fronteira.

## Não confundir agenda com lançamento

Mover um débito03/11 para27/11 deixa uma linha efetivada futura no extrato. Para
uma renovação ainda não emitida, reconciliar o produtor/consumidor durável e os
dois lados do financiamento antes de retirar registros internos errados.
Não apagar recibo bancário nem alterar uma intenção imutável já entregue.
Um recebimento antecipado legítimo precisa de evidência própria; não é equivalente
a uma emissão interna prematura de serviço.

O runtime deve efetivamente respeitar a agenda. Confirmar a indisponibilidade
antes do instante, predecessor, consumidor, payload congelado e replay sem
transferência duplicada. Não deixar cron manual sem responsável como substituto.

`NativePeriodPostingUtc` tradicionalmente converte meia-noite civil para
meia-noite Brasília. Não supor que uma fila disponível06:00 muda essa conversão.
Uma correção com Billing/PostingDate explícito09:00Z conserva06:00 Brasília na
regra atual. Conferir a versão real do consumidor; não copiar essa convenção para
outras modalidades sem confirmar. A antecedência de um minuto no financiamento
foi implementada em Standard95dcf2d,14/11/2026; conferir disponibilidade no runtime.

Intenção equivocada ainda não tentada pode exigir cancelamento da entrega e
substituição aditiva, com avanço explícito sem efeito no receptor. Preservar
intenção/recibo original e versões; nunca escrever um novo payload sobre um evento
que já recebeu identidade durável. Essa manutenção é excepcional, não receita
para fabricar intenções financeiras via SQL.

Se houver cancelamento antes da execução, revisar também entregas já agendadas;
encerrar o contrato sozinho não comprova que a fila deixou de executar.
