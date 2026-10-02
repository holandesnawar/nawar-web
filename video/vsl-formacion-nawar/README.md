# VSL Formación Nawar A0–A1 — proyecto HyperFrames

Vídeo de venta (16:9, 1920×1080, ~2:02) hecho con [HyperFrames](https://hyperframes.heygen.com):
cada escena es una página HTML animada con GSAP que se renderiza a MP4.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md` | Intención, público, reglas de marca (sin naranja, sin precio, profesores nativos…) |
| `STORYBOARD.md` | Las 25 escenas, plano a plano, atadas a la voz |
| `frame.md` | Sistema de diseño: colores, tipografías, componentes |
| `transcript.json` | Tiempos de cada palabra de la locución (alineación forzada) |
| `timing.json` | Ventana de cada escena en la línea de tiempo y sus palabras |
| `compositions/frames/NN-*.html` | Una escena por archivo (+ `.sfx.json` con sus efectos de sonido) |
| `index.html` | Montaje final (lo genera `tools/assemble.py`) |
| `tools/` | Alineador de voz, previsualizador de escenas, ensamblador, música procedural, descarga de medios |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh          # descarga los medios del Drive y los prepara (voz 1.08×, vídeos, capturas, música)
python3 tools/assemble.py           # genera index.html (MUSIC_VOL=1 si usas la música ya ducked)
npx hyperframes lint
npx hyperframes render . --quality high -o renders/vsl-nawar.mp4
```

Previsualizar una escena suelta: `python3 tools/preview_frame.py 07-intentos`.

## Cambiar la voz o la música

- **Voz nueva**: sustituye `assets/audio/voiceover.wav`, realinea con `tools/align/align3.py`
  (texto en `tools/align/narration.txt`), regenera `transcript.json` y ejecuta `python3 tools/timing.py`;
  las escenas leen sus tiempos de `timing.json`.
- **Música**: guarda la pista como `assets/audio/music.wav` (o `.mp3`) y vuelve a ensamblar.
  La base actual es procedural (provisional), en menor hasta la aparición de Nawar (52,15 s) y en mayor después.
