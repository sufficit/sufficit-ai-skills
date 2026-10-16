---
name: device-ui-android
description: "Use the built-in browser_* tools for Android websites and device_ui for native apps or the user's signed-in Chrome session. Operate Sufficit AI Genius Android accessibility controls with read_screen, click_element, and set_text rather than desktop shortcuts or raw coordinates. Use for Android interaction, device_ui/android_device_control, printing, saving PDFs, sharing, or ineffective key actions. Discover description=/role= selectors for unlabeled icons and verify the final effect of every Save/Download/Send action."
---

# Android device_ui: touch interaction

On Android, `device_ui` uses `GeniusScreenAccessibilityService`, the same accessibility system used by screen readers such as TalkBack. It can inspect and operate any foreground app, including Chrome, one screen at a time. Use it to act as the user when no structured API exists. The desktop MV3-based `browser_*` integration does not run in Android Chrome; installing another extension cannot remove that platform limitation.

## Websites: use the built-in browser

Since version 0.133, Genius Android has its own embedded browser: `browser_navigate`, `browser_get_page`, `browser_find`, `browser_click`, `browser_type` with `submit`, and `browser_back`. It reads contacts, titles, text, and CSS-selectable elements as data, without screenshots or Accessibility. Real tablet tests found a site's phone number and the lowest price through Mercado Livre's own search in 1–2 minutes; the same tasks through Chrome `device_ui` required dozens of taps and failed.

- For website reading, search, clicks, forms, and price comparisons, prefer `browser_*`.
- Use `web_search` to discover which site or URL to open.
- Reserve `device_ui` for native apps and tasks requiring the user's signed-in Chrome session. The embedded browser has separate cookies and does not share those logins. If a page requires login, tell the user instead of silently switching tools.

## Check availability

If `device_ui` is missing, call `android_device_control` with `action=status`. If disabled, direct the user to `action=open_settings`. On Android 13+, `open_app_settings` may be needed first to allow restricted settings for sideloaded apps before enabling Accessibility. The user must enable this Android-protected permission; the agent cannot do so independently.

## Prefer semantic interaction

Desktop shortcuts are not a substitute for Android menus. In a real Chrome Android test, `key` with `Ctrl+P` did not open printing. `Ctrl+A` and `Esc` are also desktop conventions. Reserve `key` for simple navigation such as Back or Enter when needed.

1. Call `read_screen` to inspect each visible element's text, role, ID, and state.
2. Use `click_element`/`set_text` with a discovered `label=`, `text=`, `description=`, `id=`, or `role=` selector.
3. Use `screenshot` when `read_screen` is empty or pixels are necessary, such as for a visual layout check.
4. Use raw `coordinate` input only as a last resort.

After every action, inspect with `read_screen` again. `device_ui` confirms that input was accepted, not that the app completed the intended operation.

A screenshot of an open Save dialog is not evidence that a file was saved. A real test stopped with the file name entered and the `SALVAR` button visible, then incorrectly reported a saved PDF; the file did not exist. For Save, Download, Send, or Confirm, perform the final click and verify the effect afterward: the dialog closes, a download notification appears, or the resulting file is found. Without confirmation, report the action as pending.

For an unlabeled icon, use its actual `description=`/`role=`, not guessed `text=`. The ⋮ menu has an accessibility description, such as `Personalizar e controlar o Google Chrome` or `Mais opções`, rather than visible text. A guessed or overly broad text selector can click a neighboring element without reporting an error. Always read the exact accessibility description and role before constructing the selector.

## Save or share a Chrome Android page as PDF

There is no desktop print shortcut or direct PDF export button on the mobile Chrome toolbar.

1. Call `read_screen` and identify the actual `description`/`role` of the top-right ⋮ menu. It has no visible label; discover the selector before calling `click_element`.
2. Read the opened menu and select Share or Print (Portuguese labels may be `Compartilhar` or `Imprimir`). Confirm the actual label for the installed version and language. The share panel and print screen belong to Android, outside Chrome. In a real test, a successful Print click returned to the page instead of exposing the expected print screen. If this happens, do not repeat unchanged clicks. Call `read_screen` alone first to allow the system accessibility tree to update.
3. In the print screen, select Save as PDF (`Salvar como PDF`) if it is not already selected.
4. Continue to the Android file-name/folder dialog and click its `SALVAR` button. Reaching the print screen is not completion.
5. Read the screen again to confirm the dialog closed and, if possible, list recent Downloads files to verify the file name. Only then report that the PDF was saved.

See [references/android-touch-patterns.md](references/android-touch-patterns.md) for typing, virtual-keyboard, and foreground-app pitfalls.
