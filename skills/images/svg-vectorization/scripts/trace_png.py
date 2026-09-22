#!/usr/bin/env python3
"""Vectorize a transparent-background PNG into a two-layer SVG
(gradient silhouette + accent mask with its own gradient).

Method (the same used for the Sufficit icon):
  1. Silhouette mask = alpha>128; accent mask = pixels matching
     --accent-expr (default: red, r>g+40 and r>b+40).
  2. Contours via crack-following (right-hand rule, FG on the right),
     enumerating ALL loops (outlines and holes); fill-rule="evenodd".
  3. RDP simplification with corner detection; Catmull-Rom smoothing
     converted to cubic curves (C).
  4. Per-channel linear gradient least-squares fitted over the real pixels
     of each mask (sweeps 0..180 deg and keeps the best fit).
  5. Output: silhouette path + accent path with userSpaceOnUse gradients,
     viewBox = silhouette bbox (origin at 0,0).

Usage:
  python3 trace_png.py input.png output.svg [--accent-expr "r>g+40 and r>b+40"]
      [--eps 2.2] [--min-area 6] [--top 0] [--corner 40]

--top N: keep only the N largest accent loops (drops anti-aliasing speckles).
Use --top 0 to keep all of them.

Dependencies: Pillow.
"""
import argparse
import math
from PIL import Image

ACCENT_EVAL = {
    'r': lambda p: p[0], 'g': lambda p: p[1], 'b': lambda p: p[2], 'a': lambda p: p[3],
}


def accent_match(p, expr):
    try:
        return bool(eval(expr, {'__builtins__': {}},
                         {k: fn(p) for k, fn in ACCENT_EVAL.items()}))
    except Exception:
        return False


def load_masks(path, expr, alpha_thr=128):
    im = Image.open(path).convert('RGBA')
    W, H = im.size
    P = im.load()
    sil = [[P[x, y][3] > alpha_thr for x in range(W)] for y in range(H)]
    acc = [[P[x, y][3] > alpha_thr and accent_match(P[x, y], expr)
            for x in range(W)] for y in range(H)]
    return im, W, H, sil, acc


def bbox_of(mask, W, H):
    xs = [x for y in range(H) for x in range(W) if mask[y][x]]
    ys = [y for y in range(H) for x in range(W) if mask[y][x]]
    if not xs:
        return 0, 0, W - 1, H - 1
    return min(xs), min(ys), max(xs), max(ys)


DIRS = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}
TURN_R = {'up': 'right', 'right': 'down', 'down': 'left', 'left': 'up'}
TURN_L = {'up': 'left', 'left': 'down', 'down': 'right', 'right': 'up'}
REVERSE = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}


def trace_all_loops(fg, W, H):
    """All contours (outer loops and holes) via crack-following."""
    used = set()
    loops = []
    for y in range(H):
        row = fg[y]
        for x in range(W):
            if not row[x]:
                continue
            if (0 < x < W - 1 and 0 < y < H - 1
                    and row[x - 1] and row[x + 1] and fg[y - 1][x] and fg[y + 1][x]):
                continue  # interior pixel, no border
            for d, c in (('right', (x, y)), ('up', (x, y + 1)),
                         ('left', (x + 1, y + 1)), ('down', (x + 1, y))):
                if (c, d) in used:
                    continue
                if not edge_ok(fg, W, H, c[0], c[1], d):
                    continue
                corner, dr = c, d
                pts = []
                while True:
                    used.add((corner, dr))
                    pts.append(corner)
                    dx, dy = DIRS[dr]
                    corner = (corner[0] + dx, corner[1] + dy)
                    for cand in (TURN_R[dr], dr, TURN_L[dr], REVERSE[dr]):
                        if ((corner, cand) not in used
                                and edge_ok(fg, W, H, corner[0], corner[1], cand)):
                            dr = cand
                            break
                    else:
                        break
                    if corner == c and dr == d:
                        break
                if len(pts) >= 8:
                    loops.append(pts)
    return loops


