# Android Navigation Traps by device_ui

Real use lessons from `device_ui`/Accessibility on Android — not hypotheses.

## Raw coordinate breaks when layout changes; selector does not

The virtual keyboard occupies much of the screen when it opens, and the content scrolls to compensate — any `coordinate` calculated before that may not point to the right element later. `click_element`/`set_text` with semantic selector do not suffer this problem: they resolve against the current accessibility tree, not against fixed pixel. It's the main reason to prefer selector to coordinate, besides being more readable.

## `type` simulates key by key; `set_text` not

The `type` action sends keyboard events in sequence — in fields with active autocomplete/suggestion, this can collide with the keyboard autocorrect and lose or change characters, especially in fields that react to each key (search with suggestions, fields with mask). When the field selector is known, `set_text` writes the value at once without this race. Reserve `type` for when there is no reliable field selector.

## BACK is contextual — it is not "closing keyboard" guaranteed

The BACK key/gesture of Android does different things depending on what is focused: close the keyboard if it is open, or browse the page/app back. If you have already closed the keyboard by other means (e.g. tapping outside the field) and sends BACK "to ensure", the result may be to leave the screen or lose unsaved form content. Confirm with `read_screen` that the keyboard is still visible before deciding whether BACK is safe there.

## Switch app in the middle of the task: read again, do not assume

`device_ui` sees only what is in the foreground at the time of call. If the task requires opening an app (Chrome, for example) from another (Genius itself), the previous screen reading (Genius) is no longer valid as soon as Chrome takes over the screen — `read_screen` again before continuing by clicking, even if the sequence seems obvious.

## After acting, confirm the effect

`device_ui` returns confirmation that the input event was accepted, not that the app reacted as expected (even `type`/`key` standard in the rest of Genius: "input events accepted; target reaction is not observable"). After a `click_element` that should open a screen, menu or dialogue, call `read_screen` and confirm that the expected element appeared before reporting success to the user — not only that the call did not fail.
