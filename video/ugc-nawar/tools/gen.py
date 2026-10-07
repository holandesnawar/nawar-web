#!/usr/bin/env python3
"""Generate the UGC ad (v2) from edit.json: index.html (the girl, her framing, audio), one full-screen insert per
explanation (compositions/ins-NN.html), the enrolment card of the ending (compositions/outro.html) and the captions
(compositions/captions.html).

v2 language = the VSL's: PAPER ground (#F5F7FF + dots) for the problem, NAWAR BLUE (radial #025dc7 → #120081 + dots)
for the solution, Poppins for display, Inter for UI text, white cards with soft indigo shadows, real platform footage
in a browser window / phone, and no orange. While the girl talks to camera nothing covers her except the captions;
when she explains, the picture cuts to a full-screen insert and back.

Every cue is a word of the edit (edit.json, tools/edit.py), so a new cut regenerates in one run:
    python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
Templates use «NAME» tokens (cue times / palette), never str.format, so CSS/JS braces stay literal.
"""
import json, os, re, subprocess, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = json.load(open(os.path.join(ROOT, "edit.json")))
INS = {i["id"]: i for i in ED["inserts"]}
WORDS = ED["words"]
TOTAL = ED["total"]
RATE = ED["rate"]
FACE = (545, 900)                     # take B face centre (zoom origin)

PAL = dict(BLUE="#0b6df0", INDIGO="#1D0084", NAVY="#120081", SKY="#4da3ff", RED="#E02D3C", GREEN="#16A34A",
           INK="#0C0C1E", INK2="#374151", MUTED="#5A6480", PAPER="#F5F7FF", LINE="#DDE6F5", APP="#F1F2F8")


def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", t)


def cue(iid, word, k=0):
    """local time (s) of the k-th occurrence of `word` inside insert iid."""
    s = INS[iid]
    hits = [w for w in WORDS if s["start"] <= w["t"] < s["start"] + s["duration"] and norm(w["text"]) == norm(word)]
    return round(hits[k]["t"] - s["start"], 3)


def at(word, k=0):
    """absolute edit time of the k-th occurrence of `word`."""
    return [w["t"] for w in WORDS if norm(w["text"]) == norm(word)][k]


