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
  - el texto de la pared («De hoorspecialist») queda fuera de cada encuadre: los planos que lo rozan tienen el borde
    derecho un poco a su izquierda, sin borrar nada (así no se toca la oreja del dependiente);
  - la tarjeta roja se repinta entera de rojo liso, sin tocar los dedos (en sus dos primeros fotogramas es solo un
    borrón de movimiento y se deja), y a la blanca se le quita la estrella (`LOGOS`);
  - en el plano 928 la ventana se queda a la izquierda del remolino naranja del escaparate todo lo que se puede sin
    cortarle la cara; el trocito que queda junto a su mandíbula (0,3 s) no se borra, porque borrarlo le mancha la mejilla.
- **Gancho (v7, el diseño final del segundo reel, `../reel-suarez-habla`):** «Aprendiendo / neerlandés con / Luis
  Suárez» en Inter ExtraBold blanco con un contorno negro grueso y redondo, y los iconos 📚 y 🇳🇱 a los lados de la línea
  del medio (`tools/img`). Está desde el primer fotograma (es también la portada) y se va a los 3,3 s. Va sobre el pecho
  y no arriba como en el segundo reel, porque aquí las caras están arriba en esos planos (la de Suárez y luego la del
  dependiente, cuya boca llega a y ≈ 890). Ya no hay pastilla pequeña arriba.
- **Cierre (v14, el PDF del método):** la pantalla índigo del cierre del segundo reel, entera en ~1 s: la pestaña roja
  «Black Friday · Últimas plazas» (sin sombra, con un punto que parpadea), «Recibe el PDF / de nuestro método / y comienza
  a hablar neerlandés ya», un mockup de la guía «Método THUIS» del cliente (`docs.holandesnawar.com/dossier/MÉTODO.pdf`):
  la portada recta delante y «Lo que incluye» y «Te lo han explicado en el idioma equivocado» abiertas detrás, giradas a
  los lados (`METODO_PAGES`); con aire debajo, la cinta azul clara (clases en directo cada semana, desde el español,
  autoestudio incluido, 16 semanas, dudas en menos de 24 h, certificado) y, con su propio espacio, el botón «Comenta
  QUIERO / y te lo enviamos por mensaje», sin sombra y sin escribir nada. Voz de Yair (`TEMPO` 1,1): «Recibe el PDF de
  nuestro método y comienza a hablar neerlandés ya. Este Black Friday quedan las últimas plazas: comenta QUIERO y te lo
  enviamos por mensaje.» (Las versiones anteriores del cierre están en git.)
- **Subtítulos (v7: abajo, como en el segundo reel, de pie sobre y = 1500):** por frases cortas, sincronizados palabra a palabra (ElevenLabs Scribe):
  - el holandés grande y en mayúsculas, todo al mismo tamaño y en dos líneas como mucho, con la palabra que se está
    diciendo en amarillo; los cortes de línea van marcados con «|» en `PHRASES`, para no dejar una palabra sola ni
    partir un nombre;
  - el español debajo, en una pastilla gris, en una sola línea donde cabe (y si no, en dos líneas equilibradas);
  - en los primeros planos de Suárez el bloque sube a la nariz para que se le vean los labios. Cambia de altura solo
    en los cortes: las frases que cruzarían uno empiezan o terminan en él. La sombra de abajo se quita ahí, para no
    oscurecerle la boca.

  El español conserva los juegos de palabras del anuncio:
  - «fluiten» → pitar: los árbitros le pitan;
  - «bank» → banco / «chupar banquillo»;
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
| `tools/esrgan_onnx.py` | Convierte el modelo de Real-ESRGAN a ONNX sin PyTorch (lee los pesos sin ejecutar el pickle) |
| `tools/fetch_assets.sh` | Lo reconstruye todo desde el Drive |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh
npx hyperframes check
npx hyperframes render . --quality high --fps 25 -o renders/reel-suarez-v15.mp4
```

Para cambiar una traducción o cortar una frase de otra manera, edita `PHRASES` en `tools/subs.py` y ejecuta
`python3 tools/subs.py && python3 tools/gen.py`. Para cambiar un encuadre, edita `SHOTS` en `tools/frame.py` y ejecuta
`python3 tools/frame.py && python3 tools/gen.py`.
