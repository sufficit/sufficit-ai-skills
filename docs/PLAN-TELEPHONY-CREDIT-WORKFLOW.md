# Fluxo de compra de crédito telefônico para agentes

Objetivo: consolidar as definições do mantenedor nesta sessão: “lançar saldo” significa comprar crédito telefônico; recebimentos financeiros são exclusivamente das integrações. Separar compra avulsa, comprometimento e recorrência, preservando histórico e identidades de operações.

1. [concluído] Atualizar a sufficit-api com referência de telefonia, roteamento de intenção e contrato de comprometimento manual/roles já publicados.
2. [concluído] Incrementar versão e digest do pacote; validar integridade, catálogo, Markdown e testes existentes.
3. [concluído] Registrar evidências, conferir alterações e fazer commit/push na main somente dos arquivos desta tarefa.

Aceite: não perguntar se “lançar saldo” significa recebimento/benefício; não registrar recebimento manual; não criar serviço substituto para compensar operação incerta; não inferir recorrência da validade; consultar e verificar compras reais, preservando recibos. Conferir API publicada antes de usar rotas; não inventar fluxo indisponível. Nenhuma escrita em clientes ou alteração de agentes/bindings faz parte deste trabalho.

Validação: python3 scripts/validate.py; python3 scripts/build_skill_index.py --check; python3 scripts/catalog_versions.py --check; python3 scripts/markdown_coverage.py; python3 -B -m unittest discover -s tests -v; git diff --check. Sem painel nativo de tarefas disponível; este arquivo acompanha a execução.

Validação local concluída: 185 pacotes íntegros, índice e versões alinhados, todos os documentos alcançáveis e 45 testes existentes passaram. Pacote sufficit-api 1.0.34. Não houve teste comportamental em agente conectado nem operação em cliente.

Entrega: main a2477ee1080d2c9de659ecc2867b55bf378254a1 enviada; CI Validate skills 42877451102 concluído com sucesso, incluindo notify-genius. Sincronização de catálogo Genius 42877531117 iniciada em seguida e observada na fila; adoção em sessões ativas não foi verificada.
