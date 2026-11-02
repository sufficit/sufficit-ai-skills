---
name: instagram-caption
description: "Write and lint an Instagram caption in Portuguese or English: the line that survives the feed cut, the body, one call to action, search terms and up to five hashtags. Use when the user asks for a caption, post description or hashtags; it does not publish, and profile copy belongs to instagram-profile-setup."
metadata:
  version: "1.0.1"
  author: "Jake Schincariol / Sufficit"
  source: "https://github.com/Jakeschincariol/instagram-agent-skill/tree/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-caption"
---

# Instagram caption

Write the caption, then read it the way the feed shows it. The linter prints that
view, so run it on every draft:

```bash
python3 -B scripts/caption_lint.py caption.txt --keywords "fluxo de caixa,gestão financeira"
```

It exits 1 on a FAIL. Fix every FAIL and decide on every WARN out loud. A linter
pass means the format is sound, not that the post will perform.

## Decide the caption's job first

- **The video already hooks.** A Reel opens with its own spoken and on-screen hook.
  The caption gives context, the search terms and the ask; do not compete with the
  video.
- **The caption is the content.** On a photo or carousel, line one is the hook: short,
  concrete and complete, or cut where the reader wants the rest.

Say which job you chose, and why.

## Gather facts

Ask for what is missing: the post's single idea, the audience, the one action wanted,
and two or three terms customers would type. Read the brand's voice file when it
exists (see [instagram-reel](../instagram-reel/SKILL.md)). Never invent numbers, clients or results. When a number is needed and unknown,
leave `{{your number}}` in the draft and flag it. Get consent before naming a client.

## Shape

```text
Line 1     Up to about 125 characters show before "... more". No greeting, hashtag
           or leading emoji.
Body       Two to six short paragraphs with a blank line between them. Search terms
           go here as phrases a person would type.
The ask    One action: comment a keyword, save, send, message or tap the link.
Hashtags   Up to five specific topic labels on the last line, or none.
```

The limit is 2,200 characters and most posts need far fewer.

## Rules

- **One ask.** With two, the reader has to choose; pick the one the post is for.
- **No link in the body.** Captions are not clickable. Point to the bio or send the
  link by DM.
- **Comment keywords are one easy word,** said in the video too. Only promise what will
  actually be delivered, and send automatic replies only through official
  Meta-approved tools.
- **Hashtags are labels.** Cut `#viral`, `#fyp`, `#explorepage` and similar tags, which
  describe nothing. Do not promise reach from hashtags.
- **Emoji are punctuation.** The linter warns above 4 per 100 characters.
- **Write alt text** for photos and carousels. Screen readers use it.
- **Respect advertising rules** for claims and testimonials.

## Platform limits go stale

The 125-character cut is approximate and moves with the device. The cap of five
hashtags was announced by Instagram in December 2025. When the app disagrees with
these numbers, the app is right: pass `--truncate` or `--hashtag-limit`, then fix the
constants in the script.

## Deliverable

Give the copy-ready caption in a fenced block, followed by the job chosen, characters
used before the cut, the ask, the search terms and the linter verdict. List the WARNs
you kept and why, plus any `{{...}}` gaps.

Nothing is published here. To publish through the Graph API or check the profile, use
[instagram-profile-manage](../instagram-profile-manage/SKILL.md).

## Credit

Adapted from `ig-caption` in
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) by
Jake Schincariol, under the MIT license in [LICENSE](LICENSE).
