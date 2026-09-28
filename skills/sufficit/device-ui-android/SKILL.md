---
name: device-ui-android
description: Usa a ferramenta device_ui do Sufficit AI Genius em Android (celular/tablet) — controle por acessibilidade (GeniusScreenAccessibilityService), sem teclado físico, sem atalhos de desktop. Use quando o dispositivo for Android, quando device_ui/android_device_control aparecerem, quando precisar imprimir/salvar PDF/compartilhar no Chrome Android, ou quando uma ação por atalho de teclado (key) não tiver efeito num app mobile. Ensina a preferir read_screen/click_element/set_text (seletor semântico) a coordenadas cruas e a atalhos de teclado, e cobre o padrão real de "salvar página em PDF" no Chrome Android (menu ⋮, nunca Ctrl+P).
---

# device_ui em Android: toque, não teclado

`device_ui` em Android é a `GeniusScreenAccessibilityService` — a mesma
Acessibilidade que leitores de tela como o TalkBack usam. Ela enxerga e opera
**qualquer app em primeiro plano**, Chrome incluso, tela por tela. É o caminho
do agente pra "agir como o usuário" no Android quando não existe API
estruturada pra tarefa (`browser_*` nativo do Genius é desktop-only — MV3 não
roda em Chrome Android, ponto final de plataforma, não é algo que dê pra
contornar com outra extensão).

## Verifique antes de usar

Se `device_ui` não estiver na sua lista de ferramentas, chame
`android_device_control` com `action=status`. Se vier desabilitado, oriente
`action=open_settings` (ou `open_app_settings` primeiro em Android 13+, pra
permitir "configurações restritas" antes de habilitar Acessibilidade — o
sistema exige esse passo extra pra apps instalados fora da loja). Sem isso
habilitado pelo usuário, `device_ui` simplesmente não aparece — não existe
jeito de ativar Acessibilidade por conta própria, é permissão sensível
protegida pelo próprio Android.

## Android é toque, não é um desktop pequeno

**Atalho de teclado não é o caminho.** `Ctrl+P` pra imprimir, `Ctrl+A` pra
selecionar tudo, `Esc` — são convenções de desktop. Num teste real (Chrome
Android, GitHub, tentando salvar a página em PDF), a ação `key` com um atalho
desse tipo **não teve efeito nenhum**: a página continuou exatamente como
estava, sem abrir diálogo de impressão. Trate `key` como recurso de último
caso pra teclas de navegação simples (voltar, enter), não como substituto de
menu.

**O caminho certo é semântico, sempre que der:**

1. `read_screen` primeiro — lista texto, função, id e estado de cada elemento
   visível. É a forma de "ver" a tela sem imagem.
2. `click_element`/`set_text` com seletor (`label=`, `text=`, `description=`,
   `id=`, `role=`) sobre o que `read_screen` encontrou.
3. `screenshot` só quando `read_screen` vier vazio ou pixels forem realmente
   necessários (ex.: conferir um layout visual).
4. Coordenada crua (`coordinate`) é o último recurso, não o primeiro.

Depois de qualquer ação, **confira o resultado com `read_screen` de novo**
antes de assumir que funcionou — `device_ui` não devolve confirmação do que
aconteceu do lado do app, só que o evento de input foi aceito.

**Ícone sem texto: use `description=`/`role=`, nunca `text=` chutado.** Botões
como o menu **⋮** não têm rótulo visível — o texto que existe pra eles é a
descrição de acessibilidade (o que o TalkBack leria em voz alta, ex.:
"Personalizar e controlar o Google Chrome" ou "Mais opções"), não um texto na
tela. Um teste real confirmou o erro comum aqui: pedir `click_element` com um
seletor de texto chutado (ou vago demais) pra esse tipo de ícone clica no
elemento errado sem dar erro nenhum — o `device_ui` aceita o clique
normalmente, só que no botão vizinho. **Sempre rode `read_screen` e confira o
`description`/`role` exatos do ícone antes de montar o seletor** — não tente
adivinhar o texto de um botão que não tem texto.

## Salvar/compartilhar página como PDF no Chrome Android

Não existe atalho de teclado nem opção de "exportar PDF" direta na barra do
Chrome mobile. O caminho real, tocável:

1. `read_screen` na barra do Chrome e identifique o `description`/`role` real
   do menu **⋮** (três pontinhos, canto superior direito) — não monte o
   seletor de cabeça, ele é um ícone sem texto (ver seção acima). Só depois
   dê `click_element` nele.
2. `read_screen` de novo (o menu que abriu é conteúdo novo) e `click_element`
   em **Compartilhar** ou **Imprimir** (o rótulo exato varia por versão do
   Chrome/idioma — confirme o texto real antes de clicar, não adivinhe).
3. Na tela de impressão, o destino **"Salvar como PDF"** já costuma vir
   selecionado; se não vier, `click_element` no seletor de destino e escolha
   essa opção.
4. Confirme com `read_screen` que a tela de impressão realmente abriu antes
   de dizer ao usuário que o PDF foi gerado — se o Chrome não mudou de tela,
   nada foi salvo, mesmo que a sequência de toques tenha "rodado sem erro".

Ver [references/android-touch-patterns.md](references/android-touch-patterns.md)
pra outras armadilhas de navegação Android (digitação, teclado virtual,
trazer app pra frente no meio de uma leitura de tela).
