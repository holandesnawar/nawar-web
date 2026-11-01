#!/usr/bin/env python3
"""The girl cut out of her room for the three Black Friday moments, where her room gives way to a backdrop of giant
running type and she stays in front of it:
  bf1 — the hook, «…este Black Friday te interesa» (take g)
  eur — «Entero por un euro» (take p, from the first frame after the take's own cut at 36.7 — her raised finger)
  bf2 — «…ofertas del Black Friday» (take p)
Each one is a range of source frames of the graded take (assets/video/take-X.mp4, 30 fps), cut out with Robust Video
Matting (RVM, ResNet-50, ONNX on CPU), which carries its memory from frame to frame, so the edge does not flicker or
break the way a frame-by-frame model does. Its memory is warmed up on the same shot only: from the take's last own cut
before the range (never across it), and if that leaves too little, on the range played backwards first.
Written to assets/video/cut-<name>.webm (VP9 with alpha), frame for frame the same pictures as the take (its own colours
where she is solid, RVM's foreground colour on the soft edge, so no room colour fringes her hair); gen.py places it on
the take's own timeline (same start, rate and framing).

RVM can keep faint bits of her room at her edge (the carved chair, the beige sofa, the flowers, a band of wall by her
hair, at 20–60 %). refine() never touches what RVM is sure of (alpha ≥ 0.9) and takes out only what IS the empty room:
a plate of the room (per pixel, the median of the take over ±6 s over the frames where RVM says that pixel is room) is
compared with each frame, and wherever she is see-through, a pixel that matches the plate fades out (smoothly, never a
hard notch; averaged over 3 frames where the picture is still, so it cannot flicker nor carry onto a moving hand); and
where the furniture sits (FURNITURE), whatever is faint, still and apart from her solid outline goes. Away from the
furniture the room test only acts where she is mostly see-through, judged over a patch (never strand by strand: the
gaps between hair strands would shimmer). In the gaps between her arms and her body (take p) the red leather chair goes
by its colour, however sure RVM is (leather(): no skin, nail or jeans colour is that red; its near-black shadow only by
her left arm, as her black hair falls by her right one), and her arm blurred over it stays solid. By the vase, a petal RVM counts as her goes when it is pure petal colour and still or in its place
(flower_map()); petal colour in her hair becomes her hair's, and her soft edge there takes her own colour (devase()).
Inside her, nothing else is touched — no colour rules on her (v6.1: the old ones bit her hands and hair). Crumbs left
beside her go.
Writes assets/video/mattes.json. The model (.raw/rvm_resnet50_fp32.onnx, ~100 MB) is downloaded once from the RVM
releases. `python3 tools/mattes.py --clean [names]` re-runs refine() on the saved raw mattes (.matte/<name>-raw.webm).
"""
import json, os, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATTES = {"bf1": ("g", 664, 718), "eur": ("p", 1101, 1152), "bf2": ("p", 1248, 1290)}   # (take, first frame, last frame)
W, H = 1080, 1920
RVM_URL = "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_resnet50_fp32.onnx"
WARM = 60                         # frames run before the range so the model's memory has settled (same shot only)
EDGE = 24                         # px from her outline where room pixels may be taken out
DIFF = (10, 30)                   # max-channel difference to the room plate: below 10 = room (out), above 30 = her (kept)
# where her room's furniture sits beside her (source px x0, x1, y0, y1; the camera never moves): the carved chair arm and
# the beige sofa by her left shoulder, the vase of flowers by her right one. There, RVM's faint leftovers (see refine())
# go: see-through (alpha < 0.75), still (the picture there doesn't change from the frames around) and more than 5 px
# from her solid outline — her hair against her and her moving hands never qualify.
FURNITURE = {k: {"chair": (0, 345, 740, 1000), "sofa": (0, 220, 960, 1250), "vase": (800, 1080, 840, 1250)} for k in "gp"}
FURNITURE["p"].update(leather_l=(0, 330, 1550, 1920), leather_r=(840, 1010, 1760, 1920))   # the red leather chair in the
                                  # gaps between her arms and her body (take p)


def take_frames(take, a, b, fps=None):
    vf = f"select=between(n\\,{a}\\,{b})" if fps is None else f"fps={fps}"
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}"] if fps else []) + \
          ["-i", os.path.join(ROOT, "assets", "video", f"take-{take}.mp4"), "-an", "-vf", vf, "-vsync", "0",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def session():
    import onnxruntime as ort
    model = os.path.join(ROOT, ".raw", "rvm_resnet50_fp32.onnx")
    if not os.path.exists(model):
        subprocess.run(["curl", "-sS", "-L", "--fail", "-o", model, RVM_URL], check=True)
    return ort.InferenceSession(model, providers=["CPUExecutionProvider"])


