---
version: 1
name: Nawar VSL — Frame (video / frame layer)
description: >
  Holandés Nawar brand at 1920×1080 for a fast kinetic VSL. Two grounds that alternate on purpose:
  PAPER (light, the "problem" world, ink + red) and NAWAR BLUE (radial #025dc7 → #120081, the
  "solution" world, white + light-blue). Poppins ExtraBold/Black for kinetic type, Inter for UI-ish
  labels, Caveat for rare hand-written annotations. Real platform footage lives inside device
  mockups. Absolutely no orange.
unit: the frame — 1920×1080
principle: one idea per beat · words land on the voice · the product is real · no orange

colors:
  # grounds
  paper: "#F5F7FF"          # light ground (problem act)
  paper-dot: "rgba(29,0,132,0.07)"   # 1.6px dots every 28px on paper
  night: "#07041F"          # near-black indigo (dramatic pause / questions)
  blue-center: "#025dc7"    # radial gradient center (brand spec)
  blue-edge: "#120081"      # radial gradient edge  (brand spec)
  blue-dot: "rgba(255,255,255,0.07)"  # dots on blue
  # brand
  indigo: "#1D0084"         # brand indigo — display text on paper, solid fills
  blue: "#025dc7"
  blue-vivid: "#0b6df0"     # buttons, progress, active states
  blue-light: "#4da3ff"     # accent word on dark grounds
  sky: "#9fd5f5"            # soft highlight on dark
  nl-red: "#AE1C27"         # logo red (Dutch flag)
  nl-blue: "#21468C"        # logo blue (Dutch flag)
  # text
  ink: "#0C0C1E"            # primary text on paper
  ink-2: "#374151"
  muted: "#5A6480"          # labels on paper
  white: "#FFFFFF"
  white-72: "rgba(255,255,255,0.72)"  # secondary text on blue
  line: "#DDE6F5"           # hairlines / card borders on paper
  # signals
  alert: "#E02D3C"          # strike-throughs, ✕, "error", stuck — problem accent
  success: "#16A34A"        # ✓ ticks on paper
  success-on-dark: "#34D399"  # ✓ ticks on blue
  # forbidden: any orange (#F58220 and friends). Yellow appears ONLY inside the logo image.

gradients:
  nawar-blue: "radial-gradient(circle at 50% 50%, #025dc7 0%, #120081 72%)"
  night-glow: "radial-gradient(circle at 50% 45%, #1a0f5c 0%, #07041F 65%)"
  headline-white: "linear-gradient(180deg, #FFFFFF 0%, rgba(255,255,255,0.78) 100%)"

typography:
  # files live in assets/fonts/ (every frame declares its own @font-face)
  display-hero:  { fontFamily: "Poppins", weight: 900, px: 190, lineHeight: 0.95, tracking: "-0.04em", upper: true }
  display-h1:    { fontFamily: "Poppins", weight: 800, px: 120, lineHeight: 1.0,  tracking: "-0.035em" }
  display-h2:    { fontFamily: "Poppins", weight: 800, px: 84,  lineHeight: 1.05, tracking: "-0.03em" }
  display-h3:    { fontFamily: "Poppins", weight: 700, px: 56,  lineHeight: 1.1,  tracking: "-0.02em" }
  lead:          { fontFamily: "Poppins", weight: 600, px: 44,  lineHeight: 1.2,  tracking: "-0.01em" }
  label:         { fontFamily: "Inter",   weight: 700, px: 22,  tracking: "0.14em", upper: true }
  ui:            { fontFamily: "Inter",   weight: 600, px: 30,  lineHeight: 1.3 }
  ui-small:      { fontFamily: "Inter",   weight: 500, px: 24,  lineHeight: 1.35 }
  hand:          { fontFamily: "Caveat",  weight: 700, px: 64 }
  font-files:
    Poppins: "poppins-latin-{500,600,700,800,900}-normal.woff2, poppins-latin-800-italic.woff2"
    Inter: "inter-latin-{400,500,600,700,800}-normal.woff2"
    Caveat: "caveat-latin-700-normal.woff2"