def edge_ok(fg, W, H, x, y, nd):
    if nd == 'up':
        r_, l_ = (x, y - 1), (x - 1, y - 1)
    elif nd == 'down':
        r_, l_ = (x - 1, y), (x, y)
    elif nd == 'right':
        r_, l_ = (x, y), (x, y - 1)
    else:
        r_, l_ = (x - 1, y - 1), (x - 1, y)

    def F(a, b):
        return 0 <= a < W and 0 <= b < H and fg[b][a]

    return F(*r_) and not F(*l_)


def area(poly):
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s / 2


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        ax, ay = pts[i]
        bx, by = pts[j]
        best, bd = -1, -1.0
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy or 1.0
        for k in range(i + 1, j):
            px_, py_ = pts[k]
            t = max(0.0, min(1.0, ((px_ - ax) * dx + (py_ - ay) * dy) / L2))
            d2 = (px_ - ax - t * dx) ** 2 + (py_ - ay - t * dy) ** 2
            if d2 > bd:
                best, bd = k, d2
        if bd > eps * eps:
            keep[best] = True
            stack += [(i, best), (best, j)]
    return [p for p, k in zip(pts, keep) if k]


def rotate_to_extreme(poly):
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    k = max(range(len(poly)), key=lambda i: (poly[i][0] - cx) ** 2 + (poly[i][1] - cy) ** 2)
    return poly[k:] + poly[:k]


def corners(poly, thr=40.0):
    n = len(poly)
    out = [False] * n
    for i in range(n):
        ax, ay = poly[(i - 1) % n]
        bx, by = poly[i]
        cx, cy = poly[(i + 1) % n]
        v1 = (bx - ax, by - ay)
        v2 = (cx - bx, cy - by)
        m1 = math.hypot(*v1) or 1
        m2 = math.hypot(*v2) or 1
        cos = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (m1 * m2)))
        if math.degrees(math.acos(cos)) > thr:
            out[i] = True
    return out


def smooth_path(poly, iscorner, tx, ty, tension=1.0):
    n = len(poly)

    def P(i):
        return (poly[i % n][0] - tx, poly[i % n][1] - ty)

    def tangent(i):
        if iscorner[i % n]:
            return (0.0, 0.0)
        p0, p2 = P(i - 1), P(i + 1)
        return ((p2[0] - p0[0]) / 6.0 * tension, (p2[1] - p0[1]) / 6.0 * tension)

    d = [f'M {P(0)[0]:.1f} {P(0)[1]:.1f}']
    for i in range(n):
        a, b = P(i), P(i + 1)
        ta, tb = tangent(i), tangent(i + 1)
        c1 = (a[0] + ta[0], a[1] + ta[1])
        c2 = (b[0] - tb[0], b[1] - tb[1])
        d.append(f'C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {b[0]:.1f} {b[1]:.1f}')
    return ' '.join(d) + ' Z'


def fit_gradient(P, W, H, mask, exclude=None, step=3):
    """Least-squares RGB linear gradient; sweeps angles 0..180 deg."""
    pts = []
    for y in range(0, H, step):
        for x in range(0, W, step):
            p = P[x, y]
            if p[3] <= 128 or not mask[y][x]:
                continue
            if exclude and exclude(p):
                continue
            pts.append((x, y, p[0], p[1], p[2]))
    if not pts:
        return None
    best = None
    for deg in range(0, 180, 2):
        th = math.radians(deg)
        ux, uy = math.cos(th), math.sin(th)
        ts = [x * ux + y * uy for x, y, *_ in pts]
        tmin, tmax = min(ts), max(ts)
        sse = 0.0
        fits = []
        ok = True
        for ci in (2, 3, 4):
            vs = [pt[ci] for pt in pts]
            n = len(vs)
            st, sv = sum(ts), sum(vs)
            stt = sum(t * t for t in ts)
            stv = sum(t * v for t, v in zip(ts, vs))
            den = n * stt - st * st
            if abs(den) < 1e-9:
                ok = False
                break
            b_ = (n * stv - st * sv) / den
            a_ = (sv - b_ * st) / n
            sse += sum((a_ + b_ * t - v) ** 2 for t, v in zip(ts, vs))
            fits.append((a_, b_))
        if ok and (best is None or sse < best[0]):
            best = (sse, th, tmin, tmax, fits)
    return best


def hx(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)


