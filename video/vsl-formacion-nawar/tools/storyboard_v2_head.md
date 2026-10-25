---
format: 1920x1080
duration: 202.9s
message: "El neerlandés no se te da mal: te lo estaban enseñando desde el inglés. Nawar te lo enseña desde el español — y esto es exactamente lo que hay dentro."
arc: Hook → Pain → Reframe → Nawar → 3 phases → Sounds → PAUSE «¿y qué hay dentro?» → DROP: laptop reveal → 16 weeks · 10 modules · +360 lessons → path → short videos → practice → flashcards → consultas → weekly live class (same teachers) → no A/B/C/D tests → outcomes → promise → CTA → end card
audience: hispanohablantes en Países Bajos / Flandes, atascados con el neerlandés
mode: autonomous
music: owner's track, re-edited on its own bar grid (audio_v2.json): STOP at 97.70 (start of frame 20), DROP at 100.92 (start of frame 21), breakdown from 168.12, riser 182.52, tension bar 184.92, RE-DROP 187.32 (start of frame 38), final hit 199.32 (frame 39 + 3.60)
---

# STORYBOARD v2 — Nawar VSL (Formación Nawar A0–A1)

All times inside a frame are **frame-relative seconds**. Exact per-word cue times for every frame are
in `timing.json` and are inlined into each frame packet — every reveal must land on its word's cue
(≤ 0.06 s early, never late). Master timeline: frame N starts at `timing.json → frames[N].start`.

v2 keeps frames 01–19 of v1 (same design, retimed to the new voice by `tools/retime_v2.py`; 01–03 are
re-grounded on NAWAR BLUE because the owner found the opening too white, 17 gets its new line). Frames
20–39 are new: the owner asked to stop the film Offlesson-style on «Vale, ¿y qué hay dentro?», reveal
the school with a laptop effect exactly on the music drop, and then show clearly EVERYTHING the
product includes.

## Video direction

**Look.** Same system as v1 (`frame.md`). The owner LOVES how NAWAR BLUE is used from the middle of
the film on — so the whole second half (20–39) is predominantly NAWAR BLUE (radial #025dc7 → #120081,
white dots, soft vignette), with NIGHT (#07041F glow) only for the "martes por la noche" beat (27) and
white cards/devices carrying the real product. Absolutely no orange anywhere. Yellow only inside the
logo image. Paper (#F5F7FF) only inside cards/UI — never as a full ground in 20–39.

**Energy.** Reference = Offlesson-style VSL: something new arrives on almost every spoken phrase; big
key words land exactly on the voice; the real product is shown inside devices; the camera moves with
purpose (push-ins, dives through screens, 3D tilts). Each frame cuts in **hard** on its first word —
the first 0.25 s carries a strong entrance move. No exits (the next frame's entrance is the
transition); only 39 fades out at the very end.

**The music is part of the edit.** Frame 20 starts at the instant the music STOPS dead — total silence
except the voice: the image must feel *paused*. Frame 21 starts exactly on the DROP: the biggest visual
hit of the film. Frames 34–37 sit on the song's breakdown (calmer, emotional, slower moves); 37 rides
the riser/tension (build, push-in, glow) and 38 starts exactly on the RE-DROP (second big hit). The
song's final hit lands at 39 + 3.60 s (right after "…cuando lo hablas.").

**Motion grammar.** power3.out for entrances, power4/expo.out for slams, ≤ 0.35 s per word reveal;
after the last reveal, hold (subtle drift ≤ 2 % scale at most). Overshoot only for logo bloom, check
pops and the CTA button. Within-frame scene changes are velocity-matched seams.

**Type.** 2–6 key words per sentence, big (Poppins 800/900); supporting words as a smaller lead-in
line (Poppins 600–700) or nothing. One accent per moment (chip OR blue-light color OR strike).

**The product is real.** Whenever the narration talks about the school, show actual platform footage
or screenshots inside a laptop/browser/phone (inventory in every packet). Never redraw the platform UI.
Props that are NOT the platform (quiz card, dice, flashcard prop, chat bubbles, toggles) are crafted
SVG/CSS in the house style.

**Negative list.** No orange. No emoji glyphs (no emoji font — draw icons as inline SVG). No brand
logos other than Nawar (no Duolingo, no Offlesson). No invented numbers/prices: the only numbers
allowed on screen are 16 semanas · 10 módulos · +360 lecciones · +30.000 alumnos siguen nuestras clases
en redes · lesson/exercise numbers visible in the real UI. No student names (blur if any appear). No
text below y=1000, nothing important within 60 px of the frame edges. No repeat/yoyo, no CSS
animations, no Math.random.

**Sound.** Each worker writes a sidecar `compositions/frames/<id>.sfx.json` (≤ 4 cues, quiet,
purposeful). The drop/re-drop already hit hard in the music — add at most a whoosh/impact that
*supports* them, never fights them. Frame 20 must stay nearly silent (one soft click on the pause, one
click on the play at the end).

---
