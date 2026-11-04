#!/usr/bin/env python3
"""×4 upscale of the ad's frames (512×288 → 2048×1152) with Real-ESRGAN «realesr-general-x4v3» (ONNX, CPU; see
tools/esrgan_onnx.py), only over the part the reel uses. Written losslessly enough (x264 CRF 10) to .raw/up.mp4, one frame
per source frame (25 fps); tools/frame.py crops the 9:16 window out of it.
  python3 tools/upscale.py [first_frame] [last_frame]
"""
import os, subprocess, sys, time
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F0, F1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (123, 993)


def main():
    import onnxruntime as ort
    s = ort.InferenceSession(os.path.join(ROOT, ".raw", "esrgan-x4v3.onnx"), providers=["CPUExecutionProvider"])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, ".raw", "suarez.mp4"), "-vf",
                          f"select=between(n\\,{F0}\\,{F1})", "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 288, 512, 3)
    assert len(fr) == F1 - F0 + 1, len(fr)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "2048x1152", "-r", "25",
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv444p",
                            os.path.join(ROOT, ".raw", "up.mp4")], stdin=subprocess.PIPE)
    t0 = time.time()
    for k, f in enumerate(fr):
        y = s.run(None, {"input": (f.astype(np.float32) / 255).transpose(2, 0, 1)[None]})[0]
        enc.stdin.write((y[0].transpose(1, 2, 0).clip(0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        if k % 100 == 0:
            print(f"  {k}/{len(fr)}  {time.time() - t0:.0f}s", flush=True)
    enc.stdin.close(); enc.wait(); assert enc.returncode == 0
    print(f"up.mp4: source frames {F0}–{F1} ×4 in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
