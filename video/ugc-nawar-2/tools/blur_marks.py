#!/usr/bin/env python3
"""Blur the third-party marks on the laptop in the hook of UGC.POV1 (the HP logo on the lid and the Intel sticker on
the palm rest) and transcode the take for the renderer.

The logo was tracked frame by frame (tools/align/pov1_logo_track.json: centre + size per frame). Here a soft
elliptical mask is drawn per frame, and ffmpeg blends a blurred copy of the picture through it. Pixels outside the
mask are untouched, so the colour stays identical to the plain transcode.
    python3 tools/blur_marks.py .raw/pov1.mov assets/video/take-1.mp4
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
STICKER = (-490, -43, 62, 42)      # Intel sticker: offset from the logo centre + semi-axes, while the laptop is on her lap
GRADE = "eq=contrast=1.05:saturation=1.05:gamma=0.98"
AUDIO = "highpass=f=80,afftdn=nr=10:nf=-42,loudnorm=I=-16:TP=-1.5:LRA=11"

def masks():
    tr = json.load(open(os.path.join(ROOT, "tools", "align", "pov1_logo_track.json")))["boxes"]
    last = max(int(k) for k in tr)
    for i in range(last + 1):
        m = Image.new("L", (W, H), 0)
        if str(i) in tr:
            x, y, w, h = tr[str(i)]; d = ImageDraw.Draw(m)
            ax, ay = 0.8 * w + 20, 0.8 * h + 20
            d.ellipse((x - ax, y - ay, x + ax, y + ay), fill=255)
            if y > 1700 and i >= 52:
                sx, sy, sa, sb = x + STICKER[0], y + STICKER[1], STICKER[2], STICKER[3]
                d.ellipse((sx - sa, sy - sb, sx + sa, sy + sb), fill=255)
            m = m.filter(ImageFilter.GaussianBlur(9))
        yield np.asarray(m, dtype=np.uint8)

def main(src, dst):
    tmp = os.path.join(ROOT, ".raw", "pov1_marks_mask.mkv")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "ffv1", tmp], stdin=subprocess.PIPE)
    for m in masks():
        p.stdin.write(m.tobytes())
    p.stdin.close(); p.wait()
    fc = (f"[1:v]format=gray,tpad=stop_mode=add:stop_duration=120:color=black[m];"
          f"[0:v]split[a][b];[b]gblur=sigma=22[bl];[bl][m]alphamerge[ov];[a][ov]overlay=shortest=1,{GRADE},format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", tmp, "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
                    "-af", AUDIO, "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-g", "15", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", dst], check=True)
    print("wrote", dst)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
