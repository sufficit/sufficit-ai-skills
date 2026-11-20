#!/usr/bin/env bash
# Read the public state of an Instagram profile without logging in.
# Usage: read_profile.sh <handle> <out-dir>
set -euo pipefail
handle="${1:?handle}"; out="${2:?out-dir}"
mkdir -p "$out"
url="https://www.instagram.com/${handle}/"
ua_preview="facebookexternalhit/1.1"

# Open Graph tags: display name, followers, following, posts, avatar.
curl -s -m 20 -L -A "$ua_preview" "$url" -o "$out/og.html"
grep -o '<meta property="og:[^>]*>' "$out/og.html" > "$out/og.txt" || true

# Rendered page with a throwaway profile: text dump and screenshot.
chrome="$(command -v google-chrome || command -v chromium || command -v chromium-browser)"
tmp_profile="$(mktemp -d)"
trap 'rm -rf "$tmp_profile"' EXIT
flags=(--headless=new --no-sandbox --disable-gpu --user-data-dir="$tmp_profile" --virtual-time-budget=15000)
timeout 90 "$chrome" "${flags[@]}" --window-size=1280,2200 --screenshot="$out/profile.png" "$url" 2>/dev/null || true
timeout 90 "$chrome" "${flags[@]}" --dump-dom "$url" 2>/dev/null > "$out/dom.html" || true
python3 -I - "$out/dom.html" > "$out/text.txt" <<'PY'
import html, re, sys
t = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", t, flags=re.S)
lines = (l.strip() for l in html.unescape(re.sub(r"<[^>]+>", "\n", t)).splitlines())
text = "\n".join(l for l in lines if l)
print(text.split("\nMeta\nAbout")[0])
PY
echo "og: $out/og.txt  text: $out/text.txt  screenshot: $out/profile.png"
