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
VSL = os.path.join(ROOT, "..", "vsl-formacion-nawar")
LAP_S, LAP_CY = 0.88, 900     # the laptop in the frame: its 1920×1080 space scaled LAP_S, the straight-on device centred at y = LAP_CY
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
    """compositions/outro.html (v9): the closing ad, O.END s long, every moment from O.cues(). The VSL's MacBook
    (../vsl-formacion-nawar/tools/gen_laptop_20_21.py: the same CSS-3D rig, imported, in its 1920×1080 space, scaled
    LAP_S into the 9:16 frame) arrives closed, seen from above, and opens straight onto the course: the lesson list
    (assets/video/plat-curso.mp4, the cursor resting on a video lesson), then, as if clicked, a video lesson with the
    teacher (plat-clase.mp4). Over it: the badge «Formación Nawar · A0 – A1», «Aprende neerlandés / desde el español»,
    a Black Friday «Últimas plazas» sign on «Black Friday», and the call to action of the second reel: an Instagram
    comment field typing «OFERTA», «Publicar», «Te enviamos los detalles por mensaje»."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("vsl_laptop", os.path.join(VSL, "tools", "gen_laptop_20_21.py"))
    L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
    c = O.cues()
    P = "lp"
    # the closed laptop seen from above, a little turned, centred where it will open (cam space)
    top = dict(zip(("x", "y"), L.pose((0, L.LIDC), (960, 560), 0.92, -12.0)), rotation=-12.0, scale=0.92)
    cen = L.CEN
    cen2 = dict(zip(("x", "y"), L.pose((0, L.BOX_H / 2 - L.HY), (960, 520), L.S1 * 1.03, 0)), rotation=0, scale=round(L.S1 * 1.03, 4))
    lap_l, lap_t = round(540 - 960 * LAP_S, 1), round(LAP_CY - 520 * LAP_S, 1)
    v = dict(c, D=O.END, INDIGO=INDIGO, SKY=SKY, RED="#DC2626", LAPL=lap_l, LAPT=lap_t, LAPS=LAP_S)
    css = """
    #o-root { position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; color: #FFFFFF; }
    .o-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    #o-ground { background: «INDIGO»; }
    .o-luz1 { position: absolute; top: -280px; right: -320px; width: 1300px; height: 1300px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.42) 0%, rgba(11,109,240,0) 65%); }
    .o-luz2 { position: absolute; bottom: -260px; left: -280px; width: 1150px; height: 1150px; border-radius: 50%;
      background: radial-gradient(circle, rgba(11,109,240,0.20) 0%, rgba(11,109,240,0) 65%); }
    .o-dots { position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,255,255,0.06) 2px, transparent 2.2px);
      background-size: 52px 52px; }
    .o-row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; }
    #o-badge { top: 196px; }
    .o-badge { display: flex; align-items: center; height: 62px; padding: 0 30px; border-radius: 999px; background: #025DC7; color: #E0F2FF;
      font-weight: 700; font-size: 25px; letter-spacing: 0.14em; text-transform: uppercase; white-space: nowrap; line-height: 1; }
    .o-h { font-family: "Poppins", sans-serif; font-weight: 700; font-size: 94px; line-height: 1.08; letter-spacing: -0.03em; white-space: nowrap; }
    #o-h1 { top: 280px; }
    #o-h1 span { background: linear-gradient(180deg, #FFFFFF 10%, rgba(255,255,255,0.6) 100%); -webkit-background-clip: text;
      background-clip: text; -webkit-text-fill-color: transparent; color: transparent; padding: 0 6px; }
    #o-h2 { top: 382px; color: «SKY»; }
    /* the laptop: the VSL's rig in its own 1920×1080 space, scaled into the frame */
    #o-lapw { position: absolute; left: «LAPL»px; top: «LAPT»px; width: 1920px; height: 1080px; transform-origin: 0 0; transform: scale(«LAPS»); }
    #o-lap { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
    #lp-browser { position: absolute; left: 0; top: 0; width: 100%; height: 100%; background: #FFFFFF; }
    /* the Black Friday sign over the laptop's top-right corner */
    #o-sign { position: absolute; left: 648px; top: 528px; transform-origin: 50% 50%; }
    .o-sign { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 20px 30px 22px; border-radius: 26px;
      background: #0C0C1E; box-shadow: 0 0 0 3px rgba(255,255,255,0.92), 0 18px 40px rgba(2,0,24,0.45); overflow: hidden; position: relative; }
    .o-sign .k { font-family: "Poppins", sans-serif; font-weight: 800; font-size: 46px; line-height: 1; letter-spacing: 0.04em; color: #FFFFFF; white-space: nowrap; }
    .o-sign .p { display: flex; align-items: center; gap: 12px; height: 54px; padding: 0 22px; border-radius: 999px; background: «RED»;
      font-weight: 800; font-size: 27px; letter-spacing: 0.10em; color: #FFFFFF; white-space: nowrap; line-height: 1; }
    #o-dot { display: block; width: 14px; height: 14px; border-radius: 50%; background: #FFFFFF; }
    #o-shine { position: absolute; top: -40px; left: -160px; width: 90px; height: 260px; transform: rotate(18deg);
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.45) 50%, rgba(255,255,255,0) 100%); }
    /* the call to action: an Instagram comment field (as in the second reel) */
    #o-cta { top: 1262px; }
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
    #o-ok { top: 1372px; }
    .o-ok { display: flex; align-items: center; gap: 14px; height: 60px; padding: 0 26px 0 14px; border-radius: 16px;
      background: rgba(34,197,94,0.18); border: 2px solid rgba(34,197,94,0.55); font-weight: 700; font-size: 29px; white-space: nowrap; }
    .o-ok svg { display: block; width: 36px; height: 36px; }
