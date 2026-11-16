---
name: sufficit-prospect-qualify
description: "Find and qualify B2B prospects for Sufficit products (WhatsApp calls answered on Sufficit VoIP, Hermes omnichannel, after-hours AI) from public evidence only, score them 0-100 and draft a first message for approval. Use when asked to find leads, qualify providers (ISPs) or prepare a prospecting round. Research only: it never sends, follows, likes or comments."
metadata:
  version: "1.0.0"
  author: "Sufficit"
  source: "https://github.com/sufficit/sufficit-ai-skills"
---

# Sufficit prospect qualify

Find a few prospects with a real, recent, verifiable reason to buy, instead of
long lists of look-alikes. Method adapted from the MIT-licensed
first-customer-finder skill (github.com/carolinacherry/claude-first-customer-finder-skill).
Sending a message belongs to [instagram-profile-manage](../../instagram/instagram-profile-manage/SKILL.md)
and only after the user approves the draft.

## 1. Product card (write it before searching)

- What we sell: WhatsApp calls answered on Sufficit VoIP plus Hermes (WhatsApp,
  Instagram and other channels in one inbox). AI covers **after hours only**,
  with humans in business hours: people dislike AI-only support, so never sell
  AI for every contact.
- User: the provider's support desk. Buyer: owner, partner or director.
- Purchase trigger: subscribers left without support at night or on weekends,
  or a support desk that no longer keeps up with growth.
- Current workaround: technician on-call phone, IVR with no exit, "leave a
  message", WhatsApp bot that only sends invoices.
- Instant disqualifiers: already advertises 24h human support; more than 50k
  followers (own large desk); no posts in 90 days; current Sufficit partners;
  anyone already contacted (check the user's prospecting log); suppliers to
  providers (treat as partnership, not sale).

If the card cannot rule anyone out, it is too vague: sharpen it first.

## 2. Five search fronts (run in parallel, one researcher subagent each)

| Front | Look for |
|---|---|
| Explicit demand | Posts or forum questions asking for a support system, chatbot, 24h support or phone system |
| Pain | Reclame Aqui, Google reviews, post comments: "nobody answers", "only a bot", "no support on weekends" |
| Workaround | Bio with "on call: message the technician", one WhatsApp per city, "we will call you back" |
| Switch | Changing ERP/system, complaints about the current telephony or chatbot vendor |
| Timing | Job ads for night or support attendants, new city, merger, new support hours |

Vary sources; a list from a single source is fragile. Good seeds: accounts that
follow many providers (provider marketing agencies, other providers' "following" lists).

## 3. Verify before scoring

- Every signal carries: link to the page actually opened, source type, visible
  date (or "no date"), and what was **seen** vs. what was **inferred**.
- Search snippets, aggregator summaries and subagent paraphrases without an
  opened link are not evidence.
- Pages that block automated reading (Reclame Aqui, LinkedIn): read through the
  user's logged-in browser or Playwright. Never bypass login, CAPTCHA or rate limits.
- Re-check the top 3 leads yourself.
- A wrong link between profile, company and owner is the worst defect (example:
  a domain that looked like the provider's belonged to another company). Keep
  inferred links labelled as inference.

## 4. Score 0-100

Rate each criterion 0-5, then weight:
`score = pain/5*25 + fit/5*25 + timing/5*20 + access/5*15 + proof/5*15`

- **Pain (25):** proven limited hours, repeated complaints, cost mentioned.
- **Fit (25):** the problem is exactly what we solve (after hours, WhatsApp, call volume).
- **Timing (20):** signal within 30 days = 5; older than 6 months = 1-2 with the date printed; or a current trigger.
- **Access (15):** owner identified with a natural professional channel.
- **Proof (15):** reliable, specific source certainly about this provider.

Bands: **80-100** approach now; **65-79** promising, confirm one signal first;
**50-64** something important missing; **below 50** drop. A lead that only
"looks like the ideal customer" with no pain or timing signal is not qualified.

Stage: **High intent** (asking for a solution or switching) > **Pain aware** >
**Trigger present** > **Profile only** (kept off the main list).

## 5. First message (draft only)

- At most 90 words: (1) mention the public signal naturally, (2) tie it to the
  exact pain, (3) one sentence on what we do, (4) end with **one** easy question.
- Use the channel the source itself offers (company profile, site contact, the
  owner's public professional page). No fake familiarity, no personal details.
- No price, and no "demo" or "15 minutes" in a first contact; offer a demo only
  to a human who already replied, never to a bot. Short blocks, link on its own
  line, then the Sufficit post as a second message.

## 6. Limits (non-negotiable)

- Only professional information published on purpose: site, company profile,
  public company registry (CNPJ) and the owner's public page.
- No data brokers, leaked bases or private groups.
- Never use a personal e-mail or mobile found in a registry; use only contacts
  the company publishes.
- Research never sends, follows, likes or comments. Every send needs the user's
  explicit approval of that draft.

## 7. Deliver the round

- Modes: **quick** (up to 5 leads), **standard** (up to 10), **deep** (up to 20, with a map of repeated pains).
- Ten strong leads beat thirty generic ones. If only 4 pass, deliver 4 and say why.
- If the user asks for speed: stop unfinished fronts, verify and score what
  exists, and state which fronts were skipped.
- Table per lead: provider, score, stage, signals (link + date), owner,
  suggested channel, draft message, then reply and date once known.
- Close with repeated pain patterns (content ideas) and the next-7-days plan.
- Record the round in the user's prospecting log so nobody is contacted twice.
