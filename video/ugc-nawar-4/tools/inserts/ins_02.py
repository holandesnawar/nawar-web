"""ins-02 · «En la pausa del trabajo, alguien dice algo, todos se ríen y tú sonríes sin saber de qué.» — real footage, one
free Mixkit clip (Mixkit Stock Video Free License) full frame in 9:16, cropped from 4K («People having a work meeting
around a table», 4547, tools/fetch_assets.sh): colleagues at the office table, one of them laughing, the high-five
landing around «todos se ríen» (v5, the client: the same group the whole time, not a cut to someone else; no Dutch
line written on screen). On «tú sonríes» a white pill with an awkward smile, «¿De qué se ríen?».
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

A_FROM, B_FROM = 0.0, 0.0        # (v3: the clips are cut and cropped to 9:16 in tools/fetch_assets.sh)
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
    body = f"""    <video id="i2-a" class="clip i2-v" src="assets/video/stock-table.mp4" muted playsinline data-start="0" data-duration="«D»" data-track-index="1"></video>
    <div class="i2-scr" style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 52%, rgba(6,4,30,0.62) 68%, rgba(6,4,30,0.62) 76%, rgba(0,0,0,0) 90%);"></div>
    <div id="i2-awk">{sub(AWK, {})}<span>¿De qué se ríen?</span></div>"""
    js = """
      tl.fromTo(q("awk"), { opacity: 0, scale: 0.7, x: 20 }, { opacity: 1, scale: 1, x: 0, duration: 0.3, ease: "back.out(1.7)" }, «TU» - 0.04);
"""
    sfx = [(c["TU"] - 0.04, "pop", 0.14)]
    return comp(iid, d, P, css, body, js, c), sfx
