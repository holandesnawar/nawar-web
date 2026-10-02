# Mac mockup — MacBook Pro (front view) + macOS window

Owner feedback on v2 (verbatim): «me gustaría un mac real, no un laptop falso» · «uno de los mockups típicos» ·
«simplemente de frente, sin que se le vean las teclas» · «tiene que quedar formato 16/9 para que no se quede
achatado en los lados» · «el marco típico de mac, con la x roja, el minimizar amarillo» · «no me gusta ese zoom
que se le hace al vídeo del mockup».

This file is the single source for the device. Copy the CSS + markup into a frame, replace `fNN-` with the
frame prefix (`f12-`, `f14-`, …) and set `--sw`. Pilots: `compositions/frames/12-metodo.html`,
`compositions/frames/14-supervivencia.html` (QA stills: `scratchpad/v2work/qa/mac-pilot-12.png`, `mac-pilot-14.png`).

## What it is

- **MacBook Pro, camera straight on.** Silver aluminium lid edge (`.fNN-mbp--grey` = space grey), thin even black
  glass bezel (slightly taller chin, like the real thing), camera notch with concave fillets and a tiny lens, a
  subtle diagonal glass reflection, the base seen only as a thin aluminium front lip (wider than the lid) with the
  centre thumb scoop, and a soft contact shadow plus a tight occlusion line. No keyboard, no Apple logo, no
  "MacBook" text.
- **Proportions.** Lid 1160u × 754u = **1.54 : 1** (real 14"/16" MBP ≈ 1.53). Screen 1120u × 700u = **16:10**.
  Bezel 16u sides/top, 30u chin, 4u aluminium edge. Notch 118u × 21u (≈ 10.5 % of the screen width). Base lip
  1236u × 27u, overhanging the lid by 38u per side.
