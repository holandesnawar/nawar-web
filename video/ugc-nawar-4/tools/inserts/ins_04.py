"""ins-04 · «(Si empiezas ya,) en Navidad vas a entender cosas que antes se te escapaban.» — v5 (the client: a Christmas
table, people talking, faces; «sin el texto ese de la familia»): just real footage, full frame in 9:16 — «Several
friends having a Christmas dinner» (Mixkit 42152, cropped from 4K, tools/fetch_assets.sh): the table set, candles,
Santa hats, talk. No text over it but the captions.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = {}
    css = """
    #i4-v { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }
    #i4-nl { left: 90px; top: 230px; font-size: 48px; transform-origin: 0% 100%; }
    #i4-es { left: 90px; top: 470px; max-width: 900px; padding: 22px 30px; border-radius: 28px; background: «BLUE»; color: #FFFFFF;
      display: flex; align-items: flex-start; gap: 18px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 40px; line-height: 1.22; }
    #i4-es .i4-flag { margin-top: 8px; width: 46px; height: 31px; flex: 0 0 46px; }
    #i4-es .i4-flag svg { width: 46px; height: 31px; }
    #i4-okrow { top: 1130px; }
    #i4-ok { gap: 14px; height: 92px; padding: 0 40px 0 24px; font-size: 42px; background: «GREEN»; color: #FFFFFF; }
    #i4-ok svg { display: block; width: 48px; height: 48px; }
"""
    body = """    <video id="i4-v" class="clip" src="assets/video/stock-xmas.mp4" muted playsinline data-start="0" data-duration="«D»" data-track-index="1"></video>
    <div class="i4-scr" style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 52%, rgba(6,4,30,0.62) 68%, rgba(6,4,30,0.62) 76%, rgba(0,0,0,0) 90%);"></div>"""
    js = """
      tl.fromTo(q("v"), { scale: 1.0 }, { scale: 1.04, duration: «D», ease: "none" }, 0);   // a slow push
"""
    sfx = []
    return comp(iid, d, P, css, body, js, c), sfx
