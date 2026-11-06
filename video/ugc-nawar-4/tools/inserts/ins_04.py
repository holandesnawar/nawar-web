"""ins-04 · «(Si empiezas ya,) en Navidad vas a entender cosas que antes se te escapaban.» — v3 (the client: v2 «está
igual el tema de Navidad… otro vídeo de Navidad en la mesa, hablando gente, siempre adaptado a 9:16»): real footage,
friends at a Christmas dinner («Couple of friends chatting during Christmas dinner», Mixkit 42157, cropped to 9:16 from
4K, tools/fetch_assets.sh). Over it, what someone says at the table, in Dutch — «Fijne feestdagen! Ga je met kerst naar
je familie?» — blurred at first (it still escapes you) and sharp on «entender», when its Spanish line slides out under
it («¡Felices fiestas! ¿Vas a ver a tu familia en Navidad?»); on «escapaban» a green «✓ Ya lo entiendes».
Dutch checked with the Dutch content checker (natural; «met kerst» is how natives say it)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(ENT=cue(iid, "entender"), ESC=cue(iid, "escapaban"))
    css = """
    #i4-v { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }
    #i4-nl { left: 90px; top: 230px; font-size: 48px; transform-origin: 0% 100%; }
    #i4-es { left: 90px; top: 470px; max-width: 900px; padding: 22px 30px; border-radius: 28px; background: «BLUE»; color: #FFFFFF;
      display: flex; align-items: flex-start; gap: 18px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 40px; line-height: 1.22; }
    #i4-es .i4-flag { margin-top: 8px; width: 46px; height: 31px; flex: 0 0 46px; }
    #i4-es .i4-flag svg { width: 46px; height: 31px; }
    #i4-okrow { top: 1130px; }
    #i4-ok { gap: 14px; height: 92px; padding: 0 40px 0 24px; font-size: 42px; background: «GREEN»; color: #FFFFFF; }
    #i4-ok svg { display: block; width: 48px; height: 48px; }
"""
    body = f"""    <video id="i4-v" class="clip" src="assets/video/stock-xmas.mp4" muted playsinline data-start="0" data-duration="«D»" data-track-index="1"></video>
    <div id="i4-nl" class="i4-bub i4-bub-w i4-bl">Fijne feestdagen! Ga je met<br/>kerst naar je familie?</div>
    <div id="i4-es" class="i4-card"><span class="i4-flag">{FLAG_ES}</span><span>¡Felices fiestas! ¿Vas a ver a tu<br/>familia en Navidad?</span></div>
    <div id="i4-okrow" class="i4-row"><div id="i4-ok" class="i4-wpill">{icon('checkw')}<span>Ya lo entiendes</span></div></div>"""
    js = """
      tl.fromTo(q("nl"), { opacity: 0, scale: 0.85, filter: "blur(9px)" }, { opacity: 0.9, scale: 1, filter: "blur(9px)", duration: 0.3, ease: "back.out(1.5)" }, 0.05);
      tl.to(q("nl"), { opacity: 1, filter: "blur(0px)", duration: 0.26, ease: "power2.out" }, «ENT» - 0.06);
      tl.set(q("nl"), { filter: "none" }, «ENT» + 0.22);
      tl.fromTo(q("es"), { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «ENT» + 0.12);
      tl.fromTo(q("ok"), { opacity: 0, y: 24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «ESC» - 0.06);
"""
    sfx = [(0.05, "pop", 0.1), (c["ENT"] - 0.06, "sparkle", 0.1), (c["ESC"] - 0.06, "chime", 0.14)]
    return comp(iid, d, P, css, body, js, c), sfx
