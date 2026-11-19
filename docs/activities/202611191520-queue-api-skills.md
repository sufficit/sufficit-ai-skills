# Gestão de filas pela API nas skills de telefonia

1. [completed] Atualizar as referências de plano de discagem e onboarding para
   usar EndPoints com a credencial do operador. Manter o helper Fleet isolado para
   instalações que ainda o provisionam.
2. [completed] Atualizar versões e catálogo. Rodar os validadores, a suíte do
   repositório e conferir o contrato de filas no OpenAPI publicado.
3. [completed] Registrar a entrega, enviar à main e verificar o CI e a propagação
   no catálogo Genius.

Os 196 pacotes, índice, versões, links Markdown e 70 testes passaram. O
OpenAPI v2 publicado confirmou os métodos documentados de catálogo,
gestão de atendentes, nós, monitoramento, ingresso e busca de agentes.

As skills passaram para `sufficit-telephony-dialplan` 0.8.2 e
`sufficit-telephony-extensions` 0.8.3 no commit `9abdaaf`. O catálogo
público do Genius retornou as duas versões e a revisão de origem
`9abdaaffd2d00c36cb7667eaf9007c7d2ed60209`.

- [CI do sufficit-ai-skills](https://github.com/sufficit/sufficit-ai-skills/actions/runs/44585989950)
- [Publicação do catálogo Genius](https://github.com/sufficit/sufficit-ai-genius/actions/runs/44586079528)
