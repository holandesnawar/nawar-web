#!/usr/bin/env python3
"""The picture and sound of the reel: the ad from source frame 135 (Suárez walking in — the brand intro before it is
cut) to frame 993 (the last frame before the brand end card), held 8 frames under the end of «…genoeg», cropped to
9:16 out of the ×4 upscale (.raw/up.mp4, tools/upscale.py) and written to assets/video/suarez-916.mp4 (1080×1920,
25 fps, the ad's own sound from 5.40 s to 40.08 s, before the brand voice-over, at −14 LUFS).
Each shot has its own 9:16 window (SHOTS: the centre in source px — 512 wide —, keyframed where the camera or the
speaker moves; a window is 162 source px wide), on whoever talks. What still shows of the brand inside a window is
taken out (LOGOS): the red business card's print and the red star on the white one.
  python3 tools/frame.py          (python3 tools/frame.py --mux: only the sound, the grade and the mux)
"""
import json, os, subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP0, F0, F1, HOLD = 123, 135, 993, 8        # up.mp4 starts at source frame 123; the reel plays 135–993, then holds
S = 4                                       # upscale factor (512×288 → 2048×1152)
WIN = 162                                   # 9:16 window width in source px (288 × 9/16)
CUTS = [123, 148, 172, 193, 302, 334, 375, 471, 495, 551, 648, 690, 740, 772, 786, 830, 866, 892, 928, 945, 960, 994]
# shot (first frame) → [(source frame, window centre x in source px)]; one smooth monotone curve through the keys
SHOTS = {      # (set from a face detector run on every 3rd frame, checked by eye on native-scale frames, re-keyed after QA)
    123: [(135, 272), (147, 212)],              # Suárez walks in (the reel opens here) — followed as he walks
    148: [(148, 330), (160, 318), (171, 300)],  # over his shoulder: the assistant, «een sportman van Ajax»
    172: [(172, 238)],                          # the Ajax badge, whole
    193: [(193, 245), (210, 296), (222, 308), (301, 308)],   # the assistant: «Ja, beroemde club. Cruijff…»
    302: [(302, 168), (333, 198)],              # Suárez, wide: «Ja, ik hoorde iets…»
    334: [(334, 215), (356, 205), (374, 255)],  # Suárez close: «…antifluitregeling» (on his mouth)
    375: [(375, 280), (400, 305), (412, 265), (424, 235), (437, 285), (470, 305)],   # the assistant bends for the hearing aid
    471: [(471, 250)],                          # the hearing aid and the thumb holding it
    495: [(495, 320), (507, 302), (550, 302)],  # the assistant close: «…fluittonen hoort»
    551: [(551, 205), (600, 290), (612, 335), (628, 340), (636, 290), (647, 245)],   # Suárez close, his head turn
    648: [(648, 290), (670, 315), (680, 230), (689, 160)],   # the assistant close, bending forward: «Oh, maar dan…»
    690: [(690, 395), (710, 372), (739, 372)],  # wide, on the assistant as he talks: «…oordopjesgamma»
    740: [(740, 350), (771, 290)],              # the sofa and his gesturing hand: «…op de bank plaats»
    772: [(772, 212), (785, 200)],              # Suárez: «Hè?»
    786: [(786, 245), (800, 205), (812, 250), (820, 280), (829, 298)],   # Suárez close: «Suárez nooit zitten…»
    830: [(830, 165), (865, 175)],              # after a dip to black: his hand with the earplugs
    866: [(866, 185), (891, 215)],              # wide on Suárez: «Nou, veel succes ermee»
    892: [(892, 305), (927, 309)],              # the assistant: «En mocht u nog een fluitje horen…»
    928: [(928, 158), (944, 232)],              # Suárez
    945: [(945, 282)],                          # the assistant holds up a red business card: «Kaartje?»
    960: [(960, 180), (978, 155), (993, 180)],  # Suárez: «Nee, nee, ik heb kaartjes genoeg»
}
# brand marks inside the windows: (first frame, last frame, kind, source rect x0, y0, x1, y1)
LOGOS = [(945, 959, "red_card", 150, 20, 240, 140),     # the assistant's red business card (the shop's logo printed light)
         (960, 974, "white_card", 215, 35, 300, 110),    # the white card with the shop's red star (out of the window from 975:
                                                         # after that the rect holds only his red shoulder — never touched)
         (148, 171, "wall", 385, 40, 512, 140),          # «De hoorspecialist» on the orange wall, where a window reaches it
         (193, 301, "wall", 385, 40, 512, 140),
         (375, 470, "wall", 385, 40, 512, 140),
         (892, 927, "wall", 385, 40, 512, 140),
         (945, 959, "wall", 385, 40, 512, 140)]


