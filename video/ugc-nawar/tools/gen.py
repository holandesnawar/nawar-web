#!/usr/bin/env python3
"""Generate the whole UGC ad from edit.json: index.html (the cut, zooms, audio), one overlay sub-composition per
shot (compositions/gfx-NN.html) and the captions (compositions/captions.html).

Every cue is a word of the edit (edit.json, tools/edit.py), so a new cut regenerates in one run:
    python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
Templates use «name» tokens (cue times / palette), never str.format, so CSS/JS braces stay literal.
"""
import json, os, re, subprocess, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = json.load(open(os.path.join(ROOT, "edit.json")))
AUD = json.load(open(os.path.join(ROOT, "audio.json")))
SHOTS = {s["n"]: s for s in ED["shots"]}
WORDS = ED["words"]
TOTAL = ED["total"]
RATE = ED["rate"]
W_, H_ = 1080, 1920

PAL = dict(BLUE="#0b6df0", DEEP="#1D0084", NAVY="#120081", SKY="#4da3ff", RED="#E02D3C", GREEN="#16A34A",
           INK="#0C0C1E", MUTED="#5A6480", PAPER="#F4F6FF", LINE="#DDE6F5")
FACE = {"a": (500, 880), "b": (545, 900)}            # face centre per take (zoom origin)


def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", t)


def cue(n, word, k=0):
    """local time (s) of the k-th occurrence of `word` in shot n."""
    hits = [w for w in WORDS if w["shot"] == n and norm(w["text"]) == norm(word)]
    return round(hits[k]["t"] - SHOTS[n]["start"], 3)


def dur(n):
    s = SHOTS[n]
    return round(TOTAL - s["start"], 3) if n == max(SHOTS) else s["duration"]


