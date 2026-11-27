#!/usr/bin/env python3
"""Carry built scenes onto a new voice take (scene windows may change length).

Usage: python3 tools/retime_stack.py <old_timing.json> <frame_id> [frame_id …]
Matches the scene's words in <old_timing.json> with the same words in the current timing.json, then
injects one more piecewise-linear time-map shim (tools/retime_v2.py mechanics) before the scene registers
its timeline, rewrites the scene duration on the root / full-length clips, remaps the other clip windows
and the SFX sidecar. Shims stack, so a scene can be carried across several voice takes.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retime_v2 import anchors, fmap, SHIM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    old = {f["id"]: f for f in json.load(open(sys.argv[1]))["frames"]}
    new = {f["id"]: f for f in json.load(open(os.path.join(ROOT, "timing.json")))["frames"]}
    for fid in sys.argv[2:]:
        f1, f2 = old[fid], new[fid]
        A = anchors(f1, f2); D1, D2 = f1["duration"], f2["duration"]
        path = os.path.join(ROOT, "compositions", "frames", f"{fid}.html")
        html = open(path).read()
        def clip(m):
            s, d = float(m.group(1)), float(m.group(2))
            ns = 0.0 if s == 0 else round(fmap(A, s), 3)
            ne = D2 if abs(s + d - D1) < 0.03 else min(round(fmap(A, s + d), 3), D2)
            return f'data-start="{ns:g}" data-duration="{round(ne - ns, 3):g}"'
        html = re.sub(r'data-start="([0-9.]+)" data-duration="([0-9.]+)"', clip, html)
        html = re.sub(r'(<div id="root"[^>]*data-duration=")[0-9.]+(")', lambda m: f"{m.group(1)}{D2:g}{m.group(2)}", html)
        reg = re.search(r'\n(\s*)window\.__timelines\["' + re.escape(fid) + r'"\]\s*=\s*tl', html)
        if not reg:
            sys.exit(f"{fid}: registration line not found")
        shim = SHIM.replace("v2 retime (tools/retime_v2.py): v1 voice cues → v2 voice cues", "v3 retime (tools/retime_stack.py): previous voice cues → v3 voice cues")
        html = html[:reg.start()] + "\n" + shim.replace("__A__", json.dumps(A)).rstrip("\n") + html[reg.start():]
        open(path, "w").write(html)
        side = os.path.join(ROOT, "compositions", "frames", f"{fid}.sfx.json")
        if os.path.exists(side):
            cues = json.load(open(side))
            for c in cues:
                c["t"] = round(fmap(A, float(c.get("t", 0))), 3)
            json.dump(cues, open(side, "w"), indent=1)
        print(f"{fid:<18} {D1:6.2f} → {D2:6.2f}  anchors {len(A):3d}")

if __name__ == "__main__":
    main()
