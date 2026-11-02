#!/usr/bin/env python3
"""Generate the UGC Black Friday ad from edit.json: index.html (the girl — take g, the hook, and take p, the body —,
her framing, the three Black Friday backdrops with her cutout in front, audio), one full-screen insert per explanation
(compositions/ins-NN.html, built by tools/inserts/ins_NN.py), what goes over her (compositions/offer.html: «Hasta el
30 de noviembre»; compositions/outro.html: the button of the ending) and the captions (compositions/captions.html).

Same language as the VSL and UGC #1/#2 (tools/common.py): while she talks to camera only captions and stickers cover
her; when she explains, the picture cuts to a full-screen graphic and back. v6.4: the ad opens on her plain shot and
zooms in fast on her face; on each Black Friday beat her room gives way to giant running type and she stays in front of it (backdrops()).

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


def offer():
    """«…solo hasta el 30 de noviembre.» over the girl, after the «1 €» backdrop: a Black Friday yellow «Hasta el 30 de
    noviembre» pill (calendar icon) lands on «30» and leaves before «Black Friday»."""
    P = "f"; t0 = ED["offer"]; d = round(ED["outro"] - t0, 3); wcue = wcue_from(t0)
    c = dict(TRE=wcue("30"), BF=wcue("black"), END=d)
    css = """
    #f-drow { top: 1120px; }
    #f-date { gap: 14px; height: 92px; padding: 0 40px 0 26px; font-size: 40px; }
    #f-date svg { display: block; width: 46px; height: 46px; color: «DARK»; }
    #f-date b { font-weight: 900; }
