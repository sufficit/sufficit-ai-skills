---
name: instagram-reel
description: "Write an Instagram Reel from one raw idea in Portuguese or English: hook options, spoken script, separate on-screen text and a timed beat sheet, in the brand's own voice. Use when the user asks for a Reel, short video script, hook or voiceover, or to create a brand voice file; it does not record, edit or publish, and captions belong to instagram-caption."
metadata:
  version: "1.0.0"
  author: "Jake Schincariol / Sufficit"
  source: "https://github.com/Jakeschincariol/instagram-agent-skill/tree/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-reel"
---

# Instagram Reel

Turn one true, specific idea into a script someone can say out loud. The user records
and approves everything; this skill publishes nothing.

## Before writing

1. **Read the voice file,** usually `instagram/<handle>/voice.md`. When there is none,
   ask for three real Reels or captions and draft it from
   [references/voice-template.md](references/voice-template.md). Use
   [instagram-video-download](../instagram-video-download/SKILL.md) and
   [video-transcribe](../../videos/video-transcribe/SKILL.md) for existing videos. If
   the user only wants one quick script, go on and say the voice is unconfirmed.
2. **Check the idea.** A Reel needs one true thing: what happened, to whom, and what it
   cost or returned. If that is missing, ask once instead of padding.
3. **Use the account's evidence.** When an
   [instagram-audit](../instagram-audit/SKILL.md) exists, it outranks the defaults here.

Never invent results, clients or numbers, even as examples. Write `{{your number}}` and
flag it. Get consent before showing a client or team member, and follow the voice file's
limits and advertising rules for claims and testimonials.

## Hooks

Write three hooks, each from a different shape and each with its spoken line and its
on-screen line:

| Shape | Use when | Example form |
| --- | --- | --- |
| Cost paid | A mistake cost something real | "Perdi `{{valor}}` por causa de..." |
| Before and after | A number moved | "De `{{antes}}` para `{{depois}}` em..." |
| Common mistake | The audience does it now | "Se você ainda faz X, ..." |
| Unexpected result | The outcome contradicts the assumption | "Cortamos X e Y subiu" |
| Client case | There is approved proof | "`{{cliente}}` tinha X; hoje..." |
| Direct question | The audience already feels the problem | "Quanto você perde quando...?" |

Discard a hook that fails any of these:

- It opens with a greeting, a name, "neste vídeo" or a plea for attention.
- It takes more than about 3 seconds to say.
- It has nothing checkable, or promises what the video does not deliver.
- The speaker would not say it that way.

Recommend one and say why. Do not give hooks a numeric score: text can reject a weak
hook but cannot pick the winner between good ones. The upstream author's own test found
the same, and its scorer misranks Portuguese. The audience data decides afterwards.

## Script shape

```text
0-3 s     Hook: spoken and on screen, with movement in the first frame
3-7 s     Stake: why this matters to the viewer, in one line
Body      One idea per beat; change the frame on each beat
Close     Deliver what the hook promised, then one ask
Last line Optionally echo a word from the hook so the replay lands cleanly
```

Default to 15 to 45 seconds and go longer only when the content needs it. This range is
a starting assumption, so replace it with what the account's audit shows. Reported upload
limits and claims about long Reels reaching fewer non-followers conflict and are not
official, so check the app before planning a long Reel.

- One idea per Reel. If the script has two, offer two Reels.
- Use short lines in spoken language, with no sentence that needs rehearsal.
- Prefer real numbers to adjectives.
- Start at the sentence you would normally reach at second six: no intro or logo.

## Time it

Put one beat per line in a file and run the script until the flags are resolved:

```bash
python3 -B scripts/beat_sheet.py script.txt --target 30 --wpm 150
```

Pass the speaker's timed rate. Without `--wpm`, the output warns that the 150 wpm default
is a planning assumption. Numbers and foreign words take longer to say than they count,
so confirm with one test read before recording.

## On-screen text

Treat it as a separate script: it is read before it is heard.

- Keep each card to six words or fewer, with the hook card up from the first frame.
- Burn in captions for the body, because many people watch muted.
- Keep text and key elements inside the safe zone. On 1080x1920, a conservative
  guide is about 270 px clear at the top, 670 px at the bottom and 65 px at the sides,
  and more on the right when text is near the action buttons. These are Meta's ad figures
  as reported by third-party guides, and the interface varies by device, so check a
  preview in the app before publishing.

## Deliverable

Reply in the user's language with:

1. The three hooks and the recommended one, with the reason.
2. The script in a fenced block, with the beat sheet.
3. On-screen cards with their timings.
4. Shot and frame suggestions per beat, only where they add something.
5. Open `{{...}}` gaps, consent still needed and the voice status.
6. A `label` for the [instagram-audit](../instagram-audit/SKILL.md) CSV, such as the hook
   shape, so later results can be compared.

Write the caption with [instagram-caption](../instagram-caption/SKILL.md). Publishing goes
through [instagram-profile-manage](../instagram-profile-manage/SKILL.md) after approval.

## Credit

Adapted from `ig-reel` and `templates/voice.md` in
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) by Jake
Schincariol, under the MIT license in [LICENSE](LICENSE).
