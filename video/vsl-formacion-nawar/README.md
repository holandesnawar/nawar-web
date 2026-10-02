# VSL Formación Nawar A0–A1 — proyecto HyperFrames (v2)

Vídeo de venta (16:9, 1920×1080, ~3:23) hecho con [HyperFrames](https://hyperframes.heygen.com):
cada escena es una página HTML animada con GSAP que se renderiza a MP4.

**v2** (sobre la v1 aprobada): voz nueva (toma B), música del cliente reeditada por compases, pausa estilo
Offlesson en «Vale, ¿y qué hay dentro?» con la música parada, apertura del portátil justo en el drop, y una
sección nueva que explica todo lo que incluye la formación (16 semanas, 10 módulos, +360 lecciones,
microlearning, lectura/escritura/escucha, flashcards, consultas, clase semanal con los mismos profes, sin
tests A/B/C/D). Las escenas 01–19 son las de la v1 reajustadas a la nueva voz; 01–03 pasan a fondo azul.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md` | Intención, público, reglas de marca (sin naranja, sin precio, profesores nativos…) |
| `STORYBOARD.md` | Las 39 escenas, plano a plano, atadas a la voz y a la música |
| `frame.md` | Sistema de diseño: colores, tipografías, componentes |
| `audio_v2.json` | Plan de montaje de audio: tomas de voz, parada, drop, re-drop, golpe final |
| `transcript.json` | Tiempos de cada palabra de la locución (alineación forzada, tiempo del archivo de voz) |
| `timing.json` | Ventana de cada escena en la línea de tiempo y sus palabras |
| `compositions/frames/NN-*.html` | Una escena por archivo (+ `.sfx.json` con sus efectos de sonido) |
| `compositions/frames_v1/` | Escenas de la v1 tal cual (fuente del reajuste de tiempos) |
| `index.html` | Montaje final (lo genera `tools/assemble.py`) |
| `tools/` | Audio v2, transcripción v2, tiempos, reajuste v1→v2, paquetes de escena, ensamblador, previsualizador |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh            # todos los medios desde el Drive (vídeos, capturas, voz B, música, fuentes, gsap, sfx)
                                      # y monta la banda sonora v2 (tools/build_audio_v2.py → assets/audio/, audio_v2.json)
python3 tools/transcript_v2.py        # transcript.json en el tiempo de la locución montada
python3 tools/timing.py               # timing.json (cortes forzados en la parada, el drop y el re-drop)
python3 tools/retime_v2.py            # escenas de la v1 → tiempos de la voz v2 sin tocar el diseño (salta 01–03 y 17,
                                      # retocadas a mano después; nómbralas para forzarlas)
python3 tools/gen_laptop_20_21.py     # escenas 20 y 21 (el portátil) salen de un único generador
python3 tools/assemble.py             # index.html
npx hyperframes lint
npx hyperframes render . --quality high -o renders/vsl-nawar-v2.mp4
```

Previsualizar una escena suelta: `python3 tools/preview_frame.py 21-portatil`.

## Música (reedición por compases, 100 BPM, compás = 2,4 s)

- Antes del drop: intro (9 compases) → hats (8) → breakdown sin bombo (6) → intro (2) → hats (8) → breakdown +
  subida + tensión (8). La música se para en seco en 97,70 s, al acabar «…los entrenamos uno a uno».
- «Vale, ¿y qué hay dentro? Te lo cuento.» suena en silencio; el drop entra en 100,92 s con el portátil.
- Después: sección completa (28 compases) → breakdown desde «Al terminar…» (168,12 s) → subida → tensión en
  «Ahora toca hablar» → re-drop en «Completa tu matrícula» (187,32 s) → golpe final justo tras «…cuando lo hablas»
  (199,32 s) y cola hasta el final.
