# Conduzir a interface da Meta sem a senha de ninguém

Funciona quando a pessoa dona da conta já está logada num navegador acessível:
Chrome de um Android por `adb` + Chrome DevTools Protocol.

## Ligação
```bash
adb devices -l
adb -s <serial> shell am start -a android.intent.action.VIEW -d "<url>" com.android.chrome
adb -s <serial> forward tcp:9333 localabstract:chrome_devtools_remote
curl -s http://127.0.0.1:9333/json/list     # lista as abas e seus ids
```
Avaliar JS numa aba: WebSocket em `ws://127.0.0.1:9333/devtools/page/<id>` e
`Runtime.evaluate`. Node 22 já tem `WebSocket` embutido, não precisa de dependência.

## O que exige toque real (adb input tap)
Cliques por script não contam como gesto do usuário: seletor de arquivos, alguns menus e
componentes que só reagem a `mousedown` nativo. Converta a posição do elemento:
`x_device = x_css * devicePixelRatio`, `y_device = altura_da_barra + y_css * devicePixelRatio`
(meça a barra do Chrome uma vez num print).

## Upload de arquivo
```
Page.setInterceptFileChooserDialog {enabled:true}
adb shell input tap <x> <y>          # no botão "Carregar arquivo"
-> evento Page.fileChooserOpened
DOM.setFileInputFiles {files:[caminho_no_aparelho], backendNodeId}
```
O caminho é do **aparelho**. Em Android 11+ o Chrome precisa de
`pm grant --user 0 com.android.chrome android.permission.READ_EXTERNAL_STORAGE`; sem isso
a Meta recusa o arquivo. Revogue depois.

## Campos de formulário
- Texto: focar o campo por JS e usar `Input.insertText` (respeita React/Vue).
  Cuidado: `insertText` vai para o **elemento focado**; se houver busca no topo do site,
  o texto pode ir para lá.
- Listas virtualizadas (países, páginas): digitar na busca **do dropdown** e escolher com
  `ArrowDown` + `Enter`; rolar por script não carrega itens fora da janela.
- Teclado virtual cobre a tela: `adb shell input keyevent 111` fecha.

## Gravar a tela
```bash
adb shell screenrecord --time-limit 180 --size 1280x800 --bit-rate 6000000 /sdcard/Download/rec.mp4
```
Limite de 3 minutos por arquivo: encadeie segmentos esperando o processo anterior morrer.
Para encerrar antes, `kill -INT <pid>` (fecha o MP4 direito). Nunca `pkill` por padrão.

## Cortar trecho vazio do vídeo
Tela "vazia" de app tem o mesmo brilho médio da interface; o que muda é não haver pixel escuro:
```bash
ffmpeg -i in.mp4 -vf "fps=2,signalstats,metadata=print:key=lavfi.signalstats.YMIN:file=ymin.txt" -f null -
# YMIN > 150 => quadro sem texto; junte os intervalos e corte com select/setpts
```

## Playwright para gravar a sua própria aplicação
Para filmar o seu próprio produto (não o site da Meta), Playwright com `recordVideo` é mais limpo:
injete o cookie de sessão, navegue, escreva legendas com um `<div>` fixo e converta para MP4
com `libx264`. Rode em primeiro plano: processo em segundo plano morre junto com a sessão.
