#!/usr/bin/env python3
"""Generate the UGC ad #2 from edit.json: index.html (the girl — two cameras, take 1 front and take 2 side, her
framing, audio), one full-screen
insert per explanation (compositions/ins-NN.html, built by tools/inserts/ins_NN.py), the «haz clic» button of the
ending (compositions/outro.html) and the captions (compositions/captions.html).

Same language as UGC #1 (tools/common.py): while she talks to camera nothing covers her but the captions; when
she explains, the picture cuts to a full-screen VSL-style insert and back. The ad opens with a zoom-out on her face.

    python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
    python3 tools/gen.py --solo ins-03 --out /tmp/x   # one insert alone at t=0 (+ its captions), to snapshot it
"""
import argparse, importlib, json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *          # noqa: F401,F403  (ED, INS, WORDS, TOTAL, RATE, PAL, comp, icon, norm, at, …)

INSERT_MODULES = [f"ins_{k:02d}" for k in range(1, len(ED["inserts"]) + 1)]


def build_inserts(only=None):
    out = []
    for name in INSERT_MODULES:
        iid = "ins-" + name[-2:]
        if only and iid != only:
            continue
        mod = importlib.import_module(f"inserts.{name}")
        html, sfx = mod.build()
        out.append((iid, html, sfx))
    return out


# ============================================================================== outro · she stays on screen, a «haz clic» button under her
def outro():
    """From «haz clic…» to the end she stays on screen (then held on her last smile) and a glossy blue button
    «MATRÍCULA» pops under her face the moment she says «haz clic»; a cursor clicks it on «clic»."""
    P = "o"; t0 = ED["outro"]; d = round(TOTAL - t0, 3)
    def wcue(word, k=0):
        hits = [w for w in WORDS if w["t"] >= t0 and norm(w["text"]) == norm(word)]
        return round(hits[k]["t"] - t0, 3)
    c = dict(HAZ=wcue("haz"), CLIC=wcue("clic"), REL=wcue("rellena"), END=round(ED["speech_end"] - t0, 3))
    css = """
    #o-wrap { position: absolute; left: 190px; top: 1150px; width: 700px; height: 132px; }
    #o-glow { position: absolute; left: -40px; top: -30px; width: 780px; height: 192px; border-radius: 96px;
      background: radial-gradient(ellipse at 50% 50%, rgba(77,163,255,0.55) 0%, rgba(77,163,255,0) 70%); }
    #o-btn { position: absolute; left: 0; top: 0; width: 700px; height: 132px; border-radius: 66px; overflow: hidden;
      background: linear-gradient(90deg, #0a52d4 0%, #1b74f2 55%, #4a98fb 100%);
      box-shadow: inset 0 0 0 3px rgba(255,255,255,0.55), inset 0 -10px 24px rgba(4,0,80,0.25), 0 20px 50px rgba(11,109,240,0.5); }
    #o-gloss { position: absolute; left: 22px; top: 8px; width: 656px; height: 52px; border-radius: 30px;
      background: linear-gradient(180deg, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0) 100%); }
    #o-shine { position: absolute; left: -240px; top: 0; width: 180px; height: 132px;
      background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.45) 50%, rgba(255,255,255,0) 100%); }
    #o-label { position: absolute; left: 0; top: 0; width: 700px; height: 132px; display: flex; align-items: center; justify-content: center;
      font-weight: 900; font-size: 74px; line-height: 1; letter-spacing: -0.01em; color: #FFFFFF; white-space: nowrap; padding-top: 4px; box-sizing: border-box;
      text-shadow: 0 0 18px rgba(255,255,255,0.55), 0 3px 0 rgba(0,30,120,0.35); }
    #o-rip { position: absolute; left: 697px; top: 1207px; width: 90px; height: 90px; border-radius: 50%; border: 5px solid #FFFFFF; box-sizing: border-box; opacity: 0; }
    #o-cur { position: absolute; left: 738px; top: 1248px; width: 60px; height: 78px; }
    #o-cur svg { display: block; width: 60px; height: 78px; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.35)); }
"""
    body = f"""    <div id="o-wrap">
      <div id="o-glow"></div>
      <div id="o-btn"><div id="o-gloss"></div><div id="o-shine"></div><div id="o-label">MATRÍCULA</div></div>
    </div>
    <div id="o-rip"></div>
    <div id="o-cur">{icon('cursor')}</div>"""
    js = """
      tl.fromTo(q("wrap"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.36, ease: "back.out(1.8)" }, «HAZ» - 0.06);
      tl.fromTo(q("glow"), { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, «HAZ»);
      tl.fromTo(q("cur"), { opacity: 0, x: 150, y: 170 }, { opacity: 1, x: 0, y: 0, duration: 0.34, ease: "power3.out" }, «HAZ» + 0.04);
      tl.to(q("btn"), { scale: 0.95, duration: 0.07, ease: "power2.out" }, «CLIC» + 0.02);
      tl.to(q("btn"), { scale: 1, duration: 0.3, ease: "back.out(2.6)" }, «CLIC» + 0.09);
      tl.to(q("cur"), { scale: 0.86, duration: 0.07, ease: "power2.out" }, «CLIC» + 0.02);
      tl.to(q("cur"), { scale: 1, duration: 0.2, ease: "power2.out" }, «CLIC» + 0.09);
      tl.fromTo(q("rip"), { scale: 0.3, opacity: 0.9 }, { scale: 1.7, opacity: 0, duration: 0.45, ease: "power2.out" }, «CLIC» + 0.02);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1120, duration: 0.7, ease: "power2.inOut" }, «REL»);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1120, duration: 0.7, ease: "power2.inOut", immediateRender: false }, «END» + 0.25);
      tl.fromTo(q("wrap"), { scale: 1 }, { keyframes: [{ scale: 1.04, duration: 0.25, ease: "power1.inOut" }, { scale: 1, duration: 0.25, ease: "power1.inOut" },
        { scale: 1.04, duration: 0.25, ease: "power1.inOut" }, { scale: 1, duration: 0.25, ease: "power1.inOut" }], immediateRender: false }, «END» + 0.1);
"""
    sfx = [(c["HAZ"] - 0.06, "pop", 0.2), (c["CLIC"] + 0.02, "click", 0.3)]
    return comp("outro", d, P, css, body, js, c), t0, d, sfx


