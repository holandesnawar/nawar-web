#!/usr/bin/env python3
"""The reel «Suárez habla neerlandés» (9:16, 25 fps), the second Luis Suárez reel:
- the interview full frame on his face (assets/video/habla-916.mp4, tools/frame.py: pushed in so his mouth sits above
  the subtitles);
- the hook, for the first seconds, at the top over his hair, in the client's design: «Hablando neerlandés / sin miedo
  como / Luis Suárez» in Inter ExtraBold, white with a thick round black outline, and the 📚 and 🇳🇱 icons of the
  client's mock-up (tools/img, cut from it) centred on either side of the middle line;
- the subtitles at the bottom: the Dutch phrase big, in capitals, one size for all, white with the word being said in
  yellow, and the Spanish under it, in a grey pill, all centred under his face;
- the closing ad (compositions/outro.html, from tools/outro.py's voice-over, book, cues and sound), in the design of the
  Black Friday page (blackfriday.holandesnawar.com/ebook): everything at once — the «Black Friday · eBook nivel A0–A1»
  badge, «Habla neerlandés / sin miedo.», the ebook opening and turning its pages under the white «Black Friday 1 €
  12,50 €» seal with «−92 %», the light-blue ticker — and, last, the call to action:
  an Instagram comment field typing «OFERTA», «Publicar», and «Te enviamos los detalles por mensaje».
  python3 tools/gen.py      → index.html, compositions/outro.html
"""
import html, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import outro as O  # noqa: E402

YEL = "#FFE11B"
SUB_BOTTOM = 1500                      # the subtitle block stands on this line (frame px): above Instagram's caption band
NL_W, NL_CX = 744, 540                 # centred, and left of its button rail (x > 912 from y ≈ 814)
NL_SIZE = 62                           # one size, two lines at most («|» in tools/subs.py breaks them)
ES_SIZE = 38
MIN_ON = 0.6                           # a phrase on screen for less than this opens a little early (after the last word
                                       # before it); one that stays long enough after its word (up to 0.7 s) does not
BRIDGE = 0.25                          # a gap shorter than this between two phrases is closed (no one-frame blink)
# the hook (v7, the client's design): Inter ExtraBold, white, a black outline of ~7.5 % of the size with round corners
# (the client's mock-up), three lines; the icons centred on the middle line, one on each side
HOOK_TOP, HOOK_SIZE, HOOK_LH = 180, 77, 1.06   # under Instagram's header, over his hair (it ends at y ≈ 425: his brows
HOOK_OUTLINE = 6                       # stay under it, also when he raises them on «Wie?»); outline px, outside the glyph
HOOK_OUT = 3.30                        # …and it leaves here (it is the cover too: on screen from the first frame)
HOOK = ["Hablando neerlandés", "sin miedo como", "Luis Suárez"]
ICONS = {"books": 108, "nl": 88}       # display height (px): about the proportions of the mock-up, clear of the other lines
ICON_DY = {"books": 22, "nl": 9}       # below the middle line's centre (px): the flag on its letters' x-height, the books
                                       # a little lower still, well clear of the «H» of «Hablando» above them
ICON_GAP = 18                          # between the middle line's outline and each icon
OUT_LEAD = 0.30                        # the closing ad comes in over the interview's last 0.3 s

