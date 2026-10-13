#!/usr/bin/env python3
"""Camera B: the close-up «second camera» cut from take 1 (UGC #2, v2).

She has to look into the lens in every shot, and the side take (UGC.POV2) has her looking off camera, so the
change of point of view is a close-up of the facing take: ZOOM× on her face, recomposed (not a centred zoom) so the
eyes sit near the upper third and the lav mic stays above the caption band. It is rendered here with ffmpeg
(lanczos + a light luma unsharp) instead of being scaled in the browser, so it keeps up with camera A in sharpness.
Same frames, same timestamps and the same audio as take-1.mp4, so a shot can switch file without moving in time.

  python3 tools/cam_b.py            # assets/video/take-1.mp4 → assets/video/take-1-b.mp4
"""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZOOM = 1.44
CROP_W, CROP_H = 750, 1334      # 1080×1920 / ZOOM, even sizes
CROP_X, CROP_Y = 166, 310       # face (≈540, 720 in the take) lands at ≈(539, 590); the frame lifts ~130 px


def face_on_screen(face):
    """where a point of the take (e.g. her face) lands in camera B."""
    return (round((face[0] - CROP_X) * 1080 / CROP_W), round((face[1] - CROP_Y) * 1920 / CROP_H))


def main():
    src = os.path.join(ROOT, "assets", "video", "take-1.mp4")
    out = os.path.join(ROOT, "assets", "video", "take-1-b.mp4")
    vf = f"crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y},scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-g", "15", "-r", "30", "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    print("camera B →", out)


if __name__ == "__main__":
    main()
