# Anuncio UGC Black Friday · Holandés Nawar (Meta / TikTok Ads, 9:16) — proyecto HyperFrames

Creativo UGC en vertical (1080×1920, 40 s) para el Black Friday: el ebook «Holandés sin miedo», de 70 páginas en
español y para imprimir, por 1 € hasta el 30 de noviembre. Es el mismo sistema y el mismo diseño que el VSL y los UGC
#1 y #2 (`../ugc-nawar`, `../ugc-nawar-2`):
- Ella habla a cámara. Cuando explica algo, la imagen corta a un gráfico a pantalla completa (papel o azul Nawar) y
  vuelve a ella.
- El ebook es la animación real del cliente («Animación Libro»), recortada de su negro y sobre el azul Nawar, con sus etiquetas.
- Objetos planos, sin sombras exteriores (v6).
- Black Friday (v5): tres veces su habitación desaparece y ella queda recortada delante de filas gigantes de texto que
  corren («BLACK FRIDAY» en el gancho, «1€» en la oferta, «BLACK FRIDAY» otra vez), con flash y golpe. El cierre es el
  botón azul del UGC #2.
- Gancho: «Si vives en Países Bajos…» (de «intro gancho», desde el segundo 15). Cuerpo: «Estado de pedido».

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md`, `STORYBOARD.md` | Petición y plano a plano |
| `edit.json` | El montaje: tramos de cada toma, ventanas de los gráficos, palabras con su tiempo |
| `index.html` | Montaje final (lo genera `tools/gen.py`): la chica (take g = gancho, take p = cuerpo), encuadres, música y efectos |
| `compositions/ins-01…04.html` | Los gráficos a pantalla completa |
| `compositions/offer.html`, `outro.html` | Lo que va sobre ella: «Hasta el 30 de noviembre» y el botón final |
| `compositions/captions.html` | Subtítulos blancos palabra a palabra, cortados por frases |
| `tools/libro_clip.py` | Corta la animación del ebook a su voz (a su velocidad hasta «ejercicios», luego «¡Hora de practicar!» quieta) y recorta el libro de su negro → `libro-ins04.webm` con transparencia |
| `tools/mattes.py` | Recorta a la chica con Robust Video Matting (ONNX, CPU; estable entre fotogramas) en los tres momentos Black Friday y limpia el recorte contra una placa de la habitación vacía, sin tocar lo que es ella (silla, sofá, cuero, flores) → `assets/video/cut-*.webm`; `--clean` repite solo la limpieza |
| `tools/sfx_impact.py` | Sintetiza el golpe de los fondos Black Friday (`assets/sfx/impact.mp3`) |
| `tools/align_fix.py` | Palabras de Whisper corregidas y re-cronometradas (`tools/align/raw_*.json` → `whisper_*.json`) |
| `tools/edit.py` | Tramos (`SEGMENTS`), cortes propios de las tomas (`JUMPS`), pausas recortadas (`TIGHT`), respiraciones (`PAUSE`) y ventanas de los gráficos (`INSERTS`) → `edit.json` |
| `tools/common.py` | Sistema de diseño (el del VSL y los UGC: papel, azul Nawar, tarjetas, pastillas) y utilidades |
| `tools/inserts/ins_NN.py` | Un módulo por gráfico |
| `tools/gen.py` | Genera todo desde `edit.json`; `--solo ins-NN --out <dir>` genera un gráfico suelto |
| `tools/build_audio.py` | Música de fondo («musica v1»): el groove entra en «este Black Friday» |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh            # tomas y música del Drive + medios de marca del VSL; genera todo
npx hyperframes check
npx hyperframes render . --quality high -o renders/nawar-ugc-bf-v6-3.mp4
```

Para cambiar cuándo entra o sale un gráfico, edita `INSERTS` en `tools/edit.py` y vuelve a ejecutar
`python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py`. Para otra combinación de gancho y
cuerpo, cambia `SEGMENTS`: todo va atado a las palabras.
