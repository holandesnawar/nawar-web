"""Shared design system + helpers for the UGC #2 compositions (same as UGC #1: the VSL's frame.md re-set for 1080×1920).

Grounds: PAPER (#F5F7FF + dots) for problems, NAWAR BLUE (radial #025dc7 → #120081 + dots) for the solution.
Type: Poppins (display) + Inter (UI). Cards: white, radius 32, soft indigo shadow. No orange anywhere.
Every insert module in tools/inserts/ does `from common import *` and returns (html, sfx) from build().
Cue helpers read edit.json: cue(iid, word, k) = local time of the k-th «word» inside insert iid.
"""
import json, os, re, subprocess, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = json.load(open(os.path.join(ROOT, "edit.json")))
INS = {i["id"]: i for i in ED["inserts"]}
WORDS = ED["words"]
TOTAL = ED["total"]
RATE = ED["rate"]

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



FLAG_EN = ('<svg viewBox="0 0 40 27"><rect width="40" height="27" fill="#012169"/><path d="M0 0 L40 27 M40 0 L0 27" stroke="#FFFFFF" stroke-width="5"/>'
           '<path d="M0 0 L40 27 M40 0 L0 27" stroke="#C8102E" stroke-width="2"/><path d="M20 0 V27 M0 13.5 H40" stroke="#FFFFFF" stroke-width="8"/>'
           '<path d="M20 0 V27 M0 13.5 H40" stroke="#C8102E" stroke-width="4.5"/></svg>')
