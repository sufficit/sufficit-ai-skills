---
name: instagram-profile-manage
description: Read and change the elements of an Instagram profile (name field, bio, link, contact buttons, highlights, pinned posts, stories) through the cheapest working channel - public read, Graph API or the user's logged-in browser - with a confirmed change set and post-change verification. Use when the user asks to apply, update or check Instagram profile items; for deciding what to write use instagram-profile-setup.
metadata:
  version: "1.1.0"
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
| Name field, bio, link, followers | Public page (no login) or Graph API `GET /{ig-user-id}?fields=name,biography,website` | Logged-in web: `instagram.com/accounts/edit/` (bio, link); name in Accounts Center (rate-limited) |
| Category, contact buttons | App / logged-in web | App: Edit profile > Contact options / Category |
| Pinned posts (max 3) | Logged-in grid (pin icon) | Post `...` menu > Pin to profile (web or app) |
| Highlights | Public page (titles, covers) | App: create from stories/archive, edit cover and title |
| Posts, Reels, Stories | Graph API / public page | Graph API Content Publishing (`media_type=REELS`/`STORIES`, Business account, Meta app token); else app |
| Delete or archive posts | Public page | App or logged-in web; never via unofficial APIs |

No API edits bio, name, link, highlights or pins. Do not use unofficial
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
   namespace (e.g. `ai/instagram/<handle>/session`), with its expiry. Reuse it
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

## Verify

Rerun the read script after a minute (caches lag) and compare against the change
set item by item. Report what changed, what is pending in the app (highlights,
contact buttons) and anything that failed with the exact message. A save in the
UI without the public page reflecting it is not done.
