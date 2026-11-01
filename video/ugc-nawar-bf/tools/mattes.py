#!/usr/bin/env python3
"""The girl cut out of her room for the three Black Friday moments (v5), where her room gives way to a backdrop of
giant running type and she stays in front of it:
  bf1 — the hook, «…este Black Friday te interesa» (take g)
  eur — «Entero por un euro» (take p, the shot after the take's own cut at 36.7, her raised finger)
  bf2 — «…ofertas del Black Friday» (take p)
Each one is a range of source frames of the graded take (assets/video/take-X.mp4, 30 fps), cut out with
`hyperframes remove-background` (local u2net_human_seg) into assets/video/cut-<name>.webm (VP9 with alpha), frame for
frame the same pictures as the take; gen.py places it on the take's own timeline (same start, rate and framing).
The model keeps two bits of her room that touch her outline — the carved arm of the chair behind her left shoulder
and the flowers behind her right one — and leaves the pink mic half transparent; clean() fixes both on every frame:
inside two small boxes beside her shoulders, the chair's brown wood and the flowers' yellow and red come out of the matte
(her skin, hair and dress are other colours); holes inside her silhouette are filled, and in front of her chest anything
next to her that isn't wall is her (the mic) — the gap of an «OK» sign, which shows the wall, stays open. Writes assets/video/mattes.json. Takes ~0.6 s a frame on CPU.
"""
import json, os, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATTES = {"bf1": ("g", 664, 718), "eur": ("p", 1101, 1152), "bf2": ("p", 1248, 1290)}   # (take, first frame, last frame)


W, H = 1080, 1920
CHAIR = (0, 400, 740, 1020)       # x0, x1, y0, y1 (source px) — beside her left shoulder
FLOWERS = (840, 1080, 860, 1110)  # beside her right shoulder
CHEST = (250, 830, 900, 1500)     # in front of her chest (hands, the mic): only she is there


def hsv(rgb):
    r, g, b = [rgb[..., k].astype(np.float32) / 255 for k in range(3)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b); d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, d / (mx + 1e-6), mx


def clean(webm):
    from scipy import ndimage as ndi
    raw = subprocess.run(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", webm, "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 4).copy()
    for f in fr:
        a = f[..., 3].astype(np.float32); h, s, v = hsv(f[..., :3])
        kill = np.zeros((H, W), bool)
        x0, x1, y0, y1 = CHAIR
        kill[y0:y1, x0:x1] |= ((h >= 8) & (h <= 42) & (s > 0.45) & (v > 0.26) & (v < 0.66))[y0:y1, x0:x1]   # brown wood (not her darker hair)
        x0, x1, y0, y1 = FLOWERS
        kill[y0:y1, x0:x1] |= (((h >= 36) & (h <= 72) & (s > 0.45) & (v > 0.45))                        # yellow flowers
                               | (((h <= 8) | (h >= 340)) & (s > 0.6) & (v > 0.35)))[y0:y1, x0:x1]     # and the red ones
        kill = ndi.binary_dilation(ndi.binary_closing(kill, iterations=3), iterations=4)
        a[kill] = 0
        body = a > 40
        filled = ndi.binary_fill_holes(body)
        wall = (s < 0.16) & (v > 0.28) & (v < 0.72)
        hole = ndi.binary_erosion(filled, iterations=5) & ~body & ~wall
        hole = ndi.binary_dilation(hole, iterations=3) & filled
        a = np.maximum(a, hole * 255.0)
        x0, x1, y0, y1 = CHEST                                                                           # her hands and the mic: whatever
        near = ndi.binary_dilation(body, iterations=25)[y0:y1, x0:x1] & ~wall[y0:y1, x0:x1] & ~kill[y0:y1, x0:x1]   # isn't wall
        a[y0:y1, x0:x1] = np.maximum(a[y0:y1, x0:x1], near * 255.0)                                       # next to her is her
        lab, n = ndi.label(a > 40)                                                                       # crumbs of carving left beside
        if n > 1:                                                                                        # her: only big pieces stay
            sizes = ndi.sum(np.ones_like(a), lab, range(1, n + 1))
            a[np.isin(lab, 1 + np.flatnonzero(sizes < 0.02 * sizes.max()))] = 0
        a = ndi.gaussian_filter(a, 0.8)                                                                  # soften the new edges a touch
        f[..., 3] = np.clip(a, 0, 255).astype(np.uint8)
    tmp = webm + ".clean.webm"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                          "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "18", "-auto-alt-ref", "0", "-row-mt", "1", tmp],
                         stdin=subprocess.PIPE)
    p.communicate(fr.tobytes()); assert p.returncode == 0
    os.replace(tmp, webm)


def main(only=None, clean_only=False):
    out = {}
    tmp = os.path.join(ROOT, ".matte"); os.makedirs(tmp, exist_ok=True)
    for name, (tk, f0, f1) in MATTES.items():
        dst = os.path.join(ROOT, "assets", "video", f"cut-{name}.webm")
        out[name] = {"take": tk, "f0": f0, "f1": f1, "src": f"assets/video/cut-{name}.webm"}
        if (only and name not in only and os.path.exists(dst)) or clean_only:
            if clean_only and (not only or name in only):
                raw = os.path.join(tmp, f"{name}-raw.webm")
                if not os.path.exists(raw):
                    subprocess.run(["cp", dst, raw], check=True)
                subprocess.run(["cp", raw, dst], check=True); clean(dst); print(f"  {name}: cleaned", flush=True)
            continue
        src = os.path.join(tmp, f"{name}-src.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, "assets", "video", f"take-{tk}.mp4"), "-an",
                        "-vf", f"select=between(n\\,{f0}\\,{f1}),setpts=N/30/TB", "-r", "30", "-c:v", "libx264", "-crf", "12",
                        "-pix_fmt", "yuv420p", src], check=True)
        subprocess.run(["npx", "--yes", "hyperframes@0.8.139", "remove-background", src, "-o", dst, "--quality", "best"],
                       check=True, cwd="/tmp", stdout=subprocess.DEVNULL)
        subprocess.run(["cp", dst, os.path.join(tmp, f"{name}-raw.webm")], check=True); clean(dst)
        print(f"  {name}: take {tk} frames {f0}–{f1} → {dst}", flush=True)
    json.dump(out, open(os.path.join(ROOT, "assets", "video", "mattes.json"), "w"), indent=1)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--clean"]
    main(args or None, clean_only="--clean" in sys.argv)
