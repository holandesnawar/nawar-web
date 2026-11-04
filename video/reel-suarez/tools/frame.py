#!/usr/bin/env python3
"""The picture and sound of the reel: the ad from source frame 135 (Suárez walking in — the brand intro before it is
cut) to frame 993 (the last frame before the brand end card), held 8 frames under the end of «…genoeg», cropped to
9:16 out of the ×4 upscale (.raw/up.mp4, tools/upscale.py) and written to assets/video/suarez-916.mp4 (1080×1920,
25 fps, the ad's own sound from 5.40 s to 40.08 s, before the brand voice-over, at −14 LUFS).
Each shot has its own 9:16 window (SHOTS: the centre in source px — 512 wide —, keyframed where the camera or the
speaker moves; a window is 162 source px wide), on whoever talks. What still shows of the brand inside a window is
taken out (LOGOS): the red business card's print and the red star on the white one.
  python3 tools/frame.py
"""
import json, os, subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP0, F0, F1, HOLD = 123, 135, 993, 8        # up.mp4 starts at source frame 123; the reel plays 135–993, then holds
S = 4                                       # upscale factor (512×288 → 2048×1152)
WIN = 162                                   # 9:16 window width in source px (288 × 9/16)
CUTS = [123, 148, 172, 193, 302, 334, 375, 471, 495, 551, 648, 690, 740, 772, 786, 866, 892, 928, 945, 960, 994]
# shot (first frame) → [(source frame, window centre x in source px)]; linear between keyframes, eased
SHOTS = {      # (set from a face detector run on every 3rd frame, and checked by eye on native-scale frames)
    123: [(123, 262)],                          # Suárez walks in (the reel opens here)
    148: [(148, 330), (160, 318), (171, 300)],  # over his shoulder: the assistant, «een sportman van Ajax»
    172: [(172, 175)],                          # the Ajax badge
    193: [(193, 245), (210, 300), (222, 318), (301, 318)],   # the assistant: «Ja, beroemde club. Cruijff…»
    302: [(302, 168), (333, 198)],              # Suárez, wide: «Ja, ik hoorde iets…»
    334: [(334, 215), (356, 205), (374, 255)],  # Suárez close: «…anti-fluitregeling» (on his mouth)
    375: [(375, 280), (405, 312), (440, 285), (470, 308)],   # the assistant: «Ah, u bedoelt…»
    471: [(471, 190)],                          # the hearing aid
    495: [(495, 320), (507, 302), (550, 302)],  # the assistant close: «…fluittonen hoort»
    551: [(551, 205), (600, 285), (647, 245)],  # Suárez close: «Zij fluiten veel te vaak tegen mij»
    648: [(648, 290), (670, 315), (689, 245)],  # the assistant close: «Oh, maar dan…»
    690: [(690, 395), (710, 372), (739, 372)],  # wide, on the assistant as he talks: «…oordopjesgamma»
    740: [(740, 250)],                          # the sofa: «Neemt u maar even op de bank plaats»
    772: [(772, 212), (785, 200)],              # Suárez: «Hè?»
    786: [(786, 195), (812, 250), (828, 300), (834, 165), (865, 175)],   # Suárez close, a dip, then his hand
    866: [(866, 185), (891, 195)],              # wide on Suárez: «Nou, veel succes ermee»
    892: [(892, 312), (927, 315)],              # the assistant: «En mocht u nog een fluitje horen…»
    928: [(928, 160), (936, 200), (944, 228)],  # Suárez
    945: [(945, 268)],                          # the assistant holds up a red business card: «Kaartje?»
    960: [(960, 180), (978, 155), (993, 180)],  # Suárez: «Nee, nee, ik heb kaartjes genoeg»
}
# brand marks inside the windows: (first frame, last frame, kind, source rect x0, y0, x1, y1)
LOGOS = [(945, 959, "red_card", 150, 20, 240, 140),     # the assistant's red business card (the shop's logo printed light)
         (960, 993, "white_card", 215, 35, 300, 110),    # the white card with the shop's red star (on its way out of frame)
         (148, 171, "wall", 385, 40, 512, 140),          # «De hoorspecialist» on the orange wall, where a window reaches it
         (193, 301, "wall", 385, 40, 512, 140),
         (375, 470, "wall", 385, 40, 512, 140),
         (892, 927, "wall", 385, 40, 512, 140),
         (945, 959, "wall", 385, 40, 512, 140)]


