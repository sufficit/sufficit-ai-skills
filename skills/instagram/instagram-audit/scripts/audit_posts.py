#!/usr/bin/env python3
"""Rank an Instagram account's posts against the account's own baseline.

Purpose: read per-post metrics from CSV and report the median, the outlier multiple,
    per-reach rates, top and bottom posts, how the top and bottom thirds differ, and
    a per-post diagnosis (hook or profile). A blank metric means unknown, never zero.
Usage:
    audit_posts.py posts.csv
    audit_posts.py posts.csv --as-of 2026-11-02 --min-age-days 3 --json
    Required columns: id, date (YYYY-MM-DD), views.
    Optional columns: format, label, reach, shares, saves, follows, leads,
    skip_rate (percent), avg_watch_s, non_follower_pct (percent).
Last modified: 2026-11-02
"""

import argparse
import csv
import datetime as dt
import json
import statistics
import sys

NUMERIC = ("reach", "shares", "saves", "follows", "leads", "skip_rate", "avg_watch_s", "non_follower_pct")
RATES = {"sends_per_reach": "shares", "saves_per_reach": "saves", "follows_per_reach": "follows", "leads_per_reach": "leads"}
COMPARED = ("skip_rate", "avg_watch_s", "non_follower_pct", *RATES)
HIT_MULTIPLE = 1.5
MISS_MULTIPLE = 0.5
TENTATIVE_AT = 10
PATTERN_AT = 30


def number(raw, column, row_id):
    text = (raw or "").strip().replace(",", ".").rstrip("%")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        raise SystemExit(f"post {row_id}: column {column} is not a number: {raw!r}") from None


def read_posts(path):
    if path == "-":
        rows = list(csv.DictReader(sys.stdin))
    else:
        with open(path, encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    posts = []
    for row in rows:
        row_id = (row.get("id") or "").strip()
        if not row_id:
            raise SystemExit("every row needs an id")
        try:
            posted = dt.date.fromisoformat((row.get("date") or "").strip())
        except ValueError:
            raise SystemExit(f"post {row_id}: date must be YYYY-MM-DD") from None
        views = number(row.get("views"), "views", row_id)
        if views is None:
            raise SystemExit(f"post {row_id}: views is required")
        post = {
            "id": row_id,
            "date": posted.isoformat(),
            "format": (row.get("format") or "").strip(),
            "label": (row.get("label") or "").strip(),
            "views": views,
        }
        for column in NUMERIC:
            post[column] = number(row.get(column), column, row_id)
        posts.append(post)
    return posts


def add_rates(post, baseline):
    post["outlier"] = post["views"] / baseline if baseline else None
    reach = post["reach"]
    for rate, column in RATES.items():
        value = post[column]
        post[rate] = value / reach if value is not None and reach else None


def median_of(posts, column):
    values = [post[column] for post in posts if post[column] is not None]
    return statistics.median(values) if values else None


def diagnose(post, medians):
    outlier = post["outlier"]
    if outlier is None:
        return "no baseline"
    if outlier >= HIT_MULTIPLE:
        follows, usual = post["follows_per_reach"], medians["follows_per_reach"]
        if follows is not None and usual is not None and follows < usual:
            return "attention without follows: check the profile"
        return "hit"
    if outlier < MISS_MULTIPLE:
        skip, usual = post["skip_rate"], medians["skip_rate"]
        if skip is None or usual is None:
            return "low views: skip rate unknown"
        return "low views: check the hook" if skip > usual else "low views: hook not the cause"
    return "normal"


def confidence(count):
    if count < TENTATIVE_AT:
        return "insufficient: report figures, do not claim a pattern"
    if count < PATTERN_AT:
        return "tentative: treat differences as leads to test"
    return "pattern: differences can support a recommendation"


def audit(posts, as_of, min_age_days):
    cutoff = as_of - dt.timedelta(days=min_age_days)
    mature = [post for post in posts if dt.date.fromisoformat(post["date"]) <= cutoff]
    baseline = statistics.median(post["views"] for post in mature) if mature else None
    for post in mature:
        add_rates(post, baseline)
    medians = {column: median_of(mature, column) for column in COMPARED}
    for post in mature:
        post["diagnosis"] = diagnose(post, medians)

    ranked = sorted(mature, key=lambda post: (post["outlier"] or 0, post["sends_per_reach"] or 0), reverse=True)
    third = len(ranked) // 3
    top, bottom = ranked[:third], ranked[-third:] if third else []
    separation = {}
    for column in COMPARED:
        high, low = median_of(top, column), median_of(bottom, column)
        if high is not None and low is not None:
            separation[column] = {"top": high, "bottom": low}
    groups = {}
    for key in ("format", "label"):
        names = sorted({post[key] for post in mature if post[key]})
        groups[key] = {
            name: {
                "posts": sum(post[key] == name for post in mature),
                "medianOutlier": median_of([post for post in mature if post[key] == name], "outlier"),
            }
            for name in names
        }
    return {
        "posts": len(posts),
        "analysed": len(mature),
        "tooRecent": len(posts) - len(mature),
        "baselineMedianViews": baseline,
        "confidence": confidence(len(mature)),
        "ranked": ranked,
        "separation": separation,
        "groups": groups,
    }


def fmt(value, percent=False):
    if value is None:
        return "?"
    return f"{value * 100:.2f}%" if percent else f"{value:,.1f}"


def render_post(post):
    print(
        f"  {fmt(post['outlier']):>7}x  {post['id']:<20} views {post['views']:>10,.0f}"
        f"  skip {fmt(post['skip_rate'])}  sends/reach {fmt(post['sends_per_reach'], True)}"
        f"  follows/reach {fmt(post['follows_per_reach'], True)}  {post['diagnosis']}"
    )


def render(result, shown=5):
    print(f"AUDIT - {result['analysed']} of {result['posts']} posts analysed, {result['tooRecent']} too recent")
    print(f"Baseline median views: {fmt(result['baselineMedianViews'])}")
    print(f"Confidence: {result['confidence']}\n")
    ranked = result["ranked"]
    print("TOP BY OUTLIER MULTIPLE")
    for post in ranked[:shown]:
        render_post(post)
    if len(ranked) > shown:
        print("\nBOTTOM BY OUTLIER MULTIPLE")
        for post in ranked[-shown:]:
            render_post(post)
    if result["separation"]:
        print("\nTOP THIRD VS BOTTOM THIRD (medians)")
        for column, pair in result["separation"].items():
            percent = column in RATES
            print(f"  {column:<20} {fmt(pair['top'], percent):>10} vs {fmt(pair['bottom'], percent):>10}")
    for key, group in result["groups"].items():
        if group:
            print(f"\nMEDIAN OUTLIER BY {key.upper()}")
            for name, stats in group.items():
                print(f"  {name:<20} {fmt(stats['medianOutlier']):>7}x  n={stats['posts']}")


def main():
    parser = argparse.ArgumentParser(description="Audit Instagram posts against the account's own median.")
    parser.add_argument("input", help="CSV file, or - for stdin")
    parser.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.datetime.now(dt.timezone.utc).date())
    parser.add_argument("--min-age-days", type=int, default=3, help="skip posts younger than this (default 3)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = audit(read_posts(args.input), args.as_of, args.min_age_days)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        render(result)


if __name__ == "__main__":
    main()
