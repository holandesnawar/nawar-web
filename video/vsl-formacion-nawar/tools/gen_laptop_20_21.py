#!/usr/bin/env python3
"""Emit compositions/frames/20-pausa.html + 21-portatil.html (and their .sfx.json) from ONE MacBook rig.

v3 — the realistic MacBook Pro of tools/mac_mockup.md, rebuilt as a small CSS-3D rig that both frames
share (same functions, only the id prefix changes), so 20's last frame and 21's first frame match:

  cam   (2D wrapper: x / y / roll / scale, origin = the hinge point)
  stage (= the .mbp device box; perspective PERSP -> PERSP_END in 21, eye ON the hinge line = deck height)
  body  (rotationX: BODY0 = seen from above, slightly from the front so the slab's edge reads; 0 = straight on)
    table-shadow plane (in the table plane: only visible from above)
    deck  (the base's top face: dark, keyless, edge-on when straight on, so never seen)
    lip   (the mockup's front lip, placed at the deck's front edge and pre-shrunk by 1/K so that,
           straight on, it projects exactly onto the mockup lip: 1236u x 27u)
    lid   (rotationX about the hinge: -90 = closed, 0 = open) = mockup lid (front face) +
          aluminium edge layers + the silver outer face (no logo)

Straight on (body 0, lid 0) the rig IS the 2D mockup (lid at z=0, lip projected 1:1).
v4 — no boot screen: the lid opens straight onto the website (nuestra-vision.mp4), which hands over to the
course page (formacion-134.mp4) on the bar line SWITCH. Durations and every word cue are read from timing.json,
so a new voice only needs `python3 tools/timing.py && python3 tools/gen_laptop_20_21.py`.

Run:  python3 tools/gen_laptop_20_21.py   (rewrites both frames + both sidecars)
"""
import os, json, math

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PROJ, "compositions", "frames")

_T = {f["id"]: f for f in json.load(open(os.path.join(PROJ, "timing.json")))["frames"]}
D20, D21 = round(_T["20-pausa"]["duration"], 3), round(_T["21-portatil"]["duration"], 3)
W20, W21 = _T["20-pausa"]["words"], _T["21-portatil"]["words"]
_TOTAL = json.load(open(os.path.join(PROJ, "timing.json")))["total"]
PAUSED_AT = _T["20-pausa"]["start"]                       # the player in 20 shows where the film paused
PLAYER_TIME = "%d:%02d / %d:%02d" % (int(PAUSED_AT) // 60, int(PAUSED_AT) % 60, int(_TOTAL) // 60, int(_TOTAL) % 60)
PLAYER_PCT = "%.1f%%" % (100 * PAUSED_AT / _TOTAL)
SWITCH = 2.4                  # 21: website -> course page (one bar after the drop, before the voice returns)


def cue(words, i, lead=0.02):
    """frame-relative reveal time for word i (lands `lead` s before the word)."""
    return round(words[i]["t"] - lead, 3)

# ---------------------------------------------------------------- device geometry (mac_mockup.md units)
SW = 896                      # --sw: screen width (px)
U = SW / 1120.0               # 1u = 0.8 px
BOX_W, BOX_H = 1236 * U, 778 * U
HX, HY = 618 * U, 751 * U     # hinge line / eye point inside the device box
LID_L, LID_W, LID_H = 38 * U, 1160 * U, 754 * U
PERSP = 3000.0                # stage perspective while seen from above (px) — 20 and 21's t=0
DD = 740 * U                  # deck depth (hinge -> front lip)
K = 1236.0 / 1160.0           # straight on: lip magnification so that base width == lid width (real MacBook)
PERSP_END = round(DD * K / (K - 1), 1)   # stage perspective once straight on (tweened in 21)
LIP_H = 27 * U / K            # physical lip height (projects to 27u)
BASE_W = 1236 * U / K         # physical base width (projects to 1236u)
LID_T = 14 * U                # lid thickness
N_EDGE = 4                    # aluminium edge layers inside the lid

# ---------------------------------------------------------------- camera poses (2D cam wrapper)
HOME_L, HOME_T = 96, 226      # device box on the canvas at the identity pose (= final pose of 21)
OX, OY = HOME_L + HX, HOME_T + HY   # cam transform-origin = hinge point


def _rot(a, x, y):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return x * c - y * s, x * s + y * c


def pose(offset, target, scale, angle):
    """cam (x, y) so that the point at `offset` from the hinge point lands on `target`."""
    rx, ry = _rot(angle, *offset)
    return round(target[0] - OX - scale * rx, 2), round(target[1] - OY - scale * ry, 2)


ROT0, S0 = -24.0, 1.15        # closed lid seen from above: diagonal, close to the lens
BODY0 = -66                   # body tilt seen from above (-90 = straight down; -74 shows the front edge's thickness)


def project(y, z, beta, persp):
    """body-local point (y down, z toward the lens at rest; relative to the hinge) -> projected y offset."""
    b = math.radians(beta)
    y2, z2 = y * math.cos(b) - z * math.sin(b), y * math.sin(b) + z * math.cos(b)
    return y2 * persp / (persp - z2)


LIDC = project(-LID_T, (751 - 3) / 2 * U, BODY0, PERSP)   # projected centre of the closed lid's outer face
DISC_X, DISC_Y = 500.0, 515.0                        # on-canvas centre of the closed lid (= the play disc)
TOP = dict(zip(("x", "y"), pose((0, LIDC), (DISC_X, DISC_Y), S0, ROT0)), rotation=ROT0, scale=S0)
S1 = 1.10                     # straight on, centred
CEN = dict(zip(("x", "y"), pose((0, BOX_H / 2 - HY), (960, 520), S1, 0)), rotation=0, scale=S1)
S2 = S1 * 1.02                # slow push (<= 3 %) while the website plays
CEN2 = dict(zip(("x", "y"), pose((0, BOX_H / 2 - HY), (960, 520), S2, 0)), rotation=0, scale=S2)
LEFT = dict(x=0, y=0, rotation=0, scale=1)
PAN = 960 - (HOME_L + BOX_W / 2)   # the right column rides in with the camera's pan (velocity-matched)
LIFT = -85                    # lid hinge angle at the 20 -> 21 seam (closed = -90)

TIP_X, TIP_Y = DISC_X + 12, DISC_Y + 16      # cursor tip on the play triangle


def js(d):
    return "{ " + ", ".join("%s: %s" % (k, v) for k, v in d.items()) + " }"


def fonts(spec):
    return "\n    ".join('@font-face { font-family: "%s"; font-weight: %d; font-style: normal; src: url("assets/fonts/%s") format("woff2"); }'
                           % (fam, w, f) for fam, w, f in spec)


NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='256' height='256'%3E%3Cfilter id='n'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='7' stitchTiles='stitch'/%3E"
         "%3CfeColorMatrix values='0 0 0 1 0  0 0 0 1 0  0 0 0 1 0  0 0 0 0 0.09'/%3E%3C/filter%3E"
         "%3Crect width='256' height='256' filter='url(%23n)'/%3E%3C/svg%3E\")")


