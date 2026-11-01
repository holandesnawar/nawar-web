"""ins-04 · «este libro: 70 páginas en español, para imprimir, con vocabulario, gramática, ejercicios prácticos.» —
THE PRODUCT, the client's own ebook animation («Animación Libro», tools/libro_clip.py) full screen on its own black,
nothing behind it: the cover of «Holandés sin miedo», which opens on «70 páginas»; the pages turn at their own speed
while she lists what's inside; «¡Hora de practicar!» lies open as she says «ejercicios prácticos» and the camera
pushes in on it until the cut back to her (on the second take, «cómo pronunciar…»). A quiet title above the book
(«Ebook» · «Holandés sin miedo») and its reflection on the black floor; the captions do the talking.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

K = 1.358                      # display scale of the 1280×720 animation (the open spread, 766 px, fills ~1040 px)
BOOK_CX, BOOK_CY = 640, 367.5  # centre of the open book in the animation (1280×720 px)
BOOK_BOTTOM = 624
CY = 760                       # where the book's centre sits in the frame
VW, VH = round(1280 * K, 1), round(720 * K, 1)
VL, VT = round(540 - BOOK_CX * K, 1), round(CY - BOOK_CY * K, 1)
PUSH = (454, 330)              # «¡Hora de practicar!» (left page), animation px


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(SET=cue(iid, "70"), EJE=cue(iid, "ejercicios"), VW=VW, VH=VH, VL=VL, VT=VT,
             RT=round(VT + BOOK_BOTTOM * K, 1), RO=round(-(VH - BOOK_BOTTOM * K), 1),
             OX=round(VL + PUSH[0] * K, 1), OY=round(VT + PUSH[1] * K, 1), RD=round(d - 1 / 30, 3))
    css = """
    #i4-bg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; background: #000000; }
    #i4-stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: «OX»px «OY»px; }
    #i4-vw { position: absolute; left: «VL»px; top: «VT»px; width: «VW»px; height: «VH»px;
      -webkit-mask-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 10%); mask-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 10%); }
    #i4-vw video, #i4-rw video { position: absolute; left: 0; top: 0; width: «VW»px; height: «VH»px; display: block; }
    #i4-rw { position: absolute; left: «VL»px; top: «RT»px; width: «VW»px; height: 300px; overflow: hidden; opacity: 0.22;
      -webkit-mask-image: linear-gradient(180deg, #000 0%, rgba(0,0,0,0) 70%); mask-image: linear-gradient(180deg, #000 0%, rgba(0,0,0,0) 70%); }
    #i4-rw video { top: «RO»px; transform: scaleY(-1); }
    #i4-lab { position: absolute; left: 0; top: 176px; width: 1080px; text-align: center; font-family: "Inter", sans-serif; font-weight: 700;
      font-size: 24px; line-height: 1; letter-spacing: 0.32em; color: rgba(255,255,255,0.55); text-transform: uppercase; }
    #i4-tit { position: absolute; left: 0; top: 218px; width: 1080px; text-align: center; font-weight: 800; font-size: 70px; line-height: 1;
      letter-spacing: -0.025em; color: #FFFFFF; white-space: nowrap; }
"""
    body = f"""    <div id="i4-bg"></div>
    <div id="i4-stage">
      <div id="i4-rw"><video id="i4-vr" class="clip" src="assets/video/libro-ins04.mp4" muted playsinline data-start="0" data-duration="«RD»" data-track-index="2"></video></div>
      <div id="i4-vw"><video id="i4-v" class="clip" src="assets/video/libro-ins04.mp4" muted playsinline data-start="0" data-duration="«D»" data-track-index="1"></video></div>
    </div>
    <div id="i4-lab">Ebook</div>
    <div id="i4-tit">Holandés sin miedo</div>"""
    js = """
      // a slow drift while the pages turn, then the push into «¡Hora de practicar!» on «ejercicios prácticos»
      tl.fromTo(q("stage"), { scale: 1.0 }, { scale: 1.035, duration: «EJE» - 0.1, ease: "none" }, 0);
      tl.fromTo(q("stage"), { scale: 1.035 }, { scale: 1.2, duration: «D» - «EJE» + 0.1, ease: "power2.inOut", immediateRender: false }, «EJE» - 0.1);
      tl.fromTo(q("lab"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, 0.1);
      tl.fromTo(q("tit"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 0.16);
      tl.to([q("lab"), q("tit")], { opacity: 0, y: -14, duration: 0.3, ease: "power2.in" }, «EJE» - 0.12);
"""
    return comp(iid, d, P, css, body, js, c), []
