#!/usr/bin/env python3
"""index.html: the reel «Aprendiendo neerlandés con Luis Suárez» (9:16, 25 fps), v7 — in the design of the second reel's
final version (../reel-suarez-habla, v7.6):
- the ad full frame (assets/video/suarez-916.mp4, tools/frame.py);
- the hook for the first seconds, in the client's design: «Aprendiendo / neerlandés con / Luis Suárez» in Inter
  ExtraBold, white with a thick round black outline, the 📚 and 🇳🇱 icons (tools/img) on either side of the middle line.
  It sits over the chest (the faces are at the top in the first shots: Suárez's, then the assistant's down to y ≈ 890);
- the subtitles at the bottom: the Dutch phrase big, in capitals, white with the word being said in yellow, the Spanish
  under it in a grey pill (raised onto the nose in Suárez's extreme close-ups, so his lips stay in sight);
- (v8) the closing card, over the ad's last 0.3 s (compositions/outro.html, from tools/outro.py's voice, cues and
  sound): no ebook (the client) — «¿Quieres aprender neerlandés tú también? Aprende con nosotros, desde el español.
  Síguenos y empieza hoy.», in the indigo of the second reel's closing ad: the Nawar logo, the question, the light-blue
  ticker and an Instagram profile card «Holandés Nawar» whose «Seguir» button is tapped on «Síguenos».
  python3 tools/gen.py
"""
import html, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import outro as O  # noqa: E402
INDIGO, SKY = "#1D0084", "#4DA3FF"
YEL = "#FFE11B"
SUB_BOTTOM = 1500                 # the subtitle block stands on this line (frame px), as in the second reel
NL_W, NL_CX = 744, 540
NL_SIZE, ES_SIZE = 62, 38
HOOK_TOP, HOOK_SIZE, HOOK_LH = 920, 77, 1.06   # over the chest, under the assistant's lips (y ≈ 890), clear of the subtitles
HOOK_OUTLINE = 6
HOOK_OUT = 3.30                   # on screen from the first frame (the cover), it leaves here
HOOK = ["Aprendiendo", "neerlandés con", "Luis Suárez"]
ICONS = {"books": 108, "nl": 88}
ICON_DY = {"books": 22, "nl": 9}
ICON_GAP = 18
OUT_LEAD = 0.30                   # the closing ad comes in over the ad's last 0.3 s
UP = [(7.96, 9.60), (16.64, 20.52), (26.04, 27.80)]       # Suárez's extreme close-ups: the subtitles sit higher, on his
UP_DY = -440                      # nose (block bottom ≈ 1060), so his lips stay in sight; the bottom shade is off there
MIN_ON = 0.6                      # a one-word phrase opens a little early (after the last word before it) to be read
ON_AT = {11: 16.64, 18: 26.04,    # these open on the cut into Suárez's close-up (the phrase before closes there: no
         22: 32.40, 23: 33.00}    # block over his lips for a frame, no jump mid-shot); «Kaartje?» on the cut to the card
OFF_AT = {18: 27.80}              # …and this one closes on the cut out of it (the dip to black)


def outline_shadow(r, color="#000"):
    """a round outline of r px around the text: the glyph shifted to every direction on two rings (text-shadow)."""
    import math
    out = []
    for rr, n in ((r, 32), (r * 0.55, 16)):
        for k in range(n):
            a = 2 * math.pi * k / n
            out.append(f"{rr * math.cos(a):.2f}px {rr * math.sin(a):.2f}px 0 {color}")
    return ", ".join(out)


