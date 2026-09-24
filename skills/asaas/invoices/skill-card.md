# asaas-invoices

Consulta, agenda e cancela notas fiscais de serviço (NFS-e) da conta de produção do ASAAS com as ferramentas `asaas_invoices_list`, `asaas_services_list`, `asaas_invoices_create` e `asaas_invoices_cancel` (quando disponível) do Sufficit AI Genius, com consult-before-write, deduplicação e aprovação explícita. Detalhes do serviço (código municipal, ISS, nome fiscal) são auto preenchidos pelo cadastro da conta quando não especificados: o agente nunca pede código municipal ao usuário e nunca inventa código; a descrição impressa na nota é campo próprio e vem do usuário. A emissão omite os campos municipais, e é essa omissão que impede criar serviço — testes em sandbox comprovaram que enviá-los cria entrada no cadastro ou altera retroativamente a associação de notas já existentes. Criar serviço é ato separado, só a pedido explícito do usuário e pelo painel (a API do ASAAS não expõe criação, edição, exclusão nem serviço padrão). A listagem identifica o cliente de cada nota (nome e documento: CNPJ completo, CPF nos 3 primeiros dígitos). A documentação oficial da API está linkada na skill, com regra de verificação e reporte de divergências/recusas à equipe.

Versão: **0.6.0** · Sufficit · MIT-0

Leia [SKILL.md](SKILL.md) para aplicar a skill.

Fonte: [sufficit-ai-skills](https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/asaas/invoices).
