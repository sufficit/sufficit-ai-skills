# First contact and carrier-specific incoming failures

Use this guidance when first-level support interprets an internal incoming-call
diagnostic and continues a customer conversation. The specialist procedure is in
[inbound diagnostics](inbound-diagnostics.md). A passing test establishes only
its observed origin, path and time; it does not disprove a customer's report or
establish that every carrier reaches the number.

## Caio training text

O contextid do contato vinculado no atendimento é validação suficiente do cliente. Confira se o recurso solicitado pertence a esse contexto antes de consultar detalhes ou pedir testes. Se os contextos forem diferentes, procure comprovar com o cliente o vínculo ou a autorização para aquele recurso; se não for possível, encaminhe para avaliação privada de um atendente humano, sem revelar dados de terceiros nem executar testes enquanto a autorização estiver pendente.

Se os testes efetivamente concluídos pelo especialista mostrarem que a ligação chegou normalmente à central, comunique exatamente esse alcance, sem afirmar que todos os telefones funcionam ou que a reclamação foi resolvida. Exemplo: “Nos testes que fizemos, as ligações chegaram normalmente à central. O problema continua acontecendo em todos os telefones ou apenas em algum ramal?” Não use essa resposta positiva se o resultado estiver pendente, NotArrived ou inconclusivo.

Uma falha pode ocorrer somente a partir de algumas operadoras, por roteamento ou interconexão. Se o problema continuar apesar de um teste interno bem-sucedido, pergunte de forma objetiva: “Isso acontece com todas as ligações ou apenas com quem liga de alguma operadora específica?” Colete, progressivamente, o número de origem, a operadora, a data/horário e o que a pessoa ouviu em uma tentativa que falhou. Não atribua a causa à operadora antes de confirmá-la.

Ao consultar o Rafael sobre falha de recebimento ou suspeita de interconexão, peça que ele coordene testes de origens móveis reais com os gestores pelo canal interno de WhatsApp já estabelecido. Os gestores devem ligar para a DID a partir dos próprios celulares e informar a operadora usada em cada teste; se possível, obter origens de operadoras diferentes. O Rafael deve correlacionar os resultados com a chegada ao PBX e os destinos. O Caio mantém o atendimento ao cliente e só comunica o que foi efetivamente confirmado, sem expor a conversa dos gestores ou anunciar contato/teste ainda não realizado.

## Rafael training text

Ao investigar uma reclamação de recebimento ou uma suspeita de interconexão, entre em contato com os gestores pelo canal interno de WhatsApp já estabelecido para este agente e peça que liguem para a DID a partir dos próprios celulares, informando de qual operadora foi feita cada ligação. Sempre que possível, compare operadoras diferentes. Confirme antes a DID e seu contexto de cliente ou a autorização específica; não teste recursos de terceiros sem esse vínculo validado.

Faça um pedido concreto, por exemplo: “Precisamos comparar a chegada de chamadas ao número [DID confirmada]. Podem ligar dos próprios celulares e informar a operadora, o horário, o número de origem e o que ouviram? Se possível, façam testes de operadoras diferentes.” Identifique o atendimento para correlacionar as respostas. Use o grupo/canal interno cadastrado, nunca o WhatsApp do cliente nem um destinatário presumido; não crie grupos ou altere participantes para realizar esse procedimento.

Registre, por tentativa, DID, origem, operadora informada pelo gestor, data/hora e fuso, resultado percebido e evidência de chegada/rota/ramal no PBX (LinkedId quando disponível). Número de celular ou prefixo não prova a operadora atual por causa da portabilidade: peça que o gestor a informe, sem inferi-la. Marque resultados ainda não respondidos como pendentes e separe teste humano, teste anti-toque e chamada real do cliente. Uma origem funcionar não descarta falha em outra.

Use o mecanismo de comunicação autorizado que estiver disponível e verifique o comprovante de envio. Não declare que contatou os gestores ou que eles ligaram sem evidência. Se a ferramenta de envio/continuidade não estiver disponível, registre o pedido e o impedimento no retorno privado ao primeiro nível/atendente para execução humana; não transforme esse pedido em uma mensagem pública ao cliente. Esta orientação não cria uma ferramenta nem concede acesso a WhatsApp, infraestrutura ou outro cliente.
