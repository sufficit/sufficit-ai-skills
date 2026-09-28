---
name: playwright-mcp
description: Usa o Playwright MCP (modo isolado/silencioso --headless ou modo bridge --extension com a extensão Chrome Web Store "Playwright MCP Bridge") como caminho opcional de automação web do Sufficit AI Genius, além do navegador nativo do usuário. Use quando o usuário mencionar Playwright, MCP Bridge, automação headless, scraping isolado, ou quando a tarefa web exigir rede/console, PDF, múltiplas abas, upload de arquivo ou snapshot de acessibilidade que o browser_* nativo do Genius não oferece. Também ensina a reconhecer se o servidor e a extensão estão instalados e a orientar o cadastro quando não estiverem.
---

# Playwright MCP e Playwright MCP Bridge

O Genius já enxerga a web pelo **próprio navegador do usuário**, via a
extensão MV3 nativa force-installed (`browser_navigate`, `browser_get_page`,
`browser_find`, `browser_click`, `browser_type` — ver `TOOLS-BROWSER.md`).
Isso é o caminho padrão, sem cadastro nenhum.

O Playwright MCP é um **segundo caminho, opcional**, que o próprio usuário
cadastra em **Extensões → Integrações → MCP → Adicionar servidor
personalizado**. Ele expõe ferramentas `mcp__<nome-do-servidor>__*` com
capacidades que o `browser_*` nativo não tem: árvore de acessibilidade
estruturada, múltiplas abas simultâneas, upload de arquivo, captura de
rede/console, exportação em PDF, drag-and-drop.

## Dois modos, dois cadastros diferentes

1. **Isolado e silencioso** (`--headless`): processo Playwright próprio, sem
   nenhum login do usuário — mesma família de propósito do `CdpBrowserToolset`
   interno do Genius (PuppeteerSharp, hoje desligado por padrão), mas com
   ferramentas mais ricas. Use para scraping ou verificação automatizada que
   **não deve tocar** as abas nem as sessões reais do usuário.
2. **Bridge para o navegador real** (`--extension`): o processo Playwright
   anexa numa aba real do Chrome/Edge do usuário através da extensão da Chrome
   Web Store **"Playwright MCP Bridge"**. É uma via alternativa à extensão
   própria do Genius — só compensa quando a tarefa precisa de uma capacidade
   do Playwright que o `browser_*` nativo não tem. Não é o caminho padrão.

## Como reconhecer se está configurado

- Ferramenta `mcp__<nome-do-servidor>__*` presente na sua lista de ferramentas
  = o servidor MCP está cadastrado, conectado e pronto. Não peça para o
  usuário reconectar sem motivo.
- Ausente = servidor não cadastrado, desabilitado, ou com erro de conexão
  (Node/`npx` ausente no host, por exemplo). Não tente contornar chamando
  Playwright por shell/terminal em nome do usuário; ensine o cadastro
  (ver abaixo).
- **Servidor MCP conectado ≠ extensão do navegador instalada.** Mesmo com o
  lado do servidor saudável, a primeira chamada real no modo bridge (por
  exemplo, navegar) pode travar ou retornar erro se a extensão não estiver
  instalada ou não tiver sido clicada na aba alvo. Repasse ao usuário a
  instrução que a própria ferramenta devolver, em vez de adivinhar — ver
  [references/setup.md](references/setup.md).

## Quando a ferramenta não existe

Se nenhuma ferramenta `mcp__playwright*__*` estiver disponível, explique que é
uma integração opcional e oriente o cadastro: **Genius → Extensões →
Integrações → MCP → Adicionar servidor personalizado**, usando exatamente os
valores de [references/setup.md](references/setup.md) (comando, argumentos,
variáveis de ambiente, nome). Não invente flags, não rode `npx` fora do Genius
para "testar" em nome do usuário, e não use os `browser_*` nativos como
substituto silencioso da lacuna — se a tarefa realmente precisa do Playwright,
diga isso com clareza e ajude no cadastro.

## Quando preferir os `browser_*` nativos em vez do Playwright

Os `browser_*` do Genius já são a via padrão para "agir como o usuário" no
navegador real: zero cadastro, force-installed, sem extensão adicional para o
usuário instalar. Prefira o Playwright bridge só quando a tarefa exigir algo
que o `browser_*` nativo não oferece (rede/console, PDF, múltiplas abas
simultâneas, upload de arquivo, drag-and-drop, snapshot de acessibilidade
estruturado). Para scraping ou verificação isolada que não deve tocar a sessão
real do usuário, use o modo `--headless`.

## Referências

- [references/setup.md](references/setup.md) — cadastro exato dos dois modos
  (campos, Node/`npx`, Windows), por que fixar versão e silenciar o stdout,
  link da extensão na Chrome Web Store, e tabela de sintomas → causa → ação.
