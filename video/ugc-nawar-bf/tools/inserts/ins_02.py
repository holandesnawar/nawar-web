"""ins-02 · «Cada vez que alguien habla por ti, tú te quedas sin practicar.» — on Nawar blue, at the counter: the
«En la gemeente» label; on «cada vez» the receptionist's white bubble («Wat is uw geboortedatum?»); on «alguien habla
por ti» your companion answers for you («12 maart 1990.»); on «tú» your own bubble comes in with three dots that
never turn into words, and fades on «te quedas»; on «sin practicar» a white «Sin practicar» pill with a red ✕ lands
under it. Same family as UGC #2 ins-01 (blue ground, white bubbles, small uppercase labels)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def build():
    iid, P = "ins-02", "i2"; d = INS[iid]["duration"]
    c = dict(CADA=cue(iid, "cada"), ALG=cue(iid, "alguien"), TU=cue(iid, "tu"), QUE=cue(iid, "quedas"), SIN=cue(iid, "sin"))
    css = """
    #i2-top { top: 190px; }
    .i2-blk { position: absolute; display: flex; align-items: flex-end; gap: 18px; }
    .i2-l { left: 100px; transform-origin: 0% 100%; }
    .i2-r { right: 100px; flex-direction: row-reverse; transform-origin: 100% 100%; }
    .i2-col { display: flex; flex-direction: column; gap: 12px; }
    .i2-l .i2-col { align-items: flex-start; }
    .i2-r .i2-col { align-items: flex-end; }
    .i2-lab { font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; line-height: 1; letter-spacing: 0.14em;
      text-transform: uppercase; color: rgba(255,255,255,0.78); white-space: nowrap; padding: 0 8px; }
    .i2-ava { display: none; position: relative; width: 88px; height: 88px; border-radius: 50%; flex: 0 0 88px; overflow: visible;
      box-shadow: 0 0 0 5px #FFFFFF; }
    .i2-face { position: absolute; left: 0; top: 0; width: 88px; height: 88px; border-radius: 50%; overflow: hidden; }
    .i2-face svg { display: block; width: 88px; height: 88px; }
    .i2-ava .i2-flag { position: absolute; right: -10px; bottom: -4px; }
    #i2-rec { top: 290px; }
    #i2-ra { background: #4B5575; }
    #i2-cmp { top: 486px; }
    #i2-ca { background: #7C5CFF; }
    #i2-cb { background: #E9E5FF; color: «INDIGO»; }
    #i2-you { top: 682px; }
    #i2-ya { background: «BLUE»; }
    #i2-yb { width: 200px; height: 98px; box-sizing: border-box; padding: 0; border-radius: 34px; border-bottom-right-radius: 10px;
      background: rgba(255,255,255,0.16); box-shadow: inset 0 0 0 2px rgba(255,255,255,0.32);
      display: flex; align-items: center; justify-content: center; gap: 16px; }
    .i2-dot { display: block; width: 18px; height: 18px; border-radius: 50%; background: #FFFFFF; }
    #i2-h { top: 898px; font-size: 70px; }
    #i2-sin { display: inline-flex; align-items: center; gap: 14px; padding: 4px 26px 10px 18px; }
    #i2-sin svg { display: block; width: 62px; height: 62px; margin-top: 6px; }
"""
    body = "\n".join([ground(P, "blue"), f"""    <div id="i2-top" class="i2-row"><div id="i2-pill" class="i2-pill"><span class="i2-flag">{FLAG_NL}</span><span>En la gemeente</span></div></div>
    <div id="i2-rec" class="i2-blk i2-l">
      <div id="i2-ra" class="i2-ava"><div class="i2-face">{person()}</div><span class="i2-flag">{FLAG_NL}</span></div>
      <div class="i2-col"><div class="i2-lab" style="display: flex; align-items: center; gap: 12px;"><span class="i2-flag" style="width: 34px; height: 23px; flex: 0 0 34px;">{FLAG_NL}</span>Recepción</div><div id="i2-rb" class="i2-bub i2-bub-w i2-bl" style="position: relative;">Wat is uw geboortedatum?</div></div>
    </div>
    <div id="i2-cmp" class="i2-blk i2-r">
      <div id="i2-ca" class="i2-ava"><div class="i2-face">{person()}</div></div>
      <div class="i2-col"><div class="i2-lab">Tu acompañante</div><div id="i2-cb" class="i2-bub i2-br" style="position: relative;">12 maart 1990.</div></div>
    </div>
    <div id="i2-you" class="i2-blk i2-r">
      <div id="i2-ya" class="i2-ava"><div class="i2-face">{person()}</div></div>
      <div class="i2-col"><div id="i2-yl" class="i2-lab">Tú</div><div id="i2-yb"><i id="i2-d0" class="i2-dot"></i><i id="i2-d1" class="i2-dot"></i><i id="i2-d2" class="i2-dot"></i></div></div>
    </div>
    <div id="i2-h" class="i2-h1"><span id="i2-h0" class="i2-w">Te quedas</span> <span id="i2-sin" class="i2-chip">{icon('xr')}<span>sin practicar</span></span></div>"""])
    js = """
      tl.fromTo(q("pill"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("rec"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «CADA» - 0.04);
      tl.fromTo(q("cmp"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «ALG» + 0.02);
      tl.fromTo(q("you"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «TU» - 0.06);
      ["d0", "d1", "d2"].forEach((id, k) => {
        tl.fromTo(q(id), { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.14, ease: "back.out(2)" }, «TU» + 0.1 + k * 0.08);
      });
      // «te quedas»: nothing comes, your side fades
      tl.fromTo(q("you"), { opacity: 1 }, { opacity: 0.45, duration: 0.3, ease: "power2.out", immediateRender: false }, «QUE» - 0.04);
      tl.fromTo(q("h0"), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, «QUE» - 0.08);
      tl.fromTo(q("sin"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.32, ease: "back.out(1.8)" }, «SIN» - 0.06);
"""
    sfx = [(c["CADA"] - 0.04, "notification", 0.14), (c["ALG"] + 0.02, "notification", 0.14), (c["TU"] - 0.06, "pop", 0.16),
           (c["SIN"] - 0.06, "click-soft", 0.24)]
    return comp(iid, d, P, css, body, js, c), sfx