# ============================================================================== captions (clean, white, no box)
SHOW = {"cuatro": "4", "nueve": "9", "diez": "10"}


def ground_at(t):
    for i in ED["inserts"]:
        if i["start"] <= t < i["start"] + i["duration"]:
            return i["ground"]
    return "girl"


def captions(window=None):
    """Word-by-word captions in pages of ≤3 words; pages never straddle a cut (girl ↔ insert, front ↔ side camera, jump cut).
    window=(a, b): only the pages inside it, re-timed to start at a (solo previews of one insert)."""
    P = "cap"
    bounds = sorted({0.0, ED["outro"]} | {s["start"] for s in ED["shots"]} | {i["start"] for i in ED["inserts"]}
                    | {round(i["start"] + i["duration"], 3) for i in ED["inserts"]})
    pages, cur = [], []
    ends = [round(i["start"] + i["duration"], 3) for i in ED["inserts"]]
    def region(t):   # a word that starts in the last 0.12 s of a graphic belongs to the girl right after it
        t = next((e for e in ends if e - 0.12 <= t < e), t)
        return max(b for b in bounds if b <= t + 1e-6)
    for w in WORDS:
        txt = SHOW.get(norm(w["text"]), w["text"]) + (w.get("punct") or "").replace(":", "").replace(";", "")
        if norm(w["text"]) == "estas" and not txt.startswith("¿"):
            txt = "¿" + txt
        if cur and region(w["t"]) != region(cur[0]["t"]):
            pages.append(cur); cur = []
        cur.append(dict(w, show=txt))
        first = not pages
        brk = any(ch in (w.get("punct") or "") for ch in ".?!,:") or len(cur) >= 3 or sum(len(x["show"]) for x in cur) >= 16
        if first:   # the very first page («Si tienes un ordenador») is on screen from frame 0
            brk = norm(w["text"]) == "ordenador"
        if brk:
            pages.append(cur); cur = []
    if cur: pages.append(cur)
    off, total = 0.0, TOTAL
    if window:
        off, total = window[0], window[1] - window[0]
        pages = [pg for pg in pages if window[0] - 1e-6 <= pg[0]["t"] < window[1]]
    body, js = [], []
    end_all = round(ED["speech_end"] + 0.12, 3)
    for k, pg in enumerate(pages):
        r0 = region(pg[0]["t"])                                            # the section the page belongs to
        t0 = 0.0 if (k == 0 and not window) else max(0.0, pg[0]["t"] - 0.03 - off, r0 - off)
        t1 = (pages[k + 1][0]["t"] - 0.03 - off) if k + 1 < len(pages) else min(end_all - off, total)
        cut = min([x for x in bounds if x > r0 + 1e-6], default=None)           # a page leaves with its section
        if cut is not None and cut - off < t1:
            t1 = round(cut - off, 3)
        g = ground_at(r0 + 0.01)
        spans = " ".join('<span id="cap-w%d-%d" class="cap-w">%s</span>' % (k, i, w["show"]) for i, w in enumerate(pg))
        up = " cap-up" if pg[0]["t"] >= ED["outro"] - 1e-3 else ""      # above the «haz clic» button
        body.append('    <div id="cap-g%d" class="cap-g cap-gr-%s%s">%s</div>' % (k, g, up, spans))
        js.append('      tl.fromTo(q("g%d"), { opacity: %d }, { opacity: 1, duration: 0.01 }, %.3f);' % (k, 1 if (k == 0 and not window) else 0, t0))
        js.append('      tl.set(q("g%d"), { opacity: 0 }, %.3f);' % (k, t1))
        for i, w in enumerate(pg if (k or window) else []):
            a = max(t0, w["t"] - 0.03 - off)
            js.append('      tl.fromTo(q("w%d-%d"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.1, ease: "power2.out" }, %.3f);' % (k, i, a))
    css = """
    .cap-g { position: absolute; left: 90px; top: 1268px; width: 900px; height: 150px; display: flex; flex-wrap: wrap; align-content: center;
      justify-content: center; column-gap: 18px; row-gap: 0px; opacity: 0; }
    .cap-up { top: 984px; }
    .cap-w { display: inline-block; font-weight: 800; font-size: 66px; line-height: 76px; letter-spacing: -0.015em; white-space: nowrap; }
    .cap-gr-girl .cap-w { color: #FFFFFF; text-shadow: 0 3px 14px rgba(0,0,0,0.55), 0 1px 3px rgba(0,0,0,0.45); }
    .cap-gr-blue .cap-w { color: #FFFFFF; text-shadow: 0 3px 16px rgba(4,0,40,0.45); }
    .cap-gr-paper .cap-w { color: «INK»; }
"""
    return comp("captions", total, P, css, "\n".join(body), "\n".join(js) + "\n"), len(pages)