- **Browser inside, macOS style (Chrome-like).** Tab strip 36u with traffic lights (12u, 20u pitch:
  red `#FF5F57`, yellow `#FEBC2E`, green `#28C840`), the active tab (Nawar favicon rebuilt from
  `assets/img/logo-nawar.png` on the site's blue tile + «Holandés Nawar» + ×), «+»; toolbar 34u with back /
  forward (disabled) / reload and the URL pill (lock + `holandesnawar.com` + star) and ⋮. Chrome = **70u**.
- **Content area = exactly 16:9.** 1120u × 630u (chrome = screen height − width·9/16 = 700u − 630u). Real
  recordings go in with `object-fit: cover`: our 2560×1376 (1.86:1) recordings lose 4.4 % of their width in total,
  never stretched or squashed.
- **Standalone macOS window** (`.fNN-win`): the same chrome and the same 16:9 content area, 12u corner radius,
  hairline border plus a light inner edge, and a real window shadow. The overall window is 16:10.

## Units and sizes

`--sw` = **screen width** (MacBook) or **window width** (window). Use a multiple of 16 so that every edge lands
on a whole pixel. One unit `u = --sw / 1120`, and every other size derives from it.

MacBook (`.fNN-mbp` box = 1236u × 778u; place it with `left/top`; the contact shadow overflows ≈ 70u below):

| --sw | u | device box (w × h) | lid | screen 16:10 | chrome | content 16:9 | content origin in box |
|---|---|---|---|---|---|---|---|
| 768 | 0.6857 | 847.5 × 533.5 | 795.4 × 517.0 | 768 × 480 | 48 | **768 × 432** | (39.8, 61.7) |
| 848 | 0.7571 | 935.8 × 589.1 | 878.3 × 570.9 | 848 × 530 | 53 | **848 × 477** | (43.9, 68.1) |
| 896 | 0.8000 | 988.8 × 622.4 | 928.0 × 603.2 | 896 × 560 | 56 | **896 × 504** | (46.4, 72.0) |
| 1024 | 0.9143 | 1130.1 × 711.3 | 1060.6 × 689.4 | 1024 × 640 | 64 | **1024 × 576** | (53.0, 82.3) |

(848 = frame 14, 896 = frame 12.) The screen origin inside the box is (58u, 20u); the content origin is (58u, 90u).

Window (`.fNN-win` box = 1120u × 700u):

| --sw | u | window | chrome | content 16:9 | radius |
|---|---|---|---|---|---|
| 640 | 0.5714 | 640 × 400 | 40 | **640 × 360** | 6.9 px |
| 960 | 0.8571 | 960 × 600 | 60 | **960 × 540** | 10.3 px |
| 1280 | 1.1429 | 1280 × 800 | 80 | **1280 × 720** | 13.7 px |

## Fonts

The chrome uses Inter 500. The frame must declare it:
`@font-face { font-family: "Inter"; font-weight: 500; font-style: normal; src: url("assets/fonts/inter-latin-500-normal.woff2") format("woff2"); }`

## CSS (prefix `fNN-`)

Frames that only use the MacBook may drop the "standalone macOS window" block and change the first selector to
`.fNN-mbp { --u: … }` (the pilots do this).

```css
/* ================= MAC MOCKUP (tools/mac_mockup.md) — MacBook Pro front view + macOS window =================
   One design unit u = screen width / 1120. Screen = 1120u × 700u (16:10). Browser chrome = 70u,
   content = 1120u × 630u = exactly 16:9. Set --sw (screen / window width, a multiple of 16) and
   everything else follows. */
.fNN-mbp, .fNN-win { --u: calc(var(--sw) / 1120); }
.fNN-mbp {
  --sw: 896px;
  --al-0: #fbfbfc; --al-1: #e4e6ea; --al-2: #c3c7ce; --al-3: #9a9fa8; --al-4: #6f747d;   /* silver */
  position: absolute; width: calc(var(--u) * 1236); height: calc(var(--u) * 778);
}
.fNN-mbp--grey { --al-0: #c4c7cc; --al-1: #8e9198; --al-2: #6c6f76; --al-3: #4d5056; --al-4: #34363b; }
/* soft contact shadow on the "table" + a tight occlusion line under the lip */
.fNN-mbp-shadow {
  position: absolute; left: calc(var(--u) * -50); top: calc(var(--u) * 746); width: calc(var(--u) * 1336); height: calc(var(--u) * 110);
  border-radius: 50%;
  background: radial-gradient(ellipse 50% 50% at 50% 40%, rgba(3,0,30,0.72) 0%, rgba(3,0,30,0.44) 34%, rgba(3,0,30,0.14) 64%, rgba(3,0,30,0) 100%);
}
.fNN-mbp-occl {
  position: absolute; left: calc(var(--u) * 30); top: calc(var(--u) * 772); width: calc(var(--u) * 1176); height: calc(var(--u) * 14);
  border-radius: 50%; background: rgba(2,0,20,0.85); filter: blur(calc(var(--u) * 4));
}
/* lid: thin aluminium edge around black glass */
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
  border-radius: calc(var(--u) * 10) calc(var(--u) * 10) calc(var(--u) * 1.5) calc(var(--u) * 1.5); overflow: hidden; background: #FFFFFF;
}
/* camera notch (with concave fillets into the bezel) + lens */
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
/* glass reflection over bezel + screen */
.fNN-mbp-reflect {
  position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none;
  background: linear-gradient(121deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.035) 30%, rgba(255,255,255,0.016) 40.5%, rgba(255,255,255,0) 42%, rgba(255,255,255,0) 100%);
}
/* base: front lip only (no keyboard), slightly wider than the lid, drawn over the lid's hinge edge */
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

/* standalone macOS window (same chrome, 16:10 overall, 16:9 content) */
.fNN-win {
  --sw: 1120px;
  position: absolute; width: calc(var(--u) * 1120); height: calc(var(--u) * 700);
  border-radius: calc(var(--u) * 12); overflow: hidden; background: #FFFFFF;
  box-shadow: 0 0 0 calc(var(--u) * 1) rgba(10,10,30,0.28), 0 calc(var(--u) * 30) calc(var(--u) * 90) rgba(4,0,40,0.50), 0 calc(var(--u) * 10) calc(var(--u) * 26) rgba(4,0,40,0.30);
}
.fNN-win-edge {
  position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: calc(var(--u) * 12); pointer-events: none;
  box-shadow: inset 0 0 0 calc(var(--u) * 1) rgba(255,255,255,0.45);
}

/* browser chrome (shared): tab strip 36u + toolbar 34u = 70u */
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
.fNN-nav { position: absolute; left: calc(var(--u) * 14); top: calc(var(--u) * 9); width: calc(var(--u) * 86); height: calc(var(--u) * 16); overflow: visible; }   /* back · forward (disabled) · reload */
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
/* 16:9 content area — real recordings, object-fit cover (never stretch) */
.fNN-content { position: absolute; left: 0; top: calc(var(--u) * 70); width: calc(var(--u) * 1120); height: calc(var(--u) * 630); overflow: hidden; background: #FFFFFF; }
.fNN-media { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: var(--fx, 50%) 50%; display: block; }
```

## Markup — MacBook Pro

`#fNN-lap` is the non-timed wrapper you animate. The `<video>` keeps its own clip attributes; **no ancestor of a
`<video>` may carry `data-start`**. Paint order matters: shadow, then lid, then base (the base lip covers the
lid's hinge edge).

```html
<div id="fNN-lap" class="fNN-mbp" style="--sw:896px; left:100px; top:230px;">
  <div class="fNN-mbp-shadow"></div><div class="fNN-mbp-occl"></div>
  <div class="fNN-mbp-lid">
    <div class="fNN-mbp-glass">
      <div class="fNN-mbp-screen">
        <div class="fNN-chrome">
          <div class="fNN-tabs"><i class="fNN-tl fNN-tl-r"></i><i class="fNN-tl fNN-tl-y"></i><i class="fNN-tl fNN-tl-g"></i>
            <div class="fNN-tab"><div class="fNN-fav"><img src="assets/img/logo-nawar.png" alt="" /></div><div class="fNN-tab-t">Holandés Nawar</div><svg class="fNN-tab-x" viewBox="0 0 10 10" aria-hidden="true"><path d="M2.2 2.2 L7.8 7.8 M7.8 2.2 L2.2 7.8" fill="none" stroke="#5F6368" stroke-width="1.3" stroke-linecap="round" /></svg></div>
            <svg class="fNN-plus" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 2.2 V11.8 M2.2 7 H11.8" fill="none" stroke="#5F6368" stroke-width="1.4" stroke-linecap="round" /></svg></div>
          <div class="fNN-bar"><svg class="fNN-nav" viewBox="0 0 86 16" aria-hidden="true"><g fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13 8 H3.4 M7.8 3.6 L3.4 8 L7.8 12.4" stroke="#5F6368" /><path d="M31 8 H40.6 M36.2 3.6 L40.6 8 L36.2 12.4" stroke="#BDC1C6" /><path d="M68.7 8.6 A4.8 4.8 0 1 1 67.3 4.5 M68 1.9 V5.1 H64.8" stroke="#5F6368" /></g></svg>
            <div class="fNN-url"><svg class="fNN-lock" viewBox="0 0 13 13" aria-hidden="true"><path d="M4.3 6 V4.3 A2.2 2.2 0 0 1 8.7 4.3 V6" fill="none" stroke="#5F6368" stroke-width="1.3" /><rect x="2.6" y="5.8" width="7.8" height="5.9" rx="1.3" fill="#5F6368" /></svg><div class="fNN-url-t">holandesnawar.com</div><svg class="fNN-star" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1.8 L8.55 5.05 L12.1 5.5 L9.5 7.95 L10.15 11.5 L7 9.8 L3.85 11.5 L4.5 7.95 L1.9 5.5 L5.45 5.05 Z" fill="none" stroke="#5F6368" stroke-width="1.1" stroke-linejoin="round" /></svg></div>
            <svg class="fNN-menu" viewBox="0 0 16 16" aria-hidden="true"><g fill="#5F6368"><circle cx="8" cy="3.4" r="1.35" /><circle cx="8" cy="8" r="1.35" /><circle cx="8" cy="12.6" r="1.35" /></g></svg></div>
        </div>
        <div class="fNN-content" style="--fx:12%;">
          <video id="fNN-vid" class="clip fNN-media" src="assets/video/<file>.mp4" muted playsinline
            data-start="<frame-local s>" data-duration="<s>" data-media-start="<source s>" data-hf-media-start-basis="local" data-track-index="2"></video>
          <!-- overlays that must sit ON the footage (focus rings, highlights) go here, in content px -->
        </div>
        <!-- overlays over the whole screen incl. chrome (dim layer, glare sweep) go here -->
      </div>
      <div class="fNN-mbp-notch"><i class="fNN-mbp-lens"></i></div>
      <div class="fNN-mbp-reflect"></div>
    </div>
  </div>
  <div class="fNN-mbp-base"><div class="fNN-mbp-thumb"></div></div>
</div>
```

## Markup — standalone macOS window

```html
<div id="fNN-win" class="fNN-win" style="--sw:960px; left:480px; top:200px;">
  <div class="fNN-chrome">
    <div class="fNN-tabs"><i class="fNN-tl fNN-tl-r"></i><i class="fNN-tl fNN-tl-y"></i><i class="fNN-tl fNN-tl-g"></i>
      <div class="fNN-tab"><div class="fNN-fav"><img src="assets/img/logo-nawar.png" alt="" /></div><div class="fNN-tab-t">Holandés Nawar</div><svg class="fNN-tab-x" viewBox="0 0 10 10" aria-hidden="true"><path d="M2.2 2.2 L7.8 7.8 M7.8 2.2 L2.2 7.8" fill="none" stroke="#5F6368" stroke-width="1.3" stroke-linecap="round" /></svg></div>
      <svg class="fNN-plus" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 2.2 V11.8 M2.2 7 H11.8" fill="none" stroke="#5F6368" stroke-width="1.4" stroke-linecap="round" /></svg></div>
    <div class="fNN-bar"><svg class="fNN-nav" viewBox="0 0 86 16" aria-hidden="true"><g fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M13 8 H3.4 M7.8 3.6 L3.4 8 L7.8 12.4" stroke="#5F6368" /><path d="M31 8 H40.6 M36.2 3.6 L40.6 8 L36.2 12.4" stroke="#BDC1C6" /><path d="M68.7 8.6 A4.8 4.8 0 1 1 67.3 4.5 M68 1.9 V5.1 H64.8" stroke="#5F6368" /></g></svg>
      <div class="fNN-url"><svg class="fNN-lock" viewBox="0 0 13 13" aria-hidden="true"><path d="M4.3 6 V4.3 A2.2 2.2 0 0 1 8.7 4.3 V6" fill="none" stroke="#5F6368" stroke-width="1.3" /><rect x="2.6" y="5.8" width="7.8" height="5.9" rx="1.3" fill="#5F6368" /></svg><div class="fNN-url-t">holandesnawar.com</div><svg class="fNN-star" viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1.8 L8.55 5.05 L12.1 5.5 L9.5 7.95 L10.15 11.5 L7 9.8 L3.85 11.5 L4.5 7.95 L1.9 5.5 L5.45 5.05 Z" fill="none" stroke="#5F6368" stroke-width="1.1" stroke-linejoin="round" /></svg></div>
      <svg class="fNN-menu" viewBox="0 0 16 16" aria-hidden="true"><g fill="#5F6368"><circle cx="8" cy="3.4" r="1.35" /><circle cx="8" cy="8" r="1.35" /><circle cx="8" cy="12.6" r="1.35" /></g></svg></div>
  </div>
  <div class="fNN-content" style="--fx:12%;">
    <video id="fNN-vid" class="clip fNN-media" src="assets/video/<file>.mp4" muted playsinline
      data-start="…" data-duration="…" data-media-start="…" data-hf-media-start-basis="local" data-track-index="2"></video>
  </div>
  <div class="fNN-win-edge"></div>
</div>
```

A still image works the same way: `<img class="fNN-media" src="assets/img/…" alt="" />` inside `.fNN-content`.

## Mounting footage (project rules)

1. `<video class="clip fNN-media" … muted playsinline>` goes directly inside `.fNN-content`. Every ancestor
   (`.fNN-content`, screen, glass, lid, `.fNN-mbp`, your wrappers) stays **non-timed** (no `data-start`).
2. `data-media-start + data-duration` ≤ the source length. Looped holds = several stacked `<video>`s on the same
   track index (see frame 14).
3. **Never animate the video or `.fNN-content`** (no scale, x, y, or size). Owner note: no zoom on the footage.
   Animate a wrapper around the whole device only.
4. `--fx` = horizontal `object-position`. Platform recordings (left blue sidebar whose labels start about 26 source
   px from the edge) use **`--fx: 12%`** so the 4.4 % crop falls mostly on the right margin and «Formación Nawar
   A0-A1 · 28 %» is not clipped. Use `50%` for centred content.
5. Mapping a source pixel (xs, ys) of a 2560×1376 recording to content px (for focus rings, arrows):
   `k = contentH / 1376`, `crop = (2560·k − contentW) · fx`, `x = xs·k − crop`, `y = ys·k`.
   Example (frame 12, content 896×504, fx 0.12): k = 0.3663, crop = 5.0, so the teacher webcam tile
   (841–1181, 179–375) maps to x 303–428, y 66–137.
   Page coordinates = device `left/top` + content origin (58u, 90u) + (x, y).

## Motion rules for the device

- **Front view only.** No `rotationY`/`rotationX` (that is what made v2 look squashed). No perspective stage.
- Entrances: animate the wrapper (`#fNN-lap` or a parent) with x/y/scale/opacity/blur, e.g. a slide-in with a
  directional SVG blur (frame 14), a velocity-matched seam plus `y: 26 → 0` (frame 12), or a rise with a scale of
  0.96 → 1.
- Holds: still, or a whole-stage drift of at most 2 %. A camera push on the whole device is allowed when the
  storyboard asks for it (frame 12 pushes toward the teacher tile), but never a zoom into the footage inside a
  fixed frame.
- The `.fNN-mbp-reflect` glass reflection is static. A one-off glare sweep may cross the screen once at the
  entrance (frame 14 `#f14-sheen`).
- Old house laptop parts to delete when rolling out: `#fNN-lapstage` (perspective), `#fNN-floor` (the device has
  its own shadow), `#fNN-bezel`/`#fNN-camdot`/`#fNN-base`/`#fNN-notch`/`#fNN-glass`, and any video-zoom wrapper.

## Lint note

`composition_file_too_large` counts physical lines outside `<style>` (limit 300). The chrome markup above is
deliberately compact (8 lines). Keep it that way when pasting.
