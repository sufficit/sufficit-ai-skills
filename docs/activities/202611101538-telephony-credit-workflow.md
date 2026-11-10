# Significado de lançar saldo e histórico de serviços tarifados

Definições explícitas do mantenedor nesta sessão: “lançar saldo” significa comprar crédito telefônico; recebimentos financeiros são sempre registrados pelas integrações e ficam fora das operações dos agentes.

Atualizada sufficit-api de 1.0.33 para 1.0.34: regra no entrypoint e descrição para descoberta; nova referência de telefonia; referências de carteira genérica e vendas encaminham ao fluxo correto. Compra avulsa, comprometimento e compra recorrente são efeitos distintos. Regras de compra usam o writer coordenado e sua identidade estável, conferem serviço/débito/crédito entregue e não recriam serviços para compensar resultados incertos. Validade do crédito não define periodicidade; crédito comum não substitui silenciosamente 0800. Inclusão inicial e recorrência dependem das operações efetivamente disponíveis, sem inventar rotas ou migração implícita.

Incluído o comprometimento manual já publicado: Confirm sem rascunho, valor positivo, ciclo de 1 a 12 meses, aniversário explícito na criação/reativação, papéis manager/salesmanager/administrator e leitura independente. O acordo não compra crédito, cria débito ou ativa recorrência.

Schema e comportamento conferidos em CallCreditPurchaseController/Runtime, CallCreditPurchaseRequest, SalesRecordHttpGateway e documentação de recorrência/settlement dos repositórios EndPoints/Base/Standard/EFData. Essas fontes orientam a referência; o OpenAPI implantado continua sendo autoridade para a execução real.

Digest, versão do catálogo, cartão da skill e índice atualizados. Validações locais: 185 pacotes íntegros; índice e versões atualizados; Markdown totalmente alcançável; 45 testes existentes passaram; diff sem erros de espaço. Não foram criados testes que apenas conferem o texto das instruções. Sem teste comportamental conectado: essas verificações não comprovam mudança de comportamento dos agentes nem adoção do pacote. Nenhuma escrita em clientes, recebimentos, serviços, roles ou bindings.

Entrega acompanhada no [plano](../PLAN-TELEPHONY-CREDIT-WORKFLOW.md). O pipeline valida o push e solicita a sincronização do catálogo do Genius; publicar no repositório não comprova instalação em sessões ativas.
