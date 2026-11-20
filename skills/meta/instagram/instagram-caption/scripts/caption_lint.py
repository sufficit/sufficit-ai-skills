#!/usr/bin/env python3
"""Lint an Instagram caption and print what the feed shows before "... more".

Purpose: check length, first line, hashtags, dead links, call to action, emoji
    density and search terms in Portuguese or English captions. Exits 1 when a
    check fails, 0 otherwise (warnings need a decision, not a rewrite).
Usage:
    caption_lint.py caption.txt
    caption_lint.py caption.txt --keywords "gestao financeira,fluxo de caixa"
    caption_lint.py - --json < caption.txt
    caption_lint.py caption.txt --truncate 110 --hashtag-limit 5
Last modified: 2026-11-02

Adapted from skills/ig-caption/caption.py in Jakeschincariol/instagram-agent-skill
(MIT, see ../LICENSE). Sufficit added Portuguese support and fixed hashtag parsing
for accented words and the case-insensitive keyword call-to-action match.
"""

import argparse
import json
import re
import sys
import textwrap
import unicodedata

CAPTION_LIMIT = 2200  # Hard caption limit.
TRUNCATE_AT = 125  # Approximate feed cut; varies by device, so keep a margin.
HASHTAG_LIMIT = 5  # Per-post cap announced by Instagram in December 2025.
EMOJI_WARN_PER_100 = 4

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
LINK_RE = re.compile(
    r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app|br)(?:\.br)?\b(?:/\S*)?",
    re.IGNORECASE,
)
EMOJI_RE = re.compile("[\u2190-\u21ff\u2600-\u27bf\U0001f300-\U0001faff]")
GREETING_RE = re.compile(
    r"^(?:oi|ol[aá]|e a[ií]|bom dia|boa tarde|boa noite|hey|hi|hello)\b", re.IGNORECASE
)
NUMBER_RE = re.compile(
    r"\d|\b(?:zero|dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|vinte|trinta"
    r"|cem|mil|milh[aã]o|milh[oõ]es|two|three|four|five|six|seven|eight|nine|ten"
    r"|twenty|thirty|hundred|thousand|million)\b",
    re.IGNORECASE,
)
NAME_RE = re.compile(r"\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b")
SENTENCE_START_RE = re.compile(r"(?:^|[.!?:\n])\s*$")

ASKS = [
    (r"(?i:comment)(?i:\s+the\s+word)?\s+\"?[A-Z0-9]{2,}\b", "comment a keyword"),
    (r"(?i:comente|comenta)(?i:\s+a\s+palavra)?\s+\"?[A-ZÀ-Ý0-9]{2,}\b", "comment a keyword"),
    (r"(?i:\b(?:dm|message) me\b|\bme chama\b|\bchama no\b|\bmande? (?:uma )?(?:dm|mensagem)\b)", "message"),
    (r"(?i:\bsave (?:this|it)\b|\bsalv[ea] (?:este|esse|esta|essa|o post|para|pra)\b)", "save"),
    (r"(?i:\bshare (?:this|it)\b|\bcompartilh[ea] (?:este|esse|esta|essa|o post|com)\b|\benvi[ea] (?:para|pra)\b)", "share"),
    (r"(?i:\bfollow (?:me|for)\b|\bsiga\b|\bsegue a gente\b)", "follow"),
    (r"(?i:\blink in (?:my |the )?bio\b|\blink na bio\b)", "link in bio"),
    (r"(?i:\bfale conosco\b|\bfale com\b|\bchame no whatsapp\b|\bagende\b|\bbook a\b)", "contact"),
    (r"(?i:\btell me\b|\bwhich one\b|\bme conta\b|\bconta (?:aqui|nos coment)\b|\bqual (?:deles|voc[eê])\b)", "answer a question"),
]
ASKS = [(re.compile(pattern), name) for pattern, name in ASKS]

FILLER_TAGS = {
    "#viral", "#fyp", "#explore", "#explorepage", "#explorar", "#foryou", "#foryoupage",
    "#paravoce", "#paravocê", "#trending", "#instagood", "#love", "#follow", "#like4like",
    "#reels", "#reelsinstagram", "#viralreels", "#instadaily", "#viralizar", "#sigodevolta",
}


def fold(text):
    """Lowercase and drop accents so 'gestao' finds 'gestão'."""
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def is_concrete(window):
    if NUMBER_RE.search(window):
        return True
    return any(
        not SENTENCE_START_RE.search(window[: match.start()]) for match in NAME_RE.finditer(window)
    )


