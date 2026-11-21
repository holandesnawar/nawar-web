"""ins-05 · «(Aprendes con lecciones grabadas) por un equipo de expertos nativos que dominan tu idioma» — a real
recorded lesson (v2: the client's new teacher video, «Errores comunes»: the teacher's webcam beside the slide, wrong →
right sentences) big in a browser window, so the lesson itself is the picture. On «expertos» the camera pushes in
towards the teacher (gently, 1.1×: the slide's right column, the corrected sentences, stays in view) and a ring lands on his webcam; «Profesores nativos holandeses» and «Expertos en español» pop under the
window on «nativos» and «dominan». The live class at ins-07 uses another video (paul-clase-1)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def build():
    iid, P = "ins-05", "i5"; d = INS[iid]["duration"]
    c = dict(EXP=cue(iid, "expertos"), NAT=cue(iid, "nativos"), DOM=cue(iid, "dominan"))
    # the window: 1000 wide → content 1000×562.5; the lesson (assets/video/profe-leccion.mp4, the slide cropped out of
    # the recording, 1736×964) covers it at k = 562.5/964, centred (≈6 px trimmed each side)
    SW, WL, WT = 1000, 40, 300
    CW, CH = 1000, 562.5
    k = CH / 964; ox = -(1736 * k - CW) / 2
    CX0, CY0, CX1, CY1 = 93, 82, 417, 286                    # the teacher's webcam in the clip
    wx, wy, ww, wh = CX0 * k + ox, CY0 * k, (CX1 - CX0) * k, (CY1 - CY0) * k
    ZOOM = 1.1                                                # the corrections column (right edge of the slide) stays in frame
    c.update(M0=5.0, VD=round(d + 0.1, 3), OX=round(wx, 2), OY=round(wy, 2),
             RL=round(wx - 5, 2), RT=round(wy - 5, 2), RW=round(ww + 10, 2), RH=round(wh + 10, 2), Z=ZOOM,
             PUSH=round(max(0.5, c["EXP"] - 0.1), 3))
    c["LAND"] = round(c["PUSH"] + 0.8, 3)
    css = WIN_CSS + """
    #i5-lrow { top: 208px; }
    #i5-lz { position: absolute; left: 0; top: 0; width: 1000px; height: 562.5px; transform-origin: «OX»px «OY»px; }
    #i5-ring { position: absolute; left: «RL»px; top: «RT»px; width: «RW»px; height: «RH»px; border-radius: 14px;
      box-shadow: 0 0 0 3px #FFFFFF, 0 0 0 9px rgba(77,163,255,0.35); transform-origin: 50% 50%; }
    #i5-p1row { top: 975px; }
    #i5-p2row { top: 1063px; }
"""
    body = "\n".join([ground(P, "blue"), f"""    <div id="i5-lrow" class="i5-row"><div id="i5-lp" class="i5-pill">{icon('play')}<span>Lecciones grabadas</span></div></div>
    """ + win(P, "win", SW, WL, WT, '<div id="i5-lz"><video id="i5-lv" class="clip i5-media" src="assets/video/profe-leccion.mp4" muted playsinline data-start="0" data-duration="«VD»" data-media-start="«M0»" data-track-index="1" data-hf-media-start-basis="local"></video><div id="i5-ring"></div></div>') + f"""
    <div id="i5-p1row" class="i5-row"><div id="i5-p1" class="i5-wpill"><span class="i5-flag i5-flagd">{FLAG_NL}</span><span>Profesores nativos holandeses</span></div></div>
    <div id="i5-p2row" class="i5-row"><div id="i5-p2" class="i5-wpill"><span class="i5-flag i5-flagd">{FLAG_ES}</span><span>Expertos en español</span></div></div>"""])
    js = """
      tl.fromTo(q("lp"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("win"), { opacity: 0, y: 110, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out" }, 0);
      // the lesson drifts, then the camera pushes in towards the teacher on «expertos» (origin = his webcam)
      tl.fromTo(q("lz"), { scale: 1 }, { scale: 1.03, duration: «PUSH» - 0.004, ease: "none" }, 0);
      tl.fromTo(q("lz"), { scale: 1.03 }, { scale: «Z», duration: 0.8, ease: "power2.inOut", immediateRender: false }, «PUSH»);
      tl.fromTo(q("lz"), { scale: «Z» }, { scale: «Z» + 0.03, duration: «D» - «LAND», ease: "none", immediateRender: false }, «LAND» + 0.004);
      tl.fromTo(q("ring"), { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, «PUSH» + 0.35);
      tl.fromTo(q("p1"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «NAT» - 0.04);
      tl.fromTo(q("p2"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «DOM» - 0.04);
"""
    sfx = [(c["PUSH"], "whoosh-short", 0.12), (c["NAT"] - 0.04, "click-soft", 0.24), (c["DOM"] - 0.04, "click-soft", 0.24)]
    return comp(iid, d, P, css, body, js, c), sfx
