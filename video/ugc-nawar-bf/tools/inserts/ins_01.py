"""ins-01 · «(Antes de pedir cita,) miras quién puede ir contigo, y si ese día no puede nadie, la cambias.» — on paper,
like a phone chat: the «Pedir cita» label, the appointment card (Huisarts, 14 nov, 10:30) drops in; your blue bubble
asks «¿Me acompañas al médico el día 14?» on «ir contigo»; two white answers come back on «no puede nadie», each with
a small red ✕; on «la cambias» the date flips from 14 to 25 and a red «Cita cambiada» pill lands on the card. Same
family as UGC #2 ins-02 (paper, white cards, indigo shadows; red only for what goes wrong)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

REPLIES = [("Ana", "#7C5CFF", "Ese día trabajo, lo siento"), ("Carlos", "#15A3A3", "Uf, no puedo…")]


def build():
    iid, P = "ins-01", "i1"; d = INS[iid]["duration"]
    c = dict(MIR=cue(iid, "miras"), CON=cue(iid, "contigo"), NO=cue(iid, "no"), NAD=cue(iid, "nadie"), CAM=cue(iid, "cambias"))
    css = """
    #i1-lrow { top: 214px; }
    #i1-lab { position: relative; }
    #i1-lab svg { display: block; width: 28px; height: 28px; color: #FFFFFF; }
    #i1-card { left: 110px; top: 300px; width: 860px; height: 236px; }
    #i1-day { position: absolute; left: 28px; top: 28px; width: 156px; height: 180px; border-radius: 22px; overflow: hidden;
      background: #FFFFFF; box-shadow: 0 0 0 3px «LINE»; }
    #i1-dayh { position: absolute; left: 0; top: 0; width: 156px; height: 50px; background: «RED»; color: #FFFFFF; text-align: center;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; line-height: 52px; letter-spacing: 0.14em; }
    .i1-num { position: absolute; left: 0; top: 52px; width: 156px; height: 128px; text-align: center; color: «INK»;
      font-weight: 800; font-size: 86px; line-height: 128px; letter-spacing: -0.03em; }
    #i1-hdr { position: absolute; left: 216px; top: 46px; font-weight: 800; font-size: 54px; line-height: 1; color: «INDIGO»; letter-spacing: -0.02em; }
    #i1-sub { position: absolute; left: 216px; top: 116px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 34px; line-height: 1;
      color: «MUTED»; white-space: nowrap; }
    #i1-chg { position: absolute; left: 216px; top: 164px; display: flex; align-items: center; gap: 10px; height: 52px; padding: 0 22px 0 14px;
      border-radius: 999px; background: «RED»; color: #FFFFFF; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; line-height: 1; letter-spacing: 0.08em; text-transform: uppercase; }
    #i1-chg svg { display: block; width: 30px; height: 30px; }
    #i1-me { right: 110px; top: 610px; transform-origin: 100% 100%; }
    .i1-rep { position: absolute; left: 110px; display: flex; align-items: flex-end; gap: 18px; transform-origin: 0% 100%; }
    .i1-ini { width: 84px; height: 84px; border-radius: 50%; flex: 0 0 84px; display: flex; align-items: center; justify-content: center;
      color: #FFFFFF; font-weight: 800; font-size: 36px; line-height: 1; box-shadow: 0 0 0 5px #FFFFFF, 0 12px 26px rgba(18,0,129,0.16); }
    .i1-rb { position: relative; }
    .i1-x { position: absolute; right: -20px; top: -20px; width: 48px; height: 48px; }
    .i1-x svg { display: block; width: 48px; height: 48px; filter: drop-shadow(0 6px 12px rgba(18,0,129,0.20)); }
    #i1-r0 { top: 822px; }
    #i1-r1 { top: 984px; }
"""
    reps = "\n".join(f"""    <div id="i1-r{k}" class="i1-rep"><div class="i1-ini" style="background:{col}">{name[0]}</div>
      <div class="i1-rb i1-bub i1-bub-w i1-bl" style="position: relative;">{txt}<div id="i1-x{k}" class="i1-x">{icon('xr')}</div></div></div>"""
                     for k, (name, col, txt) in enumerate(REPLIES))
    body = "\n".join([ground(P, "paper"), f"""    <div id="i1-lrow" class="i1-row"><div id="i1-lab" class="i1-ipill" style="position: relative;">{icon('cal')}<span>PEDIR CITA</span></div></div>
    <div id="i1-card" class="i1-card i1-on-paper">
      <div id="i1-day"><div id="i1-dayh">NOV</div><div id="i1-n0" class="i1-num">14</div><div id="i1-n1" class="i1-num">25</div></div>
      <div id="i1-hdr">Huisarts</div>
      <div id="i1-sub">Cita médica · 10:30</div>
      <div id="i1-chg">{icon('redo')}<span>Cita cambiada</span></div>
    </div>
    <div id="i1-me" class="i1-bub i1-bub-b i1-br">¿Me acompañas al médico<br/>el día 14?</div>
{reps}"""])
    js = """
      tl.fromTo(q("lab"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("card"), { opacity: 0, y: 70, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out" }, 0.04);
      tl.set(q("n1"), { opacity: 0 }, 0);
      tl.set(q("chg"), { opacity: 0 }, 0);
      tl.fromTo(q("me"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «MIR» + 0.42);
      tl.fromTo(q("r0"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «NO» - 0.12);
      tl.fromTo(q("r1"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «NAD» - 0.02);
      tl.fromTo(q("x0"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2)" }, «NO» + 0.12);
      tl.fromTo(q("x1"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2)" }, «NAD» + 0.2);
      // «la cambias»: the date flips 14 → 25, the red pill lands
      tl.to(q("n0"), { opacity: 0, y: -36, duration: 0.2, ease: "power2.in" }, «CAM» - 0.06);
      tl.fromTo(q("n1"), { opacity: 0, y: 36 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out", immediateRender: false }, «CAM» + 0.1);
      tl.fromTo(q("chg"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(1.8)", immediateRender: false }, «CAM» + 0.18);
"""
    sfx = [(c["MIR"] + 0.42, "pop", 0.16), (c["NO"] - 0.12, "notification", 0.14), (c["NAD"] - 0.02, "notification", 0.14),
           (c["CAM"] + 0.1, "click-soft", 0.22)]
    return comp(iid, d, P, css, body, js, c), sfx
