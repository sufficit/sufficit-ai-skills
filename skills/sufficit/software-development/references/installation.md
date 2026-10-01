# Instalação vinculada e conferência

Fonte canônica: https://github.com/sufficit/sufficit-ai-skills/tree/main/skills/sufficit/software-development.
A versão da skill é independente da versão do Codex. `release.json` e
`metadata.version` devem coincidir; o catálogo registra o SHA-256 do pacote completo.

## Instalar no Codex

Use o checkout canônico revisado e limpo, não uma worktree temporária:

```sh
python3 skills/sufficit/software-development/scripts/manage.py install
# Somente para migrar uma cópia antiga já revisada:
python3 skills/sufficit/software-development/scripts/manage.py install --migrate-existing
python3 skills/sufficit/software-development/scripts/manage.py check --remote
```

O destino é `$CODEX_HOME/skills/software-development`, ou
`$HOME/.codex/skills/software-development`. `--codex-home /pasta` permite testar
isoladamente. A instalação é um symlink para a pasta canônica; a cópia antiga é
preservada em `skill-backups/` fora da descoberta de skills. Links para outra
origem são recusados. O recibo em `skill-installations/software-development.json`
registra versão inicial, revisão Git, digest, origem, destino e backup.

O helper próprio é usado porque o instalador padrão do Codex copia o pacote sem
manter esse vínculo. O Codex suporta diretórios de skills ligados por symlink:
https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills.
Nesta instalação se preserva a raiz `.codex/skills` já utilizada pelo cliente;
outros ambientes podem usar `.agents/skills`, conforme a configuração/discovery
local. Não criar duas entradas com o mesmo nome em raízes diferentes.

## Conferir e atualizar

`check` verifica vínculo, versão e digest contra o manifesto local. `check --remote`
consulta o SHA atual de `main` e lê release/manifesto nesse SHA imutável, com timeouts.
Não roda pull, não troca de branch e não altera arquivos. Sem rede, retorna estado
remoto `unavailable`, não uma confirmação falsa de atualização. É executado uma vez
por sessão quando a skill é usada; não há timer/daemon instalado.

Estados remotos: `current`, `update-available`, `local-ahead`, `version-conflict` ou
`unavailable`. `current` compara o pacote, não apenas o commit global do repositório.
Mudanças em outra skill não produzem um falso aviso. Um mesmo SemVer com digest
diferente é conflito de versão e precisa ser investigado.

Quando uma atualização for desejada e autorizada:

```sh
git fetch origin main
git diff HEAD..origin/main -- skills/sufficit/software-development catalog/import-manifest.json
# Conferir Git limpo e ausência de divergência antes de avançar o checkout.
git merge --ff-only origin/main
python3 skills/sufficit/software-development/scripts/manage.py install
python3 skills/sufficit/software-development/scripts/manage.py check --remote
```

Como a instalação é ligada, avançar ou editar o checkout muda os arquivos visíveis
no Codex. Mantenha o checkout canônico em main e desenvolva a skill em worktree
separada. O recibo registra a instalação/atualização explícita, não cada leitura.
O checker detecta conteúdo local alterado ou divergência do digest e não o substitui.
Novas instruções ficam disponíveis na próxima descoberta/turno; a conferência em
disco não prova que um turno já em execução as recarregou.

## Manter uma release

Atualize `release.json`, `metadata.version` e a descrição versionada do catálogo;
recalcule o digest com `scripts/validate.py::digest` nos dois manifests. Rode
`python3 scripts/validate.py`, os testes do gerenciador e o validador de skill.
Publique a revisão e confira novamente a versão remota. Não edite a cópia instalada
como se fosse independente: o symlink altera a fonte.
