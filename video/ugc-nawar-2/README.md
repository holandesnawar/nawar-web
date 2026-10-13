# Anuncio UGC #2 · Formación Nawar (Meta / TikTok Ads, 9:16) — proyecto HyperFrames

Segundo anuncio en vertical (1080×1920, ~61 s) con el mismo estilo que el primero (`../ugc-nawar`).
- Ella habla siempre a cámara con la toma de frente (UGC.POV1). El cambio de ángulo es un primer plano de la misma
  toma (cámara B); UGC.POV2, de lado y mirando fuera de cámara, no se usa.
- Cuando explica algo, la imagen corta a un gráfico a pantalla completa con el diseño del VSL y vuelve a ella.
- Subtítulos blancos y limpios.
- Arranca con un zoom cerrado sobre su cara que se abre para descubrir el portátil, y cierra con el botón «haz clic».

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md` | Petición del cliente, público, reglas de marca |
| `STORYBOARD.md` | Plano a plano: qué aparece en cada frase y con qué movimiento |
| `edit.json` | El montaje: tramos de la toma (con su cámara, A o B), ventanas de cada gráfico y cada palabra con su tiempo en el vídeo |
| `index.html` | Montaje final (lo genera `tools/gen.py`): la chica (cámara A y su primer plano, cámara B), su encuadre, música y efectos |
| `compositions/ins-NN.html` | Los gráficos a pantalla completa (uno por explicación) |
| `compositions/outro.html` | El botón «MATRÍCULA» con cursor del cierre |
| `compositions/captions.html` | Subtítulos palabra a palabra |
| `tools/edit.py` | Tramos de la toma y su cámara (`SEGMENTS`, cortes en silencios) y ventanas de los gráficos (`INSERTS`) → `edit.json` |
| `tools/common.py` | Sistema de diseño compartido (el `frame.md` del VSL en 9:16) y utilidades |
| `tools/inserts/ins_NN.py` | Un módulo por gráfico; cada uno devuelve su composición y sus efectos |
| `tools/gen.py` | Genera todo desde `edit.json`; `--solo ins-NN --out <dir>` genera un gráfico suelto para revisarlo |
| `tools/build_audio.py` | Música de fondo (el tema del VSL, calmado; casi nada bajo el gancho) |
| `tools/cam_b.py` | Cámara B: el primer plano recompuesto de la toma (`take-1-b.mp4`, mismos fotogramas y sonido) |
| `tools/blur_marks.py` | Desenfoca el logo de HP y la pegatina de Intel del portátil (seguimiento en `tools/align/pov1_logo_track.json`) |
| `tools/align/` | Palabras con tiempos de la toma (Whisper) y el seguimiento del logo |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh            # la toma (UGC.POV1) desde el Drive + medios de marca del VSL; genera todo
npx hyperframes check
npx hyperframes render . --quality high -o renders/nawar-ugc2-v2.mp4
```

Para cambiar cuándo entra o sale un gráfico, edita `INSERTS` en `tools/edit.py` y vuelve a ejecutar:

```bash
python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
```

Todo va atado a las palabras, así que se recoloca solo.
