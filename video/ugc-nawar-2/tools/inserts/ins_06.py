"""ins-06 · «…(Cuentas con) ejercicios pensados para el día a día» — a quick flash of the real exercises (UGC #1 ins-04
design): title «Ejercicios / para el día a día», the deck of real exercise cards with their own margin, and the
Leer · Escribir · Escuchar pills, each entering with its card."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def build():
    iid, P = "ins-06", "i6"; d = INS[iid]["duration"]
    c = dict(PEN=cue(iid, "pensados"))
    IW = 860
    def crop(x0, y0, x1, y1, W, H):
        k = IW / (x1 - x0)
        return dict(w=round(W * k, 1), h=round(H * k, 1), l=round(-x0 * k, 1), t=round(-y0 * k, 1), ih=round((y1 - y0) * k, 1))
    E = crop(592, 0, 1474, 336, 1718, 690)     # «Completa la frase» (video)
    O = crop(74, 22, 1860, 690, 1902, 1080)    # «De familiefoto's» (listening)
    L = crop(244, 280, 1816, 940, 2048, 1447)  # «1.4 Lezen» (reading)
    # three beats inside ~1.7 s: write → listen → read, every card with its pill
    c.update(B1=0.04, B2=round(d * 0.36, 3), B3=round(d * 0.66, 3), ED=round(d + 0.2, 3))
    css = f"""
    #i6-h1 {{ top: 200px; }}
    #i6-h2 {{ top: 312px; }}
    .i6-card {{ position: absolute; left: 80px; top: 488px; width: 920px; border-radius: 34px; background: «APP»; transform-origin: 50% 0%;
      box-shadow: 0 40px 100px rgba(4,0,40,0.45), 0 8px 24px rgba(4,0,40,0.22); }}
    .i6-in {{ position: absolute; left: 30px; top: 30px; width: {IW}px; overflow: hidden; border-radius: 20px; background: #FFFFFF;
      box-shadow: 0 0 0 1px rgba(29,0,132,0.07); }}
    #i6-ce {{ height: {E['ih'] + 60}px; }} #i6-ce .i6-in {{ height: {E['ih']}px; }}
    #i6-co {{ height: {O['ih'] + 60}px; }} #i6-co .i6-in {{ height: {O['ih']}px; }}
    #i6-cl {{ height: {L['ih'] + 60}px; }} #i6-cl .i6-in {{ height: {L['ih']}px; }}
    #i6-ve {{ position: absolute; left: {E['l']}px; top: {E['t']}px; width: {E['w']}px; height: {E['h']}px; }}
    #i6-io {{ position: absolute; left: {O['l']}px; top: {O['t']}px; width: {O['w']}px; height: {O['h']}px; display: block; }}
    #i6-il {{ position: absolute; left: {L['l']}px; top: {L['t']}px; width: {L['w']}px; height: {L['h']}px; display: block; }}
    #i6-skills {{ top: 1010px; gap: 18px; }}
    .i6-sk {{ display: flex; align-items: center; gap: 12px; height: 70px; padding: 0 28px 0 16px; border-radius: 999px;
      background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); color: #FFFFFF; white-space: nowrap;
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 31px; line-height: 1; }}
    .i6-ic {{ position: relative; width: 44px; height: 44px; }}
    .i6-ic svg {{ position: absolute; left: 0; top: 0; width: 44px; height: 44px; }}
"""
    def skill(k, label):
        return f'<div id="i6-s{k}" class="i6-sk"><div class="i6-ic">{icon("check")}</div><span>{label}</span></div>'
    body = "\n".join([ground(P, "blue"), f"""    <div id="i6-h1" class="i6-h1">Ejercicios</div>
    <div id="i6-h2" class="i6-h1"><span id="i6-chip" class="i6-chip">para el día a día</span></div>
    <div id="i6-ce" class="i6-card"><div class="i6-in"><video id="i6-ve" class="clip" src="assets/video/completa-frase.mp4" muted playsinline data-start="0" data-duration="«ED»" data-media-start="6.0" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video></div></div>
    <div id="i6-co" class="i6-card"><div class="i6-in"><img id="i6-io" src="assets/img/ui-luisteren-audio.png" alt="" /></div></div>
    <div id="i6-cl" class="i6-card"><div class="i6-in"><img id="i6-il" src="assets/img/ui-lezen-texto.png" alt="" /></div></div>
    <div id="i6-skills" class="i6-row">{skill(1, 'Escribir')}{skill(2, 'Escuchar')}{skill(3, 'Leer')}</div>"""])
    js = """
      tl.fromTo(q("h1"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.26, ease: "power3.out" }, 0);
      tl.fromTo(q("chip"), { opacity: 0, scale: 0.7, rotation: -1.5 }, { opacity: 1, scale: 1, rotation: -1.5, duration: 0.3, ease: "back.out(1.8)" }, «PEN» - 0.06);
      tl.fromTo(q("ce"), { opacity: 0, y: 90 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «B1»);
      tl.fromTo(q("s1"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «B1»);
      tl.fromTo(q("co"), { opacity: 0, y: 110 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «B2»);
      tl.to(q("ce"), { y: -34, scale: 0.94, opacity: 0.55, duration: 0.3, ease: "power3.out" }, «B2»);
      tl.fromTo(q("s2"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «B2»);
      tl.fromTo(q("cl"), { opacity: 0, y: 110 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «B3»);
      tl.to(q("co"), { y: -34, scale: 0.94, opacity: 0.55, duration: 0.3, ease: "power3.out" }, «B3»);
      tl.to(q("ce"), { y: -62, scale: 0.88, opacity: 0.25, duration: 0.3, ease: "power3.out" }, «B3»);
      tl.fromTo(q("s3"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «B3»);
"""
    sfx = [(c["B1"], "click-soft", 0.2), (c["B2"], "click-soft", 0.2), (c["B3"], "click-soft", 0.2)]
    return comp(iid, d, P, css, body, js, c), sfx