def centre(n):
    from scipy.interpolate import PchipInterpolator
    s = max(c for c in CUTS if c <= n)
    ks = SHOTS[s]
    if len(ks) == 1 or n <= ks[0][0]:
        c = ks[0][1]
    elif n >= ks[-1][0]:
        c = ks[-1][1]
    else:
        c = float(PchipInterpolator([k[0] for k in ks], [k[1] for k in ks])(n))
    return min(max(c, WIN / 2), 512 - WIN / 2)


def wall(img, rect):
    """the shop's slogan in light letters on the out-of-focus orange wall. The letters are found at the source's own
    scale (the rect shrunk ×4: there they are thin strokes, lighter than the wall around them) and painted over, in the
    upscale, with the wall around them (a masked blur), plus the frame's grain."""
    from scipy import ndimage as ndi
    x0, y0, x1, y1 = [v * S for v in rect]
    sub = img[y0:y1, x0:x1].astype(np.float32)
    h, w = sub.shape[0] // S, sub.shape[1] // S
    sm = sub[:h * S, :w * S].reshape(h, S, w, S, 3).mean((1, 3))
    r, g, b = sm[..., 0], sm[..., 1], sm[..., 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    wallish = ndi.gaussian_filter(((r > 140) & (r > 1.25 * g) & (g > 1.2 * b)).astype(np.float32), 4) > 0.45
    text = wallish & (luma - ndi.median_filter(luma, 15) > 9)
    text = ndi.binary_opening(text, iterations=1)
    rows, cols = np.flatnonzero(text.sum(1) >= 2), np.flatnonzero(text.sum(0) >= 1)
    if not len(rows):
        return img
    band = np.zeros_like(text)                          # the whole line of lettering: its rows (± 3 px), from its first
    band[max(0, rows.min() - 3):rows.max() + 4, max(0, cols.min() - 3):] = True   # letter on, wherever there is wall
    text = band & ndi.binary_dilation(wallish, iterations=1)
    big = np.zeros(sub.shape[:2], bool); big[:h * S, :w * S] = np.kron(text, np.ones((S, S), bool))
    big = ndi.binary_dilation(big, iterations=5)
    keep = np.zeros(sub.shape[:2], bool); keep[:h * S, :w * S] = np.kron(wallish, np.ones((S, S), bool))
    keep &= ~big
    kf = keep.astype(np.float32)
    if kf.sum() < 500:
        return img
    def mblur(sig):
        num = np.stack([ndi.gaussian_filter(sub[..., c] * kf, sig) for c in range(3)], -1)
        den = ndi.gaussian_filter(kf, sig)[..., None]
        return num / np.maximum(den, 1e-6), den
    fill, den = mblur(26)
    wide, den2 = mblur(90)                              # far from any wall pixel: a wider look, then the wall's median
    fill = np.where(den > 0.05, fill, np.where(den2 > 0.02, wide, np.median(sub[keep], axis=0)))
    a = ndi.gaussian_filter(big.astype(np.float32), 4)[..., None]
    out = img.copy()
    out[y0:y1, x0:x1] = (sub * (1 - a) + fill * a).clip(0, 255).astype(np.uint8)
    return out


def erase(img, kind, rect):
    """takes the shop's print off a business card: the card is found by colour inside rect (upscaled px) and whatever
    of another colour sits inside its outline is painted with the card's own colour, softly."""
    from scipy import ndimage as ndi
    if kind == "wall":
        return wall(img, rect)
    import cv2
    x0, y0, x1, y1 = [v * S for v in rect]
    sub = img[y0:y1, x0:x1].copy()
    f = sub.astype(np.float32); r, g, b = f[..., 0], f[..., 1], f[..., 2]
    if kind == "red_card":                 # a red card with the logo printed light on it, often reaching its edge
        card = (r > 120) & (r > 1.7 * g) & (r > 1.7 * b)
        lab, n = ndi.label(ndi.binary_opening(card, iterations=2))
        if not n:
            return img
        sizes = ndi.sum(card, lab, range(1, n + 1)); k = 1 + int(np.argmax(sizes))
        if sizes[k - 1] < 600:
            return img
        pts = np.argwhere(lab == k)[:, ::-1].astype(np.int32)
        hull = np.zeros(card.shape, np.uint8); cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
        luma = 0.299 * r + 0.587 * g + 0.114 * b
        cl = np.median(luma[lab == k])
        skin = (b < 0.85 * g) & (g > 0.62 * r)                              # his fingers on the card (the print: g ≈ 0.52 r)
        face = ndi.binary_erosion(hull.astype(bool), iterations=2) & ~skin   # the whole card face is repainted plain red,
        near = ndi.binary_dilation(hull.astype(bool), iterations=12)          # (+ the light strip of print on its edge:
        face |= near & ~skin & ((f.min(-1) > 185) | ((r > 1.25 * g) & (luma > cl + 8)))   # white or pink, not the grey wall)
        plain = (lab == k) & (luma <= cl + 6)                                # from its own unprinted red (its shading kept)
        fill = np.stack([ndi.gaussian_filter(f[..., c] * plain, 14) for c in range(3)], -1) / np.maximum(ndi.gaussian_filter(plain.astype(np.float32), 14), 1e-3)[..., None]
        a = ndi.gaussian_filter(face.astype(np.float32), 2.5)[..., None]
        out = img.copy()
        out[y0:y1, x0:x1] = (f * (1 - a) + fill * a).clip(0, 255).astype(np.uint8)
        return out
    else:                                  # a white card with the logo's red star
        mark = (r > 90) & (r > 1.6 * g) & (r > 1.6 * b)      # in its rect only the star is that red (his skin is not)
    mark = ndi.binary_dilation(mark, iterations=6)
    if mark.sum() < 30:
        return img
    out = img.copy()
    out[y0:y1, x0:x1] = cv2.inpaint(sub, mark.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA)
    return out


LANCZOS_MIX = 0.3                    # share of a plain upscale in each frame: the ESRGAN look alone is waxy on faces
GRADE = "eq=contrast=1.07:saturation=1.10:gamma=0.98"   # the ad's flat, bright grade, given a little punch


def picture():
    from PIL import Image
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, ".raw", "up.mp4"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)                # streamed: the whole upscale would not fit in memory
    FB = 1152 * 2048 * 3
    def read():
        buf = dec.stdout.read(FB)
        return np.frombuffer(buf, np.uint8).reshape(1152, 2048, 3) if len(buf) == FB else None
    for _ in range(F0 - UP0):
        read()
    img0 = None
    fnp = os.path.join(ROOT, ".raw", "frames.npy")                 # the source frames (512×288), for the Lanczos mix
    if not os.path.exists(fnp):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, ".raw", "suarez.mp4"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, check=True).stdout
        np.save(fnp, np.frombuffer(raw, np.uint8).reshape(-1, 288, 512, 3))
    src = np.load(fnp, mmap_mode="r")
    n_out = F1 - F0 + 1 + HOLD
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "25", "-i", "-",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", os.path.join(ROOT, ".raw", "picture.mp4")],
                           stdin=subprocess.PIPE)
    rng = np.random.default_rng(7)
    for k in range(n_out):
        n = min(F0 + k, F1)
        if F0 + k <= F1:
            img0 = read(); assert img0 is not None, f"up.mp4 ends before source frame {n}"
        lz = np.asarray(Image.fromarray(src[n]).resize((2048, 1152), Image.LANCZOS), np.float32)
        img = (img0.astype(np.float32) * (1 - LANCZOS_MIX) + lz * LANCZOS_MIX).clip(0, 255).astype(np.uint8)
        for a, b, kind, *rect in LOGOS:
            if a <= n <= b:
                img = erase(img, kind, rect)
        c = centre(n)
        x0 = int(round((c - WIN / 2) * S)); w = WIN * S
        crop = Image.fromarray(img[:, x0:x0 + w]).resize((1080, 1920), Image.LANCZOS)
        a = np.asarray(crop).astype(np.float32)
        a += rng.normal(0, 2.2, a.shape[:2])[..., None]          # a fine grain: no waxy upscale look
        enc.stdin.write(a.clip(0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); assert enc.returncode == 0
    dec.stdout.close(); dec.wait()


def mux():
    n_out = F1 - F0 + 1 + HOLD
    dur, t0 = n_out / 25, F0 / 25
    snd = os.path.join(ROOT, ".raw", "sound.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", os.path.join(ROOT, ".raw", "suarez.mp4"),
                    "-vn", "-af", f"afade=t=in:d=0.04,afade=t=out:st={dur - 0.3:.3f}:d=0.3,loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "48000", "-ac", "2", snd], check=True)
    os.makedirs(os.path.join(ROOT, "assets", "video"), exist_ok=True)
    out = os.path.join(ROOT, "assets", "video", "suarez-916.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, ".raw", "picture.mp4"), "-i", snd, "-vf", GRADE,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    json.dump({"t0": t0, "frames": n_out, "duration": round(dur, 3), "fps": 25}, open(os.path.join(ROOT, "assets", "video", "suarez-916.json"), "w"))
    print(f"suarez-916.mp4: source frames {F0}–{F1} + {HOLD} held = {dur:.2f}s (source {t0:.2f}–{t0 + dur:.2f})")


if __name__ == "__main__":
    import sys
    if "--mux" not in sys.argv:          # --mux: only the sound, the grade and the mux (the picture is ~25 min)
        picture()
    mux()
