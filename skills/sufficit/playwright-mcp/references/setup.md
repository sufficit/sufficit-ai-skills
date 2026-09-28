# Cadastro do Playwright MCP no Genius

O Genius já suporta servidores MCP `stdio` (comando local) cadastrados pelo
próprio usuário em **Extensões → Integrações → MCP → Adicionar servidor
personalizado** — não é preciso plugin nem edição de arquivo de configuração
para usar o Playwright MCP.

## Pré-requisito: Node.js

`npx` vem junto do Node.js. Sem Node instalado no host onde o Genius roda, o
processo do servidor nem sobe (erro típico ao tentar conectar: `spawn npx
ENOENT`). Nesse caso, oriente o usuário a instalar o Node.js LTS e reabrir o
Genius antes de tentar de novo.

**Windows:** o `.cmd` do `npx` não é resolvido do mesmo jeito que num shell
interativo quando o processo é criado sem invocar um shell. Use `npx.cmd`
como comando, não `npx`.

## Campos do cadastro

| Campo | Isolado/silencioso | Bridge (navegador real) |
| --- | --- | --- |
| Nome | `playwright` | `playwright-bridge` |
| Transporte | `stdio` | `stdio` |
| Comando | `npx` (Windows: `npx.cmd`) | `npx` (Windows: `npx.cmd`) |
| Argumentos | `-y`, `@playwright/mcp@<versão fixa>`, `--headless` | `-y`, `@playwright/mcp@<versão fixa>`, `--extension` |
| Variáveis de ambiente | `NPM_CONFIG_LOGLEVEL=silent` | `NPM_CONFIG_LOGLEVEL=silent` |

Use nomes diferentes para os dois cadastros: as ferramentas ficam com prefixo
`mcp__playwright__*` e `mcp__playwright-bridge__*`, o que deixa claro qual
delas está sendo chamada. Antes de montar os argumentos, confirme o nome
exato das flags na versão instalada (`npx @playwright/mcp@<versão> --help`) —
elas podem mudar entre versões do pacote.

### Por que fixar a versão em vez de `@latest`

O transporte `stdio` é JSON-RPC linha a linha sobre `stdout`: qualquer texto
extra que o `npm`/`npx` jogue em `stdout` (aviso de atualização, resolução de
versão) corrompe o quadro da mensagem e derruba a conexão logo na primeira
troca. `@latest` faz o `npx` consultar o registro do npm a cada início — mais
lento e mais chance de ruído no `stdout`. Uma versão fixa (`@0.x.y`) evita essa
consulta e mantém o processo silencioso de fato.
`NPM_CONFIG_LOGLEVEL=silent` é a segunda camada de proteção contra ruído.

Validado ao vivo em 2026-09-28 (pacote `@playwright/mcp`, versão estável na
época **0.0.82** — confira a atual com `npm view @playwright/mcp version`, ela
muda com frequência): rodando o servidor já instalado localmente (sem passar
pelo `npx`, que é o pior caso de ruído), o handshake `initialize` completou,
`tools/list` devolveu **25 ferramentas** — bem mais que as 5 do `browser_*`
nativo do Genius, incluindo `browser_console_messages`,
`browser_handle_dialog`, `browser_emulate_media`, `browser_evaluate`,
`browser_file_upload` e `browser_drop`, capacidades que o `browser_*` nativo
não tem — e uma chamada real de `browser_navigate` (headless, contra
`github.com/sufficit`) voltou com o resultado esperado. **Zero linhas fora do
JSON-RPC no `stdout`** durante todo o teste.

### Isolado x bridge — não confunda os dois

`--headless` sobe um Chromium **isolado** que o próprio Playwright baixa e
gerencia (a primeira execução pode demorar por causa do download) — sem
login, sem cookies, sem histórico do usuário. `--extension` **não** sobe
navegador nenhum: o servidor espera a extensão da Chrome Web Store conectar
numa aba que o usuário já está usando, com a sessão real dele.

## Extensão do Chrome Web Store (só para o modo bridge)

1. O usuário instala a extensão na Chrome Web Store:
   `https://chromewebstore.google.com/detail/mmlmfjhmonkocbjadbfplnigmagldckm`.
   **Dois nomes, mesma extensão** (conferido ao vivo em 2026-09-28): a
   listagem da loja mostra **"Playwright Extension"** — é esse o nome que
   aparece no título da página e no botão "Add to Chrome". Depois de instalada
   e conectada, a própria barra de aviso do Chrome ("esta extensão está
   depurando o navegador") mostra o nome interno do manifest: **"Playwright
   MCP Bridge"**. Se o usuário disser que só achou "Playwright Extension" na
   loja, é a mesma coisa — não mande procurar de novo por "MCP Bridge".
2. Diferente da extensão própria do Genius (essa é force-installed
   automaticamente pela política gerenciada — ver `TOOLS-BROWSER.md` no
   repositório `sufficit-ai-genius`), essa extensão **não se conecta
   sozinha**: o usuário precisa clicar no ícone dela na aba que quer
   compartilhar, a cada aba nova que o agente for usar.
3. Sem esse clique, a primeira chamada de ferramenta do lado bridge (por
   exemplo, navegar) fica pendente ou retorna um erro pedindo a conexão — não
   é um problema no cadastro do servidor MCP em si.
4. **Sinal de que está funcionando:** a barra do Chrome mostrando "'Playwright
   MCP Bridge' started debugging this browser" (ou o texto equivalente em
   português) na aba compartilhada **é o comportamento esperado**, não um
   alerta de segurança nem sinal de extensão maliciosa — é o próprio Chrome
   avisando que uma extensão está com a API de debugger anexada à aba, exatamente
   o mecanismo que permite o modo bridge funcionar.

## Sintoma → causa → ação

| Sintoma | Causa provável | O que fazer |
| --- | --- | --- |
| Nenhuma ferramenta `mcp__playwright*__*` na lista | Servidor não cadastrado, desabilitado, ou falhou ao conectar | Conferir em Extensões → Integrações → MCP o estado/erro do servidor; se o erro citar `spawn ... ENOENT`, falta Node/`npx` no PATH do host que roda o Genius |
| Ferramentas presentes, mas a chamada trava ou erra no modo bridge | Extensão não instalada, ou instalada mas não clicada na aba alvo | Orientar a instalação (link acima) e o clique do ícone na aba certa |
| Ferramentas presentes, mas a chamada trava ou erra no modo `--headless` | Primeiro download do Chromium do Playwright ainda em curso, ou faltam dependências de sistema do Chromium no host (comum em Linux mínimo) | Aguardar a primeira execução terminar; se persistir em Linux, faltam bibliotecas do sistema que o Chromium exige |
| Conexão cai logo depois de cadastrar | Ruído em `stdout` (versão `@latest` sem `NPM_CONFIG_LOGLEVEL`) corrompendo o quadro `stdio` | Trocar para versão fixa e adicionar a variável de ambiente da tabela acima |

Falhas de rede/spawn podem ser tentadas de novo uma vez, com um instante de
espera. Falhas que dependem de ação do usuário (instalar Node, instalar a
extensão, clicar o ícone) não se resolvem repetindo a chamada — explique o
passo que falta antes de tentar de novo.