INDIGO, SKY, RED = "#1D0084", "#4DA3FF", "#DC2626"


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
    """compositions/outro.html: the closing ad, O.END s long, every moment from O.cues()."""
    lib = json.load(open(os.path.join(ROOT, "assets", "video", "libro.json")))
    c = O.cues()
    BW, BH = lib["width"], lib["height"]
    v = dict(c, BL=540 - BW // 2, BT=572, BW=BW, BH=BH, BS=lib["start"], BD=round(lib["end"] - lib["start"], 3),
             D=O.END, TYPEDUR=round(c["TYPE1"] - c["TYPE0"], 3), INDIGO=INDIGO, SKY=SKY, RED=RED)
    css = """
    #o-root { position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; color: #FFFFFF; }
    .o-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    /* the page's hero: indigo, two soft blue lights and a faint dot grid */
    #o-ground { background: «INDIGO»; }
    .o-luz1 { position: absolute; top: -280px; right: -320px; width: 1300px; height: 1300px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.42) 0%, rgba(11,109,240,0) 65%); }
    .o-luz2 { position: absolute; bottom: -260px; left: -280px; width: 1150px; height: 1150px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.20) 0%, rgba(11,109,240,0) 65%); }
    .o-dots { position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,255,255,0.06) 2px, transparent 2.2px);
      background-size: 52px 52px; }
    .o-row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; }
    /* the badge: «BLACK FRIDAY · EBOOK NIVEL A0 – A1» (v7.6: without the page's green dot) */
    #o-badge { top: 212px; }
    .o-badge { display: flex; align-items: center; height: 64px; padding: 0 32px; border-radius: 999px;
      background: #025DC7; color: #E0F2FF; font-weight: 700; font-size: 25px; letter-spacing: 0.14em; text-transform: uppercase;
      white-space: nowrap; line-height: 1; }
    /* the headline, as the page's title: Poppins 700, the first line in a white gradient, the second in sky blue */
    .o-h { font-family: "Poppins", sans-serif; font-weight: 700; font-size: 96px; line-height: 1.08; letter-spacing: -0.03em;
      white-space: nowrap; }
    #o-l1 { top: 296px; }
    #o-l1 span { background: linear-gradient(180deg, #FFFFFF 10%, rgba(255,255,255,0.55) 100%); -webkit-background-clip: text;
      background-clip: text; -webkit-text-fill-color: transparent; color: transparent; padding: 0 6px; }
    #o-l2 { top: 400px; color: «SKY»; }
    /* the book, and the page's white seal over its corner */
    #o-book { position: absolute; left: «BL»px; top: «BT»px; width: «BW»px; height: «BH»px; }
    #o-book video { position: absolute; left: 0; top: 0; width: «BW»px; height: «BH»px; display: block; }
    #o-seal { position: absolute; left: 120px; top: 540px; transform-origin: 30% 50%; }   /* (at 0.78: over the book's corner
                                                     and its blue band only, never over the page headings) */
    .o-seal { position: relative; padding: 20px 30px 22px; border-radius: 28px; background: #FFFFFF; overflow: hidden; }
    .o-seal .k { font-weight: 700; font-size: 25px; letter-spacing: 0.14em; color: «RED»; line-height: 1; }
    .o-seal .p { display: flex; align-items: flex-end; gap: 18px; margin-top: 28px; }   /* (the 112 px price keeps its own line box clear of the label) */
    #o-eur { display: inline-block; font-family: "Poppins", sans-serif; font-weight: 700; font-size: 112px; line-height: 1;
      letter-spacing: -0.03em; color: «INDIGO»; transform-origin: 40% 60%; }
    .o-seal s { font-family: "Poppins", sans-serif; font-weight: 600; font-size: 40px; color: #5B6380; line-height: 1; padding-bottom: 15px;
      text-decoration-color: «RED»; text-decoration-thickness: 4px; }
    #o-shine { position: absolute; top: -40px; left: -160px; width: 110px; height: 320px; transform: rotate(18deg);
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.85) 50%, rgba(255,255,255,0) 100%); opacity: 0.7; }
    #o-off { position: absolute; left: 339px; top: -16px; transform-origin: 50% 50%; }
    .o-off { padding: 12px 22px; border-radius: 999px; background: #E02D3C; color: #FFFFFF; font-family: "Poppins", sans-serif;
      font-weight: 700; font-size: 38px; line-height: 1; white-space: nowrap; }
    /* the page's light-blue ticker */
    #o-band { position: absolute; left: -10px; top: 1240px; width: 1100px; height: 64px; background: «SKY»; overflow: hidden; }
    #o-track { position: absolute; left: 0; top: 0; height: 64px; display: flex; align-items: center; white-space: nowrap; }
    #o-track span { display: flex; align-items: center; gap: 16px; padding: 0 26px; color: «INDIGO»; font-weight: 700; font-size: 30px; line-height: 1; }
    #o-track b { font-size: 26px; }
    /* the call to action: an Instagram comment field */
    #o-cta { top: 1326px; }
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
    #o-ok { top: 1436px; }
    .o-ok { display: flex; align-items: center; gap: 14px; height: 60px; padding: 0 26px 0 14px; border-radius: 16px;
      background: rgba(34,197,94,0.18); border: 2px solid rgba(34,197,94,0.55); font-weight: 700; font-size: 29px; white-space: nowrap; }
    .o-ok svg { display: block; width: 36px; height: 36px; }
"""
    # (v7.6: «Ejercicios con respuestas» out — the client says it is not so; «Vocabulario y gramática» comes from their own
    # Black Friday ad script)
    ticker = ["70 páginas", "Explicado en español", "Vocabulario y gramática", "Tuyo para siempre", "Black Friday: −92 %",
              "Descarga al momento"]
    track = "".join(f"<span><b>✦</b>{html.escape(t)}</span>" for t in ticker * 4)
    av = ('<svg class="o-av" viewBox="0 0 62 62"><circle cx="31" cy="31" r="31" fill="#E6E8EF"/><circle cx="31" cy="25" r="11" fill="#A9AFBE"/>'
          '<path d="M11 52 C14 41 22 37 31 37 C40 37 48 41 51 52 A30 30 0 0 1 11 52 Z" fill="#A9AFBE"/></svg>')
    ok = ('<svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="18" fill="#22C55E"/><path d="M10 18.5 L15.5 24 L26 12.5" fill="none" '
          'stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    body = f"""
    <div id="o-ground" class="o-full"><div class="o-luz1"></div><div class="o-luz2"></div><div class="o-dots"></div></div>
    <div id="o-badge" class="o-row"><div class="o-badge"><span>Black Friday · eBook nivel A0 – A1</span></div></div>
    <div id="o-l1" class="o-row o-h"><span>Habla neerlandés</span></div>
    <div id="o-l2" class="o-row o-h">sin miedo.</div>
    <div id="o-book"><video id="o-v" class="clip" src="assets/video/libro.webm" muted playsinline data-start="«BS»" data-duration="«BD»" data-track-index="1"></video></div>
    <div id="o-seal"><div class="o-seal"><div class="k">BLACK FRIDAY</div><div class="p"><span id="o-eur">1&nbsp;€</span><s>12,50&nbsp;€</s></div><div id="o-shine"></div></div>
      <div id="o-off"><div class="o-off">−92&nbsp;%</div></div></div>
    <div id="o-band"><div id="o-track">{track}</div></div>
    <div id="o-cta" class="o-row"><div class="o-field">{av}<span id="o-ph">Añade un comentario…</span><span id="o-typed"></span><span id="o-caret"></span><span class="o-fill"></span><span id="o-post">Publicar<i id="o-ripple"></i></span></div></div>
    <div id="o-ok" class="o-row"><div class="o-ok">{ok}<span>Te enviamos los detalles por mensaje</span></div></div>
"""
    js = """
      // everything comes in at once (0.2–0.8 s), the call to action last
      tl.fromTo("#o-ground", { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.28, ease: "power2.out" }, «GROUND»);
      tl.fromTo("#o-badge", { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.40, ease: "power3.out" }, «BADGE»);
      tl.fromTo("#o-l1", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L1»);
      tl.fromTo("#o-l2", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L2»);
      tl.fromTo("#o-book", { opacity: 0, y: 70, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "power3.out" }, «BOOK»);
      tl.fromTo("#o-band", { x: -1120 }, { x: 0, duration: 0.50, ease: "power3.out" }, «BAND»);
      tl.fromTo("#o-track", { xPercent: 0 }, { xPercent: -25, duration: «D», ease: "none" }, 0);
      tl.fromTo("#o-seal", { opacity: 0, scale: 0.45, rotation: -14 }, { opacity: 1, scale: 0.78, rotation: 0, duration: 0.50, ease: "back.out(1.8)" }, «SEAL»);
      tl.fromTo("#o-off", { opacity: 0, scale: 0.2, rotation: 30 }, { opacity: 1, scale: 1, rotation: 8, duration: 0.40, ease: "back.out(2.2)" }, «OFF»);
      tl.fromTo("#o-eur", { scale: 1 }, { scale: 1.14, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }, «EURO»);
      tl.fromTo("#o-cta", { opacity: 0, y: 46, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.5)" }, «CTA»);
      tl.set("#o-ph", { opacity: 0 }, «TYPE0»);
      tl.fromTo("#o-post", { opacity: 0.4 }, { opacity: 1, duration: 0.15 }, «TYPE0»);
      tl.fromTo("#o-ripple", { opacity: 0.9, scale: 0.2 }, { opacity: 0, scale: 1.5, duration: 0.45, ease: "power2.out", immediateRender: false }, «TAP»);
      tl.fromTo("#o-cta .o-field", { scale: 1 }, { scale: 0.97, duration: 0.09, ease: "power2.out", yoyo: true, repeat: 1 }, «TAP»);
      tl.fromTo("#o-ok", { opacity: 0, y: 22, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.40, ease: "back.out(1.6)" }, «CONFIRM»);
      tl.fromTo("#o-shine", { x: 0 }, { x: 620, duration: 0.75, ease: "power2.inOut" }, «SHINE»);
      (() => {                                               // «OFERTA» typed letter by letter (one state per letter: seek-safe)
        const el = document.getElementById("o-typed"), full = "OFERTA", typ = { n: 0 };
        el.textContent = "";
        tl.fromTo(typ, { n: 0 }, { n: full.length, duration: «TYPEDUR», ease: "none", immediateRender: false,
          onUpdate: () => { el.textContent = full.slice(0, Math.round(typ.n)); } }, «TYPE0»);
      })();
"""
    blink, k, on = [], c["CTA"], True                       # the caret blinks while waiting, steady while typing, then goes
    while k < c["TYPE0"]:
        blink.append(f'      tl.set("#o-caret", {{ opacity: {1 if on else 0} }}, {k:.3f});'); k += 0.25; on = not on
    blink += [f'      tl.set("#o-caret", {{ opacity: 1 }}, {c["TYPE0"]:.3f});', f'      tl.set("#o-caret", {{ opacity: 0 }}, {c["TAP"]:.3f});']
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


def main():
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)   # the hook's icons, cut from the client's mock-up
    for k in ICONS:
        shutil.copyfile(os.path.join(ROOT, "tools", "img", f"emoji-{k}.png"), os.path.join(ROOT, "assets", "img", f"emoji-{k}.png"))
    meta = json.load(open(os.path.join(ROOT, "assets", "video", "habla-916.json")))
    D = meta["duration"]
    OUT0 = round(D - OUT_LEAD, 3)
    TOTAL = round(OUT0 + O.END, 3)
    subs = json.load(open(os.path.join(ROOT, "subs.json")))["phrases"]
    cues = outro_html()
    body, js = [], []
    cuts = [s["reel"] for s in meta["segments"][1:]]          # the hard cuts between the moments: no phrase crosses one
    ons = []
    for k, p in enumerate(subs):
        words_k = p["words"]
        on = max(0.0, words_k[0]["t"] - 0.05)
        nxt = subs[k + 1]["words"][0]["t"] - 0.05 if k + 1 < len(subs) else D
        if min(nxt, words_k[-1]["end"] + 0.7) - on < MIN_ON and k:
            on = max(subs[k - 1]["words"][-1]["end"] + 0.03, min(on, words_k[-1]["end"] - MIN_ON))
        on = max([on] + [c for c in cuts if c <= words_k[0]["t"]])
        ons.append(on)
    for k, p in enumerate(subs):
        words_k = p["words"]
        on = ons[k]
        off = min(ons[k + 1], words_k[-1]["end"] + 0.7) if k + 1 < len(subs) else D
        if k + 1 < len(subs) and ons[k + 1] - off < BRIDGE:
            off = ons[k + 1]
        off = min([off] + [c for c in cuts if c > on])
        spans = " ".join(('<span class="br"></span> ' if i in p.get("breaks", []) else "") +
                         f'<span id="w{k}-{i}" class="w">{html.escape(w["text"])}</span>' for i, w in enumerate(words_k))
        body.append(f'      <div id="p{k}" class="ph"><div class="nl">{spans}</div>'
                    f'<div class="es"><span>{html.escape(p["es"]).replace("|", "<br>")}</span></div></div>')
        js.append(f'      tl.set("#p{k}", {{ opacity: 1 }}, {on:.3f});')
        js.append(f'      tl.fromTo("#p{k} .nl", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.16, ease: "back.out(1.6)", immediateRender: false }}, {on:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 0 }}, {off:.3f});')
        for i, w in enumerate(words_k):
            t1 = words_k[i + 1]["t"] - 0.03 if i + 1 < len(words_k) else off
            js.append(f'      tl.set("#w{k}-{i}", {{ color: "{YEL}" }}, {max(on, w["t"] - 0.03):.3f});')
            if i + 1 < len(words_k):
                js.append(f'      tl.set("#w{k}-{i}", {{ color: "#FFFFFF" }}, {t1:.3f});')
    fonts = "\n".join([f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{f.lower()}-latin-{w}-normal.woff2") format("woff2"); }}'
                       for f, w in (("Poppins", 700), ("Poppins", 900), ("Inter", 600), ("Inter", 700))] +
                      ['      @font-face { font-family: "InterV"; font-weight: 100 900; src: url("assets/fonts/inter-var-latin.woff2") format("woff2"); }'])
    icons = {k: f'<img class="em em-{k}" src="assets/img/emoji-{k}.png" alt="">' for k in ICONS}
    hook = (f'<div class="hl"><span>{html.escape(HOOK[0])}</span></div>'
            f'<div class="hl"><span class="mid">{icons["books"]}{html.escape(HOOK[1])}{icons["nl"]}</span></div>'
            f'<div class="hl"><span>{html.escape(HOOK[2])}</span></div>')
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
      <video id="v" class="clip" src="assets/video/habla-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-bot" class="shade"></div>
      <div id="hook">{hook}</div>
{chr(10).join(body)}
      <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" data-start="{OUT0}" data-duration="{O.END}" data-track-index="2" data-width="1080" data-height="1920"></div>
      <audio id="a-outro" src="assets/audio/outro.wav" data-start="{OUT0}" data-duration="{O.END}" data-track-index="3"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // the hook: on screen from the first frame (it is the cover), it leaves at {HOOK_OUT} s
      tl.to("#hook", {{ opacity: 0, scale: 0.96, duration: 0.30, ease: "power2.in" }}, {HOOK_OUT});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(page)
    print(f"index.html: {TOTAL}s (the interview {D}s, the closing ad from {OUT0}s), {len(subs)} subtitle phrases; outro cues "
          + ", ".join(f"{k} {v:.2f}" for k, v in cues.items()))


if __name__ == "__main__":
    main()
