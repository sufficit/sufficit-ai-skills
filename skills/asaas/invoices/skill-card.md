# asaas-invoices

Consulta, agenda e cancela notas fiscais de serviço (NFS-e) da conta de produção do ASAAS com as ferramentas `asaas_invoices_list`, `asaas_services_list`, `asaas_invoices_create` e `asaas_invoices_cancel` (quando disponível) do Sufficit AI Genius, com consult-before-write, deduplicação e aprovação explícita. A skill diferencia a descrição impressa na nota do enquadramento municipal: nesta conta a emissão não envia os campos municipais por padrão, e o agente nunca pede código ao usuário só para emitir nem promete preenchimento automático não documentado. Emitir nota nunca cria serviço; criar serviço é ato separado, só a pedido explícito do usuário e pelo painel (a API do ASAAS não expõe criação). A listagem identifica o cliente de cada nota (nome e documento: CNPJ completo, CPF nos 3 primeiros dígitos). A documentação oficial da API está linkada na skill, com regra de verificação e reporte de divergências.

Versão: **0.5.0** · Sufficit · MIT-0

Leia [SKILL.md](SKILL.md) para aplicar a skill.

Fonte: [sufficit-ai-skills](https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/asaas/invoices).
