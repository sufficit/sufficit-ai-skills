#!/usr/bin/env python3
"""Turn a Reel script into a timed beat sheet before recording.

Purpose: estimate each line's spoken length from word count and flag a hook past
    3 seconds, a beat past 4 seconds, runs with nothing concrete and a missing echo
    of the hook, in Portuguese or English. Timings plan an edit; they do not replace
    a test recording. Calibrate --wpm by timing the speaker reading a script aloud.
Usage:
    beat_sheet.py script.txt --target 30
    beat_sheet.py script.txt --wpm 170 --json
    beat_sheet.py - < script.txt
Last modified: 2026-11-02

Adapted from skills/ig-reel/beats.py in Jakeschincariol/instagram-agent-skill (MIT,
see ../LICENSE). Sufficit added Portuguese support and accent-insensitive matching,
stopped counting a lone dash as a word and warns when the rate is not calibrated.
"""

import argparse
import json
import re
import sys
import unicodedata

DEFAULT_WPM = 150  # Planning assumption, not a measured Portuguese average.
HOOK_WINDOW = 3.0
MAX_BEAT = 4.0
ABSTRACT_RUN = 3

WORD_RE = re.compile(r"\$?[^\W_][\w'’%-]*\$?")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]*")
NUMBER_RE = re.compile(
    r"\d|\b(?:zero|dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|vinte|trinta"
    r"|cem|mil|milh[aã]o|milh[oõ]es|two|three|four|five|six|seven|eight|nine|ten"
    r"|twenty|thirty|hundred|thousand|million)\b",
    re.IGNORECASE,
)
NAME_RE = re.compile(r"\b[A-ZÀ-Ý][a-zà-ÿ]{2,}\b")
SENTENCE_START_RE = re.compile(r"(?:^|[.!?:\n])\s*$")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "do", "for", "from", "has", "have",
    "i", "if", "in", "is", "it", "me", "my", "no", "not", "of", "on", "one", "or", "our", "so",
    "that", "the", "this", "to", "was", "we", "will", "with", "you", "your",
    "as", "ao", "aos", "com", "como", "da", "das", "de", "do", "dos", "e", "ela", "ele", "em",
    "era", "esse", "essa", "este", "esta", "eu", "foi", "isso", "mais", "mas", "meu", "minha",
    "na", "nas", "no", "nos", "o", "os", "ou", "para", "pela", "pelo", "por", "pra", "que",
    "se", "sem", "seu", "sua", "tem", "um", "uma", "voce",
}


def fold(text):
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def words(text):
    # A spoken amount such as 18.000 or 18,000 is one token here.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d)", "", text))


def is_concrete(text):
    if NUMBER_RE.search(text):
        return True
    return any(not SENTENCE_START_RE.search(text[: match.start()]) for match in NAME_RE.finditer(text))


def timecode(seconds):
    minutes, rest = divmod(seconds, 60)
    return f"{int(minutes)}:{rest:04.1f}"


def split_beats(raw, words_per_second):
    """One line is one beat, unless the line is too long to be one."""
    beats = []
    for line in (item.strip() for item in raw.splitlines()):
        if not line:
            continue
        if len(words(line)) / words_per_second <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        buffer = ""
        for part in (item.strip() for item in SENTENCE_RE.findall(line)):
            candidate = f"{buffer} {part}".strip()
            if buffer and len(words(candidate)) / words_per_second > MAX_BEAT:
                beats.append(buffer)
                buffer = part
            else:
                buffer = candidate
        if buffer:
            beats.append(buffer)
    return beats


def content_words(text):
    return {fold(word) for word in words(text)} - STOPWORDS


def analyse(raw, wpm=DEFAULT_WPM, target=None, calibrated=False):
    words_per_second = wpm / 60
    beats = split_beats(raw, words_per_second)
    if not beats:
        return None

    rows, clock = [], 0.0
    for number, text in enumerate(beats, 1):
        count = len(words(text))
        duration = count / words_per_second
        rows.append(
            {
                "beat": number,
                "start": round(clock, 2),
                "seconds": round(duration, 2),
                "words": count,
                "text": text,
                "concrete": is_concrete(text),
                "flags": [],
            }
        )
        clock += duration

    notes = []
    if not calibrated:
        notes.append(f"Rate is the {wpm:g} wpm default; time the speaker and pass --wpm.")
    hook = rows[0]
    if hook["seconds"] > HOOK_WINDOW:
        hook["flags"].append(f"hook runs {hook['seconds']:.1f}s")
        notes.append(f"Cut the hook to {int(HOOK_WINDOW * words_per_second)} words or fewer.")
    if not hook["concrete"]:
        notes.append("The hook has no number or name.")

    long_beats = [row for row in rows if row["seconds"] > MAX_BEAT]
    for row in long_beats:
        row["flags"].append(f"{row['seconds']:.1f}s on one beat")
    if long_beats:
        numbers = ", ".join(str(row["beat"]) for row in long_beats)
        notes.append(f"Beat(s) {numbers}: split the line or change what is on screen inside it.")

    run = []
    for row in rows:
        run = [] if row["concrete"] else [*run, row["beat"]]
        if len(run) == ABSTRACT_RUN:
            notes.append(f"Beats {run[0]}-{run[-1]} have nothing concrete; add a real number or name.")

    shared = sorted(content_words(hook["text"]) & content_words(rows[-1]["text"])) if len(rows) > 1 else []
    if shared:
        notes.append(f"Last beat echoes the hook: {', '.join(shared[:3])}.")
    else:
        notes.append("Last beat does not echo the hook; consider repeating one of its words.")

    total = round(clock, 2)
    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Length on target: {total:.1f}s of {target:g}s.")
        elif delta > 0:
            notes.append(f"{delta:.1f}s over target; cut about {int(delta * words_per_second)} words.")
        else:
            notes.append(f"{-delta:.1f}s under target; keep it short unless something is missing.")

    return {
        "wpm": wpm,
        "calibrated": calibrated,
        "target": target,
        "totalSeconds": total,
        "totalWords": sum(row["words"] for row in rows),
        "beats": rows,
        "notes": notes,
    }


def render(result):
    print(f"BEAT SHEET - {result['totalWords']} words, about {result['totalSeconds']:.1f}s at {result['wpm']:g} wpm\n")
    for row in result["beats"]:
        print(f"  {timecode(row['start'])}  {row['seconds']:4.1f}s  {row['text']}")
        for flag in row["flags"]:
            print(f"  {'':>14}  ^ {flag}")
    print()
    for note in result["notes"]:
        print(f"  - {note}")


def main():
    parser = argparse.ArgumentParser(description="Time a Reel script into a beat sheet.")
    parser.add_argument("input", nargs="?", default="-", help="script file, or - for stdin")
    parser.add_argument("--wpm", type=float, help=f"speaker's rate (default {DEFAULT_WPM}, uncalibrated)")
    parser.add_argument("--target", type=float, help="target length in seconds")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as handle:
            raw = handle.read()
    result = analyse(raw, args.wpm or DEFAULT_WPM, args.target, args.wpm is not None)
    if result is None:
        print("empty script", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        render(result)


if __name__ == "__main__":
    main()
