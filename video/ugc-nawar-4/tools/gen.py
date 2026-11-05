#!/usr/bin/env python3
"""Generate UGC ad #4 («Nuestro Black Friday empieza hoy») from edit.json: index.html (the girl — one take, cut to the
best of her retakes —, her framing, audio), one full-screen insert per explanation (compositions/ins-NN.html, built by
tools/inserts/ins_NN.py), what goes over her (compositions/hook.html: the «Black Friday anticipado» tag of the hook;
compositions/outro.html: the button of the ending and «Hasta el 30 de noviembre») and the captions
(compositions/captions.html).

The language of the first ads about the Formación (UGC #1/#2, tools/common.py), not the Black Friday dress of the last
one: while she talks to camera only captions and a sticker or two cover her; when she explains, the picture cuts to a
full-screen graphic on the VSL's paper or Nawar blue and back. It opens on her plain shot and zooms in fast on her face.

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


# ============================================================================== stickers over the girl
def wcue_from(t0):
    def wcue(word, k=0):
        hits = [w for w in WORDS if w["t"] >= t0 - 1e-6 and norm(w["text"]) == norm(word)]
        return round(hits[k]["t"] - t0, 3)
    return wcue


def hook():
    """the hook, «Nuestro Black Friday empieza hoy. Sí, antes de tiempo.»: a small white tag at the top, over the wall
    above her head — «Black Friday anticipado» (calendar icon) — lands on «antes de tiempo» and leaves with the hook,
    the only Black Friday dress of the ad (the rest is the Formación's look)."""
    P = "h"; sh2 = ED["shots"][1]["start"]; wcue = wcue_from(0.0)
    t0 = round(wcue("antes") - 0.1, 3); d = round(sh2 - t0, 3)
    c = dict(END=d)
    css = """
    #h-row { top: 236px; }
    #h-tag { gap: 14px; height: 80px; padding: 0 34px 0 22px; font-size: 34px; }
    #h-tag svg { display: block; width: 42px; height: 42px; color: «BLUE»; }
"""
    body = f"""    <div id="h-row" class="h-row"><div id="h-tag" class="h-wpill">{icon('cal')}<span>Black Friday anticipado</span></div></div>"""
    js = """
      tl.fromTo(q("tag"), { opacity: 0, y: -20, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, 0.0);
      tl.to(q("tag"), { opacity: 0, y: -12, duration: 0.16, ease: "power2.in" }, «END» - 0.18);
"""
    return comp("hook", d, P, css, body, js, c), t0, d, [(0.0, "pop", 0.18)]


def outro():
    """«Apúntate en el enlace de abajo y llévate el libro por solo un euro. Solo hasta el 30 de noviembre.» — the glossy
    blue button of UGC #2 («CONSÍGUELO POR 1 €») pops under her face on «apúntate»; an arrow bounces under it on «abajo»;
    on «30» the arrow gives way to a white «Hasta el 30 de noviembre» pill (calendar icon); the button breathes once on
    her last frame (held, TAIL)."""
    P = "o"; t0 = ED["outro"]; d = round(TOTAL - t0, 3); wcue = wcue_from(t0)
    c = dict(APU=wcue("apuntate"), ABA=wcue("abajo"), TRE=wcue("30"), END=round(ED["speech_end"] - t0, 3))
    css = """
    #o-wrap { position: absolute; left: 140px; top: 1150px; width: 800px; height: 128px; }
    #o-btn { position: absolute; left: 0; top: 0; width: 800px; height: 128px; border-radius: 64px; overflow: hidden;
      background: linear-gradient(90deg, #0a52d4 0%, #1b74f2 55%, #4a98fb 100%);
      box-shadow: inset 0 0 0 3px rgba(255,255,255,0.55), inset 0 -10px 24px rgba(4,0,80,0.25); }
    #o-gloss { position: absolute; left: 22px; top: 8px; width: 756px; height: 50px; border-radius: 30px;
      background: linear-gradient(180deg, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0) 100%); }
    #o-shine { position: absolute; left: -240px; top: 0; width: 180px; height: 128px;
      background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.45) 50%, rgba(255,255,255,0) 100%); }
    #o-label { position: absolute; left: 0; top: 0; width: 800px; height: 128px; display: flex; align-items: center; justify-content: center;
      font-weight: 900; font-size: 60px; line-height: 1; letter-spacing: -0.01em; color: #FFFFFF; white-space: nowrap; padding-top: 4px; box-sizing: border-box; }
    .o-e { margin-left: 0.2em; }
    #o-arrow { position: absolute; left: 488px; top: 1296px; width: 104px; height: 104px; color: #FFFFFF; }
    #o-arrow svg { display: block; width: 104px; height: 104px; }
    #o-drow { top: 1312px; }
    #o-date { gap: 14px; height: 94px; padding: 0 40px 0 26px; font-size: 41px; }
    #o-date svg { display: block; width: 46px; height: 46px; color: «BLUE»; }
    #o-date b { font-weight: 800; }
"""
    body = f"""    <div id="o-wrap">
      <div id="o-btn"><div id="o-gloss"></div><div id="o-shine"></div><div id="o-label">CONSÍGUELO POR 1<span class="o-e">€</span></div></div>
    </div>
    <div id="o-arrow">{icon('down')}</div>
    <div id="o-drow" class="o-row"><div id="o-date" class="o-wpill">{icon('cal')}<span>Hasta el <b>30 de noviembre</b></span></div></div>"""
    js = """
      tl.fromTo(q("wrap"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.36, ease: "back.out(1.8)" }, «APU» - 0.06);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1240, duration: 0.7, ease: "power2.inOut" }, «APU» + 0.3);
      tl.fromTo(q("arrow"), { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «ABA» - 0.1);
      tl.fromTo(q("arrow"), { y: 0 }, { keyframes: [{ y: 20, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" },
        { y: 20, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" }], immediateRender: false }, «ABA» + 0.14);
      tl.to(q("arrow"), { opacity: 0, y: 10, duration: 0.16, ease: "power2.in" }, «TRE» - 0.3);
      tl.fromTo(q("date"), { opacity: 0, y: 24, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «TRE» - 0.12);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1240, duration: 0.7, ease: "power2.inOut", immediateRender: false }, «END» - 0.1);
      tl.fromTo(q("wrap"), { scale: 1 }, { keyframes: [{ scale: 1.04, duration: 0.25, ease: "power1.inOut" }, { scale: 1, duration: 0.25, ease: "power1.inOut" }],
        immediateRender: false }, «END» - 0.2);
"""
    sfx = [(c["APU"] - 0.06, "pop", 0.2), (c["ABA"] - 0.1, "click-soft", 0.4), (c["TRE"] - 0.12, "pop", 0.18)]
    return comp("outro", d, P, css, body, js, c), t0, d, sfx


# ============================================================================== captions (clean, white, no box)
SHOW = {}
HL_PHRASES = []   # no coloured words: clean white captions, as in UGC #2 (pages still never split these:)
KEEP = [["black", "friday"], ["30", "de", "noviembre"], ["lista", "prioritaria"], ["un", "euro"], ["cada", "mes"], ["otro", "mes"],
        ["falta", "de", "ganas"]]
# caption pages a graphic on screen already says (words twice, one over the other, look cheap): ins-06's green pill «Lo
# ves antes que nadie» and the closing date pill «Hasta el 30 de noviembre»
HIDE = [("ins-06", ["antes", "que", "nadie"]), ("outro", ["el", "30", "de", "noviembre"])]
GLUE = {"y", "que", "con", "los", "las", "la", "el", "de", "del", "por", "en", "un", "una", "te", "tu", "cuando", "si", "a", "al", "lo", "ni",
        "es", "para"}
ARTICLE = {"el", "la", "los", "las", "un", "una", "del", "al"}   # an article before its noun: never the last word of a page
CLITIC = {"te", "me", "se", "le", "les", "nos", "os", "lo"}      # a pronoun before its verb: never the last word of a page


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
    ends = [round(i["start"] + i["duration"], 3) for i in ED["inserts"]]
    def region(t):   # a word that starts in the last 0.12 s of a graphic belongs to the girl right after it
        t = next((e for e in ends if e - 0.12 <= t < e), t)
        return max(b for b in bounds if b <= t + 1e-6)
    # the highlighted phrases (word indices), which a page never splits
    nw = [norm(w["text"]) for w in WORDS]; hl, inside = set(), set()
    for ph in HL_PHRASES + KEEP:
        for i in range(len(nw) - len(ph) + 1):
            if nw[i:i + len(ph)] == ph:
                if ph in HL_PHRASES: hl.update(range(i, i + len(ph)))
                inside.update(range(i, i + len(ph) - 1))
    # sections (no page straddles a cut), split into phrases at commas and full stops; each phrase is cut into pages by a
    # small search for the cheapest split: about 3 words / ≤ 17 characters a page, never inside a highlighted phrase, a
    # one-word page or a page ending on a word that belongs to what follows (y, que, con, de…) costs extra
    secs = []
    for i, w in enumerate(WORDS):
        if secs and region(w["t"]) == region(WORDS[secs[-1][0]]["t"]):
            secs[-1].append(i)
        else:
            secs.append([i])
    def cost(pg, whole):
        chars = sum(len(WORDS[j]["text"]) + 1 for j in pg) - 1
        if chars > 24 or (pg[-1] in inside and pg[-1] != whole[-1]):
            return 1e9
        c = abs(len(pg) - 3) * 1.0 + max(0, chars - 16) * 0.6
        if len(pg) == 1 and len(whole) > 1: c += 4
        if nw[pg[-1]] in GLUE and pg[-1] != whole[-1]: c += 8 if nw[pg[-1]] in CLITIC | ARTICLE else 5
        return c
    def split(ph):
        best = {0: (0.0, [])}
        for b in range(1, len(ph) + 1):
            best[b] = min(((best[a][0] + cost(ph[a:b], ph), best[a][1] + [ph[a:b]]) for a in range(max(0, b - 5), b)), key=lambda x: x[0])
        return best[len(ph)][1]
    pages = []
    for sec in secs:
        if sec[0] == 0:                                    # the very first page («Nuestro Black Friday») is on screen
            k = next(n for n, i in enumerate(sec) if nw[i] == "friday") + 1     # from frame 0
            pages.append(sec[:k]); sec = sec[k:]
        ph = []
        for i in sec:
            ph.append(i)
            if any(ch in (WORDS[i].get("punct") or "") for ch in ".?!,:"):
                pages += split(ph); ph = []
        if ph: pages += split(ph)
    pages = [[dict(WORDS[i], show=SHOW.get(nw[i], WORDS[i]["text"]) + (WORDS[i].get("punct") or "").replace(":", "").replace(";", ""),
                   hl=i in hl) for i in pg] for pg in pages]
    def hidden(pg):                                        # a caption the graphic on screen already says (HIDE): not shown,
        for key, words in HIDE:                            # but still timed, so the page before it leaves on time
            a, b = (INS[key]["start"], INS[key]["start"] + INS[key]["duration"]) if key in INS else (ED[key], TOTAL)
            if (words is None or [norm(w["text"]) for w in pg] == words) and a - 1e-3 <= pg[0]["t"] < b:
                return True
        return False
    off, total = 0.0, TOTAL
    if window:
        off, total = window[0], window[1] - window[0]
        pages = [pg for pg in pages if window[0] - 1e-6 <= pg[0]["t"] < window[1]]
    body, js = [], []
    end_all = round(ED["speech_end"] + 0.12, 3)
    for k, pg in enumerate(pages):
        if hidden(pg):
            continue
        r0 = region(pg[0]["t"])                                            # the section the page belongs to
        t0 = 0.0 if (k == 0 and not window) else max(0.0, pg[0]["t"] - 0.03 - off, r0 - off)
        t1 = (pages[k + 1][0]["t"] - 0.03 - off) if k + 1 < len(pages) else min(end_all - off, total)
        cut = min([x for x in bounds if x > r0 + 1e-6], default=None)           # a page leaves with its section
        if cut is not None and cut - off < t1:
            t1 = round(cut - off, 3)
        g = ground_at(r0 + 0.01)
        spans = " ".join('<span id="cap-w%d-%d" class="cap-w%s">%s</span>' % (k, i, " cap-y" if w["hl"] else "", w["show"])
                         for i, w in enumerate(pg))
        up = " cap-up" if pg[0]["t"] >= ED["outro"] - 1e-3 else ""      # above the button
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
    .cap-gr-girl .cap-w { color: #FFFFFF; text-shadow: 0 3px 14px rgba(0,0,0,0.65), 0 1px 3px rgba(0,0,0,0.55); }
    .cap-gr-blue .cap-w, .cap-gr-dark .cap-w { color: #FFFFFF; text-shadow: none; }
    .cap-g .cap-y { color: «YEL»; }
    .cap-gr-paper .cap-w { color: «INK»; }
"""
    return comp("captions", total, P, css, "\n".join(body), "\n".join(js) + "\n"), len(body)


# ============================================================================== the girl's framing
OPEN_STILLS = 4                   # her first 4 frames are stills (see index())
SHOT_GAIN = {}                    # per-shot voice gain (shot number → linear), where a retake comes out quieter or hotter
ZOOM_IN = (0.0, 0.3, 1.0, 1.18)   # v6.4, the opening hook: from her plain shot (frame 0, sharp) a fast zoom-in on her face
                                  # (t0, duration, scale from, scale to; most of it in the first ~0.12 s)


def zooms():
    """coordinate-target-zoom on the girl (origin = her face): tweens (time, duration, ease, to, from|None, wrapper). The ad
    opens on her plain shot and zooms in fast on her face (the stop-scroll), then a slow push through the hook. After that
    every stretch of the take inside a girl section starts at its own framing (the cuts hide the change) with a slow push,
    and a punch on a key word; the creator's own jump cuts inside a section (edit.py JUMPS) and the cuts between retakes
    change framing too. #zwp = the take."""
    G = ED["girl"]; Z = []
    def push(t0, t1, s0, s1, sel):
        Z.append((round(t0, 3), round(t1 - t0 - 0.004, 3), "none", {"scale": round(s1, 3)}, {"scale": round(s0, 3)}, sel))   # ends just before the next tween
    def punch(t, s, sel, d=0.22, ease="power3.out"):
        Z.append((round(t - 0.05, 3), d, ease, {"scale": s}, None, sel))
    shots = ED["shots"]
    z0, zd, zs0, zs1 = ZOOM_IN
    Z.append((z0, zd, "power3.out", {"scale": zs1}, {"scale": zs0}, "#zwp"))
    push(z0 + zd, shots[1]["start"], zs1, zs1 + 0.05, "#zwp")
    PUNCH = {"pronto": 1.1, "ahora": 1.12, "ganas": 1.1, "oferta": 1.1, "abajo": 1.1}   # on the key word
    LOOK = [1.0, 1.1, 1.02, 1.12, 1.04, 1.08, 1.0, 1.1, 1.03, 1.11]   # start framings, cycling; neighbours differ
    used = [0]
    def stretch(a, b):                                       # one look, a slow push, a punch on the key word
        s0 = LOOK[used[0] % len(LOOK)]; used[0] += 1
        pw = [w for w in WORDS if a + 0.25 <= w["t"] < b - 0.3 and norm(w["text"]) in PUNCH]
        if pw:
            t = pw[0]["t"]; k = PUNCH[norm(pw[0]["text"])] - 1.0
            push(a, t - 0.05, s0, s0 + 0.02, "#zwp"); punch(t, s0 + k, "#zwp"); push(t + 0.2, b, s0 + k, s0 + k + 0.02, "#zwp")
        else:
            push(a, b, s0, s0 + 0.04, "#zwp")
    for g in G:
        for sh in shots:
            a0, b0 = max(g["start"], sh["start"]), min(g["end"], sh["start"] + sh["duration"])
            if b0 - a0 <= 0.05:
                continue
            if sh["n"] == 1:                                  # the hook, done above (its tail after the zoom-in, if any)
                continue
            stretch(a0, b0)
    return Z


def lead_silence(path):
    """seconds of silence at the start of an sfx file (the renderer plays it from its first sample)."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.abs(np.frombuffer(raw, np.float32)); on = np.flatnonzero(x > x.max() * 0.05)
    return round(max(0.0, on[0] / 48000 - 0.01), 3) if len(on) else 0.0


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
«FONTS»    </style>
  </head>
"""


def page_head():
    return HEAD.replace("«FONTS»", FONTS + "\n")


def index(sfx_all, overlays):
    hosts = []
    for k, i in enumerate(ED["inserts"]):
        hosts.append(f'    <div id="{i["id"]}" data-composition-id="{i["id"]}" data-composition-src="compositions/{i["id"]}.html" data-start="{i["start"]}" data-duration="{i["duration"]}" data-track-index="{10 + k}" data-width="1080" data-height="1920"></div>')
    for k, (cid, t0, d) in enumerate(overlays):        # the stickers over the girl
        hosts.append(f'    <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{t0}" data-duration="{d}" data-track-index="{17 + k}" data-width="1080" data-height="1920"></div>')
    hosts.append(f'    <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="21" data-width="1080" data-height="1920"></div>')
    auds = [f'    <audio id="music" src="assets/audio/music-bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="22" data-volume="1"></audio>']
    for k, (t, name, vol, *rest) in enumerate(sfx_all):
        src = f"assets/sfx/{name}.mp3"; head = lead_silence(os.path.join(ROOT, src))   # it sounds at t, not after its silence
        dd = min(rest[0] if rest else 99, media_len(os.path.join(ROOT, src)) - head)
        dd = round(min(dd, TOTAL - t), 3)
        auds.append(f'    <audio id="sfx{k}" src="{src}" data-start="{max(0.0, round(t, 3))}" data-duration="{dd}" data-media-start="{head}" data-track-index="{30 + k}" data-volume="{vol}"></audio>')
    js = lambda dct: "{ " + ", ".join(f"{k}: {v}" for k, v in dct.items())
    ztl = []
    for (t, du, ease, to, frm, sel) in sorted(zooms(), key=lambda z: z[0]):
        du = max(0.01, round(du, 3))
        if frm is not None:
            ztl.append(f'      tl.fromTo("{sel}", {js(frm)} }}, {js(to)}, duration: {du}, ease: "{ease}", immediateRender: false }}, {round(t, 3)});')
        else:
            ztl.append(f'      tl.to("{sel}", {js(to)}, duration: {du}, ease: "{ease}" }}, {round(t, 3)});')
    # the shots: one zoom wrapper for the take (origin = her face), #zwp; 12 ms fades at each cut, a longer one at the
    # very end
    key = lambda sh: sh["take"]
    vids, face = {}, {}
    shots = ED["shots"]
    for n, sh in enumerate(shots):
        dd = sh["duration"]; last = n == len(shots) - 1
        gap = (not last) and shots[n + 1]["start"] - (sh["start"] + dd) > 0.05
        out = 0.05 if last else 0.045 if gap else (0.03 if shots[n + 1]["take"] != sh["take"] else 0.012)
        lv = SHOT_GAIN.get(sh["n"], 1.0)
        pts = [(0, 0), (0.012, lv), (dd - out, lv), (dd, 0)]
        auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in pts]}]})
        src = f"assets/video/take-{sh['take']}.mp4"
        vids.setdefault(key(sh), []).append(f'      <video id="v{sh["n"]}" class="clip" src="{src}" data-start="{sh["start"]}" data-duration="{dd}" data-media-start="{sh["media_start"]}" data-playback-rate="{RATE}" data-track-index="{sh["n"] - 1}" playsinline data-has-audio="true" data-automation=\'{auto}\'></video>')
        face.setdefault(key(sh), sh["face"])
    # v6.5: her first frames as stills over the first video, so the render never shows a frame of the take before its
    # video has seeked (twice the first 1–2 frames came out as the wrong picture); the zoom-in and blur apply as usual
    sh0 = shots[0]
    for k in range(OPEN_STILLS):
        png = os.path.join(ROOT, "assets", "img", f"open-{k}.png")
        nsrc = int((sh0["media_start"] + k / 30 * RATE) * 30 + 1e-6)              # the source frame the video shows there
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, f"assets/video/take-{sh0['take']}.mp4"),
                        "-vf", f"select=eq(n\\,{nsrc})", "-frames:v", "1", png], check=True)
        from PIL import Image
        Image.open(png).convert("RGB").save(png)
        vids[key(sh0)].append(f'      <img id="open{k}" class="clip" src="assets/img/open-{k}.png" alt="" data-start="{max(0.0, round(k / 30 - 0.002, 4))}" data-duration="0.0333" data-track-index="{40 + k}" />')
    hold, lk = ED["hold"], key(shots[-1])                                        # her last frame, held in the last shot's wrapper
    if hold["duration"] > 0:                                                     # (only if edit.py asks for a hold)
        png = os.path.join(ROOT, "assets", "img", f"take-{shots[-1]['take']}-last.png")
        nlast = int(round(shots[-1]["media_end"] * 30)) - 1                 # exactly the last frame shown (no jump)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, f"assets/video/take-{shots[-1]['take']}.mp4"),
                        "-vf", f"select=eq(n\\,{nlast})", "-frames:v", "1", png], check=True)
        from PIL import Image                                                   # no colour chunks: Chrome would tone-map it
        Image.open(png).convert("RGB").save(png)                                # darker than the video frame before it
        vids[lk].append(f'      <img id="hold" class="clip" src="assets/img/take-{shots[-1]["take"]}-last.png" alt="" data-start="{hold["start"]}" data-duration="{hold["duration"]}" data-track-index="{len(shots)}" />')
    wrap = lambda k, v, suf="": (f'    <div class="shot"><div id="zw{k}{suf}" class="zw" data-layout-allow-overflow style="transform-origin: {face[k][0]}px {face[k][1]}px;">\n'
                                 + "\n".join(v) + "\n    </div></div>\n")
    takes = "".join(wrap(k, v) for k, v in vids.items())                     # one wrapper for the take
    html = page_head() + f"""  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{takes}{chr(10).join(hosts)}
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // framing on the girl: opens on her plain shot and zooms in fast on her face; then one look per stretch, a slow push and
      // a punch on the key word (origin = her face); the ad ends when she stops talking, under the button
{chr(10).join(ztl)}
      // the opening zoom-in: frame 0 sharp, a light motion blur while it moves fastest, sharp again as it lands
      tl.fromTo("#zwp", {{ filter: "blur(0px)" }}, {{ filter: "blur(2.5px)", duration: 0.05, ease: "power1.out" }}, 0.0);
      tl.to("#zwp", {{ filter: "blur(0px)", duration: 0.16, ease: "power2.out" }}, 0.05);
      tl.set("#zwp", {{ filter: "none" }}, 0.22);
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
    open(os.path.join(out, "index.html"), "w").write(page_head() + f"""  <body>
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
        sfx_all.append((INS[iid]["start"] - 0.06, "whoosh-short", 0.1))   # its peak lands on the cut
        for t, name, vol, *rest in sfx:
            sfx_all.append((INS[iid]["start"] + t, name, vol, *rest))
    overlays = []
    sfx_all.append((0.0, "whoosh-short", 0.2))                         # the opening zoom-in
    for cid, fn in (("hook", hook), ("outro", outro)):
        html, t0, d, osfx = fn()
        open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w").write(html)
        sfx_all += [(t0 + t, name, vol) for t, name, vol in osfx]
        overlays.append((cid, t0, d))
    caps, npages = captions()
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(caps)
    index(sorted(sfx_all, key=lambda x: x[0]), overlays)
    print(f"index.html + {len(ED['inserts'])} inserts + hook/outro stickers + captions ({npages} pages) · total {TOTAL}s · {len(sfx_all)} sfx")


if __name__ == "__main__":
    main()
