#!/usr/bin/env python3
"""The picture and sound of the reel «Suárez habla neerlandés»: three moments of a Sportweek TV interview with Luis
Suárez in the empty Amsterdam ArenA (.raw/habla.mp4, 1280×720, 25 fps, interlaced bottom field first), cut one after
the other (SEGMENTS), cropped to 9:16 on his face and written to assets/video/habla-916.mp4 (1080×1920, 25 fps, the
interview's own sound at −14 LUFS).
- The source is deinterlaced (bwdif) first: its fields show as combs on every edge once it is enlarged.
- The 9:16 window (405 source px wide, the full height) follows his face: a face detector on every frame, then a
  slow, smooth camera (median + gaussian), kept left of the channel's «SPORTWEEK.NL» corner logo (x ≥ 928).
- Each window is enlarged ×4 with Real-ESRGAN («realesr-general-x4v3», ONNX on CPU) and mixed with a plain Lanczos
  enlargement (LANCZOS_MIX) and a fine grain, so his skin keeps its texture.
- The «SPORTWEEK» print on the reporter's red microphone is painted over with the microphone's own red (mic()).
  python3 tools/frame.py --track     the face track and the windows → .raw/track.json (+ a preview sheet)
  python3 tools/frame.py             the picture (~50 min) and the sound → assets/video/habla-916.mp4
  python3 tools/frame.py --mux       only the sound, the grade and the mux
"""
import json, os, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".raw", "habla.mp4")
W, H, FPS = 1280, 720, 25
WIN = 405                                  # 9:16 window width in source px (720 × 9/16)
LOGO_X = 928                               # the channel's corner logo starts here: the window stays left of it
C_MIN, C_MAX = WIN / 2, LOGO_X - 4 - WIN / 2
# (first, last) source frame of each moment, in reel order (source s × 25)
SEGMENTS = [
    (1161, 1296),   # 46.44–51.88 «Het was spannend.» «Wie?» «De wedstrijd was spannend, denk ik.» «Ja, klein beetje.»
    (1824, 2042),   # 72.96–81.72 «Feestje gevierd?» «Sorry?» «Feest. Feestje gevierd?» «Ah, nee, nee… Echt tevreden.»
    (2193, 2365),   # 87.72–94.64 «Maar nu is klaar omdat wij hebben volgende wedstrijd in vier, negen en veertig uur.»
    (3711, 4241),   # 148.44–169.68 «Ben je blij dat je in de spits staat?» … «Ik wil alleen maar spelen.»
]
DEINT = "bwdif=mode=send_frame:parity=bff:deint=all"
LANCZOS_MIX = 0.3
GRADE = "eq=contrast=1.04:saturation=1.06"


def frames(a, b):
    """source frames a..b, deinterlaced, as one array (decoded from a little before a, for the deinterlacer)."""
    pre = 4
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{(a - pre) / FPS:.3f}", "-i", SRC, "-vf", DEINT, "-frames:v",
                          str(b - a + 1 + pre), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return fr[pre:pre + b - a + 1]


def detect(fr):
    """the centre x of the biggest face in each frame (None where none is found)."""
    import cv2
    fc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    pc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
    out = []
    for f in fr:
        g = cv2.cvtColor(np.ascontiguousarray(f), cv2.COLOR_RGB2GRAY)
        fs = fc.detectMultiScale(g, 1.1, 5, minSize=(180, 180))
        if not len(fs):
            fs = pc.detectMultiScale(g, 1.1, 5, minSize=(180, 180))
            if not len(fs):
                fs = [(W - x - w, y, w, h) for x, y, w, h in pc.detectMultiScale(g[:, ::-1], 1.1, 5, minSize=(180, 180))]
        out.append(None if not len(fs) else float(max(fs, key=lambda r: r[2] * r[3])[0] + max(fs, key=lambda r: r[2] * r[3])[2] / 2))
    return out


def smooth(cx):
    """a camera that follows his face slowly: missing frames filled in, then a running median (1 s) and a gaussian
    (σ 0.5 s), kept between the frame's left edge and the corner logo."""
    from scipy.ndimage import median_filter, gaussian_filter1d
    x = np.array([np.nan if c is None else c for c in cx], float)
    ok = ~np.isnan(x)
    x = np.interp(np.arange(len(x)), np.flatnonzero(ok), x[ok])
    x = median_filter(x, size=25, mode="nearest")
    x = gaussian_filter1d(x, 12, mode="nearest")
    return np.clip(x, C_MIN, C_MAX)


