"""ins-02 · «En la pausa del trabajo, alguien dice algo, todos se ríen y tú sonríes sin saber de qué.» — v2 (the client:
«un vídeo stock de una mesa, gente hablando como en el descanso del trabajo, riéndose»): real footage instead of a
drawing, two free Mixkit clips (Mixkit Stock Video Free License), each laid out vertically as a full-width band over a
blurred, darker copy of itself (assets/video/stock-*.mp4, tools/fetch_assets.sh):
  · from the cut to «todos»: coworkers at their lunch table, chatting («Having a working lunch in the office», 24893);
    on «dice algo» a white bubble with what someone says, in quick idiomatic Dutch: «En toen stond hij met z'n mond
    vol tanden!»;
  · from «todos se ríen»: colleagues laughing around a table («Work colleagues having happy discussion around a
    table», 48479); on «tú sonríes» a white pill with an awkward smile, «¿De qué se ríen?».
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

A_FROM, B_FROM = 9.0, 0.3        # where each clip is played from (source s)
AWK = ('<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="«BLUE»"/><circle cx="17" cy="20" r="3" fill="#FFFFFF"/>'
       '<circle cx="31" cy="20" r="3" fill="#FFFFFF"/><path d="M15 31 Q24 35 33 29" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round"/></svg>')


def build():
    iid, P = "ins-02", "i2"; d = INS[iid]["duration"]
    c = dict(DICE=cue(iid, "dice"), TODOS=cue(iid, "todos"), TU=cue(iid, "tu"), SIN=cue(iid, "sin"))
    cut = round(c["TODOS"] - 0.06, 3)
    c.update(CUT=cut, DB=round(d - cut, 3), AF=A_FROM, BF=B_FROM)
    css = """
    .i2-v { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }
    #i2-say { left: 90px; top: 250px; font-size: 44px; transform-origin: 0% 100%; }
    #i2-awk { position: absolute; right: 80px; top: 1060px; display: flex; align-items: center; gap: 14px; height: 84px; padding: 0 34px 0 18px;
      border-radius: 999px; background: #FFFFFF; font-family: "Poppins", sans-serif; font-weight: 700; font-size: 36px; color: «INDIGO»;
      transform-origin: 100% 50%; }
    #i2-awk svg { display: block; width: 54px; height: 54px; }
"""
    body = f"""    <video id="i2-a" class="clip i2-v" src="assets/video/stock-lunch.mp4" muted playsinline data-start="0" data-duration="«CUT»" data-media-start="«AF»" data-track-index="1"></video>
    <video id="i2-b" class="clip i2-v" src="assets/video/stock-laugh.mp4" muted playsinline data-start="«CUT»" data-duration="«DB»" data-media-start="«BF»" data-track-index="2"></video>
    <div id="i2-say" class="i2-bub i2-bub-w i2-bl">En toen stond hij met z'n<br/>mond vol tanden!</div>
    <div id="i2-awk">{sub(AWK, {})}<span>¿De qué se ríen?</span></div>"""
    js = """
      tl.fromTo(q("say"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «DICE» - 0.08);
      tl.to(q("say"), { opacity: 0, y: -10, duration: 0.2, ease: "power2.in" }, «CUT» + 0.9);
      tl.fromTo(q("awk"), { opacity: 0, scale: 0.7, x: 20 }, { opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "back.out(1.7)" }, «TU» - 0.04);
"""
    sfx = [(c["DICE"] - 0.08, "pop", 0.12), (c["TU"] - 0.04, "pop", 0.14)]
    return comp(iid, d, P, css, body, js, c), sfx
