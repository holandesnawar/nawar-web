#!/usr/bin/env python3
"""Lint + snapshot ONE frame in isolation, so a frame worker can see what it built.

Usage:
  python3 tools/preview_frame.py <frame_id> [--at 0.5,1.2,...] [--every 0.5]

Builds .preview/<frame_id>/ (an index.html hosting only this frame for its full duration, with
symlinks to the project's assets/ and compositions/), runs `hyperframes lint` on it, then
`hyperframes snapshot` at the requested times (default: just after every word cue + the end).
Prints the lint result and the PNG / contact-sheet paths. Read the contact sheet with your image
viewer (the Read tool) and fix what you see.
"""
import argparse, json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, HYPERFRAMES_BROWSER_PATH="/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
           HYPERFRAMES_SKIP_SKILLS="1")

INDEX = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #0C0C1E; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0C0C1E; }}
      .scene {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
      <div id="el-{fid}" class="scene" data-composition-id="{fid}" data-composition-src="compositions/frames/{fid}.html" data-start="0" data-duration="{dur}" data-track-index="1" data-width="1920" data-height="1080"></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frame_id")
    ap.add_argument("--at", default=None, help="comma-separated frame-relative seconds")
    ap.add_argument("--every", type=float, default=None, help="snapshot every N seconds instead")
    a = ap.parse_args()
    timing = json.load(open(os.path.join(ROOT, "timing.json")))
    fr = next((f for f in timing["frames"] if f["id"] == a.frame_id), None)
    if fr is None:
        sys.exit(f"unknown frame id {a.frame_id}")
    src = os.path.join(ROOT, "compositions", "frames", f"{a.frame_id}.html")
    if not os.path.exists(src):
        sys.exit(f"missing {src}")
    dur = fr["duration"]
    pdir = os.path.join(ROOT, ".preview", a.frame_id)
    if os.path.isdir(pdir):
        shutil.rmtree(pdir)
    os.makedirs(pdir)
    # hard-link assets (no copy cost, real paths inside the preview dir — the bundler ignores
    # symlinked files); copy compositions fresh so the newest edits are always previewed
    subprocess.run(["cp", "-al", os.path.join(ROOT, "assets"), os.path.join(pdir, "assets")], check=True)
    shutil.copytree(os.path.join(ROOT, "compositions"), os.path.join(pdir, "compositions"))
    open(os.path.join(pdir, "index.html"), "w").write(INDEX.format(dur=dur, fid=a.frame_id))
    open(os.path.join(pdir, "hyperframes.json"), "w").write(open(os.path.join(ROOT, "hyperframes.json")).read())
    if a.at:
        times = [float(x) for x in a.at.split(",") if x.strip()]
    elif a.every:
        n = int(dur / a.every)
        times = [round(min(dur - 0.04, (i + 1) * a.every), 2) for i in range(n)]
    else:
        cues = [w["t"] for w in fr["words"]]
        times = sorted({round(min(dur - 0.04, t + 0.3), 2) for t in cues} | {round(dur - 0.05, 2)})
        # thin to at most 16 shots, always keeping the last
        while len(times) > 16:
            times = times[::2] + ([times[-1]] if times[-1] not in times[::2] else [])
    times = [t for t in times if 0 <= t < dur]
    print(f"frame {a.frame_id}: duration {dur}s, snapshots at {times}")
    lint = subprocess.run(["npx", "hyperframes", "lint", pdir], cwd=ROOT, env=ENV, capture_output=True, text=True, timeout=300)
    out = (lint.stdout + lint.stderr).strip().splitlines()
    print("---- lint ----")
    print("\n".join(l for l in out if l.strip())[-3000:])
    snapdir = os.path.join(pdir, "snaps")
    snap = subprocess.run(["npx", "hyperframes", "snapshot", pdir, "--at", ",".join(str(t) for t in times), "--no-end",
                           "-o", snapdir, "--timeout", "15000"], cwd=ROOT, env=ENV, capture_output=True, text=True, timeout=900)
    print("---- snapshot ----")
    print("\n".join((snap.stdout + snap.stderr).strip().splitlines()[-25:]))
    sheets = sorted(p for p in os.listdir(snapdir) if p.startswith("contact-sheet")) if os.path.isdir(snapdir) else []
    for p in sheets:
        print(f"CONTACT SHEET: {os.path.join(snapdir, p)}")
    pngs = sorted(p for p in os.listdir(snapdir) if p.endswith(".png")) if os.path.isdir(snapdir) else []
    for p in pngs:
        print(f"PNG: {os.path.join(snapdir, p)}")

if __name__ == "__main__":
    main()
