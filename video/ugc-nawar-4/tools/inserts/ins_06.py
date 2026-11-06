"""ins-06 · «Quien lo consiga entra en nuestra lista prioritaria y sabrá lo que estaremos preparando para este Black Friday
antes que nadie.» — v2 (the client: «te dejé un vídeo de cómo es la web… scrolleando, para que se vea todo bien»): the
real page on a phone, on paper — the client's screen recording («Grabación de pantalla 2026-11-06…», Drive «BF 2»:
«Únete a la lista prioritaria del Black Friday», the form, «Acceso anticipado», the book for 1 €), its scroll (source
0–SRC_END s) played a little faster so it ends with the insert; on «antes que nadie» a green «✓ Lo ves antes que nadie»
pill lands over the phone's lower edge (that caption isn't shown twice)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

SRC_END = 9.0                     # the recording scrolls to the end of the page by here, then stays still
VW, VH = 462, 1000                # assets/video/web.mp4 (the 394×852 recording, lanczos ×1.17)


def build():
    iid, P = "ins-06", "i6"; d = INS[iid]["duration"]
    c = dict(ANT=cue(iid, "antes"), RATE=round(SRC_END / (d - 0.2), 3))
    css = PHONE_CSS + """
    #i6-web { position: absolute; left: 0; top: 0; width: «VW»px; height: «VH»px; display: block; }
    #i6-okrow { top: 1150px; }
    #i6-ok { gap: 14px; height: 92px; padding: 0 40px 0 26px; font-size: 40px; background: «GREEN»; color: #FFFFFF; }
    #i6-ok svg { display: block; width: 48px; height: 48px; }
"""
    pw, ph = VW + 32, VH + 32
    screen = f'<video id="i6-web" class="clip" src="assets/video/web.mp4" muted playsinline data-start="0" data-duration="«D»" data-playback-rate="«RATE»" data-track-index="1"></video>'
    body = "\n".join([ground(P, "paper"), "    " + phone(P, "phone", (1080 - pw) // 2, 150, pw, ph, screen, time=None),
                      f'    <div id="i6-okrow" class="i6-row"><div id="i6-ok" class="i6-wpill">{icon("checkw")}<span>Lo ves antes que nadie</span></div></div>'])
    js = """
      tl.fromTo(q("phone"), { opacity: 0.4, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      tl.fromTo(q("ok"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «ANT» - 0.04);
"""
    sfx = [(c["ANT"] - 0.04, "chime", 0.14)]
    return comp(iid, d, P, css, body, js, dict(c, VW=VW, VH=VH)), sfx
