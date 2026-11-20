---
name: instagram-audit
description: "Audit an Instagram account's published posts from their insights: rank each post against the account's own median, compare per-reach rates, separate hook problems from profile problems and say what to stop and repeat. Use when the user asks what is working, why a post flopped or to read Instagram analytics; it does not write posts or change the profile."
metadata:
  version: "1.0.0"
  author: "Jake Schincariol / Sufficit"
  source: "https://github.com/Jakeschincariol/instagram-agent-skill/tree/d03c56bb598be770c60b201f94237e5d1a4268a6/skills/ig-audit"
---

# Instagram audit

The account's own posts are the evidence. General Instagram advice, including the
other skills here, is only a starting assumption. Raw views mostly reflect audience
size, so compare each post with what this account normally gets.

## Collect the data

Use whichever source exists, and name it in the report:

| Source | Gives | Notes |
| --- | --- | --- |
| Screenshots of in-app insights | Everything the app shows, including the retention chart and skip rate | No technical setup; do not log in to the user's account |
| Export or spreadsheet from the user | Whatever columns it has | Confirm the period and the definition of each column |
| Graph API `GET /{ig-media-id}/insights` | `views`, `reach`, `saved`, `shares`, `ig_reels_avg_watch_time`, and `follows` and `profile_visits` on feed posts and stories | Needs a professional account and an insights token from the Vault |

Check the [current metric reference](https://developers.facebook.com/documentation/instagram-platform/reference/instagram-media/insights)
before relying on an API metric: Meta changes them. The API can return an empty set
instead of 0 and can lag up to 48 hours, so leave unavailable values blank. Metrics
also need to come from one period and definition: do not mix old and new "views" data
without saying so.

Aim for the last 30 posts. Add leads per post when the business tracks them, because
views that bring no customers are not a win for a company account.

## Run the numbers

Write one row per post and do not compute by hand:

```csv
id,date,format,label,views,reach,shares,saves,follows,leads,skip_rate,avg_watch_s,non_follower_pct
DA1,2026-10-02,reel,client case,12000,9000,90,40,12,3,28,11.5,62
DA2,2026-10-09,carousel,how it works,800,700,1,6,,0,,,18
```

```bash
python3 -B scripts/audit_posts.py posts.csv
```

Only `id`, `date` and `views` are required. `label` is whatever you want to compare:
theme, hook type or offer. Posts under three days old are left out (`--min-age-days`)
because they have not finished collecting views.

| Metric | Formula | Answers |
| --- | --- | --- |
| Outlier multiple | views / account median | Was this a real hit or a normal day? |
| Skip rate | From the app: views that left in the first 3 seconds | Did the hook hold? |
| Average watch time | From insights | Did the middle hold? |
| Non-follower share | From insights | Did it reach new people? |
| Sends per reach | shares / reach | Did someone pass it on? |
| Follows and leads per reach | follows or leads / reach | Did the attention convert? |

Rank by outlier multiple, using sends per reach to break ties. Do not cite these
metrics as Instagram's ranking formula: the platform has not published one, and fixed
"healthy" benchmarks from blogs are not evidence. Compare the account with itself.

## Read the result

1. **Separate the two failures.** Low views with a skip rate above the account's usual
   point to the hook. High views with follows below the usual point to the profile: stop
   rewriting hooks and use
   [instagram-profile-setup](../instagram-profile-setup/SKILL.md).
2. **Compare top and bottom** for skip rate, format, label and length. Check day and
   time last, and only when nothing else explains the difference.
3. **Open the posts** before concluding. The script finds which posts differ, not why.
   Read the first seconds of the top and bottom posts and name what changed.
4. **Respect the sample size.** The script states its confidence. Under 10 posts, report
   the figures and claim no pattern. Under 30, offer leads to test. A pattern from one
   viral post is an anecdote. Correlation does not prove cause, so frame the advice as
   the next test.

Never fill a missing metric, never round a weak result up and never invent a reason.
Saying the data shows nothing is a valid outcome.

## Deliverable

Reply in the user's language with:

1. Source, period, posts analysed, baseline median and confidence.
2. Top and bottom posts by outlier multiple, with the supporting metrics.
3. Findings as claims with their evidence and sample size.
4. What to stop, what to repeat and the one test for the next posts.
5. Metrics that were unavailable, and what collecting them would settle.

## Credit

Method adapted from `ig-audit` in
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) by
Jake Schincariol, under the MIT license in [LICENSE](LICENSE).