# ======================================================================== shared CSS
def mockup_css(P):
    """tools/mac_mockup.md — MacBook front view + browser chrome (prefix P)."""
    css = r"""
    /* ================= MAC MOCKUP (tools/mac_mockup.md) — MacBook Pro front view ================= */
    .fNN-mbp { --u: calc(var(--sw) / 1120); }
    .fNN-mbp {
      --sw: 896px;
      --al-0: #fbfbfc; --al-1: #e4e6ea; --al-2: #c3c7ce; --al-3: #9a9fa8; --al-4: #6f747d;
      position: absolute; width: calc(var(--u) * 1236); height: calc(var(--u) * 778);
    }
    .fNN-mbp-shadow {
      position: absolute; left: calc(var(--u) * -50); top: calc(var(--u) * 746); width: calc(var(--u) * 1336); height: calc(var(--u) * 110);
      border-radius: 50%;
      background: radial-gradient(ellipse 50% 50% at 50% 40%, rgba(3,0,30,0.72) 0%, rgba(3,0,30,0.44) 34%, rgba(3,0,30,0.14) 64%, rgba(3,0,30,0) 100%);
    }
    .fNN-mbp-occl {
      position: absolute; left: calc(var(--u) * 30); top: calc(var(--u) * 772); width: calc(var(--u) * 1176); height: calc(var(--u) * 14);
      border-radius: 50%; background: rgba(2,0,20,0.85); filter: blur(calc(var(--u) * 4));
    }
    .fNN-mbp-lid {
      position: absolute; left: calc(var(--u) * 38); top: 0; width: calc(var(--u) * 1160); height: calc(var(--u) * 754);
      border-radius: calc(var(--u) * 30) calc(var(--u) * 30) calc(var(--u) * 7) calc(var(--u) * 7);
      background: linear-gradient(180deg, var(--al-1) 0%, var(--al-2) 45%, var(--al-3) 100%);
      box-shadow: inset 0 0 0 calc(var(--u) * 0.8) rgba(255,255,255,0.55), 0 calc(var(--u) * 26) calc(var(--u) * 70) rgba(4,0,40,0.30);
    }
    .fNN-mbp-glass {
      position: absolute; left: calc(var(--u) * 4); top: calc(var(--u) * 4); width: calc(var(--u) * 1152); height: calc(var(--u) * 746);
      border-radius: calc(var(--u) * 26.5) calc(var(--u) * 26.5) calc(var(--u) * 4) calc(var(--u) * 4); overflow: hidden;
      background: radial-gradient(ellipse 80% 60% at 50% 0%, #0d0e12 0%, #050506 70%);
      box-shadow: inset 0 0 0 calc(var(--u) * 1) rgba(0,0,0,0.85);
    }
    .fNN-mbp-screen {
      position: absolute; left: calc(var(--u) * 16); top: calc(var(--u) * 16); width: calc(var(--u) * 1120); height: calc(var(--u) * 700);
      border-radius: calc(var(--u) * 10) calc(var(--u) * 10) calc(var(--u) * 1.5) calc(var(--u) * 1.5); overflow: hidden; background: #000000;
    }
    .fNN-mbp-notch {
      position: absolute; left: calc(var(--u) * 517); top: calc(var(--u) * 16); width: calc(var(--u) * 118); height: calc(var(--u) * 21);
      border-radius: 0 0 calc(var(--u) * 8) calc(var(--u) * 8); background: #050506;
    }
    .fNN-mbp-notch::before, .fNN-mbp-notch::after { content: ""; position: absolute; top: 0; width: calc(var(--u) * 6); height: calc(var(--u) * 6); }
    .fNN-mbp-notch::before { left: calc(var(--u) * -6); background: radial-gradient(circle at 0% 100%, rgba(5,5,6,0) calc(var(--u) * 5.5), #050506 calc(var(--u) * 6)); }
    .fNN-mbp-notch::after { right: calc(var(--u) * -6); background: radial-gradient(circle at 100% 100%, rgba(5,5,6,0) calc(var(--u) * 5.5), #050506 calc(var(--u) * 6)); }
    .fNN-mbp-lens {
      position: absolute; left: calc(var(--u) * 55.5); top: calc(var(--u) * 7); width: calc(var(--u) * 7); height: calc(var(--u) * 7); border-radius: 50%;
      background: radial-gradient(circle at 38% 34%, #4a5a8c 0%, #1a2142 38%, #0a0b14 72%);
      box-shadow: 0 0 0 calc(var(--u) * 1.2) #111217;
    }
    .fNN-mbp-reflect {
      position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none;
      background: linear-gradient(121deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.035) 30%, rgba(255,255,255,0.016) 40.5%, rgba(255,255,255,0) 42%, rgba(255,255,255,0) 100%);
    }
    .fNN-mbp-base {
      position: absolute; left: 0; top: calc(var(--u) * 751); width: calc(var(--u) * 1236); height: calc(var(--u) * 27);
      border-radius: calc(var(--u) * 4) calc(var(--u) * 4) calc(var(--u) * 70) calc(var(--u) * 70) / calc(var(--u) * 3) calc(var(--u) * 3) calc(var(--u) * 24) calc(var(--u) * 24);
      background: linear-gradient(180deg, var(--al-0) 0%, var(--al-1) 12%, var(--al-2) 44%, var(--al-3) 76%, var(--al-4) 100%);
      box-shadow: inset 0 calc(var(--u) * -1.2) calc(var(--u) * 1.5) rgba(0,0,0,0.22), inset 0 calc(var(--u) * 0.8) 0 rgba(255,255,255,0.7);
    }
    .fNN-mbp-thumb {
      position: absolute; left: calc(var(--u) * 538); top: 0; width: calc(var(--u) * 160); height: calc(var(--u) * 8);
      border-radius: 0 0 50% 50% / 0 0 100% 100%;
      background: linear-gradient(180deg, var(--al-3) 0%, var(--al-2) 55%, var(--al-1) 100%);
      box-shadow: inset 0 calc(var(--u) * 1.6) calc(var(--u) * 2.2) rgba(0,0,0,0.30), 0 calc(var(--u) * 0.6) 0 rgba(255,255,255,0.45);
    }
"""
    return css.replace("fNN", P)


