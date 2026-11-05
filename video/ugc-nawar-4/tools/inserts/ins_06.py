"""ins-06 · «(Quien lo consiga entra en nuestra) lista prioritaria y sabrá lo que estaremos preparando para este Black
Friday antes que nadie.» — on paper: the «Lista prioritaria» card (a star) with three people already on it, each with a
green tick; on «prioritaria» your own row slides in on top, in Nawar blue — «Tú» with the ebook «Holandés sin miedo» —;
on «preparando» a second card rises under it, in indigo: «Black Friday · Formación Nawar», its lines blurred and a white
padlock on it (what we are preparing, still under wraps); on «antes que nadie» the padlock springs open and a green
«Lo ves antes que nadie» pill lands on the card. Same family as UGC #2 (paper, white cards, indigo type)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

PEOPLE = [("Laura M.", "#7C5CFF"), ("Diego R.", "#15A3A3"), ("Carmen S.", "#D9487A")]
LOCK = ('<svg viewBox="0 0 64 64"><path id="i6-shk" d="M20 30 V20 A12 12 0 0 1 44 20 V30" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'
        '<rect x="12" y="28" width="40" height="30" rx="8" fill="#FFFFFF"/><circle cx="32" cy="41" r="4.5" fill="«INDIGO»"/>'
        '<rect x="30" y="42" width="4" height="9" rx="2" fill="«INDIGO»"/></svg>')


def row(rid, name, col, sub=""):
    av = f'<div class="i6-pic" style="background: {col};">{person()}</div>'
    s = f'<div class="i6-sub">{sub}</div>' if sub else ""
    return (f'<div id="i6-{rid}" class="i6-rw">{av}<div class="i6-nm"><div class="i6-n">{name}</div>{s}</div>'
            f'<div class="i6-ck">{icon("check")}</div></div>')


def build():
    iid, P = "ins-06", "i6"; d = INS[iid]["duration"]
    c = dict(PRI=cue(iid, "prioritaria"), SAB=cue(iid, "sabra"), PRE=cue(iid, "preparando"), BLA=cue(iid, "black"),
             ANT=cue(iid, "antes"), NAD=cue(iid, "nadie"))
    css = """
    #i6-list { left: 110px; top: 170px; width: 860px; height: 560px; overflow: hidden; }
    #i6-lh { position: absolute; left: 36px; top: 30px; display: flex; align-items: center; gap: 16px; font-weight: 800; font-size: 48px;
      color: «INDIGO»; letter-spacing: -0.02em; }
    #i6-lh svg { display: block; width: 48px; height: 48px; color: «BLUE»; }
    #i6-rows { position: absolute; left: 24px; top: 118px; width: 812px; }
    .i6-rw { position: relative; display: flex; align-items: center; gap: 22px; height: 100px; padding: 0 22px; margin-bottom: 10px;
      border-radius: 22px; background: «APP»; }
    .i6-pic { width: 68px; height: 68px; flex: 0 0 68px; border-radius: 50%; overflow: hidden; }
    .i6-pic svg { display: block; width: 68px; height: 68px; }
    .i6-nm { flex: 1 1 auto; }
    .i6-n { font-family: "Inter", sans-serif; font-weight: 700; font-size: 36px; line-height: 1.1; color: «INK»; }
    .i6-sub { font-family: "Inter", sans-serif; font-weight: 600; font-size: 24px; line-height: 1.2; color: rgba(255,255,255,0.85); }
    .i6-ck svg { display: block; width: 52px; height: 52px; }
    #i6-me { background: «BLUE»; }
    #i6-me .i6-n { color: #FFFFFF; }
    #i6-me .i6-pic { box-shadow: 0 0 0 4px #FFFFFF; }
    #i6-box { left: 110px; top: 780px; width: 860px; height: 330px; background: «INDIGO»; overflow: visible; }
    #i6-bk { position: absolute; left: 40px; top: 34px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; letter-spacing: 0.14em;
      color: «SKY»; text-transform: uppercase; }
    #i6-bt { position: absolute; left: 40px; top: 74px; font-weight: 800; font-size: 50px; line-height: 1.05; color: #FFFFFF; letter-spacing: -0.02em; }
    .i6-ln { position: absolute; left: 40px; height: 22px; border-radius: 11px; background: rgba(255,255,255,0.28); filter: blur(3px); }
    #i6-lock { position: absolute; right: 54px; top: 92px; width: 140px; height: 140px; border-radius: 50%; background: rgba(255,255,255,0.12);
      display: flex; align-items: center; justify-content: center; }
    #i6-lock svg { display: block; width: 84px; height: 84px; overflow: visible; }
    #i6-okrow { top: 1080px; }
    #i6-ok { gap: 14px; height: 88px; padding: 0 38px 0 24px; font-size: 40px; background: «GREEN»; color: #FFFFFF; }
    #i6-ok svg { display: block; width: 46px; height: 46px; }
"""
    star = icon("star")
    rows = "".join(row(f"r{k}", n, col) for k, (n, col) in enumerate(PEOPLE))
    me = row("me", "Tú", "«INDIGO»", "+ el libro «Holandés sin miedo»")
    body = "\n".join([ground(P, "paper"), f"""    <div id="i6-list" class="i6-card i6-on-paper">
      <div id="i6-lh">{star}<span>Lista prioritaria</span></div>
      <div id="i6-rows">{me}{rows}</div>
    </div>
    <div id="i6-box" class="i6-card">
      <div id="i6-bk">Black Friday</div><div id="i6-bt">Formación Nawar</div>
      <div class="i6-ln" style="top: 176px; width: 470px;"></div><div class="i6-ln" style="top: 222px; width: 380px;"></div>
      <div class="i6-ln" style="top: 268px; width: 430px;"></div>
      <div id="i6-lock">{sub(LOCK, {})}</div>
    </div>
    <div id="i6-okrow" class="i6-row"><div id="i6-ok" class="i6-wpill">{icon('checkw')}<span>Lo ves antes que nadie</span></div></div>"""])
    js = """
      tl.fromTo(q("list"), { opacity: 0.4, y: 30, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      // your row: the others are pushed down as it slides in on top
      tl.fromTo(q("rows"), { y: -110 }, { y: 0, duration: 0.34, ease: "power3.out", immediateRender: true }, «PRI» + 0.02);
      tl.fromTo(q("me"), { opacity: 0, x: -60, scale: 0.94 }, { opacity: 1, x: 0, scale: 1, duration: 0.34, ease: "back.out(1.6)" }, «PRI» + 0.02);
      tl.fromTo(q("box"), { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.36, ease: "power3.out" }, «PRE» - 0.06);
      tl.fromTo(q("lock"), { scale: 1 }, { keyframes: [{ scale: 1.12, duration: 0.1 }, { scale: 1, duration: 0.16 }], immediateRender: false }, «BLA» - 0.02);
      tl.fromTo("#i6-shk", { y: 0, rotation: 0 }, { y: -10, rotation: -24, svgOrigin: "44 30", duration: 0.26, ease: "back.out(2.4)", immediateRender: false }, «ANT» - 0.04);
      tl.fromTo(q("ok"), { opacity: 0, y: 26, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «ANT» + 0.1);
"""
    sfx = [(c["PRI"] + 0.02, "pop", 0.18), (c["PRE"] - 0.06, "whoosh-short", 0.1), (c["ANT"] - 0.04, "click", 0.18),
           (c["ANT"] + 0.1, "chime", 0.14)]
    return comp(iid, d, P, css, body, js, c), sfx