radii: { card: "28px", card-sm: "18px", pill: "999px", device: "34px", key: "22px" }

shadows:
  card-on-paper: "0 30px 80px rgba(18,0,129,0.16), 0 4px 14px rgba(18,0,129,0.08)"
  card-on-blue: "0 40px 110px rgba(4,0,40,0.45)"
  glow-blue: "0 0 80px rgba(77,163,255,0.55)"

components:
  word-chip:     "inline highlight behind a key word: indigo fill + white text on paper, or white fill + indigo text on blue; radius 14px; slight -1.5° tilt allowed"
  strike:        "alert-red 10px bar that draws left→right across a word (scaleX 0→1, transform-origin left)"
  card:          "white, radius card, border 1px line, shadow card-on-paper / card-on-blue"
  pill:          "radius pill, label typography, 14px 28px padding; on blue: rgba(255,255,255,0.12) fill + 1px rgba(255,255,255,0.25) border"
  speech-bubble: "white card with a tail; Dutch text in Inter 600; the '…' reply bubble is ink-2 on #E8ECF7"
  icon-tile:     "rounded-square 180–240px, white card, one bold line icon (inline SVG, stroke 10–12px, indigo or blue-vivid) + Dutch word (display-h3) + Spanish gloss (ui-small, muted)"
  laptop:        "dark bezel #0C0C1E radius 26px, 22px inner padding, screen holds real footage (object-fit cover), aluminium base bar under it, perspective 2200px parent; may tilt rotationX/Y ≤ 20° and push in"
  phone:         "dark bezel #0C0C1E radius 64px, 16px padding, notch pill, 9:19.5 screen"
  check:         "circle 56px success fill + white tick that draws (stroke-dashoffset)"
  lock:          "padlock icon (inline SVG) — closed: muted; open: shackle rotates/lifts, blue-vivid"
  logo:          "assets/img/logo-nawar.png (754×269, transparent). Never recolor, never stretch; on paper or blue grounds; min width 360px"

grounds:
  paper:  "paper + dot grid (radial-gradient dots paper-dot, 28px). Ink text, indigo display, alert accents."
  blue:   "nawar-blue gradient + blue-dot grid + soft vignette. White text, blue-light accents."
  night:  "night-glow gradient. White text only, small and centered — the 'quiet before' beat."

motion:
  default-ease: "power3.out (entrances), power4.out / expo.out for slams"
  word-reveal: "each word lands on its VO cue (≤ 60 ms early): opacity 0→1, y 40→0 (or scale 1.25→1 + blur 10→0 for slams), 0.22–0.35 s"
  overshoot: "only for the logo bloom and checkmark pop; never as house style"
  holds: "after the last reveal, hold still; subtle 1–2px jitter at most"
  forbidden: "repeat:-1, yoyo, Math.random, Date.now, CSS transitions/@keyframes, lazy breathing, slow back-half pans"
---

# Nawar VSL — design notes

**Two worlds.** Frames 01–10 live mostly on PAPER (the viewer's frustrating reality: ink text, red
strikes, grey "dead" UI). Frame 09 drops to NIGHT for the intimate questions. Frame 11 is the turn:
the screen floods with NAWAR BLUE and stays predominantly blue for the solution (11–25), with an
occasional paper frame for contrast (vocabulary tiles, sound tiles) so the alternation keeps energy.

**Type does the talking.** The narration's key words appear big, synced to the voice. Not every word —
pick 2–6 words per sentence that carry the meaning and let them land exactly on their spoken time.
Supporting words can appear smaller as a lead-in line (lead / display-h3), key words slam (display-h1
or hero). One accent per frame: word-chip OR color OR strike — not all three.

**The product is real.** Whenever the narration talks about the school, show the actual platform
footage/screenshots inside a laptop or phone. Never redraw the platform UI from scratch.

**Dutch on screen** is always correct, short, and paired with a small Spanish gloss when it helps.
