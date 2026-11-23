# Before/after video (suggestion)

After a visible interface change, offer the user a short video of the screen changing
from the old version to the new one. It is a presentation piece for review or sharing;
it does not replace browser evidence of the real screen. Make it only when the user
accepts — it costs a few minutes.

The renderer is the story script from **unslop** by Damir Sokolovsky
([@heydamir](https://x.com/heydamir)), CC BY 4.0, mirrored in this repository at
[unslop](../../../unslop/unslop/SKILL.md#story-video). Every video it renders carries a
small `unslop by @heydamir` credit, as the licence asks; keep it.

In an installed copy of this skill the relative link may not resolve. Install the
`unslop` skill from the Sufficit catalog, or in Claude Code run
`claude plugin install unslop@heydamir` (after `claude plugin marketplace add heydamir/unslop`),
and use its `scripts/story.mjs`.

## How it works

One standalone HTML page holds the original screen (step 0). Each step adds CSS under
`.s1`, `.s2`, … that only changes values, so the browser tweens padding, colours, radii
and weights in place, with a wave across the screen and red redlines on spacing and
corners. Text that changes rolls letter by letter.

## Steps

1. **Story file** — build `unslop-story/story.html` outside the product repository
   (a temporary folder). Copy the old markup and the old CSS values as step 0; take
   them from `git show <old-commit>:<file>` when the change is already committed.
2. **Steps** — three to five, merged from the passes so each changes something
   visible, for example `Spacing, Color, Type and copy, Details`:
   `<meta name="unslop-steps" content="Spacing, Color, Type and copy, Details">`.
3. **What cannot tween** — put gradients, stock images and colour washes on their own
   layers and fade `opacity` to 0; write pill radii as half the height (not 9999px);
   use `<span class="swap" data-at="N"><span class="from">old</span><span class="to">new</span></span>`
   for changed words (at most eight); `data-out="N"` removes, `data-in="N"` adds.
4. **Redlines** — `data-gap="<stack>"` on four to six blocks of a vertical stack,
   `data-radius` on two to four elements whose corners change.
5. **Camera** — `<meta name="unslop-frame" content="x y width">`. Square by default; use
   `--wide` (16:9) when the change spans a wide hero.
6. **Render** — Playwright and ffmpeg are required. Install Playwright in the temporary
   folder, not in the product repository:

   ```bash
   cd /tmp/story-work && npm init -y && npm install -D playwright
   npx playwright install chromium   # skip when the browser cache already has it
   node <skills>/unslop/unslop/scripts/story.mjs unslop-story/story.html change.mp4 --wide
   ```

   Use `--play` instead of the output path to watch it loop live.
7. **Check** — pull a few frames and look at them before handing over:

   ```bash
   ffmpeg -loglevel error -ss 0.5 -i change.mp4 -frames:v 1 before.jpg
   ffmpeg -loglevel error -ss 7.9 -i change.mp4 -frames:v 1 after.jpg
   ffmpeg -loglevel error -i before.jpg -i after.jpg -filter_complex vstack before-after.jpg
   ```

## Honesty rules

- When the real screen depends on an API or login and cannot be rendered locally, the
  story uses sample data. Say so in the report ("illustrative numbers") and do not
  present the video as proof that production renders that way.
- The story file never ships. The product keeps its normal code, without `.s` classes
  or story attributes.
- Deliver the video path plus the stacked before/after image, so the user can review
  without playing the video.
