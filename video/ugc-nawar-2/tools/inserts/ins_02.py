"""ins-02 · «(Vivimos en un país en donde) el inglés te saca del paso, pero si has venido para quedarte, el neerlandés
es lo que te va a abrir puertas» — two stacked cards on paper: a quiet, secondary «Inglés · Te saca del paso» card
(a grey plaster: it patches, it doesn't solve), a «Si has venido para quedarte» bridge, then the strong «Neerlandés»
card whose padlock opens on «abrir» and three doors (Trabajo · Amigos · Trámites) on «puertas»."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

# simple bold line icons (48 box, stroke ~4), coloured by currentColor
PLASTER = ('<svg viewBox="0 0 48 48"><g transform="rotate(-45 24 24)" fill="none" stroke="currentColor" stroke-width="3.8" stroke-linejoin="round">'
           '<rect x="3.5" y="14.5" width="41" height="19" rx="9.5"/><path d="M17 14.5 V33.5 M31 14.5 V33.5"/></g>'
           '<g transform="rotate(-45 24 24)" fill="currentColor"><circle cx="21.2" cy="20.8" r="1.7"/><circle cx="26.8" cy="20.8" r="1.7"/>'
           '<circle cx="21.2" cy="27.2" r="1.7"/><circle cx="26.8" cy="27.2" r="1.7"/></g></svg>')
HOME = ('<svg viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M7 22 L24 8 L41 22"/><path d="M12 18.5 V40 H36 V18.5"/><path d="M20.5 40 V29.5 H27.5 V40"/></g></svg>')
CASE = ('<svg viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="6" y="14" width="36" height="26" rx="5"/><path d="M17 14 V10 A3 3 0 0 1 20 7 H28 A3 3 0 0 1 31 10 V14"/><path d="M6 25 H42"/></g></svg>')
PEOPLE = ('<svg viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
          '<circle cx="18" cy="16" r="6.5"/><path d="M5 40 C5 31 10.5 26.5 18 26.5 C25.5 26.5 31 31 31 40"/>'
          '<path d="M30.5 9.8 A6.5 6.5 0 0 1 30.5 22.2"/><path d="M35 27.5 C40 29 43 33.5 43 40"/></g></svg>')
DOC = ('<svg viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M11 6 H28 L38 16 V42 H11 Z"/><path d="M28 6 V16 H38"/><path d="M18 25 H31 M18 33 H27"/></g></svg>')


def lock(P):
    """padlock: filled body + keyhole, the shackle in two groups (lift, then swing on its right leg)."""
    return (f'<svg viewBox="0 0 64 64"><g id="{P}-shk"><g id="{P}-shkr"><path d="M20.5 30 V21 A11.5 11.5 0 0 1 43.5 21 V30" fill="none" '
            f'stroke="currentColor" stroke-width="6" stroke-linecap="round"/></g></g>'
            '<rect x="11" y="28" width="42" height="30" rx="8" fill="currentColor"/>'
            '<circle cx="32" cy="40.5" r="4.2" fill="#FFFFFF"/><path d="M32 43 V49.5" stroke="#FFFFFF" stroke-width="4.4" stroke-linecap="round"/></svg>')


def build():
    iid, P = "ins-02", "i2"; d = INS[iid]["duration"]
    c = dict(ING=cue(iid, "ingles"), SACA=cue(iid, "saca"), VEN=cue(iid, "venido"), QUE=cue(iid, "quedarte"),
             NEER=cue(iid, "neerlandes"), ABR=cue(iid, "abrir"), PUE=cue(iid, "puertas"))
    c.update(LIFT=38,   # card 2's title sits centred until «abrir», then makes room for «Te abre puertas»
             SHIFT=130)  # card 1 + bridge start lower (balanced in the content zone) and step up as card 2 arrives
    css = """
    #i2-c1 { left: 130px; top: 450px; width: 820px; height: 220px;
      box-shadow: 0 18px 50px rgba(18,0,129,0.10), 0 3px 10px rgba(18,0,129,0.06); }
    #i2-tag1 { left: 46px; top: -28px; background: #8C94AE; box-shadow: 0 6px 14px rgba(29,0,132,0.10), 0 0 0 5px #FFFFFF; }
    #i2-t1 { position: absolute; left: 54px; top: 52px; font-weight: 800; font-size: 62px; line-height: 1.1; letter-spacing: -0.025em;
      color: «INK»; white-space: nowrap; }
    #i2-s1 { position: absolute; left: 57px; top: 136px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 34px; line-height: 1.2;
      letter-spacing: -0.01em; color: «MUTED»; white-space: nowrap; }
    #i2-ic1 { position: absolute; right: 50px; top: 58px; width: 104px; height: 104px; border-radius: 50%; background: #EEF1F7; color: #A3ABC2; }
    #i2-ic1 svg { position: absolute; left: 24px; top: 24px; width: 56px; height: 56px; }

    .i2-ln { position: absolute; left: 538px; width: 4px; height: 43px; transform-origin: 50% 0%;
      background: repeating-linear-gradient(180deg, rgba(29,0,132,0.28) 0px, rgba(29,0,132,0.28) 10px, rgba(29,0,132,0) 10px, rgba(29,0,132,0) 18px); }
    #i2-lna { top: 670px; }
    #i2-lnb { top: 777px; }
    #i2-brow { top: 713px; height: 64px; }
    #i2-bridge { display: flex; align-items: center; gap: 12px; height: 64px; padding: 0 30px 0 18px; border-radius: 999px; background: «INDIGO»;
      color: #FFFFFF; white-space: nowrap; box-shadow: 0 12px 26px rgba(29,0,132,0.22), 0 0 0 6px «PAPER»;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 28px; line-height: 1; letter-spacing: -0.005em; }
    #i2-bridge svg { display: block; width: 34px; height: 34px; }
    #i2-quedarte { color: #FFFFFF; }

    #i2-c2 { left: 80px; top: 690px; width: 920px; height: 280px;
      box-shadow: 0 0 0 3px «INDIGO», 0 40px 100px rgba(18,0,129,0.24), 0 10px 26px rgba(18,0,129,0.12); }
    #i2-tag2 { left: 52px; top: -28px; }
    #i2-t2 { position: absolute; left: 58px; top: 62px; font-weight: 800; font-size: 72px; line-height: 1.1; letter-spacing: -0.03em;
      color: «INDIGO»; white-space: nowrap; }
    #i2-s2 { position: absolute; left: 62px; top: 160px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 38px; line-height: 1.2;
      letter-spacing: -0.01em; color: «INK2»; white-space: nowrap; }
    #i2-lk { position: absolute; right: 56px; top: 70px; width: 140px; height: 140px; border-radius: 50%; background: #ECEAFB; color: «INDIGO»; }
    #i2-lk svg { position: absolute; left: 30px; top: 26px; width: 80px; height: 80px; overflow: visible; }
    #i2-lring { position: absolute; right: 56px; top: 70px; width: 140px; height: 140px; border-radius: 50%; border: 5px solid «GREEN»;
      box-sizing: border-box; opacity: 0; }

    #i2-chips { top: 1018px; height: 80px; gap: 18px; }
    .i2-ch { display: flex; align-items: center; gap: 12px; height: 76px; padding: 0 30px 0 22px; border-radius: 999px; background: #FFFFFF;
      color: «INDIGO»; white-space: nowrap; box-shadow: 0 16px 36px rgba(18,0,129,0.13), 0 3px 8px rgba(18,0,129,0.07);
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 31px; line-height: 1; padding-top: 2px; box-sizing: border-box; }
    .i2-ch svg { display: block; width: 36px; height: 36px; margin-top: -2px; }
