# Anti-slop polish

Use when a screen looks generated rather than designed, or when the user asks to
"unslop", polish or clean up an existing interface. This guide is Sufficit's
adaptation of the method in **unslop** by Damir Sokolovsky
([@heydamir](https://x.com/heydamir), <https://github.com/heydamir/unslop>,
CC BY 4.0). Changes from the original: condensed, ordered for Blazor/SUI, and
subordinated to the project's `DESIGN.md` and Sufficit.Blazor.UI. The full upstream
package is mirrored in this repository as [unslop](../../../unslop/unslop/SKILL.md);
read its [signs](../../../unslop/unslop/references/signs.md) and
[tokens](../../../unslop/unslop/references/tokens.md) when you need exact values.

## Precedence

1. The user's explicit request.
2. The project's approved `DESIGN.md` and the SUI tokens/components. When an unslop
   rule contradicts a documented decision (for example, the panel's approved glass
   surfaces and warm hairlines, or a display weight of 700), the document wins.
   List each conflict in the audit instead of silently "fixing" it.
3. The anti-slop rules below.

A rule that is only habit in the code (not written in `DESIGN.md`) is not a decision:
an amber "aurora" background or a stock hero image can be removed when the documented
canvas is flat.

## Audit first, then decide how much to change

Render the real screen when possible (preview fixture, local host, published
showcase). Static greps help find spread, never replace the render:

```bash
grep -rEc "(linear|radial)-gradient|backdrop-filter|text-transform: *uppercase|font-weight: *(700|800|900)|letter-spacing: *-|infinite" --include=*.css --include=*.scss --include=*.razor src
```

List every sign with its location, then classify:

- **Heavy slop** (many signs across colour, type, icons, copy): run all passes.
- **Light slop** (designed screen with a few signs): polish only what the audit found;
  keep palette, type, layout and visual. Bigger ideas go to the report as suggestions.
- **No slop**: say so and propose at most two or three refinements with exact values.

Signs seen in Sufficit code so far: radial colour blooms and SVG grain on the body,
colour-tinted glass shadows, uppercase tracked kickers and pills, 700+ weights on
labels, a generic AI stock image behind a hero, a status shown as a saturated pill,
`infinite` pulses on non-live values, italic helper text, emoji in labels, trailing
periods on headlines and captions, a 3-column grid holding 4 stats (orphan row).

## Direction (five lines, then wait)

Write and show the audit plus these lines before editing; wait for approval unless
the user already said to proceed.

- **Product**: what it does and for whom, one sentence.
- **Character**: two or three concrete words (never clean, modern, sleek, minimal, premium).
- **World**: place or material the product belongs to (a PBX operator desk, a night
  shift, an invoice) — it tints neutrals, accent and visuals.
- **Moments**: one or two places that get rich colour and detail (a coverage map, a
  carefully drawn chart). Everything else stays quiet.
- **Signature**: one small detail only this product would have, used consistently
  (for telephony, a live status dot where the state is real).

Keep a real brand colour (Sufficit orange) as the accent; it leaves surfaces and borders
unless `DESIGN.md` says otherwise.

## Passes, in order

Finish each pass across the whole screen before the next.

1. **Spacing** — 4px grid; equal things share size; smaller gaps inside groups than
   between them; remove one-off values (`1.8rem`, `0.85rem`, `13.6px`).
2. **Colour** — one neutral ramp, three text roles (primary, secondary, muted), one
   accent used rarely; no hue gradients, gradient text, colour glows or colour shadows;
   hairline borders; semantic colours only for meaning.
3. **Icons** — one set, one size (16/18), one stroke, text-role colour; no emoji.
4. **Copy** — headline says what it does with the product's own nouns; no
   exclamation marks, greetings, hype words or unverifiable claims; no trailing period
   on headlines, labels, buttons and captions; changes say what they compare to.
5. **Type** — weights 400–500, 600 for rare emphasis; sentence case (no uppercase
   tracked labels); no negative tracking on small text; `tabular-nums` and one number
   format; no italic for emphasis.
6. **Layout** — keep sections and order; real app proportions; one primary and at most
   one secondary action; no orphan rows in stat grids.
7. **Details** — nested radius (inner = outer − padding, minimum 4); counts and meta as
   quiet text; status as a small dot plus text instead of a saturated pill; visible
   focus; charts with one accent and muted grid.
8. **Visuals** — remove decorative filler (blobs, orbs, stock people, robots). Show the
   product or its data instead. Generate images only when asked and only with an
   approved tool.
9. **Motion** — no looping pulse on things that are not live, no `transition: all`, no
   hover scale; one easing, transitions on colour/opacity/transform only.

## Blazor/SUI notes from practice

- Edit sources, not outputs: SCSS under `wwwroot/assets/scss` (the compiled
  `sufficit-blazor.css` is ignored and regenerated); SUI styles live in `src/styles`
  and `npm run build:css` regenerates `src/wwwroot`.
- A weight of 500 renders as regular when the font stack lacks that weight; check the
  render and keep hierarchy through size and colour.
- Library-wide visual changes in SUI may be guarded by tests (the helper text italic
  had a browser test) and visual baselines: update the contract deliberately, add a
  CHANGELOG entry and run the browser suite against the local catalog host.
- Removing an asset may break a test that only guarded it; delete both together.

## Checklist

- [ ] Audit listed with locations; conflicts with `DESIGN.md` called out
- [ ] Direction written and approved (or user said to proceed)
- [ ] Spacing on the 4px scale; equal things equal
- [ ] One neutral ramp, three text roles, one accent with 4.5:1 contrast where it carries text
- [ ] No hue gradients, gradient text, glows, colour shadows or blobs
- [ ] No emoji; one icon set, size and stroke
- [ ] Weights 400–600, sentence case, no italic, tabular figures
- [ ] No exclamation marks, greetings, trailing periods on short strings, unverified claims
- [ ] No looping or bouncy motion
- [ ] Template check: swap the product name — if the screen still fits another product,
      push the copy, moments and signature further
- [ ] Rendered after the change (or the limitation stated plainly)

Optionally offer a [before/after video](before-after-video.md) of the change.
