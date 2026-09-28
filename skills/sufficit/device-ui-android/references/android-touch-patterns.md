# Armadilhas de navegação Android por device_ui

Lições de uso real de `device_ui`/Acessibilidade em Android — não hipóteses.

## Coordenada crua quebra quando o layout muda; seletor não

O teclado virtual ocupa boa parte da tela quando abre, e o conteúdo rola pra
compensar — qualquer `coordinate` calculada antes disso pode não apontar mais
pro elemento certo depois. `click_element`/`set_text` com seletor semântico
não sofrem esse problema: resolvem contra a árvore de acessibilidade atual,
não contra pixel fixo. É o motivo principal pra preferir seletor a
coordenada, além de ser mais legível.

## `type` simula tecla por tecla; `set_text` não

A ação `type` manda eventos de teclado em sequência — em campos com
autocompletar/sugestão ativos, isso pode colidir com o corretor do teclado e
perder ou trocar caracteres, sobretudo em campos que reagem a cada tecla
(busca com sugestões, campos com máscara). Quando o seletor do campo é
conhecido, `set_text` escreve o valor de uma vez, sem essa corrida. Reserve
`type` para quando não há seletor de campo confiável.

## BACK é contextual — não é "fechar teclado" garantido

A tecla/gesto BACK do Android faz coisas diferentes dependendo do que está
focado: fecha o teclado se ele estiver aberto, senão navega a página/app pra
trás. Se você já fechou o teclado por outro meio (ex.: tocar fora do campo) e
manda BACK "pra garantir", o resultado pode ser sair da tela ou perder
conteúdo de formulário não salvo. Confirme com `read_screen` se o teclado
ainda está visível antes de decidir se BACK é seguro ali.

## Trocar de app no meio da tarefa: leia de novo, não assuma

`device_ui` enxerga só o que está em primeiro plano no momento da chamada. Se
a tarefa exige abrir um app (Chrome, por exemplo) a partir de outro (o
próprio Genius), a leitura de tela anterior (do Genius) não vale mais assim
que o Chrome assume a tela — `read_screen` de novo antes de continuar
clicando, mesmo que a sequência pareça óbvia.

## Depois de agir, confirme o efeito

`device_ui` devolve confirmação de que o evento de input foi aceito, não de
que o app reagiu como esperado (mesmo padrão de `type`/`key` no restante do
Genius: "input events accepted; target reaction is not observable"). Depois
de um `click_element` que deveria abrir uma tela, menu ou diálogo, chame
`read_screen` e confirme que o elemento esperado apareceu antes de reportar
sucesso ao usuário — não apenas que a chamada não deu erro.
