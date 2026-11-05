"""ins-01 · «Porque cada mes que esperas es otro mes pidiendo que te traduzcan.» — on paper, like your own chat over the
months: the headline «Mes tras mes, / pidiendo ayuda» (the second line in an indigo chip), then one blue bubble of yours
per month, each with its month tag on the left — SEP «¿Me traduces esta carta?», OCT «¿Puedes llamar tú al casero?»,
NOV «¿Me acompañas a la gemeente?» — and on «otro mes» one more, DIC «¿Me traduces esto también?», with a small red «+1».
Same family as the Black Friday ad's ins-01 and UGC #2 (paper, white/blue bubbles, indigo type; red only for what goes
wrong)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

ROWS = [("SEP", "¿Me traduces esta carta?"), ("OCT", "¿Puedes llamar tú al casero?"),
        ("NOV", "¿Me acompañas a la gemeente?"), ("DIC", "¿Me traduces esto también?")]
TOP0, STEP = 470, 158


def build():
    iid, P = "ins-01", "i1"; d = INS[iid]["duration"]
    c = dict(CADA=cue(iid, "cada"), MES=cue(iid, "mes"), ESP=cue(iid, "esperas"), OTRO=cue(iid, "otro"),
             TRA=cue(iid, "traduzcan"))
    css = """
    #i1-h { top: 168px; color: «INDIGO»; font-size: 80px; line-height: 1.05; }
    #i1-h1 { margin-top: 16px; line-height: 1; }
    #i1-chip { background: «INDIGO»; color: #FFFFFF; font-size: 62px; padding: 6px 26px 12px; border-radius: 16px; letter-spacing: -0.01em; }
    .i1-r { position: absolute; left: 100px; width: 880px; height: 120px; }
    .i1-m { position: absolute; left: 0; top: 26px; width: 120px; height: 68px; border-radius: 18px; background: #FFFFFF;
      box-shadow: inset 0 0 0 2px «LINE»; display: flex; align-items: center; justify-content: center;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; letter-spacing: 0.14em; color: «MUTED»; }
    .i1-r .i1-bub { right: 0; top: 0; transform-origin: 100% 100%; }
    .i1-plus { position: absolute; right: -18px; top: -22px; height: 52px; padding: 0 16px; border-radius: 999px; background: «RED»;
      color: #FFFFFF; display: flex; align-items: center; font-family: "Inter", sans-serif; font-weight: 800; font-size: 28px; }
    #i1-m3 { background: «INDIGO»; color: #FFFFFF; box-shadow: none; }
"""
    rows = "\n".join(f"""    <div id="i1-r{k}" class="i1-r" style="top: {TOP0 + k * STEP}px;"><div id="i1-m{k}" class="i1-m">{m}</div>
      <div id="i1-b{k}" class="i1-bub i1-bub-b i1-br">{t}{'<div id="i1-plus" class="i1-plus">+1</div>' if k == 3 else ''}</div></div>"""
                     for k, (m, t) in enumerate(ROWS))
    body = "\n".join([ground(P, "paper"), f"""    <div id="i1-h" class="i1-h1"><div id="i1-h0" class="i1-w">Mes tras mes,</div><div id="i1-h1"><span id="i1-chip" class="i1-chip">pidiendo ayuda</span></div></div>
{rows}"""])
    starts = [0.0, round(c["MES"] - 0.04, 3), round(c["ESP"] + 0.16, 3), round(c["OTRO"] - 0.06, 3)]
    js = """
      tl.fromTo(q("h0"), { opacity: 0.3, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      tl.fromTo(q("chip"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, 0.16);
      tl.set(q("plus"), { opacity: 0 }, 0);
"""
    for k, t in enumerate(starts):
        frm = "{ opacity: 0.35, y: 26 }" if k == 0 else "{ opacity: 0, y: 26 }"
        js += f'      tl.fromTo(q("r{k}"), {frm}, {{ opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }}, {t});\n'
        js += f'      tl.fromTo(q("b{k}"), {{ scale: 0.82 }}, {{ scale: 1, duration: 0.3, ease: "back.out(1.6)" }}, {t});\n'
    js += """      tl.fromTo(q("plus"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.26, ease: "back.out(2.2)", immediateRender: false }, «OTRO» + 0.22);
      tl.to(q("r3"), { keyframes: [{ x: -8, duration: 0.05 }, { x: 7, duration: 0.06 }, { x: -4, duration: 0.06 }, { x: 0, duration: 0.06 }] }, «TRA» - 0.04);
"""
    sfx = [(starts[1], "pop", 0.12), (starts[2], "pop", 0.12), (starts[3], "pop", 0.16), (c["OTRO"] + 0.22, "notification", 0.14)]
    return comp(iid, d, P, css, body, js, c), sfx