"""
    body = f"""    <div id="f-drow" class="f-row"><div id="f-date" class="f-ypill">{icon('cal')}<span>Hasta el <b>30 de noviembre</b></span></div></div>"""
    js = """
      tl.fromTo(q("date"), { opacity: 0, y: 26, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «TRE» - 0.08);
      tl.to(q("date"), { opacity: 0, y: 16, duration: 0.16, ease: "power2.in" }, «BF» - 0.32);   // gone before the backdrop
"""
    sfx = [(c["TRE"] - 0.08, "pop", 0.3)]
    return comp("offer", d, P, css, body, js, c), t0, d, sfx


def pron():
    """«cómo pronunciar los sonidos…» on her face, right after the ebook: the list's last item, «✓ Pronunciación», as a
    white pill (the same place as the deadline pill), from «cómo» to just after «sonidos»."""
    P = "n"; t_c = next(w["t"] for w in WORDS if norm(w["text"]) == "como")
    t_s = next(w for w in WORDS if norm(w["text"]) == "sonidos")
    end4 = INS["ins-04"]["start"] + INS["ins-04"]["duration"]
    t0 = round(max(t_c - 0.08, end4), 3); d = round(t_s["end"] + 0.5 - t0, 3)   # never over the ebook's last frame
    c = dict(END=d)
    css = """
    #n-row { top: 1120px; }
    #n-pill { gap: 14px; height: 88px; padding: 0 38px 0 22px; font-size: 38px; }
    #n-pill svg { display: block; width: 48px; height: 48px; }
"""
    body = f"""    <div id="n-row" class="n-row"><div id="n-pill" class="n-wpill">{icon('check')}<span>Pronunciación</span></div></div>"""
    js = """
      tl.fromTo(q("pill"), { opacity: 0, y: 24, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.7)" }, 0.02);
      tl.to(q("pill"), { opacity: 0, y: 14, duration: 0.18, ease: "power2.in" }, «END» - 0.2);
"""
    return comp("pron", d, P, css, body, js, c), t0, d, [(0.02, "pop", 0.2)]


def outro():
    """«Consigue el tuyo en el enlace abajo.» — the glossy blue button of UGC #2 («CONSÍGUELO POR 1 €») pops under her
    face on «consigue»; an arrow bounces under it on «abajo»; the button breathes once on her last frame (held, TAIL)."""
    P = "o"; t0 = ED["outro"]; d = round(TOTAL - t0, 3); wcue = wcue_from(t0)
    c = dict(CON=wcue("consigue"), ABA=wcue("abajo"), END=round(ED["speech_end"] - t0, 3))
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
      font-weight: 900; font-size: 60px; line-height: 1; letter-spacing: -0.01em; color: #FFFFFF; white-space: nowrap; padding-top: 4px; box-sizing: border-box;
      }
    #o-arrow { position: absolute; left: 488px; top: 1296px; width: 104px; height: 104px; color: #FFFFFF; }
    #o-arrow svg { display: block; width: 104px; height: 104px; }
"""
    body = f"""    <div id="o-wrap">
      <div id="o-btn"><div id="o-gloss"></div><div id="o-shine"></div><div id="o-label">CONSÍGUELO POR 1 €</div></div>
    </div>
    <div id="o-arrow">{icon('down')}</div>"""
    js = """
      tl.fromTo(q("wrap"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.36, ease: "back.out(1.8)" }, «CON» - 0.06);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1240, duration: 0.7, ease: "power2.inOut" }, «CON» + 0.3);
      tl.fromTo(q("arrow"), { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «ABA» - 0.1);
      tl.fromTo(q("arrow"), { y: 0 }, { keyframes: [{ y: 20, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" },
        { y: 20, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" }], immediateRender: false }, «ABA» + 0.14);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1240, duration: 0.7, ease: "power2.inOut", immediateRender: false }, «END» - 0.1);
      tl.fromTo(q("wrap"), { scale: 1 }, { keyframes: [{ scale: 1.04, duration: 0.25, ease: "power1.inOut" }, { scale: 1, duration: 0.25, ease: "power1.inOut" }],
        immediateRender: false }, «END» - 0.2);
"""
    sfx = [(c["CON"] - 0.06, "pop", 0.2), (c["ABA"] - 0.1, "click-soft", 0.4)]
    return comp("outro", d, P, css, body, js, c), t0, d, sfx


# ============================================================================== captions (clean, white, no box)
SHOW = {}
HL_PHRASES = []   # no coloured words: clean white captions, as in UGC #2 (pages still never split these:)
KEEP = [["black", "friday"], ["70", "paginas"], ["30", "de", "noviembre"], ["lista", "prioritaria"]]
# caption pages a graphic on screen already says (v6.3: words twice, one over the other, look cheap): the ins-02
# headline «Te quedas ✕ sin practicar» (0:16), the date pill «Hasta el 30 de noviembre», and the closing button
# «CONSÍGUELO POR 1 €» with its arrow (every page from the outro on: None)
HIDE = [("ins-02", ["tu", "te", "quedas"]), ("ins-02", ["sin", "practicar"]), ("offer", ["el", "30", "de", "noviembre"]),
        ("outro", None)]
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
    def hidden(pg):                                        # a caption the graphic on screen already says (HIDE): not shown,
        for key, words in HIDE:                            # but still timed, so the page before it leaves on time
            a, b = (INS[key]["start"], INS[key]["start"] + INS[key]["duration"]) if key in INS else \
                   (ED[key], ED["outro"] if key == "offer" else TOTAL)
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
ZOOM_IN = (0.0, 0.3, 1.0, 1.18)   # v6.4, the opening hook: from her plain shot (frame 0, sharp) a fast zoom-in on her face
                                  # (t0, duration, scale from, scale to; most of it in the first ~0.12 s)


def zooms():
    """coordinate-target-zoom on the girl (origin = her face in each take): tweens (time, duration, ease, to, from|None,
    wrapper). v6.4: the ad opens on her plain shot and zooms in fast on her face (the stop-scroll), a slow push to «este
    Black Friday», where the framing snaps back out as the backdrop comes in. After that every stretch of a take inside a
    girl section starts at its own framing (the cuts
    hide the change) with a slow push, and a punch on a key word; a jump cut inside a section (the take's own cuts, see
    edit.py JUMPS) changes framing too. #zwg = take g (the hook), #zwp = take p (the body)."""
    G = ED["girl"]; Z = []
    def push(t0, t1, s0, s1, sel):
        Z.append((round(t0, 3), round(t1 - t0 - 0.004, 3), "none", {"scale": round(s1, 3)}, {"scale": round(s0, 3)}, sel))   # ends just before the next tween
    def punch(t, s, sel, d=0.22, ease="power3.out"):
        Z.append((round(t - 0.05, 3), d, ease, {"scale": s}, None, sel))
    wrap = lambda sh: "#zw" + sh["take"]
    shots = ED["shots"]
    # intro (v6.4): the ad opens on her plain shot and zooms in fast on her face in the first fraction of a second
    # (ZOOM_IN, a light motion blur at its fastest in index()), the stop-scroll; then a slow push to «este Black Friday»,
    # where it snaps out as her room gives way to the backdrop (see BACKDROPS)
    hb = ED["hook_bf"]; t_bf = round(hb - 0.08, 3)
    z0, zd, zs0, zs1 = ZOOM_IN
    Z.append((z0, zd, "power3.out", {"scale": zs1}, {"scale": zs0}, "#zwg"))
    push(z0 + zd, t_bf, zs1, zs1 + 0.04, "#zwg")
    Z.append((t_bf, 0.34, "expo.out", {"scale": 1.04}, None, "#zwg")); push(t_bf + 0.34, ED["shots"][1]["start"], 1.04, 1.09, "#zwg")
    PUNCH = {"anos": 1.12, "facil": 1.1, "creado": 1.1, "black": 1.08, "abajo": 1.1}   # on the key word (not on «euro»: she leans in)
    LOOK = {"g": [1.04], "p": [1.0, 1.1, 1.02, 1.12, 1.04, 1.08, 1.0, 1.1]}   # start framings, cycling; neighbours differ
    used = {"g": 0, "p": 0}
    def stretch(a, b, sh):                                   # one look, a slow push, a punch on the key word
        tk = sh["take"]; s0 = LOOK[tk][used[tk] % len(LOOK[tk])]; used[tk] += 1
        pw = [w for w in WORDS if a + 0.25 <= w["t"] < b - 0.3 and norm(w["text"]) in PUNCH]
        if pw:
            t = pw[0]["t"]; k = PUNCH[norm(pw[0]["text"])] - 1.0
            push(a, t - 0.05, s0, s0 + 0.02, wrap(sh)); punch(t, s0 + k, wrap(sh)); push(t + 0.2, b, s0 + k, s0 + k + 0.02, wrap(sh))
        else:
            push(a, b, s0, s0 + 0.04, wrap(sh))
    outs = sorted(b["t_out"] for b in backdrops() if b["out_flash"])     # a backdrop leaving inside a shot = a jump cut
    for g in G:
        for sh in shots:
            a0, b0 = max(g["start"], sh["start"]), min(g["end"], sh["start"] + sh["duration"])
            if b0 - a0 <= 0.05 or sh["n"] == 1:                 # shot 1 = the hook, done above
                continue
            cuts = [a0] + [x for x in outs if a0 + 0.3 < x < b0 - 0.3] + [b0]
            for a, b in zip(cuts, cuts[1:]):
                stretch(a, b, sh)
    return Z



# ============================================================================== the Black Friday backdrops (v5)
# Three times her room gives way to giant running type and she stays in front of it (her cutout, tools/mattes.py):
# «…este BLACK FRIDAY te interesa» (black, «BLACK FRIDAY» rows), «Entero por un euro» (Nawar blue, «1 €» rows, her raised
# finger in front) and «…ofertas del BLACK FRIDAY» (black again). Each one comes in on a white flash and a hit, rows
# solid and outlined, running in opposite directions; it lives inside her take's zoom wrapper, between the take and the
# cutout, so it takes the same framing.
def backdrops():
    mats = json.load(open(os.path.join(ROOT, "assets", "video", "mattes.json")))
    blacks = [w["t"] for w in WORDS if norm(w["text"]) == "black"]
    sh7 = next(s for s in ED["shots"] if s["take"] == "p" and s["media_start"] - 0.02 <= mats["eur"]["f0"] / 30 <= s["media_end"])
    win = [("bf1", "bf", round(ED["hook_bf"] - 0.08, 3), ED["shots"][1]["start"]),
           ("eur", "eur", sh7["start"], round(next(w["t"] for w in WORDS if w["t"] > sh7["start"] and norm(w["text"]) == "solo") - 0.06, 3)),
           ("bf2", "bf", round(blacks[1], 3), ED["outro"])]   # on «Black» itself (her eyes open), out on the cut to the button
    out = []
    for name, kind, t_in, t_out in win:
        m = mats[name]; m0 = m["f0"] / 30
        sh = next(s for s in ED["shots"] if s["take"] == m["take"] and s["media_start"] - 0.02 <= m0 <= s["media_end"]
                  and s["start"] <= t_in < s["start"] + s["duration"] + 1e-3) if name != "eur" else sh7
        e0 = sh["start"] + (m0 - sh["media_start"]) / RATE            # edit time of the cutout's first frame
        flash = t_in
        t_in = round(max(t_in, e0 + 0.001), 3)                       # eur: from the first frame after the take's own cut
        ms = (round((t_in - e0) * RATE * 30) + 0.01) / 30             # on a whole source frame: the renderer floors it
        ms = round(ms, 4)
        if name == "eur":                                             # «Entero» starts 30 ms before the take's own cut (a
            t_in, ms = flash, 0.0003                                  # frame of the pose before it): the backdrop is there from
                                                                      # the shot's first frame, the cutout one frame early
        assert ms >= 0 and ms + (t_out - t_in) * RATE <= (m["f1"] - m["f0"] + 1) / 30 + 1e-3, (name, ms)
        out.append(dict(name=name, kind=kind, take=m["take"], t_in=t_in, t_out=round(t_out, 3), src=m["src"], ms=ms,
                        flash=round(flash, 3), out_flash=name != "bf1"))   # bf1 leaves on a real cut; eur flashes on the shot cut
    return out


# rows of one word each (frame px, outside the zoom so they never scale): (top, word, style); the captions' band
# (y 1150–1460) stays clear. bf: near-black, «BLACK» white, «FRIDAY» BF yellow; eur: Nawar blue, «1€» yellow / white.
BX_ROWS = {"bf": [(10, "BLACK", "s"), (380, "FRIDAY", "y"), (750, "BLACK", "o"), (1500, "FRIDAY", "oy")],   # (no row at the
           # very bottom: only its top showed, as white blobs through the gaps between her arms and her body)
           "eur": [(0, "1€", "y"), (380, "1€", "o"), (760, "1€", "y"), (1500, "1€", "o")]}
BX_CSS = """
      .bx { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; opacity: 0; }
      .bx-bf { background: radial-gradient(ellipse 70% 50% at 50% 38%, #17152e 0%, #09080f 60%, #040308 100%); }
      .bx-eur { background: radial-gradient(circle at 50% 32%, #3a95ff 0%, #0b56e0 42%, #120081 100%); }
      .bx-rows { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 700px; }
      .bx-row { position: absolute; left: 0; white-space: nowrap; font-family: "Poppins", sans-serif; font-weight: 900; line-height: 1;
        letter-spacing: -0.035em; }
      .bx-row span { display: inline-block; height: 1em; line-height: 1em; vertical-align: top; }
      .bx-bf .bx-row { font-size: 300px; }
      .bx-eur .bx-row { font-size: 380px; letter-spacing: -0.05em; }
      .bx-s { color: #FFFFFF; }
      .bx-y { color: #FFD60A; }
      .bx-o { color: rgba(255,255,255,0.10); -webkit-text-stroke: 4px rgba(255,255,255,0.70); }
      .bx-oy { color: rgba(255,214,10,0.10); -webkit-text-stroke: 4px rgba(255,214,10,0.75); }
      .bx-vig { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 70% at 50% 42%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.40) 100%); }
      #flash { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #FFFFFF; opacity: 0; pointer-events: none; }
"""
BX_W = {("bf", "BLACK"): 1010, ("bf", "FRIDAY"): 1080, ("eur", "1€"): 560}   # word widths at their size (px, measured roughly)
GAP = 120


def bx_html(b):
    rows = []
    for k, (top, word, st) in enumerate(BX_ROWS[b["kind"]]):
        rows.append(f'          <div id="bx-{b["name"]}-r{k}" class="bx-row bx-{st}" style="top: {top}px;">'
                    + (f'<span style="margin-right: {GAP}px">{word}</span>' * 6) + '</div>')
    return (f'      <div id="bx-{b["name"]}" class="bx bx-{b["kind"]}"><div id="bx-{b["name"]}-rows" class="bx-rows">\n' + "\n".join(rows)
            + '\n        </div><div class="bx-vig"></div></div>'), len(rows)


def cut_html(b):
    return (f'      <video id="cut-{b["name"]}" class="clip" src="{b["src"]}" data-start="{b["t_in"]}" data-duration="{round(b["t_out"] - b["t_in"], 3)}" '
            f'data-media-start="{b["ms"]}" data-playback-rate="{RATE}" data-track-index="{60 + ["bf1", "eur", "bf2"].index(b["name"])}" muted playsinline></video>')


def bx_js(b, n):
    """in: bf1 on a white flash, the rows landing from big; eur, the rows sliding in from both sides (lighter flash); bf2,
    the rows punching in with a short shake. Rows drift slowly so a whole word reads beside her; out: a light flash
    with her new framing (zooms() cuts there)."""
    d = round(b["t_out"] - b["t_in"], 3); w = b["name"]; t0 = b["t_in"]; speed = 150
    js = [f'      tl.set("#bx-{w}", {{ opacity: 0 }}, 0);', f'      tl.set("#bx-{w}", {{ opacity: 1 }}, {t0});',
          f'      tl.set("#bx-{w}", {{ opacity: 0 }}, {b["t_out"]});']
    if w == "bf1":
        js += [f'      tl.fromTo("#bx-{w}-rows", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.38, ease: "expo.out", immediateRender: false }}, {t0});',
               f'      tl.fromTo("#flash", {{ opacity: 0.75 }}, {{ opacity: 0, duration: 0.22, ease: "power2.out", immediateRender: false }}, {t0});']
    elif w == "eur":
        js += [f'      tl.fromTo("#flash", {{ opacity: 0.6 }}, {{ opacity: 0, duration: 0.2, ease: "power2.out", immediateRender: false }}, {b["flash"]});']
    else:
        js += [f'      tl.fromTo("#bx-{w}-rows", {{ scale: 0.82 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, {t0});',
               f'      tl.fromTo("#bx-{w}-rows", {{ x: 0 }}, {{ keyframes: [{{ x: -18, duration: 0.04 }}, {{ x: 14, duration: 0.05 }}, {{ x: -9, duration: 0.05 }}, '
               f'{{ x: 5, duration: 0.05 }}, {{ x: 0, duration: 0.05 }}], immediateRender: false }}, {t0});']
    if b["out_flash"]:
        js.append(f'      tl.fromTo("#flash", {{ opacity: 0.3 }}, {{ opacity: 0, duration: 0.14, ease: "power2.out", immediateRender: false }}, {b["t_out"]});')
    for k, (top, word, st) in enumerate(BX_ROWS[b["kind"]]):
        ww = BX_W[(b["kind"], word)] + GAP
        centre = round((1080 - BX_W[(b["kind"], word)]) / 2 - ww * 2)          # the third copy centred in the frame
        dirn = -1 if k % 2 == 0 else 1
        x0, x1 = centre - dirn * speed * d / 2, centre + dirn * speed * d / 2
        if w == "eur":                                                          # slide in from the sides first
            js.append(f'      tl.fromTo("#bx-{w}-r{k}", {{ x: {round(x0 - dirn * 1300)} }}, {{ x: {round(x0)}, duration: 0.32, ease: "expo.out", immediateRender: false }}, {t0});')
            js.append(f'      tl.fromTo("#bx-{w}-r{k}", {{ x: {round(x0)} }}, {{ x: {round(x1)}, duration: {round(d - 0.32, 3)}, ease: "none", immediateRender: false }}, {round(t0 + 0.32, 3)});')
        else:
            js.append(f'      tl.fromTo("#bx-{w}-r{k}", {{ x: {round(x0)} }}, {{ x: {round(x1)}, duration: {d}, ease: "none", immediateRender: false }}, {t0});')
    return js


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
«FONTS»«BX_CSS»    </style>
  </head>
"""


def page_head():
    return HEAD.replace("«FONTS»", FONTS + "\n").replace("«BX_CSS»", BX_CSS)


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
    with_cut = {"#zw" + b["take"] for b in backdrops()}
    for (t, du, ease, to, frm, sel) in sorted(zooms(), key=lambda z: z[0]):
        du = max(0.01, round(du, 3)); sel = f"{sel}, {sel}c" if sel in with_cut else sel
        if frm is not None:
            ztl.append(f'      tl.fromTo("{sel}", {js(frm)} }}, {js(to)}, duration: {du}, ease: "{ease}", immediateRender: false }}, {round(t, 3)});')
        else:
            ztl.append(f'      tl.to("{sel}", {js(to)}, duration: {du}, ease: "{ease}" }}, {round(t, 3)});')
    # the shots: one zoom wrapper per take (origin = her face there): #zwg = take g (the hook), #zwp = take p (the body);
    # 12 ms fades at each cut, 30 ms where the take changes, a longer one at the very end
    key = lambda sh: sh["take"]
    vids, face = {}, {}
    shots = ED["shots"]
    eur_t = next(b["t_in"] for b in backdrops() if b["name"] == "eur")
    nw = [norm(w["text"]) for w in WORDS]
    dip = next(i for i in range(len(nw)) if nw[i:i + 4] == ["por", "eso", "hemos", "creado"])
    dip = (WORDS[dip]["t"] - 0.03, WORDS[dip + 4]["t"] - 0.04)               # «Por eso hemos creado» comes out 6 LU hot
    for n, sh in enumerate(shots):
        dd = sh["duration"]; last = n == len(shots) - 1
        gap = (not last) and shots[n + 1]["start"] - (sh["start"] + dd) > 0.05
        out = 0.05 if last else 0.045 if gap else (0.03 if shots[n + 1]["take"] != sh["take"] else 0.012)
        lv = 1.25 if sh["start"] - 1e-3 <= eur_t < sh["start"] + dd else 1.0    # «Entero por un euro»: the quietest line, +2 dB
        pts = [(0, 0), (0.012, lv)]
        if sh["start"] < dip[0] and dip[1] < sh["start"] + dd:
            a, b = dip[0] - sh["start"], dip[1] - sh["start"]
            pts += [(a, lv), (a + 0.03, 0.7), (b - 0.03, 0.7), (b, lv)]
        pts += [(dd - out, lv), (dd, 0)]
        auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(t, 3), "v": v} for t, v in pts]}]})
        src = f"assets/video/take-{sh['take']}.mp4"
        vids.setdefault(key(sh), []).append(f'      <video id="v{sh["n"]}" class="clip" src="{src}" data-start="{sh["start"]}" data-duration="{dd}" data-media-start="{sh["media_start"]}" data-playback-rate="{RATE}" data-track-index="{sh["n"] - 1}" playsinline data-has-audio="true" data-automation=\'{auto}\'></video>')
        face.setdefault(key(sh), sh["face"])
    hold, lk = ED["hold"], key(shots[-1])                                        # her last frame, held in the last shot's wrapper
    if hold["duration"] > 0:                                                     # (only if edit.py asks for a hold)
        png = os.path.join(ROOT, "assets", "img", f"take-{shots[-1]['take']}-last.png")
        nlast = int(round(shots[-1]["media_end"] * 30)) - 1                 # exactly the last frame shown (no jump)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, f"assets/video/take-{shots[-1]['take']}.mp4"),
                        "-vf", f"select=eq(n\\,{nlast})", "-frames:v", "1", png], check=True)
        from PIL import Image                                                   # no colour chunks: Chrome would tone-map it
        Image.open(png).convert("RGB").save(png)                                # darker than the video frame before it
        vids[lk].append(f'      <img id="hold" class="clip" src="assets/img/take-{shots[-1]["take"]}-last.png" alt="" data-start="{hold["start"]}" data-duration="{hold["duration"]}" data-track-index="{len(shots)}" />')
    bxs = backdrops(); bxjs, bxh, cuts = [], [], {}
    for b in bxs:          # the backdrops over both takes (not zoomed), then her cutouts in a twin of her take's wrapper
        h, n = bx_html(b); bxh.append(h); bxjs += bx_js(b, n); cuts.setdefault(b["take"], []).append(cut_html(b))
    wrap = lambda k, v, suf="": (f'    <div class="shot"><div id="zw{k}{suf}" class="zw" data-layout-allow-overflow style="transform-origin: {face[k][0]}px {face[k][1]}px;">\n'
                                 + "\n".join(v) + "\n    </div></div>\n")
    takes = "".join(wrap(k, v) for k, v in vids.items())                     # one wrapper per take, in order of appearance
    takes += '    <div class="shot">\n' + "\n".join(bxh) + '\n    </div>\n' + "".join(wrap(k, v, "c") for k, v in cuts.items())
    takes += '    <div id="flash"></div>\n'
    html = page_head() + f"""  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{takes}{chr(10).join(hosts)}
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // framing on the girl: opens tight and zooms out, punches on «Black Friday»; then one look per stretch, a slow push and a
      // punch on the key word (origin = her face); the ad ends when she stops talking, under the button
{chr(10).join(ztl)}
      // the opening zoom-in: frame 0 sharp, a light motion blur while it moves fastest, sharp again as it lands
      tl.fromTo("#zwg", {{ filter: "blur(0px)" }}, {{ filter: "blur(2.5px)", duration: 0.05, ease: "power1.out" }}, 0.0);
      tl.to("#zwg", {{ filter: "blur(0px)", duration: 0.16, ease: "power2.out" }}, 0.05);
      tl.set("#zwg", {{ filter: "none" }}, 0.22);
      // the Black Friday backdrops: in on a white flash, rows running both ways, out at the cut / on the next words
      tl.set("#flash", {{ opacity: 0 }}, 0);
{chr(10).join(bxjs)}
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
        if iid == "ins-04":                                                   # back to her on the second take, a soft one
            sfx_all.append((INS[iid]["start"] + INS[iid]["duration"] - 0.08, "whoosh-short", 0.10))
        for t, name, vol, *rest in sfx:
            sfx_all.append((INS[iid]["start"] + t, name, vol, *rest))
    overlays = []
    sfx_all.append((0.0, "whoosh-short", 0.2))                         # the opening zoom-in
    for b in backdrops():                  # the hit under each backdrop; on «Entero» it lands in the breath before the word
        sfx_all += [(b["t_in"] - 0.06, "whoosh-short", 0.14),          # v6.4: the hits ~3 dB lower
                    (b["t_in"] - 0.06, "impact", 0.21) if b["name"] == "eur" else (b["t_in"], "impact", 0.28)]   # eur: just before «Entero»
        if b["out_flash"]:
            sfx_all.append((b["t_out"] - 0.06, "whoosh-short", 0.1))
    for cid, fn in (("pron", pron), ("offer", offer), ("outro", outro)):
        html, t0, d, osfx = fn()
        open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w").write(html)
        sfx_all += [(t0 + t, name, vol) for t, name, vol in osfx]
        overlays.append((cid, t0, d))
    caps, npages = captions()
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(caps)
    index(sorted(sfx_all, key=lambda x: x[0]), overlays)
    print(f"index.html + {len(ED['inserts'])} inserts + 3 backdrops + offer/outro stickers + captions ({npages} pages) · total {TOTAL}s · {len(sfx_all)} sfx")


if __name__ == "__main__":
    main()
