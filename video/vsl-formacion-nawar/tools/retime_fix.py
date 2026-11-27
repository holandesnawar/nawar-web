#!/usr/bin/env python3
"""Re-sync already-built scenes after word timings were corrected (same voice, same scene windows).

Usage: python3 tools/retime_fix.py <old_timing.json> <frame_id> [frame_id …]
Compares the scene's word cues in <old_timing.json> with the current timing.json and injects a
piecewise-linear time-map shim (same mechanics as tools/retime_v2.py) right before the scene registers
its timeline, plus remaps its clip windows and SFX sidecar. Shims stack: each run adds one more block.
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
        assert abs(f1["duration"] - f2["duration"]) < 1e-6, f"{fid}: scene window changed — rebuild instead"
        A = anchors(f1, f2)
        path = os.path.join(ROOT, "compositions", "frames", f"{fid}.html")
        html = open(path).read()
        def clip(m):
            s, d = float(m.group(1)), float(m.group(2))
            if s == 0 and abs(d - f2["duration"]) < 0.02:
                return m.group(0)
            ns = round(fmap(A, s), 3); ne = min(round(fmap(A, s + d), 3), f2["duration"])
            return f'data-start="{ns:g}" data-duration="{round(ne - ns, 3):g}"'
        html = re.sub(r'data-start="([0-9.]+)" data-duration="([0-9.]+)"', clip, html)
        reg = re.search(r'\n(\s*)window\.__timelines\["' + re.escape(fid) + r'"\]\s*=\s*tl', html)
        if not reg:
            sys.exit(f"{fid}: registration line not found")
        shim = SHIM.replace("v2 retime (tools/retime_v2.py): v1 voice cues → v2 voice cues", "retime fix (tools/retime_fix.py): corrected word cues")
        html = html[:reg.start()] + "\n" + shim.replace("__A__", json.dumps(A)).rstrip("\n") + html[reg.start():]
        open(path, "w").write(html)
        side = os.path.join(ROOT, "compositions", "frames", f"{fid}.sfx.json")
        if os.path.exists(side):
            cues = json.load(open(side))
            for c in cues:
                c["t"] = round(fmap(A, float(c.get("t", 0))), 3)
            json.dump(cues, open(side, "w"), indent=1)
        print(fid, "anchors", A)

if __name__ == "__main__":
    main()