def mic(win):
    """the reporter's red microphone, low in the window, with «SPORTWEEK» printed light on it: the print (what is not
    the mic's red inside its outline) is painted with the mic's own red around it, softly."""
    from scipy import ndimage as ndi
    f = win.astype(np.float32); r, g, b = f[..., 0], f[..., 1], f[..., 2]
    red = (r > 150) & (r > 1.9 * g) & (r > 1.9 * b)
    red[: int(win.shape[0] * 0.55)] = False                    # only low in the frame (the stadium's seats are higher up)
    lab, n = ndi.label(ndi.binary_opening(red, iterations=2))
    if not n:
        return win
    sizes = ndi.sum(red, lab, range(1, n + 1)); k = 1 + int(np.argmax(sizes))
    if sizes[k - 1] < 800:
        return win
    body = lab == k
    body |= red & ndi.binary_dilation(body, iterations=25)     # (+ its thin red rim cut off by the letters)
    P = 14                                                     # its outline, closed over the letters (thin strokes),
    pad = np.pad(body, P, mode="constant", constant_values=False)   # also where the frame's edge cuts the mic: there
    for side, edge in (("l", body[:, :3].any(1)), ("b", body[-3:, :].any(0))):   # the cut is part of its outline
        if edge.sum() > 8:
            i = np.flatnonzero(edge); sl = slice(i.min() + P, i.max() + 1 + P)
            if side == "l":
                pad[sl, :P] = True
            else:
                pad[-P:, sl] = True
    region = ndi.binary_closing(pad, iterations=9, border_value=0)[P:-P, P:-P]
    region = ndi.binary_fill_holes(region)
    inside = region & ~body                                    # the print and its pink rim: whatever is not the mic's red
    if inside.sum() < 30:
        return win
    face = ndi.binary_dilation(inside, iterations=3) & region
    plain = (body & ~ndi.binary_dilation(inside, iterations=3)).astype(np.float32)
    num = np.stack([ndi.gaussian_filter(f[..., c] * plain, 6) for c in range(3)], -1)
    den = ndi.gaussian_filter(plain, 6)[..., None]
    fill = np.where(den > 0.05, num / np.maximum(den, 1e-3), np.median(f[plain > 0], 0))
    a = ndi.gaussian_filter(face.astype(np.float32), 1.2)[..., None]
    return (f * (1 - a) + fill * a).clip(0, 255).astype(np.uint8)


