# Contatos

## Identidade e descoberta

Contatos são identificados exclusivamente por GUID. Pesquise no OpenAPI vivo por
`contact search`, `contact attribute`, `contact important` ou `contact delete`
antes de chamar. Use o contexto do usuário autenticado por padrão; informe
`contextId` somente quando o usuário escolheu claramente outro contexto que ele
tem permissão para gerir.

As chaves usuais de atributo são:

| Informação | `key` | Uso de `value` e `description` |
| --- | --- | --- |
| Nome/título | `titulo` | nome em `value` |
| E-mail | `email` | endereço em `value`; rótulo opcional em `description` |
| Telefone | `phone` | número em `value`; tipo como `cellular` ou `business` em `description` |
| CPF/CNPJ | `cadastro` | documento em `value` |
| Marcador | `marcador` | categoria em `value`; marcador em `description` |
| Proprietário | `idproprietario` | vínculo gerido pelo servidor na criação |

Não invente chaves para dados conhecidos. Preserve a grafia recebida em atributos
customizados existentes.

## Pesquisar e conferir

Prefira `POST /Contact/Search`, pois aceita filtros e projeção de atributos. Uma
pesquisa textual típica tem esta forma, adaptada ao contexto e ao pedido:

```json
{
  "contextId": "GUID-DO-CONTEXTO",
  "value": {
    "text": "termo",
    "exactmatch": false,
    "keys": ["titulo", "email", "phone", "cadastro"]
  },
  "keys": ["titulo", "email", "phone", "cadastro", "marcador"],
  "limit": 20
}
```

Para um GUID conhecido, use `contactId` e limite 1. Resposta `204` significa que
nada foi encontrado no escopo consultado. Não conclua que o contato não existe em
todos os contextos e não amplie a busca sem autorização.

Antes de alterar, marcar ou excluir, recupere o contato e confirme GUID, título e o
atributo relevante. Se nome, telefone ou e-mail corresponder a várias pessoas,
apresente as opções e não escolha sozinho.

## Criar e atualizar

`POST /Contact` cria quando `id` é o GUID vazio e atualiza quando recebe um GUID
existente. O corpo contém `attributes`, cada um com `key`, `value` e
`description`. Na criação, o servidor gera o GUID e adiciona o proprietário da
sessão. Inclua pelo menos `titulo` e somente os dados solicitados.

Para editar um atributo isolado, prefira
`POST /Contact/Attribute?contactid=...` com corpo como:

```json
{
  "key": "email",
  "value": "pessoa@example.com",
  "description": "trabalho"
}
```

Essa operação identifica um atributo pela combinação de `key` e `description`.
Leia o valor existente antes: mudar a descrição pode criar outro atributo em vez
de renomear o anterior. Para remoção pontual, descubra e use
`DELETE /Contact/Attribute` com `contactid`, `key` e `description` exatos. Não use
valor vazio como atalho para exclusão.

Quando a atualização integral por `POST /Contact` for necessária, preserve os
atributos existentes que não fazem parte do pedido. O endpoint adiciona ou altera
os atributos enviados, mas o agente não deve tratar uma resposta curta como prova
de que toda a ficha permanece correta; releia o contato após a escrita.

## Importância e exclusão

`POST /Contact/Important` recebe `contactid`, `status` e uma descrição opcional.
Marcar como importante protege o contato contra exclusão comum. Ao remover uma
marcação, use a mesma descrição quando ela existir e valide o estado depois.

`DELETE /Contact?contactid=...` remove permanentemente todos os atributos do
contato. Execute apenas quando o usuário pedir exclusão, depois de uma leitura
imediata que confirme o alvo exato. Informe que é permanente e obtenha confirmação
se o pedido inicial não demonstrar ciência disso. Não remova automaticamente a
marcação de importante para fazer a exclusão passar. Administradores podem ignorar
essa proteção no servidor, portanto a conferência prévia continua obrigatória.

Após qualquer escrita, faça nova pesquisa pelo GUID e reporte o estado observado.
Minimize CPF/CNPJ, telefones, endereços e e-mails na resposta ao usuário.
