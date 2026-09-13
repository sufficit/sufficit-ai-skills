# CI da Sufficit

Use este fluxo quando um PR, issue ou missão mencionar CI, checks, Actions, runner, build ou
testes. A conta GitHub conectada ao Genius é o primeiro caminho para diagnóstico. Os manuais de
infraestrutura são fonte administrativa interna e nunca devem ser copiados para uma resposta,
issue, log, skill pública ou repositório de produto.

## Fontes de verdade

Consulte nesta ordem:

1. `AGENTS.md` ou a instrução equivalente do repositório;
2. `.github/workflows/*.yml` na revisão que executou;
3. `scripts/ci-local.sh` e scripts chamados por ele;
4. checks, jobs, etapas, logs e artefatos da execução no GitHub;
5. estado dos runners, somente se o job estiver aguardando infraestrutura.

O workflow do próprio repositório vence qualquer exemplo desta referência. Algumas bases
Sufficit antigas ainda selecionam apenas `openclaw-ci`; não altere labels por associação de nome.

## Diagnóstico autônomo

1. Leia o PR com `statusCheckRollup`, `headRefOid`, `baseRefName`, `files` e URL.
2. Para cada check sem sucesso, identifique workflow, execução, job, etapa e horário.
3. Se o job terminou, leia `--log-failed`; se necessário, consulte o job específico e baixe o
   artefato de resultado. **Não peça ao humano para colar logs disponíveis no GitHub.**
4. Leia o diff do PR e os testes alterados, mas não conclua que uma falha é preexistente apenas
   porque o nome do teste não coincide com os arquivos modificados.
5. Procure evidência: reproduza na worktree, confira a mesma suíte na base ou compare execuções
   recentes da branch base. Registre comando, falha e relação causal em poucas linhas.
6. Tome a próxima ação que já está autorizada: corrigir a regressão, devolver ao autor, repetir
   uma falha transitória uma vez ou acompanhar o runner. Encaminhe decisão ao humano somente
   quando restar uma escolha de produto ou risco sem regra no repositório.

Consultas úteis, sempre como a lista `arguments` de `github_cli`:

```json
["pr", "view", "536", "--repo", "owner/repo", "--json", "number,title,headRefOid,baseRefName,files,statusCheckRollup,url"]
```

```json
["run", "view", "34672730158", "--repo", "owner/repo", "--json", "status,conclusion,jobs,url"]
```

```json
["run", "view", "34672730158", "--repo", "owner/repo", "--job", "103497052889", "--log-failed"]
```

```json
["run", "list", "--repo", "owner/repo", "--branch", "main", "--workflow", "CI", "--limit", "5", "--json", "databaseId,status,conclusion,headSha,createdAt,url"]
```

## Classificação e ação

| Evidência | Classificação | Próxima ação |
|---|---|---|
| Teste reproduz na branch do PR e passa na base | Regressão do PR | Autor corrige; revisor solicita alteração e devolve a tarefa |
| Mesmo teste falha na base ou em execução anterior comparável | Falha preexistente comprovada | Vincule a falha existente e aplique a política de merge do repositório |
| Timeout, download temporário ou serviço externo oscila; nova tentativa não repete | Transitória | Reexecute somente os jobs com falha e acompanhe até terminar |
| Job fica `queued` e nenhum runner compatível está online/livre | Runner indisponível ou ocupado | Consulte runners/labels; aguarde se ocupado ou encaminhe falha operacional objetiva |
| Execução foi cancelada | Cancelamento | Determine se foi manual, por concorrência, timeout ou superseded antes de repetir |
| Logs/API retornam acesso negado | Autorização insuficiente | Informe permissão e endpoint ausentes; não invente diagnóstico |

Falhas preexistentes não são automaticamente irrelevantes. Verifique se quebram o contrato do
PR, impedem uma revisão confiável ou ocultam outra regressão. A decisão final segue as regras de
branch e revisão do repositório.

## Reexecução e acompanhamento

Antes de repetir, consulte o estado atual. Uma chamada de escrita com resultado ambíguo deve ser
confirmada por nova leitura para evitar execuções duplicadas.

```json
["run", "rerun", "34672730158", "--repo", "owner/repo", "--failed"]
```

