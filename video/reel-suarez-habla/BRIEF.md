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

### Revisión de la v6

Revisores independientes (gancho y portada, imagen del cierre, sonido y sincronía, regresiones de la entrevista), cada
fallo comprobado por otro agente:
- **Corregido:** el ebook cerrado se quedaba completamente quieto unos 3 s (43,0–46,2 s) mientras sigue la voz. Ahora
  entra un poco más pequeño y crece despacio hasta su tamaño justo cuando se abre (sin cambiar el libro abierto).
- **Al publicar:** la cuadrícula del perfil de Instagram recorta el reel a 3:4 centrado (y 240–1680) y cortaría la
  primera línea del gancho. En «Editar portada → Cuadrícula del perfil», sube el recorte hasta arriba (unos 70 px; por
  ejemplo, y 170–1610).
- Comprobado sin fallos: el gancho no toca ojos ni cejas en ningún fotograma; los emojis salen bien; la entrevista es
  idéntica a la v5; el paso a azul no tiene fotogramas negros; el libro no se corta en ningún fotograma ni tiene halo; el
  volumen de la entrevista (−14,6 LUFS) y del cierre (−15,2 LUFS) casan, con el pico real a −2,2 dBTP; la voz se entiende
  entera; cada texto del cierre entra en su palabra.

## Petición de la v7, la versión final (cliente, 4 nov 2026)

«Me gustaría que saliese todo de una. Voz Yair Narration Spanish. Coge el diseño del título y lo que necesites en esta
página propia del Black Friday del ebook: https://blackfriday.holandesnawar.com/ebook, y que salga casi todo de una para
que la gente no se vaya; el final de "comenta OFERTA y te envío los detalles" sí está bien que aparezca el último. Algo
más guay para el final. El principio, lo de "aprende neerlandés", sigue sin gustarme, muy Android: coge literalmente
estos iconos, 📚 y 🇳🇱, letra Inter extra negrita, efecto contorno negro, tamaño 53 más o menos, algo así como en la
foto [su maqueta: el título en tres líneas con contorno negro y los iconos de Apple a los lados], pero con los iconos
mejor centrados. Tómate tu tiempo para esta versión final.»

- **Gancho:** su maqueta, medida: Inter 800 (la de la propia página, variable), blanco, contorno negro de ≈ 7,5 % del
  tamaño con esquinas redondeadas (sombras en dos anillos: el contorno de CSS deja picos en las tildes), tres líneas.
  Los iconos son los de su maqueta, recortados de ella (el fondo blanco puro que toca el borde se quita; el blanco de las
  páginas y de la franja de la bandera se queda), a ambos lados de la línea del medio y centrados en ella.
- **Cierre:** el sistema de la página (índigo #1D0084 con luces azules y puntos; la pastilla de la cabecera; el título en
  Poppins 700 con degradado blanco y la segunda línea en #4DA3FF; el sello blanco «BLACK FRIDAY 1€ 12,50 €»; «−92 %»;
  la cinta azul claro con ✦; las estrellas y «Más de 40 personas ya lo tienen»). Todo entra en menos de un segundo; el
  libro se abre enseguida. La llamada a comentar es lo último: un campo de comentario de Instagram que escribe «OFERTA»,
  toca «Publicar» y confirma «Te enviamos los detalles por mensaje».
- **Voz:** «Yair - Narration Spanish», el mismo texto. Comprobada con Scribe (lee «Hablan neerlandés» por la unión de
  «habla» con «neerlandés», que es como suena al hablar).
- Los datos de la oferta («1 €», «12,50 €», «−92 %», «Más de 40 personas ya lo tienen») son los de la página.

### Revisión de la v7

Revisores independientes (el gancho frente a la maqueta, el cierre frente a la página, movimiento/sincronía/sonido y
regresiones de la entrevista), cada fallo comprobado por otro agente. Corregido antes de entregar:
- **Iconos del gancho:** con 118 px rozaban la «H» de «Hablando» y la «s» de «neerlandés», y quedaban un poco altos.
  Ahora miden 108 y 88 px y van centrados en las letras de la línea del medio (9 px más abajo): ya no tocan nada.
- **Sello del precio:** tapaba los títulos de las páginas del libro abierto. Ahora va al 78 % y más arriba: solo cubre la
  esquina del libro y su franja azul, como en la página.
- **«1 €»:** con espacio entre el 1 y el €, como en la página (antes se leía pegado).
- **El aviso del mensaje:** sonaba 0,3 s tarde (el archivo empieza con silencio); recortado, suena con la pastilla.
- Comprobado sin fallos: el contorno y los iconos frente a la maqueta, la entrevista idéntica a la v6, el resto del
  cierre (todo entra antes de 43 s salvo la llamada, la cinta sin saltos, sin solapes, dentro de las zonas seguras), la
  voz de Yair entera y clara, y el volumen (−14,7 LUFS en total, −15,1 el cierre, pico real −2,2 dBTP).

## Petición de la v7.1 y la v7.2 (cliente, 4 nov 2026)

«El icono de libro tiene que ir un poquito más abajo para que no toque la H de "Hablando".» (v7.1: los libros, 13 px más
abajo que la bandera; ya no tocan la «H».)

«No me gusta la voz del final, parece barata: usa la de Eleven v4, que es la buena, y con alguna entonación al inicio,
porque si no aburre. Quita lo de "+40 personas lo tienen" y echa un poco abajo la línea azul que va pasando, y así
separamos un poco, que está tan apretado en medio; así bajamos un poco y no toca el título. Que la voz diga "libro", no
"ebook".»

- **Voz (v7.2):** la misma voz (Yair) con el modelo eleven_v4, y «libro». Para la entonación del principio, la primera
  frase va con `[excited]` y signos de exclamación, y el resto con `[warmly]`. De varias tomas, la elegida sube en la
  primera frase (tono medio ≈ 240 Hz) y vuelve al tono normal de Yair en el resto (≈ 156 Hz, como en la v7). Comprobada
  con Scribe: se transcribe igual que el texto.
- **Sin «Más de 40 personas ya lo tienen».**
- **Más aire:** el ebook va al 92 % y 52 px más abajo, el sello 34 px más abajo (el «−92 %» queda a unos 45 px del
  título) y la cinta azul 18 px más abajo y algo más fina, con unos 40 px de aire bajo el libro. La llamada a comentar
  sigue dentro de la zona segura (termina en y ≈ 1496).