# ============================================================================== the girl's framing
def zooms():
    """coordinate-target-zoom on the girl (origin = her face in each camera): tweens (time, duration, ease, to,
    from|None, wrapper). The ad opens tight on her face and zooms out fast to reveal the laptop («Si tienes un
    ordenador…»). After that every stretch of a camera inside a girl section starts at its own framing (the cuts hide
    the change) with a slow push and a punch on a key word; a jump cut inside a section (the take's own cuts, see
    edit.py JUMPS) changes framing too. #zw1 = front camera (take 1, the whole ad), #zw2 = side
    camera (take 2, the ending only)."""
    G = ED["girl"]; Z = []
    def push(t0, t1, s0, s1, sel):
        Z.append((round(t0, 3), round(t1 - t0 - 0.004, 3), "none", {"scale": round(s1, 3)}, {"scale": round(s0, 3)}, sel))   # ends just before the next tween
    def punch(word, s, sel, k=0, d=0.22, ease="power3.out"):
        Z.append((round(at(word, k) - 0.05, 3), d, ease, {"scale": s}, None, sel))
    wrap = lambda sh: "#zw" + sh["take"]
    shots = ED["shots"]
    # intro: tight on her face → zoom out to reveal the laptop, then push and punch on «neerlandés»
    Z.append((0.0, 0.75, "power3.out", {"scale": 1.02}, {"scale": 1.36}, "#zw1"))
    push(0.75, at("neerlandes") - 0.05, 1.02, 1.06, "#zw1"); punch("neerlandes", 1.14, "#zw1")
    PUNCH = {"bajan": 1.12}                                     # front camera, on the key word
    LOOK = {"1": [1.08, 1.0, 1.12, 1.02, 1.14, 1.0, 1.1, 1.04], "2": [1.0, 1.06, 1.03, 1.08]}   # start framings, cycling per
                                                                                 # camera; neighbours differ, so a jump cut reads
    used = {"1": 0, "2": 0}
    for g in G[:-1]:                                            # (the CTA has its own moves below)
        for sh in shots:
            a, b = max(g["start"], sh["start"]), min(g["end"], sh["start"] + sh["duration"])
            if b - a <= 0.05 or sh["n"] == 1:                   # shot 1 = the hook, done above
                continue
            tk = sh["take"]; s0 = LOOK[tk][used[tk] % len(LOOK[tk])]; used[tk] += 1
            pw = [w for w in PUNCH if tk == "1" and a <= at(w) < b]
            if pw:
                push(a, at(pw[0]) - 0.05, s0, s0 + 0.02, wrap(sh)); punch(pw[0], PUNCH[pw[0]], wrap(sh))
            else:
                push(a, b, s0, s0 + 0.04, wrap(sh))
    # the CTA: front camera («¿Estás listo…?» lands on a punch; «haz clic en el botón de aquí abajo,»), then the side
    # camera she now looks into; the jump cut over her pause hides behind a reframe
    cta = [s for s in shots if s["start"] >= G[-1]["start"] - 1e-3]
    Z.append((G[-1]["start"], 0.26, "power3.out", {"scale": 1.15}, {"scale": 1.02}, wrap(cta[0])))
    o = ED["outro"]; push(o + 0.2, cta[0]["start"] + cta[0]["duration"], 1.15, 1.17, wrap(cta[0]))
    for k, sh in enumerate(cta[1:]):
        end = TOTAL if sh is shots[-1] else sh["start"] + sh["duration"]
        push(sh["start"], end, 1.0 + 0.06 * k, 1.03 + 0.06 * k, wrap(sh))
    return Z


