# Anuncio UGC #2 · Formación Nawar (Meta / TikTok Ads, 9:16) — proyecto HyperFrames

Segundo anuncio en vertical (1080×1920, ~64 s) con el mismo estilo que el primero (`../ugc-nawar`).
- Montaje a dos cámaras que se alternan por frase: UGC.POV1 (de frente) y UGC.POV2 (de lado). En el cierre ella se
  gira hacia la cámara de lado y le habla («rellena el formulario… te atenderá»).
- Cuando explica algo, la imagen corta a un gráfico a pantalla completa con el diseño del VSL y vuelve a ella.
- Subtítulos blancos y limpios.
- Arranca con un zoom cerrado sobre su cara que se abre para descubrir el portátil, y cierra con el botón «haz clic».

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md` | Petición del cliente, público, reglas de marca |
| `STORYBOARD.md` | Plano a plano: qué aparece en cada frase y con qué movimiento |
| `edit.json` | El montaje: tramos de cada toma, ventanas de cada gráfico y cada palabra con su tiempo en el vídeo |
| `index.html` | Montaje final (lo genera `tools/gen.py`): la chica (las dos cámaras), su encuadre, música y efectos |
| `compositions/ins-NN.html` | Los gráficos a pantalla completa (uno por explicación) |
| `compositions/outro.html` | El botón «MATRÍCULA» con cursor del cierre |
| `compositions/captions.html` | Subtítulos palabra a palabra |
| `tools/edit.py` | Tramos de cada toma (`SEGMENTS`: qué cámara dice cada frase, cortes en silencios) y ventanas de los gráficos (`INSERTS`) → `edit.json` |
| `tools/common.py` | Sistema de diseño compartido (el `frame.md` del VSL en 9:16) y utilidades |
| `tools/inserts/ins_NN.py` | Un módulo por gráfico; cada uno devuelve su composición y sus efectos |
| `tools/gen.py` | Genera todo desde `edit.json`; `--solo ins-NN --out <dir>` genera un gráfico suelto para revisarlo |
| `tools/build_audio.py` | Música de fondo (el tema del VSL, calmado; casi nada bajo el gancho) |
| `tools/blur_marks.py` | Desenfoca el logo de HP y la pegatina de Intel del portátil (seguimiento en `tools/align/pov1_logo_track.json`) |
| `tools/align/` | Palabras con tiempos de cada toma (Whisper) y el seguimiento del logo |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh            # las tomas y la lección del profe desde el Drive + medios de marca del VSL; genera todo
npx hyperframes check
npx hyperframes render . --quality high -o renders/nawar-ugc2-v4.mp4
```

Para cambiar cuándo entra o sale un gráfico, edita `INSERTS` en `tools/edit.py` y vuelve a ejecutar:

```bash
python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
```

Todo va atado a las palabras, así que se recoloca solo.
