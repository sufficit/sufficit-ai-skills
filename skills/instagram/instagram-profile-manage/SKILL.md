---
name: instagram-profile-manage
description: Read and change the elements of an Instagram profile (name field, bio, link, contact buttons, highlights, pinned posts, stories) and send a direct message from the account, through the cheapest working channel - public read, Graph API or the user's logged-in browser - with a confirmed change set and post-change verification. Use when the user asks to apply, update or check Instagram profile items; for deciding what to write use instagram-profile-setup.
metadata:
  version: "1.3.1"
  author: "Sufficit"
  source: "https://github.com/sufficit/sufficit-ai-skills"
---

# Instagram profile manage

Apply profile changes with the fewest steps and verify them from outside. Decide
the copy first with [instagram-profile-setup](../instagram-profile-setup/SKILL.md);
this skill only reads, applies and checks.

## Pick the channel per item

Meta's API covers publishing and reading, not profile editing. Use this matrix and
do not search for an API that does not exist.

| Item | Read | Change |
|---|---|---|
| Bio | Public page or Graph API `GET /{ig-user-id}?fields=biography` | Logged-in web: `instagram.com/accounts/edit/`, Bio textarea + Submit |
| Name field | Public page (`og:title`) | Logged-in web: Accounts Center > Profiles > the profile > Name (rate-limited: 2 per 14 days) |
| Link / website | Public page | App only. On web `accounts/edit` the Website field is disabled ("editing links is only available on mobile") |
| Category, contact buttons | App / logged-in web | App only: Edit profile > Contact options / Category |
| Pinned posts (max 3) | Logged-in grid (pin icon) | App only in practice: "Pin to your profile" is often absent from the web `...` menu (confirmed missing for a Business account, Oct 2026) |
| Highlights | Public page (titles, covers) | App only: create from stories/archive, edit cover and title |
| Posts, Reels, Stories | Graph API / public page | Graph API Content Publishing (`media_type=REELS`/`STORIES`, Business account, Meta app token); else app |
| Delete or archive posts | Public page | App or logged-in web; never via unofficial APIs |

On the web, treat only Name (Accounts Center) and Bio as reliably editable;
link, pins, highlights, contact buttons and category are app-only. Two name
rules: Instagram rejects its own trademarks ("WhatsApp", "Instagram", "Facebook")
and the `|` character in the name field, though the bio accepts them. No API
edits bio, name, link, highlights or pins. Do not use unofficial
"private API" libraries, bots or bought tools: they violate the terms and get
accounts restricted.

## Read the current state (no login)

Run [scripts/read_profile.sh](scripts/read_profile.sh) `<handle> <out-dir>`. It
saves the Open Graph tags (name, followers, following, post count, avatar), a
rendered text dump (name field, link, highlight titles) and a screenshot of the
grid via headless Chrome with a throwaway profile. Read the screenshot to see
highlights and the first grid rows. A login wall on the JSON endpoint
(`require_login`) is normal; the HTML and render still work. Logged-out views do
not show bio line breaks reliably, pinned markers, category or contact buttons.

## Authentication for changes

Changes need the account owner's session. Most users are non-technical, so make
it a one-time login and let the Vault hold the result; do not ask a layperson to
copy cookies or paste tokens. The Vault (Identity vault, encrypted and audited) is
the only place a captured session or credential may rest.

Preferred flow:

1. Open a dedicated automation browser profile and let the user log in once in
   that window (including 2FA). This window is for the account, not their
   everyday browsing.
2. Capture the resulting session and store it in the Vault under the account's
   namespace (e.g. `personal/instagram/<handle>/session`, or a shared company
context; the `ai/` namespace is read-only for a user token, so writes there are
rejected), with its expiry. Reuse it
   from the Vault on later runs so the user does not log in again until it
   expires.
3. For a shared company account, keep the login credentials in the Vault too and
   use them only to refresh that session in the automation profile.

Rules that keep it from leaking:

- A session or credential lives in the Vault, never in a loose file, log, shell
  history, env var, or temporary profile left on disk. If you write it anywhere
  to use it, delete that copy in the same run.
