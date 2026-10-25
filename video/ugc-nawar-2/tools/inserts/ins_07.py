"""ins-07 · «…una clase en directo para reforzar lo aprendido y trabajar la pronunciación» — the live class (paul-clase-1,
the VSL's live-class video, in a call window with EN DIRECTO and a correction), then G · UI · UU · EU tiles.
Same design as UGC #1 ins-05."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

def build():
    iid, P = "ins-07", "i7"; d = INS[iid]["duration"]
    c = dict(DIR=cue(iid, "directo"), REF=cue(iid, "reforzar"), TRA=cue(iid, "trabajar"), PRO=cue(iid, "pronunciacion"))
    c["SWAP"] = round(c["TRA"] - 0.16, 3)
    c["VD"] = round(c["SWAP"] + 0.3, 3)
    # player region of paul-clase-1 (x 744–2480, y 10–970) covering a 960×504 area
    k = 960 / 1736
    c.update(VW=round(2502 * k, 1), VH=round(992 * k, 1), VL=round(-744 * k, 1), VT=round(-10 * k - (960 * k - 504) / 2, 1))
    css = """
    #i7-h1 { top: 200px; }
    #i7-h2 { top: 294px; }
    #i7-call { position: absolute; left: 60px; top: 452px; width: 960px; height: 576px; border-radius: 30px; overflow: hidden; background: #0C0C1E; }
    #i7-top { position: absolute; left: 0; top: 0; width: 960px; height: 72px; display: flex; align-items: center; gap: 18px; padding-left: 22px; box-sizing: border-box; }
    #i7-live { display: flex; align-items: center; gap: 10px; height: 42px; padding: 0 18px 0 14px; border-radius: 999px; background: «RED»; color: #FFFFFF;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 20px; letter-spacing: 0.14em; white-space: nowrap; }
    #i7-ldot { display: block; width: 12px; height: 12px; border-radius: 50%; background: #FFFFFF; }
    #i7-ttl { font-family: "Inter", sans-serif; font-weight: 600; font-size: 24px; color: rgba(255,255,255,0.74); white-space: nowrap; }
    #i7-vid { position: absolute; left: 0; top: 72px; width: 960px; height: 504px; overflow: hidden; }
    #i7-v { position: absolute; left: «VL»px; top: «VT»px; width: «VW»px; height: «VH»px; }
    #i7-ctl { position: absolute; left: 330px; top: 414px; width: 300px; height: 72px; display: flex; justify-content: center; gap: 18px; }
    .i7-cb { position: relative; width: 66px; height: 66px; border-radius: 50%; background: rgba(12,12,30,0.62); }
    .i7-cb svg { position: absolute; left: 15px; top: 15px; width: 36px; height: 36px; }
    #i7-hang { background: «RED»; }
    #i7-fix { top: 1078px; gap: 18px; }
    .i7-fx { display: flex; align-items: center; gap: 12px; height: 70px; padding: 0 28px; border-radius: 999px; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 32px; line-height: 1; }
    #i7-bad { position: relative; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); color: rgba(255,255,255,0.8); }
    #i7-bads { position: absolute; left: 22px; top: 32px; width: calc(100% - 44px); height: 6px; border-radius: 3px; background: «RED»; transform-origin: 0% 50%; }
    #i7-arr { width: 44px; height: 44px; color: #FFFFFF; }
    #i7-arr svg { display: block; width: 44px; height: 44px; }
    #i7-good { background: #FFFFFF; color: «INDIGO»; padding-left: 14px; box-shadow: 0 16px 40px rgba(4,0,40,0.3); }
    #i7-good svg { display: block; width: 40px; height: 40px; }
    #i7-prow { top: 250px; }
    .i7-tile { position: absolute; width: 404px; height: 330px; border-radius: 36px; background: #FFFFFF;
      box-shadow: 0 40px 100px rgba(4,0,40,0.42), 0 8px 24px rgba(4,0,40,0.2); }
    .i7-big { position: absolute; left: 0; top: 52px; width: 404px; text-align: center; font-weight: 900; font-size: 150px; line-height: 1;
      letter-spacing: -0.04em; color: «INDIGO»; }
    .i7-ex { position: absolute; left: 0; top: 236px; width: 404px; text-align: center; font-family: "Inter", sans-serif; font-weight: 600;
      font-size: 34px; line-height: 1; color: «MUTED»; }
