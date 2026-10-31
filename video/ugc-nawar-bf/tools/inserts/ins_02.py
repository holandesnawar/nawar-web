"""ins-02 · «Cada vez que alguien habla por ti, tú te quedas sin practicar.» — at the gemeente counter: a white
«En la gemeente» pill (NL flag) sits on top; on «cada vez» the receptionist's white bubble pops on the left
(«Wat is uw geboortedatum?»); on «alguien habla» your companion's purple bubble answers from your side
(«12 maart 1990»); on «tú» your own Nawar-blue bubble comes in with three dots that never turn into words, and on
«te quedas» it greys out; on «sin practicar» a red «SIN PRACTICAR» stamp slams in under it (tilted, fast scale-down,
small shake of the scene). Same family as ins-01: dark ground, white cards, Nawar blue for you, red for what goes
wrong."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def build():
    iid, P = "ins-02", "i2"; d = INS[iid]["duration"]
    c = dict(CADA=cue(iid, "cada"), ALG=cue(iid, "alguien"), HAB=cue(iid, "habla"), TU=cue(iid, "tu"),
             QUE=cue(iid, "quedas"), SIN=cue(iid, "sin"), PRA=cue(iid, "practicar"), PURPLE="#7C5CFF", DIM="#33496F")
    css = """
    #i2-top { top: 244px; }
    .i2-blk { position: absolute; display: flex; align-items: flex-end; gap: 20px; }
    .i2-l { left: 90px; transform-origin: 0% 100%; }
    .i2-r { right: 90px; flex-direction: row-reverse; transform-origin: 100% 100%; }
    .i2-col { display: flex; flex-direction: column; gap: 14px; }
    .i2-l .i2-col { align-items: flex-start; }
    .i2-r .i2-col { align-items: flex-end; }
    .i2-lab { font-family: "Inter", sans-serif; font-weight: 700; font-size: 30px; line-height: 1; letter-spacing: 0.14em;
      text-transform: uppercase; color: rgba(255,255,255,0.82); white-space: nowrap; padding: 0 10px; }
    .i2-ava { position: relative; width: 104px; height: 104px; border-radius: 50%; flex: 0 0 104px;
      box-shadow: 0 0 0 5px rgba(255,255,255,0.92), 0 14px 30px rgba(0,0,0,0.45); }
    .i2-face { position: absolute; left: 0; top: 0; width: 104px; height: 104px; border-radius: 50%; overflow: hidden; }
    .i2-face svg { display: block; width: 104px; height: 104px; }
    .i2-ava .i2-flag { position: absolute; right: -8px; bottom: -2px; }
    .i2-b { position: relative; padding: 28px 40px; border-radius: 36px; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 46px; line-height: 1.2; letter-spacing: -0.01em;
      box-shadow: 0 24px 50px rgba(0,0,0,0.40); }
    #i2-rec { top: 384px; }
    #i2-rb { background: #FFFFFF; color: «INK»; border-bottom-left-radius: 10px; }
    #i2-ra { background: #4B5575; }
    #i2-cmp { top: 594px; }
    #i2-cb { background: «PURPLE»; color: #FFFFFF; border-bottom-right-radius: 10px; }
    #i2-ca { background: «PURPLE»; }
    #i2-you { top: 804px; }
    #i2-yb { width: 230px; height: 111px; box-sizing: border-box; padding: 0; background: «BLUE»; border-bottom-right-radius: 10px;
      display: flex; align-items: center; justify-content: center; gap: 18px; }
    #i2-ya { background: «BLUE»; }
    .i2-dot { display: block; width: 22px; height: 22px; border-radius: 50%; background: #FFFFFF; }
    #i2-stamp { position: absolute; left: 150px; top: 1034px; width: 780px; height: 140px; border-radius: 26px; background: «RED»;
      display: flex; align-items: center; justify-content: center; transform-origin: 50% 50%;
      box-shadow: inset 0 0 0 7px #FFFFFF, inset 0 0 0 13px «RED», 0 30px 70px rgba(0,0,0,0.55), 0 0 60px rgba(224,45,60,0.35); }
    #i2-st { font-weight: 900; font-size: 80px; line-height: 1; letter-spacing: 0.02em; color: #FFFFFF; white-space: nowrap; padding-top: 6px; }
"""
    body = "\n".join([ground(P, "dark"), f"""    <div id="i2-scene" class="i2-full">
    <div id="i2-top" class="i2-row"><div id="i2-pill" class="i2-wpill"><span class="i2-flag i2-flagd">{FLAG_NL}</span><span>En la gemeente</span></div></div>
    <div id="i2-rec" class="i2-blk i2-l">
      <div id="i2-ra" class="i2-ava"><div class="i2-face">{person()}</div><span class="i2-flag">{FLAG_NL}</span></div>
      <div class="i2-col"><div class="i2-lab">Recepción</div><div id="i2-rb" class="i2-b">Wat is uw geboortedatum?</div></div>
    </div>
    <div id="i2-cmp" class="i2-blk i2-r">
      <div id="i2-ca" class="i2-ava"><div class="i2-face">{person()}</div></div>
      <div class="i2-col"><div class="i2-lab">Tu acompañante</div><div id="i2-cb" class="i2-b">12 maart 1990.</div></div>
    </div>
    <div id="i2-you" class="i2-blk i2-r">
      <div id="i2-ya" class="i2-ava"><div class="i2-face">{person()}</div></div>
      <div class="i2-col"><div id="i2-yl" class="i2-lab">Tú</div><div id="i2-yb" class="i2-b"><i id="i2-d0" class="i2-dot"></i><i id="i2-d1" class="i2-dot"></i><i id="i2-d2" class="i2-dot"></i></div></div>
    </div>
    <div id="i2-stamp"><div id="i2-st">SIN PRACTICAR</div></div>
    </div>"""])
    js = """
      tl.fromTo(q("pill"), { opacity: 0, y: -24, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "power3.out" }, 0);
      // «cada vez»: the receptionist asks
      tl.fromTo(q("rec"), { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.7)" }, «CADA» - 0.04);
      // «alguien habla por ti»: the companion answers from your side
      tl.fromTo(q("cmp"), { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.7)" }, «ALG» + 0.02);
      // «tú»: your bubble comes in, the dots try…
      tl.fromTo(q("you"), { opacity: 0, scale: 0.7, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.7)" }, «TU» - 0.06);
      ["d0", "d1", "d2"].forEach((id, k) => {
        tl.fromTo(q(id), { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.14, ease: "back.out(2.4)" }, «TU» + 0.1 + k * 0.08);
      });
      // «te quedas»: …and the bubble greys out, nothing comes
      tl.fromTo(q("yb"), { backgroundColor: "«BLUE»" }, { backgroundColor: "«DIM»", duration: 0.3, ease: "power2.out" }, «QUE» - 0.04);
      tl.fromTo(q("ya"), { backgroundColor: "«BLUE»" }, { backgroundColor: "«DIM»", duration: 0.3, ease: "power2.out" }, «QUE» - 0.04);
      tl.fromTo([q("d0"), q("d1"), q("d2")], { opacity: 1 }, { opacity: 0.45, duration: 0.3, ease: "power2.out", immediateRender: false }, «QUE» - 0.04);
      tl.fromTo(q("yl"), { opacity: 1 }, { opacity: 0.4, duration: 0.3, ease: "power2.out", immediateRender: false }, «QUE» - 0.04);
      // «sin practicar»: the red stamp slams in, the scene takes the hit
      tl.fromTo(q("stamp"), { opacity: 0, scale: 1.9, rotation: -14 }, { opacity: 1, scale: 1, rotation: -5, duration: 0.17, ease: "power4.in" }, «SIN» - 0.06);
      tl.to(q("stamp"), { keyframes: [{ scale: 0.96, duration: 0.05 }, { scale: 1, duration: 0.12, ease: "back.out(2)" }] }, «SIN» + 0.11);
      tl.to(q("scene"), { keyframes: [{ x: -12, y: 4, duration: 0.05 }, { x: 10, y: -3, duration: 0.05 }, { x: -6, y: 2, duration: 0.05 }, { x: 0, y: 0, duration: 0.05 }] }, «SIN» + 0.11);
"""
    sfx = [(c["CADA"] - 0.04, "notification", 0.14), (c["ALG"] + 0.02, "notification", 0.14), (c["TU"] - 0.06, "pop", 0.16),
           (c["SIN"] + 0.11, "error", 0.3)]
    return comp(iid, d, P, css, body, js, c), sfx
