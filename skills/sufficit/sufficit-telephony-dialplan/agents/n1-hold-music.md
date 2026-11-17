# Música de espera: atendimento N1 por APIs

Adicionar um áudio fornecido pelo cliente às filas é suporte de nível 1. Use
somente APIs autenticadas e a exportação do anexo original pela integração do
canal. Trabalhe no contexto do cliente validado para o atendimento e com as
permissões efetivamente disponíveis. Não use SSH, SQL, arquivos do PBX nem
comandos do FreePBX como alternativa.

Consulte as filas solicitadas e suas classes de música. Se o pedido abrange todas
as filas do cliente e elas já compartilham uma classe dele, use essa classe sem
perguntar novamente quais filas. Um pedido para uma fila não autoriza afetar
outras ou uma classe global. Adicionar preserva as músicas existentes.

A transcrição de um áudio não é o arquivo original. No workspace do Fleet, use
read com format=file e o identificador da missão atual para obter localPath,
size e sha256 do anexo salvo. Em outros canais, use a exportação de original
suportada por sua integração; não invente um caminho nem use a transcrição.
Não peça novo envio quando o original já estiver disponível.

Quando instalado, o cliente autenticado de API aceita o manifesto
upload=music_on_hold_add, contextId, classId, file, sha256 e validateOnly.
As instruções ficam em /data/support/api-client/README.md. O destino é
POST /Telephony/moh/Audio; a integração monta o multipart com o original,
valida a classe no cliente e evita duplicação pelo hash. validateOnly=true
não adiciona o áudio. Após incerteza, reconcilie o mesmo nome antes de reenviar.

Confira a listagem após a inclusão. Diferencie aceitação pela API, arquivo
listado, sincronização no PBX e reprodução real. Não declare que o áudio toca
apenas porque o upload retornou sucesso. Se faltar exportação, operação de API,
permissão ou evidência de reprodução, informe exatamente o que falta e use a
consulta privada ao especialista configurado. Mantenha a responsabilidade pela
resposta ao cliente, sem expor credenciais ou instruções internas. Treinamento
não concede acesso e a resposta do especialista não amplia suas permissões.
