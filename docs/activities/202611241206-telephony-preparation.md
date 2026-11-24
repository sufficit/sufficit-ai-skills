# Onboarding telefônico sem serviços contratados

A skill de ramais 0.10.4 orienta a consultar e preparar o cliente pela API de
telefonia, confirmar o contexto por releitura e só então obter o título na
prévia de ramal. O preparo aceita clientes cadastrados sem serviços. A etapa
de DID depende da disponibilidade de uma linha do próprio cliente e do escopo
autorizado. O roteiro trata indisponibilidade da nova rota como preparação
pendente para a versão instalada.
[Roteiro do agente](../../skills/sufficit/sufficit-telephony-extensions/references/customer-onboarding.md).

Validação em cópia limpa com os arquivos da entrega. Passaram a validação da
skill, dos 214 pacotes públicos, do índice, das versões, da cobertura Markdown
e 70 testes de repositório. O digest do pacote financeiro foi atualizado para
refletir o commit já existente 6eb0467 e liberar a validação do catálogo.

A entrega da skill requer a sincronização normal do catálogo Genius. O fluxo
operacional requer a versão do EndPoints que expõe a nova preparação.