def chrome_css(P):
    css = r"""
    /* browser chrome: tab strip 36u + toolbar 34u = 70u; content 1120u x 630u = 16:9 */
    .fNN-chrome { position: absolute; left: 0; top: 0; width: calc(var(--u) * 1120); height: calc(var(--u) * 70); font-family: "Inter", sans-serif; }
    .fNN-tabs { position: absolute; left: 0; top: 0; width: 100%; height: calc(var(--u) * 36); background: #DEE1E6; }
    .fNN-tl { position: absolute; top: calc(var(--u) * 12); width: calc(var(--u) * 12); height: calc(var(--u) * 12); border-radius: 50%; }
    .fNN-tl-r { left: calc(var(--u) * 13); background: #FF5F57; box-shadow: inset 0 0 0 calc(var(--u) * 0.6) #E0443E; }
    .fNN-tl-y { left: calc(var(--u) * 33); background: #FEBC2E; box-shadow: inset 0 0 0 calc(var(--u) * 0.6) #DEA123; }
    .fNN-tl-g { left: calc(var(--u) * 53); background: #28C840; box-shadow: inset 0 0 0 calc(var(--u) * 0.6) #1AAB29; }
    .fNN-tab {
      position: absolute; left: calc(var(--u) * 82); top: calc(var(--u) * 7); width: calc(var(--u) * 232); height: calc(var(--u) * 29);
      border-radius: calc(var(--u) * 9) calc(var(--u) * 9) 0 0; background: #FFFFFF;
    }
    .fNN-tab::before, .fNN-tab::after { content: ""; position: absolute; bottom: 0; width: calc(var(--u) * 9); height: calc(var(--u) * 9); }
    .fNN-tab::before { left: calc(var(--u) * -9); background: radial-gradient(circle at 0% 0%, rgba(255,255,255,0) calc(var(--u) * 8.6), #FFFFFF calc(var(--u) * 9)); }
    .fNN-tab::after { right: calc(var(--u) * -9); background: radial-gradient(circle at 100% 0%, rgba(255,255,255,0) calc(var(--u) * 8.6), #FFFFFF calc(var(--u) * 9)); }
    .fNN-fav {
      position: absolute; left: calc(var(--u) * 12); top: calc(var(--u) * 7); width: calc(var(--u) * 15); height: calc(var(--u) * 15);
      border-radius: calc(var(--u) * 3.5); overflow: hidden; background: radial-gradient(circle at 50% 45%, #2fb6f2 0%, #0b6df0 80%);
    }
    .fNN-fav img { position: absolute; left: calc(var(--u) * 1.2); top: calc(var(--u) * 5.2); width: calc(var(--u) * 12.6); height: auto; display: block; }
    .fNN-tab-t {
      position: absolute; left: calc(var(--u) * 35); top: 0; height: calc(var(--u) * 29); line-height: calc(var(--u) * 29);
      font-size: calc(var(--u) * 12); font-weight: 500; color: #202124; white-space: nowrap;
    }
    .fNN-tab-x { position: absolute; right: calc(var(--u) * 10); top: calc(var(--u) * 9.5); width: calc(var(--u) * 10); height: calc(var(--u) * 10); }
    .fNN-plus { position: absolute; left: calc(var(--u) * 330); top: calc(var(--u) * 11); width: calc(var(--u) * 14); height: calc(var(--u) * 14); }
    .fNN-bar { position: absolute; left: 0; top: calc(var(--u) * 36); width: 100%; height: calc(var(--u) * 34); background: #FFFFFF; box-shadow: inset 0 calc(var(--u) * -1) 0 #DADCE0; }
    .fNN-nav { position: absolute; left: calc(var(--u) * 14); top: calc(var(--u) * 9); width: calc(var(--u) * 86); height: calc(var(--u) * 16); overflow: visible; }
    .fNN-menu { position: absolute; left: calc(var(--u) * 1086); top: calc(var(--u) * 9); width: calc(var(--u) * 16); height: calc(var(--u) * 16); }
    .fNN-url {
      position: absolute; left: calc(var(--u) * 102); top: calc(var(--u) * 4); width: calc(var(--u) * 962); height: calc(var(--u) * 26);
      border-radius: calc(var(--u) * 13); background: #F1F3F4;
    }
    .fNN-lock { position: absolute; left: calc(var(--u) * 12); top: calc(var(--u) * 6.5); width: calc(var(--u) * 13); height: calc(var(--u) * 13); }
    .fNN-url-t {
      position: absolute; left: calc(var(--u) * 33); top: 0; height: calc(var(--u) * 26); line-height: calc(var(--u) * 26);
      font-size: calc(var(--u) * 13); font-weight: 500; color: #202124; white-space: nowrap;
    }
    .fNN-star { position: absolute; right: calc(var(--u) * 11); top: calc(var(--u) * 6); width: calc(var(--u) * 14); height: calc(var(--u) * 14); }
    .fNN-content { position: absolute; left: 0; top: calc(var(--u) * 70); width: calc(var(--u) * 1120); height: calc(var(--u) * 630); overflow: hidden; background: #FFFFFF; }
    .fNN-media { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: var(--fx, 50%) 50%; display: block; }
"""
    return css.replace("fNN", P)