def outro_html():
    """compositions/outro.html: the closing card, O.END s long, every moment from O.cues()."""
    c = O.cues()
    v = dict(c, D=O.END, INDIGO=INDIGO, SKY=SKY)
    css = """
    #o-root { position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; color: #FFFFFF; }
    .o-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    /* the ground of the second reel's closing ad: indigo, two soft blue lights and a faint dot grid */
    #o-ground { background: «INDIGO»; }
    .o-luz1 { position: absolute; top: -280px; right: -320px; width: 1300px; height: 1300px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.42) 0%, rgba(11,109,240,0) 65%); }
    .o-luz2 { position: absolute; bottom: -260px; left: -280px; width: 1150px; height: 1150px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.20) 0%, rgba(11,109,240,0) 65%); }
    .o-dots { position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,255,255,0.06) 2px, transparent 2.2px);
      background-size: 52px 52px; }
    .o-row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; }
    /* the logo on a white pill (it is drawn for a white ground) */
    #o-logo { top: 330px; }
    .o-logo { display: flex; align-items: center; justify-content: center; height: 128px; padding: 0 44px; border-radius: 999px; background: #FFFFFF; }
    .o-logo img { display: block; height: 88px; }
    /* the question, as the page's title: Poppins 700, white gradient, «neerlandés» in sky blue */
    .o-h { font-family: "Poppins", sans-serif; font-weight: 700; font-size: 100px; line-height: 1.08; letter-spacing: -0.03em; white-space: nowrap; }
    .o-h span { background: linear-gradient(180deg, #FFFFFF 10%, rgba(255,255,255,0.6) 100%); -webkit-background-clip: text;
      background-clip: text; -webkit-text-fill-color: transparent; color: transparent; padding: 0 6px; }
    #o-l1 { top: 520px; }
    #o-l2 { top: 628px; color: «SKY»; }
    #o-l3 { top: 736px; }
    /* the answer: «Aprende con nosotros, desde el español» */
    #o-sub { top: 898px; }
    .o-sub { display: flex; align-items: center; gap: 16px; font-weight: 600; font-size: 44px; line-height: 1.2; color: #E0F2FF; white-space: nowrap; }
    .o-sub b { font-weight: 800; color: #FFFFFF; }
    /* the light-blue ticker */
    #o-band { position: absolute; left: -10px; top: 1028px; width: 1100px; height: 64px; background: «SKY»; overflow: hidden; }
    #o-track { position: absolute; left: 0; top: 0; height: 64px; display: flex; align-items: center; white-space: nowrap; }
    #o-track span { display: flex; align-items: center; gap: 16px; padding: 0 26px; color: «INDIGO»; font-weight: 700; font-size: 30px; line-height: 1; }
    #o-track b { font-size: 26px; }
    /* the call to action: an Instagram profile card with its «Seguir» button */
    #o-card { top: 1170px; }
    .o-card { position: relative; display: flex; align-items: center; gap: 20px; width: 744px; height: 180px; padding: 0 26px; border-radius: 38px;
      background: #FFFFFF; color: #0C0C1E; white-space: nowrap; }
    .o-av { position: relative; display: flex; align-items: center; justify-content: center; width: 108px; height: 108px; flex: 0 0 108px;
      border-radius: 50%; background: conic-gradient(from 200deg, #FEDA75, #FA7E1E, #D62976, #962FBF, #4F5BD5, #FEDA75); }
    .o-av i { display: flex; align-items: center; justify-content: center; width: 98px; height: 98px; border-radius: 50%; background: #FFFFFF;
      border: 4px solid #FFFFFF; overflow: hidden; }
    .o-av img { display: block; width: 86px; }
    .o-who { display: flex; flex-direction: column; gap: 6px; flex: 1 1 auto; }
    .o-name { display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 34px; line-height: 1; }
    .o-name svg { display: block; width: 30px; height: 30px; }
    .o-bio { font-weight: 500; font-size: 27px; line-height: 1.15; color: #5B6380; }
    #o-btn { position: relative; display: flex; align-items: center; justify-content: center; width: 216px; height: 76px; flex: 0 0 216px; border-radius: 18px;
      background: #0095F6; overflow: hidden; }
    #o-btn span { position: absolute; font-weight: 700; font-size: 31px; line-height: 1; }
    #o-follow { color: #FFFFFF; }
    #o-following { color: #0C0C1E; opacity: 0; }
    #o-ripple { position: absolute; left: 50%; top: 50%; width: 220px; height: 220px; margin: -110px 0 0 -110px; border-radius: 50%;
      background: rgba(255,255,255,0.45); opacity: 0; }
    #o-shine { position: absolute; top: -40px; left: -180px; width: 110px; height: 260px; transform: rotate(18deg);
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.7) 50%, rgba(255,255,255,0) 100%); opacity: 0.6; }
"""
    ticker = ["Desde cero", "Explicado en español", "Vocabulario y gramática", "Pronunciación", "Paso a paso", "Con Holandés Nawar"]
    track = "".join(f"<span><b>✦</b>{html.escape(t)}</span>" for t in ticker * 4)
    tick = ('<svg viewBox="0 0 30 30"><circle cx="15" cy="15" r="15" fill="#0095F6"/><path d="M8.5 15.5 L13 20 L21.5 10.5" fill="none" '
            'stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    body = f"""
    <div id="o-ground" class="o-full"><div class="o-luz1"></div><div class="o-luz2"></div><div class="o-dots"></div></div>
    <div id="o-logo" class="o-row"><div class="o-logo"><img src="assets/img/logo-nawar.png" alt="Nawar"></div></div>
    <div id="o-l1" class="o-row o-h"><span>¿Quieres aprender</span></div>
    <div id="o-l2" class="o-row o-h">neerlandés</div>
    <div id="o-l3" class="o-row o-h"><span>tú también?</span></div>
    <div id="o-sub" class="o-row"><div class="o-sub"><span>Aprende con nosotros, <b>desde el español</b></span></div></div>
    <div id="o-band"><div id="o-track">{track}</div></div>
    <div id="o-card" class="o-row"><div class="o-card"><div class="o-av"><i><img src="assets/img/logo-nawar.png" alt=""></i></div>
      <div class="o-who"><div class="o-name"><span>Holandés Nawar</span>{tick}</div><div class="o-bio">Neerlandés en español</div></div>
      <div id="o-btn"><span id="o-follow">Seguir</span><span id="o-following">Siguiendo</span><i id="o-ripple"></i><i id="o-shine"></i></div></div></div>
"""
    js = """
      // everything comes in at once (0.2–0.8 s), as in the second reel's closing ad; the button is tapped on «Síguenos»
      tl.fromTo("#o-ground", { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.28, ease: "power2.out" }, «GROUND»);
      tl.fromTo("#o-logo", { opacity: 0, y: -24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "back.out(1.6)" }, «LOGO»);
      tl.fromTo("#o-l1", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L1»);
      tl.fromTo("#o-l2", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L2»);
      tl.fromTo("#o-l3", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L3»);
      tl.fromTo("#o-sub", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «SUB»);
      tl.fromTo("#o-band", { x: -1120 }, { x: 0, duration: 0.50, ease: "power3.out" }, «BAND»);
      tl.fromTo("#o-track", { xPercent: 0 }, { xPercent: -25, duration: «D», ease: "none" }, 0);
      tl.fromTo("#o-card", { opacity: 0, y: 46, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.5)" }, «CARD»);
      tl.fromTo("#o-btn", { scale: 1 }, { scale: 1.08, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }, «SIGUE»);
      tl.fromTo("#o-btn", { scale: 1 }, { scale: 0.92, duration: 0.08, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, «TAP»);
      tl.fromTo("#o-ripple", { opacity: 0.9, scale: 0.2 }, { opacity: 0, scale: 1.4, duration: 0.45, ease: "power2.out", immediateRender: false }, «TAP»);
      tl.set("#o-btn", { backgroundColor: "#EFEFF2" }, «DONE»);
      tl.set("#o-follow", { opacity: 0 }, «DONE»);
      tl.set("#o-following", { opacity: 1 }, «DONE»);
      tl.fromTo("#o-shine", { x: 0 }, { x: 560, duration: 0.75, ease: "power2.inOut" }, «SHINE»);
"""
    def sub(s):
        for key in sorted(v, key=len, reverse=True):
            s = s.replace(f"«{key}»", str(v[key]))
        return s
    fonts = "\n".join([f'    @font-face {{ font-family: "Poppins"; font-weight: {w}; src: url("assets/fonts/poppins-latin-{w}-normal.woff2") format("woff2"); }}'
                       for w in (700,)] +
                      ['    @font-face { font-family: "Inter"; font-weight: 100 900; src: url("assets/fonts/inter-var-latin.woff2") format("woff2"); }'])
    page = f"""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
{fonts}
{sub(css)}
  </style>
  <div id="o-root" data-composition-id="outro" data-width="1080" data-height="1920" data-duration="{O.END}">
{sub(body)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{sub(js)}
      window.__timelines["outro"] = tl;
    }})();
  </script>
</template>
"""
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    open(os.path.join(ROOT, "compositions", "outro.html"), "w").write(page)
    return c


def segments(on, off):
    """the y offset of a phrase over its time on screen: UP_DY inside Suárez's close-ups. It changes only on a cut, and never for a bit shorter than 0.4 s (that bit takes its neighbour's place)."""
    base = 0
    cuts = sorted({c for ab in UP for c in ab if on < c < off})
    edges = [on] + cuts + [off]
    segs = [[edges[i], edges[i + 1], UP_DY if any(a <= (edges[i] + edges[i + 1]) / 2 < b for a, b in UP) else base]
            for i in range(len(edges) - 1)]
    while len(segs) > 1:
        i = min(range(len(segs)), key=lambda j: segs[j][1] - segs[j][0])
        if segs[i][1] - segs[i][0] >= 0.4:
            break
        j = i - 1 if i == len(segs) - 1 or (i > 0 and segs[i - 1][1] - segs[i - 1][0] >= segs[i + 1][1] - segs[i + 1][0]) else i + 1
        a, b = sorted((i, j))
        keep = segs[j][2]
        segs[a:b + 1] = [[segs[a][0], segs[b][1], keep]]
    return segs


def main():
    meta = json.load(open(os.path.join(ROOT, "assets", "video", "suarez-916.json")))
    D = meta["duration"]
    outro_html()
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    for k in ICONS:
        shutil.copyfile(os.path.join(ROOT, "tools", "img", f"emoji-{k}.png"), os.path.join(ROOT, "assets", "img", f"emoji-{k}.png"))
    OEND = O.END
    OUT0 = round(D - OUT_LEAD, 3)
    TOTAL = round(OUT0 + OEND, 3)
    subs = json.load(open(os.path.join(ROOT, "subs.json")))["phrases"]
    body, js = [], []
    ons = []
    for k, p in enumerate(subs):
        words = p["words"]
        on = max(0.0, words[0]["t"] - 0.05)
        if words[-1]["end"] - on < MIN_ON and k:                   # short: open early, after the phrase before it is said
            on = max(subs[k - 1]["words"][-1]["end"] + 0.03, min(on, words[-1]["end"] - MIN_ON))
        ons.append(ON_AT.get(k, on))
    for k, p in enumerate(subs):
        words = p["words"]
        on = ons[k]
        off = OFF_AT.get(k, min(ons[k + 1], words[-1]["end"] + 0.7) if k + 1 < len(subs) else D)
        spans = " ".join(('<span class="br"></span> ' if i in p.get("breaks", []) else "") +
                         f'<span id="w{k}-{i}" class="w">{html.escape(w["text"])}</span>' for i, w in enumerate(words))
        body.append(f'      <div id="p{k}" class="ph"><div class="nl">{spans}</div>'
                    f'<div class="es"><span>{html.escape(p["es"]).replace("|", "<br>")}</span></div></div>')
        for a, b, dy in segments(on, off):
            js.append(f'      tl.set("#p{k}", {{ y: {dy} }}, {a:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 1 }}, {on:.3f});')
        js.append(f'      tl.fromTo("#p{k} .nl", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.16, ease: "back.out(1.6)", immediateRender: false }}, {on:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 0 }}, {off:.3f});')
        for i, w in enumerate(words):
            t1 = words[i + 1]["t"] - 0.03 if i + 1 < len(words) else off
            js.append(f'      tl.set("#w{k}-{i}", {{ color: "{YEL}" }}, {max(on, w["t"] - 0.03):.3f});')
            if i + 1 < len(words):
                js.append(f'      tl.set("#w{k}-{i}", {{ color: "#FFFFFF" }}, {t1:.3f});')
    fonts = "\n".join([f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{f.lower()}-latin-{w}-normal.woff2") format("woff2"); }}'
                       for f, w in (("Poppins", 700), ("Poppins", 900), ("Inter", 600), ("Inter", 700))] +
                      ['      @font-face { font-family: "InterV"; font-weight: 100 900; src: url("assets/fonts/inter-var-latin.woff2") format("woff2"); }'])
    icons = {k: f'<img class="em em-{k}" src="assets/img/emoji-{k}.png" alt="">' for k in ICONS}
    hook = (f'<div class="hl"><span>{html.escape(HOOK[0])}</span></div>'
            f'<div class="hl"><span class="mid">{icons["books"]}{html.escape(HOOK[1])}{icons["nl"]}</span></div>'
            f'<div class="hl"><span>{html.escape(HOOK[2])}</span></div>')
    shade = "\n".join(f'      tl.set("#shade-bot", {{ opacity: 0 }}, {a:.2f});\n      tl.set("#shade-bot", {{ opacity: 1 }}, {b:.2f});' for a, b in UP)
    page = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{fonts}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #v {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .shade {{ position: absolute; left: 0; width: 1080px; pointer-events: none; }}
      /* a soft shade at the bottom, under the subtitles */
      #shade-bot {{ top: 1180px; height: 740px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.26) 45%, rgba(0,0,0,0.34) 100%); }}
      /* the hook: the client's design — Inter ExtraBold, white, a thick round black outline, the icons on the middle line */
      #hook {{ position: absolute; left: 0; top: {HOOK_TOP}px; width: 1080px; text-align: center; color: #FFFFFF;
        font-family: "InterV", sans-serif; font-weight: 800; font-size: {HOOK_SIZE}px; line-height: {HOOK_LH}; letter-spacing: -0.012em;
        text-shadow: {outline_shadow(HOOK_OUTLINE)}; transform-origin: 50% 40%; }}
      #hook .hl {{ white-space: nowrap; }}
      #hook .mid {{ position: relative; display: inline-block; }}
      #hook .em {{ position: absolute; top: 50%; display: block; }}
      #hook .em-books {{ height: {ICONS["books"]}px; top: calc(50% + {ICON_DY["books"]}px); right: calc(100% + {ICON_GAP + HOOK_OUTLINE}px); transform: translateY(-50%); }}
      #hook .em-nl {{ height: {ICONS["nl"]}px; top: calc(50% + {ICON_DY["nl"]}px); left: calc(100% + {ICON_GAP + HOOK_OUTLINE}px); transform: translateY(-50%); }}
      .ph {{ position: absolute; left: {NL_CX - 505}px; bottom: {1920 - SUB_BOTTOM}px; width: 1010px; display: flex; flex-direction: column;
        align-items: center; gap: 6px; opacity: 0; }}
      .nl {{ width: {NL_W}px; font-size: {NL_SIZE}px; display: flex; flex-wrap: wrap; justify-content: center; column-gap: 0.26em; row-gap: 0;
        font-family: "Poppins", sans-serif; font-weight: 900; line-height: 1.02; text-transform: uppercase; letter-spacing: -0.01em;
        color: #FFFFFF; -webkit-text-stroke: 10px #000; paint-order: stroke fill; text-shadow: 0 6px 16px rgba(0,0,0,0.5);
        transform-origin: 50% 60%; }}
      .w {{ display: inline-block; color: #FFFFFF; }}
      .br {{ flex-basis: 100%; height: 0; }}
      .es span {{ display: inline-block; max-width: {NL_W}px; padding: 8px 24px 10px; border-radius: 18px; text-align: center;
        background: rgba(78,78,84,0.78); color: #FFFFFF; font-family: "Poppins", sans-serif; font-weight: 700; font-size: {ES_SIZE}px;
        line-height: 1.2; letter-spacing: -0.005em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}" data-fps="25">
      <video id="v" class="clip" src="assets/video/suarez-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-bot" class="shade"></div>
      <div id="hook">{hook}</div>
{chr(10).join(body)}
      <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" data-start="{OUT0}" data-duration="{OEND}" data-track-index="2" data-width="1080" data-height="1920"></div>
      <audio id="a-outro" src="assets/audio/outro.wav" data-start="{OUT0}" data-duration="{OEND}" data-track-index="3"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // the hook: on screen from the first frame (it is the cover), it leaves at {HOOK_OUT} s
      tl.to("#hook", {{ opacity: 0, scale: 0.96, duration: 0.30, ease: "power2.in" }}, {HOOK_OUT});
      // the bottom shade is off in Suárez's extreme close-ups (it would darken his lips)
{shade}
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(page)
    print(f"index.html: {TOTAL}s (the ad {D}s, the closing card from {OUT0}s), {len(subs)} subtitle phrases")


if __name__ == "__main__":
    main()
