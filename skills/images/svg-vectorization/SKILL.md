---
name: svg-vectorization
description: Vectorizes transparent-background PNG icons and logos into faithful two-layer SVGs (gradient silhouette + brand accent), traced from real pixels and validated by IoU against the original image before deployment. Use to convert a PNG to SVG, recreate a brand icon from references, or audit a generated SVG. Do not use for photos, art with complex photographic gradients, or images without well-defined contours.
metadata:
  version: "1.0.0"
---

# PNG-to-SVG vectorization

Convert a transparent-background PNG into a faithful vector SVG without
drawing "from memory": the tracing comes from the real pixels of the reference
and fidelity is **measured** (IoU) against the original image — never assumed.

This skill was born from a real case: the Sufficit icon used in a product was
an invented SVG (a gray square with a red swoosh) that had nothing to do with
the brand. With the correct references in hand, the method below recreated
the real icon (gradient gray swirl + red glyph) with IoU 0.98 and validated it
in the browser's real engine before deployment.

## When to use (and when not)

**Use** when you have: a transparent-background PNG of a logo/icon; one or
more references (screenshots work, with the care described in step 1); and a
need for an editable, scalable, faithful SVG.

**Do not use** for: photos, textures, complex photographic gradients (the
2-layer + linear-gradient model does not represent them), or art without
well-defined contours. In those cases an optimized PNG/WebP is the honest
answer.

## Principles

1. **See before tracing.** Without direct vision of the PNG, generate ASCII
   maps and palettes; describe the structure before any vectorization
   command.
2. **Trace from pixels, not from memory.** Contours come from an algorithm
   (crack-following); colors come from a least-squares fit over the real
   pixels.
3. **Validate the file, not the intention.** IoU is measured on the SVG **on
   disk** (independent parse) and, ideally, rendered by the browser's real
   engine. Never trust only the tracer's in-memory shapes.
4. **Always compare against the original.** Side-by-side panel (reference ×
   render) + a number. Both together; neither alone.

## Workflow

Prerequisites: `python3`, Pillow, numpy; `google-chrome` (or chromium)
optional but recommended for independent validation. The scripts live in
`scripts/` in this skill.

### 1. See the reference

```bash
python3 scripts/analyze_png.py reference.png --cols 64
```

Output: dimensions, alpha bbox, dominant colors, quantized palette with an
ASCII region map, and — if an accent exists (default: red) — the isolated
accent mask. Read the map and answer before proceeding:

- How many shapes/fronts does the silhouette have? Are there holes/parallel
  arms?
- Is the accent (brand color) one continuous inner shape or does it shatter?
- Does the palette suggest a gradient (smooth variation) or flat colors?
- If the reference is a screenshot with an opaque background: which component
  is the icon and which is page noise? (In the real case, a red layout bar
  was 2× larger than the glyph — it was isolated by connected components,
  discarding whatever touched the border.)

### 2. Trace

```bash
python3 scripts/trace_png.py reference.png output.svg --top 2
```

What the tracer does: silhouette mask (alpha>128) and accent mask
(`--accent-expr`, red by default); **all** contours via crack-following
(outlines and holes, with `fill-rule="evenodd"`); RDP simplification with
corner preservation; Catmull-Rom smoothing converted to cubic curves; and one
linear gradient per layer, least-squares fitted by sweeping 0–180° over the
real pixels.

Parameters that matter:

- `--top N` — keep only the N largest accent loops. Rendered icons carry
  anti-aliasing speckles (real case: 12 loops, 10 were noise of 6–1052 px²).
  `--top 2` is the typical starting point (outline + hole).
- `--eps` (default 2.2) — RDP tolerance; raise it if the contour comes out
  jagged, lower it if it loses detail.
- `--accent-expr` — e.g. `"r>g+40 and r>b+40"` for red; adapt it to the brand
  color (the expression is evaluated with r, g, b, a).

### 3. Validate the file on disk

```bash
python3 scripts/verify_svg.py output.svg reference.png --chrome --panel panel.png
```

Measures per-layer IoU (base and accent) between the rasterization of the
**file** and the bbox-normalized reference, on two routes: own parse (flattened
Béziers) and headless Chrome (the real engine of the SVG consumer). Verdict:
**PASS ≥ 0.96 · WARN ≥ 0.90 · FAIL < 0.90** (the script exits with code 1 on
FAIL). The panel renders the visual side-by-side comparison.

If it fails: lower `--eps`, adjust `--top`/`--min-area`, and check the step-1
map again. **A suddenly very low IoU (e.g. 0.4) is usually a verifier
alignment bug** (duplicated bbox offset, wrong canvas), not a bad SVG —
before touching the trace, reconcile via two routes (exactly what `--chrome`
provides).

### 4. Deploy at the target size

If the product expects a standard viewBox (e.g. 512×512), wrap the paths in a
group and re-validate after the transform:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="none">
  <defs><!-- userSpaceOnUse gradients: original coordinates remain valid --></defs>
  <g transform="translate(0 TY) scale(S)">
    <!-- original paths, untouched -->
  </g>
</svg>
```

with `S = 512/original_width` and `TY = (512 − original_height·S)/2`. Run
`verify_svg.py` again against the transformed file. Finally, confirm in the
real consumer (e.g. the asset import in the app) and leave the commit to
whoever maintains the repository.

## Real case (numbers)

Sufficit icon, 1254×1254 reference with transparency:

- analysis: gradient-gray silhouette (#BBBABC→#616062), gradient-red accent
  (#DA2A2C→#C20E13), ~17% of pixels visible;
- trace: 6 silhouette loops + 2 accent loops (10 speckles discarded via
  top-2), gradients fitted at 88° and 108°;
- validation: file-vs-reference IoU 0.983 (base) / 0.969 (accent); after the
  512 transform: 0.973 / 0.961; in headless Chrome: 0.971 / 0.967.

## Known pitfalls

- **A verifier can be wrong too.** In the real case, a typo in the Bézier
  formula (`3·mt·tt²` instead of `3·mt²·t` for control point 1) made a
  verifier report IoU 0.46 for a file that was actually 0.98. Always validate
  through two independent routes before condemning the SVG.
- **`magick svg:` is not fit for validation.** ImageMagick treats SVG as MSVG
  and rendered the file as **empty**. Use headless Chrome/chromium as the
  independent engine.
- **Misalignment looks like a shape error.** IoU ~0.3–0.5 with a small pixel
  error is often a duplicated offset (bbox added twice) or a comparison
  canvas in another coordinate space.
- **Anti-aliasing speckles.** Renders carry isolated dots of the accent
  color; without `--top`, each one becomes a `<path>` (and pollutes the
  file).
- **Screenshot ≠ canonical source.** When more than one reference exists,
  compare the glyphs to each other (connected components + normalized IoU)
  and pick the highest-resolution one with a transparent background; record
  the choice.

## Final checklist

1. ASCII map read and structure described in words.
2. SVG generated from pixels (not hand-drawn), speckles filtered.
3. `verify_svg.py` PASSing (≥ 0.96) — file on disk, two routes.
4. Visual panel checked against the original (light and dark backgrounds).
5. Target-viewBox transform re-validated.
6. Asset in place at the consumer; commit left to the maintainer.