def sub(s, d):
    def f(m):
        v = {**PAL, **d}[m.group(1)]
        return ("%.3f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)
    return re.sub(r"«([A-Z][A-Z0-9_]*)»", f, s)


FONTS = "\n".join('    @font-face { font-family: "%s"; font-weight: %d; font-style: normal; src: url("assets/fonts/%s") format("woff2"); }'
                  % (f, w, fn) for f, w, fn in [("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 700, "poppins-latin-700-normal.woff2"),
                                                ("Poppins", 800, "poppins-latin-800-normal.woff2"), ("Poppins", 900, "poppins-latin-900-normal.woff2"),
                                                ("Inter", 500, "inter-latin-500-normal.woff2"), ("Inter", 600, "inter-latin-600-normal.woff2"),
                                                ("Inter", 700, "inter-latin-700-normal.woff2")])

# shared components (frame.md of the VSL, re-set for 1080×1920)
BASE = """
    #root { position: absolute; inset: 0; overflow: hidden; font-family: "Poppins", sans-serif; color: «INK»; }
    .«P»-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    .«P»-paper { background: «PAPER»; }
    .«P»-paper-light { position: absolute; inset: 0;
      background: radial-gradient(ellipse 70% 42% at 50% 34%, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0) 72%),
                  radial-gradient(ellipse 110% 90% at 50% 45%, rgba(29,0,132,0) 58%, rgba(29,0,132,0.07) 100%); }
    .«P»-paper-dots { position: absolute; left: -30px; top: -30px; width: 1140px; height: 1980px;
      background-image: radial-gradient(circle, rgba(29,0,132,0.075) 1.7px, transparent 1.9px); background-size: 30px 30px; }
    .«P»-blue { background: radial-gradient(circle at 50% 36%, #025dc7 0%, #120081 72%); }
    .«P»-blue-dots { position: absolute; left: -30px; top: -30px; width: 1140px; height: 1980px;
      background-image: radial-gradient(circle, rgba(255,255,255,0.07) 1.7px, transparent 1.9px); background-size: 30px 30px; }
    .«P»-blue-amb { position: absolute; left: 40px; top: 260px; width: 1000px; height: 900px; border-radius: 50%;
      background: radial-gradient(ellipse at 50% 50%, rgba(77,163,255,0.20) 0%, rgba(77,163,255,0.07) 45%, rgba(77,163,255,0) 70%); }
    .«P»-blue-vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 40%, rgba(4,0,40,0) 55%, rgba(4,0,40,0.40) 100%); }
    .«P»-card { position: absolute; background: #FFFFFF; border-radius: 32px; }
    .«P»-on-paper { box-shadow: 0 30px 80px rgba(18,0,129,0.16), 0 4px 14px rgba(18,0,129,0.08); }
    .«P»-on-blue { box-shadow: 0 40px 110px rgba(4,0,40,0.45), 0 8px 24px rgba(4,0,40,0.25); }
    .«P»-row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; }
    .«P»-pill { display: flex; align-items: center; gap: 14px; height: 60px; padding: 0 28px 0 20px; border-radius: 999px;
      background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); color: #FFFFFF; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 23px; line-height: 1; letter-spacing: 0.14em; text-transform: uppercase; }
    .«P»-pill svg { display: block; width: 28px; height: 28px; }
    .«P»-wpill { display: flex; align-items: center; gap: 16px; height: 72px; padding: 0 32px 0 18px; border-radius: 999px;
      background: #FFFFFF; color: «INDIGO»; white-space: nowrap; box-shadow: 0 16px 40px rgba(4,0,40,0.30);
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 30px; line-height: 1; letter-spacing: -0.005em; }
    .«P»-ipill { position: absolute; display: flex; align-items: center; gap: 12px; height: 56px; padding: 0 24px 0 14px; border-radius: 999px;
      background: «INDIGO»; color: #FFFFFF; white-space: nowrap; box-shadow: 0 8px 18px rgba(29,0,132,0.16), 0 0 0 5px #FFFFFF;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; line-height: 1; letter-spacing: 0.14em; }
    .«P»-flag { display: block; width: 40px; height: 27px; border-radius: 6px; overflow: hidden; flex: 0 0 40px; box-shadow: 0 0 0 2px rgba(255,255,255,0.85); }
    .«P»-flag svg { display: block; width: 40px; height: 27px; }
    .«P»-flagd { box-shadow: 0 0 0 2px rgba(12,12,30,0.08); }
    .«P»-av { position: absolute; width: 96px; height: 96px; border-radius: 50%; overflow: hidden;
      box-shadow: 0 0 0 6px #FFFFFF, 0 14px 30px rgba(18,0,129,0.18); }
    .«P»-av svg { display: block; width: 96px; height: 96px; }
    .«P»-bub { position: absolute; padding: 26px 36px; border-radius: 34px; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 40px; line-height: 1.22; letter-spacing: -0.01em; }
    .«P»-bub-w { background: #FFFFFF; color: «INK»; box-shadow: 0 24px 50px rgba(18,0,129,0.13), 0 4px 10px rgba(18,0,129,0.07); }
    .«P»-bub-g { background: #E8ECF7; color: «INK2»; }
    .«P»-bub-b { background: «BLUE»; color: #FFFFFF; box-shadow: 0 24px 50px rgba(4,0,40,0.35); }
    .«P»-bl { border-bottom-left-radius: 10px; }
    .«P»-br { border-bottom-right-radius: 10px; }
    .«P»-h1 { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 800; font-size: 84px; line-height: 1.05;
      letter-spacing: -0.03em; color: #FFFFFF; white-space: nowrap; }
    .«P»-chip { display: inline-block; padding: 0 22px 6px; border-radius: 18px; background: #FFFFFF; color: «INDIGO»; }
    .«P»-acc { color: «SKY»; }
    .«P»-w { display: inline-block; }
"""

# browser window chrome (the VSL's tools/mac_mockup.md, scaled with --u)
WIN_CSS = """
    .«P»-win { --u: calc(var(--sw) / 1120); position: absolute; width: calc(var(--u) * 1120); height: calc(var(--u) * 700);
      border-radius: calc(var(--u) * 14); overflow: hidden; background: #FFFFFF;
      box-shadow: 0 0 0 calc(var(--u) * 1) rgba(10,10,30,0.28), 0 calc(var(--u) * 34) calc(var(--u) * 90) rgba(4,0,40,0.50), 0 calc(var(--u) * 10) calc(var(--u) * 26) rgba(4,0,40,0.30); }
    .«P»-win-edge { position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: calc(var(--u) * 14); box-shadow: inset 0 0 0 calc(var(--u) * 1) rgba(255,255,255,0.45); }
    .«P»-chrome { position: absolute; left: 0; top: 0; width: calc(var(--u) * 1120); height: calc(var(--u) * 70); font-family: "Inter", sans-serif; }
    .«P»-tabs { position: absolute; left: 0; top: 0; width: 100%; height: calc(var(--u) * 36); background: #DEE1E6; }
    .«P»-tl { position: absolute; top: calc(var(--u) * 12); width: calc(var(--u) * 12); height: calc(var(--u) * 12); border-radius: 50%; }
    .«P»-tl-r { left: calc(var(--u) * 13); background: #FF5F57; }
    .«P»-tl-y { left: calc(var(--u) * 33); background: #FEBC2E; }
    .«P»-tl-g { left: calc(var(--u) * 53); background: #28C840; }
    .«P»-tab { position: absolute; left: calc(var(--u) * 82); top: calc(var(--u) * 7); width: calc(var(--u) * 232); height: calc(var(--u) * 29);
      border-radius: calc(var(--u) * 9) calc(var(--u) * 9) 0 0; background: #FFFFFF; }
    .«P»-fav { position: absolute; left: calc(var(--u) * 12); top: calc(var(--u) * 7); width: calc(var(--u) * 15); height: calc(var(--u) * 15);
      border-radius: calc(var(--u) * 3.5); overflow: hidden; background: radial-gradient(circle at 50% 45%, #2fb6f2 0%, #0b6df0 80%); }
    .«P»-fav img { position: absolute; left: calc(var(--u) * 1.2); top: calc(var(--u) * 5.2); width: calc(var(--u) * 12.6); height: auto; display: block; }
    .«P»-tab-t { position: absolute; left: calc(var(--u) * 35); top: 0; height: calc(var(--u) * 29); line-height: calc(var(--u) * 29);
      font-size: calc(var(--u) * 12); font-weight: 500; color: #202124; white-space: nowrap; }
    .«P»-bar { position: absolute; left: 0; top: calc(var(--u) * 36); width: 100%; height: calc(var(--u) * 34); background: #FFFFFF; box-shadow: inset 0 calc(var(--u) * -1) 0 #DADCE0; }
    .«P»-url { position: absolute; left: calc(var(--u) * 102); top: calc(var(--u) * 4); width: calc(var(--u) * 962); height: calc(var(--u) * 26);
      border-radius: calc(var(--u) * 13); background: #F1F3F4; }
    .«P»-url-t { position: absolute; left: calc(var(--u) * 33); top: 0; height: calc(var(--u) * 26); line-height: calc(var(--u) * 26);
      font-size: calc(var(--u) * 13); font-weight: 500; color: #202124; white-space: nowrap; }
    .«P»-lock { position: absolute; left: calc(var(--u) * 12); top: calc(var(--u) * 6.5); width: calc(var(--u) * 13); height: calc(var(--u) * 13); }
    .«P»-content { position: absolute; left: 0; top: calc(var(--u) * 70); width: calc(var(--u) * 1120); height: calc(var(--u) * 630); overflow: hidden; background: #FFFFFF; }
    .«P»-media { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
"""


def win(P, wid, sw, left, top, content):
    return f"""<div id="{P}-{wid}" class="{P}-win" style="--sw:{sw}px; left:{left}px; top:{top}px;">
        <div class="{P}-chrome">
          <div class="{P}-tabs"><i class="{P}-tl {P}-tl-r"></i><i class="{P}-tl {P}-tl-y"></i><i class="{P}-tl {P}-tl-g"></i>
            <div class="{P}-tab"><div class="{P}-fav"><img src="assets/img/logo-nawar.png" alt="" /></div><div class="{P}-tab-t">Holandés Nawar</div></div></div>
          <div class="{P}-bar"><div class="{P}-url"><svg class="{P}-lock" viewBox="0 0 13 13"><path d="M4.3 6 V4.3 A2.2 2.2 0 0 1 8.7 4.3 V6" fill="none" stroke="#5F6368" stroke-width="1.3" /><rect x="2.6" y="5.8" width="7.8" height="5.9" rx="1.3" fill="#5F6368" /></svg><div class="{P}-url-t">app.holandesnawar.com</div></div></div>
        </div>
        <div class="{P}-content">{content}</div>
        <div class="{P}-win-edge"></div>
      </div>"""


def ground(P, kind):
    if kind == "paper":
        return f'    <div class="{P}-full {P}-paper"><div class="{P}-paper-dots"></div><div class="{P}-paper-light"></div></div>'
    return f'    <div class="{P}-full {P}-blue"><div class="{P}-blue-dots"></div><div class="{P}-blue-amb"></div><div class="{P}-blue-vig"></div></div>'


FLAG_NL = '<svg viewBox="0 0 40 27"><rect width="40" height="9" fill="#AE1C27" /><rect y="9" width="40" height="9" fill="#FFFFFF" /><rect y="18" width="40" height="9" fill="#21468C" /></svg>'
FLAG_ES = '<svg viewBox="0 0 40 27"><rect width="40" height="27" fill="#AA151B" /><rect y="7" width="40" height="13" fill="#F1BF00" /></svg>'


def person(fg="#FFFFFF"):
    return f'<svg viewBox="0 0 96 96"><circle cx="48" cy="38" r="17.5" fill="{fg}" /><path d="M13 101 C13 75 29 62 48 62 C67 62 83 75 83 101 Z" fill="{fg}" /></svg>'


ICON = {
    "steth": '<svg viewBox="0 0 120 120"><g fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><path d="M34 18 V48 A23 23 0 0 0 80 48 V18"/><path d="M57 71 V84 A16 16 0 0 0 89 84 V77"/><circle cx="89" cy="64" r="12"/></g></svg>',
    "phone": '<svg viewBox="0 0 48 48"><path d="M15.5 6.5 l5 9 -3.2 3.4 c2.2 4.6 5.6 8 10.2 10.2 l3.4 -3.2 9 5 -2.2 7.6 c-0.4 1.3 -1.6 2.1 -3 2 C19 39.4 8.6 29 7.5 14.6 c-0.1 -1.4 0.7 -2.6 2 -3 z" fill="#FFFFFF"/></svg>',
    "check": '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="«GREEN»"/><path d="M18 33 L28 43 L47 22" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "checkw": '<svg viewBox="0 0 64 64"><path d="M16 33 L28 45 L49 21" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "play": '<svg viewBox="0 0 28 28"><circle cx="14" cy="14" r="13" fill="#FFFFFF"/><path d="M11 8.5 L19.5 14 L11 19.5 Z" fill="«INDIGO»"/></svg>',
    "book": '<svg viewBox="0 0 48 48"><path d="M6 10 Q16 6 24 12 Q32 6 42 10 V38 Q32 34 24 40 Q16 34 6 38 Z" fill="none" stroke="currentColor" stroke-width="4.2" stroke-linejoin="round"/><path d="M24 12 V40" stroke="currentColor" stroke-width="4.2"/></svg>',
    "pen": '<svg viewBox="0 0 48 48"><path d="M10 38 L12 30 L32 10 L38 16 L18 36 Z" fill="none" stroke="currentColor" stroke-width="4.2" stroke-linejoin="round"/><path d="M28 14 L34 20" stroke="currentColor" stroke-width="4.2"/></svg>',
    "ear": '<svg viewBox="0 0 48 48"><path d="M10 29 V24 A14 14 0 0 1 38 24 V29" fill="none" stroke="currentColor" stroke-width="4.2"/><rect x="7" y="27" width="9" height="13" rx="4" fill="currentColor"/><rect x="32" y="27" width="9" height="13" rx="4" fill="currentColor"/></svg>',
    "trans": '<svg viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 10 H24 M15 6 V10 M10 10 C11 17 16 22 22 24 M20 10 C19 17 14 22 8 25"/><path d="M26 42 L33 24 L40 42 M28.5 36 H37.5"/></g></svg>',
    "down": '<svg viewBox="0 0 48 48"><path d="M24 8 V38 M12 27 L24 39 L36 27" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "chev": '<svg viewBox="0 0 120 70"><path d="M14 12 L60 56 L106 12" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "mic": '<svg viewBox="0 0 48 48"><rect x="18" y="7" width="12" height="22" rx="6" fill="#FFFFFF"/><path d="M12 23 A12 12 0 0 0 36 23 M24 35 V41" fill="none" stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round"/></svg>',
    "cam": '<svg viewBox="0 0 48 48"><rect x="6" y="14" width="25" height="20" rx="5" fill="#FFFFFF"/><path d="M31 21 L42 15 V33 L31 27 Z" fill="#FFFFFF"/></svg>',
    "hang": '<svg viewBox="0 0 48 48"><path d="M6 27 C14 18 34 18 42 27 l-3.5 5.5 -7 -2.5 -0.5 -4.5 C27 24.5 21 24.5 17 25.5 l-0.5 4.5 -7 2.5 z" fill="#FFFFFF"/></svg>',
    "cursor": '<svg viewBox="0 0 40 52"><path d="M4 3 L4 41 L14 32 L21 48 L28 45 L21 29 L35 29 Z" fill="#FFFFFF" stroke="#0C0C1E" stroke-width="3" stroke-linejoin="round"/></svg>',
}


def icon(name):
    return sub(ICON[name], {})


def comp(cid, d, P, css, body, js, cues=None, extra_css=""):
    cues = dict(cues or {}, P=P, D=float(d))
    return sub("""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
""" + FONTS + BASE + extra_css + css + """
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


def typing_js(el_id, text, t0, t1):
    """discrete-text-sequence: the text grows with a proxy, one state per character (seek-safe)."""
    return sub("""
      (() => {
        const el = q("«EL»"), full = «TXT»; const typ = { n: 0 };
        el.textContent = "";
        tl.fromTo(typ, { n: 0 }, { n: full.length, duration: «DUR», ease: "none", immediateRender: false,
          onUpdate: () => { el.textContent = full.slice(0, Math.round(typ.n)); } }, «T0»);
      })();
""", dict(EL=el_id, TXT=json.dumps(text, ensure_ascii=False), DUR=float(t1 - t0), T0=float(t0)))


def blink_js(el_id, t0, t1, period=0.5):
    """a caret that blinks with discrete sets (no repeat/yoyo)."""
    out, t, on = [], t0, True
    while t < t1:
        out.append(f'      tl.set(q("{el_id}"), {{ opacity: {1 if on else 0} }}, {t:.3f});')
        t += period / 2; on = not on
    return "\n".join(out) + "\n"


# call card shared by ins-01 (ringing → answered) and ins-06 (in call)
CALL_CSS = """
    .«P»-call-av { position: absolute; left: 32px; top: 33px; width: 104px; height: 104px; border-radius: 50%; background: «INDIGO»; }
    .«P»-call-av svg { position: absolute; left: 18px; top: 18px; width: 68px; height: 68px; }
    .«P»-ring { position: absolute; left: 32px; top: 33px; width: 104px; height: 104px; border-radius: 50%; border: 5px solid «BLUE»; box-sizing: border-box; opacity: 0; }
    .«P»-call-name { position: absolute; left: 168px; top: 30px; font-weight: 700; font-size: 46px; line-height: 1.15; letter-spacing: -0.02em; color: «INK»; white-space: nowrap; }
    .«P»-call-st { position: absolute; left: 170px; top: 98px; display: flex; align-items: center; gap: 12px; font-family: "Inter", sans-serif;
      font-weight: 600; font-size: 29px; line-height: 1.1; color: «MUTED»; white-space: nowrap; }
    .«P»-dot { display: block; width: 14px; height: 14px; border-radius: 50%; background: «GREEN»; }
    .«P»-call-btn { position: absolute; right: 34px; top: 40px; width: 90px; height: 90px; border-radius: 50%; background: «GREEN»;
      box-shadow: 0 12px 26px rgba(22,163,74,0.35); }
    .«P»-call-btn svg { position: absolute; left: 21px; top: 21px; width: 48px; height: 48px; }
"""


def call_card(P, left, top, status_html, extra=""):
    return f"""    <div id="{P}-call" class="{P}-card {P}-on-paper" style="left:{left}px; top:{top}px; width:900px; height:170px;">
      <div class="{P}-ring" id="{P}-ring1"></div><div class="{P}-ring" id="{P}-ring2"></div>
      <div class="{P}-call-av">{icon('steth')}</div>
      <div class="{P}-call-name">Huisarts</div>
      {status_html}
      <div class="{P}-call-btn">{icon('phone')}</div>{extra}
    </div>"""


# ============================================================================== ins-01 · practicas, llamas… te bloqueas
def ins01():
    iid, P = "ins-01", "i1"; d = INS[iid]["duration"]
    c = dict(PRA=cue(iid, "practicas"), FRA=cue(iid, "frase"), LLA=cue(iid, "llamas"), CON=cue(iid, "contestan"),
             BLO=cue(iid, "bloqueas"))
    c["TE2"] = cue(iid, "te", 1)
    css = CALL_CSS + """
    #i1-note { left: 90px; top: 296px; width: 900px; height: 284px; }
    #i1-tag { left: 130px; top: 266px; }
    #i1-note-t { position: absolute; left: 50px; top: 70px; width: 810px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 56px;
      line-height: 1.2; letter-spacing: -0.015em; color: «INK»; }
    #i1-note-g { position: absolute; left: 52px; top: 218px; font-family: "Inter", sans-serif; font-weight: 500; font-size: 31px; color: «MUTED»; white-space: nowrap; }
    #i1-b1 { left: 214px; top: 846px; transform-origin: 0% 100%; }
    #i1-av1 { left: 90px; top: 858px; background: #9fd5f5; }
    #i1-b2 { right: 214px; top: 1014px; min-width: 260px; transform-origin: 100% 100%; }
    #i1-av2 { right: 90px; top: 1026px; background: «INDIGO»; }
    #i1-caret { display: inline-block; width: 5px; height: 46px; margin-left: 4px; border-radius: 3px; background: «INDIGO»; vertical-align: -6px; }
    #i1-stamp { position: absolute; left: 330px; top: 1098px; width: 400px; height: 104px; border-radius: 20px; box-sizing: border-box;
      border: 7px solid «RED»; background: rgba(255,255,255,0.86); display: flex; align-items: center; justify-content: center; }
    #i1-stamp-t { font-weight: 800; font-size: 60px; line-height: 1; letter-spacing: 0.06em; padding-left: 0.06em; padding-top: 6px;
      color: rgba(224,45,60,0.12); -webkit-text-stroke: 3px «RED»; white-space: nowrap; }
