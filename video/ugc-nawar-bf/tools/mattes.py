#!/usr/bin/env python3
"""The girl cut out of her room for the three Black Friday moments (v5), where her room gives way to a backdrop of
giant running type and she stays in front of it:
  bf1 — the hook, «…este Black Friday te interesa» (take g)
  eur — «Entero por un euro» (take p, the shot after the take's own cut at 36.7, her raised finger)
  bf2 — «…ofertas del Black Friday» (take p)
Each one is a range of source frames of the graded take (assets/video/take-X.mp4, 30 fps), cut out with
`hyperframes remove-background` (local u2net_human_seg) into assets/video/cut-<name>.webm (VP9 with alpha), frame for
frame the same pictures as the take; gen.py places it on the take's own timeline (same start, rate and framing).
The model keeps bits of her room that touch her outline — the carved arm of the chair and the beige sofa behind her
left shoulder, the vase of flowers behind her right one — and leaves the pink mic half transparent; clean() fixes it on
every frame: inside the furniture's boxes, wood, sofa and flower colours come out of the matte where the picture is the
room as usual (her skin, hair and dress are other colours, and her hand passing over moves); in front of her chest,
the mic's pale pink and black fur next to her hand are her; the gap between her arm and her body stays open; crumbs go and
the edge is pulled in 1 px and softened. Writes assets/video/mattes.json. Takes ~0.6 s a frame on CPU.
"""
import json, os, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATTES = {"bf1": ("g", 664, 718), "eur": ("p", 1100, 1152), "bf2": ("p", 1248, 1290)}   # (take, first frame, last frame)


W, H = 1080, 1920
# where her room's furniture sits beside her, per take (source px: x0, x1, y0, y1) — the camera never moves
CHAIR = {"g": (0, 300, 760, 990), "p": (0, 345, 760, 990)}         # the carved chair arm, above her left shoulder (left of her hair)
SOFA = {"g": (0, 200, 960, 1140), "p": (0, 200, 960, 1140)}         # the beige sofa back, beside her left shoulder
SOFA_IN = {"bf1", "eur"}          # where the model kept it (in bf2 her hand rests there: leave it alone)
FLOWERS = {"g": (780, 1080, 840, 1220), "p": (780, 1080, 840, 1240)}  # the vase of flowers, her right
CHEST = (250, 830, 900, 1500)     # in front of her chest (hands, the mic): only she is there


def hsv(rgb):
    r, g, b = [rgb[..., k].astype(np.float32) / 255 for k in range(3)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b); d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, d / (mx + 1e-6), mx


def plate(take, f0, f1):
    """the room as it usually is around this clip: per-pixel median luma of the take over ±6 s, 4 frames a second."""
    a, b = max(0.0, f0 / 30 - 6), f1 / 30 + 6
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i",
                          os.path.join(ROOT, "assets", "video", f"take-{take}.mp4"), "-vf", "fps=4,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.median(np.frombuffer(raw, np.uint8).reshape(-1, H, W), axis=0).astype(np.float32)