def run(sess, frames, rec=None):
    """RVM over frames (uint8 N×H×W×3); returns (alphas, fgrs, rec)."""
    rec = rec or [np.zeros((1, 1, 1, 1), np.float32)] * 4; dr = np.array([0.25], np.float32)
    al, fg = [], []
    for fr in frames:
        src = (fr.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        f, p, *rec = sess.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": dr})
        al.append(p[0, 0]); fg.append((f[0].transpose(1, 2, 0) * 255).clip(0, 255).astype(np.uint8))
    return al, fg, rec


def last_cut(frames):
    """index of the first frame after the last cut in frames (0 if none): mean luma difference of the frame pair > 20."""
    small = frames[:, ::8, ::8].astype(np.float32).mean(-1)
    d = np.abs(np.diff(small, axis=0)).mean((1, 2))
    cuts = np.flatnonzero(d > 20)
    return int(cuts[-1] + 1) if len(cuts) else 0


def rvm(sess, take, f0, f1):
    a = max(0, f0 - WARM)
    frames = take_frames(take, a, f1)
    assert len(frames) == f1 - a + 1, (len(frames), f1 - a + 1)
    k0 = f0 - a
    s = last_cut(frames[:k0 + 1])                              # warm up on the same shot only
    rec = None
    if k0 - s < 20:                                            # too short: settle on the range played backwards first
        _, _, rec = run(sess, frames[k0:k0 + 30][::-1])
    al, fg, _ = run(sess, frames[s:], rec)
    al, fg = al[k0 - s:], fg[k0 - s:]
    rng = frames[k0:]
    rgb = np.stack([np.where(x[..., None] > 0.97, f, g) for x, f, g in zip(al, rng, fg)])
    return rgb, np.stack(al).astype(np.float32), (s + a)


def plate(sess, take, f0, f1):
    """the empty room around this clip: per pixel, the median of the take over ±6 s (4 fps) taken only over the frames
    where RVM says that pixel is room (alpha < 0.05) — so the vase and the chair have a plate even though she is next
    to them most of the time; fewer than 4 such frames: no plate (NaN)."""
    a, b = max(0.0, f0 / 30 - 6), f1 / 30 + 6
    fr = take_frames(take, a, b, fps=4)
    _, _, rec = run(sess, [fr[0]] * 4)                         # settle its memory on the first picture
    al, _, _ = run(sess, fr, rec)
    st = fr.astype(np.float32)
    room = np.stack(al) < 0.05
    st[~room] = np.nan
    with np.errstate(invalid="ignore"):
        pl = np.nanmedian(st, axis=0)
    pl[room.sum(0) < 4] = np.nan
    return pl


def flowers(c, loose=False):
    """the vase's red and yellow petals (her skin: R/G ≈ 1.3–1.4, B/G ≈ 0.8, never this; her hair is dark and grey).
    loose: also the petals' darker mixes with her hair."""
    c = c.astype(np.float32); r, g, b = c[..., 0], c[..., 1], c[..., 2]
    if loose:
        return ((r > 1.6 * g) & (r > 1.5 * b) & (r > 35)) | ((b < 0.5 * g) & (g > 60) & (r > 0.8 * g))
    return ((r > 1.8 * g) & (r > 1.6 * b) & (r > 90)) | ((r > 150) & (g > 120) & (b < 0.55 * g))


def leather(c):
    """the dark red leather chair seen between her arms and her body (take p): R/G ≥ 2.3 down to its deepest shadow; her
    skin is R/G ≈ 1.3–1.4 and ≤ 1.95 in shadow, her red nail art is bright — never this. blurred: also its dark brown
    where her moving arm smears over it (R < 75, R/B ≥ 2.2) — her brown hair and her bracelet's dark glints are that
    colour too, so only where RVM is unsure (see refine()). deep: its near-black shadow, down to (4, 0, 1) — her black
    hair is that colour too (7, 2, 2), so only by her left arm, where her hair never reaches."""
    c = c.astype(np.float32); r, g, b = c[..., 0], c[..., 1], c[..., 2]
    red = (r > 2.2 * g) & (r > 2.2 * b) & (r > 12) & (r < 170)
    deep = (r > 2.2 * g) & (r > 2.2 * b) & (r - np.maximum(g, b) >= 3) & (r <= 12)
    return red, red | ((r > 1.5 * g) & (r > 2.2 * b) & (r > 12) & (r < 75)), deep


def flower_map(orig, al, pl, take):
    """where the vase's petals are in this clip (the camera never moves): the plate's petals, and petal colour that stays
    put over 3+ frames where she is not solid — her hands and her nail art move; grown by 10 px, inside the vase box."""
    from scipy import ndimage as ndi
    x0, x1, y0, y1 = FURNITURE[take]["vase"]
    box = np.zeros((H, W), bool); box[y0:y1, x0:x1] = True
    seen = sum((flowers(o, True) & (a < 0.97)).astype(np.int16) for o, a in zip(orig, al))
    pf = flowers(np.nan_to_num(pl).astype(np.uint8)) & ~np.isnan(pl[..., 0])
    return box & ndi.binary_dilation((seen >= 3) | pf, iterations=10)


def refine(orig, al, pl, take, fmap):
    """orig: the take's own frames (what the room test compares with the plate — not RVM's foreground estimate)."""
    from scipy import ndimage as ndi
    n = len(al); fac = np.ones_like(al); force = np.ones_like(al); lift = np.zeros_like(al)
    F = FURNITURE[take]
    def mask(*names):
        m = np.zeros((H, W), bool)
        for k in names:
            if k in F:
                x0, x1, y0, y1 = F[k]; m[y0:y1, x0:x1] = True
        return m
    box, vase, lea, lea_l = mask("chair", "sofa", "vase"), mask("vase"), mask("leather_l", "leather_r"), mask("leather_l")
    luma = [(0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]).astype(np.float32) for f in orig]
    stills = []
    for k in range(n):
        a = al[k]
        still = np.maximum(np.abs(luma[k] - luma[max(0, k - 2)]), np.abs(luma[k] - luma[min(n - 1, k + 2)]))
        still = ndi.uniform_filter(still, 7) < 6; stills.append(still)
        away = ndi.distance_transform_edt(a < 0.9)             # px from her solid core
        faint = box & (a < 0.75) & still
        g = np.clip((away - 5) / 7, 0, 1)                      # 5 px from her: kept … 12 px: gone
        fur = np.where(faint, 1 - g, 1.0)
        with np.errstate(invalid="ignore"):
            diff = np.max(np.abs(orig[k].astype(np.float32) - pl), axis=-1)          # NaN where there is no plate
        t = np.clip((diff - DIFF[0]) / (DIFF[1] - DIFF[0]), 0, 1); t = t * t * (3 - 2 * t)   # smoothstep
        t = ndi.gaussian_filter(np.where(np.isnan(diff), 1.0, t), 2.5)   # judged over a patch, not strand by strand
        cand = np.where(box, a < 0.9, a < 0.5)                 # by the furniture: wherever RVM is unsure; elsewhere only
        cand &= ~vase | still                                  # where she is mostly see-through; by the vase only if still
        fac[k] = np.where(a >= 0.9, 1.0, np.where(cand, t, 1.0) * fur)   # what RVM is sure of is never touched
        if lea.any():                                          # the gaps between her arms and her body: the red leather chair
            red, brown, deep = leather(orig[k])               # (the blurred brown where RVM is unsure, and the near-black
            left = ((brown & (a < 0.95)) | deep) & lea_l       # shadow: only by her left arm, where her hair never reaches;
            red &= lea_l | (orig[k][..., 0] > 30)              # by her right arm, where her dark red-brown hair falls, only
            hide = ndi.binary_closing(ndi.binary_opening(red | left, np.ones((3, 3))), np.ones((7, 7))) & lea   # the lit leather)
            lab, m = ndi.label(hide)                           # (its pale cracks too) goes, however sure RVM is — the patches of
            if m:                                              # it, not a thin reddish shadow along her arm; small holes in it
                sz = ndi.sum(hide, lab, range(1, m + 1)); hide &= ~np.isin(lab, 1 + np.flatnonzero(sz < 300))   # filled
            holes, m = ndi.label(ndi.binary_fill_holes(hide) & ~hide)
            if m:
                sz = ndi.sum(holes > 0, holes, range(1, m + 1)); hide |= np.isin(holes, 1 + np.flatnonzero(sz < 600))
            hide = ndi.gaussian_filter(hide.astype(np.float32), 1.5)   # RVM is; what isn't leather there is her arm, top or jeans,
            force[k] = 1 - hide                                # blurred by the movement: never see-through
            lift[k] = np.where(lea, ndi.gaussian_filter(np.clip((a - 0.4) / 0.25, 0, 1), 1.0) * (1 - hide), 0)
        petal = fmap & flowers(orig[k]) & (still | (diff < 25))   # a petal itself (pure petal colour, still or in its place)
        petal = ndi.binary_opening(petal, np.ones((3, 3)))     # RVM counts as her goes; a strand of hair over it is a mix, not
        force[k] *= 1 - ndi.gaussian_filter(petal.astype(np.float32), 1.0)   # pure petal colour, and stays
    mean3 = (np.concatenate([fac[:1], fac[:-1]]) + fac + np.concatenate([fac[1:], fac[-1:]])) / 3   # over 3 frames: no
    fac = np.where(np.stack(stills), mean3, fac)               # flicker — only where the picture is still (never onto a moving hand)
    fac = np.where(al >= 0.9, 1.0, fac)
    out = []
    for k in range(n):
        f = ndi.gaussian_filter(fac[k], 1.5)
        a = np.maximum(np.where(al[k] >= 0.9, al[k], ndi.gaussian_filter(al[k] * f, 0.5)), lift[k]) * force[k]
        lab, m = ndi.label(a > 0.16)                           # crumbs beside her go
        if m > 1:
            sz = ndi.sum(np.ones_like(a), lab, range(1, m + 1))
            a[np.isin(lab, 1 + np.flatnonzero(sz < 0.02 * sz.max()))] = 0
        out.append(a)
    return out


