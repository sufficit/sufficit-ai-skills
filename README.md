# Sufficit AI Skills

Espelho público e versionado de 168 skills preparadas para o catálogo v2 do
Sufficit AI Genius. A publicação no Genius depende de sincronizar uma revisão
imutável deste repositório. Os pacotes mantêm instruções e recursos sob demanda; o
manifesto registra a origem, a revisão, a autoria, a licença e o digest de cada
conteúdo importado.

## Skills

| Coleção | Quantidade | Origem |
| --- | ---: | --- |
| Android | 22 | `android/skills`, Apache-2.0 |
| Google | 127 | `google/skills`, Apache-2.0 |
| Refero | 1 | `referodesign/refero_skill`, MIT |
| Matt Pocock | 1 | `mattpocock/skills`, MIT |
| MikroTik | 1 | `tikoci/routeros-skills` (adaptação Sufficit), MIT |
| Sufficit | 8 | Sufficit, MIT-0 |
| Images | 1 | Sufficit, MIT-0 |
| Instagram | 1 | Sufficit, MIT-0 |
| Videos | 1 | Sufficit, MIT-0 |
| Asaas | 4 | Sufficit, MIT-0 |
| QuePasa | 1 | Sufficit, MIT-0 |

As skills ficam em [`skills/android`](skills/android),
[`skills/asaas`](skills/asaas),
[`skills/google`](skills/google), [`skills/images`](skills/images),
[`skills/instagram`](skills/instagram),
[`skills/mikrotik`](skills/mikrotik), [`skills/quepasa`](skills/quepasa),
[`skills/refero`](skills/refero),
[`skills/videos`](skills/videos) e
[`skills/sufficit`](skills/sufficit). O
snapshot importado está em [`catalog/upstream-v2.json`](catalog/upstream-v2.json)
e a correspondência verificável em
[`catalog/import-manifest.json`](catalog/import-manifest.json).

O catálogo distribuído pelo Genius fixa cada pacote em um commit completo.
Alterações em `main` não substituem silenciosamente uma versão já revisada ou
instalada. Consulte [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) para
autoria e licenças.

A skill `software-development` possui instalação vinculada para Codex e conferência
de versão remota: [pacote](skills/sufficit/software-development/SKILL.md).

A skill [`clear-technical-writing`](skills/sufficit/clear-technical-writing/SKILL.md) orienta escrita técnica
clara, com adaptação em português e distinção entre revisão editorial e conformidade
com o padrão inglês. É uma adaptação independente da Sufficit.

The [`instagram-video-download`](skills/instagram/instagram-video-download/SKILL.md) skill saves Instagram
videos locally with yt-dlp and verifies the resulting media streams. The
[`video-transcribe`](skills/videos/video-transcribe/SKILL.md) skill turns local videos or audio into a
Markdown transcript with Whisper and ffmpeg.

## Skill language

Write all skill instructions, supporting documentation, cards, and agent metadata
in English. Catalog descriptions must also be English. Preserve API identifiers,
commands, and exact UI labels or provider messages when translating would make
instructions inaccurate; explain those literals in English. This package-language
rule does not override a user's requested response language.
