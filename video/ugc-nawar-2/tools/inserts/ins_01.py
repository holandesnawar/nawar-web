"""ins-01 · «(En cuatro semanas) ya puedes presentarte, hacer compras y pedir lo que necesitas sin ayuda.» — the
«Semana 4» pill, then a calm checklist of three everyday situations, each with what you'd actually say in Dutch
(white speech bubble under the label); every row lands on its word and its tick pops a beat later. On «sin ayuda»
a green «Sin ayuda» pill closes the list. Same family as UGC #1 ins-06 (Semana 16 · Cita confirmada) and the VSL's
«AL TERMINAR» checklist."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


ROWS = [("Presentarte", "Goedemiddag, ik heet Ana."),
        ("Hacer compras", "Mag ik een tasje, alsjeblieft?"),
        ("Pedir lo que necesitas", "Sorry, mag ik iets vragen?")]


def build():
    iid, P = "ins-01", "i1"; d = INS[iid]["duration"]
    c = dict(PRE=cue(iid, "presentarte"), HAC=cue(iid, "hacer"), PED=cue(iid, "pedir"), SIN=cue(iid, "sin"), AYU=cue(iid, "ayuda"))
    css = """
    #i1-wrow { top: 218px; }
    #i1-list { position: absolute; left: 0; top: 368px; width: 1080px; display: flex; justify-content: center; }
    #i1-col { display: flex; flex-direction: column; gap: 58px; }
    .i1-it { display: grid; grid-template-columns: 66px auto; column-gap: 26px; row-gap: 18px; align-items: center; }
    .i1-tick { position: relative; width: 66px; height: 66px; grid-row: 1; grid-column: 1; }
    .i1-ring { position: absolute; left: 0; top: 0; width: 66px; height: 66px; border-radius: 50%; box-sizing: border-box;
      border: 4px solid rgba(255,255,255,0.34); }
    .i1-ok { position: absolute; left: 0; top: 0; width: 66px; height: 66px; }
    .i1-ok svg { display: block; width: 66px; height: 66px; filter: drop-shadow(0 6px 14px rgba(4,0,40,0.30)); }
    .i1-lab { grid-row: 1; grid-column: 2; font-weight: 700; font-size: 48px; line-height: 60px; letter-spacing: -0.015em; color: #FFFFFF; white-space: nowrap; }
    .i1-say { grid-row: 2; grid-column: 2; justify-self: start; padding: 22px 32px; border-radius: 30px; border-top-left-radius: 10px; white-space: nowrap;
      background: #FFFFFF; color: «INK»; box-shadow: 0 22px 46px rgba(4,0,40,0.32), 0 4px 10px rgba(4,0,40,0.16); transform-origin: 0% 0%;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 37px; line-height: 1.22; letter-spacing: -0.01em; }
    #i1-okrow { top: 1084px; }
    #i1-done { display: flex; align-items: center; gap: 14px; height: 72px; padding: 0 32px 0 18px; border-radius: 999px; background: «GREEN»; color: #FFFFFF;
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 31px; line-height: 1; white-space: nowrap; box-shadow: 0 16px 40px rgba(4,0,40,0.32); }
    #i1-done svg { display: block; width: 40px; height: 40px; }
"""
    rows = "\n".join(f"""        <div id="i1-r{k}" class="i1-it">
          <div class="i1-tick"><div id="i1-g{k}" class="i1-ring"></div><div id="i1-k{k}" class="i1-ok">{icon('check')}</div></div>
          <div id="i1-l{k}" class="i1-lab">{lab}</div>
          <div id="i1-b{k}" class="i1-say">{nl}</div>
        </div>""" for k, (lab, nl) in enumerate(ROWS))
    body = "\n".join([ground(P, "blue"), f"""    <div id="i1-wrow" class="i1-row"><div id="i1-wk" class="i1-wpill"><span class="i1-flag i1-flagd">{FLAG_NL}</span><span>Semana 4</span></div></div>
    <div id="i1-list">
      <div id="i1-col">
{rows}
      </div>
    </div>
    <div id="i1-okrow" class="i1-row"><div id="i1-done">{icon('checkw')}<span>Sin ayuda</span></div></div>"""])
    js = """
      tl.fromTo(q("wk"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      // the list starts centred in the content zone and steps up as rows arrive (ends where it is laid out)
      tl.fromTo(q("list"), { y: 170 }, { y: 170, duration: 0.01 }, 0);
      tl.to(q("list"), { y: 85, duration: 0.4, ease: "power3.inOut" }, «HAC» - 0.2);
      tl.to(q("list"), { y: 0, duration: 0.4, ease: "power3.inOut" }, «PED» - 0.2);
"""
    for k, key in enumerate(("PRE", "HAC", "PED")):
        js += f"""
      tl.fromTo(q("g{k}"), {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.28, ease: "back.out(1.8)" }}, «{key}» - 0.08);
      tl.fromTo(q("l{k}"), {{ opacity: 0, x: -26 }}, {{ opacity: 1, x: 0, duration: 0.34, ease: "power3.out" }}, «{key}» - 0.08);
      tl.fromTo(q("b{k}"), {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }}, «{key}» + 0.02);
      tl.fromTo(q("k{k}"), {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, «{key}» + 0.25);
      tl.to(q("g{k}"), {{ opacity: 0, duration: 0.14, ease: "power2.out" }}, «{key}» + 0.27);
"""
    js += """
      tl.fromTo(q("done"), { opacity: 0, scale: 0.6, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SIN» - 0.06);
"""
    sfx = [(c["PRE"] - 0.06, "pop", 0.18), (c["HAC"] - 0.06, "pop", 0.18), (c["PED"] - 0.06, "pop", 0.18), (c["SIN"] - 0.04, "chime", 0.22)]
    return comp(iid, d, P, css, body, js, c), sfx
