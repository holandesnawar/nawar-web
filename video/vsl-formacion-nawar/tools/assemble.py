#!/usr/bin/env python3
"""Assemble index.html for the Nawar VSL.

- One sub-composition host per frame (timing.json windows), track 1, abutting exactly.
- One continuous voiceover <audio> starting at vo_offset (track 10).
- Optional music bed assets/audio/music.(mp3|wav) (track 11) with fade in/out.
- SFX cues from compositions/frames/<id>.sfx.json — [{"t": frame-relative s (may be negative to
  pre-roll into the previous frame), "sfx": "<name>", "volume": 0..1}] — each on its own lane (20+).
Frames whose HTML is missing are skipped (reported), so partial assemblies preview fine.
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX_DIR = os.path.join(ROOT, "assets", "sfx")
# Film-level SFX policy (mix pass): bass impacts only on the key beats; whooshes softer overall.
IMPACT_FRAMES = {"01-hook", "02-no-valgas", "07-intentos", "11-nawar-nace", "22-clase-directo"}
TYPE_GAIN = {"whoosh-short": 0.7, "whoosh": 0.7, "pop": 0.85}

def dur_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)

def main():
    t = json.load(open(os.path.join(ROOT, "timing.json")))
    total = round(t["total"], 3)
    vo = os.path.join(ROOT, "assets", "audio", "voiceover.wav")
    vo_dur = round(dur_of(vo), 3)
    body, missing, sfx_lines = [], [], []
    sfx_n = 0
    for f in t["frames"]:
        fid = f["id"]
        path = os.path.join(ROOT, "compositions", "frames", f"{fid}.html")
        if not os.path.exists(path) or not open(path).read().strip():
            missing.append(fid)
            continue
        body.append(
            f'      <div id="el-f{fid}" class="scene" data-composition-id="{fid}" data-composition-src="compositions/frames/{fid}.html" '
            f'data-start="{f["start"]}" data-duration="{f["duration"]}" data-track-index="1" data-width="1920" data-height="1080"></div>')
        side = os.path.join(ROOT, "compositions", "frames", f"{fid}.sfx.json")
        if os.path.exists(side):
            try:
                cues = json.load(open(side))
            except Exception as e:
                print(f"WARN bad sfx sidecar {side}: {e}")
                cues = []
            for c in cues[:6]:
                name = str(c.get("sfx", "")).replace(".mp3", "")
                if name.startswith("impact-bass") and fid not in IMPACT_FRAMES:
                    continue
                src = os.path.join(SFX_DIR, f"{name}.mp3")
                if not os.path.exists(src):
                    print(f"WARN {fid}: unknown sfx {name}")
                    continue
                start = round(max(0.0, f["start"] + float(c.get("t", 0))), 3)
                d = round(min(dur_of(src), total - start), 3)
                if d <= 0.05:
                    continue
                vol = max(0.0, min(1.0, float(c.get("volume", 0.35)) * TYPE_GAIN.get(name, 1.0)))
                sfx_lines.append(f'      <audio id="el-sfx-{sfx_n}" src="assets/sfx/{name}.mp3" data-start="{start}" data-duration="{d}" '
                                 f'data-track-index="{20 + sfx_n}" data-volume="{vol}"></audio>')
                sfx_n += 1
    audio = [f'      <audio id="el-vo" src="assets/audio/voiceover.wav" data-start="{t["vo_offset"]}" data-duration="{vo_dur}" data-track-index="10" data-volume="1"></audio>']
    for ext in ("wav", "mp3", "m4a"):
        m = os.path.join(ROOT, "assets", "audio", f"music.{ext}")
        if os.path.exists(m):
            mvol = float(os.environ.get("MUSIC_VOL", "0.16"))
            audio.append(f'      <audio id="el-music" src="assets/audio/music.{ext}" data-start="0" data-duration="{total}" data-track-index="11" data-volume="{mvol}"></audio>')
            break
    html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Nawar VSL</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #07041F; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #07041F; }}
      .scene {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(body)}
{chr(10).join(audio)}
{chr(10).join(sfx_lines)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(html)
    print(f"index.html: {len(body)} frames, total {total}s, vo {vo_dur}s @ {t['vo_offset']}, sfx {sfx_n}, music {'yes' if len(audio) > 1 else 'no'}")
    if missing:
        print("missing frames:", ", ".join(missing))

if __name__ == "__main__":
    main()