def main():
    ap = argparse.ArgumentParser(description='Vectorize a (alpha) PNG into a 2-layer SVG.')
    ap.add_argument('png')
    ap.add_argument('svg')
    ap.add_argument('--accent-expr', default='r>g+40 and r>b+40',
                    help='expression for the accent mask (default: red)')
    ap.add_argument('--eps', type=float, default=2.2, help='RDP tolerance in px')
    ap.add_argument('--min-area', type=float, default=6.0)
    ap.add_argument('--top', type=int, default=0,
                    help='keep only the N largest accent loops (0 = all)')
    ap.add_argument('--corner', type=float, default=40.0)
    args = ap.parse_args()

    im, W, H, sil, acc = load_masks(args.png, args.accent_expr)
    P = im.load()
    bx0, by0, bx1, by1 = bbox_of(sil, W, H)
    VW, VH = bx1 - bx0 + 1, by1 - by0 + 1
    print(f'[bbox] ({bx0},{by0})-({bx1},{by1}) viewBox 0 0 {VW} {VH}')

    sil_loops = [L for L in trace_all_loops(sil, W, H) if abs(area(L)) >= args.min_area]
    acc_all = [L for L in trace_all_loops(acc, W, H) if abs(area(L)) >= args.min_area]
    if args.top and args.top > 0:
        acc_all.sort(key=lambda L: abs(area(L)), reverse=True)
        acc_loops = acc_all[:args.top]
    else:
        acc_loops = acc_all
    print(f'[loops] silhouette={len(sil_loops)} accent={len(acc_loops)} '
          f'(raw {len(acc_all)}, areas={[round(abs(area(L))) for L in acc_loops]})')

    def build(loops):
        polys = [rdp(rotate_to_extreme(L), args.eps) for L in loops]
        parts = [smooth_path(p, corners(p, args.corner), bx0, by0) for p in polys if len(p) >= 3]
        return ' '.join(parts), polys

    sil_d, sil_poly = build(sil_loops)
    acc_d, acc_poly = build(acc_loops)
    print(f'[rdp] vertices silhouette={sum(len(p) for p in sil_poly)} '
          f'accent={sum(len(p) for p in acc_poly)}')

    g_fit = fit_gradient(P, W, H, sil,
                         exclude=lambda p: accent_match(p, args.accent_expr))
    a_fit = fit_gradient(P, W, H, acc)

    def stops(fit, name):
        sse, th, tmin, tmax, fits = fit
        ux, uy = math.cos(th), math.sin(th)
        x1, y1 = ux * tmin - bx0, uy * tmin - by0
        x2, y2 = ux * tmax - bx0, uy * tmax - by0
        c_lo = tuple(max(0, min(255, round(a_ + b_ * tmin))) for a_, b_ in fits)
        c_hi = tuple(max(0, min(255, round(a_ + b_ * tmax))) for a_, b_ in fits)
        return (f'<linearGradient id="{name}" gradientUnits="userSpaceOnUse" '
                f'x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}">\n'
                f'      <stop offset="0" stop-color="{hx(c_lo)}"/>\n'
                f'      <stop offset="1" stop-color="{hx(c_hi)}"/>\n    </linearGradient>'), \
               hx(c_lo), hx(c_hi), math.degrees(th)

    g_grad, g_lo, g_hi, g_deg = stops(g_fit, 'base-gradient')
    a_grad, a_lo, a_hi, a_deg = stops(a_fit, 'accent-gradient')
    print(f'[base gradient]   {g_lo} -> {g_hi} @ {g_deg:.0f}°')
    print(f'[accent gradient] {a_lo} -> {a_hi} @ {a_deg:.0f}°')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" fill="none">\n'
           f'  <defs>\n    {g_grad}\n    {a_grad}\n  </defs>\n'
           f'  <path fill-rule="evenodd" fill="url(#base-gradient)" d="{sil_d}"/>\n'
           f'  <path fill-rule="evenodd" fill="url(#accent-gradient)" d="{acc_d}"/>\n'
           f'</svg>\n')
    open(args.svg, 'w').write(svg)
    print(f'[svg] {args.svg} ({len(svg)} bytes)')


if __name__ == '__main__':
    main()
