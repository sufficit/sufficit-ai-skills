#!/usr/bin/env python3
"""Validate an SVG produced by trace_png.py against the reference PNG.

Golden rule: validate the FILE on disk, never the tracer's in-memory shapes.
And distrust any single number: this script validates through two routes
(own parse + headless Chrome, when available) — in the real case that
originated this skill, a typo in the Bézier flattening made one verifier
report IoU 0.46 for a file that was actually 0.98.

What it does:
  1. Parses the SVG (ElementTree) and its path(s) — absolute M/C/Z.
  2. Rasterizes by flattening Béziers (correct formula:
     (1-t)^3*P0 + 3(1-t)^2*t*C1 + 3(1-t)*t^2*C2 + t^3*P3) with accumulated
     XOR (evenodd), on a canvas with the viewBox aspect ratio.
  3. Reference masks (alpha and accent) cropped by the SAME window — the
     silhouette bbox — and resized to that canvas. Never normalize each
     layer by its own bbox: layers sit at different relative positions
     inside the icon and would end up at different scales (it looks like a
     shape error, but it is misalignment).
  4. Per-layer IoU with a verdict: PASS >= 0.96 | WARN >= 0.90 | FAIL.
  5. PNG comparison panel (reference | flattened render).
  6. --chrome: renders the file itself in headless Chrome (the browser's
     real engine) and measures IoU again. Do not use `magick svg:` for this
     — ImageMagick treats SVG as MSVG and renders it empty.

Usage:
  python3 verify_svg.py icon.svg reference.png [--accent-expr "r>g+40 and r>b+40"]
      [--size 512] [--panel panel.png] [--chrome]

Dependencies: Pillow, numpy. Optional: google-chrome/chromium on PATH.
"""
import argparse
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageChops

NS = '{http://www.w3.org/2000/svg}'
ACCENT_EVAL = {'r': lambda p: p[0], 'g': lambda p: p[1],
               'b': lambda p: p[2], 'a': lambda p: p[3]}


def accent_match(rgba, expr):
    try:
        return bool(eval(expr, {'__builtins__': {}},
                         {k: fn(rgba) for k, fn in ACCENT_EVAL.items()}))
    except Exception:
        return False


def parse_path(d):
    """Absolute M/C/Z -> list of polygons (Béziers flattened)."""
    tokens = re.findall(r'[MLCZ]|-?\d+\.?\d*', d)
    subs, cur, last = [], [], (0.0, 0.0)
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == 'M':
            if cur:
                subs.append(cur)
            x, y = float(tokens[i + 1]), float(tokens[i + 2])
            i += 3
            cur = [(x, y)]
            last = (x, y)
        elif t == 'C':
            c1 = (float(tokens[i + 1]), float(tokens[i + 2]))
            c2 = (float(tokens[i + 3]), float(tokens[i + 4]))
            p3 = (float(tokens[i + 5]), float(tokens[i + 6]))
            i += 7
            for s in range(1, 13):  # 12 segments per curve
                t_ = s / 12
                mt = 1 - t_
                cur.append((mt**3 * last[0] + 3 * mt * mt * t_ * c1[0]
                            + 3 * mt * t_ * t_ * c2[0] + t_**3 * p3[0],
                            mt**3 * last[1] + 3 * mt * mt * t_ * c1[1]
                            + 3 * mt * t_ * t_ * c2[1] + t_**3 * p3[1]))
            last = p3
        elif t == 'Z':
            i += 1
            if cur:
                subs.append(cur)
                cur = []
        else:
            i += 1
    if cur:
        subs.append(cur)
    return subs


def raster(d, vw, vh, size):
    """Accumulated XOR of the subpaths (evenodd) at the viewBox aspect."""
    w = size
    h = max(1, round(size * vh / vw))
    sx, sy = w / vw, h / vh
    acc = Image.new('1', (w, h), 0)
    for poly in parse_path(d):
        if len(poly) < 3:
            continue
        tmp = Image.new('1', (w, h), 0)
        ImageDraw.Draw(tmp).polygon([(x * sx, y * sy) for x, y in poly], fill=1)
        acc = ImageChops.logical_xor(acc, tmp)
    return np.array(acc, dtype=bool), w, h


def ref_masks(png, expr):
    im = Image.open(png).convert('RGBA')
    p = im.load()
    w, h = im.size
    sil = np.zeros((h, w), dtype=bool)
    acc = np.zeros((h, w), dtype=bool)
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if a > 128:
                sil[y, x] = True
                if accent_match((r, g, b, a), expr):
                    acc[y, x] = True
    return im, sil, acc


def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def window_resize(mask, box, w, h):
    """Crop by the COMMON window (silhouette bbox) and resize to (w, h)."""
    x0, y0, x1, y1 = box
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    img = Image.fromarray((sub * 255).astype(np.uint8), 'L').resize((w, h), Image.BILINEAR)
    return np.array(img) > 127


def iou(a, b):
    u = int(np.logical_or(a, b).sum())
    return int(np.logical_and(a, b).sum()) / u if u else 0.0


