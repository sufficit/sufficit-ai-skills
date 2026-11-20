# Drive Meta interface without anyone's password

Works when the account owner is already logged into an accessible browser: Chrome on Android by `adb` + Chrome DevTools Protocol.

## Connection
```bash
adb devices -l
adb -s <serial> shell am start -a android.intent.action.VIEW -d "<url>" com.android.chrome
adb -s <serial> forward tcp:9333 localabstract:chrome_devtools_remote
curl -s http://127.0.0.1:9333/json/list     # list tabs and their IDs
```
Evaluate JS in a tab: WebSocket in `ws://127.0.0.1:9333/devtools/page/<id>` and `Runtime.evaluate`. Node 22 already has `WebSocket` built in, does not need dependency.

## What requires real touch (adb input tap)

Clicks per script do not count as user gesture: file selector, some menus and components that only react to native `mousedown`. Convert element position: `x_device = x_css * devicePixelRatio`, `y_device = toolbar_height + y_css * devicePixelRatio` (measure the Chrome bar once in a screenshot).

## File Upload
```
Page.setInterceptFileChooserDialog {enabled:true}
adb shell input tap <x> <y>          # on the "Carregar arquivo" (Upload file) button
-> event Page.fileChooserOpened
DOM.setFileInputFiles {files:[path_on_device], backendNodeId}
```
Use a path on the device. On Android 11+ Chrome needs `pm grant --user 0 com.android.chrome android.permission.READ_EXTERNAL_STORAGE`; without this Meta rejects the file. Revoke the permission afterward.

## Form fields
- Text: focus on the field by JS and use `Input.insertText` (React/Vue respect). Caution: `insertText` goes to the focused element; if there is search at the top of the site, the text can go there.
- Virtualized lists (countries, pages): type in dropdown search and choose with `ArrowDown` + `Enter`; scroll by script does not load items outside the window.
- Virtual keyboard covers the screen: `adb shell input keyevent 111` closes.

## Record the screen
```bash
adb shell screenrecord --time-limit 180 --size 1280x800 --bit-rate 6000000 /sdcard/Download/rec.mp4
```
Limit of 3 minutes per file: chain segments waiting for the previous process to die. To close before, `kill -INT <pid>` (finalize the MP4 correctly). Never `pkill` by a broad pattern.

## Cut empty video snippet

App "empty" screen has the same average brightness as the interface; what changes is that there is no dark pixel:
```bash
ffmpeg -i in.mp4 -vf "fps=2,signalstats,metadata=print:key=lavfi.signalstats.YMIN:file=ymin.txt" -f null -
# YMIN > 150 => frame without text; combine intervals and trim with select/setpts
```

## Playwright to record your own application

To film your own product (not Meta website), Playwright with `recordVideo` is cleaner: inject the session cookie, navigate, write subtitles with a fixed `<div>` and convert to MP4 with `libx264`. Run in the foreground: process in the background dies along with the session.
