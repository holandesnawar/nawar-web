"""ins-04 · «este libro: 70 páginas en español, para imprimir, con vocabulario, gramática, ejercicios prácticos.» —
THE PRODUCT, the client's own ebook animation («Animación Libro», tools/libro_clip.py), the book lifted off its black and
floating on Nawar blue (v6: no black, no frame, no shadow), with v4's labels back:
  · the cover of «Holandés sin miedo» opens on «70 páginas»; the pages turn at their own speed (a soft page sound on
    the cover and each turn) while she lists what's inside; «¡Hora de practicar!» lies open as she says «ejercicios
    prácticos» and the camera pushes in on it until the cut back to her (on the second take, «cómo pronunciar…»);
  · under the book, white pills land on their words — «70 páginas», «En español» (ES flag), «Para imprimir» (printer) —
    then a ticked row: Vocabulario, Gramática, Ejercicios, and Pronunciación as she finishes the list (she says «cómo
    pronunciar» right after the cut); the «Ebook · Holandés sin miedo» label on top once the book is open.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

K = 1.3                        # display scale of the 1280×720 animation (the open spread, 766 px → ~1000 px)
BOOK_CX, BOOK_CY = 640, 367.5  # centre of the open book in the animation (1280×720 px)
CY = 590                       # where the book's centre sits in the frame
VW, VH = round(1280 * K, 1), round(720 * K, 1)
VL, VT = round(540 - BOOK_CX * K, 1), round(CY - BOOK_CY * K, 1)
PUSH = (454, 330)              # «¡Hora de practicar!» (left page), animation px
PAGES = [(0.50, 0.2), (1.75, 0.14), (2.75, 0.14), (3.75, 0.14)]   # the cover opening and three page turns (animation s, volume)


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(SET=cue(iid, "70"), ESP=cue(iid, "espanol"), IMP=cue(iid, "imprimir"), VOC=cue(iid, "vocabulario"),
             GRA=cue(iid, "gramatica"), EJE=cue(iid, "ejercicios"), PRA=cue(iid, "practicos"),
             VW=VW, VH=VH, VL=VL, VT=VT, OX=round(VL + PUSH[0] * K, 1), OY=round(VT + PUSH[1] * K, 1))
    css = """
    #i4-stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: «OX»px «OY»px; }
    #i4-vw { position: absolute; left: «VL»px; top: «VT»px; width: «VW»px; height: «VH»px;
      -webkit-mask-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 11%); mask-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 11%); }
    #i4-vw video { position: absolute; left: 0; top: 0; width: «VW»px; height: «VH»px; display: block; }
    #i4-lrow { top: 168px; }
    #i4-prow { top: 968px; gap: 16px; }
    .i4-wpill { gap: 12px; height: 76px; padding: 0 30px 0 18px; font-size: 33px; }
    .i4-wpill svg { display: block; width: 40px; height: 40px; color: «INDIGO»; }
    .i4-wpill .i4-flag svg { width: 40px; height: 27px; }
    #i4-crow { top: 1064px; gap: 10px; width: 1040px; left: 20px; }
    .i4-ck { display: flex; align-items: center; gap: 8px; height: 62px; padding: 0 22px 0 10px; border-radius: 999px;
      background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.30); color: #FFFFFF; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 27px; line-height: 1; }
    .i4-ck svg { display: block; width: 36px; height: 36px; }
"""
    pills = [("p0", icon("book"), "70 páginas"), ("p1", f'<span class="i4-flag i4-flagd">{FLAG_ES}</span>', "En español"),
             ("p2", icon("print"), "Para imprimir")]
    checks = ["Vocabulario", "Gramática", "Ejercicios", "Pronunciación"]
    body = "\n".join([ground(P, "blue"), f"""    <div id="i4-stage">
      <div id="i4-vw"><video id="i4-v" class="clip" src="assets/video/libro-ins04.webm" muted playsinline data-start="0" data-duration="«D»" data-track-index="1"></video></div>
    </div>
    <div id="i4-lrow" class="i4-row"><div id="i4-lab" class="i4-pill">{icon('book').replace('currentColor', '#FFFFFF')}<span>Ebook · Holandés sin miedo</span></div></div>
    <div id="i4-prow" class="i4-row">{"".join(f'<div id="i4-{pid}" class="i4-wpill">{ic}<span>{t}</span></div>' for pid, ic, t in pills)}</div>
    <div id="i4-crow" class="i4-row">{"".join(f'<div id="i4-c{k}" class="i4-ck">{icon("check")}<span>{t}</span></div>' for k, t in enumerate(checks))}</div>"""])
    js = """
      // a slow drift while the pages turn, then the push into «¡Hora de practicar!» on «ejercicios prácticos»
      tl.fromTo(q("stage"), { scale: 1.0 }, { scale: 1.03, duration: «EJE» - 0.1, ease: "none" }, 0);
      tl.fromTo(q("stage"), { scale: 1.03 }, { scale: 1.1, duration: «D» - «EJE» + 0.1, ease: "power2.inOut", immediateRender: false }, «EJE» - 0.1);
      tl.fromTo(q("lab"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 1.0);
"""
    for (pid, _, _), key in zip(pills, ("SET", "ESP", "IMP")):
        js += f'      tl.fromTo(q("{pid}"), {{ opacity: 0, y: 24, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, «{key}» - 0.06);\n'
    for k, (key, lead) in enumerate((("VOC", 0.05), ("GRA", 0.05), ("EJE", 0.05), ("PRA", -0.3))):
        js += f'      tl.fromTo(q("c{k}"), {{ opacity: 0, y: 18, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "back.out(1.7)" }}, «{key}» - {lead});\n'
    sp = 4.40 / (c["EJE"] - 0.10)                     # the animation's speed in the played part (tools/libro_clip.py)
    sfx = [(round(t / sp, 3), "page", v) for t, v in PAGES]
    sfx += [(c["SET"] - 0.06, "pop", 0.16), (c["ESP"] - 0.06, "pop", 0.16), (c["IMP"] - 0.06, "pop", 0.2)]
    sfx += [(c[k] - 0.05, "click-soft", 0.18) for k in ("VOC", "GRA", "EJE")] + [(c["PRA"] + 0.3, "click-soft", 0.18)]
    return comp(iid, d, P, css, body, js, c), sfx
