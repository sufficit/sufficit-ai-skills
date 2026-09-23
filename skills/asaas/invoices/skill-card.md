# asaas-invoices

Emite e consulta notas fiscais de serviço (NFS-e) da conta de produção do ASAAS pelas ferramentas `asaas_invoices_list`, `asaas_services_list` e `asaas_invoices_create` do Sufficit AI Genius, com deduplicação e aprovação explícita. A emissão não especifica serviço: código municipal e ISS vêm do cadastro de serviços da conta, e o agente nunca pede código ao usuário só para emitir. Emitir nota nunca cria serviço; criar serviço é ato separado, só a pedido explícito do usuário e pelo painel (a API do ASAAS não expõe criação). A listagem identifica o cliente de cada nota (nome e documento: CNPJ completo, CPF nos 3 primeiros dígitos).

Versão: **0.4.1** · Sufficit · MIT-0

Leia [SKILL.md](SKILL.md) para aplicar a skill.

Fonte: [sufficit-ai-skills](https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/asaas/invoices).
