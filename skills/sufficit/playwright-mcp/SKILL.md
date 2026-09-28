---
name: playwright-mcp
description: Usa o Playwright MCP (modo isolado/silencioso --headless ou modo bridge --extension com a extensão Chrome Web Store "Playwright Extension"/"Playwright MCP Bridge") como caminho opcional de automação web do Sufficit AI Genius, além do navegador nativo do usuário — em desktop via stdio local, e no Genius mobile/tablet obrigatoriamente via http contra um servidor hospedado, já que mobile não suporta stdio. O próprio agente cadastra/habilita/desabilita/remove o servidor chamando mcp_server_add, mcp_server_set_enabled e mcp_server_remove diretamente — não precisa guiar o usuário pela tela de Extensões, exceto em builds antigos do Genius sem essas ferramentas. Use quando o usuário mencionar Playwright, MCP Bridge, automação headless, scraping isolado, o agente do Genius no tablet/celular, ou quando a tarefa web exigir rede/console, PDF, múltiplas abas, upload de arquivo ou snapshot de acessibilidade que o browser_* nativo do Genius não oferece.
---

# Playwright MCP e Playwright MCP Bridge

O Genius já enxerga a web pelo **próprio navegador do usuário**, via a
extensão MV3 nativa force-installed (`browser_navigate`, `browser_get_page`,
`browser_find`, `browser_click`, `browser_type` — ver `TOOLS-BROWSER.md`).
Isso é o caminho padrão, sem cadastro nenhum.

O Playwright MCP é um **segundo caminho, opcional**. Ele expõe ferramentas
`mcp__<nome-do-servidor>__*` com capacidades que o `browser_*` nativo não tem:
árvore de acessibilidade estruturada, múltiplas abas simultâneas, upload de
arquivo, captura de rede/console, exportação em PDF, drag-and-drop.

**Cadastro é self-service — use as ferramentas, não guie o usuário pela tela.**
Desde a adição de `mcp_server_add`/`mcp_server_set_enabled`/`mcp_server_remove`
(2026-09-28), o próprio agente cadastra, habilita, desabilita e remove
servidores MCP chamando essas ferramentas diretamente — não é mais preciso
mandar o usuário abrir Extensões → Catálogo → Adicionar servidor personalizado.
Se o usuário pedir "liga o Playwright" ou similar, **chame `mcp_server_add`
você mesmo** com os valores de [references/setup.md](references/setup.md); só
oriente a tela manual se essas ferramentas não estiverem na sua lista (ver
"Quando a ferramenta não existe" abaixo — normalmente significa build antigo
do Genius, anterior a essa funcionalidade).

## Dois modos de navegação

1. **Isolado e silencioso** (`--headless`): processo Playwright próprio, sem
   nenhum login do usuário — mesma família de propósito do `CdpBrowserToolset`
   interno do Genius (PuppeteerSharp, hoje desligado por padrão), mas com
   ferramentas mais ricas. Use para scraping ou verificação automatizada que
   **não deve tocar** as abas nem as sessões reais do usuário.
2. **Bridge para o navegador real** (`--extension`): o processo Playwright
   anexa numa aba real de um Chrome/Edge **desktop** através da extensão da
   Chrome Web Store listada como **"Playwright Extension"** (nome interno do
   manifest: "Playwright MCP Bridge" — ver [references/setup.md](references/setup.md)).
   É uma via alternativa à extensão própria do Genius — só compensa quando a
   tarefa precisa de uma capacidade do Playwright que o `browser_*` nativo não
   tem. Não é o caminho padrão. **Este modo sempre controla o navegador de um
   computador desktop** — não existe extensão de navegador em Chrome mobile,
   então não há "bridge" para o próprio Chrome do tablet/celular.

## Desktop x mobile: transporte diferente, cadastro diferente

**O Genius mobile (tablet/celular) não suporta MCP por `stdio`** — o próprio
código do Genius recusa essa combinação (`MCP stdio is unavailable on mobile;
use HTTP`). Isso muda o cadastro conforme o dispositivo:

- **Genius desktop:** cadastra o servidor como `stdio`, comando `npx`, e o
  Genius sobe o processo Playwright localmente sob demanda. Zero infra extra.
- **Genius mobile (o agente rodando no tablet):** não existe processo local
  para subir. O servidor Playwright MCP precisa estar **rodando de forma
  persistente em algum host sempre ligado** (o desktop do usuário, um
  notebook, um servidor Sufficit) com `--port`, e o cadastro no tablet aponta
  para esse endereço por `http`, não por `stdio`. Ver
  [references/setup.md](references/setup.md) para o endereço exato do
  endpoint (validado ao vivo) e o alerta de segurança sobre expor esse
  servidor na rede — **ele não tem autenticação própria**.

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

Primeiro, distinga os dois níveis de ausência:

1. **`mcp_server_add` presente, mas nenhuma ferramenta `mcp__playwright*__*`:**
   o Playwright MCP em si só não foi cadastrado ainda. Chame `mcp_server_add`
   você mesmo com os valores de [references/setup.md](references/setup.md) —
   não peça permissão para o usuário navegar até uma tela; isso é exatamente o
   que essa ferramenta existe para evitar. Depois de chamar, confira
   `connected`/`error` no resultado antes de declarar sucesso.
2. **Nem `mcp_server_add` existe:** esta versão do Genius é anterior à
   funcionalidade de autogestão de MCP (2026-09-28). Só nesse caso oriente o
   cadastro manual: **Genius → Extensões → Catálogo → Adicionar servidor
   personalizado**, com os mesmos valores de
   [references/setup.md](references/setup.md), ou sugira atualizar o Genius.

Em ambos os casos: não invente flags, não rode `npx` fora do Genius para
"testar" em nome do usuário, e não use os `browser_*` nativos como substituto
silencioso da lacuna — se a tarefa realmente precisa do Playwright, diga isso
com clareza.

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
  em desktop (campos, Node/`npx`, Windows, por que fixar versão e silenciar o
  stdout), o cadastro por `http` obrigatório no Genius mobile/tablet contra um
  servidor hospedado (endpoint validado ao vivo, alerta de segurança sobre
  falta de autenticação), link da extensão na Chrome Web Store, e tabela de
  sintomas → causa → ação.
