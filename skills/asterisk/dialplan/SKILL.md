---
name: asterisk-dialplan
description: Write, review and format traditional Asterisk dialplan with consistent conventions for context comments, TAB indentation, English text and change headers. Use for extensions.conf and dialplan includes, contexts, exten, same, priorities and subroutines; not for AEL, Lua or SIP/PJSIP peer configuration.
metadata:
  version: "1.0.0"
  author: "Sufficit"
---

# Asterisk dialplan

## Language and scope

Write new or revised comments, change descriptions, diagnostic messages, descriptive
identifiers and accompanying technical documentation in **English**. Keep official
application/function names, existing public context names, protocol literals,
customer data and the exact ownership lines unchanged. Do not rename deployed
identifiers just to translate them. Preserve historical entries as recorded; write
new change entries in English. This rule does not change the user's chat language
or authorize translating customer-facing prompts.

Read the target repository's AGENTS.md first. These are authoring conventions, not
universal Asterisk syntax requirements. Asterisk executes contexts, extensions and
priorities, not indentation. `same =>` reuses the preceding extension; `n` means
the next priority. Recessing `same` does not create a conditional block.

## File ownership and change history

Preserve the repository's ownership and license notice at the top of each maintained
dialplan `.conf`. Do not impose a company name or an "all rights reserved" notice
on another project's files. Follow its AGENTS.md or existing header template; if
ownership is unspecified, do not invent it.

Then record the **two latest actual changes**, newest first:

```text
;### YYYY/MM/DD HH:MM - (AUTHOR) - Concise English description
```

Use the actual change time in the repository's documented timezone, the actual
author/agent, and describe what changed. Do not invent a
second entry for a new file. Keep at most two change entries; Git/activity records
retain older history. Update the header in the same change as the file, including
formatting changes. Separate the header from the body with one blank line.

Use the repository's header checker/generator when available. Inspect any generated
diff before accepting it, preserve manually recorded history, and follow its rules
for generated or archived files. Do not rewrite unrelated headers. These defaults
yield to explicit repository requirements.

## Context layout

- Put `[context-name]` at column one.
- Place the context's purpose comment **below** its declaration, with `;` at column
  one. Describe inputs, outputs/termination and dependencies when they matter.
- Leave one blank line between the context comment and its first extension.
- Prefix `exten =>` with **one literal TAB**.
- Prefix `same =>` with **two literal TABs**, one level beyond `exten`.
- Start another extension with one TAB and separate extensions with a blank line.
- Align instruction-specific comments with the instruction they explain. Keep
  `n(label)` at the same level as other `same` lines.
- Before an instruction-specific comment inside an extension, leave one blank line
  to separate the comment block from the preceding instruction. Keep the comment
  adjacent to the instruction it explains; do not insert blank lines between each
  line of a multi-line comment. Context descriptions still follow `[context]` directly.
- Preserve argument whitespace, quoting, escapes and empty arguments such as
  `Dial(resource,,t)`. Do not pad argument lists for column alignment.

Original example with literal TABs (the complete file also needs the header):

```asterisk
[app-example]
; Input: s. Demonstrates sequencing without answering the call.
; Output: terminates the channel. No external dependencies.

	exten => s,1,NoOp(Start)
		same => n,Hangup()
```

## Behavior and integration

Verify the target Asterisk version, driver and include graph. FreePBX's version
does not identify the Asterisk version or channel driver. Distinguish source,
installed configuration and loaded dialplan.

Prefer `n` and named labels for new code. Check entry priorities, branch targets,
GoSub/Return pairs and termination paths. Do not renumber old code during a style
change. Check persisted destinations and callers before renaming or moving contexts.

Follow the repository's directory structure and context naming conventions. Keep
native application code separate from framework integration where the project does
so; do not move FreePBX dependencies without replacing or documenting them.

Document significant answer/early-media, recording/CDR, transfer and fallback
behavior. Do not add these effects implicitly. Contact resolution and authorization
are separate from busy-state checks. Reuse existing SIP/PJSIP/media resolvers when
they fit the contract. Do not generalize a direct-call route's policy to all calls.

Respect the project's data-access and outage policy. Identify synchronous external
dependencies in the call path and reuse its established resolution mechanisms.
Do not introduce ODBC, HTTP or framework dependencies as a side effect of formatting.

## Validation

Format only the requested scope. Generated FreePBX files are not durable source.
For a formatting-only edit of simple lines, compare ordered executable lines before
and after, removing only leading whitespace and whole-line comments. Keep argument
contents unchanged. This comparison is insufficient for multiline comments or
continuations; inspect those explicitly or load the file in an isolated Asterisk.
Check literal TABs, `git diff --check`, headers and include paths.

For behavior changes, exercise relevant branches with synthetic destinations in an
isolated compatible Asterisk. Report static-only checks accurately when runtime
validation is unavailable. Do not reload production or originate real calls solely
to validate formatting. Skill use does not authorize publication or deployment.

## Official references

Reviewed on 2026-10-28; recheck version-sensitive behavior when necessary.

- [Contexts, Extensions, and Priorities](https://docs.asterisk.org/Configuration/Dialplan/Contexts-Extensions-and-Priorities/): `n`, labels and `same`, with indented examples.
- [Creating a Simple IVR Menu](https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Creating-a-Simple-IVR-Menu/): complete example with recessed `same` lines.
- [Asterisk 18 configuration parser](https://github.com/asterisk/asterisk/blob/18/main/config.c): `ast_strip(process_buf)` strips outer whitespace before parsing; it does not justify changing whitespace inside values.

The exact TAB depth and placement of context comments above are this skill's default
style; the official examples do not mandate literal TABs.
