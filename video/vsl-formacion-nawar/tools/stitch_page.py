#!/usr/bin/env python3
"""Rebuild the platform's «Inicio» dashboard as ONE tall page image from the screen recording.

The owner wants the laptop in 14-supervivencia to start at the top of the page and then scroll, slowly,
to the interesting part (not to land at the bottom as the raw recording does). The recording scrolls too
fast, so the page is stitched instead: every frame of the scroll (media 0.53–5.0 s, already at the top)
is matched to the previous one (vertical shift of the main column), each frame is placed at its scroll
offset, and every row is the per-pixel median of the frames that saw it (the mouse pointer drops out).
The fixed sidebar is the median of all frames (drops the link-hover bubble and the sticky jitter at the top).

Outputs (half the recording's resolution, i.e. a 1280 × 688 viewport):
  assets/img/ui-inicio-sidebar.png   230 × 688
  assets/img/ui-inicio-page.png      1050 × (688 + total scroll)
Run: python3 tools/stitch_page.py
"""
import os, subprocess
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "video", "inicio-home.mp4")
W, H, X0 = 1280, 688, 230            # viewport (half-res) and the sidebar's right edge
T0, T1, K0 = 0.4, 5.0, 4             # decode window; frame K0 (0.53 s) is the first one at the very top


def main():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(T0), "-i", SRC, "-t", str(T1 - T0), "-vf",
                          f"scale={W}:-2:flags=lanczos", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    F = np.frombuffer(raw[: n * W * H * 3], np.uint8).reshape(n, H, W, 3)[K0:]
    g = F[:, :, X0 + 10: W - 25].mean(3)
    Y = [0]
    for k in range(1, len(F)):
        a, b = g[k - 1], g[k]
        errs = [np.abs(a[s + 40: H - 40] - b[40: H - 40 - s]).mean() for s in range(0, 160)]
        Y.append(Y[-1] + int(np.argmin(errs)))
    Y = np.array(Y)
    CH = H + int(Y[-1])
    page = np.zeros((CH, W - X0, 3), np.uint8)
    for y0 in range(0, CH, 48):
        y1 = min(CH, y0 + 48)
        stack = [f[y0 - Y[k]: y1 - Y[k], X0:] for k, f in enumerate(F) if y0 - Y[k] >= 0 and y1 - Y[k] <= H]
        if stack:
            page[y0:y1] = np.median(np.stack(stack), axis=0).astype(np.uint8)
        else:                                    # the last rows: only partially covered frames
            k = len(F) - 1; a = y0 - Y[k]
            page[y0:y1] = F[k][a: a + (y1 - y0), X0:]
    side = np.median(F[:, :, :X0], axis=0).astype(np.uint8)
    out = os.path.join(ROOT, "assets", "img")
    Image.fromarray(side).save(os.path.join(out, "ui-inicio-sidebar.png"))
    Image.fromarray(page).save(os.path.join(out, "ui-inicio-page.png"))
    print(f"frames {len(F)}  total scroll {Y[-1]} px  page {page.shape[1]}x{page.shape[0]}")


if __name__ == "__main__":
    main()