def sub(s, d):
    def f(m):
        v = {**PAL, **d}[m.group(1)]
        return ("%.3f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)
    return re.sub(r"«([A-Z][A-Z0-9_]*)»", f, s)


FONTS = "\n".join('    @font-face { font-family: "%s"; font-weight: %d; font-style: normal; src: url("assets/fonts/%s") format("woff2"); }'
                  % (f, w, fn) for f, w, fn in [("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 700, "poppins-latin-700-normal.woff2"),
                                                ("Poppins", 800, "poppins-latin-800-normal.woff2"), ("Poppins", 900, "poppins-latin-900-normal.woff2"),
                                                ("Inter", 600, "inter-latin-600-normal.woff2"), ("Inter", 700, "inter-latin-700-normal.woff2")])

BASE = """
    #root { position: absolute; inset: 0; overflow: hidden; font-family: "Poppins", sans-serif; }
    .«P»-card { position: absolute; background: #FFFFFF; border-radius: 34px; overflow: hidden;
      box-shadow: 0 30px 70px rgba(8,4,48,0.40), 0 6px 18px rgba(8,4,48,0.22); }
    .«P»-chip { position: absolute; display: flex; align-items: center; gap: 12px; height: 54px; padding: 0 24px; border-radius: 999px;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 25px; letter-spacing: 0.06em; white-space: nowrap; }
    .«P»-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    .«P»-blue { background: radial-gradient(ellipse 90% 70% at 50% 40%, #0a5fd6 0%, #1b2bb0 46%, #120081 100%); }
    .«P»-night { background: radial-gradient(ellipse 90% 60% at 50% 28%, #21308f 0%, #0d0b38 62%, #07051f 100%); }
    .«P»-dots { position: absolute; left: -40px; top: -40px; width: 1160px; height: 2000px;
      background-image: radial-gradient(circle, rgba(255,255,255,0.10) 2.2px, transparent 2.6px); background-size: 38px 38px; }
    .«P»-flag { position: relative; width: 58px; height: 40px; border-radius: 8px; overflow: hidden; flex: 0 0 58px;
      box-shadow: inset 0 0 0 2px rgba(12,12,30,0.10); background: linear-gradient(#AE1C27 0 33.4%, #FFFFFF 33.4% 66.6%, #21468C 66.6% 100%); }
    .«P»-bub { position: absolute; padding: 22px 30px; border-radius: 30px; font-weight: 600; font-size: 38px; line-height: 1.25; }
    .«P»-bl { background: #FFFFFF; color: «INK»; border-bottom-left-radius: 10px; }
    .«P»-br { background: «BLUE»; color: #FFFFFF; border-bottom-right-radius: 10px; }
    .«P»-w { display: inline-block; }
"""

ICON = {
    "steth": '<svg viewBox="0 0 120 120"><g fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><path d="M34 18 V48 A23 23 0 0 0 80 48 V18"/><path d="M57 71 V84 A16 16 0 0 0 89 84 V77"/><circle cx="89" cy="64" r="12"/></g></svg>',
    "phone": '<svg viewBox="0 0 64 64"><path d="M20 6 h24 a6 6 0 0 1 6 6 v40 a6 6 0 0 1 -6 6 h-24 a6 6 0 0 1 -6 -6 v-40 a6 6 0 0 1 6 -6 z" fill="«DEEP»"/><rect x="19" y="13" width="26" height="36" rx="3" fill="#FFFFFF"/><circle cx="32" cy="54" r="2.6" fill="#FFFFFF"/></svg>',
    "check": '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="«GREEN»"/><path d="M18 33 L28 43 L47 22" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "cross": '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="«RED»"/><path d="M21 21 L43 43 M43 21 L21 43" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/></svg>',
    "play": '<svg viewBox="0 0 32 32"><path d="M10 6 L26 16 L10 26 Z" fill="«BLUE»"/></svg>',
    "book": '<svg viewBox="0 0 48 48"><path d="M6 10 Q16 6 24 12 Q32 6 42 10 V38 Q32 34 24 40 Q16 34 6 38 Z" fill="none" stroke="«BLUE»" stroke-width="4.5" stroke-linejoin="round"/><path d="M24 12 V40" stroke="«BLUE»" stroke-width="4.5"/></svg>',
    "pen": '<svg viewBox="0 0 48 48"><path d="M10 38 L12 30 L32 10 L38 16 L18 36 Z" fill="none" stroke="«BLUE»" stroke-width="4.5" stroke-linejoin="round"/><path d="M28 14 L34 20" stroke="«BLUE»" stroke-width="4.5"/></svg>',
    "ear": '<svg viewBox="0 0 48 48"><path d="M10 28 V24 A14 14 0 0 1 38 24 V28" fill="none" stroke="«BLUE»" stroke-width="4.5"/><rect x="7" y="26" width="9" height="14" rx="4" fill="«BLUE»"/><rect x="32" y="26" width="9" height="14" rx="4" fill="«BLUE»"/></svg>',
    "cal": '<svg viewBox="0 0 48 48"><rect x="6" y="10" width="36" height="32" rx="6" fill="none" stroke="#FFFFFF" stroke-width="4.5"/><path d="M6 20 H42 M16 6 V14 M32 6 V14" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/></svg>',
    "sun": '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="8" fill="«BLUE»"/><g stroke="«BLUE»" stroke-width="4" stroke-linecap="round"><path d="M24 4 V10 M24 38 V44 M4 24 H10 M38 24 H44 M10 10 L14 14 M34 34 L38 38 M38 10 L34 14 M14 34 L10 38"/></g></svg>',
    "moon": '<svg viewBox="0 0 48 48"><path d="M30 6 A18 18 0 1 0 42 32 A14 14 0 0 1 30 6 Z" fill="«BLUE»"/></svg>',
    "dawn": '<svg viewBox="0 0 48 48"><path d="M10 34 A14 14 0 0 1 38 34 Z" fill="«BLUE»"/><path d="M4 40 H44" stroke="«BLUE»" stroke-width="4" stroke-linecap="round"/></svg>',
    "down": '<svg viewBox="0 0 120 80"><path d="M14 14 L60 62 L106 14" fill="none" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


def icon(name):
    return sub(ICON[name], {})


def comp(cid, d, P, css, body, js, cues=None):
    cues = dict(cues or {}, P=P, D=float(d))
    return sub("""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
""" + FONTS + BASE + css + """
  </style>
  <div id="root" data-composition-id="«CID»" data-width="1080" data-height="1920" data-duration="«D»">
""" + body + """
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      const q = (id) => document.getElementById("«P»-" + id);
""" + js + """
      window.__timelines["«CID»"] = tl;
    })();
  </script>
</template>
""", dict(cues, CID=cid))


def typing_js(el_id, text, t0, t1, caret=None):
    """discrete-text-sequence: the text grows with a proxy, one state per character (seek-safe)."""
    return sub("""
      (() => {
        const el = q("«EL»"), full = «TXT»; const typ_«EL» = { n: 0 };
        el.textContent = "";
        tl.fromTo(typ_«EL», { n: 0 }, { n: full.length, duration: «DUR», ease: "none", immediateRender: false,
          onUpdate: () => { el.textContent = full.slice(0, Math.round(typ_«EL».n)); } }, «T0»);
      })();
""", dict(EL=el_id, TXT=json.dumps(text, ensure_ascii=False), DUR=float(t1 - t0), T0=float(t0)))


# ============================================================================== gfx-01 · hook
def gfx01():
    n, P = 1, "g01"; d = dur(n)
    c = dict(MED=cue(n, "medico"), ESC=cue(n, "escucha"))
    css = """
    #g01-card { left: 70px; top: 248px; width: 940px; height: 286px; }
    #g01-row { position: absolute; left: 44px; top: 36px; display: flex; align-items: center; gap: 16px;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; letter-spacing: 0.12em; color: «BLUE»; }
    .g01-l { position: absolute; left: 44px; font-weight: 900; font-size: 62px; line-height: 1.08; letter-spacing: -0.02em; color: «DEEP»; white-space: nowrap; }
    #g01-mk { position: relative; display: inline-block; padding: 0 10px; }
    #g01-mkbg { position: absolute; left: 0; top: 6px; width: 100%; height: 76px; border-radius: 14px; background: «BLUE»; transform-origin: 0% 50%; }
    #g01-mkt { position: relative; }
"""
    body = """    <div id="g01-card" class="g01-card">
      <div id="g01-row"><div class="g01-flag"></div><div>PAÍSES BAJOS</div></div>
      <div class="g01-l" style="top: 96px;">¿Te cuesta pedir cita</div>
      <div class="g01-l" style="top: 168px;">en el <span id="g01-mk"><span id="g01-mkbg"></span><span id="g01-mkt">médico</span></span>?</div>
    </div>"""
    js = """
      tl.fromTo(q("card"), { scale: 0.94, y: -14 }, { scale: 1, y: 0, duration: 0.42, ease: "back.out(1.7)" }, 0);
      tl.fromTo(q("mkbg"), { scaleX: 0 }, { scaleX: 1, duration: 0.26, ease: "power3.out" }, «MED»);
      tl.fromTo(q("mkt"), { color: "«DEEP»" }, { color: "#FFFFFF", duration: 0.12, ease: "none" }, «MED» + 0.06);
      tl.fromTo(q("card"), { scale: 1 }, { scale: 0.97, duration: 0.22, ease: "power2.out", immediateRender: false }, «ESC»);
"""
    return comp("gfx-01", d, P, css, body, js, c), [(c["MED"], "pop", 0.22)]


# ============================================================================== gfx-02 · la llamada
def gfx02():
    n, P = 2, "g02"; d = dur(n)
    c = dict(PRA=cue(n, "practicas"), FRA=cue(n, "frase"), LLA=cue(n, "llamas"), CON=cue(n, "contestan"),
             BLO=cue(n, "bloqueas"))
    c["TYP1"] = round(c["LLA"] - 0.08, 3)
    css = """
    #g02-note { left: 70px; top: 248px; width: 940px; height: 300px; }
    #g02-lab { position: absolute; left: 44px; top: 38px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 25px; letter-spacing: 0.12em; color: «BLUE»; }
    #g02-typed { position: absolute; left: 44px; top: 92px; width: 850px; font-weight: 700; font-size: 50px; line-height: 1.22; color: «INK»; }
    #g02-call { opacity: 0; }
    #g02-av { position: absolute; left: 440px; top: 330px; width: 200px; height: 200px; border-radius: 50%;
      background: rgba(255,255,255,0.12); box-shadow: 0 0 0 14px rgba(255,255,255,0.06); display: flex; align-items: center; justify-content: center; }
    #g02-av svg { width: 120px; height: 120px; }
    #g02-ring { position: absolute; left: 440px; top: 330px; width: 200px; height: 200px; border-radius: 50%; border: 6px solid rgba(255,255,255,0.35); }
    #g02-name { position: absolute; left: 0; top: 572px; width: 1080px; text-align: center; font-weight: 800; font-size: 68px; line-height: 1.1; color: #FFFFFF; }
    #g02-org { position: absolute; left: 0; top: 676px; width: 1080px; text-align: center; font-family: "Inter", sans-serif; font-weight: 600; font-size: 32px; color: rgba(255,255,255,0.72); }
    #g02-st1, #g02-st2 { position: absolute; left: 0; top: 736px; width: 1080px; text-align: center; font-family: "Inter", sans-serif; font-weight: 600; font-size: 32px; }
    #g02-st1 { color: rgba(255,255,255,0.82); }
    #g02-st2 { color: #5fe08e; opacity: 0; }
    #g02-who { position: absolute; left: 70px; top: 812px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; color: rgba(255,255,255,0.6); }
    #g02-b1 { left: 70px; top: 854px; width: 820px; }
    #g02-b2w { position: absolute; right: 70px; top: 1048px; width: 520px; height: 112px; }
    #g02-b2, #g02-b2r, #g02-b2c { position: absolute; right: 0; top: 0; font-weight: 800; font-size: 44px; }
    #g02-b2r { background: «RED»; opacity: 0; }
    #g02-b2c { background: «SKY»; opacity: 0; }
    #g02-tag { right: 70px; top: 980px; background: «RED»; color: #FFFFFF; font-weight: 800; letter-spacing: 0.14em; }
    .g02-btn { position: absolute; top: 1560px; width: 132px; height: 132px; border-radius: 50%; background: rgba(255,255,255,0.14); }
    #g02-hang { background: «RED»; }
"""
    body = """    <div id="g02-note" class="g02-card">
      <div id="g02-lab">TU FRASE, ENSAYADA</div>
      <div id="g02-typed"></div>
    </div>
    <div id="g02-call" class="g02-full g02-night">
      <div class="g02-dots"></div>
      <div id="g02-ring"></div>
      <div id="g02-av">""" + icon("steth") + """</div>
      <div id="g02-name">Huisarts</div>
      <div id="g02-org">Huisartsenpraktijk</div>
      <div id="g02-st1">Bellen…</div>
      <div id="g02-st2">● 00:01</div>
      <div id="g02-who">RECEPCIÓN</div>
      <div id="g02-b1" class="g02-bub g02-bl">Goedemorgen, huisartsenpraktijk! Waarmee kan ik u helpen?</div>
      <div id="g02-tag" class="g02-chip">BLOQUEO</div>
      <div id="g02-b2w"><div id="g02-b2r" class="g02-bub">Eh… ik… ehm…</div><div id="g02-b2c" class="g02-bub">Eh… ik… ehm…</div><div id="g02-b2" class="g02-bub g02-br">Eh… ik… ehm…</div></div>
      <div class="g02-btn" style="left: 196px;"></div><div class="g02-btn" style="left: 474px;"></div><div id="g02-hang" class="g02-btn" style="left: 752px;"></div>
    </div>"""
    js = """
      // the rehearsed line (discrete-text-sequence)
      tl.fromTo(q("note"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.34, ease: "power3.out" }, «PRA» - 0.06);
""" + typing_js("typed", "Goedemorgen, ik wil graag een afspraak maken…", c["PRA"], c["TYP1"]) + """
      // «llamas»: the call screen
      tl.fromTo(q("call"), { opacity: 0, y: 90 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «LLA» - 0.06);
      tl.fromTo(q("ring"), { scale: 1, opacity: 0.9 }, { scale: 1.5, opacity: 0, duration: 0.7, ease: "power1.out", repeat: 1 }, «LLA»);
      tl.fromTo(q("st1"), { opacity: 1 }, { opacity: 0.35, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 1 }, «LLA» + 0.1);
      // «te contestan»: connected, the receptionist speaks fast
      tl.set(q("st1"), { opacity: 0 }, «CON»);
      tl.fromTo(q("st2"), { opacity: 0 }, { opacity: 1, duration: 0.1, ease: "none" }, «CON»);
      tl.fromTo(q("who"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "none" }, «CON»);
      tl.fromTo(q("b1"), { opacity: 0, y: 24, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, «CON» + 0.02);
      // «te bloqueas»: her bubble glitches (chromatic-glitch, deterministic hash on quantised time) + BLOQUEO
      tl.fromTo(q("b2"), { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power3.out" }, «BLO» - 0.06);
      tl.fromTo(q("tag"), { opacity: 0, scale: 1.4, rotation: -6 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.22, ease: "back.out(2)" }, «BLO» + 0.08);
      (() => {
        const hash = (k) => { const x = Math.sin(k * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
        const r = q("b2r"), cc = q("b2c"), main = q("call"); const amp = { a: 0 };
        tl.set([r, cc], { opacity: 0.85 }, «BLO»);
        tl.fromTo(amp, { a: 1 }, { a: 0, duration: 0.42, ease: "power2.in",
          onUpdate: () => {
            const step = Math.floor(tl.time() / 0.04);
            r.style.transform = "translate(" + (amp.a * (hash(step * 13 + 1) * 2 - 1) * 16).toFixed(1) + "px," + (amp.a * (hash(step * 7 + 2) * 2 - 1) * 6).toFixed(1) + "px)";
            cc.style.transform = "translate(" + (amp.a * (hash(step * 13 + 5) * 2 - 1) * 16).toFixed(1) + "px," + (amp.a * (hash(step * 7 + 9) * 2 - 1) * 6).toFixed(1) + "px)";
            main.style.transform = "translate(" + (amp.a * (hash(step * 3 + 4) * 2 - 1) * 9).toFixed(1) + "px,0px)";
          } }, «BLO»);
        tl.set([r, cc], { opacity: 0 }, «BLO» + 0.43);
      })();
"""
    sfx = [(c["LLA"] - 0.08, "whoosh-short", 0.22), (c["LLA"] + 0.05, "ringback", 0.32), (c["CON"] - 0.04, "click-soft", 0.3),
           (c["BLO"] - 0.04, "glitch-1-short", 0.16), (c["BLO"] + 0.06, "error", 0.22)]
    return comp("gfx-02", d, P, css, body, js, c), sfx


# ============================================================================== gfx-03 · el favor / tu país
def gfx03():
    n, P = 3, "g03"; d = dur(n)
    c = dict(ALG=cue(n, "alguien"), MAS=cue(n, "mas"), FAV=cue(n, "favor"), ALGO=cue(n, "algo"), PAIS=cue(n, "pais"),
             SIN=cue(n, "sin"))
    css = """
    #g03-card { left: 70px; top: 248px; width: 940px; height: 300px; }
    .g03-av { position: absolute; top: 46px; width: 150px; height: 150px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
      font-weight: 800; font-size: 46px; color: #FFFFFF; }
    #g03-me { left: 110px; background: «BLUE»; }
    #g03-other { left: 680px; background: #9AA3BC; }
    .g03-nm { position: absolute; top: 214px; width: 260px; text-align: center; font-family: "Inter", sans-serif; font-weight: 700; font-size: 28px; color: «MUTED»; }
    #g03-ph { position: absolute; left: 140px; top: 70px; width: 96px; height: 96px; }
    #g03-arr { position: absolute; left: 290px; top: 110px; width: 360px; height: 26px; }
    #g03-fav { left: 610px; top: 6px; background: «PAPER»; color: «DEEP»; }
    #g03-s2 { position: absolute; left: 0; top: 0; width: 940px; height: 300px; background: #FFFFFF; opacity: 0; }
    #g03-k { position: absolute; left: 50px; top: 44px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; letter-spacing: 0.12em; color: «BLUE»; }
    #g03-big { position: absolute; left: 50px; top: 92px; font-weight: 900; font-size: 64px; line-height: 1.05; color: «DEEP»; white-space: nowrap; }
    #g03-ok { position: absolute; left: 50px; top: 186px; display: flex; align-items: center; gap: 18px; font-weight: 900; font-size: 60px; color: «GREEN»; }
    #g03-ok svg { width: 74px; height: 74px; }
"""
    body = """    <div id="g03-card" class="g03-card">
      <div id="g03-s1">
      <div id="g03-me" class="g03-av">Tú</div><div class="g03-nm" style="left: 55px;">Tú</div>
      <div id="g03-other" class="g03-av">?</div><div class="g03-nm" style="left: 625px;">Otra persona</div>
      <svg id="g03-arr" viewBox="0 0 360 26"><path id="g03-arrp" d="M4 13 H340 M322 3 L344 13 L322 23" fill="none" stroke="«LINE»" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 1" pathLength="1"/></svg>
      <div id="g03-ph">""" + icon("phone") + """</div>
      <div id="g03-fav" class="g03-chip">TE HACE EL FAVOR</div>
      </div>
      <div id="g03-s2">
        <div id="g03-k">EN TU PAÍS</div>
        <div id="g03-big">Llamar al médico</div>
        <div id="g03-ok">""" + icon("check") + """<span>¡Sin pensarlo!</span></div>
      </div>
    </div>"""
    js = """
      tl.fromTo(q("card"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.34, ease: "power3.out" }, «ALG» - 0.08);
      q("arrp").setAttribute("stroke-dashoffset", "1");
      tl.fromTo(q("arrp"), { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power2.out" }, «MAS» - 0.05);
      tl.fromTo(q("ph"), { x: 0, rotation: 0 }, { x: 570, rotation: 14, duration: 0.6, ease: "power2.inOut" }, «MAS»);
      tl.fromTo(q("fav"), { opacity: 0, y: 14, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(1.8)" }, «FAV» - 0.04);
      // «Algo que en tu país…»: the second state
      tl.fromTo(q("s2"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «ALGO» - 0.06);
      tl.set(q("s1"), { opacity: 0 }, «ALGO» + 0.26);
      tl.fromTo(q("ok"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, «SIN» - 0.04);
"""
    return comp("gfx-03", d, P, css, body, js, c), [(c["ALG"] - 0.1, "pop", 0.2), (c["SIN"] - 0.02, "pop", 0.22)]


# ============================================================================== gfx-04 · el tiempo / el inglés
def gfx04():
    n, P = 4, "g04"; d = dur(n)
    c = dict(TIE=cue(n, "tiempo"), POR=cue(n, "porque"), ALG=cue(n, "alguien"), TRA=cue(n, "traduce"), CAM=cue(n, "cambia"),
             ING=cue(n, "ingles"))
    css = """
    #g04-card { left: 70px; top: 248px; width: 940px; height: 300px; }
    #g04-box { position: absolute; left: 44px; top: 44px; width: 250px; height: 212px; border-radius: 26px; background: «DEEP»; overflow: hidden; }
    #g04-boxh { position: absolute; left: 0; top: 0; width: 250px; height: 56px; background: «BLUE»; display: flex; align-items: center; justify-content: center; }
    #g04-boxh svg { width: 34px; height: 34px; }
    #g04-yr { position: absolute; left: 0; top: 56px; width: 250px; height: 156px; overflow: hidden; }
    #g04-col { position: absolute; left: 0; top: 0; width: 250px; }
    .g04-y { width: 250px; height: 156px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 74px; color: #FFFFFF; }
    #g04-k { position: absolute; left: 330px; top: 52px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; letter-spacing: 0.12em; color: «MUTED»; }
    #g04-t { position: absolute; left: 330px; top: 96px; font-weight: 900; font-size: 58px; line-height: 1.05; color: «DEEP»; white-space: nowrap; }
    #g04-no { left: 330px; top: 196px; background: «RED»; color: #FFFFFF; font-weight: 800; }
    #g04-s2 { position: absolute; left: 0; top: 0; width: 940px; height: 300px; background: «PAPER»; opacity: 0; }
    #g04-nl { left: 40px; top: 40px; max-width: 600px; font-size: 36px; background: #FFFFFF; color: «INK»; box-shadow: 0 6px 18px rgba(8,4,48,0.12); }
    #g04-tr { left: 640px; top: 56px; background: «DEEP»; color: #FFFFFF; font-weight: 800; }
    #g04-en { left: 210px; top: 164px; font-size: 40px; font-weight: 800; background: #FFFFFF; color: «DEEP»; box-shadow: 0 0 0 5px «RED», 0 10px 24px rgba(8,4,48,0.18); }
    #g04-enc { left: 76px; top: 184px; height: 64px; background: «RED»; color: #FFFFFF; font-weight: 800; font-size: 28px; }
"""
    years = "".join('<div class="g04-y">%d</div>' % y for y in range(2021, 2026))
    body = """    <div id="g04-card" class="g04-card">
      <div id="g04-s1">
      <div id="g04-box"><div id="g04-boxh">""" + icon("cal") + """</div><div id="g04-yr"><div id="g04-col">""" + years + """</div></div></div>
      <div id="g04-k">PASAN LOS AÑOS…</div>
      <div id="g04-t">y sigues igual</div>
      <div id="g04-no" class="g04-chip">✕ NO SE ARREGLA SOLO</div>
      </div>
      <div id="g04-s2">
        <div id="g04-nl" class="g04-bub g04-bl">Hoe kan ik u helpen?</div>
        <div id="g04-tr" class="g04-chip">TE TRADUCEN</div>
        <div id="g04-enc" class="g04-chip">EN</div>
        <div id="g04-en" class="g04-bub">Oh, let's just speak English!</div>
      </div>
    </div>"""
    js = """
      tl.fromTo(q("card"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.34, ease: "power3.out" }, «TIE» - 0.16);
      // vertical-spring-ticker: 2021 → 2025, one stepped tween per year
      [1, 2, 3, 4].forEach((k) => {
        tl.fromTo(q("col"), { y: -(k - 1) * 156 }, { y: -k * 156, duration: 0.12, ease: "back.out(1.4)", immediateRender: false }, «TIE» + 0.02 + (k - 1) * 0.13);
      });
      tl.fromTo(q("no"), { opacity: 0, scale: 0.8, x: -10 }, { opacity: 1, scale: 1, x: 0, duration: 0.24, ease: "back.out(2)" }, «POR» - 0.08);
      // «alguien que te traduce o que te cambia al inglés»
      tl.fromTo(q("s2"), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power2.out" }, «ALG» - 0.1);
      tl.set(q("s1"), { opacity: 0 }, «ALG» + 0.14);
      tl.fromTo(q("nl"), { opacity: 0, y: 20, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "back.out(1.6)" }, «ALG» - 0.06);
      tl.fromTo(q("tr"), { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2)" }, «TRA» - 0.06);
      tl.fromTo(q("nl"), { opacity: 1 }, { opacity: 0.35, duration: 0.2, ease: "none", immediateRender: false }, «CAM»);
      tl.fromTo(q("en"), { opacity: 0, scale: 1.25, rotation: -3 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.24, ease: "back.out(1.8)" }, «CAM» - 0.02);
      tl.fromTo(q("enc"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }, «ING» - 0.06);
"""
    return comp("gfx-04", d, P, css, body, js, c), [(c["TIE"] - 0.18, "pop", 0.2), (c["ALG"] - 0.1, "pop", 0.18), (c["CAM"] - 0.05, "whoosh-short", 0.22)]


# ============================================================================== gfx-05 · Nawar + profes nativos
def gfx05():
    n, P = 5, "g05"; d = dur(n)
    c = dict(NAW=cue(n, "nawar"), TE=cue(n, "te"), NEE=cue(n, "neerlandes"), CON=cue(n, "con"), EQU=cue(n, "equipo"),
             NAT=cue(n, "nativos"), DOM=cue(n, "dominan"), IDI=cue(n, "idioma"))
    c["OUT"] = round(c["CON"] - 0.02, 3)
    c["VDUR"] = round(d - (c["EQU"] - 0.12), 3); c["VST"] = round(c["EQU"] - 0.12, 3)
    css = """
    #g05-brand { opacity: 0; }
    #g05-glow { position: absolute; left: 140px; top: 360px; width: 800px; height: 800px; border-radius: 50%;
      background: radial-gradient(circle, rgba(77,163,255,0.45) 0%, rgba(77,163,255,0) 65%); }
    #g05-logo { position: absolute; left: 190px; top: 560px; width: 700px; height: 250px; }
    #g05-l1 { position: absolute; left: 0; top: 866px; width: 1080px; text-align: center; font-weight: 700; font-size: 50px; color: rgba(255,255,255,0.82); }
    #g05-l2 { position: absolute; left: 0; top: 930px; width: 1080px; text-align: center; font-weight: 900; font-size: 96px; letter-spacing: -0.02em; color: #FFFFFF; }
    #g05-card { left: 70px; top: 240px; width: 940px; height: 340px; }
    #g05-tile { position: absolute; left: 30px; top: 30px; width: 280px; height: 280px; border-radius: 24px; overflow: hidden; background: #dfe3ee; }
    #g05-v { position: absolute; left: -439px; top: -28px; width: 1401px; height: 556px; object-fit: fill; }   /* Paul's webcam (src x 742–1326) */
    #g05-live { left: 46px; top: 236px; height: 40px; padding: 0 14px; font-size: 18px; background: rgba(12,12,30,0.72); color: #FFFFFF; }
    #g05-k { position: absolute; left: 350px; top: 44px; display: flex; align-items: center; gap: 14px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 25px; letter-spacing: 0.12em; color: «BLUE»; }
    #g05-h { position: absolute; left: 350px; top: 92px; font-weight: 900; font-size: 66px; line-height: 1.05; color: «DEEP»; white-space: nowrap; }
    #g05-s { position: absolute; left: 350px; top: 192px; font-weight: 700; font-size: 44px; line-height: 1.2; color: «INK»; white-space: nowrap; }
    #g05-es { position: relative; display: inline-block; padding: 0 10px; }
    #g05-esbg { position: absolute; left: 0; top: 4px; width: 100%; height: 56px; border-radius: 12px; background: «BLUE»; transform-origin: 0% 50%; }
    #g05-est { position: relative; }
"""
    body = """    <div id="g05-brand" class="g05-full g05-blue">
      <div class="g05-dots"></div><div id="g05-glow"></div>
      <img id="g05-logo" src="assets/img/logo-nawar.png" alt="Nawar" />
      <div id="g05-l1">te enseñamos</div>
      <div id="g05-l2">neerlandés</div>
    </div>
    <div id="g05-card" class="g05-card">
      <div id="g05-tile"><video id="g05-v" class="clip" src="assets/video/paul-clase-1.mp4" muted playsinline data-start="«VST»" data-duration="«VDUR»" data-media-start="1" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video></div>
      <div id="g05-live" class="g05-chip">PROFE PAUL</div>
      <div id="g05-k"><div class="g05-flag"></div><div>PROFESORES NATIVOS</div></div>
      <div id="g05-h">Holandeses</div>
      <div id="g05-s">expertos en <span id="g05-es"><span id="g05-esbg"></span><span id="g05-est">español</span></span></div>
    </div>"""
    js = """
      // brand slam (full screen) on «Nawar»
      tl.fromTo(q("brand"), { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "none" }, «NAW» - 0.16);
      tl.fromTo(q("glow"), { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.8, ease: "power2.out" }, «NAW» - 0.1);
      tl.fromTo(q("logo"), { scale: 1.35, opacity: 0, filter: "blur(14px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.34, ease: "expo.out" }, «NAW» - 0.04);
      tl.fromTo(q("l1"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, «TE» - 0.04);
      tl.fromTo(q("l2"), { opacity: 0, y: 40, scale: 1.08 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "power3.out" }, «NEE» - 0.04);
      tl.fromTo(q("brand"), { opacity: 1, scale: 1 }, { opacity: 0, scale: 1.06, duration: 0.18, ease: "power2.in", immediateRender: false }, «OUT» - 0.18);
      // the teachers
      tl.fromTo(q("card"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.34, ease: "power3.out" }, «EQU» - 0.1);
      tl.fromTo(q("h"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.28, ease: "power3.out" }, «NAT» - 0.04);
      tl.fromTo(q("s"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.28, ease: "power3.out" }, «DOM» - 0.04);
      tl.fromTo(q("esbg"), { scaleX: 0 }, { scaleX: 1, duration: 0.24, ease: "power3.out" }, «IDI» - 0.06);
      tl.fromTo(q("est"), { color: "«INK»" }, { color: "#FFFFFF", duration: 0.1, ease: "none" }, «IDI» - 0.02);
"""
    return comp("gfx-05", d, P, css, body, js, c), [(c["NAW"] - 0.18, "whoosh", 0.2), (c["NAW"] - 0.02, "sparkle", 0.22), (c["EQU"] - 0.12, "pop", 0.2)]


# ============================================================================== gfx-06 · lecciones grabadas
def gfx06():
    n, P = 6, "g06"; d = dur(n)
    c = dict(LEC=cue(n, "lecciones"), CUA=cue(n, "cuando"), TU=cue(n, "tu"), PUE=cue(n, "puedas"))
    c["VST"] = round(c["LEC"] - 0.1, 3); c["VDUR"] = round(d - c["VST"], 3)
    css = """
    #g06-card { left: 90px; top: 236px; width: 900px; height: 500px; background: #0d0b38; }
    #g06-v { position: absolute; left: -151px; top: -4px; width: 1222px; height: 624px; object-fit: fill; }   /* the lesson slide incl. his webcam */
    #g06-chip { left: 26px; top: 392px; background: #FFFFFF; color: «BLUE»; font-weight: 800; }
    #g06-chip svg { width: 26px; height: 26px; }
    #g06-bar { position: absolute; left: 26px; top: 470px; width: 848px; height: 10px; border-radius: 5px; background: rgba(255,255,255,0.3); }
    #g06-fill { position: absolute; left: 0; top: 0; width: 848px; height: 10px; border-radius: 5px; background: «SKY»; transform-origin: 0% 50%; }
    #g06-times { position: absolute; left: 90px; top: 700px; width: 900px; display: flex; justify-content: center; gap: 18px; }
    .g06-t { position: relative; display: flex; align-items: center; gap: 12px; height: 72px; padding: 0 26px; border-radius: 999px; background: #FFFFFF;
      box-shadow: 0 14px 34px rgba(8,4,48,0.35); font-weight: 800; font-size: 34px; color: «DEEP»; }
    .g06-t svg { width: 36px; height: 36px; }
"""
    body = """    <div id="g06-card" class="g06-card">
      <video id="g06-v" class="clip" src="assets/video/paul-clase-2.mp4" muted playsinline data-start="«VST»" data-duration="«VDUR»" data-media-start="1.5" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video>
      <div id="g06-chip" class="g06-chip">""" + icon("play") + """LECCIÓN GRABADA</div>
      <div id="g06-bar"><div id="g06-fill"></div></div>
    </div>
    <div id="g06-times"><div id="g06-t1" class="g06-t">""" + icon("dawn") + """07:30</div><div id="g06-t2" class="g06-t">""" + icon("sun") + """14:00</div><div id="g06-t3" class="g06-t">""" + icon("moon") + """23:15</div></div>"""
    js = """
      tl.fromTo(q("card"), { y: -50, opacity: 0, scale: 0.95 }, { y: 0, opacity: 1, scale: 1, duration: 0.36, ease: "power3.out" }, «LEC» - 0.1);
      tl.fromTo(q("fill"), { scaleX: 0.18 }, { scaleX: 0.46, duration: «D» - «LEC», ease: "none" }, «LEC»);
      [["t1", «CUA»], ["t2", «TU»], ["t3", «PUE»]].forEach(([id, t]) => {
        tl.fromTo(q(id), { opacity: 0, y: 26, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(2)" }, t - 0.06);
      });
"""
    return comp("gfx-06", d, P, css, body, js, c), [(c["LEC"] - 0.12, "whoosh-short", 0.2), (c["CUA"] - 0.06, "pop", 0.16), (c["PUE"] - 0.06, "pop", 0.16)]


# ============================================================================== gfx-07 · ejercicios de verdad (full screen)
def gfx07():
    n, P = 7, "g07"; d = dur(n)
    c = dict(EJE=cue(n, "ejercicios"), VER=cue(n, "verdad"), LEE=cue(n, "leer"), ESC=cue(n, "escribir"), ENT=cue(n, "entrenar"),
             SIM=cue(n, "simple"), TES=cue(n, "test"))
    c["VDUR"] = round(d - 0.04, 3)
    css = """
    #g07-bg { background: «PAPER»; }
    #g07-dots { position: absolute; left: -40px; top: -40px; width: 1160px; height: 2000px;
      background-image: radial-gradient(circle, rgba(29,0,132,0.08) 2.2px, transparent 2.6px); background-size: 38px 38px; }
    #g07-h1 { position: absolute; left: 70px; top: 246px; font-weight: 900; font-size: 100px; line-height: 1.0; letter-spacing: -0.03em; color: «DEEP»; }
    #g07-h2 { position: absolute; left: 70px; top: 360px; padding: 0 26px; border-radius: 24px; background: «BLUE»;
      font-weight: 900; font-size: 92px; line-height: 1.18; letter-spacing: -0.02em; color: #FFFFFF; transform-origin: 0% 50%; }
    #g07-card { left: 60px; top: 540px; width: 960px; height: 400px; border: 3px solid «LINE»; }
    #g07-v { position: absolute; left: -738.5px; top: -2px; width: 2114.5px; height: 849px; object-fit: fill; }
    #g07-skills { position: absolute; left: 60px; top: 980px; width: 960px; display: flex; gap: 18px; }
    .g07-s { display: flex; align-items: center; gap: 14px; height: 92px; padding: 0 30px; border-radius: 26px; background: #FFFFFF;
      box-shadow: 0 14px 30px rgba(8,4,48,0.14); font-weight: 800; font-size: 40px; color: «DEEP»; border: 3px solid «LINE»; }
    .g07-s svg { width: 46px; height: 46px; }
    #g07-quiz { left: 604px; top: 262px; width: 420px; height: 168px; border: 3px solid «LINE»; }
    #g07-qt { position: absolute; left: 30px; top: 22px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; color: «MUTED»; }
    #g07-opts { position: absolute; left: 30px; top: 74px; display: flex; gap: 12px; }
    .g07-o { width: 80px; height: 64px; border-radius: 16px; border: 3px solid «LINE»; display: flex; align-items: center; justify-content: center;
      font-weight: 800; font-size: 32px; color: «MUTED»; }
    #g07-strike { position: absolute; left: 590px; top: 344px; width: 450px; height: 14px; border-radius: 7px; background: «RED»; transform-origin: 0% 50%; }
    #g07-x { position: absolute; left: 960px; top: 226px; width: 92px; height: 92px; }
"""
    body = """    <div id="g07-all" class="g07-full">
      <div id="g07-bg" class="g07-full"><div id="g07-dots"></div></div>
      <div id="g07-h1">Ejercicios</div>
      <div id="g07-h2">de verdad</div>
      <div id="g07-card" class="g07-card"><video id="g07-v" class="clip" src="assets/video/completa-frase.mp4" muted playsinline data-start="0.04" data-duration="«VDUR»" data-media-start="5.2" data-playback-rate="1.45" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video></div>
      <div id="g07-skills"><div id="g07-s1" class="g07-s">""" + icon("book") + """Leer</div><div id="g07-s2" class="g07-s">""" + icon("pen") + """Escribir</div><div id="g07-s3" class="g07-s">""" + icon("ear") + """Oído</div></div>
      <div id="g07-quiz" class="g07-card"><div id="g07-qt">UN SIMPLE TEST</div><div id="g07-opts"><div class="g07-o">A</div><div class="g07-o">B</div><div class="g07-o">C</div><div class="g07-o">D</div></div></div>
      <div id="g07-strike"></div>
      <div id="g07-x">""" + icon("cross") + """</div>
    </div>"""
    js = """
      tl.fromTo(q("all"), { x: 1080 }, { x: 0, duration: 0.3, ease: "power4.out" }, 0);
      tl.fromTo(q("h1"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «EJE» - 0.06);
      tl.fromTo(q("h2"), { opacity: 0, scaleX: 0.4 }, { opacity: 1, scaleX: 1, duration: 0.28, ease: "power3.out" }, «VER» - 0.06);
      tl.fromTo(q("card"), { opacity: 0, y: 60, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.36, ease: "power3.out" }, 0.12);
      // waterfall-entry: the three skills on their words
      [["s1", «LEE»], ["s2", «ESC»], ["s3", «ENT»]].forEach(([id, t]) => {
        tl.fromTo(q(id), { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(1.8)" }, t - 0.06);
        tl.fromTo(q(id), { backgroundColor: "#FFFFFF" }, { backgroundColor: "#E6F0FF", duration: 0.3, ease: "none", immediateRender: false }, t);
      });
      // «en vez de un simple test»: the A/B/C/D card is struck through
      tl.fromTo(q("quiz"), { opacity: 0, y: 30, rotation: 0 }, { opacity: 1, y: 0, rotation: -3, duration: 0.26, ease: "back.out(1.6)" }, «SIM» - 0.12);
      tl.fromTo(q("strike"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power3.out" }, «TES» - 0.04);
      tl.fromTo(q("x"), { opacity: 0, scale: 0.4, rotation: -20 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.24, ease: "back.out(2.4)" }, «TES» + 0.04);
"""
    sfx = [(-0.04, "whoosh-short", 0.24), (c["LEE"] - 0.06, "pop", 0.14), (c["ESC"] - 0.06, "pop", 0.14), (c["ENT"] - 0.06, "pop", 0.14),
           (c["TES"] - 0.02, "error", 0.18)]
    return comp("gfx-07", d, P, css, body, js, c), sfx


# ============================================================================== gfx-08 · cada semana, clase en directo
def gfx08():
    n, P = 8, "g08"; d = dur(n)
    c = dict(CAD=cue(n, "cada"), CLA=cue(n, "clase"), DIR=cue(n, "directo"), REF=cue(n, "reforzar"), APR=cue(n, "aprendido"),
             TRA=cue(n, "trabajar"), PRO=cue(n, "pronunciacion"))
    c["IN"] = round(c["CLA"] - 0.08, 3); c["OUT"] = round(c["TRA"] - 0.36, 3)
    c["VDUR"] = round(c["OUT"] + 0.25 - c["IN"], 3)
    css = """
    #g08-ev { left: 70px; top: 248px; width: 940px; height: 300px; background: «PAPER»; }
    #g08-k { left: 34px; top: 30px; background: «BLUE»; color: #FFFFFF; font-weight: 800; }
    #g08-k svg { width: 30px; height: 30px; }
    #g08-img { position: absolute; left: 30px; top: 104px; width: 880px; height: 173px; }
    .g08-hl { position: absolute; top: 158px; height: 112px; border-radius: 20px; border: 5px solid «BLUE»; }
    #g08-call { opacity: 0; }
    #g08-tile { position: absolute; left: 60px; top: 236px; width: 960px; height: 820px; border-radius: 34px; overflow: hidden; background: #1a1d3a; }
    #g08-v { position: absolute; left: -1220px; top: -280px; width: 4113px; height: 1631px; object-fit: fill; }
    #g08-live { left: 28px; top: 28px; background: «RED»; color: #FFFFFF; font-weight: 800; letter-spacing: 0.14em; }
    #g08-dot { width: 14px; height: 14px; border-radius: 50%; background: #FFFFFF; }
    #g08-rep { right: 28px; top: 28px; background: rgba(255,255,255,0.92); color: «DEEP»; font-weight: 800; }
    #g08-rep svg { width: 30px; height: 30px; }
    #g08-pp { position: absolute; left: 60px; top: 1072px; width: 960px; display: flex; gap: 14px; }
    .g08-p { width: 92px; height: 92px; border-radius: 22px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 32px; color: #FFFFFF; }
    #g08-pr { left: 70px; top: 248px; width: 940px; height: 300px; }
    #g08-pk { left: 34px; top: 30px; background: «DEEP»; color: #FFFFFF; font-weight: 800; }
    #g08-wave { position: absolute; left: 40px; top: 110px; width: 560px; height: 160px; display: flex; align-items: center; gap: 9px; }
    .g08-b { width: 14px; height: 140px; border-radius: 7px; background: «BLUE»; transform-origin: 50% 50%; }
    #g08-snd { position: absolute; left: 630px; top: 104px; width: 280px; display: flex; flex-wrap: wrap; gap: 14px; }
    .g08-sn { width: 126px; height: 74px; border-radius: 20px; background: «DEEP»; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 40px; color: #FFFFFF; }
"""
    bars = "".join('<div class="g08-b"></div>' for _ in range(24))
    parts = "".join('<div class="g08-p" style="background: %s;">%s</div>' % (col, ini) for ini, col in
                    [("LU", "#3b5bdb"), ("MA", "#7b5bd6"), ("JO", "#0b8a8a"), ("AN", "#c2367a"), ("TÚ", "#0b6df0")])
    body = """    <div id="g08-ev" class="g08-card">
      <div id="g08-k" class="g08-chip">""" + icon("cal") + """CADA SEMANA</div>
      <img id="g08-img" src="assets/img/ui-eventos-semana.png" alt="Próximos eventos: clases en directo" />
      <div id="g08-h1" class="g08-hl" style="left: 32px; width: 432px;"></div><div id="g08-h2" class="g08-hl" style="left: 466px; width: 432px;"></div>
    </div>
    <div id="g08-call" class="g08-full g08-night">
      <div class="g08-dots"></div>
      <div id="g08-tile">
        <video id="g08-v" class="clip" src="assets/video/paul-clase-1.mp4" muted playsinline data-start="«IN»" data-duration="«VDUR»" data-media-start="3" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video>
        <div id="g08-live" class="g08-chip"><div id="g08-dot"></div>EN DIRECTO</div>
        <div id="g08-rep" class="g08-chip">""" + icon("check") + """Repaso del módulo</div>
      </div>
      <div id="g08-pp">""" + parts + """</div>
    </div>
    <div id="g08-pr" class="g08-card">
      <div id="g08-pk" class="g08-chip">PRONUNCIACIÓN</div>
      <div id="g08-wave">""" + bars + """</div>
      <div id="g08-snd"><div class="g08-sn">ui</div><div class="g08-sn">uu</div><div class="g08-sn">eu</div><div class="g08-sn">g</div></div>
    </div>"""
    js = """
      // «cada semana»: the real upcoming-events card (two live classes, one week apart)
      tl.fromTo(q("ev"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.34, ease: "power3.out" }, «CAD» - 0.08);
      tl.fromTo(q("h1"), { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.24, ease: "power3.out" }, «CAD» + 0.3);
      tl.fromTo(q("h2"), { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.24, ease: "power3.out" }, «CAD» + 0.52);
      // «clase en directo»: the live call takes the screen
      tl.fromTo(q("call"), { opacity: 0, scale: 1.04 }, { opacity: 1, scale: 1, duration: 0.24, ease: "power3.out" }, «IN»);
      tl.fromTo(q("dot"), { opacity: 1 }, { opacity: 0.25, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 5 }, «IN» + 0.2);
      tl.fromTo(q("live"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.24, ease: "power3.out" }, «DIR» - 0.08);
      tl.fromTo("#g08-pp .g08-p", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.24, ease: "back.out(1.8)", stagger: 0.06 }, «IN» + 0.18);
      tl.fromTo(q("rep"), { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2)" }, «APR» - 0.08);
      tl.fromTo(q("call"), { opacity: 1 }, { opacity: 0, duration: 0.16, ease: "power2.in", immediateRender: false }, «OUT»);
      tl.set(q("ev"), { opacity: 0 }, «IN»);
      // «trabajar la pronunciación»: voice bars (gsap-effects audio visualizer, deterministic)
      tl.fromTo(q("pr"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.32, ease: "power3.out" }, «OUT» + 0.06);
      (() => {
        const bars = Array.from(document.querySelectorAll("#g08-wave .g08-b")); const p = { t: 0 };
        tl.fromTo(p, { t: 0 }, { t: «D» - «OUT», duration: «D» - «OUT», ease: "none", onUpdate: () => {
          bars.forEach((b, i) => {
            const v = 0.22 + 0.78 * Math.abs(Math.sin(p.t * 7.3 + i * 0.62) * Math.sin(p.t * 3.1 + i * 0.27));
            b.style.transform = "scaleY(" + v.toFixed(3) + ")";
          });
        } }, «OUT»);
      })();
      tl.fromTo("#g08-snd .g08-sn", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)", stagger: 0.07 }, «PRO» - 0.08);
"""
    sfx = [(c["CAD"] - 0.1, "pop", 0.18), (c["IN"] - 0.04, "whoosh-short", 0.22), (c["IN"] + 0.12, "notification", 0.18),
           (c["APR"] - 0.08, "pop", 0.14), (c["OUT"] + 0.04, "pop", 0.16)]
    return comp("gfx-08", d, P, css, body, js, c), sfx


# ============================================================================== gfx-09 · 16 semanas: llamas tú
def gfx09():
    n, P = 9, "g09"; d = dur(n)
    c = dict(DIE=cue(n, "dieciseis"), SEM=cue(n, "semanas"), ERE=cue(n, "eres"), LLA=cue(n, "llama"), CIT=cue(n, "cita"),
             SIN=cue(n, "sin"), NAD=cue(n, "nadie"))
    css = """
    #g09-card { left: 70px; top: 244px; width: 940px; height: 430px; }
    #g09-num { position: absolute; left: 40px; top: 36px; width: 330px; text-align: center; font-weight: 900; font-size: 230px; line-height: 1; letter-spacing: -0.05em; color: «DEEP»; font-variant-numeric: tabular-nums; }
    #g09-sem { position: absolute; left: 390px; top: 96px; font-weight: 900; font-size: 92px; line-height: 1.0; letter-spacing: -0.02em; color: «BLUE»; }
    #g09-sub { position: absolute; left: 394px; top: 214px; font-weight: 700; font-size: 40px; color: «INK»; white-space: nowrap; }
    #g09-pills { position: absolute; left: 44px; top: 330px; width: 852px; height: 26px; display: flex; gap: 8px; }
    .g09-p { position: relative; flex: 1 1 0; height: 26px; border-radius: 13px; background: «LINE»; overflow: hidden; }
    .g09-pf { position: absolute; left: 0; top: 0; width: 100%; height: 26px; border-radius: 13px; background: «BLUE»; transform-origin: 0% 50%; }
    #g09-s2 { position: absolute; left: 0; top: 0; width: 940px; height: 430px; background: «PAPER»; opacity: 0; }
    #g09-hd { position: absolute; left: 0; top: 0; width: 940px; height: 96px; background: #FFFFFF; border-bottom: 3px solid «LINE»; }
    #g09-hav { position: absolute; left: 28px; top: 16px; width: 64px; height: 64px; border-radius: 50%; background: «DEEP»; display: flex; align-items: center; justify-content: center; }
    #g09-hav svg { width: 40px; height: 40px; }
    #g09-hn { position: absolute; left: 112px; top: 12px; font-weight: 800; font-size: 34px; line-height: 1.15; color: «INK»; }
    #g09-hs { position: absolute; left: 112px; top: 56px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 24px; line-height: 1.15; color: «GREEN»; }
    #g09-me { right: 30px; top: 118px; max-width: 700px; font-size: 34px; }
    #g09-rx { left: 30px; top: 232px; max-width: 640px; font-size: 34px; box-shadow: 0 6px 18px rgba(8,4,48,0.10); }
    #g09-ok { right: 30px; top: 344px; height: 64px; background: «GREEN»; color: #FFFFFF; font-weight: 800; font-size: 28px; }
    #g09-ok svg { width: 34px; height: 34px; }
"""
    pills = "".join('<div class="g09-p"><div id="g09-pf%d" class="g09-pf"></div></div>' % i for i in range(16))
    body = """    <div id="g09-card" class="g09-card">
      <div id="g09-s1">
      <div id="g09-num">1</div>
      <div id="g09-sem">SEMANAS</div>
      <div id="g09-sub">y llamas tú</div>
      <div id="g09-pills">""" + pills + """</div>
      </div>
      <div id="g09-s2">
        <div id="g09-hd"><div id="g09-hav">""" + icon("steth") + """</div><div id="g09-hn">Huisarts</div><div id="g09-hs">● En llamada · 00:12</div></div>
        <div id="g09-me" class="g09-bub g09-br">Goedemorgen! Ik wil graag een afspraak maken.</div>
        <div id="g09-rx" class="g09-bub g09-bl">Natuurlijk. Dinsdag om tien uur?</div>
        <div id="g09-ok" class="g09-chip">""" + icon("check") + """CITA CONFIRMADA</div>
      </div>
    </div>"""
    js = """
      tl.fromTo(q("card"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.34, ease: "power3.out" }, «DIE» - 0.12);
      // counting-dynamic-scale 1 → 16 with the week pills filling in step
      (() => {
        const el = q("num"); const p = { v: 1 };
        tl.fromTo(p, { v: 1 }, { v: 16, duration: «SEM» - «DIE» + 0.2, ease: "power2.out",
          onUpdate: () => { el.textContent = String(Math.round(p.v)); } }, «DIE»);
        tl.fromTo(el, { scale: 0.86 }, { scale: 1, duration: «SEM» - «DIE» + 0.2, ease: "power2.out" }, «DIE»);
        for (let i = 0; i < 16; i++) tl.fromTo(q("pf" + i), { scaleX: 0 }, { scaleX: 1, duration: 0.1, ease: "power2.out" }, «DIE» + i * («SEM» - «DIE» + 0.1) / 16);
      })();
      tl.fromTo(q("sem"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.26, ease: "power3.out" }, «SEM» - 0.06);
      tl.fromTo(q("sub"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.26, ease: "power3.out" }, «SEM» + 0.2);
      // «eres tú quien llama y pide la cita»
      tl.fromTo(q("s2"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.22, ease: "power3.out" }, «ERE» - 0.08);
      tl.set(q("s1"), { opacity: 0 }, «ERE» + 0.14);
      tl.fromTo(q("me"), { opacity: 0, y: 20, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "back.out(1.6)" }, «LLA» - 0.06);
      tl.fromTo(q("rx"), { opacity: 0, y: 20, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "back.out(1.6)" }, «CIT» - 0.06);
      tl.fromTo(q("ok"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, «SIN» - 0.2);
"""
    sfx = [(c["DIE"] - 0.14, "pop", 0.18), (c["SEM"], "sparkle", 0.16), (c["ERE"] - 0.1, "pop", 0.16), (c["LLA"] - 0.06, "pop", 0.14),
           (c["CIT"] - 0.06, "pop", 0.14), (c["SIN"] - 0.2, "chime", 0.28)]
    return comp("gfx-09", d, P, css, body, js, c), sfx


# ============================================================================== gfx-10 · CTA + end card
def gfx10():
    n, P = 10, "g10"; d = dur(n)
    c = dict(EST=cue(n, "estas"), COM=cue(n, "comenzar"), HAZ=cue(n, "haz"), CLI=cue(n, "clic"), BOT=cue(n, "boton"),
             ABA=cue(n, "abajo"), REL=cue(n, "rellena"), FOR=cue(n, "formulario"), PER=cue(n, "persona"), EQU=cue(n, "equipo"),
             ATE=cue(n, "atendera"))
    c["END"] = round(AUD["final_hit"] - SHOTS[n]["start"] - 0.04, 3)
    c["SEND"] = round(c["FOR"] + 0.42, 3)
    css = """
    #g10-pill { left: 230px; top: 252px; height: 84px; padding: 0 30px 0 22px; background: #FFFFFF; color: «DEEP»; font-family: "Poppins", sans-serif;
      font-weight: 800; font-size: 30px; letter-spacing: 0.04em; box-shadow: 0 18px 40px rgba(8,4,48,0.35); }
    #g10-plogo { width: 150px; height: 54px; background: url("assets/img/logo-nawar.png") center / 100% 100% no-repeat; }
    #g10-arrows { position: absolute; left: 420px; top: 1470px; width: 240px; height: 300px; }
    .g10-a { position: absolute; left: 30px; width: 180px; height: 120px; }
    .g10-a svg { width: 180px; height: 120px; filter: drop-shadow(0 8px 16px rgba(8,4,48,0.5)); }
    #g10-aq { left: 380px; top: 1352px; background: «BLUE»; color: #FFFFFF; font-weight: 800; font-size: 30px; letter-spacing: 0.12em; height: 66px; }
    #g10-form { left: 90px; top: 246px; width: 900px; height: 500px; }
    #g10-ft { position: absolute; left: 44px; top: 36px; font-weight: 900; font-size: 50px; color: «DEEP»; }
    .g10-lb { position: absolute; left: 44px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; color: «MUTED»; }
    .g10-in { position: absolute; left: 44px; width: 812px; height: 84px; border-radius: 20px; border: 3px solid «LINE»; background: «PAPER»;
      font-weight: 700; font-size: 38px; line-height: 84px; padding-left: 26px; color: «INK»; box-sizing: border-box; }
    #g10-btn { position: absolute; left: 44px; top: 392px; width: 812px; height: 84px; border-radius: 22px; background: «BLUE»;
      display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 40px; color: #FFFFFF; }
    #g10-btnok { position: absolute; left: 44px; top: 392px; width: 812px; height: 84px; border-radius: 22px; background: «GREEN»;
      display: flex; align-items: center; justify-content: center; gap: 14px; font-weight: 800; font-size: 40px; color: #FFFFFF; opacity: 0; }
    #g10-btnok svg { width: 44px; height: 44px; }
    #g10-rip { position: absolute; left: 400px; top: 384px; width: 100px; height: 100px; border-radius: 50%; background: rgba(255,255,255,0.55); opacity: 0; }
    #g10-chat { position: absolute; left: 0; top: 0; width: 900px; height: 500px; background: «PAPER»; opacity: 0; }
    #g10-ch { position: absolute; left: 0; top: 0; width: 900px; height: 110px; background: #FFFFFF; border-bottom: 3px solid «LINE»; }
    #g10-cav { position: absolute; left: 30px; top: 18px; width: 74px; height: 74px; border-radius: 50%; background: «DEEP»; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    #g10-clogo { width: 66px; height: 24px; background: url("assets/img/logo-nawar.png") center / 100% 100% no-repeat; }
    #g10-cn { position: absolute; left: 124px; top: 16px; font-weight: 800; font-size: 36px; line-height: 1.15; color: «INK»; }
    #g10-cs { position: absolute; left: 124px; top: 64px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 24px; line-height: 1.15; color: «GREEN»; }
    #g10-typ { left: 30px; top: 150px; width: 150px; height: 84px; background: #FFFFFF; box-shadow: 0 6px 18px rgba(8,4,48,0.10); display: flex; align-items: center; justify-content: center; gap: 12px; }
    .g10-td { width: 16px; height: 16px; border-radius: 50%; background: «MUTED»; }
    #g10-msg { left: 30px; top: 150px; max-width: 760px; font-size: 40px; box-shadow: 0 6px 18px rgba(8,4,48,0.10); }
    #g10-msg2 { left: 30px; top: 292px; max-width: 760px; font-size: 40px; box-shadow: 0 6px 18px rgba(8,4,48,0.10); }
    #g10-end { opacity: 0; }
    #g10-elogo { position: absolute; left: 215px; top: 560px; width: 650px; height: 232px; }
    #g10-et { position: absolute; left: 0; top: 830px; width: 1080px; text-align: center; font-weight: 800; font-size: 60px; color: #FFFFFF; }
    #g10-eb { position: absolute; left: 150px; top: 960px; width: 780px; height: 120px; border-radius: 60px; background: #FFFFFF;
      display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 50px; color: «DEEP»; box-shadow: 0 24px 60px rgba(8,4,48,0.45); }
    #g10-ea { position: absolute; left: 450px; top: 1140px; width: 180px; height: 120px; }
    #g10-ea svg { width: 180px; height: 120px; }
    #g10-sp { position: absolute; left: 0; top: 1300px; width: 1080px; display: flex; justify-content: center; align-items: center; gap: 16px;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 32px; color: rgba(255,255,255,0.86); }
    #g10-sp b { font-family: "Poppins", sans-serif; font-weight: 800; color: #FFFFFF; }
    #g10-sp svg { width: 44px; height: 44px; }
"""
    body = """    <div id="g10-pill" class="g10-chip"><div id="g10-plogo"></div><span>FORMACIÓN NAWAR</span></div>
    <div id="g10-aq" class="g10-chip">AQUÍ ABAJO</div>
    <div id="g10-arrows"><div id="g10-a1" class="g10-a" style="top: 0px;">""" + icon("down") + """</div><div id="g10-a2" class="g10-a" style="top: 90px;">""" + icon("down") + """</div><div id="g10-a3" class="g10-a" style="top: 180px;">""" + icon("down") + """</div></div>
    <div id="g10-form" class="g10-card">
      <div id="g10-fs1">
      <div id="g10-ft">Empieza tu formación</div>
      <div class="g10-lb" style="top: 124px;">NOMBRE</div><div id="g10-i1" class="g10-in" style="top: 156px;"></div>
      <div class="g10-lb" style="top: 258px;">TELÉFONO</div><div id="g10-i2" class="g10-in" style="top: 290px; height: 84px;"></div>
      <div id="g10-btn">Enviar</div>
      <div id="g10-btnok">""" + icon("check") + """Enviado</div>
      <div id="g10-rip"></div>
      </div>
      <div id="g10-chat">
        <div id="g10-ch"><div id="g10-cav"><div id="g10-clogo"></div></div><div id="g10-cn">Equipo Nawar</div><div id="g10-cs">● en línea</div></div>
        <div id="g10-typ" class="g10-bub"><div class="g10-td"></div><div class="g10-td"></div><div class="g10-td"></div></div>
        <div id="g10-msg" class="g10-bub g10-bl">¡Hola! Soy del equipo Nawar.</div>
        <div id="g10-msg2" class="g10-bub g10-bl">Te ayudamos a empezar.</div>
      </div>
    </div>
    <div id="g10-end" class="g10-full g10-blue">
      <div class="g10-dots"></div>
      <img id="g10-elogo" src="assets/img/logo-nawar.png" alt="Nawar" />
      <div id="g10-et">Formación Nawar</div>
      <div id="g10-eb">Rellena el formulario</div>
      <div id="g10-ea">""" + icon("down") + """</div>
      <div id="g10-sp"><svg viewBox="0 0 48 48"><circle cx="18" cy="16" r="8" fill="none" stroke="#FFFFFF" stroke-width="4"/><path d="M4 40 Q4 28 18 28 Q32 28 32 40" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/><circle cx="34" cy="18" r="6" fill="none" stroke="#FFFFFF" stroke-width="3.5"/><path d="M36 28 Q44 29 44 38" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/></svg><span><b>+30.000</b> alumnos siguen nuestras clases en redes</span></div>
    </div>"""
    js = """
      tl.fromTo(q("pill"), { y: -30, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «EST» - 0.06);
      // «haz clic en el botón de acá abajo»: arrows toward the platform button
      tl.fromTo(q("aq"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.24, ease: "back.out(2)" }, «HAZ» - 0.06);
      [["a1", 0], ["a2", 1], ["a3", 2]].forEach(([id, i]) => {
        tl.fromTo(q(id), { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.22, ease: "power3.out" }, «HAZ» + i * 0.07);
        tl.fromTo(q(id), { y: 0 }, { y: 22, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 7, immediateRender: false }, «HAZ» + 0.3 + i * 0.07);
      });
      tl.fromTo(q("pill"), { opacity: 1 }, { opacity: 0, duration: 0.16, ease: "none", immediateRender: false }, «REL» - 0.14);
      // «rellena el formulario»: the form fills and is sent (press-release-spring + click ripple)
      tl.fromTo(q("form"), { y: -40, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.32, ease: "power3.out" }, «REL» - 0.1);
""" + typing_js("i1", "María", c["REL"] + 0.14, c["REL"] + 0.42) + typing_js("i2", "+31 6 •••• ••••", c["REL"] + 0.44, c["SEND"] - 0.06) + """
      tl.fromTo(q("btn"), { scale: 1 }, { scale: 0.94, duration: 0.07, ease: "power2.in" }, «SEND»);
      tl.to(q("btn"), { scale: 1, duration: 0.2, ease: "back.out(3)" }, «SEND» + 0.07);
      tl.fromTo(q("rip"), { opacity: 0.7, scale: 0.2 }, { opacity: 0, scale: 6, duration: 0.45, ease: "power2.out" }, «SEND» + 0.02);
      tl.fromTo(q("btnok"), { opacity: 0 }, { opacity: 1, duration: 0.14, ease: "none" }, «SEND» + 0.12);
      tl.set(q("btn"), { opacity: 0 }, «SEND» + 0.27);
      // «una persona de nuestro equipo te atenderá»
      tl.fromTo(q("chat"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.18, ease: "power3.out" }, «PER» - 0.12);
      tl.set(q("fs1"), { opacity: 0 }, «PER» + 0.06);
      tl.fromTo("#g10-typ .g10-td", { y: 0 }, { y: -10, duration: 0.18, ease: "sine.inOut", yoyo: true, repeat: 3, stagger: 0.08 }, «PER»);
      tl.fromTo(q("typ"), { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "none" }, «PER» - 0.04);
      tl.set(q("typ"), { opacity: 0 }, «EQU» - 0.08);
      tl.fromTo(q("msg"), { opacity: 0, y: 16, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(1.6)" }, «EQU» - 0.08);
      tl.fromTo(q("msg2"), { opacity: 0, y: 16, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(1.6)" }, «ATE» - 0.04);
      // end card on the music's final hit
      tl.fromTo(q("end"), { opacity: 0, scale: 1.05 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power3.out" }, «END»);
      tl.fromTo(q("elogo"), { scale: 1.25, opacity: 0, filter: "blur(12px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out" }, «END» + 0.04);
      tl.fromTo(q("et"), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.26, ease: "power3.out" }, «END» + 0.16);
      tl.fromTo(q("eb"), { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «END» + 0.26);
      tl.fromTo(q("ea"), { y: 0 }, { y: 24, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 2 }, «END» + 0.36);
      tl.fromTo(q("sp"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «END» + 0.34);
"""
    sfx = [(c["EST"] - 0.08, "pop", 0.16), (c["CLI"] - 0.04, "click", 0.3), (c["REL"] - 0.12, "whoosh-short", 0.2),
           (c["REL"] + 0.14, "typing", 0.16, 0.6), (c["SEND"] - 0.03, "click", 0.32), (c["EQU"] - 0.1, "notification", 0.2),
           (c["END"], "sparkle", 0.22)]
    return comp("gfx-10", d, P, css, body, js, c), sfx


# ============================================================================== captions (asr-keyword-glow, karaoke form)
ACCENT = {"bloqueas": "RED", "ingles": "RED", "test": "RED", "nawar": "BLUE"}
SHOW = {"dieciseis": "16"}


def captions():
    P = "cap"
    pages, cur = [], []
    for w in WORDS:
        txt = SHOW.get(norm(w["text"]), w["text"])
        if w.get("punct") == "?":
            txt += "?"
        if w["text"].lower().startswith(("estás",)):
            txt = "¿" + txt
        cur.append(dict(w, show=txt))
        brk = any(ch in (w.get("punct") or "") for ch in ".?!,:") or len(cur) >= 3 or sum(len(x["show"]) for x in cur) >= 15
        if brk:
            pages.append(cur); cur = []
    if cur: pages.append(cur)
    body, js = [], []
    for k, pg in enumerate(pages):
        t0 = max(0.0, pg[0]["t"] - 0.04) if k else 0.0
        t1 = pages[k + 1][0]["t"] - 0.04 if k + 1 < len(pages) else min(ED["speech_end"] + 0.3, TOTAL)
        spans = "".join('<span class="cap-w"><span id="cap-p%d-%d" class="cap-bg" style="background: %s;"></span><span class="cap-t">%s</span></span>'
                        % (k, i, PAL[ACCENT.get(norm(w["text"]), "BLUE")], w["show"]) for i, w in enumerate(pg))
        body.append('    <div id="cap-g%d" class="cap-g">%s</div>' % (k, spans))
        if k == 0:   # the very first frame already carries a caption (thumbnail / scroll-stop)
            js.append('      tl.fromTo(q("g0"), { opacity: 1, scale: 1 }, { opacity: 1, scale: 1, duration: 0.01 }, 0);')
        else:
            js.append('      tl.fromTo(q("g%d"), { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.12, ease: "power3.out" }, %.3f);' % (k, t0))
        js.append('      tl.set(q("g%d"), { opacity: 0 }, %.3f);' % (k, t1))
        for i, w in enumerate(pg):
            a = max(t0, w["t"] - 0.02); b = pg[i + 1]["t"] - 0.02 if i + 1 < len(pg) else t1
            js.append('      tl.fromTo(q("p%d-%d"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.08, ease: "power2.out" }, %.3f);' % (k, i, a))
            js.append('      tl.set(q("p%d-%d"), { opacity: 0 }, %.3f);' % (k, i, b))
    css = """
    .cap-g { position: absolute; left: 70px; top: 1150px; width: 940px; height: 200px; display: flex; flex-wrap: wrap; align-content: center;
      justify-content: center; column-gap: 6px; row-gap: 0px; opacity: 0; }
    .cap-w { position: relative; display: inline-block; padding: 0 12px; }
    .cap-bg { position: absolute; left: 0; top: 10px; width: 100%; height: 86px; border-radius: 18px; opacity: 0; }
    .cap-t { position: relative; display: block; font-weight: 800; font-size: 74px; line-height: 104px; letter-spacing: -0.01em; color: #FFFFFF;
      -webkit-text-stroke: 10px #0b0a2e; paint-order: stroke fill; text-shadow: 0 6px 18px rgba(0,0,0,0.35); white-space: nowrap; }
"""
    return comp("captions", TOTAL, P, css, "\n".join(body), "\n".join(js) + "\n")


# ============================================================================== index.html
def zooms():
    """coordinate-target-zoom, origin on the face: (shot, at, to, duration, ease). Times are absolute."""
    S = SHOTS; Z = []
    def at(n, word, k=0): return round(cue(n, word, k) + S[n]["start"], 3)
    end = lambda n: round(S[n]["start"] + S[n]["duration"], 3)
    Z += [(1, 0.0, 1.04, 2.85, "sine.inOut", 1.0), (1, at(1, "escucha") - 0.04, 1.22, 0.2, "power3.out", None)]
    Z += [(2, S[2]["start"], 1.07, end(2) - S[2]["start"], "none", 1.0)]
    Z += [(3, S[3]["start"], 1.1, at(3, "sin") - 0.07 - S[3]["start"], "none", 1.03), (3, at(3, "sin") - 0.05, 1.2, 0.2, "power3.out", None)]
    Z += [(4, S[4]["start"], 1.1, at(4, "cambia") - 0.04 - S[4]["start"], "none", 1.05), (4, at(4, "cambia") - 0.04, 1.24, 0.2, "power3.out", None)]
    Z += [(5, S[5]["start"], 1.06, at(5, "nativos") - 0.04 - S[5]["start"], "none", 1.0), (5, at(5, "nativos") - 0.04, 1.16, 0.2, "power3.out", None)]
    Z += [(6, S[6]["start"], 1.05, S[6]["duration"], "none", 1.0)]
    Z += [(7, S[7]["start"], 1.0, 0.1, "none", 1.0)]
    Z += [(8, S[8]["start"], 1.04, at(8, "cada") - 0.04 - S[8]["start"], "none", 1.0), (8, at(8, "cada") - 0.04, 1.15, 0.2, "power3.out", None),
          (8, at(8, "trabajar") - 0.4, 1.08, 0.01, "none", None), (8, at(8, "trabajar") - 0.39, 1.13, end(8) - at(8, "trabajar") + 0.39, "none", None)]
    Z += [(9, S[9]["start"], 1.08, at(9, "eres") - 0.06 - S[9]["start"], "none", 1.03), (9, at(9, "eres") - 0.04, 1.18, 0.2, "power3.out", None),
          (9, at(9, "sin") - 0.05, 1.08, 0.3, "power2.inOut", None), (9, at(9, "nadie") - 0.05, 1.22, 0.2, "power3.out", None)]
    Z += [(10, S[10]["start"], 1.04, at(10, "comenzar") - 0.04 - S[10]["start"], "none", 1.0), (10, at(10, "comenzar") - 0.04, 1.15, 0.2, "power3.out", None),
          (10, at(10, "haz") - 0.05, 1.0, 0.3, "power2.inOut", None)]
    return Z


def media_len(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return round(float(out.strip()), 3)


def index(sfx_all):
    shots, hosts, auds, ztl = [], [], [], []
    for s in ED["shots"]:
        n, tk = s["n"], s["take"]; fx, fy = FACE[tk]
        d = s["duration"] if n < max(SHOTS) else round(TOTAL - s["start"], 3)
        media_d = s["duration"]
        auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 0.012, "v": 1},
                          {"t": round(media_d - 0.02, 3), "v": 1}, {"t": media_d, "v": 0}]}]})
        shots.append(f"""    <div class="shot" id="sh{n}"><div class="zw" id="zw{n}" data-layout-allow-overflow style="transform-origin: {fx}px {fy}px;">
      <video id="v{n}" class="clip" src="assets/video/take-{tk}.mp4" data-start="{s['start']}" data-duration="{d}" data-media-start="{s['media_start']}" data-playback-rate="{RATE}" data-track-index="{(n + 1) % 2}" playsinline data-has-audio="true" data-automation='{auto}'></video>
    </div></div>""")
        hosts.append(f'    <div id="gfx-{n:02d}" data-composition-id="gfx-{n:02d}" data-composition-src="compositions/gfx-{n:02d}.html" data-start="{s["start"]}" data-duration="{d}" data-track-index="{n}" data-width="1080" data-height="1920"></div>')
    hosts.append(f'    <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-width="1080" data-height="1920"></div>')
    auds.append(f'    <audio id="music" src="assets/audio/music-bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="12" data-volume="1"></audio>')
    for k, (t, name, vol, *rest) in enumerate(sfx_all):
        src = "assets/audio/ringback.wav" if name == "ringback" else f"assets/sfx/{name}.mp3"
        dd = min(rest[0] if rest else 99, media_len(os.path.join(ROOT, src)))
        dd = round(min(dd, TOTAL - t), 3)
        auds.append(f'    <audio id="sfx{k}" src="{src}" data-start="{max(0.0, round(t, 3))}" data-duration="{dd}" data-track-index="{20 + k}" data-volume="{vol}"></audio>')
    for (n, t, to, du, ease, frm) in zooms():
        if frm is not None:
            ztl.append(f'      tl.fromTo("#zw{n}", {{ scale: {frm} }}, {{ scale: {to}, duration: {max(0.01, round(du, 3))}, ease: "{ease}" }}, {round(t, 3)});')
        else:
            ztl.append(f'      tl.to("#zw{n}", {{ scale: {to}, duration: {max(0.01, round(du, 3))}, ease: "{ease}" }}, {round(t, 3)});')
    html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0a2e; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0b0a2e; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
      .zw {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; will-change: transform; }}
      .zw video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}">
{chr(10).join(shots)}
{chr(10).join(hosts)}
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // punch-in zooms on the face (coordinate-target-zoom, origin = the face)
{chr(10).join(ztl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(html)


def main():
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    sfx_all = []
    for n, fn in enumerate([gfx01, gfx02, gfx03, gfx04, gfx05, gfx06, gfx07, gfx08, gfx09, gfx10], start=1):
        html, sfx = fn()
        open(os.path.join(ROOT, "compositions", f"gfx-{n:02d}.html"), "w").write(html)
        for item in sfx:
            t, name, vol, *rest = item
            sfx_all.append((SHOTS[n]["start"] + t, name, vol, *rest))
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(captions())
    index(sorted(sfx_all, key=lambda x: x[0]))
    print(f"index.html + 10 overlays + captions · total {TOTAL}s · {len(sfx_all)} sfx")


if __name__ == "__main__":
    main()