"""
    tiles = [("G", "goed", 121, 366), ("UI", "huis", 555, 366), ("UU", "uur", 121, 730), ("EU", "leuk", 555, 730)]
    tile_html = "\n".join(f'      <div id="i7-t{k}" class="i7-tile" style="left:{x}px; top:{y}px;"><div class="i7-big">{b}</div><div class="i7-ex">{e}</div></div>'
                          for k, (b, e, x, y) in enumerate(tiles))
    body = "\n".join([ground(P, "blue"), f"""    <div id="i7-s1" class="i7-full">
      <div id="i7-h1" class="i7-h1">Clase en directo</div>
      <div id="i7-h2" class="i7-h1 i7-acc">cada semana</div>
      <div id="i7-call" class="i7-on-blue">
        <div id="i7-top"><div id="i7-live"><span id="i7-ldot"></span><span>EN DIRECTO</span></div><div id="i7-ttl">Clase semanal · Holandés Nawar</div></div>
        <div id="i7-vid"><video id="i7-v" class="clip" src="assets/video/paul-clase-1.mp4" muted playsinline data-start="0" data-duration="«VD»" data-media-start="5.2" data-track-index="1" data-hf-media-start-basis="local" data-layout-allow-overflow></video>
          <div id="i7-ctl"><div class="i7-cb">{icon('mic')}</div><div class="i7-cb">{icon('cam')}</div><div id="i7-hang" class="i7-cb">{icon('hang')}</div></div></div>
      </div>
      <div id="i7-fix" class="i7-row"><div id="i7-bad" class="i7-fx"><span>Werkt jij?</span><div id="i7-bads"></div></div><div id="i7-arr">{icon('down').replace('M24 8 V38 M12 27 L24 39 L36 27', 'M8 24 H38 M27 12 L39 24 L27 36')}</div><div id="i7-good" class="i7-fx">{icon('check')}<span>Werk jij?</span></div></div>
    </div>
    <div id="i7-s2" class="i7-full">
      <div id="i7-prow" class="i7-row"><div id="i7-pp" class="i7-pill"><span>Pronunciación</span></div></div>
{tile_html}
    </div>"""])
    js = """
      tl.fromTo(q("h1"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("h2"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.1);
      tl.fromTo(q("call"), { opacity: 0, y: 100, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.44, ease: "power3.out" }, 0.04);
      tl.fromTo(q("live"), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.2)" }, «DIR» - 0.06);
      tl.fromTo(q("ldot"), { opacity: 1 }, { keyframes: [{ opacity: 0.25, duration: 0.3 }, { opacity: 1, duration: 0.3 }, { opacity: 0.25, duration: 0.3 }, { opacity: 1, duration: 0.3 }], immediateRender: false }, «DIR» + 0.3);
      tl.fromTo(q("bad"), { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.28, ease: "power3.out" }, «REF» - 0.08);
      tl.fromTo(q("bads"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power2.out" }, «REF» + 0.3);
      tl.fromTo(q("arr"), { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 0.22, ease: "power3.out" }, «REF» + 0.42);
      tl.fromTo(q("good"), { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, «REF» + 0.52);
      tl.to(q("s1"), { opacity: 0, y: -90, duration: 0.24, ease: "power2.in" }, «SWAP» - 0.2);
      tl.fromTo(q("s2"), { opacity: 0 }, { opacity: 1, duration: 0.01 }, «SWAP» - 0.02);
      tl.fromTo(q("pp"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.26, ease: "power3.out" }, «SWAP»);
      tl.fromTo(q("t0"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.02);
      tl.fromTo(q("t1"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.12);
      tl.fromTo(q("t2"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.22);
      tl.fromTo(q("t3"), { opacity: 0, scale: 0.6, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «SWAP» + 0.32);
"""
    sfx = [(c["DIR"] - 0.06, "notification", 0.2), (c["REF"] + 0.52, "ping", 0.2), (c["SWAP"], "whoosh-short", 0.12),
           (c["SWAP"] + 0.02, "pop", 0.16), (c["SWAP"] + 0.22, "pop", 0.16)]
    return comp(iid, d, P, css, body, js, c), sfx

