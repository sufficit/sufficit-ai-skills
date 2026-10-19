---
name: instagram-profile-setup
description: Audit and set up an Instagram business or startup profile so it gets found in search and converts visitors, covering the first steps of a new account: account type, name field, bio, link, highlights, pinned posts and first content. Use when the user asks to create, review or improve an Instagram profile or bio; does not post, run ads or automate the account.
metadata:
  version: "1.1.0"
  author: "Sufficit"
  source: "https://github.com/sufficit/sufficit-ai-skills"
---

# Instagram profile setup

Turn an Instagram profile into a page that a stranger can find through search and
understand in a few seconds: what the business does, why to trust it and what to do
next. Deliver concrete copy the user can paste, not generic advice.

## Gather facts first

Ask for or read what is missing before writing anything:

- Business name, what it sells, for whom, and the main problem it solves.
- Terms customers would type to find it (product category, niche, city if local).
- Proof: client results, numbers, testimonials, press, notable customers.
- The single next step wanted from a visitor (WhatsApp, booking, site, store, DM).
- Current profile: handle, name field, bio, link, highlights, pinned posts. A
  screenshot or the public URL is enough; do not log in to the user's account.

Never invent results, testimonials, client names or numbers. If proof is missing,
mark the slot as a gap and suggest how to collect it.

## The profile ladder

Treat each element as one step up. Most profiles stop at the first step. Audit in
this order and report which step the profile reaches.

1. **Photo.** A bare logo is the baseline, the same as everyone else. Use a logo
   readable at small size (the avatar is a tiny circle) or, for founder-led
   brands, a clear face photo. Keep it consistent with other channels.
2. **Name field (searchable).** Instagram search matches the typed query against
   the username and the name field, so put the brand plus what it does, e.g.
   `CaixaLeve | Financeiro p/ restaurantes`. The name field is separate from the
   @handle; keep the handle short, stable and easy to spell. Front-load the
   keyword; only roughly the first 30 characters show reliably. Name changes are
   rate-limited, so settle on it before changing.
3. **Bio as a salesperson.** Three lines within the 150-character limit:
   - what you solve, for whom (outcome, not features);
   - one proof that you deliver (number, client, result);
   - the next step, with the call to action pointing to the link.
   Avoid slogans, emoji walls and hashtags that send people away.
4. **Link.** One clear destination tied to the call to action: a WhatsApp click
   link (`https://wa.me/<number>?text=<prefilled message>`), booking page or a
   landing page. Instagram allows several links; put the primary one first and
   keep the list short. Add contact buttons (WhatsApp, email, phone) available to
   professional accounts.
5. **Highlights.** Replace personal or stale stories (old trips, events) with
   sales material: results, testimonials, offer/pricing, how it works, FAQ. This
   is where a visitor checks whether to trust the business. Use simple, consistent
   covers with one-word titles.
6. **Pinned posts.** Instagram lets you pin up to three posts. Do not pin the most
   viral video by default; pin three that sell:
   - how it works (product or service in action);
   - a client case (problem, solution, result);
   - who is behind it (founder or team introduction).
7. **Top step: consistent content.** A feed that keeps reinforcing the promise in
   the bio, with clear calls to action, so new visitors keep converting.

## Profiles with more than one product

Keep one umbrella promise in the name field (the two terms customers search,
e.g. `Brand | VoIP e WhatsApp`). In the bio give each product one line with its
name and outcome, then shared proof and a single call to action. Give each
product its own highlight and, when possible, one pinned post; the third pin
goes to a client case or the team. If the products have separate landing pages,
add them as extra links after the primary call to action. Do not link a product's
login page as if it were a sales page.

## First steps for a new account

1. Switch to a professional account (Business for companies, Creator for
   personal brands) to unlock insights, category label, contact buttons and
   scheduling. Pick the category closest to what customers search for.
2. Choose the handle: brand name, no confusing numbers or underscores; secure the
   same handle on other networks when possible.
3. Fill photo, name field, bio and link using the ladder above.
4. Connect the Facebook Page / Meta Business portfolio if ads, shop or the
   WhatsApp button will be used.
5. Publish at least six to nine posts before promoting the profile so the grid
   is not empty: include the three future pinned posts, a few Reels and a
   carousel that teaches something useful.
6. Create the core highlights (results, testimonials, offer, FAQ) even if each
   starts with one story.
7. Turn on two-factor authentication and keep recovery email/phone owned by the
   company, not a former employee or agency.
8. After two to four weeks, review insights (profile visits, link taps, follows
   by source) and adjust the name field keyword, bio and pinned posts.

## Content and engagement basics

- Reels reach non-followers; carousels and saves build trust with followers;
  stories keep existing followers warm. Mix them instead of relying on one format.
- Hook in the first seconds, captions on video (many watch muted), one idea per
  post, one call to action per post.
- Comment-keyword calls to action ("comment STARTUP and I send you...") raise
  engagement, but only promise what you will actually deliver. Sending replies
  automatically requires an official Meta-approved tool; never use unofficial
  bots, bought followers or engagement pods, which risk restrictions on the
  account.
- Reply to comments and DMs quickly; the first hour after posting matters.
- Respect advertising and consumer rules for claims and testimonials, and get
  consent before showing a client's name or face.

## Deliverable

Produce a short report in the user's language:

1. Current step on the ladder and the top three fixes, highest impact first.
2. Ready-to-paste copy: two or three name-field options, two bio options (with
   character counts), the link text, highlight list with titles, and the three
   pinned-post briefs.
3. Gaps the user must fill (proof, photos, testimonials) and a simple first-month
   content plan if the account is new.

Verify character limits by counting, and tell the user to confirm current limits
in the app, since Instagram changes them. Ready-made prompts for each part are in
[references/prompts.md](references/prompts.md). To read the live profile or apply
the approved copy, use [instagram-profile-manage](../instagram-profile-manage/SKILL.md).