"""
    body = "\n".join([ground(P, "paper"),
        f"""    <div id="i1-note" class="i1-card i1-on-paper">
      <div id="i1-note-t"></div>
      <div id="i1-note-g">Quiero pedir una cita.</div>
    </div>
    <div id="i1-tag" class="i1-ipill"><span class="i1-flag">{FLAG_NL}</span><span>TU FRASE</span></div>""",
        call_card(P, 90, 638, '<div class="i1-call-st" id="i1-st1">Llamando…</div><div class="i1-call-st" id="i1-st2"><span class="i1-dot"></span>En llamada · 00:01</div>'),
        f"""    <div id="i1-av1" class="i1-av">{person()}</div>
    <div id="i1-b1" class="i1-bub i1-bub-w i1-bl">Huisartsenpraktijk, goedemorgen!</div>
    <div id="i1-av2" class="i1-av">{person()}</div>
    <div id="i1-b2" class="i1-bub i1-bub-w i1-br"><span id="i1-b2-t"></span><span id="i1-caret"></span></div>
    <div id="i1-stamp"><div id="i1-stamp-t">BLOQUEO</div></div>"""])
    js = """
      tl.fromTo(q("note"), { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.34, ease: "power3.out" }, 0);
      tl.fromTo(q("tag"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 0.08);
""" + typing_js("note-t", "Ik wil graag een afspraak maken.", 0.1, c["FRA"] + 0.12) + """
      tl.fromTo(q("call"), { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }, «LLA» - 0.08);
      tl.fromTo(q("st2"), { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);
      tl.fromTo(q("ring1"), { opacity: 0.55, scale: 1 }, { opacity: 0, scale: 1.7, duration: 0.6, ease: "power2.out" }, «LLA»);
      tl.fromTo(q("ring2"), { opacity: 0.55, scale: 1 }, { opacity: 0, scale: 1.7, duration: 0.6, ease: "power2.out" }, «LLA» + 0.42);
      tl.to(q("st1"), { opacity: 0, duration: 0.1 }, «CON» - 0.06);
      tl.to(q("st2"), { opacity: 1, duration: 0.12 }, «CON» - 0.02);
      tl.fromTo(q("av1"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «CON» - 0.04);
      tl.fromTo(q("b1"), { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, «CON»);
      tl.fromTo(q("av2"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)" }, «TE2» - 0.08);
      tl.fromTo(q("b2"), { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(1.6)" }, «TE2» - 0.04);
""" + typing_js("b2-t", "Ik… eh…", c["TE2"] - 0.02, c["BLO"] + 0.3) + blink_js("caret", c["BLO"] + 0.32, d, 0.44) + """
      tl.fromTo(q("stamp"), { opacity: 0, scale: 1.55, rotation: -7 }, { opacity: 1, scale: 1, rotation: -7, duration: 0.2, ease: "power4.out" }, «BLO» + 0.04);
      tl.fromTo(q("b2"), { x: 0 }, { keyframes: [{ x: -9, duration: 0.05 }, { x: 8, duration: 0.05 }, { x: -5, duration: 0.05 }, { x: 0, duration: 0.05 }], immediateRender: false }, «BLO» + 0.2);
"""
    sfx = [(0.1, "typing", 0.2, c["FRA"]), (c["LLA"], "ringback", 0.3), (c["CON"], "pop", 0.26), (c["BLO"] + 0.04, "error", 0.24)]
    return comp(iid, d, P, css, body, js, c), sfx


# ============================================================================== ins-02 · alguien te traduce o te cambia al inglés
def ins02():
    iid, P = "ins-02", "i2"; d = INS[iid]["duration"]
    c = dict(POR=cue(iid, "porque"), QUE=cue(iid, "que", 0), O=cue(iid, "o"), CAM=cue(iid, "cambia"), ING=cue(iid, "ingles"))
    css = """
    #i2-av1 { left: 90px; top: 392px; background: #9fd5f5; }
    #i2-b1 { left: 214px; top: 380px; transform-origin: 0% 100%; }
    #i2-nl { left: 254px; top: 348px; }
    #i2-lab { position: absolute; right: 214px; top: 610px; display: flex; align-items: center; gap: 10px; color: «MUTED»;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 23px; letter-spacing: 0.14em; white-space: nowrap; }
    #i2-lab svg { display: block; width: 34px; height: 34px; }
    #i2-av2 { right: 90px; top: 672px; background: «MUTED»; }
    #i2-b2 { right: 214px; top: 660px; transform-origin: 100% 100%; }
    #i2-stack { position: absolute; left: 214px; top: 940px; width: 760px; height: 160px; }
    .i2-ghost { position: absolute; left: 0; top: 0; }
    #i2-av3 { left: 90px; top: 952px; background: #9fd5f5; }
    #i2-b3 { left: 0; top: 0; transform-origin: 0% 100%; }
    #i2-en { left: 254px; top: 908px; }
"""
    b3txt = "Oh, let’s just speak English!"
    body = "\n".join([ground(P, "paper"), f"""    <div id="i2-av1" class="i2-av">{person()}</div>
    <div id="i2-b1" class="i2-bub i2-bub-w i2-bl">Wat is uw geboortedatum?</div>
    <div id="i2-nl" class="i2-ipill"><span class="i2-flag">{FLAG_NL}</span><span>NL</span></div>
    <div id="i2-lab">{icon('trans')}<span>TE TRADUCEN</span></div>
    <div id="i2-av2" class="i2-av">{person()}</div>
    <div id="i2-b2" class="i2-bub i2-bub-g i2-br">Te pide tu fecha de nacimiento.</div>
    <div id="i2-stack">
      <div id="i2-g2" data-layout-allow-overlap class="i2-ghost i2-bub i2-bub-w i2-bl">{b3txt}</div>
      <div id="i2-g1" data-layout-allow-overlap class="i2-ghost i2-bub i2-bub-w i2-bl">{b3txt}</div>
      <div id="i2-b3" class="i2-bub i2-bub-w i2-bl">{b3txt}</div>
    </div>
    <div id="i2-av3" class="i2-av">{person()}</div>
    <div id="i2-en" class="i2-ipill"><span class="i2-flag">{FLAG_EN}</span><span>EN</span></div>"""])
    js = """
      tl.fromTo(q("av1"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 0);
      tl.fromTo(q("b1"), { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, 0.04);
      tl.fromTo(q("nl"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)" }, 0.14);
      tl.fromTo(q("lab"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «QUE» - 0.1);
      tl.fromTo(q("av2"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «QUE» - 0.06);
      tl.fromTo(q("b2"), { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, «QUE» - 0.02);
      tl.to([q("av1"), q("b1"), q("nl"), q("lab"), q("av2"), q("b2")], { opacity: 0.42, duration: 0.25, ease: "power2.out" }, «O» - 0.04);
      tl.fromTo(q("av3"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «O» - 0.06);
      tl.fromTo(q("b3"), { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, «O» - 0.02);
      tl.fromTo(q("en"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)" }, «O» + 0.1);
      tl.fromTo(q("g1"), { opacity: 0, y: 0, scale: 1 }, { opacity: 0.6, y: 18, scale: 0.97, duration: 0.3, ease: "power3.out" }, «ING» - 0.06);
      tl.fromTo(q("g2"), { opacity: 0, y: 0, scale: 1 }, { opacity: 0.32, y: 36, scale: 0.94, duration: 0.34, ease: "power3.out" }, «ING» + 0.04);
"""
    sfx = [(0.04, "pop", 0.24), (c["QUE"], "pop", 0.22), (c["O"], "pop", 0.26)]
    return comp(iid, d, P, css, body, js, c), sfx


FLAG_EN = ('<svg viewBox="0 0 40 27"><rect width="40" height="27" fill="#012169"/><path d="M0 0 L40 27 M40 0 L0 27" stroke="#FFFFFF" stroke-width="5"/>'
           '<path d="M0 0 L40 27 M40 0 L0 27" stroke="#C8102E" stroke-width="2"/><path d="M20 0 V27 M0 13.5 H40" stroke="#FFFFFF" stroke-width="8"/>'
           '<path d="M20 0 V27 M0 13.5 H40" stroke="#C8102E" stroke-width="4.5"/></svg>')


# ============================================================================== ins-03 · profesores nativos → lecciones grabadas
def ins03():
    """The recorded-lesson video (paul-clase-2, the VSL's «vídeos del curso»; the live class at ins-05 uses the other
    one): first Paul's webcam big in a card, then the card flies into its place inside the lesson player (same video,
    same instant, so the hand-off is seamless) and the browser window reveals the whole lesson."""
    iid, P = "ins-03", "i3"; d = INS[iid]["duration"]
    c = dict(EXP=cue(iid, "expertos"), DOM=cue(iid, "dominan"), CUE=cue(iid, "cuentas"), CUA=cue(iid, "cuando"))
    c["SWAP"] = round(c["CUE"] - 0.12, 3)
    M0 = 0.5                                                   # media time at local 0 (both copies stay in sync)
    # webcam inside paul-clase-2 (2424×1238), inset past its rounded corners
    WX0, WY0, WX1, WY1 = 354, 94, 736, 304
    CW = 800; k = CW / (WX1 - WX0); CH = round((WY1 - WY0) * k, 1)
    CL, CT = 140, 360                                          # card on screen
    # the same webcam inside the window: --sw 960 → chrome 60 px, content 960×540, video object-fit: cover
    WL, WT = 60, 296
    kc = 540 / 1238; ox = -(2424 * kc - 960) / 2
    tx = WL + WX0 * kc + ox; ty = WT + 60 + WY0 * kc; s_end = (WX1 - WX0) * kc / CW
    c.update(CH=CH, VW=round(2424 * k, 1), VH=round(1238 * k, 1), VL=round(-WX0 * k, 1), VT=round(-WY0 * k, 1),
             CL=CL, CT=CT, FX=round(tx - CL, 2), FY=round(ty - CT, 2), FS=round(s_end, 4), M0=M0,
             LAND=round(c["SWAP"] + 0.6, 3), CVD=round(c["SWAP"] + 0.8, 3), WST=round(c["SWAP"] - 0.06, 3),
             WMS=round(M0 + c["SWAP"] - 0.06, 3), WD=round(d - c["SWAP"] + 0.1, 3))
    css = WIN_CSS + """
    #i3-card { left: «CL»px; top: «CT»px; width: 800px; height: «CH»px; overflow: hidden; border-radius: 36px; background: #0C0C1E; transform-origin: 0% 0%; }
    #i3-cv { position: absolute; left: «VL»px; top: «VT»px; width: «VW»px; height: «VH»px; }
    #i3-cgrad { position: absolute; left: 0; bottom: 0; width: 800px; height: 200px; background: linear-gradient(180deg, rgba(4,0,40,0) 0%, rgba(4,0,40,0.6) 100%); }
    #i3-cedge { position: absolute; inset: 0; border-radius: 36px; box-shadow: inset 0 0 0 2px rgba(255,255,255,0.22); }
    #i3-name { position: absolute; left: 40px; bottom: 84px; font-weight: 700; font-size: 42px; line-height: 1; color: #FFFFFF; white-space: nowrap; }
    #i3-role { position: absolute; left: 42px; bottom: 44px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 26px; line-height: 1; color: rgba(255,255,255,0.8); white-space: nowrap; }
    #i3-p1row { top: 852px; }
    #i3-p2row { top: 940px; }
    #i3-lrow { top: 208px; }
    #i3-lz { position: absolute; left: 0; top: 0; width: 100%; height: 100%; transform-origin: 58% 42%; }
    #i3-phone { position: absolute; left: 712px; top: 594px; width: 300px; height: 618px; border-radius: 54px; background: #0C0C1E;
      box-shadow: 0 40px 100px rgba(4,0,40,0.55), 0 0 0 2px rgba(255,255,255,0.10); }
    #i3-screen { position: absolute; left: 14px; top: 14px; width: 272px; height: 590px; border-radius: 42px; overflow: hidden; background: #FFFFFF; }
    #i3-shot { position: absolute; left: 0; top: 0; width: 272px; height: 592px; display: block; }
    #i3-notch { position: absolute; left: 96px; top: 12px; width: 80px; height: 22px; border-radius: 11px; background: #0C0C1E; }
"""
    body = "\n".join([ground(P, "blue"), f"""    <div id="i3-s2" class="i3-full">
      <div id="i3-lrow" class="i3-row"><div id="i3-lp" class="i3-pill">{icon('play')}<span>Lecciones grabadas</span></div></div>
      """ + win(P, "win", 960, WL, WT, '<div id="i3-lz"><video id="i3-lv" class="clip i3-media" src="assets/video/paul-clase-2.mp4" muted playsinline data-start="«WST»" data-duration="«WD»" data-media-start="«WMS»" data-track-index="2" data-hf-media-start-basis="local"></video></div>') + f"""
      <div id="i3-phone"><div id="i3-screen"><img id="i3-shot" src="assets/img/ui-curso-movil.png" alt="" /></div><div id="i3-notch"></div></div>
    </div>
    <div id="i3-s1" class="i3-full">
      <div id="i3-card" class="i3-card i3-on-blue">
        <video id="i3-cv" class="clip" src="assets/video/paul-clase-2.mp4" muted playsinline data-start="0" data-duration="«CVD»" data-media-start="«M0»" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video>
        <div id="i3-cgrad"></div><div id="i3-cedge"></div>
        <div id="i3-name">Paul</div><div id="i3-role">Profesor de Nawar</div>
      </div>
      <div id="i3-p1row" class="i3-row"><div id="i3-p1" class="i3-wpill"><span class="i3-flag i3-flagd">{FLAG_NL}</span><span>Profesores nativos holandeses</span></div></div>
      <div id="i3-p2row" class="i3-row"><div id="i3-p2" class="i3-wpill"><span class="i3-flag i3-flagd">{FLAG_ES}</span><span>Expertos en español</span></div></div>
    </div>"""])
    js = """
      tl.fromTo(q("card"), { opacity: 0, y: 60, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out" }, 0);
      tl.fromTo(q("p1"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «EXP» - 0.04);
      tl.fromTo(q("p2"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «DOM» - 0.04);
      // the card flies into the webcam of the lesson player (match cut on the same frame)
      tl.to([q("p1"), q("p2"), q("name"), q("role"), q("cgrad")], { opacity: 0, duration: 0.16, ease: "power2.out" }, «SWAP» - 0.12);
      tl.fromTo(q("s2"), { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, «SWAP»);
      tl.to(q("card"), { x: «FX», y: «FY», scale: «FS», duration: 0.6, ease: "power3.inOut" }, «SWAP»);
      tl.to(q("card"), { opacity: 0, duration: 0.12, ease: "none" }, «LAND»);
      tl.fromTo(q("lp"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «SWAP» + 0.3);
      tl.fromTo(q("lz"), { scale: 1 }, { scale: 1.14, duration: «D» - «LAND», ease: "power1.inOut" }, «LAND»);
      tl.fromTo(q("phone"), { opacity: 0, x: 160, rotation: 7 }, { opacity: 1, x: 0, rotation: 0, duration: 0.46, ease: "power3.out" }, «CUA» - 0.16);
      tl.fromTo(q("shot"), { y: 0 }, { y: -40, duration: «D» - «CUA», ease: "power1.inOut" }, «CUA» + 0.1);
"""
    sfx = [(c["EXP"] - 0.04, "click-soft", 0.24), (c["DOM"] - 0.04, "click-soft", 0.24), (c["SWAP"], "whoosh-short", 0.14), (c["CUA"] - 0.16, "pop", 0.2)]
    return comp(iid, d, P, css, body, js, c), sfx


# ============================================================================== ins-04 · leer, escribir, oído — no un test
def ins04():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(LEE=cue(iid, "leer"), ESC=cue(iid, "escribir"), ENT=cue(iid, "entrenar"), OID=cue(iid, "oido"), EN=cue(iid, "en"),
             TES=cue(iid, "test"))
    # crops (source px) → inner width 860
    IW = 860
    def crop(x0, y0, x1, y1, W, H):
        k = IW / (x1 - x0)
        return dict(w=round(W * k, 1), h=round(H * k, 1), l=round(-x0 * k, 1), t=round(-y0 * k, 1), ih=round((y1 - y0) * k, 1))
    L = crop(244, 280, 1816, 940, 2048, 1447)
    E = crop(592, 0, 1474, 336, 1718, 690)
    O = crop(74, 22, 1860, 690, 1902, 1080)
    c.update(LIH=L["ih"], EIH=E["ih"], OIH=O["ih"], ED=round(d - c["ESC"] + 0.2, 3), EST=round(max(0.0, c["ESC"] - 0.12), 3))
    css = f"""
    #i4-h1 {{ top: 200px; }}
    #i4-h2 {{ top: 312px; }}
    .i4-card {{ position: absolute; left: 80px; top: 488px; width: 920px; border-radius: 34px; background: «APP»; transform-origin: 50% 0%;
      box-shadow: 0 40px 100px rgba(4,0,40,0.45), 0 8px 24px rgba(4,0,40,0.22); }}
    .i4-in {{ position: absolute; left: 30px; top: 30px; width: {IW}px; overflow: hidden; border-radius: 20px; background: #FFFFFF;
      box-shadow: 0 0 0 1px rgba(29,0,132,0.07); }}
    #i4-cl {{ height: {L['ih'] + 60}px; }} #i4-cl .i4-in {{ height: {L['ih']}px; }}
    #i4-ce {{ height: {E['ih'] + 60}px; }} #i4-ce .i4-in {{ height: {E['ih']}px; }}
    #i4-co {{ height: {O['ih'] + 60}px; }} #i4-co .i4-in {{ height: {O['ih']}px; }}
    #i4-il {{ position: absolute; left: {L['l']}px; top: {L['t']}px; width: {L['w']}px; height: {L['h']}px; display: block; }}
    #i4-ve {{ position: absolute; left: {E['l']}px; top: {E['t']}px; width: {E['w']}px; height: {E['h']}px; }}
    #i4-io {{ position: absolute; left: {O['l']}px; top: {O['t']}px; width: {O['w']}px; height: {O['h']}px; display: block; }}
    #i4-skills {{ top: 1000px; gap: 18px; }}
    .i4-sk {{ display: flex; align-items: center; gap: 12px; height: 70px; padding: 0 28px 0 16px; border-radius: 999px;
      background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); color: #FFFFFF; white-space: nowrap;
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 31px; line-height: 1; }}
    .i4-ic {{ position: relative; width: 44px; height: 44px; }}
    .i4-ic svg {{ position: absolute; left: 0; top: 0; width: 44px; height: 44px; }}
    .i4-ok {{ opacity: 0; }}
    #i4-test {{ top: 1100px; }}
    #i4-tp {{ position: relative; display: flex; align-items: center; gap: 12px; height: 62px; padding: 0 26px 0 18px; border-radius: 999px;
      background: rgba(255,255,255,0.08); border: 1px dashed rgba(255,255,255,0.35); color: rgba(255,255,255,0.72); white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; letter-spacing: 0.12em; }}
    .i4-opt {{ display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%;
      border: 2px solid rgba(255,255,255,0.45); font-size: 20px; letter-spacing: 0; }}
    #i4-strike {{ position: absolute; left: -10px; top: 28px; width: calc(100% + 20px); height: 7px; border-radius: 4px; background: «RED»; transform-origin: 0% 50%; }}
"""
    def skill(k, ic, label):
        return (f'<div id="i4-s{k}" class="i4-sk"><div class="i4-ic"><div id="i4-n{k}">{icon(ic)}</div>'
                f'<div id="i4-k{k}" class="i4-ok">{icon("check")}</div></div><span>{label}</span></div>')
    body = "\n".join([ground(P, "blue"), f"""    <div id="i4-h1" class="i4-h1">Ejercicios</div>
    <div id="i4-h2" class="i4-h1"><span id="i4-chip" class="i4-chip">de verdad</span></div>
    <div id="i4-cl" class="i4-card"><div class="i4-in"><img id="i4-il" src="assets/img/ui-lezen-texto.png" alt="" /></div></div>
    <div id="i4-ce" class="i4-card"><div class="i4-in"><video id="i4-ve" class="clip" src="assets/video/completa-frase.mp4" muted playsinline data-start="«EST»" data-duration="«ED»" data-media-start="5.6" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video></div></div>
    <div id="i4-co" class="i4-card"><div class="i4-in"><img id="i4-io" src="assets/img/ui-luisteren-audio.png" alt="" /></div></div>
    <div id="i4-skills" class="i4-row">{skill(1, 'book', 'Leer')}{skill(2, 'pen', 'Escribir')}{skill(3, 'ear', 'Escuchar')}</div>
    <div id="i4-test" class="i4-row"><div id="i4-tp"><span class="i4-opt">A</span><span class="i4-opt">B</span><span class="i4-opt">C</span><span class="i4-opt">D</span><span>TIPO TEST</span><div id="i4-strike"></div></div></div>"""])
    js = """
      tl.fromTo(q("h1"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("chip"), { opacity: 0, scale: 0.7, rotation: -1.5 }, { opacity: 1, scale: 1, rotation: -1.5, duration: 0.32, ease: "back.out(1.8)" }, 0.08);
      tl.fromTo(q("cl"), { opacity: 0, y: 90 }, { opacity: 1, y: 0, duration: 0.36, ease: "power3.out" }, «LEE» - 0.1);
      tl.fromTo(q("ce"), { opacity: 0, y: 110 }, { opacity: 1, y: 0, duration: 0.36, ease: "power3.out" }, «ESC» - 0.1);
      tl.to(q("cl"), { y: -34, scale: 0.94, opacity: 0.55, duration: 0.36, ease: "power3.out" }, «ESC» - 0.1);
      tl.fromTo(q("co"), { opacity: 0, y: 110 }, { opacity: 1, y: 0, duration: 0.36, ease: "power3.out" }, «ENT» - 0.08);
      tl.to(q("ce"), { y: -34, scale: 0.94, opacity: 0.55, duration: 0.36, ease: "power3.out" }, «ENT» - 0.08);
      tl.to(q("cl"), { y: -62, scale: 0.88, opacity: 0.25, duration: 0.36, ease: "power3.out" }, «ENT» - 0.08);
      tl.fromTo(q("skills"), { opacity: 0 }, { opacity: 1, duration: 0.01 }, 0);
      tl.fromTo(q("s1"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, «LEE» - 0.06);
      tl.fromTo(q("s2"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, «ESC» - 0.06);
      tl.fromTo(q("s3"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, «OID» - 0.06);
      tl.to(q("n1"), { opacity: 0, duration: 0.1 }, «LEE» + 0.24); tl.fromTo(q("k1"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.26, ease: "back.out(2.2)" }, «LEE» + 0.24);
      tl.to(q("n2"), { opacity: 0, duration: 0.1 }, «ESC» + 0.3); tl.fromTo(q("k2"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.26, ease: "back.out(2.2)" }, «ESC» + 0.3);
      tl.to(q("n3"), { opacity: 0, duration: 0.1 }, «OID» + 0.2); tl.fromTo(q("k3"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.26, ease: "back.out(2.2)" }, «OID» + 0.2);
      tl.fromTo(q("tp"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.26, ease: "power3.out" }, «EN» - 0.06);
      tl.fromTo(q("strike"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power2.out" }, «TES» - 0.04);
      tl.to(q("tp"), { opacity: 0.55, duration: 0.2 }, «TES» + 0.18);
"""
    sfx = [(c["LEE"] - 0.1, "click-soft", 0.22), (c["ESC"] - 0.1, "click-soft", 0.22), (c["ENT"] - 0.08, "click-soft", 0.22), (c["TES"] - 0.04, "click", 0.2)]
    return comp(iid, d, P, css, body, js, c), sfx


# ============================================================================== ins-05 · clase en directo → pronunciación
def ins05():
    iid, P = "ins-05", "i5"; d = INS[iid]["duration"]
    c = dict(DIR=cue(iid, "directo"), REF=cue(iid, "reforzar"), TRA=cue(iid, "trabajar"), PRO=cue(iid, "pronunciacion"))
    c["SWAP"] = round(c["TRA"] - 0.16, 3)
    c["VD"] = round(c["SWAP"] + 0.3, 3)
    # player region of paul-clase-1 (x 744–2480, y 10–970) covering a 960×504 area
    k = 960 / 1736
    c.update(VW=round(2502 * k, 1), VH=round(992 * k, 1), VL=round(-744 * k, 1), VT=round(-10 * k - (960 * k - 504) / 2, 1))
    css = """
    #i5-h1 { top: 200px; }
    #i5-h2 { top: 294px; }
    #i5-call { position: absolute; left: 60px; top: 452px; width: 960px; height: 576px; border-radius: 30px; overflow: hidden; background: #0C0C1E; }
    #i5-top { position: absolute; left: 0; top: 0; width: 960px; height: 72px; display: flex; align-items: center; gap: 18px; padding-left: 22px; box-sizing: border-box; }
    #i5-live { display: flex; align-items: center; gap: 10px; height: 42px; padding: 0 18px 0 14px; border-radius: 999px; background: «RED»; color: #FFFFFF;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 20px; letter-spacing: 0.14em; white-space: nowrap; }
    #i5-ldot { display: block; width: 12px; height: 12px; border-radius: 50%; background: #FFFFFF; }
    #i5-ttl { font-family: "Inter", sans-serif; font-weight: 600; font-size: 24px; color: rgba(255,255,255,0.74); white-space: nowrap; }
    #i5-vid { position: absolute; left: 0; top: 72px; width: 960px; height: 504px; overflow: hidden; }
    #i5-v { position: absolute; left: «VL»px; top: «VT»px; width: «VW»px; height: «VH»px; }
    #i5-ctl { position: absolute; left: 330px; top: 414px; width: 300px; height: 72px; display: flex; justify-content: center; gap: 18px; }
    .i5-cb { position: relative; width: 66px; height: 66px; border-radius: 50%; background: rgba(12,12,30,0.62); }
    .i5-cb svg { position: absolute; left: 15px; top: 15px; width: 36px; height: 36px; }
    #i5-hang { background: «RED»; }
    #i5-fix { top: 1078px; gap: 18px; }
    .i5-fx { display: flex; align-items: center; gap: 12px; height: 70px; padding: 0 28px; border-radius: 999px; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 32px; line-height: 1; }
    #i5-bad { position: relative; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); color: rgba(255,255,255,0.8); }
    #i5-bads { position: absolute; left: 22px; top: 32px; width: calc(100% - 44px); height: 6px; border-radius: 3px; background: «RED»; transform-origin: 0% 50%; }
    #i5-arr { width: 44px; height: 44px; color: #FFFFFF; }
    #i5-arr svg { display: block; width: 44px; height: 44px; }
    #i5-good { background: #FFFFFF; color: «INDIGO»; padding-left: 14px; box-shadow: 0 16px 40px rgba(4,0,40,0.3); }
    #i5-good svg { display: block; width: 40px; height: 40px; }
    #i5-prow { top: 250px; }
    .i5-tile { position: absolute; width: 404px; height: 330px; border-radius: 36px; background: #FFFFFF;
      box-shadow: 0 40px 100px rgba(4,0,40,0.42), 0 8px 24px rgba(4,0,40,0.2); }
    .i5-big { position: absolute; left: 0; top: 52px; width: 404px; text-align: center; font-weight: 900; font-size: 150px; line-height: 1;
      letter-spacing: -0.04em; color: «INDIGO»; }
    .i5-ex { position: absolute; left: 0; top: 236px; width: 404px; text-align: center; font-family: "Inter", sans-serif; font-weight: 600;
      font-size: 34px; line-height: 1; color: «MUTED»; }
"""
    tiles = [("G", "goed", 121, 366), ("UI", "huis", 555, 366), ("UU", "uur", 121, 730), ("EU", "leuk", 555, 730)]
    tile_html = "\n".join(f'      <div id="i5-t{k}" class="i5-tile" style="left:{x}px; top:{y}px;"><div class="i5-big">{b}</div><div class="i5-ex">{e}</div></div>'
                          for k, (b, e, x, y) in enumerate(tiles))
    body = "\n".join([ground(P, "blue"), f"""    <div id="i5-s1" class="i5-full">
      <div id="i5-h1" class="i5-h1">Clase en directo</div>
      <div id="i5-h2" class="i5-h1 i5-acc">cada semana</div>
      <div id="i5-call" class="i5-on-blue">
        <div id="i5-top"><div id="i5-live"><span id="i5-ldot"></span><span>EN DIRECTO</span></div><div id="i5-ttl">Clase semanal · Holandés Nawar</div></div>
        <div id="i5-vid"><video id="i5-v" class="clip" src="assets/video/paul-clase-1.mp4" muted playsinline data-start="0" data-duration="«VD»" data-media-start="5.2" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video>
          <div id="i5-ctl"><div class="i5-cb">{icon('mic')}</div><div class="i5-cb">{icon('cam')}</div><div id="i5-hang" class="i5-cb">{icon('hang')}</div></div></div>
      </div>
      <div id="i5-fix" class="i5-row"><div id="i5-bad" class="i5-fx"><span>Werkt jij?</span><div id="i5-bads"></div></div><div id="i5-arr">{icon('down').replace('M24 8 V38 M12 27 L24 39 L36 27', 'M8 24 H38 M27 12 L39 24 L27 36')}</div><div id="i5-good" class="i5-fx">{icon('check')}<span>Werk jij?</span></div></div>
    </div>
    <div id="i5-s2" class="i5-full">
      <div id="i5-prow" class="i5-row"><div id="i5-pp" class="i5-pill"><span>Pronunciación</span></div></div>
{tile_html}
    </div>"""])
    js = """
      tl.fromTo(q("h1"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("h2"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.1);
      tl.fromTo(q("call"), { opacity: 0, y: 100, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.44, ease: "power3.out" }, 0.04);
      tl.fromTo(q("live"), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.2)" }, «DIR» - 0.06);
      tl.fromTo(q("ldot"), { opacity: 1 }, { keyframes: [{ opacity: 0.25, duration: 0.3 }, { opacity: 1, duration: 0.3 }, { opacity: 0.25, duration: 0.3 }, { opacity: 1, duration: 0.3 }], immediateRender: false }, «DIR» + 0.3);
      tl.fromTo(q("bad"), { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.28, ease: "power3.out" }, «REF» - 0.08);
      tl.fromTo(q("bads"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power2.out" }, «REF» + 0.3);
      tl.fromTo(q("arr"), { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 0.22, ease: "power3.out" }, «REF» + 0.42);
      tl.fromTo(q("good"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «REF» + 0.52);
      tl.to(q("s1"), { opacity: 0, y: -90, duration: 0.24, ease: "power2.in" }, «SWAP» - 0.2);
      tl.fromTo(q("s2"), { opacity: 0 }, { opacity: 1, duration: 0.01 }, «SWAP» - 0.02);
      tl.fromTo(q("pp"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.26, ease: "power3.out" }, «SWAP»);
      tl.fromTo(q("t0"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.02);
      tl.fromTo(q("t1"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.12);
      tl.fromTo(q("t2"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.22);
      tl.fromTo(q("t3"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.32);
"""
    sfx = [(c["DIR"] - 0.06, "notification", 0.2), (c["REF"] + 0.52, "ping", 0.2), (c["SWAP"], "whoosh-short", 0.12),
           (c["SWAP"] + 0.02, "pop", 0.16), (c["SWAP"] + 0.22, "pop", 0.16)]
    return comp(iid, d, P, css, body, js, c), sfx


# ============================================================================== ins-06 · eres tú el que llama
def ins06():
    iid, P = "ins-06", "i6"; d = INS[iid]["duration"]
    c = dict(ERE=cue(iid, "eres"), PED=cue(iid, "pedir"), CIT=cue(iid, "cita"))
    css = CALL_CSS + """
    #i6-wrow { top: 236px; }
    #i6-av1 { right: 90px; top: 622px; background: «INDIGO»; }
    #i6-b1 { right: 214px; top: 576px; width: 620px; white-space: normal; transform-origin: 100% 100%; }
    #i6-av2 { left: 90px; top: 856px; background: #9fd5f5; }
    #i6-b2 { left: 214px; top: 844px; transform-origin: 0% 100%; }
    #i6-okrow { top: 1030px; }
    #i6-ok { display: flex; align-items: center; gap: 14px; height: 80px; padding: 0 34px 0 18px; border-radius: 999px; background: «GREEN»; color: #FFFFFF;
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 36px; line-height: 1; white-space: nowrap; box-shadow: 0 18px 44px rgba(4,0,40,0.35); }
    #i6-ok svg { display: block; width: 48px; height: 48px; }
"""
    body = "\n".join([ground(P, "blue"), f"""    <div id="i6-wrow" class="i6-row"><div id="i6-wk" class="i6-wpill"><span class="i6-flag i6-flagd">{FLAG_NL}</span><span>Semana 16</span></div></div>""",
        call_card(P, 90, 350, '<div class="i6-call-st"><span class="i6-dot"></span>En llamada · 00:14</div>').replace("i6-on-paper", "i6-on-blue"),
        f"""    <div id="i6-av1" class="i6-av">{person()}</div>
    <div id="i6-b1" class="i6-bub i6-bub-b i6-br">Goedemorgen! Ik wil graag een afspraak maken.</div>
    <div id="i6-av2" class="i6-av">{person()}</div>
    <div id="i6-b2" class="i6-bub i6-bub-w i6-bl">Natuurlijk. Dinsdag om tien uur?</div>
    <div id="i6-okrow" class="i6-row"><div id="i6-ok">{icon('checkw')}<span>Cita confirmada</span></div></div>"""])
    js = """
      tl.fromTo(q("wk"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, 0);
      tl.fromTo(q("call"), { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }, 0.02);
      tl.fromTo(q("av1"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)" }, «ERE» + 0.04);
      tl.fromTo(q("b1"), { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, «ERE» + 0.08);
      tl.fromTo(q("av2"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)" }, «PED» - 0.12);
      tl.fromTo(q("b2"), { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }, «PED» - 0.08);
      tl.fromTo(q("ok"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.34, ease: "back.out(2)" }, «CIT» - 0.04);
"""
    sfx = [(c["ERE"] + 0.08, "pop", 0.24), (c["PED"] - 0.08, "pop", 0.24), (c["CIT"] - 0.04, "chime", 0.28)]
    return comp(iid, d, P, css, body, js, c), sfx


# ============================================================================== outro · she stays on screen, enrolment block below
def outro():
    """From «haz clic en el botón de acá abajo» to the end the girl stays on screen (framed higher, then held on her
    last smile) and a clean enrolment card slides up in the lower third: logo + «Matrícula abierta», the course, the
    allowed stats, the button «Rellena el formulario ↓» and «Una persona del equipo te contactará»."""
    P = "o"; t0 = ED["outro"]; d = round(TOTAL - t0, 3)
    def wcue(word, k=0):
        hits = [w for w in WORDS if w["t"] >= t0 and norm(w["text"]) == norm(word)]
        return round(hits[k]["t"] - t0, 3)
    c = dict(REL=wcue("rellena"), PER=wcue("persona"), END=round(ED["speech_end"] - t0, 3))
    css = """
    #o-card { left: 80px; top: 1112px; width: 920px; height: 388px; border-radius: 38px;
      box-shadow: 0 34px 90px rgba(4,0,40,0.38), 0 8px 22px rgba(4,0,40,0.18); }
    #o-logo { position: absolute; left: 40px; top: 32px; width: 146px; height: 52px; background: url("assets/img/logo-nawar.png") left center / contain no-repeat; }
    #o-open { position: absolute; right: 36px; top: 36px; display: flex; align-items: center; gap: 10px; height: 44px; padding: 0 18px 0 14px; border-radius: 999px;
      background: #EAF7EF; color: #15803D; font-family: "Inter", sans-serif; font-weight: 700; font-size: 19px; line-height: 1; letter-spacing: 0.14em; white-space: nowrap; }
    #o-dot { display: block; width: 12px; height: 12px; border-radius: 50%; background: «GREEN»; }
    #o-title { position: absolute; left: 40px; top: 104px; font-weight: 800; font-size: 46px; line-height: 1.05; letter-spacing: -0.025em; color: «INK»; white-space: nowrap; }
    #o-stats { position: absolute; left: 42px; top: 166px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 26px; line-height: 1; color: «MUTED»; white-space: nowrap; }
    #o-btn { position: absolute; left: 40px; top: 214px; width: 840px; height: 94px; border-radius: 22px; background: «BLUE»; overflow: hidden;
      box-shadow: 0 14px 30px rgba(11,109,240,0.35); }
    #o-bt { position: absolute; left: 0; top: 0; width: 840px; height: 94px; display: flex; align-items: center; justify-content: center; gap: 14px;
      font-weight: 700; font-size: 36px; line-height: 1; color: #FFFFFF; white-space: nowrap; }
    #o-arr { position: relative; width: 40px; height: 40px; color: #FFFFFF; }
    #o-arr svg { position: absolute; left: 0; top: 0; width: 40px; height: 40px; }
    #o-shine { position: absolute; left: -260px; top: 0; width: 200px; height: 94px;
      background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.32) 50%, rgba(255,255,255,0) 100%); }
    #o-team { position: absolute; left: 0; top: 334px; width: 920px; display: flex; justify-content: center; align-items: center; gap: 12px;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 25px; line-height: 1; color: «MUTED»; white-space: nowrap; }
    #o-ph { position: relative; width: 34px; height: 34px; border-radius: 50%; background: «BLUE»; }
    #o-ph svg { position: absolute; left: 8px; top: 8px; width: 18px; height: 18px; }
"""
    body = f"""    <div id="o-card" class="o-card">
      <div id="o-logo"></div>
      <div id="o-open"><span id="o-dot"></span><span>MATRÍCULA ABIERTA</span></div>
      <div id="o-title">Formación Nawar A0–A1</div>
      <div id="o-stats">16 semanas · 10 módulos · +360 lecciones</div>
      <div id="o-btn"><div id="o-shine"></div><div id="o-bt"><span>Rellena el formulario</span><div id="o-arr">{icon('down')}</div></div></div>
      <div id="o-team"><div id="o-ph">{icon('phone')}</div><span>Una persona del equipo te contactará</span></div>
    </div>"""
    js = """
      tl.fromTo(q("card"), { opacity: 0, y: 150 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.02);
      tl.fromTo([q("logo"), q("open")], { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.16);
      tl.fromTo(q("title"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.22);
      tl.fromTo(q("stats"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.28);
      tl.fromTo(q("btn"), { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.36, ease: "back.out(1.7)" }, 0.34);
      tl.fromTo(q("team"), { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «PER» - 0.08);
      tl.to(q("btn"), { scale: 0.97, duration: 0.08, ease: "power2.out" }, «REL»);
      tl.to(q("btn"), { scale: 1, duration: 0.3, ease: "back.out(2.4)" }, «REL» + 0.08);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1300, duration: 0.7, ease: "power2.inOut" }, «REL» + 0.04);
      tl.fromTo(q("shine"), { x: 0 }, { x: 1300, duration: 0.7, ease: "power2.inOut", immediateRender: false }, «END» + 0.2);
      tl.fromTo(q("arr"), { y: 0 }, { keyframes: [{ y: 7, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" },
        { y: 7, duration: 0.22, ease: "power1.inOut" }, { y: 0, duration: 0.22, ease: "power1.inOut" }], immediateRender: false }, «END» - 0.2);
"""
    sfx = [(0.02, "whoosh-short", 0.12), (c["REL"], "click-soft", 0.2), (c["PER"] - 0.08, "notification", 0.16)]
    return comp("outro", d, P, css, body, js, c), t0, d, sfx


# ============================================================================== captions (clean, white, no box)
SHOW = {"dieciseis": "16"}


def ground_at(t):
    for i in ED["inserts"]:
        if i["start"] <= t < i["start"] + i["duration"]:
            return i["ground"]
    return "girl"


def captions():
    P = "cap"
    bounds = sorted({0.0, ED["outro"]} | {i["start"] for i in ED["inserts"]} | {round(i["start"] + i["duration"], 3) for i in ED["inserts"]})
    pages, cur = [], []
    def region(t): return max(b for b in bounds if b <= t + 1e-6)
    for k, w in enumerate(WORDS):
        txt = SHOW.get(norm(w["text"]), w["text"]) + (w.get("punct") or "").replace(":", "").replace(";", "")
        if norm(w["text"]) == "estas":
            txt = "¿" + txt
        if cur and region(w["t"]) != region(cur[0]["t"]):
            pages.append(cur); cur = []
        cur.append(dict(w, show=txt))
        first = not pages
        lim_w, lim_c = (5, 26) if first else (3, 16)
        brk = any(ch in (w.get("punct") or "") for ch in ".?!,:") or len(cur) >= lim_w or sum(len(x["show"]) for x in cur) >= lim_c
        if first and norm(w["text"]) != "bajos":
            brk = False
        if brk:
            pages.append(cur); cur = []
    if cur: pages.append(cur)
    body, js = [], []
    end_all = round(ED["speech_end"] + 0.12, 3)
    for k, pg in enumerate(pages):
        t0 = max(0.0, pg[0]["t"] - 0.03) if k else 0.0
        t1 = (pages[k + 1][0]["t"] - 0.03) if k + 1 < len(pages) else end_all
        g = ground_at(pg[0]["t"] + 0.01)
        spans = " ".join('<span id="cap-w%d-%d" class="cap-w">%s</span>' % (k, i, w["show"]) for i, w in enumerate(pg))
        up = " cap-up" if pg[0]["t"] >= ED["outro"] - 1e-3 else ""      # above the enrolment card
        body.append('    <div id="cap-g%d" class="cap-g cap-gr-%s%s">%s</div>' % (k, g, up, spans))
        js.append('      tl.fromTo(q("g%d"), { opacity: %d }, { opacity: 1, duration: 0.01 }, %.3f);' % (k, 1 if k == 0 else 0, t0))
        js.append('      tl.set(q("g%d"), { opacity: 0 }, %.3f);' % (k, t1))
        for i, w in enumerate(pg if k else []):     # the first page is on screen from frame 0 (thumbnail / scroll-stop)
            a = max(t0, w["t"] - 0.03)
            js.append('      tl.fromTo(q("w%d-%d"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.1, ease: "power2.out" }, %.3f);' % (k, i, a))
    css = """
    .cap-g { position: absolute; left: 90px; top: 1268px; width: 900px; height: 150px; display: flex; flex-wrap: wrap; align-content: center;
      justify-content: center; column-gap: 18px; row-gap: 0px; opacity: 0; }
    .cap-up { top: 972px; }
    .cap-w { display: inline-block; font-weight: 800; font-size: 66px; line-height: 76px; letter-spacing: -0.015em; white-space: nowrap; }
    .cap-gr-girl .cap-w { color: #FFFFFF; text-shadow: 0 3px 14px rgba(0,0,0,0.55), 0 1px 3px rgba(0,0,0,0.45); }
    .cap-gr-blue .cap-w { color: #FFFFFF; text-shadow: 0 3px 16px rgba(4,0,40,0.45); }
    .cap-gr-paper .cap-w { color: «INK»; }
"""
    return comp("captions", TOTAL, P, css, "\n".join(body), "\n".join(js) + "\n"), len(pages)


# ============================================================================== index.html
def zooms():
    """coordinate-target-zoom on the girl (origin = her face): tweens (time, duration, ease, to, from|None). Each
    section after an insert starts at its own framing (the cut hides the change), with a slow push and a punch on a
    key word. For the outro she is framed higher (y −150) so the enrolment card sits under her face."""
    G = ED["girl"]; Z = []
    def push(g, s0, s1, until=None):
        Z.append((g["start"], round((until or g["end"]) - g["start"], 3), "none", {"scale": s1}, {"scale": s0, "y": 0}))
    def punch(word, s, k=0, d=0.22, ease="power3.out"):
        Z.append((round(at(word, k) - 0.05, 3), d, ease, {"scale": s}, None))
    def cut(word, s0, s1, until, k=0):
        t = round(at(word, k) - 0.04, 3); Z.append((t, round(until - t, 3), "none", {"scale": s1}, {"scale": s0, "y": 0}))
    g = G[0]; push(g, 1.0, 1.05, at("escucha") - 0.05); punch("escucha", 1.15); cut("seguro", 1.04, 1.07, g["end"])
    g = G[1]; push(g, 1.12, 1.15, at("algo") - 0.04); cut("algo", 1.02, 1.05, at("sin") - 0.05); punch("sin", 1.16); cut("eso", 1.06, 1.09, g["end"])
    g = G[2]; push(g, 1.0, 1.03, at("nawar") - 0.05); punch("nawar", 1.13)
    g = G[3]; push(g, 1.14, 1.18)
    g = G[4]; push(g, 1.0, 1.04, at("cada") - 0.05); punch("cada", 1.13)
    g = G[5]; push(g, 1.16, 1.2)
    g = G[6]; push(g, 1.02, 1.05, at("estas") - 0.05); punch("estas", 1.15)
    o = ED["outro"]
    Z.append((round(o - 0.45, 3), 0.6, "power2.inOut", {"scale": 1.15, "y": -150}, None))
    Z.append((round(o + 0.15, 3), round(TOTAL - o - 0.15, 3), "none", {"scale": 1.19}, None))
    return Z


def media_len(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return round(float(out.strip()), 3)


def index(sfx_all, out_t0, out_d):
    fx, fy = FACE; d = ED["clip_end"]
    auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 0.012, "v": 1},
                      {"t": round(d - 0.06, 3), "v": 1}, {"t": d, "v": 0}]}]})
    hosts = []
    for k, i in enumerate(ED["inserts"]):
        hosts.append(f'    <div id="{i["id"]}" data-composition-id="{i["id"]}" data-composition-src="compositions/{i["id"]}.html" data-start="{i["start"]}" data-duration="{i["duration"]}" data-track-index="{2 + k}" data-width="1080" data-height="1920"></div>')
    hosts.append(f'    <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" data-start="{out_t0}" data-duration="{out_d}" data-track-index="9" data-width="1080" data-height="1920"></div>')
    hosts.append(f'    <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-width="1080" data-height="1920"></div>')
    auds = [f'    <audio id="music" src="assets/audio/music-bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="1"></audio>']
    for k, (t, name, vol, *rest) in enumerate(sfx_all):
        src = "assets/audio/ringback.wav" if name == "ringback" else f"assets/sfx/{name}.mp3"
        dd = min(rest[0] if rest else 99, media_len(os.path.join(ROOT, src)))
        dd = round(min(dd, TOTAL - t), 3)
        auds.append(f'    <audio id="sfx{k}" src="{src}" data-start="{max(0.0, round(t, 3))}" data-duration="{dd}" data-track-index="{20 + k}" data-volume="{vol}"></audio>')
    ztl = []
    js = lambda dct: "{ " + ", ".join(f"{k}: {v}" for k, v in dct.items())
    for (t, du, ease, to, frm) in sorted(zooms(), key=lambda z: z[0]):
        du = max(0.01, round(du, 3))
        if frm is not None:
            ztl.append(f'      tl.fromTo("#zw", {js(frm)} }}, {js(to)}, duration: {du}, ease: "{ease}", immediateRender: false }}, {round(t, 3)});')
        else:
            ztl.append(f'      tl.to("#zw", {js(to)}, duration: {du}, ease: "{ease}" }}, {round(t, 3)});')
    hold = ED["hold"]
    html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #120081; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #120081; }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
      #zw {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; will-change: transform; }}
      #zw video, #zw img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}">
    <div class="shot"><div id="zw" data-layout-allow-overflow style="transform-origin: {fx}px {fy}px;">
      <video id="girl" class="clip" src="assets/video/take-{ED['take']}.mp4" data-start="0" data-duration="{d}" data-media-start="0" data-playback-rate="{RATE}" data-track-index="0" playsinline data-has-audio="true" data-automation='{auto}'></video>
      <img id="hold" class="clip" src="assets/img/take-b-last.png" alt="" data-start="{hold['start']}" data-duration="{hold['duration']}" data-track-index="1" />
    </div></div>
{chr(10).join(hosts)}
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // framing on the girl: one look per section, a slow push and a punch on the key word (origin = her face);
      // the take ends on her smile, held (#hold, its last frame) under the enrolment card
{chr(10).join(ztl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(html)


def main():
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "compositions")):
        if f.endswith(".html"):
            os.remove(os.path.join(ROOT, "compositions", f))
    sfx_all = []
    for fn in [ins01, ins02, ins03, ins04, ins05, ins06]:
        html, sfx = fn()
        iid = "ins-0" + fn.__name__[-1]
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