def track():
    from PIL import Image, ImageDraw
    out = {}
    tiles = []
    for a, b in SEGMENTS:
        fr = frames(a, b)
        cx = detect(fr)
        c = smooth(cx)
        out[f"{a}"] = {"raw": cx, "centre": [round(float(v), 1) for v in c]}
        print(f"segment {a}–{b}: {sum(v is None for v in cx)}/{len(cx)} frames without a face; centre {c.min():.0f}–{c.max():.0f}")
        for k in range(0, len(fr), 15):
            x0 = int(round(c[k] - WIN / 2))
            t = Image.fromarray(np.ascontiguousarray(fr[k][:, x0:x0 + WIN])).resize((135, 240))
            ImageDraw.Draw(t).text((3, 3), f"{(a + k) / FPS:.1f}", fill=(255, 255, 0))
            tiles.append(t)
    json.dump(out, open(os.path.join(ROOT, ".raw", "track.json"), "w"))
    cols = 16
    sheet = Image.new("RGB", (135 * cols, 240 * ((len(tiles) + cols - 1) // cols)))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 135, (i // cols) * 240))
    sheet.save(os.path.join(ROOT, ".raw", "track.jpg"), quality=88)


def stream(a, b):
    """source frames a..b, deinterlaced, one at a time."""
    pre = 4
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{(a - pre) / FPS:.3f}", "-i", SRC, "-vf", DEINT, "-frames:v",
                            str(b - a + 1 + pre), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    FB = W * H * 3
    for k in range(b - a + 1 + pre):
        buf = dec.stdout.read(FB)
        assert len(buf) == FB, f"source ends before frame {a + k - pre}"
        if k >= pre:
            yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    dec.stdout.close(); dec.wait()


def picture():
    import time
    import onnxruntime as ort
    from PIL import Image
    sess = ort.InferenceSession(os.path.join(ROOT, ".raw", "esrgan-x4v3.onnx"), providers=["CPUExecutionProvider"])
    tr = json.load(open(os.path.join(ROOT, ".raw", "track.json")))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", os.path.join(ROOT, ".raw", "picture.mp4")],
                           stdin=subprocess.PIPE)
    rng = np.random.default_rng(7)
    M = 16                                                         # context around the window for the upscaler
    t0, done, total = time.time(), 0, sum(b - a + 1 for a, b in SEGMENTS)
    for a, b in SEGMENTS:
        cs = tr[str(a)]["centre"]
        assert len(cs) >= b - a + 1, "re-run --track: the segments changed"
        for k, f in enumerate(stream(a, b)):
            left = cs[k] - WIN / 2                                 # the window's left edge, sub-pixel
            x0 = int(np.floor(left))
            fx = f.copy()
            fx[:, x0:x0 + WIN + 1] = mic(np.ascontiguousarray(f[:, x0:x0 + WIN + 1]))
            c0, c1 = max(0, x0 - M), min(W, x0 + WIN + 1 + M)
            crop = np.ascontiguousarray(fx[:, c0:c1])
            y = sess.run(None, {"input": (crop.astype(np.float32) / 255).transpose(2, 0, 1)[None]})[0][0].transpose(1, 2, 0)
            up = Image.fromarray((y.clip(0, 1) * 255 + 0.5).astype(np.uint8))
            ox = (left - c0) * 4
            es = np.asarray(up.resize((1080, 1920), Image.LANCZOS, box=(ox, 0, ox + WIN * 4, H * 4)), np.float32)
            lz = np.asarray(Image.fromarray(crop).resize((1080, 1920), Image.LANCZOS, box=(left - c0, 0, left - c0 + WIN, H)), np.float32)
            img = es * (1 - LANCZOS_MIX) + lz * LANCZOS_MIX
            img += rng.normal(0, 2.0, img.shape[:2])[..., None]   # a fine grain: no waxy upscale look
            enc.stdin.write(img.clip(0, 255).astype(np.uint8).tobytes())
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{total}  {time.time() - t0:.0f}s", flush=True)
    enc.stdin.close(); enc.wait(); assert enc.returncode == 0


def mux():
    """the interview's own sound under each moment, joined with 25 ms fades, at −14 LUFS."""
    parts, filt = [], []
    for i, (a, b) in enumerate(SEGMENTS):
        d = (b - a + 1) / FPS
        parts += ["-ss", f"{a / FPS:.3f}", "-t", f"{d:.3f}", "-i", SRC]
        filt.append(f"[{i}:a]aresample=48000,atrim=0:{d:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.025,afade=t=out:st={d - 0.025:.3f}:d=0.025[a{i}]")
    n = len(SEGMENTS)
    filt.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    snd = os.path.join(ROOT, ".raw", "sound.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *parts, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "48000", "-ac", "2", snd], check=True)
    out = os.path.join(ROOT, "assets", "video", "habla-916.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, ".raw", "picture.mp4"), "-i", snd, "-vf", GRADE,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    frames_n = sum(b - a + 1 for a, b in SEGMENTS)
    starts, t = [], 0.0
    for a, b in SEGMENTS:
        starts.append({"reel": round(t, 3), "source": round(a / FPS, 3), "frames": b - a + 1}); t += (b - a + 1) / FPS
    json.dump({"frames": frames_n, "duration": round(frames_n / FPS, 3), "fps": FPS, "segments": starts},
              open(os.path.join(ROOT, "assets", "video", "habla-916.json"), "w"))
    print(f"habla-916.mp4: {len(SEGMENTS)} moments, {frames_n} frames = {frames_n / FPS:.2f}s")


if __name__ == "__main__":
    if "--track" in sys.argv:
        track()
    elif "--mux" in sys.argv:
        mux()
    else:
        picture()
        mux()
