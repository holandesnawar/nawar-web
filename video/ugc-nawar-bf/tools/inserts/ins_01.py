"""ins-01 · «(Antes de pedir cita,) miras quién puede ir contigo, y si ese día no puede nadie, la cambias.» — the
appointment card (Huisarts, 14 nov, 10:30) drops in; your blue bubble asks «¿Me acompañas al médico el día 14?»
on «ir contigo»; the two answers come back on «no puede nadie» (each with a red ✕); on «la cambias» the date flips
from 14 to 25 and a red «Cita cambiada» pill lands on the card. Reference module for the Black Friday family: dark
ground, white cards, Nawar blue for you, red for what goes wrong."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

REPLIES = [("Ana", "#7C5CFF", "Ese día trabajo, lo siento"), ("Carlos", "#15A3A3", "Uf, no puedo…")]


def build():
    iid, P = "ins-01", "i1"; d = INS[iid]["duration"]
    c = dict(MIR=cue(iid, "miras"), CON=cue(iid, "contigo"), NO=cue(iid, "no"), NAD=cue(iid, "nadie"), CAM=cue(iid, "cambias"))
    css = """
    #i1-card { left: 90px; top: 270px; width: 900px; height: 262px; }
    #i1-day { position: absolute; left: 30px; top: 30px; width: 166px; height: 202px; border-radius: 24px; overflow: hidden;
      background: #FFFFFF; box-shadow: 0 0 0 3px «LINE»; }
    #i1-dayh { position: absolute; left: 0; top: 0; width: 166px; height: 54px; background: «RED»; color: #FFFFFF; text-align: center;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 28px; line-height: 56px; letter-spacing: 0.14em; }
    .i1-num { position: absolute; left: 0; top: 56px; width: 166px; height: 146px; text-align: center; color: «INK»;
      font-weight: 800; font-size: 96px; line-height: 146px; letter-spacing: -0.03em; }
    #i1-hdr { position: absolute; left: 232px; top: 46px; font-weight: 800; font-size: 60px; line-height: 1; color: «INK»; letter-spacing: -0.02em; }
    #i1-sub { position: absolute; left: 232px; top: 122px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 38px; line-height: 1;
      color: «MUTED»; white-space: nowrap; }
    #i1-chg { position: absolute; left: 232px; top: 178px; display: flex; align-items: center; gap: 10px; height: 50px; padding: 0 22px 0 14px;
      border-radius: 999px; background: «RED»; color: #FFFFFF; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 25px; line-height: 1; letter-spacing: 0.06em; text-transform: uppercase; }
    #i1-chg svg { display: block; width: 30px; height: 30px; }
    #i1-me { right: 90px; top: 640px; transform-origin: 100% 100%; font-size: 46px; padding: 30px 40px; }
    .i1-rep { position: absolute; left: 90px; display: flex; align-items: flex-end; gap: 18px; transform-origin: 0% 100%; }
    .i1-ava { width: 92px; height: 92px; border-radius: 50%; flex: 0 0 92px; display: flex; align-items: center; justify-content: center;
      color: #FFFFFF; font-weight: 800; font-size: 38px; line-height: 1; box-shadow: 0 10px 24px rgba(0,0,0,0.35); }
    .i1-rb { position: relative; padding: 24px 34px; border-radius: 34px; border-bottom-left-radius: 10px; background: #FFFFFF; color: «INK»;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 44px; line-height: 1.2; letter-spacing: -0.01em; white-space: nowrap;
      box-shadow: 0 24px 50px rgba(0,0,0,0.40); }
    .i1-x { position: absolute; right: -22px; top: -22px; width: 52px; height: 52px; }
    .i1-x svg { display: block; width: 52px; height: 52px; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.35)); }
    #i1-r0 { top: 880px; }
    #i1-r1 { top: 1060px; }
"""
    reps = "\n".join(f"""    <div id="i1-r{k}" class="i1-rep"><div class="i1-ava" style="background:{col}">{name[0]}</div>
      <div class="i1-rb">{txt}<div id="i1-x{k}" class="i1-x">{icon('xr')}</div></div></div>""" for k, (name, col, txt) in enumerate(REPLIES))
    body = "\n".join([ground(P, "dark"), f"""    <div id="i1-card" class="i1-card i1-on-dark">
      <div id="i1-day"><div id="i1-dayh">NOV</div><div id="i1-n0" class="i1-num">14</div><div id="i1-n1" class="i1-num">25</div></div>
      <div id="i1-hdr">Huisarts</div>
      <div id="i1-sub">Cita médica · 10:30</div>
      <div id="i1-chg">{icon('redo')}<span>Cita cambiada</span></div>
    </div>
    <div id="i1-me" class="i1-bub i1-bub-b i1-br">¿Me acompañas al médico<br/>el día 14?</div>
{reps}"""])
    js = """
      tl.fromTo(q("card"), { opacity: 0, y: 70, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "power3.out" }, 0);
      tl.set(q("n1"), { opacity: 0 }, 0);
      tl.set(q("chg"), { opacity: 0 }, 0);
      tl.fromTo(q("me"), { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.7)" }, «MIR» + 0.42);
      tl.fromTo(q("r0"), { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.7)" }, «NO» - 0.12);
      tl.fromTo(q("r1"), { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.7)" }, «NAD» - 0.02);
      tl.fromTo(q("x0"), { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2.2)" }, «NO» + 0.12);
      tl.fromTo(q("x1"), { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2.2)" }, «NAD» + 0.2);
      // «la cambias»: the date flips 14 → 25, the card gives a small shake, the red pill lands
      tl.to(q("n0"), { opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }, «CAM» - 0.06);
      tl.fromTo(q("n1"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out", immediateRender: false }, «CAM» + 0.1);
      tl.to(q("card"), { keyframes: [{ x: -10, duration: 0.05 }, { x: 9, duration: 0.05 }, { x: -6, duration: 0.05 }, { x: 0, duration: 0.05 }] }, «CAM» + 0.08);
      tl.fromTo(q("chg"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)", immediateRender: false }, «CAM» + 0.18);
"""
    sfx = [(c["MIR"] + 0.42, "pop", 0.16), (c["NO"] - 0.12, "notification", 0.14), (c["NAD"] - 0.02, "notification", 0.14),
           (c["CAM"] + 0.08, "error", 0.12)]
    return comp(iid, d, P, css, body, js, c), sfx