def rig_css(P):
    edge_r = "%.1fpx %.1fpx %.1fpx %.1fpx" % (30 * U, 30 * U, 16 * U, 16 * U)
    return f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Poppins", sans-serif; }}

    /* ---------- ground: NAWAR BLUE + dots + vignette ---------- */
    #{P}-ground {{ position: absolute; inset: 0; overflow: hidden; background: radial-gradient(circle at 50% 46%, #025dc7 0%, #120081 72%); }}
    #{P}-dots {{
      position: absolute; inset: 0;
      background-image: radial-gradient(circle, rgba(255,255,255,0.07) 1.6px, transparent 1.7px);
      background-size: 28px 28px; background-position: 14px 14px;
    }}
    #{P}-vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse 72% 70% at 50% 46%, rgba(4,0,40,0) 52%, rgba(4,0,40,0.42) 100%); }}

    /* ---------- 2D cam > perspective stage (= device box) > 3D body ---------- */
    #{P}-cam {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: {OX:.1f}px {OY:.1f}px; }}
    #{P}-stage {{ left: {HOME_L}px; top: {HOME_T}px; perspective: {PERSP:.0f}px; perspective-origin: {HX:.1f}px {HY:.1f}px; }}
    #{P}-body {{ position: absolute; left: 0; top: 0; width: {BOX_W:.1f}px; height: {BOX_H:.1f}px; transform-style: preserve-3d; transform-origin: {HX:.1f}px {HY:.1f}px; }}
    /* the table under the closed laptop (only seen from above) */
    #{P}-tsp {{ position: absolute; left: {LID_L:.1f}px; top: {HY + LIP_H:.1f}px; width: {LID_W:.1f}px; height: {LID_H:.1f}px; transform-origin: 50% 0; transform: rotateX(90deg); }}
    #{P}-tsh {{
      position: absolute; left: 10px; top: 4px; width: {LID_W - 20:.1f}px; height: {LID_H - 14:.1f}px; border-radius: 40px;
      background: rgba(3,0,30,0.55);
      box-shadow: -14px 30px 60px 10px rgba(3,0,30,0.50), -4px 10px 18px 2px rgba(3,0,30,0.45);
    }}
    /* the base: deck top (dark, keyless — edge-on when straight on) + the front lip */
    #{P}-deck {{
      position: absolute; left: {(BOX_W - BASE_W) / 2:.1f}px; top: {HY - 14:.1f}px; width: {BASE_W:.1f}px; height: {DD + 14:.1f}px;
      transform-origin: 50% 14px; transform: rotateX(90deg); border-radius: 6px 6px 22px 22px;
      background: linear-gradient(180deg, #121318 0%, #1c1e24 70%, #2a2d34 100%);
    }}
    #{P}-lipw {{ position: absolute; left: 0; top: 0; width: {BOX_W:.1f}px; height: {BOX_H:.1f}px; transform-origin: {HX:.1f}px {HY:.1f}px; transform: translateZ({DD:.1f}px) scale({1 / K:.5f}); }}
    /* the lid: hinge = (580u, 751u); front face = the mockup lid, back = silver aluminium, no logo */
    #{P}-lid {{ position: absolute; left: {LID_L:.1f}px; top: 0; width: {LID_W:.1f}px; height: {LID_H:.1f}px; transform-style: preserve-3d; transform-origin: {LID_W / 2:.1f}px {751 * U:.1f}px; }}
    #{P}-lidf {{ left: 0; backface-visibility: hidden; }}
    .{P}-edge {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: {edge_r}; background: #a3a8b0; }}
    #{P}-lido {{
      position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: {edge_r}; overflow: hidden;
      transform: translateZ(-{LID_T:.1f}px) rotateY(180deg); backface-visibility: hidden;
      background: {NOISE}, radial-gradient(ellipse 120% 95% at 70% 82%, #f4f5f7 0%, #e3e5e9 40%, #cdd0d6 76%, #b8bcc4 100%);
      box-shadow: inset -2px -2px 0 rgba(255,255,255,0.90), inset 2px 2px 0 rgba(110,116,128,0.40), inset 0 0 0 1px rgba(255,255,255,0.45),
        inset -5px -5px 10px rgba(255,255,255,0.35), inset 0 0 46px rgba(30,70,190,0.18);
    }}
    /* soft studio reflection: one broad band + a faint second one */
    #{P}-lidr {{
      position: absolute; left: 0; top: 0; width: 100%; height: 100%;
      background: linear-gradient(302deg, rgba(255,255,255,0) 22%, rgba(255,255,255,0.34) 36%, rgba(255,255,255,0.10) 47%, rgba(255,255,255,0) 58%, rgba(255,255,255,0) 72%, rgba(255,255,255,0.12) 78%, rgba(255,255,255,0) 84%);
    }}
    /* the black display hinge seen along the back edge */
    #{P}-hinge {{ position: absolute; left: {110 * U:.1f}px; top: {LID_H - 9 * U:.1f}px; width: {LID_W - 220 * U:.1f}px; height: {9 * U:.1f}px; border-radius: {4 * U:.1f}px; background: linear-gradient(180deg, #34363c 0%, #18191d 100%); }}