def devase(rgb, al, orig, take, fmap):
    """by the flower vase, her soft edge takes the colour of her nearest pixel that is not petal-coloured (her own strands
    of hair are soft there: they are their own source); and where the petals are (flower_map()), petal colour in her
    hair becomes her hair's — a smooth blend of the dark pixels around it, never a patchwork of copied ones. Only the
    colour changes, never the shape."""
    from scipy import ndimage as ndi
    x0, x1, y0, y1 = FURNITURE[take]["vase"]
    box = np.zeros((H, W), bool); box[y0:y1, x0:x1] = True
    out = rgb.copy()
    for k, a in enumerate(al):
        tint = flowers(rgb[k], True) | flowers(orig[k], True)
        src = (a >= 0.5) & ~tint
        fix = box & (a > 0.01) & (a < 0.97) & ~tint
        if fix.any() and src.any():
            _, (iy, ix) = ndi.distance_transform_edt(~src, return_indices=True)
            out[k][fix] = rgb[k][iy[fix], ix[fix]]
        dye = box & (a > 0.01) & tint & (fmap | (a < 0.97))
        if dye.any() and src.any():
            c = rgb[k].astype(np.float32)
            w = src * (1 - c.mean(-1) / 255) ** 2              # her hair (dark) leads the blend
            num = np.stack([ndi.gaussian_filter(c[..., j] * w, 8) for j in range(3)], -1)
            den = ndi.gaussian_filter(w, 8)[..., None]
            _, (iy, ix) = ndi.distance_transform_edt(~src, return_indices=True)
            fill = np.where(den > 1e-3, num / np.maximum(den, 1e-6), c[iy, ix])
            out[k][dye] = fill[dye].clip(0, 255).astype(np.uint8)
    return out


