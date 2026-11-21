#!/usr/bin/env python3
"""The ebook for ins-05, cut to her words, from the client's «Animación Libro» (7 s on black: the cover of «Holandés sin
miedo» opens — «Cómo usar este libro | Woordenschat» —, the pages turn — De familie, the pronouns table, De nummers,
«¡Hora de practicar!», Hebben en zijn | Klanken — and it closes again on the cover at 6.0 s).

assets/video/libro-ins05.webm (1920×1080, VP9 with alpha, silent, lanczos-upscaled from 1280×720) lasts exactly as long
as ins-05, the book lifted off its black (it floats on Nawar blue, no black box): the whole animation up to the closed
cover (source 0–CLOSE) played a little faster, so it opens on «nuestro libro», turns its pages while she says what it is
(«…para principiantes, explicado en español…») and lands closed on the cover just before «un euro», where the price
arrives (ins_05.py); that frame holds to the cut back to her.
The key: the animation's background is pure black, so alpha = how far a pixel is from black, made solid inside the
book's outline (holes filled: its dark print stays opaque) and zero outside it (the faint dark reflection under the book
goes), and the edge colours are un-premultiplied (they were blended with black), so no dark rim shows on the blue.
"""
import json, os, subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".raw", "libro2.mp4")
CLOSE = 6.20                      # source seconds: the book has closed flat on its cover (from 6.0); held from here
IID = "ins-05"


def main():
    ed = json.load(open(os.path.join(ROOT, "edit.json")))
    ins = next(i for i in ed["inserts"] if i["id"] == IID)
    t0, d = ins["start"], ins["duration"]
    un = [w for w in ed["words"] if t0 <= w["t"] < t0 + d and w["text"].lower() == "un"][-1]["t"] - t0
    a_out = round(un - 0.12, 3)                        # closed on the cover a beat before «un euro»
    sp = CLOSE / a_out
    n_a = int(round(a_out * 30)); n = int(round(d * 30)) + 2; n_b = n - n_a
    fa1 = int(round(CLOSE * 30))
    fc = (f"[0:v]split=2[s0][s1];"
          f"[s0]trim=start_frame=0:end_frame={fa1},setpts=(PTS-STARTPTS)/{sp:.5f},fps=30,trim=end_frame={n_a},setpts=N/30/TB[a];"
          f"[s1]trim=start_frame={fa1}:end_frame={fa1 + 1},loop=loop={n_b - 1}:size=1:start=0,setpts=N/30/TB[b];"
          f"[a][b]concat=n=2:v=1:a=0,scale=1920:1080:flags=lanczos,unsharp=5:5:0.35,format=yuv420p[v]")
    mid = os.path.join(ROOT, ".raw", "libro-ins05.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[v]", "-r", "30", "-c:v", "libx264",
                    "-crf", "12", "-preset", "slow", "-movflags", "+faststart", mid], check=True)
    out = os.path.join(ROOT, "assets", "video", "libro-ins05.webm")
    n = key(mid, out)
    json.dump({"speed": round(sp, 4), "played": a_out, "close": CLOSE, "frames": n},
              open(os.path.join(ROOT, "assets", "video", "libro-ins05.json"), "w"))
    print(f"libro-ins05.webm: played 0–{CLOSE}s in {a_out:.2f}s (×{sp:.3f}) + the closed cover held {n_b / 30:.2f}s = {n / 30:.2f}s ({IID} {d}s)")


def key(src, dst, W=1920, H=1080):
    from scipy import ndimage as ndi
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "16", "-auto-alt-ref", "0", "-row-mt", "1", dst],
                           stdin=subprocess.PIPE)
    def silhouette(f):
        m = f.max(-1)
        book = ndi.binary_fill_holes(ndi.binary_closing(m > 45, iterations=2))          # the book itself (its darkest edge is navy)
        lab, n = ndi.label(book)
        if n > 1:                                                            # specks of the faint reflection under it go
            sz = ndi.sum(np.ones(book.shape), lab, range(1, n + 1)); book = np.isin(lab, 1 + np.flatnonzero(sz >= 0.05 * sz.max()))
        return book
    books = [silhouette(f) for f in fr]
    for k, f in enumerate(fr):
        rgb = f.astype(np.float32); m = rgb.max(-1)
        soft = np.clip((m - 30) / 30, 0, 1)                                  # distance from black (the faint contact shadow, m 25–32, goes)
        nb = [books[j] for j in (k - 1, k + 1) if 0 <= j < len(books)]       # where the book is in the frames on both sides — and it
        both = nb[0] & nb[-1]                                                # holds still there — it is here too: on the first frame the
        still = both.sum() > 0.98 * (nb[0] | nb[-1]).sum()                   # cover's dark canal water touches its bottom edge and
        book = books[k] | both if still else books[k]                        # would read as a bite out of it (never while a page flips)
        solid = ndi.binary_erosion(book, iterations=2)
        a = np.maximum(soft, solid.astype(np.float32)) * ndi.binary_dilation(book, iterations=1)   # nothing outside the book
        a = ndi.gaussian_filter(a, 0.7)
        un = np.where(a[..., None] > 0.04, rgb / np.maximum(soft, 0.04)[..., None], 0)   # un-premultiply the black-blended edge
        rgb = np.where(solid[..., None], rgb, np.clip(un, 0, 255))
        enc.stdin.write(np.dstack([rgb, a * 255]).clip(0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); assert enc.returncode == 0
    return len(fr)


if __name__ == "__main__":
    main()
