#!/usr/bin/env python3
"""The picture and sound of the reel «Suárez habla neerlandés»: three moments of a Sportweek TV interview with Luis
Suárez in the empty Amsterdam ArenA (.raw/habla.mp4, 1280×720, 25 fps, interlaced bottom field first), cut one after
the other (SEGMENTS), cropped to 9:16 on his face and written to assets/video/habla-916.mp4 (1080×1920, 25 fps, the
interview's own sound, balanced and at −14 LUFS).
- The source is deinterlaced (bwdif) first: its fields show as combs on every edge once it is enlarged.
- The 9:16 window (405 source px wide, the full height) follows his face: YuNet finds it in every frame, then a
  smooth camera (median + gaussian) that keeps his whole face inside the window, left of the channel's «SPORTWEEK.NL»
  corner logo (x ≥ 928).
- Each window is enlarged ×4 with Real-ESRGAN («realesr-general-x4v3», ONNX on CPU) and mixed with a plain Lanczos
  enlargement (LANCZOS_MIX) and a fine grain, so his skin keeps its texture.
- The «SPORTWEEK» print on the reporter's red microphone is painted over with the microphone's own red (mic(): in every
  frame, also where the window's edge cuts the mic; checked on every window before the upscale).
- The sound: a high-pass at 90 Hz, the reporter 6 dB down (he is close to the mic), −14 LUFS in two passes (sound()).
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
    (2193, 2365),   # 87.72–94.64 «Maar nu is klaar omdat wij hebben volgende wedstrijd in, in vier… in achtenveertig uur.»
    (3711, 4241),   # 148.44–169.68 «Ben je blij dat je in de spits staat?» … «Ik wil alleen maar spelen.»
]
DEINT = "bwdif=mode=send_frame:parity=bff:deint=all"
LANCZOS_MIX = 0.4                          # (a bit more of the plain enlargement: his skin keeps the source's texture)
GRADE = "eq=contrast=1.04:saturation=1.06"


def frames(a, b):
    """source frames a..b, deinterlaced, as one array (decoded from a little before a, for the deinterlacer)."""
    pre = 4
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{(a - pre) / FPS:.3f}", "-i", SRC, "-vf", DEINT, "-frames:v",
                          str(b - a + 1 + pre), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return fr[pre:pre + b - a + 1]


def detect(fr):
    """his face in each frame, with YuNet (OpenCV's face detector, .raw/yunet.onnx): the biggest face's box (x0, x1)
    and its centre (the eyes and the nose, so the hair does not pull it off), or None where there is no face.
    (v1 used OpenCV's Haar cascades: they missed a quarter of the frames and took his chin for a face.)"""
    import cv2
    det = cv2.FaceDetectorYN.create(os.path.join(ROOT, ".raw", "yunet.onnx"), "", (W, H), 0.6, 0.3, 5000)
    out = []
    for f in fr:
        _, fs = det.detect(cv2.cvtColor(np.ascontiguousarray(f), cv2.COLOR_RGB2BGR))
        if fs is None or not len(fs):
            out.append(None)
            continue
        x, y, w, h, rx, ry, lx, ly, nx, ny = max(fs, key=lambda r: r[2] * r[3])[:10]
        out.append((float((rx + lx + 2 * nx) / 4), float(x), float(x + w)))
    return out


def smooth(det):
    """a camera that follows his face smoothly: missing frames filled in, a running median and a gaussian (σ 0.3 s),
    then nudged so his whole face stays at least FACE_M px inside the window, and kept between the frame's left edge
    and the corner logo (clipped before the last smoothing, so it eases into that limit)."""
    from scipy.ndimage import median_filter, gaussian_filter1d
    def fill(v):
        v = np.array(v, float); ok = ~np.isnan(v)
        return np.interp(np.arange(len(v)), np.flatnonzero(ok), v[ok])
    cx = fill([np.nan if d is None else d[0] for d in det])
    x0 = fill([np.nan if d is None else d[1] for d in det])
    x1 = fill([np.nan if d is None else d[2] for d in det])
    x = gaussian_filter1d(median_filter(cx, size=9, mode="nearest"), 8, mode="nearest")
    lo, hi = x1 + FACE_M - WIN / 2, x0 - FACE_M + WIN / 2
    for _ in range(4):
        x = np.where(lo > hi, (lo + hi) / 2, np.clip(x, lo, hi))
        x = gaussian_filter1d(np.clip(x, C_MIN, C_MAX), 3, mode="nearest")
    return np.clip(x, C_MIN, C_MAX)


FACE_M = 18                                # source px of margin between his face and the window's edges


def mic(win):
    """the reporter's red microphone, low in the window, with «SPORTWEEK» printed light on it: the print is painted with
    the mic's own red around it, softly. The mic is its red (every part of it, also where the print band cuts it in two),
    its outline is closed over the letters and along the frame's edge where the window cuts it, and clipped to its convex
    hull (the foam ball is convex: no red teeth into the seats behind). The print is what is not the mic's red inside
    that outline, and any light (white or pink) pixel on the mic."""
    import cv2
    from scipy import ndimage as ndi
    f = win.astype(np.float32); r, g, b = f[..., 0], f[..., 1], f[..., 2]
    hw = win.shape[0]
    red = (r > 150) & (r > 1.9 * g) & (r > 1.9 * b)
    red[: int(hw * 0.55)] = False                              # only low in the frame (the stadium's seats are higher up)
    op = ndi.binary_opening(red, iterations=2)
    lab, n = ndi.label(op)
    if not n:
        return win
    sizes = ndi.sum(op, lab, range(1, n + 1)); k = 1 + int(np.argmax(sizes))
    if sizes[k - 1] < 800:
        return win
    body = lab == k
    top = np.flatnonzero(body.any(1))[0]
    near = ndi.binary_dilation(body, iterations=40)
    for j in range(1, n + 1):                                  # the parts the print band cuts off
        if j != k and sizes[j - 1] >= 300:
            comp = lab == j
            if (comp & near).any() and np.flatnonzero(comp.any(1))[0] >= top - 10:
                body |= comp
    shade = (r > 110) & (r > 1.9 * g) & (r > 1.9 * b)
    body |= shade & ndi.binary_dilation(body, iterations=25)  # (+ its shaded rim, and the thin red cut off by the letters)
    core = ndi.binary_opening(body, iterations=4)
    if core.sum() < 300:
        return win
    P = 14
    pad = np.pad(body, P, mode="constant", constant_values=False)
    ext = core.copy()
    le, be = body[:, :3].any(1), body[-3:, :].any(0)
    L, B = le.sum() > 8, be.sum() > 8
    if L:                                                      # where the frame's edge cuts the mic, the cut is part
        i0 = np.flatnonzero(le)                                # of its outline (to the corner, if both edges are cut)
        pad[i0.min() + P:(None if B else i0.max() + 1 + P), :P] = True
        ext[i0.min():(None if B else i0.max() + 1), 0] = True
    if B:
        i0 = np.flatnonzero(be)
        pad[-P:, (0 if L else i0.min() + P):i0.max() + 1 + P] = True
        ext[-1, (0 if L else i0.min()):i0.max() + 1] = True
    hull = np.zeros(body.shape, np.uint8)
    cv2.fillPoly(hull, [cv2.convexHull(np.argwhere(ext)[:, ::-1].astype(np.int32))], 1)
    hull = ndi.binary_dilation(hull.astype(bool), iterations=2)
    region = ndi.binary_fill_holes(ndi.binary_closing(pad, iterations=9, border_value=0))[P:-P, P:-P]
    region &= hull
    light = ((f.min(-1) > 120) | ((r > 170) & (g > 0.62 * r))) & ndi.binary_dilation(body, iterations=6) & region
    inside = (region & ~body) | light
    redfrac = ndi.uniform_filter(body.astype(np.float32), 31, mode="nearest")
    inside &= redfrac > 0.3                                    # on the mic: never the shirt or the stands next to it
    if inside.sum() < 30:
        return win
    inside = ndi.binary_dilation(inside, iterations=1)
    face = ndi.binary_dilation(inside, iterations=3) & (region | body)
    srcp = np.ascontiguousarray(win).copy()                    # (only the mic's red to take from: not the shirt or the
    srcp[~body & ~face] = np.median(win[body & ~face], 0).astype(np.uint8)   # stands where it touches the frame's edge)
    fill = cv2.inpaint(srcp, face.astype(np.uint8), 9, cv2.INPAINT_TELEA).astype(np.float32)
    fill = ndi.gaussian_filter(fill, (2.5, 2.5, 0)) * face[..., None] + fill * ~face[..., None]   # (no streaks)
    a = ndi.gaussian_filter(face.astype(np.float32), 1.5)[..., None]
    return (f * (1 - a) + fill * a).clip(0, 255).astype(np.uint8)


def track():
    from PIL import Image, ImageDraw
    out = {}
    tiles = []
    for a, b in SEGMENTS:
        fr = frames(a, b)
        det = detect(fr)
        c = smooth(det)
        out[f"{a}"] = {"raw": det, "centre": [round(float(v), 1) for v in c]}
        print(f"segment {a}–{b}: {sum(v is None for v in det)}/{len(det)} frames without a face; centre {c.min():.0f}–{c.max():.0f}")
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


REPORTER_DB = -6                           # the reporter is off screen and close to the mic: 5–8 LU louder than Suárez
FADE_OUT = [0.025, 0.06, 0.025, 0.025]     # each moment's sound fades out over this (the 2nd ends on a voiced «m»)


def sound():
    """the interview's own sound under each moment, joined with short fades; a high-pass at 90 Hz (the handheld mic's
    wind and handling rumble, and the low thump of the reporter's «p»s); the reporter's lines 6 dB down (Scribe's
    speaker_1, ramped over 80 ms); −14 LUFS in two passes (linear), true peak under −2 dBTP → .raw/sound.wav."""
    import wave
    parts, filt = [], []
    for i, (a, b) in enumerate(SEGMENTS):
        d = (b - a + 1) / FPS
        parts += ["-ss", f"{a / FPS:.3f}", "-t", f"{d:.3f}", "-i", SRC]
        fo = FADE_OUT[i]
        filt.append(f"[{i}:a]aresample=48000,atrim=0:{d:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.025,afade=t=out:st={d - fo:.3f}:d={fo}[a{i}]")
    n = len(SEGMENTS)
    filt.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,highpass=f=90:poles=2[out]")
    pre = os.path.join(ROOT, ".raw", "sound_pre.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *parts, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "48000", "-ac", "2",
                    "-c:a", "pcm_s16le", pre], check=True)
    # the reporter's words (reel seconds), merged where they are less than 0.3 s apart
    words = [w for w in json.load(open(os.path.join(ROOT, ".raw", "scribe.json")))["words"]
             if w.get("type") == "word" and w.get("speaker_id") == "speaker_1"]
    win, t = [], 0.0
    for a, b in SEGMENTS:
        s0, s1 = a / FPS, (b + 1) / FPS
        for w in words:
            if s0 <= w["start"] < s1:
                win.append([t + w["start"] - s0 - 0.12, t + min(w["end"], s1) - s0 + 0.12])
        t += (b - a + 1) / FPS
    win.sort(); merged = []
    for a, b in win:
        if merged and a - merged[-1][1] < 0.3:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    with wave.open(pre) as wf:
        sr, nch = wf.getframerate(), wf.getnchannels()
        x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).reshape(-1, nch).astype(np.float32)
    tt = np.arange(len(x)) / sr
    duck = np.zeros(len(x), np.float32); R = 0.08
    for a, b in merged:
        duck = np.maximum(duck, np.clip((tt - a + R) / R, 0, 1) * np.clip((b + R - tt) / R, 0, 1))
    x *= (1 - (1 - 10 ** (REPORTER_DB / 20)) * duck)[:, None]
    ducked = os.path.join(ROOT, ".raw", "sound_duck.wav")
    with wave.open(ducked, "wb") as wf:
        wf.setnchannels(nch); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes(x.clip(-32768, 32767).astype(np.int16).tobytes())
    m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", ducked, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    snd = os.path.join(ROOT, ".raw", "sound.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ducked, "-af", ln, "-ar", "48000", "-ac", "2", snd], check=True)
    print(f"sound: {len(merged)} reporter lines ducked {REPORTER_DB} dB; measured {m['input_i']} LUFS → −14")
    return snd


def mux():
    """the picture (.raw/picture.mp4), graded, with the sound → assets/video/habla-916.mp4 (+ .json)."""
    snd = sound()
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
