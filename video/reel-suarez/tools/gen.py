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
FREEZE_AT = 33.70                 # (v10) the closing freezes on this frame of the ad: Suárez, puzzled, into the lens
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
    """compositions/outro.html (v10): not an ad card — the reel goes on. Suárez frozen on his puzzled look into the
    lens (the ad's frame at FREEZE_AT, assets/img/freeze.png) with a slow push, a dark fade at the bottom, and over it,
    in the hook's style (Inter ExtraBold, white, round black outline), the voice's beats: «Suárez no pilló ni una» →
    «¿Y a ti, cuántas veces te ha pasado?» with the viewer's pain as pills (en el gemeente · con el casero · en el
    dentista) → «Aprende neerlandés» with two advantages (✓ Desde el español · ✓ A tu ritmo) → an Instagram comment
    field typing «QUIERO» → «Te contamos nuestro método por mensaje»."""
    import subprocess
    c = O.cues()
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{FREEZE_AT}", "-i", os.path.join(ROOT, "assets", "video", "suarez-916.mp4"),
                    "-frames:v", "1", os.path.join(ROOT, "assets", "img", "freeze.png")], check=True)
    v = dict(c, D=O.END, TYPEDUR=round(c["TYPE1"] - c["TYPE0"], 3), OUTLINE=outline_shadow(6))
    css = """
    #o-root { position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; color: #FFFFFF; }
    .o-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    #o-freeze { transform-origin: 50% 22%; }
    #o-freeze img { display: block; width: 1080px; height: 1920px; object-fit: cover; }
    #o-flash { background: #FFFFFF; opacity: 0; }
    #o-shade { background: linear-gradient(180deg, rgba(4,2,20,0) 0%, rgba(4,2,20,0) 28%, rgba(4,2,20,0.62) 42%, rgba(4,2,20,0.80) 60%, rgba(4,2,20,0.86) 100%); }
    .o-row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; }
    .o-ol { flex-direction: column; text-align: center; font-family: "InterV", sans-serif; font-weight: 800; letter-spacing: -0.012em;
      line-height: 1.06; color: #FFFFFF; text-shadow: «OUTLINE»; white-space: nowrap; }
    #o-l1, #o-l2 { top: 780px; font-size: 84px; }
    #o-ap { top: 760px; font-size: 92px; }
    .o-y { color: #FFE11B; }
    /* the pain: white pills, stacked, a little askew */
    #o-pains { position: absolute; left: 0; top: 1000px; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 18px; }
    .o-pain { display: flex; align-items: center; gap: 14px; height: 84px; padding: 0 34px 0 22px; border-radius: 999px; background: #FFFFFF;
      color: #0C0C1E; font-weight: 700; font-size: 40px; white-space: nowrap; line-height: 1; box-shadow: 0 14px 34px rgba(0,0,0,0.35); }
    .o-pain svg { display: block; width: 42px; height: 42px; }
    #o-p1 { transform: rotate(-2deg); } #o-p2 { transform: rotate(1.5deg); } #o-p3 { transform: rotate(-1deg); }
    /* the advantages */
    #o-bens { top: 892px; gap: 18px; }
    .o-ben { display: flex; align-items: center; gap: 12px; height: 74px; padding: 0 28px 0 16px; border-radius: 999px; background: #FFFFFF;
      color: #0C0C1E; font-weight: 700; font-size: 34px; white-space: nowrap; line-height: 1; box-shadow: 0 12px 30px rgba(0,0,0,0.30); }
    .o-ben svg { display: block; width: 42px; height: 42px; }
    /* the call to action: an Instagram comment field */
    #o-cta { top: 1030px; }
    .o-field { position: relative; display: flex; align-items: center; gap: 18px; width: 744px; height: 96px; padding: 0 30px 0 18px;
      border-radius: 999px; background: #FFFFFF; white-space: nowrap; }
    .o-av { display: block; width: 62px; height: 62px; flex: 0 0 62px; }
    #o-ph { position: absolute; left: 98px; font-weight: 500; font-size: 32px; color: #8E8E8E; }
    #o-typed { font-family: "Poppins", sans-serif; font-weight: 800; font-size: 40px; color: #0C0C1E; line-height: 1; letter-spacing: 0.02em; }
    #o-caret { display: block; width: 4px; height: 46px; border-radius: 2px; background: #0095F6; margin-left: -14px; }
    .o-fill { flex: 1 1 auto; }
    #o-post { position: relative; font-weight: 700; font-size: 32px; color: #0095F6; }
    #o-ripple { position: absolute; left: 50%; top: 50%; width: 150px; height: 150px; margin: -75px 0 0 -75px; border-radius: 50%;
      background: rgba(0,149,246,0.30); opacity: 0; }
    #o-ok { top: 1144px; }
    .o-ok { display: flex; align-items: center; gap: 14px; height: 64px; padding: 0 26px 0 14px; border-radius: 16px;
      background: rgba(34,197,94,0.22); border: 2px solid rgba(34,197,94,0.65); font-weight: 700; font-size: 30px; white-space: nowrap; }
    .o-ok svg { display: block; width: 36px; height: 36px; }
"""
    x = ('<svg viewBox="0 0 42 42"><circle cx="21" cy="21" r="21" fill="#EF4444"/><path d="M14 14 L28 28 M28 14 L14 28" fill="none" '
         'stroke="#FFFFFF" stroke-width="3.8" stroke-linecap="round"/></svg>')
    ok = ('<svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="18" fill="#22C55E"/><path d="M10 18.5 L15.5 24 L26 12.5" fill="none" '
          'stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    ok42 = ok.replace('viewBox="0 0 36 36"', 'viewBox="0 0 36 36" width="42" height="42"')
    av = ('<svg class="o-av" viewBox="0 0 62 62"><circle cx="31" cy="31" r="31" fill="#E6E8EF"/><circle cx="31" cy="25" r="11" fill="#A9AFBE"/>'
          '<path d="M11 52 C14 41 22 37 31 37 C40 37 48 41 51 52 A30 30 0 0 1 11 52 Z" fill="#A9AFBE"/></svg>')
    body = f"""
    <div id="o-freeze" class="o-full"><img src="assets/img/freeze.png" alt=""></div>
    <div id="o-shade" class="o-full"></div>
    <div id="o-flash" class="o-full"></div>
    <div id="o-l1" class="o-row o-ol"><div>Suárez no pilló</div><div>ni una</div></div>
    <div id="o-l2" class="o-row o-ol"><div>¿Y a ti, cuántas veces</div><div>te ha <span class="o-y">pasado</span>?</div></div>
    <div id="o-pains">
      <div id="o-p1" class="o-pain">{x}<span>En el gemeente</span></div>
      <div id="o-p2" class="o-pain">{x}<span>Con el casero</span></div>
      <div id="o-p3" class="o-pain">{x}<span>En el dentista</span></div>
    </div>
    <div id="o-ap" class="o-row o-ol"><div>Aprende neerlandés</div></div>
    <div id="o-bens" class="o-row"><div id="o-b1" class="o-ben">{ok42}<span>Desde el español</span></div><div id="o-b2" class="o-ben">{ok42}<span>A tu ritmo</span></div></div>
    <div id="o-cta" class="o-row"><div class="o-field">{av}<span id="o-ph">Añade un comentario…</span><span id="o-typed"></span><span id="o-caret"></span><span class="o-fill"></span><span id="o-post">Publicar<i id="o-ripple"></i></span></div></div>
    <div id="o-ok" class="o-row"><div class="o-ok">{ok}<span>Te contamos nuestro método por mensaje</span></div></div>
"""
    js = """
      // the freeze: a quick flash and punch-in on Suárez's look, then a slow push the whole time
      tl.fromTo("#o-flash", { opacity: 0.55 }, { opacity: 0, duration: 0.28, ease: "power2.out" }, «FREEZE»);
      tl.fromTo("#o-freeze", { scale: 1.10 }, { scale: 1.0, duration: 0.35, ease: "power3.out" }, «FREEZE»);
      tl.fromTo("#o-freeze", { scale: 1.0 }, { scale: 1.06, duration: «D» - 0.35, ease: "none", immediateRender: false }, «FREEZE» + 0.35);
      tl.fromTo("#o-shade", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, «FREEZE» + 0.1);
      // the beats
      tl.fromTo("#o-l1", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «L1»);
      tl.to("#o-l1", { opacity: 0, y: -30, duration: 0.18, ease: "power2.in" }, «L2» - 0.16);
      tl.fromTo("#o-l2", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «L2»);
      tl.fromTo("#o-p1", { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)" }, «C1»);
      tl.fromTo("#o-p2", { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)" }, «C2»);
      tl.fromTo("#o-p3", { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)" }, «C3»);
      tl.to(["#o-l2", "#o-pains"], { opacity: 0, y: -30, duration: 0.2, ease: "power2.in" }, «AP» - 0.18);
      tl.fromTo("#o-ap", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «AP»);
      tl.fromTo("#o-b1", { opacity: 0, y: 24, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)" }, «B1»);
      tl.fromTo("#o-b2", { opacity: 0, y: 24, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)" }, «B2»);
      // the call to action
      tl.fromTo("#o-cta", { opacity: 0, y: 46, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)" }, «CTA»);
      tl.set("#o-ph", { opacity: 0 }, «TYPE0»);
      tl.fromTo("#o-post", { opacity: 0.4 }, { opacity: 1, duration: 0.15 }, «TYPE0»);
      tl.fromTo("#o-ripple", { opacity: 0.9, scale: 0.2 }, { opacity: 0, scale: 1.5, duration: 0.45, ease: "power2.out", immediateRender: false }, «TAP»);
      tl.fromTo("#o-cta .o-field", { scale: 1 }, { scale: 0.97, duration: 0.09, ease: "power2.out", yoyo: true, repeat: 1 }, «TAP»);
      tl.fromTo("#o-ok", { opacity: 0, y: 22, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.40, ease: "back.out(1.6)" }, «CONFIRM»);
      (() => {                                               // «QUIERO» typed letter by letter (one state per letter: seek-safe)
        const el = document.getElementById("o-typed"), full = "QUIERO", typ = { n: 0 };
        el.textContent = "";
        tl.fromTo(typ, { n: 0 }, { n: full.length, duration: «TYPEDUR», ease: "none", immediateRender: false,
          onUpdate: () => { el.textContent = full.slice(0, Math.round(typ.n)); } }, «TYPE0»);
      })();
"""
    blink, k, on = [], c["CTA"], True
    while k < c["TYPE0"]:
        blink.append(f'      tl.set("#o-caret", {{ opacity: {1 if on else 0} }}, {k:.3f});'); k += 0.25; on = not on
    blink += [f'      tl.set("#o-caret", {{ opacity: 1 }}, {c["TYPE0"]:.3f});', f'      tl.set("#o-caret", {{ opacity: 0 }}, {c["TAP"]:.3f});']
    def sub(s):
        for key in sorted(v, key=len, reverse=True):
            s = s.replace(f"«{key}»", str(v[key]))
        return s
    fonts = "\n".join([f'    @font-face {{ font-family: "Poppins"; font-weight: {w}; src: url("assets/fonts/poppins-latin-{w}-normal.woff2") format("woff2"); }}'
                       for w in (700, 800)] +
                      ['    @font-face { font-family: "Inter"; font-weight: 100 900; src: url("assets/fonts/inter-var-latin.woff2") format("woff2"); }',
                       '    @font-face { font-family: "InterV"; font-weight: 100 900; src: url("assets/fonts/inter-var-latin.woff2") format("woff2"); }'])
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
