"""ins-04 · «(Si empiezas ya,) en Navidad vas a entender cosas que antes se te escapaban.» — on paper: on top, the way from
today to Christmas — «HOY» (noviembre) on the left, «NAVIDAD» (a tree) on the right — and a blue bar that fills between
them as she says «en Navidad»; under it, Sanne's white bubble in Dutch, «Fijne feestdagen! Ga je met kerst naar je
familie?», blurred at first (it still escapes you) and sharp on «entender», when its Spanish line slides out under it
(«¡Felices fiestas! ¿Vas a ver a tu familia en Navidad?», ES flag); on «escapaban» a green «✓ Ya lo entiendes» lands.
Dutch checked with the Dutch content checker (natural, «met kerst» is how natives say it)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

TREE = ('<svg viewBox="0 0 48 48"><path d="M24 4 L34 18 H29 L37 29 H31 L40 40 H8 L17 29 H11 L19 18 H14 Z" fill="#FFFFFF"/>'
        '<rect x="21" y="40" width="6" height="6" rx="1.5" fill="#FFFFFF"/></svg>')
FACE_S = ('<svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="48" fill="#15A3A3"/><circle cx="35" cy="40" r="5" fill="#FFFFFF"/>'
          '<circle cx="61" cy="40" r="5" fill="#FFFFFF"/><path d="M32 58 Q48 72 64 58" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/></svg>')


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(NAV=cue(iid, "navidad"), ENT=cue(iid, "entender"), COS=cue(iid, "cosas"), ESC=cue(iid, "escapaban"))
    css = """
    #i4-way { left: 90px; top: 180px; width: 900px; height: 230px; }
    .i4-end { position: absolute; top: 32px; width: 150px; text-align: center; }
    .i4-dot { width: 100px; height: 100px; margin: 0 auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .i4-dot svg { display: block; width: 60px; height: 60px; }
    .i4-lb { margin-top: 14px; font-family: "Inter", sans-serif; font-weight: 800; font-size: 30px; letter-spacing: 0.12em; color: «INDIGO»; }
    .i4-sm { margin-top: 6px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 26px; color: «MUTED»; }
    #i4-e0 { left: 20px; } #i4-e1 { right: 20px; }
    #i4-d0 { background: «INDIGO»; } #i4-d1 { background: «GREEN»; }
    #i4-d0 i { display: block; width: 30px; height: 30px; border-radius: 50%; background: #FFFFFF; }
    #i4-track { position: absolute; left: 190px; top: 74px; width: 520px; height: 18px; border-radius: 9px; background: «LINE»; overflow: hidden; }
    #i4-fill { position: absolute; left: 0; top: 0; width: 520px; height: 18px; border-radius: 9px; background: «BLUE»; transform-origin: 0% 50%; }
    #i4-av { left: 90px; top: 540px; width: 130px; height: 130px; }
    #i4-av svg { width: 130px; height: 130px; }
    #i4-nl { left: 250px; top: 480px; font-size: 52px; transform-origin: 0% 100%; }
    #i4-nl b { font-weight: 700; color: «INDIGO»; }
    #i4-es { left: 250px; top: 780px; width: 740px; height: 190px; border-radius: 30px; background: «BLUE»; color: #FFFFFF; }
    #i4-esf { position: absolute; left: 30px; top: 34px; width: 48px; height: 32px; flex: none; }
    #i4-esf svg { width: 48px; height: 32px; }
    #i4-est { position: absolute; left: 100px; top: 26px; width: 610px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 42px;
      line-height: 1.22; }
    #i4-okrow { top: 1050px; }
    #i4-ok { gap: 14px; height: 96px; padding: 0 42px 0 26px; font-size: 44px; background: «GREEN»; color: #FFFFFF; }
    #i4-ok svg { display: block; width: 50px; height: 50px; }
"""
    body = "\n".join([ground(P, "paper"), f"""    <div id="i4-way" class="i4-card i4-on-paper">
      <div id="i4-e0" class="i4-end"><div id="i4-d0" class="i4-dot"><i></i></div><div class="i4-lb">HOY</div><div class="i4-sm">noviembre</div></div>
      <div id="i4-track"><div id="i4-fill"></div></div>
      <div id="i4-e1" class="i4-end"><div id="i4-d1" class="i4-dot">{TREE}</div><div class="i4-lb">NAVIDAD</div><div class="i4-sm">diciembre</div></div>
    </div>
    <div id="i4-av" class="i4-av">{FACE_S}</div>
    <div id="i4-nl" class="i4-bub i4-bub-w i4-bl"><b>Sanne</b><br/>Fijne feestdagen! Ga je met<br/>kerst naar je familie?</div>
    <div id="i4-es" class="i4-card"><div id="i4-esf" class="i4-flag">{FLAG_ES}</div><div id="i4-est">¡Felices fiestas! ¿Vas a ver a tu familia en Navidad?</div></div>
    <div id="i4-okrow" class="i4-row"><div id="i4-ok" class="i4-wpill">{icon('checkw')}<span>Ya lo entiendes</span></div></div>"""])
    js = """
      tl.fromTo(q("way"), { opacity: 0.4, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      tl.fromTo(q("fill"), { scaleX: 0.04 }, { scaleX: 1, duration: «ENT» - 0.05, ease: "power2.inOut" }, 0.05);
      tl.fromTo(q("d1"), { scale: 1 }, { keyframes: [{ scale: 1.25, duration: 0.12 }, { scale: 1, duration: 0.18, ease: "back.out(2)" }], immediateRender: false }, «ENT»);
      tl.fromTo(q("av"), { opacity: 0.4, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("nl"), { opacity: 0.5, filter: "blur(9px)" }, { opacity: 0.85, filter: "blur(9px)", duration: 0.3, ease: "power2.out" }, 0);
      tl.to(q("nl"), { opacity: 1, filter: "blur(0px)", duration: 0.26, ease: "power2.out" }, «ENT» - 0.06);
      tl.set(q("nl"), { filter: "none" }, «ENT» + 0.22);
      tl.fromTo(q("es"), { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }, «ENT» + 0.12);
      tl.fromTo(q("ok"), { opacity: 0, y: 24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «ESC» - 0.06);
"""
    sfx = [(c["ENT"] - 0.06, "sparkle", 0.12), (c["ENT"] + 0.12, "whoosh-short", 0.08), (c["ESC"] - 0.06, "chime", 0.14)]
    return comp(iid, d, P, css, body, js, c), sfx