def analyse(text, cut=TRUNCATE_AT, keywords=None, hashtag_limit=HASHTAG_LIMIT):
    caption = text.strip()
    chars = len(caption)
    first_line = caption.split("\n", 1)[0].strip()
    window = caption[:cut]
    tag_matches = list(HASHTAG_RE.finditer(caption))
    tags = [match.group(1) for match in tag_matches]
    filler = [tag for tag in tags if tag.casefold() in FILLER_TAGS]
    links = LINK_RE.findall(caption)
    emoji = EMOJI_RE.findall(caption)
    asks = sorted({name for pattern, name in ASKS if pattern.search(caption)})
    keywords = [term.strip() for term in (keywords or []) if term.strip()]
    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    over = chars - CAPTION_LIMIT
    add(
        "LENGTH",
        "FAIL" if over > 0 else "PASS",
        f"{chars} / {CAPTION_LIMIT} characters" + (f", {over} over" if over > 0 else ""),
    )

    if not first_line:
        add("FIRST LINE", "FAIL", "the caption is empty")
    elif first_line[0] in "#@":
        add("FIRST LINE", "FAIL", "opens on a hashtag or mention instead of a sentence")
    elif GREETING_RE.search(first_line):
        add("FIRST LINE", "WARN", "opens on a greeting, which spends the visible window")
    elif len(first_line) > cut:
        add("FIRST LINE", "WARN", f"{len(first_line)} characters, cut at about {cut} mid-thought")
    else:
        add("FIRST LINE", "PASS", f"{len(first_line)} characters, lands whole")

    concrete = is_concrete(window)
    add(
        "HOOK IS CONCRETE",
        "PASS" if concrete else "WARN",
        "number or name in the visible window" if concrete else "nothing checkable before the cut",
    )

    if len(tags) > hashtag_limit:
        add("HASHTAGS", "FAIL", f"{len(tags)} tags, over the cap of {hashtag_limit}")
    elif filler:
        add("HASHTAGS", "WARN", f"{len(tags)} tag(s), generic: {', '.join(filler[:3])}")
    else:
        add("HASHTAGS", "PASS", f"{len(tags)} tag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if any(match.start(1) < cut for match in tag_matches):
        add("TAG PLACEMENT", "WARN", "a hashtag sits inside the visible window")
    else:
        add("TAG PLACEMENT", "PASS", "no hashtag in the visible window")

    if links:
        add("LINKS", "WARN", f"{len(links)} link(s) in the body; captions are not clickable")
    else:
        add("LINKS", "PASS", "no dead links in the body")

    if len(asks) == 1:
        add("ONE ASK", "PASS", f"one call to action: {asks[0]}")
    elif not asks:
        add("ONE ASK", "WARN", "no call to action recognised; decide what this post is for")
    else:
        add("ONE ASK", "WARN", f"{len(asks)} asks: {', '.join(asks)}")

    density = len(emoji) * 100 / max(chars, 1)
    add(
        "EMOJI",
        "WARN" if density > EMOJI_WARN_PER_100 else "PASS",
        f"{len(emoji)} emoji, {density:.1f} per 100 characters",
    )

    if keywords:
        folded, folded_window = fold(caption), fold(window)
        found = [term for term in keywords if fold(term) in folded]
        missing = [term for term in keywords if term not in found]
        visible = [term for term in found if fold(term) in folded_window]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        detail = f"{len(found)}/{len(keywords)} present, {len(visible)} in the visible window"
        add("SEARCH TERMS", status, detail + (f". Missing: {', '.join(missing)}" if missing else ""))

    statuses = {check["status"] for check in checks}
    verdict = "FIX" if "FAIL" in statuses else ("REVIEW" if "WARN" in statuses else "READY")
    return {
        "characters": chars,
        "limit": CAPTION_LIMIT,
        "truncateAt": cut,
        "visible": window,
        "truncated": chars > cut,
        "hashtags": tags,
        "links": links,
        "emoji": len(emoji),
        "asks": asks,
        "checks": checks,
        "verdict": verdict,
    }


def render(result, width=52):
    print(f"CAPTION LINT - {result['characters']} / {result['limit']} chars\n")
    print("  WHAT THE FEED SHOWS")
    print("  +" + "-" * (width + 2) + "+")
    for raw_line in result["visible"].split("\n"):
        for line in textwrap.wrap(raw_line, width) or [""]:
            print(f"  | {line:<{width}} |")
    tail = "... more" if result["truncated"] else "(fits)"
    print("  +" + "-" * (width - len(tail)) + f" {tail} " + "+\n")
    for check in result["checks"]:
        print(f"  {check['status']:<5} {check['check']:<17} {check['detail']}")
    print(f"\n  VERDICT  {result['verdict']}")


def main():
    parser = argparse.ArgumentParser(description="Lint an Instagram caption.")
    parser.add_argument("input", nargs="?", default="-", help="caption file, or - for stdin")
    parser.add_argument("--truncate", type=int, default=TRUNCATE_AT)
    parser.add_argument("--hashtag-limit", type=int, default=HASHTAG_LIMIT)
    parser.add_argument("--keywords", default="", help="comma-separated search terms")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as handle:
            raw = handle.read()
    result = analyse(raw, args.truncate, args.keywords.split(","), args.hashtag_limit)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        render(result)
    sys.exit(1 if result["verdict"] == "FIX" else 0)


if __name__ == "__main__":
    main()
