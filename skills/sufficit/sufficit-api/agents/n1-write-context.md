# Contexto obrigatório nas escritas N1

Antes de QUALQUER escrita no cadastro de um cliente — criação, alteração,
vínculo, troca de senha de ramal, provisionamento, desativação, exclusão ou upload —
use o customerContextId validado do atendimento e a autorização correspondente.
Não confunda com o contexto do Fleet, clientId OAuth, agentId, classId, queueId
ou ID/prefixo do ramal. Nome, prefixo e GUID no texto servem para busca, não
autorizam escolher outro cliente. Não pergunte novamente se o vínculo já resolve.

Leia o recurso ou preview e confirme o proprietário; confira também cada recurso
vinculado, o destino e a conversa de origem do anexo. Mantenha esse mesmo contexto
no path/query/body exigido pela API e no readback. Se a ferramenta já o fixa no
servidor, use o vínculo: não acrescente um parâmetro não suportado nem tente trocá-lo.
O contexto exigido é o do negócio, mesmo em rotas que só recebem o ID do recurso.

Contexto ausente, global, conflitante ou vínculo/atendimento alterado interrompe
a escrita. Não trate erro/resultado vazio como autorização para tentar outro
cliente. Separe lotes por contexto validado; não reaproveite IDs/corpo do cliente
anterior. Relações entre empresas usam seu fluxo autorizado próprio, sem mover
recursos para burlar a validação. Preserve os demais campos; use revisão/If-Match
ou requestId estável quando suportado. Após falha incerta, releia os mesmos IDs.

Prefira ferramentas de domínio com isolamento no servidor. O script público
sufficit-api/scripts/customer_write_guard.py verifica GUIDs, snapshots de dono e
contextos no corpo, e prepara manifesto MOH de WAV canônico em validateOnly.
Ele NÃO autentica snapshots, concede permissão nem envia requisições; nunca
construa um JSON de posse para fingir que o script comprovou acesso. Sem API,
exportação ou permissão, registre a capacidade que falta e mantenha a pendência.
Isso não torna a operação inerentemente humana nem autoriza SSH, SQL ou ações
fora do escopo de telefonia N1.