def centre(n):
    s = max(c for c in CUTS if c <= n)
    ks = SHOTS[s]
    if n <= ks[0][0]:
        c = ks[0][1]
    elif n >= ks[-1][0]:
        c = ks[-1][1]
    else:
        (a, ca), (b, cb) = next((p, q) for p, q in zip(ks, ks[1:]) if p[0] <= n <= q[0])
        u = (n - a) / (b - a); u = u * u * (3 - 2 * u)
        c = ca + (cb - ca) * u
    return min(max(c, WIN / 2), 512 - WIN / 2)


def wall(img, rect):
    """the shop's slogan in light letters on the out-of-focus orange wall: the letters (lighter or less saturated than
    the wall around them) are painted over with the wall (OpenCV inpainting)."""
    import cv2
    from scipy import ndimage as ndi
    x0, y0, x1, y1 = [v * S for v in rect]
    sub = img[y0:y1, x0:x1].copy()
    f = sub.astype(np.float32); r, g, b = f[..., 0], f[..., 1], f[..., 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    sat = (f.max(-1) - f.min(-1)) / np.maximum(f.max(-1), 1)
    orange = (r > 140) & (r > 1.25 * g) & (g > 1.2 * b)
    wallish = ndi.binary_closing(ndi.gaussian_filter(orange.astype(np.float32), 12) > 0.45, iterations=8)
    ml, ms = ndi.median_filter(luma, 41), ndi.median_filter(sat, 41)
    text = wallish & ((luma - ml > 14) | (ms - sat > 0.10))
    text = ndi.binary_dilation(ndi.binary_opening(text, iterations=1), iterations=4)
    if not text.any():
        return img
    out = img.copy()
    out[y0:y1, x0:x1] = cv2.inpaint(sub, text.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
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
        mark = hull.astype(bool) & (luma > cl + 12) & (np.abs(g - b) < 30)   # the light print (not his skin: g ≫ b)
    else:                                  # a white card with the logo's red star
        mark = (r > 90) & (r > 1.6 * g) & (r > 1.6 * b)      # in its rect only the star is that red (his skin is not)
    mark = ndi.binary_dilation(mark, iterations=6)
    if mark.sum() < 30:
        return img
    out = img.copy()
    out[y0:y1, x0:x1] = cv2.inpaint(sub, mark.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA)
    return out


def main():
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
    n_out = F1 - F0 + 1 + HOLD
    dur = n_out / 25
    t0 = F0 / 25
    vid = os.path.join(ROOT, ".raw", "picture.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "25", "-i", "-",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    rng = np.random.default_rng(7)
    log = []
    for k in range(n_out):
        n = min(F0 + k, F1)
        if F0 + k <= F1:
            img0 = read(); assert img0 is not None, f"up.mp4 ends before source frame {n}"
        img = img0
        for a, b, kind, *rect in LOGOS:
            if a <= n <= b:
                img = erase(img, kind, rect)
        c = centre(n)
        x0 = int(round((c - WIN / 2) * S)); w = WIN * S
        crop = Image.fromarray(img[:, x0:x0 + w]).resize((1080, 1920), Image.LANCZOS)
        a = np.asarray(crop).astype(np.float32)
        a += rng.normal(0, 2.2, a.shape[:2])[..., None]          # a fine grain: no waxy upscale look
        enc.stdin.write(a.clip(0, 255).astype(np.uint8).tobytes())
        log.append({"k": k, "src": n, "centre": round(c, 1)})
    enc.stdin.close(); enc.wait(); assert enc.returncode == 0
    dec.stdout.close(); dec.wait()
    snd = os.path.join(ROOT, ".raw", "sound.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", os.path.join(ROOT, ".raw", "suarez.mp4"),
                    "-vn", "-af", f"afade=t=in:d=0.04,afade=t=out:st={dur - 0.3:.3f}:d=0.3,loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "48000", "-ac", "2", snd], check=True)
    os.makedirs(os.path.join(ROOT, "assets", "video"), exist_ok=True)
    out = os.path.join(ROOT, "assets", "video", "suarez-916.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", snd, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    json.dump({"t0": t0, "frames": n_out, "duration": round(dur, 3), "fps": 25}, open(os.path.join(ROOT, "assets", "video", "suarez-916.json"), "w"))
    print(f"suarez-916.mp4: source frames {F0}–{F1} + {HOLD} held = {dur:.2f}s (source {t0:.2f}–{t0 + dur:.2f})")


if __name__ == "__main__":
    main()
