#!/usr/bin/env python3
"""Retime the v1 scenes (01–19) to the v2 voice without touching their design.

For each scene: word cues of the v1 voice (timing_v1.json) are matched to the same words in the v2 voice
(timing.json); the matches give a piecewise-linear time map v1 → v2. A small runtime shim is injected right
before the scene registers its GSAP timeline: every top-level child is moved to its mapped start; long
moves (≥ 1 s, e.g. camera drifts) are stretched so they still end where they should. Clip windows
(data-start/data-duration), the scene duration and the SFX sidecar cues are remapped with the same map.
Sources: compositions/frames_v1/ → output: compositions/frames/.
"""
import difflib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "compositions", "frames_v1")
DST = os.path.join(ROOT, "compositions", "frames")
IDS = ["01-hook", "02-no-valgas", "03-tres-minutos", "04-llevas-anos", "05-situaciones", "06-atascado", "07-intentos",
       "08-app-silencio", "09-preguntas", "10-escuelas", "11-nawar-nace", "12-metodo", "13-tres-fases", "14-supervivencia",
       "15-vocabulario", "16-estructura", "17-traducir", "18-sonidos", "19-delatan"]
# 01–03 (re-grounded on blue) and 17 (new line) were hand-edited after the retime: only touched when named explicitly
HAND_EDITED = {"01-hook", "02-no-valgas", "03-tres-minutos", "17-traducir"}
norm = lambda s: s.lower().strip(",.¿?¡!…:;")

def anchors(f1, f2):
    a = [norm(w["text"]) for w in f1["words"]]; b = [norm(w["text"]) for w in f2["words"]]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    pts = [(0.0, 0.0)]
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            w1, w2 = f1["words"][blk.a + k], f2["words"][blk.b + k]
            pts.append((w1["t"], w2["t"]))
    pts.append((f1["duration"], f2["duration"]))
    out = []
    for p in sorted(pts):
        if out and (p[0] <= out[-1][0] + 1e-3 or p[1] <= out[-1][1] + 1e-3):
            continue
        out.append((round(p[0], 3), round(p[1], 3)))
    return out

def fmap(A, t):
    if t <= A[0][0]:
        return t - A[0][0] + A[0][1]
    for (a0, b0), (a1, b1) in zip(A, A[1:]):
        if t <= a1:
            return b0 + (t - a0) * (b1 - b0) / (a1 - a0)
    return A[-1][1] + (t - A[-1][0])

SHIM = """      // v2 retime (tools/retime_v2.py): v1 voice cues → v2 voice cues, piecewise linear. Design untouched.
      ((tl, A) => {
        const f = (t) => {
          if (t <= A[0][0]) return t - A[0][0] + A[0][1];
          for (let i = 1; i < A.length; i++) if (t <= A[i][0]) { const [a0, b0] = A[i - 1], [a1, b1] = A[i]; return b0 + (t - a0) * (b1 - b0) / (a1 - a0); }
          const [a, b] = A[A.length - 1]; return b + (t - a);
        };
        tl.getChildren(false, true, true).forEach((c) => {
          const s = c.startTime(), d = c.duration(), ns = f(s);
          if (d >= 1.0 && !(c.vars && c.vars.repeat)) {
            const nd = Math.max(0.05, f(s + d) - ns);
            if (c instanceof gsap.core.Timeline) c.timeScale((c.timeScale() || 1) * d / nd); else c.duration(nd);
          }
          c.startTime(ns);
        });
      })(tl, __A__);
"""

def main(only=None):
    t1 = {f["id"]: f for f in json.load(open(os.path.join(ROOT, "timing_v1.json")))["frames"]}
    t2 = {f["id"]: f for f in json.load(open(os.path.join(ROOT, "timing.json")))["frames"]}
    report = {}
    for fid in IDS:
        if (only and fid not in only) or (not only and fid in HAND_EDITED):
            continue
        f1, f2 = t1[fid], t2[fid]
        A = anchors(f1, f2)
        html = open(os.path.join(SRC, f"{fid}.html")).read()
        D1, D2 = f1["duration"], f2["duration"]
        # scene duration on the root + clips: remap windows
        def clip(m):
            s, d = float(m.group(1)), float(m.group(2))
            ns = 0.0 if s == 0 else round(fmap(A, s), 3)
            ne = D2 if abs(s + d - D1) < 0.02 else round(fmap(A, s + d), 3)
            return f'data-start="{ns:g}" data-duration="{round(min(ne, D2) - ns, 3):g}"'
        html = re.sub(r'data-start="([0-9.]+)" data-duration="([0-9.]+)"', clip, html)
        html = re.sub(r'(<div id="root"[^>]*data-duration=")[0-9.]+(")', lambda m: f"{m.group(1)}{D2:g}{m.group(2)}", html)
        reg = re.search(r'\n(\s*)window\.__timelines\["' + re.escape(fid) + r'"\]\s*=\s*tl', html)
        if not reg:
            sys.exit(f"{fid}: registration line not found")
        html = html[:reg.start()] + "\n" + SHIM.replace("__A__", json.dumps(A)).rstrip("\n") + html[reg.start():]
        open(os.path.join(DST, f"{fid}.html"), "w").write(html)
        side = os.path.join(SRC, f"{fid}.sfx.json")
        if os.path.exists(side):
            cues = json.load(open(side))
            for c in cues:
                c["t"] = round(fmap(A, float(c.get("t", 0))), 3)
            json.dump(cues, open(os.path.join(DST, f"{fid}.sfx.json"), "w"), indent=1)
        report[fid] = {"v1": D1, "v2": D2, "anchors": len(A)}
        print(f"{fid:<18} {D1:6.2f} → {D2:6.2f}  anchors {len(A):3d}  max |shift| {max(abs(a - b) for a, b in A):.2f}s")

if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