def clean(webm, take, f0, f1, name):
    """furniture out, mic in, softer edge (see the module doc). A furniture pixel goes only where the picture there is
    the room as it usually is (luma within 14 of plate()): when her hand or hair passes over the flowers it differs, and
    stays."""
    from scipy import ndimage as ndi
    raw = subprocess.run(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", webm, "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 4).copy()
    luma = lambda f: (0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]).astype(np.float32)
    med = plate(take, f0, f1)
    for f in fr:
        a = f[..., 3].astype(np.float32); h, s, v = hsv(f[..., :3])
        room = np.abs(luma(f) - med) < 14
        skin = (h <= 32) & (s >= 0.24) & (s <= 0.62) & (v > 0.5)
        kill = np.zeros((H, W), bool)
        x0, x1, y0, y1 = CHAIR[take]                                       # wood: s ≥ 0.5, v 0.23–0.51 (her skin v > 0.6, hair v ≈ 0.1)
        wood = (h >= 12) & (h <= 32) & (s > 0.5) & (v > 0.2) & (v < 0.56) & ~skin
        kill[y0:y1, x0:x1] |= wood[y0:y1, x0:x1]                          # colour alone: her hair is darker, her skin lighter
        x0, x1, y0, y1 = SOFA[take] if name in SOFA_IN else (0, 0, 0, 0)
        sofa = (h >= 10) & (h <= 50) & (s < 0.40) & (v > 0.4)            # beige like skin, but paler (her shoulder s ≈ 0.47)
        kill[y0:y1, x0:x1] |= (sofa & (np.abs(luma(f) - med) < 10))[y0:y1, x0:x1]   # and exactly where the room always is
        x0, x1, y0, y1 = FLOWERS[take]
        flow = ((s > 0.62) & (v > 0.4) & ~((h >= 195) & (h <= 245)) & ~((h >= 290) | (h <= 6))) \
               | ((h >= 34) & (h <= 72) & (s > 0.4) & (v > 0.5)) | ((h >= 60) & (h <= 170) & (s > 0.16) & (v > 0.18)) \
               | (((h <= 6) | (h >= 352)) & (s > 0.62) & (v > 0.38))         # (bright petals: her dark hair, v < 0.35, never)
        # (orange, yellow, green stems, deep red — never her pink nails or the pink mic, h 300–350)
        kill[y0:y1, x0:x1] |= (flow & ~skin & room)[y0:y1, x0:x1]
        kill = ndi.binary_closing(kill, iterations=2)
        lab, n = ndi.label(kill)                                       # specks (a warm glint in her hair) are not furniture
        if n:
            sz = ndi.sum(np.ones(kill.shape), lab, range(1, n + 1))
            kill = np.isin(lab, 1 + np.flatnonzero(sz >= 120))
        kill = ndi.binary_dilation(kill, iterations=3)
        a[kill] = 0
        body = a > 40
        mic = (((h >= 290) | (h <= 25)) & (s >= 0.06) & (v > 0.55)) | (v < 0.2)      # pale pink body, black fur (the wall is grey-olive)
        x0, x1, y0, y1 = CHEST                                  # the mic: every pink/black patch in front of her chest that
        m = ndi.binary_closing(mic[y0:y1, x0:x1] & ~kill[y0:y1, x0:x1], iterations=2)   # touches her (hand, fingers) is her
        lab, n = ndi.label(m)
        if n:
            touch = np.unique(lab[ndi.binary_dilation(body[y0:y1, x0:x1], iterations=4) & (lab > 0)])
            add = ndi.binary_fill_holes(np.isin(lab, touch[touch > 0]))
            a[y0:y1, x0:x1] = np.maximum(a[y0:y1, x0:x1], add * 255.0)
        lab, n = ndi.label(a > 40)                                                                       # crumbs left beside her:
        if n > 1:                                                                                        # only big pieces stay
            sizes = ndi.sum(np.ones_like(a), lab, range(1, n + 1))
            a[np.isin(lab, 1 + np.flatnonzero(sizes < 0.02 * sizes.max()))] = 0
        a = ndi.gaussian_filter(ndi.grey_erosion(a, size=3), 1.0)                                        # a softer, cleaner edge
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
                subprocess.run(["cp", raw, dst], check=True); clean(dst, tk, f0, f1, name); print(f"  {name}: cleaned", flush=True)
            continue
        src = os.path.join(tmp, f"{name}-src.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, "assets", "video", f"take-{tk}.mp4"), "-an",
                        "-vf", f"select=between(n\\,{f0}\\,{f1}),setpts=N/30/TB", "-r", "30", "-c:v", "libx264", "-crf", "12",
                        "-pix_fmt", "yuv420p", src], check=True)
        subprocess.run(["npx", "--yes", "hyperframes@0.8.139", "remove-background", src, "-o", dst, "--quality", "best"],
                       check=True, cwd="/tmp", stdout=subprocess.DEVNULL)
        subprocess.run(["cp", dst, os.path.join(tmp, f"{name}-raw.webm")], check=True); clean(dst, tk, f0, f1, name)
        print(f"  {name}: take {tk} frames {f0}–{f1} → {dst}", flush=True)
    json.dump(out, open(os.path.join(ROOT, "assets", "video", "mattes.json"), "w"), indent=1)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--clean"]
    main(args or None, clean_only="--clean" in sys.argv)
