# Consultas de leitura da conta ASAAS

Estas duas operações foram verificadas na conta de produção da Sufficit em
2026-09-23 e retornaram **HTTP 200**. O registro descreve consultas reais,
não apenas os códigos de sucesso previstos no schema. Nenhuma nota foi
agendada e nenhum cadastro foi alterado durante a verificação.

## Dados comerciais — identificar a conta

```http
GET https://api.asaas.com/v3/myAccount/commercialInfo
```

- Finalidade: identificar o titular e consultar os dados comerciais atuais.
- Campos úteis para identificação: `companyName`, `name` e `personType`.
- Resultado observado: HTTP 200; a identidade comercial confirmou a conta
  da Sufficit. Não confunda essa identificação com a identificação do
  tomador de uma nota.
- Esta consulta **não identifica o serviço padrão** de Notas Fiscais ›
  Configurações › Serviços.
- Fonte: [Recuperar dados comerciais](https://docs.asaas.com/reference/recuperar-dados-comerciais).

## Informações fiscais — consultar a configuração existente

```http
GET https://api.asaas.com/v3/fiscalInfo/
```

- Finalidade: consultar a configuração fiscal atual antes de tirar
  conclusões sobre a conta ou propor alterações.
- Resultado observado: HTTP 200, com `object: "customerFiscalInfo"`.
- Campos retornados relevantes: `simplesNacional`, `cnae`,
  `specialTaxRegime`, `serviceListItem`, `nbsCode`,
  `nationalPortalTaxCalculationRegime` e `serviceProvisionCityDefaultType`.
  Valores podem ser nulos ou vazios; não complete nem interprete como uma
  escolha fiscal sem evidência.
- `serviceProvisionCityDefaultType` representa a **cidade padrão da
  prestação**, não o serviço padrão. Retornou `null` na consulta observada.
- A resposta observada **não trouxe a lista dos serviços pré-cadastrados
  do painel nem o identificador do serviço marcado como padrão**.
- Segundo a documentação, HTTP 404 significa que não há configuração fiscal
  cadastrada. Informe a ausência; consultar não autoriza criar configuração.
- Fonte: [Recuperar informações fiscais](https://docs.asaas.com/reference/recuperar-informacoes-fiscais).

## Limites da evidência

HTTP 200 confirma que a consulta foi atendida, não que todos os dados
necessários à emissão estão disponíveis ou que algum serviço foi escolhido.
Essas leituras não comprovam preenchimento automático de campos omitidos
no agendamento e não autorizam emitir uma nota para descobrir o padrão.

`GET /v3/fiscalInfo/services` é outra operação: lista serviços **municipais**,
não os serviços pré-cadastrados no painel. Na mesma investigação retornou
HTTP 400, com a mensagem "O código de serviços municipais não está habilitado
para esta conta." Não o registre como consulta bem-sucedida e não interprete
essa recusa como ausência de serviços cadastrados no painel.

## Uso no Genius e proteção de dados

- Estes endpoints são capacidades verificadas da **API do Asaas**. A inclusão
  desta referência na skill **não implementa ferramentas novas no plugin**.
  Na versão inspecionada em 2026-09-23, não havia ferramentas dedicadas a
  essas duas consultas; `asaas_connection_test` consulta `/v3/myAccount/status`
  e não substitui nenhuma delas.
- Descubra se a versão em uso oferece ferramentas correspondentes. Se não
  oferecer, informe o limite e reporte a necessidade à equipe do plugin;
  não invente nomes de ferramentas nem finja que executou a consulta.
- Execute somente leitura, sem body. Não use POST/PUT nem agende uma nota
  como parte da consulta. Não altere configurações para resolver uma recusa.
- A autenticação deve ficar no host confiável, pela referência de Vault
  `personal/asaas/production/api-key`. Não contorne a ausência de ferramenta
  por shell/script nem peça a chave ao usuário na conversa.
- Nunca exponha credenciais, cabeçalhos de autenticação ou o corpo bruto da
  resposta. Apresente somente os campos necessários à pergunta, respeitando
  a política de dados pessoais das skills ASAAS. Não copie para a skill
  pública dados privados retornados pela conta.
- Um HTTP 200 observado nesta conta e data não garante sucesso em outras
  contas ou consultas futuras. Relate o status e o motivo reais de cada
  execução, sem alterar a conta ou repetir automaticamente recusas.