Depois, acompanhe com `run view` até `completed`. Não crie laço rápido: jobs self-hosted podem
aguardar capacidade e cada instância processa um job por vez. Um job `queued` é espera, não erro.
Uma falha determinística repetida deve ser corrigida ou devolvida ao responsável, sem novas
tentativas idênticas.

Use `workflow run` somente se o YAML declarar `workflow_dispatch` e a solicitação autorizar o
disparo. Um push de correção normalmente cria outra execução; confirme antes de disparar mais uma.

## Contrato atual dos runners Sufficit

O CI compartilhado tem runners separados por plataforma. No Genius, o contrato atual é:

| Plataforma | Labels pedidas pelo workflow | Runner primário do Genius |
|---|---|---|
| Linux | `self-hosted, Linux, X64, openclaw-ci, ci-primary` | `linux-ci-genius-contigencia` |
| Windows | `self-hosted, Windows, X64, windows-ci, ci-primary` | `windows-ci-contigencia` |
| macOS/iOS | `self-hosted, macOS, X64, macos-ci, ci-primary` | `macos-ci` |

`openclaw-ci` é uma label histórica; ela não identifica sozinha a máquina real. `ci-primary`
seleciona o destino preferencial e deve existir em somente um runner compatível por plataforma e
repositório. Outros repositórios podem usar combinações diferentes, portanto leia `runs-on` no
workflow antes de diagnosticar.

Esse mapa identifica o destino primário de `sufficit/sufficit-ai-genius`, não autoriza acesso ao
host. O workflow seleciona labels, não o nome do runner. Um runner legado ou reserva sem
`ci-primary` não satisfaz um job que exige essa label e não deve ser apresentado como o servidor
correto. Sempre consulte a API, pois estado, capacidade e failover mudam sem alterar esta skill.

Se a conta tiver permissão administrativa, consulte o estado sem revelar credenciais:

```json
["api", "repos/owner/repo/actions/runners", "--jq", ".runners[] | {name,status,busy,labels:[.labels[].name]}"]
```

Cruze as labels do job com as labels retornadas pela API:

- `online` e `busy=true` significa que o runner correto está saudável e executando outro job;
  acompanhe a fila, sem pedir restauração do servidor;
- `online` e livre, mas um job permanece na fila, exige conferência do `runs-on`, do escopo do
  runner e de concorrência do workflow;
- `offline` só bloqueia o job quando esse runner é o único que satisfaz todas as labels exigidas;
- um runner reserva offline e sem `ci-primary` não explica a falha de um job primário;
- um job que chegou a executar e terminou com falha exige leitura dos logs; isso não prova que o
  servidor está fora do ar.

Não ofereça “aprovar sem o check” como solução automática para indisponibilidade do runner. Se o
check for obrigatório, preserve-o. Quando o primário estiver temporariamente offline, registre a
falha operacional com as evidências disponíveis, acompanhe seu retorno em intervalos moderados e
reexecute apenas os jobs com falha assim que houver runner compatível online. Encaminhe ao operador
somente quando a API comprovar ausência persistente de capacidade compatível ou quando for preciso
alterar host, registro ou labels; isso é uma ação operacional, não uma decisão de produto do usuário.

O agente de desenvolvimento/revisão não deve reiniciar hosts, alterar labels, registrar runner ou
usar acesso administrativo apenas para destravar um PR. Quando houver falha de infraestrutura,
entregue ao operador: repositório, workflow, run/job, plataforma, labels exigidas, estado observado,
horário e link. Nunca inclua token de registro, senha, endereço privado ou conteúdo de Vault.

## CI local antes do merge

Quando o repositório fornecer `scripts/ci-local.sh`, execute-o na worktree limpa antes de concluir.
Não injete a autorização GitHub no shell. O shell executa a validação local; `github_cli` consulta
e atualiza o GitHub dentro de seu próprio limite de credencial. Se o repositório exigir um status
do commit, publique-o pela API somente depois de o comando local terminar com sucesso e conforme
o processo documentado no próprio repositório.

Resuma ao humano o resultado em linguagem direta: o que falhou, causa comprovada, relação com o
PR, ação tomada e estado atual. Não despeje logs, metadados ou comandos completos na conversa.
