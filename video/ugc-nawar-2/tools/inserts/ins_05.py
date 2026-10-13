"""ins-05 · «(Aprendes con lecciones grabadas) por un equipo de expertos nativos que dominan tu idioma» — the recorded
lesson (paul-clase-2, the VSL's «vídeos del curso»; the live class at ins-07 uses the other video) in a browser
window, then the camera dives into Paul's webcam: a card grows out of the player on the same frame (same video,
same instant) to a big portrait with «Profesores nativos holandeses» and «Expertos en español».
The reverse of UGC #1 ins-03, because here she says «lecciones grabadas» first."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def build():
    iid, P = "ins-05", "i5"; d = INS[iid]["duration"]
    c = dict(EXP=cue(iid, "expertos"), NAT=cue(iid, "nativos"), DOM=cue(iid, "dominan"))
    c["FLIP"] = round(max(0.7, c["EXP"] - 0.32), 3)
    M0 = 1.0                                                   # media time at local 0 (both copies stay in sync)
    WX0, WY0, WX1, WY1 = 354, 94, 736, 304                     # webcam inside paul-clase-2 (2424×1238), past its corners
    CW = 800; k = CW / (WX1 - WX0); CH = round((WY1 - WY0) * k, 1)
    CL, CT = 140, 360
    WL, WT = 60, 296
    kc = 540 / 1238; ox = -(2424 * kc - 960) / 2
    tx = WL + WX0 * kc + ox; ty = WT + 60 + WY0 * kc; s0 = (WX1 - WX0) * kc / CW
    c.update(CH=CH, VW=round(2424 * k, 1), VH=round(1238 * k, 1), VL=round(-WX0 * k, 1), VT=round(-WY0 * k, 1),
             CL=CL, CT=CT, FX=round(tx - CL, 2), FY=round(ty - CT, 2), FS=round(s0, 4), M0=M0,
             LAND=round(c["FLIP"] + 0.6, 3), VD=round(d + 0.1, 3))
    c.update(CST=round(c["FLIP"] - 0.1, 3), CMS=round(M0 + c["FLIP"] - 0.1, 3), CVD=round(d - c["FLIP"] + 0.2, 3))   # the card copy only lives from the dive on
    css = WIN_CSS + """
    #i5-card { left: «CL»px; top: «CT»px; width: 800px; height: «CH»px; overflow: hidden; border-radius: 36px; background: #0C0C1E; transform-origin: 0% 0%; }
    #i5-cv { position: absolute; left: «VL»px; top: «VT»px; width: «VW»px; height: «VH»px; }
    #i5-cgrad { position: absolute; left: 0; bottom: 0; width: 800px; height: 200px; background: linear-gradient(180deg, rgba(4,0,40,0) 0%, rgba(4,0,40,0.6) 100%); }
    #i5-cedge { position: absolute; inset: 0; border-radius: 36px; box-shadow: inset 0 0 0 2px rgba(255,255,255,0.22); }
    #i5-name { position: absolute; left: 40px; bottom: 84px; font-weight: 700; font-size: 42px; line-height: 1; color: #FFFFFF; white-space: nowrap; }
    #i5-role { position: absolute; left: 42px; bottom: 44px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 26px; line-height: 1; color: rgba(255,255,255,0.8); white-space: nowrap; }
    #i5-p1row { top: 852px; }
    #i5-p2row { top: 940px; }
    #i5-lrow { top: 208px; }
"""
    body = "\n".join([ground(P, "blue"), f"""    <div id="i5-s1" class="i5-full">
      <div id="i5-lrow" class="i5-row"><div id="i5-lp" class="i5-pill">{icon('play')}<span>Lecciones grabadas</span></div></div>
      """ + win(P, "win", 960, WL, WT, '<video id="i5-lv" class="clip i5-media" src="assets/video/paul-clase-2.mp4" muted playsinline data-start="0" data-duration="«VD»" data-media-start="«M0»" data-track-index="2" data-hf-media-start-basis="local"></video>') + f"""
    </div>
    <div id="i5-s2" class="i5-full">
      <div id="i5-card" class="i5-card i5-on-blue">
        <video id="i5-cv" class="clip" src="assets/video/paul-clase-2.mp4" muted playsinline data-start="«CST»" data-duration="«CVD»" data-media-start="«CMS»" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video>
        <div id="i5-cgrad"></div><div id="i5-cedge"></div>
        <div id="i5-name">Paul</div><div id="i5-role">Profesor de Nawar</div>
      </div>
      <div id="i5-p1row" class="i5-row"><div id="i5-p1" class="i5-wpill"><span class="i5-flag i5-flagd">{FLAG_NL}</span><span>Profesores nativos holandeses</span></div></div>
      <div id="i5-p2row" class="i5-row"><div id="i5-p2" class="i5-wpill"><span class="i5-flag i5-flagd">{FLAG_ES}</span><span>Expertos en español</span></div></div>
    </div>"""])
    js = """
      tl.fromTo(q("lp"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.02);
      tl.fromTo(q("win"), { opacity: 0, y: 110, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out" }, 0);
      // the dive: a card appears exactly over the player's webcam and grows to the portrait (same frame)
      tl.fromTo(q("card"), { opacity: 0, x: «FX», y: «FY», scale: «FS» }, { opacity: 1, duration: 0.04, ease: "none" }, «FLIP»);
      tl.to(q("card"), { x: 0, y: 0, scale: 1, duration: 0.6, ease: "power3.inOut" }, «FLIP» + 0.04);
      tl.to(q("s1"), { opacity: 0, duration: 0.36, ease: "power2.in" }, «FLIP» + 0.18);
      tl.fromTo([q("cgrad"), q("name"), q("role")], { opacity: 0 }, { opacity: 1, duration: 0.24, ease: "power2.out" }, «LAND»);
      tl.fromTo(q("p1"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, Math.max(«NAT» - 0.04, «LAND»));
      tl.fromTo(q("p2"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «DOM» - 0.04);
"""
    sfx = [(c["FLIP"], "whoosh-short", 0.14), (c["NAT"] - 0.04, "click-soft", 0.24), (c["DOM"] - 0.04, "click-soft", 0.24)]
    return comp(iid, d, P, css, body, js, c), sfx
