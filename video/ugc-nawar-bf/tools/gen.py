#!/usr/bin/env python3
"""Generate the UGC Black Friday ad from edit.json: index.html (the girl — take g, the hook, and take p, the body —,
her framing, audio), one full-screen insert per explanation (compositions/ins-NN.html, built by
tools/inserts/ins_NN.py), the stickers over her (compositions/hook.html: «Países Bajos» and the «BLACK FRIDAY» tape;
compositions/offer.html: the 1 € burst, «hasta el 30 de noviembre», the tape again), the button of the ending
(compositions/outro.html) and the captions (compositions/captions.html).

Same language as UGC #1/#2 (tools/common.py), in its Black Friday dress: while she talks to camera only captions and
stickers cover her; when she explains, the picture cuts to a full-screen dark graphic and back. The ad opens tight on
her face and zooms out; «este Black Friday» slams the tape in with a punch.

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


BF_CSS = """
    .«P»-bf { display: flex; align-items: center; gap: 14px; height: 78px; padding: 0 30px; border-radius: 18px; background: #0C0C1E;
      color: #FFFFFF; white-space: nowrap; box-shadow: inset 0 0 0 2px rgba(255,255,255,0.18), 0 18px 40px rgba(0,0,0,0.35);
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 34px; line-height: 1; letter-spacing: 0.12em; padding-top: 3px; box-sizing: border-box; }
    .«P»-bf i { display: block; width: 12px; height: 12px; border-radius: 50%; background: «SKY»; font-style: normal; }
"""


def hook():
    """«Si vives en Países Bajos…»: a white «Países Bajos» pill (NL flag) on «Países»; on «este Black Friday» a black
    «BLACK FRIDAY» label lands at the top (with the punch on her); both leave at the cut to take p."""
    P = "h"; d = ED["shots"][1]["start"]; wcue = wcue_from(0.0)
    c = dict(PAI=wcue("paises"), BF=round(ED["hook_bf"] - 0.05, 3), END=d)
    css = BF_CSS + """
    #h-prow { top: 196px; }
    #h-pill { transform-origin: 50% 50%; }
    #h-brow { top: 190px; }
"""
    body = f"""    <div id="h-prow" class="h-row"><div id="h-pill" class="h-wpill"><span class="h-flag h-flagd">{FLAG_NL}</span><span>Países Bajos</span></div></div>
    <div id="h-brow" class="h-row"><div id="h-bf" class="h-bf"><i></i><span>BLACK FRIDAY</span><i></i></div></div>"""
    js = """
      tl.fromTo(q("pill"), { opacity: 0, y: 20, scale: 1.0 }, { opacity: 1, y: 0, scale: 1.2, duration: 0.3, ease: "back.out(1.6)" }, «PAI» - 0.05);
      tl.to(q("pill"), { opacity: 0, y: -16, duration: 0.16, ease: "power2.in" }, «BF» - 0.14);
      tl.fromTo(q("bf"), { opacity: 0, scale: 0.6, y: 10 }, { opacity: 1, scale: 1.15, y: 0, duration: 0.3, ease: "back.out(2)" }, «BF»);
"""
    sfx = [(c["PAI"] - 0.05, "pop", 0.16), (c["BF"], "whoosh-short", 0.16), (c["BF"] + 0.02, "pop", 0.22)]
    return comp("hook", d, P, css, body, js, c), 0.0, d, sfx


def offer():
    """«Entero por un euro, solo hasta el 30 de noviembre. Esta es una de nuestras ofertas del Black Friday.» over the
    girl: on «euro» a white price card lands in the top-right corner, clear of her face («BLACK FRIDAY» label, «1 €»);
    a white «Hasta el 30 de noviembre» pill on «30»; on «Black Friday» the label gives a small pulse; all leave at the
    call to action."""
    P = "f"; t0 = ED["offer"]; d = round(ED["outro"] - t0, 3); wcue = wcue_from(t0)
    c = dict(EUR=wcue("euro"), TRE=wcue("30"), BF=wcue("black"), END=d)
    css = BF_CSS + """
    #f-card { left: 742px; top: 222px; width: 290px; height: 250px; transform: rotate(4deg); transform-origin: 50% 50%;
      box-shadow: 0 30px 70px rgba(0,0,0,0.35), 0 6px 16px rgba(0,0,0,0.18); }
    #f-lab { position: absolute; left: 22px; top: 20px; height: 44px; padding: 0 16px; border-radius: 12px; font-size: 20px; gap: 9px; }
    #f-lab i { width: 8px; height: 8px; }
    #f-eur { position: absolute; left: 0; top: 96px; width: 290px; height: 130px; text-align: center; font-weight: 900; font-size: 120px; line-height: 130px;
      letter-spacing: -0.04em; color: «INDIGO»; }
    #f-drow { top: 1130px; }
    #f-date { gap: 14px; height: 80px; padding: 0 34px 0 22px; font-size: 36px; }
    #f-date svg { display: block; width: 42px; height: 42px; color: «RED»; }
    #f-date b { color: «RED»; font-weight: 800; }
