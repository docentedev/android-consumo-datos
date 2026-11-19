# Storylines — video de la arquitectura de ConsumoDatos

Tres films distintos sobre la misma fuente: la arquitectura real del commit
`17ba569` (`feature/result-01`) y sus guías (`docs/guia-completa-estudiantes.md`,
`docs/integracion-servicio-https.md`, `docs/guia-unit-testing.md`). Ninguno está
construido. Elegir uno ⇒ escribir `SPEC.md` y construir.

Patrones tomados de los videos anteriores del proyecto (`video-remote`, `video-room`,
`video-test`, `tests-paso-a-paso`): 1920×1080 @ 30 fps; un `index.html` con una escena
por capítulo y seams espejados; `SPEC.md` con números y `STORYLINES.md`; editor
Darcula/GitHub a sangre (#0D1117 / #1E1E1E), verde Android #3DDC84 y azul #38BDF8
como acentos, tipografía Inter/Roboto para títulos y mono para código; un objeto
portador (la ficha “Aviso”) que cruza capas; código y cifras reales del repo, sin
datos inventados; sin voz en pantalla.

Supuestos (no preguntados): 8:30–9:30 de duración (el objetivo es ≥ 8 min),
1920×1080 @ 30 fps, sin voz (el texto en pantalla manda, en español), cama de
música del catálogo gratis a 120 BPM; si no hay catálogo sin sesión se entrega en
silencio y se documenta cómo agregarla. Sin elementos de pago.

---

## 1. RECOMENDADO: “El aviso que cruza las capas”

- **Device:** un caso real del repo — `Notice(id="notice_1", text="Texto de aviso",
  createdAt="2025-01-01T10:00:00Z")` — entra por HTTPS, cruza OkHttp → Retrofit →
  `NoticeRemoteDataSource` → `NoticeRepositoryImpl` → Room → `Flow` →
  `NoticeViewModel` → `StateFlow` → `NoticeScreen`, y cuando la red cae sigue
  vivo en la pantalla porque Room lo re-emite. En cada parada cae el pedazo real
  de código que lo mueve y su prueba.
- **Form:** *object-to-object chain* de diez capítulos; la ficha es el portador
  que el ojo sigue y el corte ocurre siempre sobre la ficha (sale por un lado,
  entra por el otro en la escena siguiente).
- **Qué ve y siente:** ve la misma ficha atravesar el sistema y siente que la
  arquitectura se demuestra, no se describe; el clímax es el apagón de red donde
  la ficha permanece en pantalla sin un solo byte nuevo.
- **Primeros 2 s:** frame 0 — la ficha “Aviso” aterriza sobre el editor a sangre;
  a 0.6 s entra «¿qué lee la pantalla cuando no hay red?»; a 2.0 s la ficha sale
  hacia el primer módulo Hilt.
- **Beats:** hook (la pregunta) → `@HiltAndroidApp` + 3 módulos / 12 proveedores →
  dominio (`Notice`, 2 interfaces de repositorio) → red (`Config`, 2 interceptores,
  `@GET`, DTO paginado) → mapeo (`toEntity` / `toDomain`) → repositorio SSOT
  (`observeNotices` vs `refreshNotices`) → Room (`Flow`, `REPLACE`, `notices` v1) →
  ViewModel + Compose (`StateFlow`, `collectAsStateWithLifecycle`, `LazyColumn`) →
  `NetworkMonitor` y banner offline → `@POST send-email` como segundo viaje →
  13 pruebas con fakes → claim: «La UI lee Room; la red sólo lo actualiza».
- **Look:** el editor de los videos anteriores, a sangre, con código real del
  repo y resaltado de línea; ficha de papel claro como único material cálido;
  verde #3DDC84 reservado a estados de éxito y a la palabra clave de cada
  capítulo, azul #38BDF8 para los nombres de capa; una sola idea por cuadro.
- **Sound:** cama a 120 BPM (cortes en beat), tick al aterrizar cada prueba,
  whoosh corto en cada salto de capa, un riser único cuando la ficha sobrevive
  al `onLost`, pop en el `BUILD SUCCESSFUL`.

## 2. “El mapa que se dibuja”

- **Device:** el diagrama ASCII de `docs/guia-completa-estudiantes.md` —
  `[Servidor REST HTTPS] → OkHttp/Retrofit → RemoteDataSource → Repository →
  Room ↔ Flow → ViewModel → Compose UI`, con `NetworkMonitor` entrando desde
  abajo — dibujado desde cero, una arista por capítulo.
- **Form:** *one frame that rebuilds / endless zoom*: el mapa se arma en un solo
  plano y la cámara se sumerge en cada nodo; al nombrarlo, el nodo se abre y
  muestra el archivo real; al salir, vuelve al mapa con una arista más.
- **Qué ve y siente:** ve construirse el plano completo y afterwards lo recorre
  como una maqueta; siente que entiende el todo antes que cada pieza, y que
  cada pieza encaja en el todo.
- **Primeros 2 s:** frame 0 — una línea sola, `[Servidor REST HTTPS]`, en el
  centro; a 1.0 s se dibuja la flecha hacia abajo y a 2.0 s aparece `OkHttp`.
- **Beats:** servidor → interceptor ApiKey → Retrofit + DTO → RemoteDataSource →
  Repository (bifurcación local/remota) → Room (Flow) → NetworkMonitor →
  ViewModel (StateFlow) → Compose (banner + lista) → el lazo SSOT completo →
  claim con el diagrama terminado.
- **Look:** plano de ingeniería sobre #0D1117: rejilla 12 columnas, líneas de
  2 px en azul #38BDF8, nodos con etiqueta mono encima de la parte que nombran,
  acento verde #3DDC84 sólo en la flecha de retorno del `Flow`; sin tarjetas
  flotantes ni leyendas.
- **Sound:** metrónomo suave a 120 BPM que marca cada arista, un clic mecánico
  al trazar cada línea, cama que se densifica a medida que el mapa crece y se
  abre en el lazo final.

## 3. “DTO ≠ Entity ≠ Notice” (la bold: tipo que lleva el argumento)

- **Device:** la misma ficha presentada como tres objetos distintos que no se
  parecen: `NoticeResponseDto` (JSON con `user_id`, `created_at`), `NoticeEntity`
  (tabla `notices`) y `Notice` (modelo de dominio). Cada capa intenta usar la
  equivocada y el error se muestra en pantalla antes de corregirse.
- **Form:** *cut on the beat*, póster suizo a dos tintas: cortes duros cada
  medio beat, tipografía gigante y código real entrando como contraprueba.
- **Qué ve y siente:** ve que las tres capas son tres contratos distintos y que el
  repositorio es la única pieza autorizada a traducirlos; siente el alivio de
  una regla clara después de ver el error.
- **Primeros 2 s:** frame 0 — tres palabras en tipo enorme, `DTO · ENTITY ·
  NOTICE`, con la primera tachada en rojo; a 2.0 s cambia a `DTO ≠ ENTITY`.
- **Beats:** el error de mandar el DTO a la UI → `SerializedName` → `toEntity()`
  → `INSERT OR REPLACE` en Room → `toDomain()` → `Flow` al ViewModel →
  `StateFlow` a Compose → el mismo viaje con `send-email` → la regla en una
  línea → claim: «Ningún DTO llega a la pantalla».
- **Look:** campo plano #101418 y verde Android #3DDC84 alternando por corte,
  tipo Roboto/Archivo Black a 180–240 px, código en mono 28 px, grano de
  impresión 2 %, sin degradados, sin cards.
- **Sound:** cama cortada al beat, un golpe seco por cada tachado, un pop por
  cada traducción correcta, sin ticks de tecla.
