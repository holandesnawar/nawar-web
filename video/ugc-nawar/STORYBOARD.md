---
format: 1080x1920
duration: 51.6s
message: "Si vives en Países Bajos y te bloqueas al llamar en neerlandés, Nawar te lleva en 16 semanas a llamar tú: rellena el formulario."
audience: hispanohablantes en Países Bajos / Flandes
mode: autonomous
arc: hook (identificación) → dolor (la llamada, el bloqueo, el inglés) → giro (Nawar, profes nativos que hablan tu idioma) → prueba (lecciones grabadas, ejercicios de verdad, clase en directo) → resultado (16 semanas: llamas tú) → CTA (botón + formulario)
---

# STORYBOARD — Nawar UGC ad (Meta / TikTok, 9:16)

Times are edit seconds (`edit.json`, built by `tools/edit.py`): two takes alternated sentence by sentence at 1.05×.
Every overlay is a sub-composition whose window equals its shot; its cues come from `edit.json` word times.

## Direction

- **Look:** the real footage carries the ad (UGC = trust). Graphics are the Nawar system — NAWAR BLUE
  (#025dc7 → #120081 radial, #0b6df0 accent), white cards with 28px radius and real shadows, Poppins 800/900 +
  Inter. Red #E02D3C only for the block/error, green #16A34A only for success. No orange, no emoji glyphs.
- **Zones:** graphics live in the top band (y 230–700, over the wall) or take the full frame as short cutaways;
  her face (y 700–1080) stays clear while she is on screen; captions sit at y≈1235; nothing important below
  y 1480 (TikTok/Reels UI) except the CTA arrows that point at the platform button.
- **Rhythm:** something changes every 1–2 s: angle switch on each sentence, punch-in zooms on the key word,
  top cards on the nouns, full-screen cutaways for the call, the brand, the product and the live class.
- **Captions:** 1–3 words per page, Poppins 800 white with a dark stroke, the spoken word on a blue pill
  (karaoke form of `asr-keyword-glow`); «bloqueas» red, «Nawar» / «16 semanas» accented.

## Frame 1 — gfx-01 · hook (shot 1, B front, 0.00–3.86)
- src: compositions/gfx-01.html · rules: spring-pop-entrance, coordinate-target-zoom (punch on «escucha esto»)
- Sticker visible on frame 0: flag chip + «Si vives en Países Bajos…»; on «médico» a «Huisarts» pill joins;
  «escucha esto» = punch-in to 1.22 on her face.

## Frame 2 — gfx-02 · la llamada (shot 2, B, 3.86–8.38)
- src: compositions/gfx-02.html · rules: discrete-text-sequence (typing the rehearsed line), chromatic-glitch (block)
- «practicas la frase»: note card typing «Goedemorgen, ik wil graag een afspraak maken…».
- «llamas»: full-screen call screen (Huisartsenpraktijk, calling…, ringback); «te contestan»: connected +
  fast Dutch bubble; «te bloqueas»: her bubble «Eh… ik… ehm…» glitches, red «BLOQUEO» tag.

## Frame 3 — gfx-03 · el favor (shot 3, A side, 8.38–13.24)
- rules: spring-pop-entrance, svg-path-draw
- «alguien más»: phone passes from «Tú» to «Otra persona»; «en tu país … sin pensarlo»: chips
  «Tu idioma ✓ sin pensarlo» vs «Neerlandés ✗ te bloqueas».

## Frame 4 — gfx-04 · el tiempo y el inglés (shot 4, B, 13.24–17.64)
- rules: vertical-spring-ticker (years), spring-pop-entrance
- «con el tiempo»: year ticker 2021→2025 struck in red; «alguien que te traduce»: bubbles; «te cambia al
  inglés»: «Oh, let's just speak English!» + punch-in.

## Frame 5 — gfx-05 · Nawar (shot 5, A, 17.64–22.47)
- rules: spring-pop-entrance, ambient-glow-bloom
- «Nawar»: full-screen blue brand slam (logo + «te enseñamos neerlandés»), back to her on «con un equipo»;
  teacher card (Paul, real class footage) «Profesores nativos · expertos en español»; «dominan tu idioma»:
  his bubble «¡Te lo explico en español!».

## Frame 6 — gfx-06 · lecciones grabadas (shot 6, B, 22.47–25.25)
- rules: spring-pop-entrance, stat-bars-and-fills (lesson progress)
- Real recorded lesson in a card «Lección grabada»; «cuando tú puedas»: time chips light up.

## Frame 7 — gfx-07 · ejercicios de verdad (shot 7, A, 25.25–30.53)
- rules: waterfall-entry (skills), css-marker-patterns (strike)
- Full-screen product cutaway: real «Completa la frase» exercise; chips Leer · Escribir · Entrenar el oído on
  their words; «simple test»: an A/B/C/D card struck through in red.

## Frame 8 — gfx-08 · clase en directo (shot 8, B, 30.53–37.02)
- rules: spring-pop-entrance, gsap-effects (audio visualizer on «pronunciación»)
- «cada semana»: weekday row with the class day lit; «clase en directo»: full-screen live class (Paul) with
  «EN DIRECTO» badge; «pronunciación»: voice bars.

## Frame 9 — gfx-09 · 16 semanas (shot 9, A, 37.02–43.27)
- rules: counting-dynamic-scale (1→16), stat-bars-and-fills (16 week pills), spring-pop-entrance
- «dieciséis semanas»: count-up + pills; «eres tú quien llama y pide la cita»: call card, her Dutch line +
  «Cita confirmada ✓»; «a nadie»: punch-in.

## Frame 10 — gfx-10 · CTA (shot 10, B, 43.27–51.61)
- rules: cursor-click-ripple, press-release-spring, spring-pop-entrance
- «comenzar»: punch-in; «botón de acá abajo»: arrows bouncing toward the platform button; «rellena el
  formulario»: form card fills + «Enviar» click; «te atenderá»: «Equipo Nawar» bubble; end card (logo,
  «Formación Nawar», «Rellena el formulario»).

## Frame 11 — captions (0–51.61)
- src: compositions/captions.html · rules: asr-keyword-glow (karaoke form)
