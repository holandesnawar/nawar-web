"""ins-04 · «(En Nawar practicas) con situaciones que vas a vivir en el día a día. Nada de la teoría que luego no
usas.» — the VSL's icon tile, four times: a 2×2 grid of real-life situations (de huisarts · de supermarkt ·
het werk · de gemeente, each with its Spanish gloss) pops on «situaciones». On «nada de la teoría» the grid eases up
and a dull grey «Teoría que no usas» card (a grammar-table skeleton) slides in under it; on «no usas» a red strike
runs through its label (house strike-through, as «tipo test» / «Werkt jij?») the card stays solid and legible."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


# line icons on a 240 box (VSL icon tile: indigo strokes, one blue accent, a light blue fill)
TILE_ICONS = {
    "huisarts": """
        <path class="i4-st" d="M50 32 H68 V100 A46 46 0 0 0 160 100 V32 H178" />
        <path class="i4-st" d="M114 146 V168 A30 30 0 0 0 174 168 V160" />
        <circle class="i4-acc" cx="174" cy="134" r="26" fill="#E3EDFD" />
        <circle cx="174" cy="134" r="8" fill="«BLUE»" />""",
    "supermarkt": """
        <rect class="i4-acc" x="104" y="44" width="48" height="42" rx="8" fill="#E3EDFD" />
        <path class="i4-st" d="M20 50 H48 L80 164 H194" />
        <path class="i4-st" d="M58 86 H216 L198 144 H74 Z" fill="#FFFFFF" />
        <circle class="i4-acc" cx="100" cy="198" r="15" fill="#FFFFFF" />
        <circle class="i4-acc" cx="178" cy="198" r="15" fill="#FFFFFF" />""",
    "werk": """
        <rect x="28" y="80" width="184" height="128" rx="22" fill="#E3EDFD" />
        <path class="i4-st" d="M86 80 V60 Q86 44 102 44 H138 Q154 44 154 60 V80" />
        <rect class="i4-st" x="28" y="80" width="184" height="128" rx="22" />
        <path class="i4-st" d="M28 132 H98 M142 132 H212" />
        <rect class="i4-acc" x="98" y="116" width="44" height="34" rx="8" fill="#FFFFFF" />""",
    "gemeente": """
        <path class="i4-st" d="M28 92 L120 38 L212 92 Z" fill="#E3EDFD" />
        <circle cx="120" cy="71" r="10" fill="«BLUE»" />
        <path class="i4-st" d="M40 114 H200" />
        <path class="i4-acc" d="M64 140 V170 M101 140 V170 M139 140 V170 M176 140 V170" />
        <path class="i4-st" d="M46 192 H194 M26 214 H214" />""",
}

TILES = [("huisarts", "de", "huisarts", "el médico de cabecera"),
         ("supermarkt", "de", "supermarkt", "el súper"),
         ("werk", "het", "werk", "el trabajo"),
         ("gemeente", "de", "gemeente", "el ayuntamiento")]

PIN = ('<svg viewBox="0 0 48 48"><path d="M24 43 C24 43 10 29.5 10 19 A14 14 0 0 1 38 19 C38 29.5 24 43 24 43 Z" fill="none" '
       'stroke="#FFFFFF" stroke-width="4.2" stroke-linejoin="round"/><circle cx="24" cy="19" r="5" fill="#FFFFFF"/></svg>')


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(SIT=cue(iid, "situaciones"), VIV=cue(iid, "vivir"), NAD=cue(iid, "nada"),
             TEO=cue(iid, "teoria"), LUE=cue(iid, "luego"), NO=cue(iid, "no"), USA=cue(iid, "usas"))
    # geometry: 2×2 tiles 420×300 (gap 32) under a pill; the whole block lifts LIFT px for the theory card
    TW, TH, G = 420, 300, 32
    GL = (1080 - (2 * TW + G)) // 2
    PT, GT, LIFT = 326, 438, 130
    c.update(LIFT=LIFT, GL=GL, GT=GT, PT=PT, TW=TW, TH=TH, GW=2 * TW + G, GH=2 * TH + G,
             CT=GT + 2 * TH + G - LIFT + 40)
    css = """
    #i4-prow { top: «PT»px; }
    #i4-grid { position: absolute; left: «GL»px; top: «GT»px; width: «GW»px; height: «GH»px; }
    .i4-tile { position: absolute; width: «TW»px; height: «TH»px; border-radius: 32px; background: #FFFFFF;
      box-shadow: 0 34px 80px rgba(4,0,40,0.38), 0 8px 22px rgba(4,0,40,0.20); }
    .i4-panel { position: absolute; left: 20px; top: 20px; width: 380px; height: 160px; border-radius: 20px; overflow: hidden;
      background-color: «PAPER»; box-shadow: inset 0 0 0 1px «LINE»;
      background-image: radial-gradient(circle, rgba(29,0,132,0.07) 1.6px, transparent 1.8px); background-size: 26px 26px; background-position: 4px 4px; }
    .i4-ico { position: absolute; left: 120px; top: 10px; width: 140px; height: 140px; overflow: visible; }
    .i4-st { fill: none; stroke: «INDIGO»; stroke-width: 16; stroke-linecap: round; stroke-linejoin: round; }
    .i4-acc { fill: none; stroke: «BLUE»; stroke-width: 16; stroke-linecap: round; stroke-linejoin: round; }
    .i4-nl { position: absolute; left: 30px; top: 198px; font-weight: 700; font-size: 44px; line-height: 1; letter-spacing: -0.02em;
      color: «INK»; white-space: nowrap; }
    .i4-art { color: «BLUE»; font-weight: 600; }
    .i4-es { position: absolute; left: 31px; top: 254px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 26px; line-height: 1;
      color: «MUTED»; white-space: nowrap; }
    #i4-theo { position: absolute; left: «GL»px; top: «CT»px; width: «GW»px; height: 212px; border-radius: 32px; background: #D9DDE7;
      box-shadow: 0 30px 70px rgba(4,0,40,0.32), 0 6px 18px rgba(4,0,40,0.16); }
    .i4-thr { position: absolute; left: 36px; top: 28px; display: flex; align-items: center; gap: 16px; white-space: nowrap; }
    #i4-th { color: #5A6276; }
    .i4-thr svg { display: block; width: 44px; height: 44px; }
    .i4-tlab { position: relative; font-family: "Inter", sans-serif; font-weight: 700; font-size: 40px; line-height: 1; letter-spacing: -0.01em; }
    #i4-tab { position: absolute; left: 36px; top: 98px; width: 800px; height: 84px; border-radius: 14px; overflow: hidden;
      box-shadow: inset 0 0 0 2px #C4C9D5; display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 28px 28px 28px; }
    .i4-cell { position: relative; box-shadow: inset -2px 0 0 #C4C9D5, inset 0 -2px 0 #C4C9D5; }
    .i4-hd { background: #CBD0DB; }
    .i4-bar { position: absolute; left: 18px; top: 10px; height: 8px; border-radius: 4px; background: #B5BBC9; }
    .i4-hd .i4-bar { background: #9EA5B5; }
    #i4-sl { position: absolute; left: -10px; top: 22px; width: calc(100% + 20px); height: 8px; border-radius: 4px; background: «RED»;
      transform-origin: 0% 50%; }
"""
    def tile(k, key, art, word, es):
        x = (k % 2) * (TW + G); y = (k // 2) * (TH + G)
        return f"""        <div id="i4-t{k}" class="i4-tile" style="left:{x}px; top:{y}px;">
          <div class="i4-panel"><svg class="i4-ico" viewBox="0 0 240 240">{TILE_ICONS[key]}</svg></div>
          <div class="i4-nl"><span class="i4-art">{art}</span> {word}</div>
          <div class="i4-es">{es}</div>
        </div>"""
    widths = [[150, 120, 132], [96, 170, 120], [128, 104, 156]]
    cells = "".join(f'<div class="i4-cell{" i4-hd" if r == 0 else ""}"><i class="i4-bar" style="width:{w}px"></i></div>'
                    for r, row in enumerate(widths) for w in row)
    body = "\n".join([ground(P, "blue"), f"""    <div id="i4-prow" class="i4-row"><div id="i4-pill" class="i4-pill">{PIN}<span>Situaciones reales</span></div></div>
    <div id="i4-grid">
{chr(10).join(tile(k, *t) for k, t in enumerate(TILES))}
    </div>
    <div id="i4-theo">
      <div id="i4-th" class="i4-thr">{icon('book')}<span id="i4-tht" class="i4-tlab">Teoría que no usas<i id="i4-sl"></i></span></div>
      <div id="i4-tab">{cells}</div>
    </div>"""])
    js = """
      tl.fromTo(q("pill"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);   // the label is there from the cut, no empty ground
      [0, 1, 2, 3].forEach((k) => {
        tl.fromTo(q("t" + k), { opacity: 0, scale: 0.7, y: 34 }, { opacity: 1, scale: 1, y: 0, duration: 0.36, ease: "back.out(1.7)" }, «SIT» - 0.06 + k * 0.12);
      });
      // «nada de la teoría»: the block lifts, the grey theory card slides in under it
      tl.to([q("prow"), q("grid")], { y: -«LIFT», duration: 0.46, ease: "power3.inOut" }, «NAD» - 0.14);
      tl.fromTo(q("theo"), { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 0.46, ease: "power3.out" }, «NAD» + 0.1);   // clears the lifting grid; bottom stays above the caption band
      // «no usas»: its label struck through; the card stays solid
      tl.fromTo(q("sl"), { scaleX: 0 }, { scaleX: 1, duration: 0.24, ease: "power2.out" }, «NO» - 0.06);
"""
    sfx = [(c["SIT"] - 0.06, "pop", 0.18), (c["SIT"] + 0.3, "pop", 0.15), (c["NO"] - 0.06, "click", 0.22)]
    return comp(iid, d, P, css, body, js, c), sfx
