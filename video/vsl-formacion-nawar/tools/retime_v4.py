#!/usr/bin/env python3
"""Carry the built scenes onto the v4 voice take with ONE time map per scene.

Every earlier take added one more runtime shim (v2 retime, retime fix, v3 retime …). This tool folds them:
the composite of a scene's existing maps (its design time → previous take) is followed by the map previous
take → current take (the scene's words in <old_timing.json> matched to the same words in timing.json, or a
hand-made word pairing for scenes whose script changed), and the scene gets a single shim with the
composite anchors. Clip windows, the scene duration and the SFX sidecar are already in previous-take time,
so they are remapped with the second map only.

Usage: python3 tools/retime_v4.py <old_timing.json> [frame_id …]
       (default: every scene except 20/21, which tools/gen_laptop_20_21.py regenerates from timing.json)
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retime_v2 import anchors, fmap, SHIM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"20-pausa", "21-portatil"}
LABEL = "voice retime (tools/retime_v4.py): design-time cues → v4 voice cues (earlier takes folded in), piecewise linear. Design untouched."

# scenes whose words changed in v4: (old word index, new word index) pairs
PAIRS = {
    # «… impuestos, sacas adelante a tu familia.» → «… impuestos, tienes tu vida montada.»
    "04-llevas-anos": [(i, i) for i in range(7)] + [(7, 7), (8, 8), (9, 9), (11, 10)],
    # «… el médico, el colegio de tus hijos y el ayuntamiento.» → «… el médico, el ayuntamiento y tu día a día.»
    # tile 3 (now de gemeente) rides «ayuntamiento», tile 4 (now de routine) rides «día»
    "15-vocabulario": [(i, i) for i in range(9)] + [(9, 9), (13, 11), (15, 12)] + [(16 + k, 15 + k) for k in range(6)],
}

BLOCK = re.compile(r"\n[ \t]*// [^\n]*retime[^\n]*\n[ \t]*\(\(tl, A\) => \{.*?\}\)\(tl, (\[\[.*?\]\])\);", re.S)


def pairs_anchors(f1, f2, pairs):
    pts = [(0.0, 0.0)] + [(f1["words"][i]["t"], f2["words"][j]["t"]) for i, j in pairs] + [(f1["duration"], f2["duration"])]
    out = []
    for p in sorted(pts):
        if out and (p[0] <= out[-1][0] + 1e-3 or p[1] <= out[-1][1] + 1e-3):
            continue
        out.append((round(p[0], 3), round(p[1], 3)))
    return out


def inverse(F, y, lo=-5.0, hi=60.0):
    for _ in range(80):
        mid = (lo + hi) / 2
        if F(mid) < y: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def main():
    old = {f["id"]: f for f in json.load(open(sys.argv[1]))["frames"]}
    new = {f["id"]: f for f in json.load(open(os.path.join(ROOT, "timing.json")))["frames"]}
    ids = sys.argv[2:] or [k for k in new if k not in SKIP]
    for fid in ids:
        f1, f2 = old[fid], new[fid]
        G = pairs_anchors(f1, f2, PAIRS[fid]) if fid in PAIRS else anchors(f1, f2)
        D1, D2 = f1["duration"], f2["duration"]
        path = os.path.join(ROOT, "compositions", "frames", f"{fid}.html")
        html = open(path).read()
        maps = [json.loads(m.group(1)) for m in BLOCK.finditer(html)]
        html = BLOCK.sub("", html)
        # composite design time → previous take
        def F(t, n=len(maps)):
            for A in maps[:n]:
                t = fmap(A, t)
            return t
        xs = set()
        for k, A in enumerate(maps):
            xs |= {round(inverse(lambda t: F(t, k), a[0]), 4) for a in A}
        xs |= {round(inverse(F, g[0]), 4) for g in G}
        H = []
        for x in sorted(xs):
            p = (round(x, 3), round(fmap(G, F(x)), 3))
            if H and (p[0] <= H[-1][0] + 1e-3 or p[1] <= H[-1][1] + 1e-3):
                continue
            H.append(p)
        reg = re.search(r'\n(\s*)window\.__timelines\["' + re.escape(fid) + r'"\]\s*=\s*tl', html)
        if not reg:
            sys.exit(f"{fid}: registration line not found")
        shim = SHIM.replace("v2 retime (tools/retime_v2.py): v1 voice cues → v2 voice cues, piecewise linear. Design untouched.", LABEL)
        html = html[:reg.start()] + "\n" + shim.replace("__A__", json.dumps(H)).rstrip("\n") + html[reg.start():]
        # clip windows + scene duration (previous-take time → current take)
        def clip(m):
            s, d = float(m.group(1)), float(m.group(2))
            ns = 0.0 if s == 0 else round(fmap(G, s), 3)
            ne = D2 if abs(s + d - D1) < 0.03 else min(round(fmap(G, s + d), 3), D2)
            return f'data-start="{ns:g}" data-duration="{round(ne - ns, 3):g}"'
        html = re.sub(r'data-start="([0-9.]+)" data-duration="([0-9.]+)"', clip, html)
        html = re.sub(r'(<div id="root"[^>]*data-duration=")[0-9.]+(")', lambda m: f"{m.group(1)}{D2:g}{m.group(2)}", html)
        open(path, "w").write(html)
        side = os.path.join(ROOT, "compositions", "frames", f"{fid}.sfx.json")
        if os.path.exists(side):
            cues = json.load(open(side))
            for c in cues:
                c["t"] = round(fmap(G, float(c.get("t", 0))), 3)
            json.dump(cues, open(side, "w"), indent=1)
        print(f"{fid:<18} {D1:6.2f} → {D2:6.2f}  folded {len(maps)} map(s), {len(H)} anchors")


if __name__ == "__main__":
    main()
