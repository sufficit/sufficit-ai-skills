# Teste de registro SIP na skill de telefonia

A versão 0.8.0 da skill [sufficit-telephony-dialplan](../../skills/sufficit/sufficit-telephony-dialplan/SKILL.md) orienta a testar o REGISTER temporário de uma interconexão do cliente. A [referência de operação](../../skills/sufficit/sufficit-telephony-dialplan/references/sip-registration-test.md) descreve autorização do destino, preservação de contatos ativos, histórico e retirada, prazos do modo síncrono, uso da chave idempotente, respostas 202 e 200 e recuperação pelo GET após avisos do WebSocket.

O conteúdo foi conferido com o contrato do EndPoints em d77d760. A referência exige confirmar a disponibilidade do modo assíncrono no OpenAPI ativo. A atualização se limita à skill e ao catálogo.

Validação local concluída para os 195 pacotes, índice, versões, cobertura Markdown e 70 testes.