def encode(rgb, al, dst):
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "18", "-auto-alt-ref", "0", "-row-mt", "1", dst],
                           stdin=subprocess.PIPE)
    for c, a in zip(rgb, al):
        enc.stdin.write(np.dstack([c, (a * 255).clip(0, 255).astype(np.uint8)]).tobytes())
    enc.stdin.close(); enc.wait(); assert enc.returncode == 0


def decode(webm):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", webm, "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 4)
    return fr[..., :3].copy(), fr[..., 3].astype(np.float32) / 255


def main(only=None, clean_only=False):
    out = {}
    tmp = os.path.join(ROOT, ".matte"); os.makedirs(tmp, exist_ok=True)
    sess = None
    for name, (tk, f0, f1) in MATTES.items():
        dst = os.path.join(ROOT, "assets", "video", f"cut-{name}.webm"); rawf = os.path.join(tmp, f"{name}-raw.webm")
        out[name] = {"take": tk, "f0": f0, "f1": f1, "src": f"assets/video/cut-{name}.webm"}
        if only and name not in only:
            continue
        sess = sess or session()
        if clean_only and os.path.exists(rawf):
            rgb, al = decode(rawf); note = "re-refined"
        else:
            rgb, al, s = rvm(sess, tk, f0, f1); encode(rgb, al, rawf); note = f"RVM from frame {s}"
        orig = take_frames(tk, f0, f1)
        plf = os.path.join(tmp, f"{name}-plate.npy")
        if clean_only and os.path.exists(plf):
            pl = np.load(plf)
        else:
            pl = plate(sess, tk, f0, f1); np.save(plf, pl)
        fmap = flower_map(orig, al, pl, tk)
        ref = refine(orig, al, pl, tk, fmap)
        encode(devase(rgb, ref, orig, tk, fmap), ref, dst)
        print(f"  {name}: take {tk} frames {f0}–{f1} ({note}) → {dst}", flush=True)
    json.dump(out, open(os.path.join(ROOT, "assets", "video", "mattes.json"), "w"), indent=1)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--clean"]
    main(args or None, clean_only="--clean" in sys.argv)