"""

    def chip(k, svg, label):
        return f'<div id="i2-ch{k}" class="i2-ch">{svg}<span>{label}</span></div>'

    body = "\n".join([ground(P, "paper"), f"""    <div id="i2-c1" class="i2-card" data-layout-allow-overflow>
      <div id="i2-tag1" class="i2-ipill"><span class="i2-flag">{FLAG_EN}</span><span>EN</span></div>
      <div id="i2-t1">Inglés</div>
      <div id="i2-s1">Te saca del paso</div>
      <div id="i2-ic1">{PLASTER}</div>
    </div>
    <div id="i2-lna" class="i2-ln"></div>
    <div id="i2-lnb" class="i2-ln"></div>
    <div id="i2-brow" class="i2-row"><div id="i2-bridge">{HOME}<span>Si has venido para <span id="i2-quedarte">quedarte</span></span></div></div>
    <div id="i2-c2" class="i2-card" data-layout-allow-overflow>
      <div id="i2-tag2" class="i2-ipill"><span class="i2-flag">{FLAG_NL}</span><span>NL</span></div>
      <div id="i2-t2">Neerlandés</div>
      <div id="i2-s2">Te abre puertas</div>
      <div id="i2-lring"></div>
      <div id="i2-lk">{lock(P)}</div>
    </div>
    <div id="i2-chips" class="i2-row">{chip(1, CASE, 'Trabajo')}{chip(2, PEOPLE, 'Amigos')}{chip(3, DOC, 'Trámites')}</div>"""])

    js = """
      // card 1 · «el inglés te saca del paso»: quiet, secondary
      tl.fromTo(q("c1"), { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.42, ease: "power3.out" }, 0.02);
      tl.fromTo(q("tag1"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «ING» - 0.08);
      tl.fromTo(q("t1"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «ING» - 0.08);
      tl.fromTo(q("s1"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, «SACA» - 0.06);
      tl.fromTo(q("ic1"), { opacity: 0, scale: 0.6, rotation: -24 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.36, ease: "back.out(1.8)" }, «SACA» - 0.04);
      // bridge · «si has venido para quedarte»
      tl.fromTo(q("lna"), { scaleY: 0 }, { scaleY: 1, duration: 0.26, ease: "power2.out" }, «VEN» - 0.14);
      tl.fromTo(q("bridge"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.32, ease: "back.out(1.8)" }, «VEN» - 0.06);
      tl.fromTo(q("quedarte"), { color: "#FFFFFF" }, { color: "«SKY»", duration: 0.2, ease: "power2.out" }, «QUE» - 0.06);
      // card 2 · «el neerlandés»: the stack steps up to make room, card 1 steps back, the bigger indigo card rises
      tl.to([q("c1"), q("lna"), q("brow"), q("lnb")], { y: -«SHIFT», duration: 0.5, ease: "power3.inOut" }, «NEER» - 0.3);
      tl.to(q("c1"), { opacity: 0.5, scale: 0.97, duration: 0.36, ease: "power2.out" }, «NEER» - 0.08);
      tl.fromTo(q("c2"), { opacity: 0, y: 90, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.44, ease: "power3.out" }, «NEER» - 0.09);
      tl.fromTo(q("lnb"), { scaleY: 0 }, { scaleY: 1, duration: 0.34, ease: "power2.out" }, «NEER» - 0.08);
      tl.fromTo(q("tag2"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «NEER» - 0.04);
      tl.fromTo(q("t2"), { opacity: 0, y: «LIFT» + 18 }, { opacity: 1, y: «LIFT», duration: 0.32, ease: "power3.out" }, «NEER» - 0.06);
      tl.fromTo(q("lk"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.36, ease: "back.out(1.8)" }, «NEER» + 0.02);
      tl.fromTo(q("s2"), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «ABR» - 0.08);
      tl.to(q("t2"), { y: 0, duration: 0.3, ease: "power3.out" }, «ABR» - 0.09);
      // «abrir»: the padlock opens (shackle lifts, swings on its right leg) and turns green
      tl.fromTo(q("shk"), { y: 0 }, { y: -9, duration: 0.14, ease: "power2.out" }, «ABR» - 0.04);
      tl.fromTo(q("shkr"), { rotation: 0 }, { rotation: 24, svgOrigin: "43.5 30", duration: 0.26, ease: "back.out(2.2)" }, «ABR» + 0.06);
      tl.set(q("lk"), { color: "«GREEN»", backgroundColor: "#E3F4E8" }, «ABR» + 0.06);   // one step: no muddy indigo→green blend
      tl.to(q("lk"), { keyframes: [{ scale: 1.08, duration: 0.1, ease: "power2.out" }, { scale: 1, duration: 0.22, ease: "power2.inOut" }] }, «ABR» + 0.04);
      tl.fromTo(q("lring"), { opacity: 0, scale: 1 }, { opacity: 0.6, duration: 0.01 }, «ABR» + 0.05);
      tl.to(q("lring"), { opacity: 0, scale: 1.45, duration: 0.5, ease: "power2.out" }, «ABR» + 0.06);
      // «puertas»: three doors it opens
      tl.fromTo(q("ch1"), { opacity: 0, y: 24, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "back.out(1.8)" }, «PUE» - 0.1);
      tl.fromTo(q("ch2"), { opacity: 0, y: 24, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "back.out(1.8)" }, «PUE» - 0.07);
      tl.fromTo(q("ch3"), { opacity: 0, y: 24, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "back.out(1.8)" }, «PUE» - 0.04);
"""
    sfx = [(c["ING"] - 0.08, "pop", 0.2), (c["VEN"] - 0.06, "click-soft", 0.22), (c["ABR"] - 0.04, "click", 0.2),
           (c["PUE"] - 0.1, "sparkle", 0.05)]   # soft: it read as a game sound at 0.12
    return comp(iid, d, P, css, body, js, c), sfx