"""
    rig = L.rig_css(P)
    rig = rig[rig.index("    /* ---------- 2D cam"):]                     # (not the VSL's #root nor its ground: ours is the indigo)
    css_rig = rig + L.mockup_css(P) + L.chrome_css(P)
    screen = f"""                  <div id="lp-browser">
                    <div class="lp-chrome">
                      <div class="lp-tabs"><i class="lp-tl lp-tl-r"></i><i class="lp-tl lp-tl-y"></i><i class="lp-tl lp-tl-g"></i>
                        <div class="lp-tab"><div class="lp-fav"><img src="assets/img/logo-nawar.png" alt="" /></div><div class="lp-tab-t">Formación Nawar A0–A1</div><svg class="lp-tab-x" viewBox="0 0 10 10" aria-hidden="true"><path d="M2.2 2.2 L7.8 7.8 M7.8 2.2 L2.2 7.8" fill="none" stroke="#5F6368" stroke-width="1.3" stroke-linecap="round" /></svg></div>
                        <svg class="lp-plus" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 2.2 V11.8 M2.2 7 H11.8" fill="none" stroke="#5F6368" stroke-width="1.4" stroke-linecap="round" /></svg></div>
                      <div class="lp-bar"><svg class="lp-nav" viewBox="0 0 86 16" aria-hidden="true"><g fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13 8 H3.4 M7.8 3.6 L3.4 8 L7.8 12.4" stroke="#5F6368" /><path d="M31 8 H40.6 M36.2 3.6 L40.6 8 L36.2 12.4" stroke="#BDC1C6" /><path d="M68.7 8.6 A4.8 4.8 0 1 1 67.3 4.5 M68 1.9 V5.1 H64.8" stroke="#5F6368" /></g></svg>
                        <div class="lp-url"><svg class="lp-lock" viewBox="0 0 13 13" aria-hidden="true"><path d="M4.3 6 V4.3 A2.2 2.2 0 0 1 8.7 4.3 V6" fill="none" stroke="#5F6368" stroke-width="1.3" /><rect x="2.6" y="5.8" width="7.8" height="5.9" rx="1.3" fill="#5F6368" /></svg><div class="lp-url-t">app.holandesnawar.com</div><svg class="lp-star" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1.8 L8.55 5.05 L12.1 5.5 L9.5 7.95 L10.15 11.5 L7 9.8 L3.85 11.5 L4.5 7.95 L1.9 5.5 L5.45 5.05 Z" fill="none" stroke="#5F6368" stroke-width="1.1" stroke-linejoin="round" /></svg></div>
                        <svg class="lp-menu" viewBox="0 0 16 16" aria-hidden="true"><g fill="#5F6368"><circle cx="8" cy="3.4" r="1.35" /><circle cx="8" cy="8" r="1.35" /><circle cx="8" cy="12.6" r="1.35" /></g></svg></div>
                    </div>
                    <div class="lp-content">
                      <video id="lp-vid1" class="clip lp-media" src="assets/video/plat-curso.mp4" muted playsinline data-start="0" data-duration="«SWITCH»" data-media-start="0" data-track-index="2"></video>
                      <video id="lp-vid2" class="clip lp-media" src="assets/video/plat-clase.mp4" muted playsinline data-start="«SWITCH»" data-duration="{round(O.END - c['SWITCH'], 3)}" data-media-start="0" data-track-index="3"></video>
                    </div>
                  </div>"""
    av = ('<svg class="o-av" viewBox="0 0 62 62"><circle cx="31" cy="31" r="31" fill="#E6E8EF"/><circle cx="31" cy="25" r="11" fill="#A9AFBE"/>'
          '<path d="M11 52 C14 41 22 37 31 37 C40 37 48 41 51 52 A30 30 0 0 1 11 52 Z" fill="#A9AFBE"/></svg>')
    ok = ('<svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="18" fill="#22C55E"/><path d="M10 18.5 L15.5 24 L26 12.5" fill="none" '
          'stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    body = f"""
    <div id="o-ground" class="o-full"><div class="o-luz1"></div><div class="o-luz2"></div><div class="o-dots"></div></div>
    <div id="o-badge" class="o-row"><div class="o-badge"><span>Formación Nawar · A0 – A1</span></div></div>
    <div id="o-h1" class="o-row o-h"><span>Aprende neerlandés</span></div>
    <div id="o-h2" class="o-row o-h">desde el español</div>
    <div id="o-lapw" data-layout-allow-overflow><div id="o-lap">
{L.rig_html(P, screen)}
    </div></div>
    <div id="o-sign" data-layout-allow-overlap><div class="o-sign"><div class="k" data-layout-allow-overlap>BLACK FRIDAY</div><div class="p" data-layout-allow-overlap><i id="o-dot"></i><span>ÚLTIMAS PLAZAS</span></div><i id="o-shine"></i></div></div>
    <div id="o-cta" class="o-row"><div class="o-field">{av}<span id="o-ph">Añade un comentario…</span><span id="o-typed"></span><span id="o-caret"></span><span class="o-fill"></span><span id="o-post">Publicar<i id="o-ripple"></i></span></div></div>
    <div id="o-ok" class="o-row"><div class="o-ok">{ok}<span>Te enviamos los detalles por mensaje</span></div></div>
