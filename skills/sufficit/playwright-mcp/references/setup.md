# Cadastro do Playwright MCP no Genius

O Genius já suporta servidores MCP cadastrados pelo próprio usuário em
**Extensões → Integrações → MCP → Adicionar servidor personalizado** — não é
preciso plugin nem edição de arquivo de configuração para usar o Playwright
MCP. O transporte muda conforme o dispositivo: **desktop usa `stdio`** (esta
seção); **Genius mobile/tablet exige `http`** contra um servidor hospedado —
ver [Genius mobile/tablet](#genius-mobiletablet-cadastro-por-http) mais
abaixo, é uma seção separada porque o cadastro é bem diferente.

## Desktop: cadastro `stdio`

### Pré-requisito: Node.js

`npx` vem junto do Node.js. Sem Node instalado no host onde o Genius roda, o
processo do servidor nem sobe (erro típico ao tentar conectar: `spawn npx
ENOENT`). Nesse caso, oriente o usuário a instalar o Node.js LTS e reabrir o
Genius antes de tentar de novo.

**Windows:** o `.cmd` do `npx` não é resolvido do mesmo jeito que num shell
interativo quando o processo é criado sem invocar um shell. Use `npx.cmd`
como comando, não `npx`.

### Campos do cadastro

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

## Genius mobile/tablet: cadastro por `http`

**Por que não dá pra copiar o cadastro `stdio` do desktop:** o Genius recusa
`stdio` em mobile por design — não existe processo local para o app subir
dentro do Android/iOS. O agente do Genius que roda no tablet só enxerga o
Playwright se houver um servidor Playwright MCP **já rodando, de forma
persistente, em algum host sempre ligado** e alcançável pela rede — o desktop
do usuário, um notebook, ou um servidor Sufficit. Esse host que sobe o
processo com Node/`npx`; o tablet só conecta em `http`.

### Subir o servidor em modo `http`/SSE

No host que vai ficar sempre ligado (ex.: `systemd`, ou qualquer supervisor de
processo — não é um comando pra rodar manualmente toda vez):

```bash
npx -y @playwright/mcp@<versão fixa> --headless --isolated \
  --port 8931 --host <ip-interno-de-vpn>
```

**Validado ao vivo em 2026-09-28**: ao subir com `--port`, o processo imprime
no start (uma única vez, no início — não é ruído contínuo no `stdout` do
protocolo):

```
Listening on http://localhost:8931
Put this in your client config:
{
  "mcpServers": {
    "playwright": { "url": "http://localhost:8931/mcp" }
  }
}
For legacy SSE transport support, you can use the /sse endpoint instead.
```

Testei o handshake HTTP completo contra esse endpoint (o mesmo que o
`HttpClientTransport` do Genius fala — Streamable HTTP com fallback SSE,
`AutoDetect`): `initialize` devolveu `Mcp-Session-Id` no cabeçalho da
resposta, `tools/list` trouxe as mesmas 25 ferramentas do teste por `stdio`, e
um `browser_navigate` real contra `github.com/sufficit` funcionou. O endpoint
`/mcp` é o correto para o cadastro no Genius; `/sse` existe só como
compatibilidade com clientes MCP antigos.

### Campos do cadastro no Genius mobile

| Campo | Valor |
| --- | --- |
| Nome | `playwright` (ou `playwright-bridge` se este host também tiver `--extension` — ver abaixo) |
| Transporte | `http` |
| Endpoint | `http://<ip-interno-de-vpn>:8931/mcp` |

Sem comando, sem argumentos, sem variável de ambiente — isso tudo já foi
decidido na hora de subir o processo no host. O Genius mobile só precisa da
URL.

### ⚠️ Segurança: este endpoint não tem autenticação própria

Conferido no `--help` do pacote: não existe flag de token, bearer ou senha
para o transporte `http`. Quem alcançar `<host>:<porta>/mcp` pela rede
controla um navegador real **sem pedir nada** — inclusive `browser_evaluate`
(executa JavaScript arbitrário na página) e `browser_file_upload`. `--allowed-
hosts`/`--allowed-origins` restringem para onde o *navegador* pode navegar,
não quem pode *falar com o servidor* — não são controle de acesso ao MCP.

**Nunca** bind em `0.0.0.0` numa rede exposta à internet ou compartilhada com
quem não deveria ter esse controle. Bind só na interface de VPN/Tailscale do
host (não `0.0.0.0` solto), e cadastre no tablet o IP dessa VPN — não um IP
público. Trate a URL completa (host:porta) como segredo equivalente a uma
senha: quem a tiver, controla o navegador daquele host.

### Modo bridge (`--extension`) a partir do mobile

Se o host que sobe o servidor `--port` também usar `--extension` (em vez de
`--headless`), o tablet consegue acionar o navegador **desktop** desse host
através do Playwright MCP — mas continua sendo o navegador do desktop que é
controlado, nunca o Chrome do próprio tablet (Chrome mobile não roda
extensões). Deixe isso claro para o usuário antes de configurar: "bridge no
mobile" quer dizer "o tablet manda o computador tal abrir e mexer no
navegador dele", não "o tablet ganha um navegador Playwright próprio".

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
| Cadastro `stdio` funciona no desktop mas o mesmo cadastro falha no Genius mobile | Mobile não suporta `stdio` — erro esperado, não é falha de configuração | Cadastrar o mobile por `http` contra um servidor `--port` já rodando em host sempre ligado (ver seção mobile/tablet acima); nunca tentar `stdio` no app mobile |
| Genius mobile não conecta no servidor `http` | Servidor não está rodando, porta/IP errados, firewall bloqueando, ou o servidor está bindado só em `localhost` do outro host (inalcançável pela rede) | Confirmar que o processo está ativo no host, que `--host` não é `localhost`/`127.0.0.1` (precisa ser a interface de rede/VPN), e que a porta está liberada só para a VPN — nunca abrir para a internet |

Falhas de rede/spawn podem ser tentadas de novo uma vez, com um instante de
espera. Falhas que dependem de ação do usuário (instalar Node, instalar a
extensão, clicar o ícone) não se resolvem repetindo a chamada — explique o
passo que falta antes de tentar de novo.