"""


def ui_css(P):
    """player chrome (paused): scrim, play disc, cursor, control bar — shared so the seam matches."""
    return f"""
    #{P}-scrim {{ position: absolute; inset: 0; background: radial-gradient(ellipse 80% 80% at 44% 48%, rgba(4,0,40,0.08) 0%, rgba(4,0,40,0.22) 50%, rgba(3,0,30,0.58) 100%); }}
    #{P}-disc {{ position: absolute; left: {DISC_X - 80:.0f}px; top: {DISC_Y - 80:.0f}px; width: 160px; height: 160px; }}
    #{P}-discb {{
      position: absolute; inset: 0; border-radius: 50%;
      background: linear-gradient(180deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.03) 55%), rgba(10,10,32,0.50);
      box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.40), 0 18px 44px rgba(2,0,24,0.40);
    }}
    #{P}-dpress {{ position: absolute; inset: 0; border-radius: 50%; background: rgba(2,0,20,0.35); opacity: 0; }}
    .{P}-dico {{ position: absolute; left: 0; top: 0; width: 160px; height: 160px; display: block; }}
    #{P}-cursor {{ position: absolute; left: {TIP_X - 3:.0f}px; top: {TIP_Y - 3:.0f}px; width: 30px; height: 46px; }}
    #{P}-cursori {{ position: absolute; left: 0; top: 0; width: 30px; height: 46px; transform-origin: 3px 3px; filter: drop-shadow(0 3px 5px rgba(0,0,0,0.40)); }}
    #{P}-ctl {{
      position: absolute; left: 96px; top: 908px; width: 1728px; height: 64px; box-sizing: border-box;
      display: flex; align-items: center; gap: 28px; padding: 0 30px; border-radius: 18px;
      background: rgba(10,8,34,0.62); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.14), 0 16px 40px rgba(3,0,28,0.30);
      font-family: "Inter", sans-serif;
    }}
    .{P}-ic {{ position: relative; width: 26px; height: 26px; flex: 0 0 26px; }}
    .{P}-ic svg {{ position: absolute; left: 0; top: 0; width: 26px; height: 26px; display: block; }}
    #{P}-time {{ font-weight: 600; font-size: 22px; line-height: 1; color: rgba(255,255,255,0.80); white-space: nowrap; font-variant-numeric: tabular-nums; }}
    #{P}-track {{ position: relative; flex: 1 1 auto; height: 5px; border-radius: 3px; background: rgba(255,255,255,0.26); }}
    #{P}-fill {{ position: absolute; left: 0; top: 0; width: {PLAYER_PCT}; height: 5px; border-radius: 3px; background: #FFFFFF; }}
    #{P}-knob {{ position: absolute; left: {PLAYER_PCT}; top: 2.5px; width: 16px; height: 16px; margin: -8px 0 0 -8px; border-radius: 50%; background: #FFFFFF; box-shadow: 0 2px 6px rgba(0,0,0,0.35); }}
