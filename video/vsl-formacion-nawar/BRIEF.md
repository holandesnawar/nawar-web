---
workflow: product-launch-video
flow: automation
storyboard: no
message: "El neerlandés no se te da mal: te lo estaban enseñando desde el inglés. Nawar te lo enseña desde el español."
destination: website / YouTube / VSL embed
aspect: 1920x1080
language: es
audience: hispanohablantes que viven (o van a vivir) en Países Bajos o Flandes y llevan tiempo atascados con el neerlandés
length: ~2 min (set by the recorded voiceover, 1:55 + end card)
angle: PAS — pain validation → reframe (not your fault, the method) → Nawar method → inside the school
VO_MODE: verbatim (voiceover already recorded in ElevenLabs; chosen take sped up 1.08×)
---

## Intent

A VSL (video sales letter) for the Formación Nawar A0–A1 of Holandés Nawar, an online Dutch school
for Spanish speakers. The owner wants it "espectacular / brutal", matching the energy of a reference
VSL ("objetivo"): fast kinetic typography synced word-by-word to the voice, a fresh visual metaphor on
nearly every sentence, white ↔ deep-color alternation, 3D-ish props, zoom / blur / whip transitions,
and the real product shown inside device mockups.

## Assets

- assets/audio/voiceover.wav — final narration (take "ElevenLabs Audio Confident Oct 2 2026.mp3", rubberband 1.08×, -16 LUFS). Starts at master t=0.40 s.
- transcript.json / timing.json — forced-aligned word timings (espeak-ng + MFCC DTW, pause-anchored) and the 25-frame plan.
- assets/video/inicio-home.mp4 — platform dashboard recording (Hola Team, progreso, hoja de ruta semanal).
- assets/video/formacion-cv.mp4 — course page + module list scroll.
- assets/video/clases-video-dentro.mp4 — inside a lesson: video class with native teacher, samenvatting, lezen, quiz.
- assets/video/consulta-nueva.mp4 — creating a new consulta ("cómo se traduce gezellig?").
- assets/img/ui-*.png, web-*.png — platform and website screenshots (from Material.pdf). Student name blurred.
- assets/img/logo-nawar.png — transparent wordmark (red/white/blue + Spanish swoosh).

## Customizations

- Kinetic on-screen text quotes the narration's key words, synced to the word timings (reference VSL style). This deliberately overrides the generic "never render narration text" frame rule. There is NO caption track.
- Brand-blue scenes use the owner's background spec: radial gradient centered 50% 50%, #025dc7 → #120081.
- SFX from the bundled media-use pack, mounted at the root.
- Custom assembly (tools/assemble.py) instead of assemble-index.mjs: one continuous voiceover track, and platform videos kept inside frame sub-compositions so their device mockups can tilt and zoom.

## Notes

- NO orange anywhere (owner rule). Yellow only inside the logo.
- Teachers: "profesores nativos holandeses, expertos en español".
- Social proof allowed on screen: "+30.000 alumnos siguen nuestras clases en redes". Never invent other numbers.
- No price anywhere.
- The script's "(logo Duolingo)" note is NOT followed literally: a generic gamified language app is drawn instead (third-party trademark in an ad). Offer the owner the swap.
- On-screen Dutch must be correct, natural Dutch (reviewed).
- Music: no BGM provider is reachable from this environment (HeyGen/HF blocked); ask the owner for a track (e.g. ElevenLabs Music).
