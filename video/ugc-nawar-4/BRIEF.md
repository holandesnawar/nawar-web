---
workflow: general-video
flow: automation
storyboard: no
message: "Nuestro Black Friday empieza hoy: el libro «Holandés sin miedo» para principiantes, explicado en español, por 1 € hasta el 30 de noviembre; quien lo consigue entra en la lista prioritaria y ve antes que nadie lo que preparamos para el Black Friday (la Formación Nawar)."
destination: meta-tiktok-ads
aspect: 1080x1920
language: es
audience: hispanohablantes que viven en Países Bajos y van dejando el neerlandés para el mes que viene
length: 46s
angle: ugc-ad
---

## Intent

Petición del cliente (5 nov 2026): «Vamos con otro UGC: te lo dejo en el Drive. Sería como el de Black Friday, pero no
tanto así, sino como los primeros que hicimos sobre la formación. Dale con una v1. Está en la carpeta de UGC, con todos
los detalles.»

- Contenido de Black Friday (la oferta del libro a 1 € y la lista prioritaria), con el lenguaje de los UGC #1 y #2 de
  la Formación: ella a cámara; cuando explica, gráfico a pantalla completa sobre papel o azul Nawar y vuelta a ella;
  subtítulos blancos; cierre con el botón azul.
- Nada del vestido Black Friday del último anuncio: sin fondos de texto gigantes detrás de ella, sin amarillo ni negro.
  Solo una etiqueta blanca discreta en el gancho («Black Friday anticipado») y la mención en los gráficos de la oferta.

## Assets

- .raw/pedido.mov «Estado de pedido FO4233.mov» (Drive, carpeta «UGC», 4 nov, 83 s, vertical): todo el anuncio de una
  vez, con repeticiones. Las mejores tomas (`tools/edit.py`):
  - gancho «Nuestro Black Friday empieza hoy. Sí, antes de tiempo.», tres veces: la primera (las comillas con las manos
    desde el primer fotograma; la más viva);
  - «…y no es falta de ganas…», dos veces: la segunda (más alta y con más energía: 254 Hz de tono medio frente a 208);
  - «Si empiezas ya, en Navidad vas a entender…», dos veces: la segunda («cosas que antes se te escapaban», mejor frase
    que «…que antes ni sabías», y con más energía);
  - «Quien lo consiga entra en nuestra lista prioritaria…»: la última, la única completa;
  - «Solo hasta el 30 de noviembre», dos veces: la primera (la mano junto a la boca, como contando un secreto; más
    entonación).
- «Animación Libro» (7 s, fondo negro): la portada de «Holandés sin miedo» se abre, pasan las páginas y se cierra.
- Logo, tipografías y efectos del VSL; música: «musica v1» del cliente (la de UGC #2 y del anuncio de Black Friday).
- El documento «UGC 3» de la carpeta no se ha podido leer: docs.google.com no está permitido en la red de esta sesión.
  La v1 sigue lo que ella dice en la toma.

## Customizations

- Neerlandés de los gráficos revisado (como nativo): «En toen stond hij met z'n mond vol tanden!» (un modismo que un
  principiante no pilla: por eso sonríes sin saber de qué) y «Fijne feestdagen! Ga je met kerst naar je familie?».
- Los datos de la oferta (1 €, 12,50 €, hasta el 30 de noviembre) son los de la página de Black Friday.

## Revisión de la v1 (antes de entregar, v1.1)

Cuatro revisores independientes (voz y montaje, gráficos y subtítulos, continuidad de imagen, sonido) y cada hallazgo
comprobado por otro agente. Confirmado y corregido:
- «Por eso lo abrimos ahora» sonaba unos 8 LU más alto que la frase de antes: −3,6 dB en esa frase y +2 / +2,5 dB en
  las dos anteriores (`SHOT_GAIN` en `tools/gen.py`).
- Subtítulos: «y no / es falta de ganas» separaba la negación de su verbo → «y no es / falta de ganas,».
- La etiqueta «Black Friday anticipado» tapaba su pelo y su frente → sobre su camiseta, encima de los subtítulos.
- En el calendario la nota partía los números de los días por la mitad → ocupa justo la última semana.
- El último fotograma congelado era el primero de un parpadeo y uno por delante del vídeo → el fotograma anterior, con
  los ojos abiertos.
- El corte de «…el mes que viene.» a «Por eso lo abrimos ahora» no cambiaba de encuadre → ahora todo corte dentro de
  ella cambia de encuadre.
- «nadie» se cortaba en seco → llega hasta el corte propio de la grabación, con un fundido de 35 ms.
- El sonido de «Pospuesto» no se oía → más alto (sigue más de 10 dB bajo la voz).
Descartado tras comprobarlo: finales de «febrero», «euro» y «escapaban» (cortes propios de la grabación, sin clic ni
pérdida de la palabra), la /s/ de «siempre», los «sparkle» y los márgenes de ins-01 e ins-05.


## Petición de la v2 (cliente, 6 nov 2026)

«Te he dejado una versión cortada mejor para que no improvises, está en la carpeta BF 2. Me gustaría para el segundo 0:11
un vídeo stock de una mesa, gente hablando como en el descanso del trabajo, riéndose ("en la mesa del trabajo y todos se
ríen y tú no"). La música no me gusta mucho, ya que es el mismo estilo anuncio: otra cosa más tranquila de fondo. No es
"la gemeente" sino "el gemeente"; usa otras frases que sean más dolor para el buyer persona: llamar para hablar con el
casero, ir a una cita del dentista. Dale un lavado al diseño del calendario y al del segundo 0:06, que se ve algo IA. Sobre
la lista prioritaria te dejé un vídeo de cómo es la web, scrolleando.»

- **El corte del cliente** («Cortado BF2 Video.mp4») tal cual: mismo orden, mismas pausas, sin acelerar. Solo se quita
  la frase repetida («…es que siempre hay un motivo para que empieces el mes que viene», dos veces seguidas: va la
  primera). El corte termina en «Solo hasta el 30 de noviembre» (sin «Apúntate…»): el botón sale ahí.
- **0:09–0:14, vídeo de stock** (Mixkit, licencia gratuita): la mesa del almuerzo en la oficina hasta «todos», con la
  frase en neerlandés en una burbuja, y compañeros riéndose desde «todos se ríen», con «¿De qué se ríen?» en «tú sonríes».
- **Música:** la del VSL (la del UGC #1), tranquila, unos 22 LU bajo la voz.
- **ins-01** (0:05): un chat real en un móvil con Laura: «¿Puedes llamar tú al casero?», «¿Me acompañas a la cita del
  dentista?», «¿Vienes conmigo al gemeente?», «¿Me traduces esta carta?».
- **ins-03** (0:16): la pantalla de bloqueo con el recordatorio «Empezar neerlandés» que se pospone de enero a febrero y a
  marzo.
- **ins-06** (0:35): la página real de la lista prioritaria, en un móvil, con su scroll.
