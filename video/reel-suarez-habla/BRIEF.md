---
workflow: general-video
flow: custom
format: 9:16 (1080×1920), 25 fps
---

# Brief · Reel «Suárez habla neerlandés» (segundo reel de Luis Suárez)

## Petición (cliente, 4 nov 2026)

«Buena versión. Te dejé otro vídeo diferente por si podemos hacer lo mismo con ese para un reel. Está bien este
diseño; solo lo de aprende neerlandés, esa etiqueta es fea, la verdad, no es como las que veníamos haciendo, ¿sabes?,
más estilo Apple, bonito.»

## Material (Drive, carpeta «Luis Suárez»)

- «Luis Suarez habla Nederlands.mp4»: entrevista de Sportweek TV a Luis Suárez en el Amsterdam ArenA vacío (4:17, 1280×720,
  25 fps, entrelazado). Lleva el logo «SPORTWEEK.NL» en la esquina, el micrófono con «SPORTWEEK» impreso y, al principio
  y al final, la cortinilla del canal.
- «luis ajax» (un documento de Google): no se ha podido leer desde aquí (la red de este entorno no llega a docs.google.com).

## Decisiones (v1, corregidas en v2)

- **Tres momentos** de la entrevista, uno tras otro (42,4 s), elegidos porque son graciosos y se entienden:
  1. «Het was spannend.» — «Wie?» (no entiende la pregunta y pregunta «¿quién?»).
  2. «Feestje gevierd?» — «Sorry?» — «… in vier… in achtenveertig uur.» (en cuatro… en cuarenta y ocho horas: empieza
     «en cuatro…» y se corrige; en neerlandés el 48 se dice «ocho-y-cuarenta»).
  3. «Ben je blij dat je in de spits staat?» — «Voor mij maakt niet uit… Ik wil alleen maar spelen.»
- **Sin la marca del canal:** fuera la cortinilla «Sportweek TV», el logo de la esquina queda fuera del encuadre y el
  texto del micrófono se borra.
- **9:16 a pantalla completa** sobre su cara, como el primer reel.
- **Etiquetas nuevas, estilo Apple** (blanco esmerilado, Inter, bandera redonda), también en el primer reel (v4).
- **Subtítulos** como en el primer reel. Aquí su cara llena el plano, así que van arriba, sobre el pelo, y se le ven los
  ojos y la boca. Las frases del periodista llevan una pastilla «Periodista».

## Correcciones de la v3 (revisión de la v2)

- **Micrófono:** ya no quedan puntas blancas de letras donde el borde del encuadre corta el micrófono (a los 1,3 s,
  4 s, 10,5 s y 37 s).
- **Portada:** el primer fotograma ya no lleva la mancha roja del micrófono que salía del plano (es una copia del segundo).
- **Título:** la tarjeta, más compacta, va sobre la barbilla y ya no le tapa el labio de abajo.
- **Subtítulos:** las frases de Suárez en dos líneas suben un poco más (ya no tocan las cejas); ninguna frase pasa al
  momento siguiente ni parpadea; «in vier… in achtenveertig uur» sin la repetición; «op» se marca con el primer «op»;
  «Por mí, no hay problema».
- **Encuadre:** más margen a los lados de la cara (24 px del original en vez de 18).
- **Sonido:** el periodista del segundo momento, más bajo (ya no salta entre «Feestje gevierd?» y «Sorry?»), y el
  último momento, más alto (las respuestas de Suárez ya no se quedan 4–5 LU por debajo).

## Petición de la v4 (cliente, 4 nov 2026)

«Subtítulos arriba no, mejor abajo. Arriba la tarjeta esa de aprendiendo neerlandés con Luis Suárez, pero tiene que ser
algo más grande; ahora se ve pequeña. O mejor quita eso y deja solo subtítulos y su traducción abajo. Dame dos versiones
para así elegir mejor.»