"""


# ======================================================================== shared markup
EDGE_LAYERS = [round(-LID_T * (i + 1) / (N_EDGE + 1), 2) for i in range(N_EDGE)]


def rig_html(P, screen_inner):
    edges = "".join('<div class="%s-edge" style="transform: translateZ(%.2fpx);"></div>' % (P, z) for z in EDGE_LAYERS)
    return f"""    <div id="{P}-cam">
      <div id="{P}-stage" class="{P}-mbp">
        <div id="{P}-csh" class="{P}-mbp-shadow"></div><div id="{P}-coc" class="{P}-mbp-occl"></div>
        <div id="{P}-body">
          <div id="{P}-tsp"><div id="{P}-tsh"></div></div>
          <div id="{P}-deck"></div>
          <div id="{P}-lipw"><div class="{P}-mbp-base"><div class="{P}-mbp-thumb"></div></div></div>
          <div id="{P}-lid">
            <div id="{P}-lido"><div id="{P}-lidr"></div><div id="{P}-hinge"></div></div>
            {edges}
            <div id="{P}-lidf" class="{P}-mbp-lid">
              <div class="{P}-mbp-glass">
                <div class="{P}-mbp-screen">
{screen_inner}
                </div>
                <div class="{P}-mbp-notch"><i class="{P}-mbp-lens"></i></div>
                <div class="{P}-mbp-reflect"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>"""


def ground_html(P, dur):
    return f"""    <div id="{P}-ground" class="clip" data-start="0" data-duration="{dur}" data-track-index="0"><div id="{P}-dots"></div><div id="{P}-vig"></div></div>"""


CURSOR_SVG = ('<svg viewBox="0 0 30 46" width="30" height="46" style="display:block; overflow:visible;" aria-hidden="true">'
              '<path d="M 2.5 2.5 L 2.5 34 L 10 26.6 L 15 38.6 L 20.4 36.4 L 15.5 24.6 L 26 24.6 Z" fill="#0C0C10" stroke="#FFFFFF" stroke-width="2.2" stroke-linejoin="round"></path></svg>')
PLAY_SVG = '<path d="M 66 52 L 66 108 Q 66 115 72.5 111.4 L 114 85.6 Q 119.5 80 114 74.4 L 72.5 48.6 Q 66 45 66 52 Z" fill="#FFFFFF"></path>'
PAUSE_SVG = '<rect x="58" y="52" width="15" height="56" rx="4" fill="#FFFFFF"></rect><rect x="87" y="52" width="15" height="56" rx="4" fill="#FFFFFF"></rect>'


def ui_html(P):
    return f"""    <div id="{P}-scrim"></div>
    <div id="{P}-disc"><div id="{P}-discb"></div><div id="{P}-dpress"></div>
      <svg id="{P}-dpause" class="{P}-dico" viewBox="0 0 160 160" aria-hidden="true">{PAUSE_SVG}</svg>
      <svg id="{P}-dplay" class="{P}-dico" viewBox="0 0 160 160" aria-hidden="true">{PLAY_SVG}</svg></div>
    <div id="{P}-ctl">
      <div class="{P}-ic"><svg id="{P}-bplay" viewBox="0 0 26 26" aria-hidden="true"><path d="M 7 4.2 L 7 21.8 Q 7 23.8 8.8 22.8 L 22.2 14.4 Q 23.8 13 22.2 11.6 L 8.8 3.2 Q 7 2.2 7 4.2 Z" fill="#FFFFFF"></path></svg>
        <svg id="{P}-bpause" viewBox="0 0 26 26" aria-hidden="true"><rect x="5.5" y="4" width="5.5" height="18" rx="1.6" fill="#FFFFFF"></rect><rect x="15" y="4" width="5.5" height="18" rx="1.6" fill="#FFFFFF"></rect></svg></div>
      <div id="{P}-time">{PLAYER_TIME}</div>
      <div id="{P}-track"><div id="{P}-fill"></div><div id="{P}-knob"></div></div>
      <div class="{P}-ic"><svg viewBox="0 0 26 26" aria-hidden="true"><path d="M 3.5 9.5 L 7.8 9.5 L 13 4.8 L 13 21.2 L 7.8 16.5 L 3.5 16.5 Z" fill="#FFFFFF"></path><path d="M 17 9 Q 19.8 13 17 17 M 19.8 6.2 Q 24.6 13 19.8 19.8" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"></path></svg></div>
      <div class="{P}-ic"><svg viewBox="0 0 26 26" aria-hidden="true"><path d="M 4 9.5 L 4 4 L 9.5 4 M 16.5 4 L 22 4 L 22 9.5 M 22 16.5 L 22 22 L 16.5 22 M 9.5 22 L 4 22 L 4 16.5" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"></path></svg></div>
    </div>
    <div id="{P}-cursor"><div id="{P}-cursori">{CURSOR_SVG}</div></div>"""


def init_js(P, el, props):
    """initial state rendered at t=0 (a tl.set at 0 is not rendered when the renderer seeks exactly 0)."""
    d = js(props)
    return f'      tl.fromTo($("{P}-{el}"), {d}, {{ {d[2:-2]}, duration: 0.001 }}, 0);\n'


def rig_state_js(P, cam, body, lid):
    return init_js(P, "cam", cam) + init_js(P, "body", {"rotationX": body}) + init_js(P, "lid", {"rotationX": lid})


# ======================================================================== FRAME 20
def frame20():
    P = "f20"
    CUR0 = round(W20[4]["end"] + 0.018, 3)       # the cursor sets off as «dentro?» ends
    PRESS = round(W20[7]["end"] + 0.011, 3)      # ... and presses play as «enseño.» ends
    LIFT_T = PRESS + 0.10                        # the lid starts to lift
    css = fonts([("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 800, "poppins-latin-800-normal.woff2"),
                 ("Inter", 600, "inter-latin-600-normal.woff2")])
    css += rig_css(P) + mockup_css(P) + ui_css(P)
    css += f"""
    /* ---------- the question (right column, on the blue) ---------- */
    #{P}-q {{ position: absolute; left: 1232px; top: 300px; width: 620px; }}
    .{P}-line {{ position: absolute; left: 0; white-space: nowrap; }}
    .{P}-w {{ display: inline-block; }}
    .{P}-w + .{P}-w {{ margin-left: 0.25em; }}
    .{P}-lead {{ font-weight: 600; font-size: 44px; line-height: 1.2; letter-spacing: -0.01em; color: rgba(255,255,255,0.72); }}
    .{P}-h {{ font-weight: 800; font-size: 96px; line-height: 1.04; letter-spacing: -0.03em; color: #FFFFFF; }}
    #{P}-dentro {{ color: #4da3ff; }}
"""
    screen_inner = ""
    html = f"""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    {css.strip()}
  </style>

  <div id="root" data-composition-id="20-pausa" data-width="1920" data-height="1080" data-duration="{D20}">
{ground_html(P, D20)}
{rig_html(P, screen_inner)}
{ui_html(P)}
    <div id="{P}-q">
      <div class="{P}-line" style="top: 0;"><span id="{P}-w0" class="{P}-w {P}-lead">Vale,</span></div>
      <div class="{P}-line" style="top: 70px;"><span id="{P}-w1" class="{P}-w {P}-h">¿Y</span> <span id="{P}-w2" class="{P}-w {P}-h">qué</span> <span id="{P}-w3" class="{P}-w {P}-h">hay</span></div>
      <div class="{P}-line" style="top: 170px;"><span id="{P}-dentro" class="{P}-w {P}-h">dentro?</span></div>
      <div class="{P}-line" style="top: 310px;"><span id="{P}-w5" class="{P}-w {P}-lead">Te</span> <span id="{P}-w6" class="{P}-w {P}-lead">lo</span> <span id="{P}-w7" class="{P}-w {P}-lead">enseño.</span></div>
    </div>
  </div>

  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const $ = (id) => document.getElementById(id);

      // the frozen frame: closed MacBook seen from above, diagonal (shared rig state with 21's t=0)
{rig_state_js(P, TOP, BODY0, -90)}
      // ===== Scene 1 (0.0-0.5): the film PAUSES — scrim settles, pause flash in the disc, controls rise =====
      tl.fromTo($("{P}-scrim"), {{ opacity: 0.35 }}, {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, 0);
      tl.fromTo($("{P}-disc"), {{ opacity: 0, scale: 1.14 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }}, 0);
      tl.fromTo($("{P}-dpause"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.1, ease: "power1.in" }}, 0.3);
      tl.fromTo($("{P}-dplay"), {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "power2.out" }}, 0.4);
      tl.fromTo($("{P}-ctl"), {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }}, 0.02);
{init_js(P, "bpause", {"opacity": 0})}{init_js(P, "dpress", {"opacity": 0})}
      // ===== Scene 2 (0.5-1.9): Vale, / ¿Y qué hay / dentro? on the voice =====
      [["{P}-w0", {cue(W20, 0)}], ["{P}-w1", {cue(W20, 1)}], ["{P}-w2", {cue(W20, 2)}], ["{P}-w3", {cue(W20, 3)}], ["{P}-dentro", {cue(W20, 4)}]].forEach(([id, t]) => {{
        tl.fromTo($(id), {{ opacity: 0, y: 28 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, t);
      }});

      // ===== Scene 3 (1.9-2.81): Te lo enseño. + the cursor presses play; the lid starts to lift =====
      [["{P}-w5", {cue(W20, 5)}], ["{P}-w6", {cue(W20, 6)}], ["{P}-w7", {cue(W20, 7)}]].forEach(([id, t]) => {{
        tl.fromTo($(id), {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.26, ease: "power2.out" }}, t);
      }});
      tl.fromTo($("{P}-cursor"), {{ x: 1000, y: 640 }}, {{ x: 0, y: 0, duration: {PRESS - 0.06 - CUR0:.3f}, ease: "power2.inOut" }}, {CUR0});
      tl.fromTo($("{P}-cursori"), {{ scale: 1 }}, {{ scale: 0.86, duration: 0.05, ease: "power2.out" }}, {PRESS});
      tl.to($("{P}-cursori"), {{ scale: 1, duration: 0.1, ease: "power2.out" }}, {PRESS + 0.08:.3f});
      tl.fromTo($("{P}-dpress"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, ease: "power2.out", immediateRender: false }}, {PRESS});
      tl.fromTo($("{P}-disc"), {{ scale: 1 }}, {{ scale: 0.95, duration: 0.05, ease: "power2.out", immediateRender: false }}, {PRESS});
      tl.to($("{P}-disc"), {{ scale: 1, duration: 0.12, ease: "power2.out" }}, {PRESS + 0.08:.3f});
      tl.set($("{P}-bplay"), {{ opacity: 0 }}, {PRESS + 0.06:.3f});
      tl.set($("{P}-bpause"), {{ opacity: 1 }}, {PRESS + 0.06:.3f});
      tl.fromTo($("{P}-lid"), {{ rotationX: -90 }}, {{ rotationX: {LIFT}, duration: {D20 - LIFT_T:.3f}, ease: "power2.in", immediateRender: false }}, {LIFT_T:.3f});

      window.__timelines["20-pausa"] = tl;
    }})();
  </script>