"""
    body = f"""    <div id="f-card" class="f-card"><div id="f-lab" class="f-bf"><i></i><span>BLACK FRIDAY</span></div><div id="f-eur">1 €</div></div>
    <div id="f-drow" class="f-row"><div id="f-date" class="f-wpill">{icon('cal')}<span>Hasta el <b>30 de noviembre</b></span></div></div>"""
    js = """
      tl.fromTo(q("card"), { opacity: 0, scale: 0.6, rotation: -8 }, { opacity: 1, scale: 1, rotation: 4, duration: 0.38, ease: "back.out(1.8)" }, «EUR» - 0.08);
      tl.fromTo(q("date"), { opacity: 0, y: 26, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «TRE» - 0.08);
      tl.to(q("lab"), { keyframes: [{ scale: 1.12, duration: 0.14, ease: "power2.out" }, { scale: 1, duration: 0.22, ease: "power2.inOut" }] }, «BF» - 0.04);
      tl.to([q("card"), q("date")], { opacity: 0, scale: 0.92, duration: 0.16, ease: "power2.in" }, «END» - 0.16);
"""
    sfx = [(c["EUR"] - 0.08, "pop", 0.24), (c["TRE"] - 0.08, "pop", 0.3)]
    return comp("offer", d, P, css, body, js, c), t0, d, sfx


def outro():
    """«Consigue el tuyo en el enlace abajo, y al conseguirlo entras directamente en nuestra lista prioritaria del Black
    Friday.» — the glossy blue button of UGC #2 («CONSÍGUELO POR 1 €») pops under her face on «consigue»; an arrow
    bounces under it on «abajo»; on «lista prioritaria» the arrow gives way to a white «Lista prioritaria Black Friday»
    pill with a green tick."""
    P = "o"; t0 = ED["outro"]; d = round(TOTAL - t0, 3); wcue = wcue_from(t0)
    c = dict(CON=wcue("consigue"), ABA=wcue("abajo"), LIS=wcue("lista"), END=round(ED["speech_end"] - t0, 3))
    css = """
    #o-wrap { position: absolute; left: 140px; top: 1150px; width: 800px; height: 128px; }
    #o-glow { position: absolute; left: -40px; top: -30px; width: 880px; height: 188px; border-radius: 94px;
      background: radial-gradient(ellipse at 50% 50%, rgba(77,163,255,0.55) 0%, rgba(77,163,255,0) 70%); }
    #o-btn { position: absolute; left: 0; top: 0; width: 800px; height: 128px; border-radius: 64px; overflow: hidden;
      background: linear-gradient(90deg, #0a52d4 0%, #1b74f2 55%, #4a98fb 100%);
      box-shadow: inset 0 0 0 3px rgba(255,255,255,0.55), inset 0 -10px 24px rgba(4,0,80,0.25), 0 20px 50px rgba(11,109,240,0.5); }
    #o-gloss { position: absolute; left: 22px; top: 8px; width: 756px; height: 50px; border-radius: 30px;
      background: linear-gradient(180deg, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0) 100%); }
    #o-shine { position: absolute; left: -240px; top: 0; width: 180px; height: 128px;
      background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.45) 50%, rgba(255,255,255,0) 100%); }
    #o-label { position: absolute; left: 0; top: 0; width: 800px; height: 128px; display: flex; align-items: center; justify-content: center;
      font-weight: 900; font-size: 60px; line-height: 1; letter-spacing: -0.01em; color: #FFFFFF; white-space: nowrap; padding-top: 4px; box-sizing: border-box;
      text-shadow: 0 0 18px rgba(255,255,255,0.45), 0 3px 0 rgba(0,30,120,0.35); }
    #o-arrow { position: absolute; left: 488px; top: 1296px; width: 104px; height: 104px; color: #FFFFFF; }
    #o-arrow svg { display: block; width: 104px; height: 104px; filter: drop-shadow(0 6px 14px rgba(0,0,0,0.45)); }
    #o-lrow { top: 1312px; }
    #o-list { gap: 14px; height: 80px; padding: 0 34px 0 18px; font-size: 34px; }
    #o-list svg { display: block; width: 48px; height: 48px; }
    #o-list b { color: «BLUE»; font-weight: 800; }