- **Las dos versiones** llevan los subtítulos abajo, sobre la barbilla (el bloque se apoya en y = 1500, por encima de la
  franja del texto de Instagram, y a la izquierda de su columna de botones). El holandés pasa de 76 a 66 px y el español
  de 42 a 40 px, para que el bloque tape lo menos posible de la boca. La sombra de arriba pasa abajo.
- **Con tarjeta:** la tarjeta del título, más grande (817 × 200 px en vez de la pastilla pequeña), arriba todo el reel.
- **Solo subtítulos:** sin tarjeta ni pastilla.
- La imagen y el sonido no cambian (los de la v3).

## Petición de la v5 (cliente, 4 nov 2026)

«Está bien, solo que los subtítulos tapan la boca de Luis Suárez. ¿Hay alguna forma de subir un poco la cámara para que
los subtítulos sigan debajo pero no tapen su boca? ¿Y a la vez que esté centrado? Quita lo de "Periodista" del
principio, solo molesta.»

- **Cámara más arriba:** el original no tiene imagen por debajo del encuadre (la ventana 9:16 ya usa toda su altura), así
  que la imagen se acerca un 15 % desde el borde de abajo (`PUSH` en `tools/frame.py`). Su boca pasa de y ≈ 1225 a
  y ≈ 1105 (mediana); se pierde algo de pelo arriba. Los subtítulos ya no le tocan el labio salvo dos ratos en que baja
  la cabeza (3,7–4,2 s y 10,6–11,3 s, el «Ah, nee, nee…» riéndose): 31 fotogramas en vez de 257.
- **Centrado:** su cabeza va en el centro en cada momento (`centres()`), y los subtítulos también, centrados en x = 540
  (antes, en 490): el holandés a 62 px y el español a 38 px, en 744 px de ancho, así siguen fuera de la columna de
  botones. «en cuatro… / en cuarenta y ocho horas» va en dos líneas.
- **Sin «Periodista».**
- Las dos versiones siguen: con la tarjeta grande arriba y solo subtítulos.

## Petición de la v6 (cliente, 4 nov 2026)

«Quería algo así para los primeros segundos arriba, sin que tape la cara de él [una captura con el texto de Instagram:
"Hablando neerlandés sin miedo como Luis Suárez" con 📚 y 🇳🇱]. Para el final, me gustaría algo con la voz de ElevenLabs
presentando nuestro ebook: "habla sin miedo también como Luis Suárez, nuestro ebook para Black Friday por 1 euro, comenta
OFERTA y te enviamos los detalles". Así se apuntan a la lista y ya pueden comprar el ebook: genera alcance y venta a la
vez. Tenemos un vídeo chulo para presentarlo, te lo dejo en la carpeta, y usamos nuestro estilo como siempre, pero no tan
llamativo. Ya está en la carpeta MARIO.»

- **Gancho:** el texto de la captura, en tres líneas equilibradas con los emojis a los lados de la del medio, como en
  ella; los 3,3 primeros segundos, sobre el pelo (y 204–420), sin tocarle las cejas. Sustituye a la tarjeta: la v6 es una
  sola versión.
- **El vídeo del ebook:** en «MARIO» está «Animación libro interactivo.html» (la misma animación que «Animación Libro»
  del anuncio de Black Friday, pero en HTML, con fondo transparente y nítida). Se convierte en vídeo transparente
  fotograma a fotograma, sin la sombra (como en el anuncio de Black Friday).
- **La voz:** «Nawar Def» (la voz en español peninsular de la cuenta), con el texto del cliente ordenado: «Habla
  neerlandés sin miedo, como Luis Suárez. Nuestro ebook, Holandés sin miedo, este Black Friday por solo un euro. Comenta
  OFERTA y te enviamos los detalles.» Comprobada con Scribe: se transcribe igual.
- **Estilo «no tan llamativo»:** el azul y las pastillas del anuncio de Black Friday, sin las filas gigantes ni los
  golpes; la música de ese anuncio, muy de fondo. En el cierre no sale Suárez (no parece que él anuncie el ebook).
- La oferta y la fecha («1 €», «hasta el 30 de noviembre») son las del anuncio de Black Friday.
