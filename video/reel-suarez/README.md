# Reel «Aprendiendo neerlandés con Luis Suárez» · Holandés Nawar (Instagram, 9:16) — proyecto HyperFrames

Segunda entrega del formato del reel de Mario Casas (100 000 visitas): una escena real en neerlandés, en vertical,
con el título arriba y subtítulos en holandés y en español. Esta vez es el anuncio de Luis Suárez en el Ajax
(«Comercial Geestige Suarez Ajax»), recortado sin la marca del anuncio.

- **Corte:** del anuncio de 45 s queda la escena (de 5,40 s a 40,08 s del original, unos 34,7 s). Fuera quedan la
  presentación de la tienda, con su nombre en voz y en imagen, y el cierre con el logo y la voz de la marca.
- **9:16 a pantalla completa:** cada plano tiene su encuadre vertical sobre quien habla (`SHOTS` en `tools/frame.py`),
  con paneos suaves donde la cámara o el que habla se mueven.
- **Nitidez:** el original es de 512×288. Se reescala ×4 con Real-ESRGAN («realesr-general-x4v3», en ONNX y en CPU)
  antes de recortar, con un grano fino para que no quede con aspecto de cera y un poco más de contraste y color que el original.
- **Sin marca:**
  - no aparece el rótulo de la tienda;
  - el texto de la pared («De hoorspecialist») queda fuera de cada encuadre;
  - se borra lo impreso en las dos tarjetas de visita (`LOGOS`).
- **Título:** «📚 Aprendiendo neerlandés con Luis Suárez 🇳🇱», grande desde el primer fotograma (gancho y portada). A los 3 s pasa a una etiqueta pequeña arriba («Neerlandés con Luis Suárez»), para no tapar las caras en los primeros planos.
- **Subtítulos:** por frases cortas, sincronizados palabra a palabra (ElevenLabs Scribe):
  - el holandés grande y en mayúsculas, con la palabra que se está diciendo en amarillo;
  - el español debajo, en una pastilla gris.

  El español conserva los juegos de palabras del anuncio:
  - «fluiten» → pitar: los árbitros le pitan;
  - «bank» → banco / banquillo;
  - «kaartje» → tarjeta: amarillas y rojas.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md`, `STORYBOARD.md` | Petición y plano a plano |
| `index.html` | El reel (lo genera `tools/gen.py`) |
| `subs.json` | Subtítulos con el tiempo de cada palabra (lo genera `tools/subs.py`) |
| `tools/subs.py` | Las frases en holandés y en español (`PHRASES`), alineadas con la transcripción de Scribe |
| `tools/frame.py` | El corte, el encuadre 9:16 de cada plano, el borrado de la marca y el sonido (−14 LUFS) → `assets/video/suarez-916.mp4` |
| `tools/upscale.py` | El reescalado ×4 del tramo usado → `.raw/up.mp4` |
| `tools/emoji.py` | Dibuja 📚 y 🇳🇱 (Noto Color Emoji) en PNG |
| `tools/esrgan_onnx.py` | Convierte el modelo de Real-ESRGAN a ONNX sin PyTorch (lee los pesos sin ejecutar el pickle) |
| `tools/fetch_assets.sh` | Lo reconstruye todo desde el Drive |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh
npx hyperframes check
npx hyperframes render . --quality high --fps 25 -o renders/reel-suarez-v2.mp4
```

Para cambiar una traducción o cortar una frase de otra manera, edita `PHRASES` en `tools/subs.py` y ejecuta
`python3 tools/subs.py && python3 tools/gen.py`. Para cambiar un encuadre, edita `SHOTS` en `tools/frame.py` y ejecuta
`python3 tools/frame.py && python3 tools/gen.py`.
