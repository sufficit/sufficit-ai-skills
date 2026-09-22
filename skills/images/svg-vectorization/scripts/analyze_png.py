#!/usr/bin/env python3
"""Inspect a PNG before vectorizing: dimensions, alpha bbox, dominant colors,
quantized palette and ASCII maps (regions and accent mask).

A model without direct vision of the PNG uses these maps as its "eyes": they
reveal structure (bands, arms, glyphs, holes) and palette before any tracing.

Usage:
  python3 analyze_png.py image.png [--cols 64]

Output:
  - size, mode, alpha bbox, % of opaque pixels;
  - top colors (bucketed in steps of 12);
  - 8-color palette (median cut) with symbols + ASCII region map;
  - if a dominant red accent exists (>1% of pixels), an isolated ASCII map of
    the accent mask (usually the glyph that needs its own SVG layer).

Dependencies: Pillow (numpy is not required here).
"""
import argparse
from collections import Counter
from PIL import Image

SYMBOLS = '.oO#@%&*=+'


def stats(im):
    W, H = im.size
    bbox = im.getbbox()
    cnt = Counter()
    total = 0
    for r, g, b, a in im.getdata():
        if a > 200:
            cnt[(r // 12 * 12, g // 12 * 12, b // 12 * 12)] += 1
            total += 1
    print(f'size: {W}x{H} | mode: {im.mode} | alpha bbox: {bbox}')
    print(f'opaque pixels: {total} ({100 * total / (W * H):.1f}%)')
    for c, n in cnt.most_common(12):
        print(f'  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  {100 * n / max(1, total):5.1f}%')
    return total


def palette_map(im, cols=64):
    W, H = im.size
    rows = max(1, round(cols * H / W))
    ar = im.resize((cols, rows), Image.LANCZOS)
    q = ar.convert('RGB').quantize(colors=8, method=Image.MEDIANCUT)
    pal = q.getpalette()
    freq = Counter(list(q.getdata()))
    order = sorted(range(8), key=lambda i: -freq.get(i, 0))
    print(f'\nquantized palette (symbol, color, % of pixels) and {cols}x{rows} map:')
    remap = {}
    for rank, i in enumerate(order):
        r, g, b = pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2]
        share = 100 * freq.get(i, 0) / (cols * rows)
        print(f'  {SYMBOLS[rank]} #{r:02X}{g:02X}{b:02X}  {share:5.1f}%')
        remap[i] = SYMBOLS[rank]
    px = list(q.getdata())
    alpha = ar.split()[3]
    for y in range(rows):
        line = ''.join(remap[px[y * cols + x]] if alpha.getpixel((x, y)) > 120 else ' '
                       for x in range(cols))
        print(' |' + line + '|')


def accent_map(im, cols=64, thr=40):
    """Map of the accent (e.g. brand red) isolated by r>g+thr and r>b+thr."""
    W, H = im.size
    ar = im.resize((cols, max(1, round(cols * H / W))), Image.LANCZOS)
    mask = []
    n = 0
    for y in range(ar.height):
        row = []
        for x in range(cols):
            r, g, b, a = ar.getpixel((x, y))
            on = a > 120 and r > g + thr and r > b + thr
            row.append(on)
            n += on
        mask.append(row)
    share = 100 * n / (cols * ar.height)
    print(f'\naccent (r>g+{thr} & r>b+{thr}): {share:.1f}% of visible pixels')
    if share < 1.0:
        print('  (below 1% — no map; tune --red-threshold if needed)')
        return
    for row in mask:
        print(' |' + ''.join('#' if v else '.' for v in row) + '|')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('png')
    ap.add_argument('--cols', type=int, default=64)
    ap.add_argument('--red-threshold', type=int, default=40)
    args = ap.parse_args()
    im = Image.open(args.png).convert('RGBA')
    stats(im)
    palette_map(im, args.cols)
    accent_map(im, args.cols, args.red_threshold)


if __name__ == '__main__':
    main()