def media_len(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return round(float(out.strip()), 3)


HEAD = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #120081; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #120081; }
      .shot { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
      .zw { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; will-change: transform; }
      .zw video, .zw img { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    </style>
  </head>
"""


def index(sfx_all, out_t0, out_d):
    hosts = []
    for k, i in enumerate(ED["inserts"]):
        hosts.append(f'    <div id="{i["id"]}" data-composition-id="{i["id"]}" data-composition-src="compositions/{i["id"]}.html" data-start="{i["start"]}" data-duration="{i["duration"]}" data-track-index="{10 + k}" data-width="1080" data-height="1920"></div>')
    hosts.append(f'    <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" data-start="{out_t0}" data-duration="{out_d}" data-track-index="20" data-width="1080" data-height="1920"></div>')
    hosts.append(f'    <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="21" data-width="1080" data-height="1920"></div>')
    auds = [f'    <audio id="music" src="assets/audio/music-bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="22" data-volume="1"></audio>']
    for k, (t, name, vol, *rest) in enumerate(sfx_all):
        src = f"assets/sfx/{name}.mp3"
        dd = min(rest[0] if rest else 99, media_len(os.path.join(ROOT, src)))
        dd = round(min(dd, TOTAL - t), 3)
        auds.append(f'    <audio id="sfx{k}" src="{src}" data-start="{max(0.0, round(t, 3))}" data-duration="{dd}" data-track-index="{30 + k}" data-volume="{vol}"></audio>')
    js = lambda dct: "{ " + ", ".join(f"{k}: {v}" for k, v in dct.items())
    ztl = []
    for (t, du, ease, to, frm, sel) in sorted(zooms(), key=lambda z: z[0]):
        du = max(0.01, round(du, 3))
        if frm is not None:
            ztl.append(f'      tl.fromTo("{sel}", {js(frm)} }}, {js(to)}, duration: {du}, ease: "{ease}", immediateRender: false }}, {round(t, 3)});')
        else:
            ztl.append(f'      tl.to("{sel}", {js(to)}, duration: {du}, ease: "{ease}" }}, {round(t, 3)});')
    # the shots: one zoom wrapper per camera (origin = her face there): #zw1 = take 1 (front), #zw2 = take 2 (side);
    # 12 ms fades at each cut, 30 ms where the take changes, a longer one at the very end
    key = lambda sh: sh["take"]
    vids, face = {}, {}
    shots = ED["shots"]
    for n, sh in enumerate(shots):
        dd = sh["duration"]; last = n == len(shots) - 1
        out = 0.12 if last else (0.03 if shots[n + 1]["take"] != sh["take"] else 0.012)
        auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 0.012, "v": 1},
                          {"t": round(dd - out, 3), "v": 1}, {"t": dd, "v": 0}]}]})
        src = f"assets/video/take-{sh['take']}.mp4"
        vids.setdefault(key(sh), []).append(f'      <video id="v{sh["n"]}" class="clip" src="{src}" data-start="{sh["start"]}" data-duration="{dd}" data-media-start="{sh["media_start"]}" data-playback-rate="{RATE}" data-track-index="{sh["n"] - 1}" playsinline data-has-audio="true" data-automation=\'{auto}\'></video>')
        face.setdefault(key(sh), sh["face"])
    hold, lk = ED["hold"], key(shots[-1])                                        # her last frame, held in the last shot's wrapper
    if hold["duration"] > 0:                                                     # (only if edit.py asks for a hold)
        vids[lk].append(f'      <img id="hold" class="clip" src="assets/img/take-{shots[-1]["take"]}-last.png" alt="" data-start="{hold["start"]}" data-duration="{hold["duration"]}" data-track-index="{len(shots)}" />')
    others = "".join(f'    <div class="shot"><div id="zw{k}" class="zw" data-layout-allow-overflow style="transform-origin: {face[k][0]}px {face[k][1]}px;">\n'
                     + "\n".join(v) + "\n    </div></div>\n" for k, v in vids.items() if k != "1")   # the side camera, on top of the front one
    html = HEAD + f"""  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}">
    <div class="shot"><div id="zw1" class="zw" data-layout-allow-overflow style="transform-origin: {face['1'][0]}px {face['1'][1]}px;">
{chr(10).join(vids['1'])}
    </div></div>
{others}{chr(10).join(hosts)}
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // framing on the girl: opens tight and zooms out; then one look per section, a slow push and a punch on the key word
      // (origin = her face); the ad ends when she stops talking, under the «haz clic» button
{chr(10).join(ztl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(html)


def solo(iid, out):
    """A tiny project with one insert at t=0 and its captions, sharing this project's assets (for snapshots)."""
    ins = next(i for i in ED["inserts"] if i["id"] == iid)
    os.makedirs(os.path.join(out, "compositions"), exist_ok=True)
    if not os.path.exists(os.path.join(out, "assets")):
        os.symlink(os.path.join(ROOT, "assets"), os.path.join(out, "assets"))
    for f in ("hyperframes.json", "package.json"):
        shutil.copy(os.path.join(ROOT, f), out)
    (_, html, _), = build_inserts(only=iid)
    open(os.path.join(out, "compositions", f"{iid}.html"), "w").write(html)
    caps, _ = captions(window=(ins["start"], ins["start"] + ins["duration"]))
    open(os.path.join(out, "compositions", "captions.html"), "w").write(caps)
    d = ins["duration"]
    open(os.path.join(out, "index.html"), "w").write(HEAD + f"""  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{d}">
    <div id="{iid}" data-composition-id="{iid}" data-composition-src="compositions/{iid}.html" data-start="0" data-duration="{d}" data-track-index="1" data-width="1080" data-height="1920"></div>
    <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{d}" data-track-index="2" data-width="1080" data-height="1920"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
    print(f"solo {iid} ({d}s) → {out}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--solo"); ap.add_argument("--out")
    a = ap.parse_args()
    if a.solo:
        return solo(a.solo, a.out)
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "compositions")):
        if f.endswith(".html"):
            os.remove(os.path.join(ROOT, "compositions", f))
    sfx_all = []
    for iid, html, sfx in build_inserts():
        open(os.path.join(ROOT, "compositions", f"{iid}.html"), "w").write(html)
        sfx_all.append((INS[iid]["start"], "whoosh-short", 0.1))
        for t, name, vol, *rest in sfx:
            sfx_all.append((INS[iid]["start"] + t, name, vol, *rest))
    html, t0, d, osfx = outro()
    open(os.path.join(ROOT, "compositions", "outro.html"), "w").write(html)
    sfx_all += [(t0 + t, name, vol) for t, name, vol in osfx]
    caps, npages = captions()
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(caps)
    index(sorted(sfx_all, key=lambda x: x[0]), t0, d)
    print(f"index.html + {len(ED['inserts'])} inserts + outro + captions ({npages} pages) · total {TOTAL}s · {len(sfx_all)} sfx")


if __name__ == "__main__":
    main()