"""
    js = L.rig_state_js(P, top, L.BODY0, -90) + """
      tl.fromTo("#o-ground", { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.28, ease: "power2.out" }, «GROUND»);
      tl.fromTo("#o-badge", { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.40, ease: "power3.out" }, «BADGE»);
      tl.fromTo("#o-h1", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «H1»);
      tl.fromTo("#o-h2", { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «H2»);
      // the laptop: in closed, seen from above; the camera comes down to straight on as the lid swings open (the VSL's move)
      tl.fromTo("#o-lap", { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, «LAP»);
      tl.fromTo($("lp-cam"), CAM_TOP, Object.assign({}, CAM_CEN, { duration: 1.05, ease: "power3.out", immediateRender: false }), «OPEN»);
      tl.fromTo($("lp-body"), { rotationX: BODY0 }, { rotationX: 0, duration: 0.5, ease: "power3.out", immediateRender: false }, «OPEN»);
      tl.fromTo($("lp-lid"), { rotationX: -90 }, { rotationX: 0, duration: 0.92, ease: "power2.inOut", immediateRender: false }, «OPEN» + 0.06);
      tl.fromTo($("lp-stage"), { perspective: PERSP }, { perspective: PERSP_END, duration: 1.0, ease: "power2.inOut" }, «OPEN»);
      tl.fromTo($("lp-tsp"), { opacity: 1 }, { opacity: 0, duration: 0.35, ease: "power1.in" }, «OPEN» + 0.05);
      tl.fromTo([$("lp-csh"), $("lp-coc")], { opacity: 0 }, { opacity: 1, duration: 0.55, ease: "power2.out" }, «OPEN» + 0.4);
      tl.fromTo($("lp-cam"), CAM_CEN, Object.assign({}, CAM_CEN2, { duration: «D» - «OPEN» - 1.05, ease: "sine.inOut", immediateRender: false }), «OPEN» + 1.05);
      // the Black Friday sign lands on «Black Friday»; its dot blinks
      tl.fromTo("#o-sign", { opacity: 0, scale: 0.4, rotation: -16 }, { opacity: 1, scale: 1, rotation: 6, duration: 0.5, ease: "back.out(1.9)" }, «POSTER»);
      tl.fromTo("#o-shine", { x: 0 }, { x: 560, duration: 0.75, ease: "power2.inOut" }, «POSTER» + 0.45);
      tl.fromTo("#o-shine", { x: 0 }, { x: 560, duration: 0.75, ease: "power2.inOut", immediateRender: false }, «SHINE»);
      // the call to action
      tl.fromTo("#o-cta", { opacity: 0, y: 46, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.5)" }, «CTA»);
      tl.set("#o-ph", { opacity: 0 }, «TYPE0»);
      tl.fromTo("#o-post", { opacity: 0.4 }, { opacity: 1, duration: 0.15 }, «TYPE0»);
      tl.fromTo("#o-ripple", { opacity: 0.9, scale: 0.2 }, { opacity: 0, scale: 1.5, duration: 0.45, ease: "power2.out", immediateRender: false }, «TAP»);
      tl.fromTo("#o-cta .o-field", { scale: 1 }, { scale: 0.97, duration: 0.09, ease: "power2.out", yoyo: true, repeat: 1 }, «TAP»);
      tl.fromTo("#o-ok", { opacity: 0, y: 22, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.40, ease: "back.out(1.6)" }, «CONFIRM»);
      (() => {                                               // «OFERTA» typed letter by letter (one state per letter: seek-safe)
        const el = document.getElementById("o-typed"), full = "OFERTA", typ = { n: 0 };
        el.textContent = "";
        tl.fromTo(typ, { n: 0 }, { n: full.length, duration: «TYPEDUR», ease: "none", immediateRender: false,
          onUpdate: () => { el.textContent = full.slice(0, Math.round(typ.n)); } }, «TYPE0»);
      })();
"""
    js = (js.replace("CAM_TOP", L.js(top)).replace("CAM_CEN2", L.js(cen2)).replace("CAM_CEN", L.js(cen))
            .replace("BODY0", str(L.BODY0)).replace("PERSP_END", str(L.PERSP_END)).replace("PERSP", f"{L.PERSP:.0f}"))
    v["TYPEDUR"] = round(c["TYPE1"] - c["TYPE0"], 3)
    blink, k, on = [], c["POSTER"] + 0.5, True                # the sign's dot blinks; the caret blinks while waiting
    while k < O.END:
        blink.append(f'      tl.set("#o-dot", {{ opacity: {1 if on else 0.25} }}, {k:.3f});'); k += 0.4; on = not on
    k, on = c["CTA"], True
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
{css_rig}
  </style>
  <div id="o-root" data-composition-id="outro" data-width="1080" data-height="1920" data-duration="{O.END}">
{sub(body)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const $ = (id) => document.getElementById(id);
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