"""
    body = f"""    <div id="o-wrap">
      <div id="o-glow"></div>
      <div id="o-btn"><div id="o-gloss"></div><div id="o-shine"></div><div id="o-label">CONSÍGUELO POR 1 €</div></div>
    </div>
    <div id="o-arrow">{icon('down')}</div>
    <div id="o-lrow" class="o-row"><div id="o-list" class="o-wpill">{icon('check')}<span>Lista prioritaria <b>Black Friday</b></span></div></div>"""
    js = """
      tl.fromTo(q("wrap"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.36, ease: "back.out(1.8)" }, «CON» - 0.06);
      tl.fromTo(q("glow"), { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, «CON»);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1240, duration: 0.7, ease: "power2.inOut" }, «CON» + 0.3);
      tl.fromTo(q("arrow"), { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «ABA» - 0.1);
      tl.fromTo(q("arrow"), { y: 0 }, { keyframes: [{ y: 20, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" },
        { y: 20, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" }], immediateRender: false }, «ABA» + 0.14);
      tl.to(q("arrow"), { opacity: 0, duration: 0.16, ease: "power2.in" }, «LIS» - 0.2);
      tl.fromTo(q("list"), { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «LIS» - 0.06);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1240, duration: 0.7, ease: "power2.inOut", immediateRender: false }, «LIS» + 0.2);
      tl.fromTo(q("wrap"), { scale: 1 }, { keyframes: [{ scale: 1.04, duration: 0.25, ease: "power1.inOut" }, { scale: 1, duration: 0.25, ease: "power1.inOut" }],
        immediateRender: false }, «END» - 0.2);
"""
    sfx = [(c["CON"] - 0.06, "pop", 0.2), (c["ABA"] - 0.1, "click-soft", 0.22), (c["LIS"] - 0.06, "chime", 0.2)]
    return comp("outro", d, P, css, body, js, c), t0, d, sfx


# ============================================================================== captions (clean, white, no box)
SHOW = {}
HL_PHRASES = []   # no coloured words: clean white captions, as in UGC #2 (pages still never split these:)
KEEP = [["black", "friday"], ["70", "paginas"], ["30", "de", "noviembre"], ["lista", "prioritaria"]]
GLUE = {"y", "que", "con", "los", "las", "la", "el", "de", "del", "por", "en", "un", "una", "te", "tu", "cuando", "si", "a", "al", "lo", "ni"}
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
        if nw[pg[-1]] in GLUE and pg[-1] != whole[-1]: c += 8 if nw[pg[-1]] in CLITIC else 5
        return c
    def split(ph):
        best = {0: (0.0, [])}
        for b in range(1, len(ph) + 1):
            best[b] = min(((best[a][0] + cost(ph[a:b], ph), best[a][1] + [ph[a:b]]) for a in range(max(0, b - 5), b)), key=lambda x: x[0])
        return best[len(ph)][1]
    pages = []
    for sec in secs:
        if sec[0] == 0:                                    # the very first page («Si vives en Países Bajos») is on screen
            k = next(n for n, i in enumerate(sec) if nw[i] == "bajos") + 1      # from frame 0
            pages.append(sec[:k]); sec = sec[k:]
        ph = []
        for i in sec:
            ph.append(i)
            if any(ch in (WORDS[i].get("punct") or "") for ch in ".?!,:"):
                pages += split(ph); ph = []
        if ph: pages += split(ph)
    pages = [[dict(WORDS[i], show=SHOW.get(nw[i], WORDS[i]["text"]) + (WORDS[i].get("punct") or "").replace(":", "").replace(";", ""),
                   hl=i in hl) for i in pg] for pg in pages]
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
    .cap-gr-blue .cap-w, .cap-gr-dark .cap-w { color: #FFFFFF; text-shadow: 0 3px 16px rgba(0,0,0,0.55); }
    .cap-g .cap-y { color: «YEL»; }
    .cap-gr-paper .cap-w { color: «INK»; }
"""
    return comp("captions", total, P, css, "\n".join(body), "\n".join(js) + "\n"), len(pages)


# ============================================================================== the girl's framing
def zooms():
    """coordinate-target-zoom on the girl (origin = her face in each take): tweens (time, duration, ease, to, from|None,
    wrapper). The ad opens tight on her face and zooms out fast; a slow push to «este Black Friday», which lands on a
    punch (with the tape). After that every stretch of a take inside a girl section starts at its own framing (the cuts
    hide the change) with a slow push, and a punch on a key word; a jump cut inside a section (the take's own cuts, see
    edit.py JUMPS) changes framing too. #zwg = take g (the hook), #zwp = take p (the body)."""
    G = ED["girl"]; Z = []
    def push(t0, t1, s0, s1, sel):
        Z.append((round(t0, 3), round(t1 - t0 - 0.004, 3), "none", {"scale": round(s1, 3)}, {"scale": round(s0, 3)}, sel))   # ends just before the next tween
    def punch(t, s, sel, d=0.22, ease="power3.out"):
        Z.append((round(t - 0.05, 3), d, ease, {"scale": s}, None, sel))
    wrap = lambda sh: "#zw" + sh["take"]
    shots = ED["shots"]
    # intro: tight on her face → zoom out, push, punch on «Black Friday» (the hook's shot)
    hb = ED["hook_bf"]
    Z.append((0.0, 0.7, "power3.out", {"scale": 1.03}, {"scale": 1.34}, "#zwg"))
    push(0.7, hb - 0.05, 1.03, 1.08, "#zwg"); punch(hb, 1.18, "#zwg", d=0.2, ease="power4.out")
    PUNCH = {"anos": 1.12, "facil": 1.1, "creado": 1.1, "abajo": 1.1}   # on the key word (not on «euro»: she leans in)
    LOOK = {"g": [1.04], "p": [1.0, 1.1, 1.02, 1.12, 1.04, 1.08, 1.0, 1.1]}   # start framings, cycling; neighbours differ
    used = {"g": 0, "p": 0}
    for g in G:
        for sh in shots:
            a, b = max(g["start"], sh["start"]), min(g["end"], sh["start"] + sh["duration"])
            if b - a <= 0.05 or sh["n"] == 1:                   # shot 1 = the hook, done above
                continue
            tk = sh["take"]; s0 = LOOK[tk][used[tk] % len(LOOK[tk])]; used[tk] += 1
            pw = [w for w in WORDS if a + 0.25 <= w["t"] < b - 0.3 and norm(w["text"]) in PUNCH]
            if pw:
                t = pw[0]["t"]; push(a, t - 0.05, s0, s0 + 0.02, wrap(sh)); punch(t, s0 + PUNCH[norm(pw[0]["text"])] - 1.0, wrap(sh))
                push(t + 0.2, b, s0 + PUNCH[norm(pw[0]["text"])] - 1.0, s0 + PUNCH[norm(pw[0]["text"])] - 0.98, wrap(sh))
            else:
                push(a, b, s0, s0 + 0.04, wrap(sh))
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
    </style>
  </head>
"""


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
    # the shots: one zoom wrapper per take (origin = her face there): #zwg = take g (the hook), #zwp = take p (the body);
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
    takes = "".join(f'    <div class="shot"><div id="zw{k}" class="zw" data-layout-allow-overflow style="transform-origin: {face[k][0]}px {face[k][1]}px;">\n'
                    + "\n".join(v) + "\n    </div></div>\n" for k, v in vids.items())   # one wrapper per take, in order of appearance
    html = HEAD + f"""  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{takes}{chr(10).join(hosts)}
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // framing on the girl: opens tight and zooms out, punches on «Black Friday»; then one look per stretch, a slow push and a
      // punch on the key word (origin = her face); the ad ends when she stops talking, under the button
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
        sfx_all.append((INS[iid]["start"] - 0.06, "whoosh-short", 0.1))   # its peak lands on the cut
        for t, name, vol, *rest in sfx:
            sfx_all.append((INS[iid]["start"] + t, name, vol, *rest))
    overlays = []
    for cid, fn in (("hook", hook), ("offer", offer), ("outro", outro)):
        html, t0, d, osfx = fn()
        open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w").write(html)
        sfx_all += [(t0 + t, name, vol) for t, name, vol in osfx]
        overlays.append((cid, t0, d))
    caps, npages = captions()
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(caps)
    index(sorted(sfx_all, key=lambda x: x[0]), overlays)
    print(f"index.html + {len(ED['inserts'])} inserts + hook/offer/outro stickers + captions ({npages} pages) · total {TOTAL}s · {len(sfx_all)} sfx")


if __name__ == "__main__":
    main()