- Do not lift the session out of the user's everyday browser profile; have them
  log into the automation window instead. Never ask for the password in chat and
  never disable 2FA.
- If no Vault entry and no login is available, deliver a ready-to-paste change
  set and stop.

## Apply a change set

1. Write the change set: each item with current value, new value and character
   count (bio 150, name field: keep the keyword within the first 30). Use only
   facts the user or their site confirms.
2. Get explicit approval of the final texts: the profile is public and name
   changes are rate-limited (about twice per 14 days).
3. Apply in one session, cheapest first: bio + link (one save in
   `accounts/edit`), then name, then contact buttons/category, then pins, then
   highlights. Highlights need existing stories; publish them first (API or app),
   then add them to the highlight and set the cover.
4. Use a WhatsApp link with a prefilled message to track the source:
   `https://wa.me/<country+number>?text=<url-encoded message>`.
5. Do not delete posts or highlights unless the user names them; prefer archive,
   which is reversible.

## Send a direct message (logged-in web)

Sending a DM is outbound and visible to a third party: send only when the user
asked for that recipient and text, send it once, and report it as sent only after
reading it back in the thread.

1. Resolve the thread id first. A DM is addressed to a numeric thread, never to a
   handle: `instagram.com/direct/t/<handle>/` is not a valid route and silently
   lands on the inbox, where typing and clicking reach the wrong place.
   - Known recipient: open the thread from the inbox list or a saved
     `https://www.instagram.com/direct/t/<thread-id>/`.
   - Unknown thread id: on `instagram.com/direct/inbox/` use the new-message
     (compose) control, type the handle in the **Pesquisar/Search** field, pick
     the exact handle from the results (check name and avatar, never a lookalike)
     and press **Chat/Conversar**. The URL then shows `/direct/t/<thread-id>/`;
     record that id for later turns. The profile's **Enviar mensagem/Message**
     button also opens it. A first contact may live under **Pedidos/Requests** on
     the recipient's side; that does not change the sender's thread id.
2. Confirm the open thread before typing: the header shows the recipient's handle
   and the URL carries the thread id. If either is missing, stop and resolve again.
3. Draft the text for a person reading on a phone, not as one dense line. Follow
   [human-readable notification guidance](../../sufficit/clear-technical-writing/references/notifications.md):
   - Short: a greeting line, one or two sentences on why you are writing, one
     sentence on the offer, then an easy yes/no question. Cut anything the
     recipient does not need to answer it.
   - Line breaks between blocks and a blank line before the closing question;
     a link goes on its own line. Instagram DMs show no Markdown, so no `*bold*`,
     headings or bullet syntax; one emoji at most.
   - Read the exact text back before sending: if it is a single paragraph or
     longer than about six short lines, rewrite it.
4. Type into the thread's `div[role='textbox']` (placeholder "Mensagem..."), not a
   `textarea`. In that box **Enter sends**: never put the whole message in one
   typed string with `\n` or Enter between blocks, or each block goes out as a
   separate message. Insert each line break with **Shift+Enter** (type a block,
   press Shift+Enter, type the next), check the box shows the broken lines, then
   send once with **Enter** in that box. Do not click a generic nested
   `div` guessed as the Send button: it can be a navigation element that drops
   back to the inbox without sending, and the text is lost.
5. Verify: take a screenshot or read the page and confirm the sent bubble (and any
   link preview card) in the thread. If it is not there, reopen the thread by id
   and check again before retyping, so the message is never sent twice. The web
   shows "Seen/Visto" only after the recipient reads it; absence of a read mark is
   not a failure, but do not claim delivery or reading without seeing it.
6. Only the recipient can open a conversation for a business inbox tool such as
   Chatwoot/Hermes; a DM started here is the account's first contact.

## Verify

Rerun the read script after a minute (caches lag) and compare against the change
set item by item. Report what changed, what is pending in the app (highlights,
contact buttons) and anything that failed with the exact message. A save in the
UI without the public page reflecting it is not done.
