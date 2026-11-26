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
METODO_PAGES = (1, 2, 3)          # (v13) the guide's sheets in the mockup: in front (the cover), behind left, behind right
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


def metodo_pages():
    """the three sheets of the method guide (the client's «MÉTODO.pdf», docs.holandesnawar.com/dossier, in
    .raw/metodo-pdf/metodo.pdf) → assets/img/metodo-N.jpg: the cover, «Lo que incluye», «Te lo han explicado en el
    idioma equivocado»."""
    import subprocess, tempfile
    from PIL import Image
    pdf = os.path.join(ROOT, ".raw", "metodo-pdf", "metodo.pdf")
    for n in METODO_PAGES:
        out = os.path.join(ROOT, "assets", "img", f"metodo-{n}.jpg")
        if os.path.exists(out):
            continue
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["pdftoppm", "-r", "150", "-png", "-f", str(n), "-l", str(n), pdf, os.path.join(d, "p")], check=True)
            png = os.path.join(d, sorted(os.listdir(d))[0])
            Image.open(png).convert("RGB").save(out, quality=92)


def outro_html():
    """compositions/outro.html (v13, the client: the method guide as a mockup — three sheets, one straight and two turned
    to the sides, «so you see you get something real» — a «Black Friday · últimas plazas» tab, and no typing): the
    indigo screen of the second reel's closing ad, all in within ~1 s: the red tab, (v14) «Recibe el PDF / de nuestro método /
    y comienza a hablar neerlandés ya»,
    the guide's cover straight in front with «Lo que incluye» and «Te lo han explicado en el idioma equivocado» fanned
    out behind it, the light-blue ticker with what the course is (from the guide) and a «Comenta QUIERO» button that
    pulses when the voice says it."""
    metodo_pages()
    c = O.cues()
    v = dict(c, D=O.END, INDIGO=INDIGO, SKY=SKY, RED="#DC2626")
    css = """
    #o-root { position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; color: #FFFFFF; }
    .o-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    #o-ground { background: «INDIGO»; }
    .o-luz1 { position: absolute; top: -280px; right: -320px; width: 1300px; height: 1300px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.42) 0%, rgba(11,109,240,0) 65%); }
    .o-luz2 { position: absolute; bottom: -260px; left: -280px; width: 1150px; height: 1150px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.20) 0%, rgba(11,109,240,0) 65%); }
    .o-dots { position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,255,255,0.06) 2px, transparent 2.2px); background-size: 52px 52px; }
    .o-row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; }
    /* the tab: Black Friday · últimas plazas */
    #o-tab { top: 180px; }
    .o-tab { display: flex; align-items: center; gap: 14px; height: 66px; padding: 0 32px 0 26px; border-radius: 999px; background: «RED»;
      font-weight: 800; font-size: 27px; letter-spacing: 0.12em; color: #FFFFFF; white-space: nowrap; line-height: 1;
      }
    #o-dot { display: block; width: 14px; height: 14px; border-radius: 50%; background: #FFFFFF; }
    .o-h { font-family: "Poppins", sans-serif; font-weight: 700; font-size: 92px; line-height: 1.08; letter-spacing: -0.03em; white-space: nowrap; }
    #o-l1 { top: 262px; }
    #o-l1 span { background: linear-gradient(180deg, #FFFFFF 10%, rgba(255,255,255,0.6) 100%); -webkit-background-clip: text;
      background-clip: text; -webkit-text-fill-color: transparent; color: transparent; padding: 0 6px; }
    #o-l2 { top: 362px; color: «SKY»; }
    #o-l3 { top: 478px; font-weight: 600; font-size: 40px; color: #E0F2FF; white-space: nowrap; }
    #o-l3 b { font-weight: 800; color: #FFFFFF; }
    /* the guide: three A4 sheets, the cover straight in front, two fanned out behind */
    .o-sheet { position: absolute; display: block; border-radius: 10px; overflow: hidden; background: #FFFFFF;
      box-shadow: 0 0 0 1.5px rgba(255,255,255,0.25), 0 26px 60px rgba(2,0,24,0.55), 0 6px 14px rgba(2,0,24,0.35); }
    .o-sheet img { display: block; width: 100%; height: 100%; object-fit: cover; }
    #o-s1 { left: 330px; top: 562px; width: 420px; height: 594px; z-index: 3; box-shadow: 0 0 0 3px rgba(255,255,255,0.55), 0 30px 70px rgba(2,0,24,0.65), 0 6px 14px rgba(2,0,24,0.35); }
    #o-s2 { left: 190px; top: 622px; width: 360px; height: 509px; z-index: 1; transform-origin: 70% 90%; }
    #o-s3 { left: 530px; top: 622px; width: 360px; height: 509px; z-index: 2; transform-origin: 30% 90%; }
    #o-shine { position: absolute; top: -60px; left: -260px; width: 140px; height: 800px; transform: rotate(18deg);
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.22) 50%, rgba(255,255,255,0) 100%); }
    /* the light-blue ticker: what the course is (from the guide) */
    #o-band { position: absolute; left: -10px; top: 1238px; width: 1100px; height: 64px; background: «SKY»; overflow: hidden; }
    #o-track { position: absolute; left: 0; top: 0; height: 64px; display: flex; align-items: center; white-space: nowrap; }
    #o-track span { display: flex; align-items: center; gap: 16px; padding: 0 26px; color: «INDIGO»; font-weight: 700; font-size: 30px; line-height: 1; }
    #o-track b { font-size: 26px; }
    /* the call to action: a button, no typing */
    #o-cta { top: 1362px; flex-direction: column; gap: 12px; }
    .o-btn { display: flex; align-items: center; gap: 18px; height: 96px; padding: 0 44px 0 32px; border-radius: 999px; background: #FFFFFF;
      color: #0C0C1E; white-space: nowrap; }
    .o-btn svg { display: block; width: 48px; height: 48px; }
    .o-btn span { font-weight: 700; font-size: 40px; line-height: 1; }
    .o-btn b { font-family: "Poppins", sans-serif; font-weight: 800; color: «INDIGO»; letter-spacing: 0.02em; }
    .o-sub { font-weight: 600; font-size: 28px; color: #E0F2FF; white-space: nowrap; }
"""
    ticker = ["Clases en directo cada semana", "Desde el español", "Autoestudio incluido", "16 semanas", "Dudas resueltas en menos de 24 h", "Certificado Holandés Nawar"]
    track = "".join(f"<span><b>✦</b>{html.escape(t)}</span>" for t in ticker * 4)
    bubble = ('<svg viewBox="0 0 52 52"><path d="M26 6 C14.4 6 5 14.2 5 24.4 C5 29.6 7.4 34.2 11.3 37.6 L9.6 46 L18.6 41.6 C20.9 42.3 23.4 42.7 26 42.7 '
              'C37.6 42.7 47 34.5 47 24.4 C47 14.2 37.6 6 26 6 Z" fill="none" stroke="«INDIGO»" stroke-width="4" stroke-linejoin="round"/></svg>')
    body = f"""
    <div id="o-ground" class="o-full"><div class="o-luz1"></div><div class="o-luz2"></div><div class="o-dots"></div></div>
    <div id="o-tab" class="o-row"><div class="o-tab"><i id="o-dot"></i><span>BLACK FRIDAY · ÚLTIMAS PLAZAS</span></div></div>
    <div id="o-l1" class="o-row o-h"><span>Recibe el PDF</span></div>
    <div id="o-l2" class="o-row o-h">de nuestro método</div>
    <div id="o-l3" class="o-row">y comienza a <b>&nbsp;hablar neerlandés ya</b></div>
    <div id="o-s2" class="o-sheet"><img src="assets/img/metodo-{METODO_PAGES[1]}.jpg" alt=""></div>
    <div id="o-s3" class="o-sheet"><img src="assets/img/metodo-{METODO_PAGES[2]}.jpg" alt=""></div>
    <div id="o-s1" class="o-sheet"><img src="assets/img/metodo-{METODO_PAGES[0]}.jpg" alt=""><i id="o-shine"></i></div>
    <div id="o-band"><div id="o-track">{track}</div></div>
    <div id="o-cta" class="o-row"><div class="o-btn">{bubble}<span>Comenta <b>QUIERO</b></span></div><div class="o-sub">y te lo enviamos por mensaje</div></div>
"""
    js = """
      // everything in at once (0.2–1.0 s), as in the second reel's closing ad
      tl.fromTo("#o-ground", { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.28, ease: "power2.out" }, «GROUND»);
      tl.fromTo("#o-tab", { opacity: 0, y: -24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.40, ease: "back.out(1.8)" }, «TAB»);
      tl.fromTo("#o-l1", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L1»);
      tl.fromTo("#o-l2", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L2»);
      tl.fromTo("#o-l3", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.40, ease: "power3.out" }, «L2» + 0.08);
      // the sheets: they come up together, then the two behind fan out to the sides
      tl.fromTo(["#o-s1", "#o-s2", "#o-s3"], { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, «PAGES»);
      tl.fromTo("#o-s2", { x: 140, rotation: 0 }, { x: 0, rotation: -11, duration: 0.5, ease: "back.out(1.4)" }, «FAN»);
      tl.fromTo("#o-s3", { x: -200, rotation: 0 }, { x: 0, rotation: 11, duration: 0.5, ease: "back.out(1.4)" }, «FAN»);
      tl.fromTo("#o-s1", { scale: 1 }, { scale: 1.04, duration: «D» - «FAN» - 0.5, ease: "sine.inOut" }, «FAN» + 0.5);
      tl.fromTo("#o-shine", { x: 0 }, { x: 900, duration: 0.9, ease: "power2.inOut" }, «FAN» + 0.4);
      tl.fromTo("#o-shine", { x: 0 }, { x: 900, duration: 0.9, ease: "power2.inOut", immediateRender: false }, «SHINE»);
      tl.fromTo("#o-band", { x: -1120 }, { x: 0, duration: 0.50, ease: "power3.out" }, «BAND»);
      tl.fromTo("#o-track", { xPercent: 0 }, { xPercent: -25, duration: «D», ease: "none" }, 0);
      tl.fromTo("#o-cta", { opacity: 0, y: 46, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.5)" }, «CTA»);
      // the tab pulses on «Black Friday»; the button on «QUIERO»
      tl.fromTo("#o-tab", { scale: 1 }, { scale: 1.08, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, «BF»);
      tl.fromTo("#o-cta .o-btn", { scale: 1 }, { scale: 1.08, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }, «QUIERO»);
"""
    blink, k, on = [], c["TAB"] + 0.4, True
    while k < O.END:
        blink.append(f'      tl.set("#o-dot", {{ opacity: {1 if on else 0.25} }}, {k:.3f});'); k += 0.4; on = not on
    def sub(s):
        for key in sorted(v, key=len, reverse=True):
            s = s.replace(f"«{key}»", str(v[key]))
        return s
    fonts = "\n".join([f'    @font-face {{ font-family: "Poppins"; font-weight: {w}; src: url("assets/fonts/poppins-latin-{w}-normal.woff2") format("woff2"); }}'
                       for w in (700, 800)] +
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
{chr(10).join(blink)}
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