</template>
"""
    return html


# ======================================================================== FRAME 21
def frame21():
    P = "f21"
    PAN_T = cue(W21, 0, 0.023)                  # the camera pans as «Dieciséis» starts
    css = fonts([("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 800, "poppins-latin-800-normal.woff2"),
                 ("Poppins", 900, "poppins-latin-900-normal.woff2"), ("Inter", 500, "inter-latin-500-normal.woff2"),
                 ("Inter", 600, "inter-latin-600-normal.woff2")])
    css += rig_css(P) + mockup_css(P) + chrome_css(P) + ui_css(P)
    css += f"""
    /* ---------- screen: the browser (website, then the course page) ---------- */
    #{P}-browser {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; background: #FFFFFF; }}
    #{P}-url2 {{ opacity: 0; }}

    /* ---------- right column: 16 / semanas / de formación guiada ---------- */
    #{P}-col {{ position: absolute; left: 1176px; top: 262px; width: 664px; height: 560px; }}
    #{P}-num {{ position: absolute; left: -12px; top: 0; font-weight: 900; font-size: 250px; line-height: 1; letter-spacing: -0.05em; color: #FFFFFF; white-space: nowrap; }}
    #{P}-sem {{ position: absolute; left: 0; top: 252px; font-weight: 800; font-size: 96px; line-height: 1.04; letter-spacing: -0.03em; color: #FFFFFF; white-space: nowrap; }}
    #{P}-pills {{ position: absolute; left: 0; top: 386px; width: 664px; height: 10px; }}
    .{P}-pill {{ position: absolute; top: 0; width: 34px; height: 10px; border-radius: 5px; background: rgba(255,255,255,0.18); overflow: hidden; }}
    .{P}-pf {{ position: absolute; left: 0; top: 0; width: 34px; height: 10px; border-radius: 5px; background: #4da3ff; transform-origin: 0% 50%; }}
    #{P}-sub {{ position: absolute; left: 0; top: 424px; white-space: nowrap; }}
    .{P}-lead {{ display: inline-block; font-weight: 600; font-size: 44px; line-height: 1.2; letter-spacing: -0.01em; color: rgba(255,255,255,0.72); }}
    .{P}-lead + .{P}-lead {{ margin-left: 0.25em; }}
    #{P}-guiada {{ color: #4da3ff; }}
"""
    screen_inner = f"""                  <div id="{P}-browser">
                    <div class="{P}-chrome">
                      <div class="{P}-tabs"><i class="{P}-tl {P}-tl-r"></i><i class="{P}-tl {P}-tl-y"></i><i class="{P}-tl {P}-tl-g"></i>
                        <div class="{P}-tab"><div class="{P}-fav"><img src="assets/img/logo-nawar.png" alt="" /></div><div class="{P}-tab-t">Holandés Nawar</div><svg class="{P}-tab-x" viewBox="0 0 10 10" aria-hidden="true"><path d="M2.2 2.2 L7.8 7.8 M7.8 2.2 L2.2 7.8" fill="none" stroke="#5F6368" stroke-width="1.3" stroke-linecap="round" /></svg></div>
                        <svg class="{P}-plus" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 2.2 V11.8 M2.2 7 H11.8" fill="none" stroke="#5F6368" stroke-width="1.4" stroke-linecap="round" /></svg></div>
                      <div class="{P}-bar"><svg class="{P}-nav" viewBox="0 0 86 16" aria-hidden="true"><g fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13 8 H3.4 M7.8 3.6 L3.4 8 L7.8 12.4" stroke="#5F6368" /><path d="M31 8 H40.6 M36.2 3.6 L40.6 8 L36.2 12.4" stroke="#BDC1C6" /><path d="M68.7 8.6 A4.8 4.8 0 1 1 67.3 4.5 M68 1.9 V5.1 H64.8" stroke="#5F6368" /></g></svg>
                        <div class="{P}-url"><svg class="{P}-lock" viewBox="0 0 13 13" aria-hidden="true"><path d="M4.3 6 V4.3 A2.2 2.2 0 0 1 8.7 4.3 V6" fill="none" stroke="#5F6368" stroke-width="1.3" /><rect x="2.6" y="5.8" width="7.8" height="5.9" rx="1.3" fill="#5F6368" /></svg><div id="{P}-url1" class="{P}-url-t">holandesnawar.com</div><div id="{P}-url2" class="{P}-url-t">app.holandesnawar.com</div><svg class="{P}-star" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1.8 L8.55 5.05 L12.1 5.5 L9.5 7.95 L10.15 11.5 L7 9.8 L3.85 11.5 L4.5 7.95 L1.9 5.5 L5.45 5.05 Z" fill="none" stroke="#5F6368" stroke-width="1.1" stroke-linejoin="round" /></svg></div>
                        <svg class="{P}-menu" viewBox="0 0 16 16" aria-hidden="true"><g fill="#5F6368"><circle cx="8" cy="3.4" r="1.35" /><circle cx="8" cy="8" r="1.35" /><circle cx="8" cy="12.6" r="1.35" /></g></svg></div>
                    </div>
                    <div class="{P}-content" style="--fx:50%;">
                      <video id="{P}-vid1" class="clip {P}-media" src="assets/video/nuestra-vision-hero.mp4" muted playsinline data-start="0" data-duration="{SWITCH}" data-media-start="0" data-hf-media-start-basis="local" data-track-index="2"></video>
                      <video id="{P}-vid2" class="clip {P}-media" src="assets/video/formacion-134.mp4" muted playsinline data-start="{SWITCH}" data-duration="{D21 - SWITCH:.3f}" data-media-start="0" data-hf-media-start-basis="local" data-track-index="2"></video>
                    </div>
                  </div>"""
    pills = "".join('<div class="%s-pill" style="left: %dpx;"><div id="%s-pf%d" class="%s-pf"></div></div>' % (P, i * 42, P, i, P) for i in range(16))
    html = f"""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    {css.strip()}
  </style>

  <div id="root" data-composition-id="21-portatil" data-width="1920" data-height="1080" data-duration="{D21}">
{ground_html(P, D21)}
{rig_html(P, screen_inner)}
{ui_html(P)}
    <div id="{P}-col">
      <div id="{P}-num">16</div>
      <div id="{P}-sem">semanas</div>
      <div id="{P}-pills">{pills}</div>
      <div id="{P}-sub"><span id="{P}-w3" class="{P}-lead">de</span> <span id="{P}-w4" class="{P}-lead">formación</span> <span id="{P}-guiada" class="{P}-lead">guiada</span></div>
    </div>
  </div>

  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const $ = (id) => document.getElementById(id);

      // seam: identical to the last frame of 20-pausa (lid lifted {LIFT + 90} deg, play pressed)
{rig_state_js(P, TOP, BODY0, LIFT)}{init_js(P, "bplay", {"opacity": 0})}{init_js(P, "dpause", {"opacity": 0})}
      // ===== Scene 1 (0.0-1.0): THE DROP — the player hides, the camera cranes down, the lid swings open =====
      tl.fromTo($("{P}-scrim"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.6, ease: "power2.out" }}, 0);
      tl.fromTo($("{P}-disc"), {{ opacity: 1, scale: 1 }}, {{ opacity: 0, scale: 1.1, duration: 0.18, ease: "power2.out" }}, 0);
      tl.fromTo($("{P}-dpress"), {{ opacity: 1 }}, {{ opacity: 1, duration: 0.01 }}, 0);
      tl.fromTo($("{P}-cursor"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.16, ease: "power1.out" }}, 0);
      tl.fromTo($("{P}-ctl"), {{ opacity: 1, y: 0 }}, {{ opacity: 0, y: 36, duration: 0.3, ease: "power2.in" }}, 0);
      // camera: from above (diagonal, close) to straight on, centred
      tl.fromTo($("{P}-cam"), {js(TOP)}, {{ {js(CEN)[2:-2]}, duration: 1.05, ease: "power3.out" }}, 0);
      // body: top view -> deck height (reaches the deck plane before the lid is more than a few degrees open)
      tl.fromTo($("{P}-body"), {{ rotationX: {BODY0} }}, {{ rotationX: 0, duration: 0.5, ease: "power3.out" }}, 0);
      // lid: swings up about the hinge, ends straight on
      tl.fromTo($("{P}-lid"), {{ rotationX: {LIFT} }}, {{ rotationX: 0, duration: 0.92, ease: "power2.inOut" }}, 0.06);
      tl.fromTo($("{P}-stage"), {{ perspective: {PERSP:.0f} }}, {{ perspective: {PERSP_END}, duration: 1.0, ease: "power2.inOut" }}, 0);
      // shadows: the table shadow (seen from above) hands over to the mockup's contact shadow
      tl.fromTo($("{P}-tsp"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, ease: "power1.in" }}, 0.05);
      tl.fromTo([$("{P}-csh"), $("{P}-coc")], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.55, ease: "power2.out" }}, 0.4);

      // ===== Scene 2 (1.05-SWITCH): the website plays while the camera pushes in slowly =====
      tl.fromTo($("{P}-cam"), {js(CEN)}, {{ {js(CEN2)[2:-2]}, duration: {PAN_T + 0.02 - 1.05:.3f}, ease: "sine.inOut", immediateRender: false }}, 1.05);

      // ===== Scene 3 (SWITCH): the browser navigates to the course page =====
      tl.set($("{P}-url1"), {{ opacity: 0 }}, {SWITCH});
      tl.set($("{P}-url2"), {{ opacity: 1 }}, {SWITCH});

      // ===== Scene 4 (voice back): the Mac glides left; 16 semanas de formación guiada =====
      tl.fromTo($("{P}-cam"), {js(CEN2)}, {{ x: 0, y: 0, rotation: 0, scale: 1, duration: 0.8, ease: "power3.inOut", immediateRender: false }}, {PAN_T});
      tl.fromTo($("{P}-col"), {{ x: {PAN:.1f} }}, {{ x: 0, duration: 0.8, ease: "power3.inOut" }}, {PAN_T});
      tl.fromTo($("{P}-num"), {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {cue(W21, 0, 0.013)});
      tl.fromTo($("{P}-sem"), {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }}, {cue(W21, 1, 0.023)});
      tl.fromTo($("{P}-w3"), {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.26, ease: "power2.out" }}, {cue(W21, 2, 0.025)});
      tl.fromTo($("{P}-w4"), {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.26, ease: "power2.out" }}, {cue(W21, 3, 0.017)});
      tl.fromTo($("{P}-guiada"), {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.28, ease: "power2.out" }}, {cue(W21, 4, 0.021)});
      tl.fromTo($("{P}-pills"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power1.out" }}, {cue(W21, 1, -0.007)});
      for (let i = 0; i < 16; i++) {{
        tl.fromTo($("{P}-pf" + i), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.14, ease: "power2.out" }}, {cue(W21, 1, -0.067)} + i * 0.054);
      }}

      window.__timelines["21-portatil"] = tl;
    }})();
  </script>
</template>
"""
    return html


SFX20 = [{"t": 0.0, "sfx": "click-soft", "volume": 0.2}, {"t": 2.52, "sfx": "click", "volume": 0.25}]
SFX21 = [{"t": 0.0, "sfx": "whoosh", "volume": 0.18}]

if __name__ == "__main__":
    for name, body in (("20-pausa.html", frame20()), ("21-portatil.html", frame21())):
        open(os.path.join(OUT, name), "w").write(body.strip() + "\n")
    json.dump(SFX20, open(os.path.join(OUT, "20-pausa.sfx.json"), "w"), indent=2)
    json.dump(SFX21, open(os.path.join(OUT, "21-portatil.sfx.json"), "w"), indent=2)
    print("ok  TOP", TOP, " CEN", CEN, " P_END", PERSP_END, " lip %.1fx%.2f" % (BASE_W, LIP_H))