def verdict(v):
    return 'PASS' if v >= 0.96 else ('WARN' if v >= 0.90 else 'FAIL')


def chrome_render(svg_path, size, workdir):
    """Render the SVG in headless Chrome; returns RGBA or None."""
    chrome = shutil.which('google-chrome') or shutil.which('chromium')
    if not chrome:
        return None
    html = (f'<!doctype html><html><head><style>html,body{{margin:0;background:#fff}}'
            f'img{{width:{size}px;display:block}}</style></head><body>'
            f'<img src="file://{svg_path}"></body></html>')
    hp = f'{workdir}/render.html'
    pp = f'{workdir}/chrome.png'
    open(hp, 'w').write(html)
    r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
                        f'--screenshot={pp}', f'--window-size={size},{size}',
                        '--default-background-color=FFFFFFFF', f'file://{hp}'],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return None
    return Image.open(pp).convert('RGBA')


def masks_from_opaque(img, expr):
    """Silhouette = non-white pixels; accent = expression (white background)."""
    p = img.load()
    w, h = img.size
    sil = np.zeros((h, w), dtype=bool)
    acc = np.zeros((h, w), dtype=bool)
    for y in range(h):
        for x in range(w):
            r, g, b, a = p[x, y]
            if r < 250 or g < 250 or b < 250:
                sil[y, x] = True
                if accent_match((r, g, b, a), expr):
                    acc[y, x] = True
    return sil, acc


def main():
    ap = argparse.ArgumentParser(description='Validate an SVG vs reference PNG (IoU).')
    ap.add_argument('svg')
    ap.add_argument('png')
    ap.add_argument('--accent-expr', default='r>g+40 and r>b+40')
    ap.add_argument('--size', type=int, default=512)
    ap.add_argument('--panel')
    ap.add_argument('--chrome', action='store_true',
                    help='also validate with a headless Chrome render')
    args = ap.parse_args()

    root = ET.parse(args.svg).getroot()
    vb = [float(v) for v in root.get('viewBox').split()]
    vw, vh = vb[2], vb[3]
    paths = [el.get('d') for el in root.iter(NS + 'path')]
    print(f'[svg] viewBox={vb} paths={len(paths)}')
    if len(paths) < 1:
        raise SystemExit('SVG has no paths')

    # reference: COMMON window = silhouette bbox (not each layer's own!)
    ref_im, sil_ref, acc_ref = ref_masks(args.png, args.accent_expr)
    ref_box = bbox(sil_ref)
    if ref_box is None:
        raise SystemExit('reference has no opaque pixels')

    sil_s, w, h = raster(paths[0], vw, vh, args.size)
    acc_s, _, _ = (raster(paths[1], vw, vh, args.size) if len(paths) > 1
                   else (np.zeros_like(sil_s), w, h))
    sil_r = window_resize(sil_ref, ref_box, w, h)
    acc_r = window_resize(acc_ref, ref_box, w, h)

    v1, v2 = iou(sil_s, sil_r), iou(acc_s, acc_r)
    print(f'[own parse]  IoU base={v1:.4f} ({verdict(v1)}) '
          f'accent={v2:.4f} ({verdict(v2)})')

    if args.chrome:
        with tempfile.TemporaryDirectory() as td:
            img = chrome_render(args.svg, args.size, td)
        if img is None:
            print('[chrome] unavailable — skipping independent route')
        else:
            cs, ca = masks_from_opaque(img, args.accent_expr)
            cbox = bbox(cs)
            cs_n = window_resize(cs, cbox, w, h)
            ca_n = window_resize(ca, cbox, w, h)
            c1, c2 = iou(cs_n, sil_r), iou(ca_n, acc_r)
            print(f'[chrome]     IoU base={c1:.4f} ({verdict(c1)}) '
                  f'accent={c2:.4f} ({verdict(c2)})')
            v1, v2 = min(v1, c1), min(v2, c2)

    if args.panel:
        x0, y0, x1, y1 = ref_box
        ref_crop = ref_im.crop((x0, y0, x1 + 1, y1 + 1)).resize((w, h), Image.LANCZOS)
        r_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        gray = Image.new('RGBA', (w, h), (150, 150, 151, 255))
        red = Image.new('RGBA', (w, h), (214, 42, 44, 255))
        r_img.paste(gray, (0, 0), Image.fromarray((sil_s * 255).astype(np.uint8), 'L'))
        r_img.paste(red, (0, 0), Image.fromarray((acc_s * 255).astype(np.uint8), 'L'))
        panel = Image.new('RGB', (w * 2 + 60, h + 40), (255, 255, 255))
        panel.paste(ref_crop, (20, 20), ref_crop)
        panel.paste(r_img, (w + 40, 20), r_img)
        panel.save(args.panel)
        print(f'[panel] {args.panel}')

    ok = v1 >= 0.90 and v2 >= 0.90
    print(f'[verdict] {"OK" if ok else "FAILED"} (minimum 0.90; target 0.96)')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
