# SPEC — “El aviso que cruza las capas”

GOAL:    al terminar, el viewer dice «la UI lee Room; la red sólo lo actualiza» y
         puede nombrar las 6 paradas del aviso (Hilt → Dominio → Red → Mapeo →
         Repositorio → Room → UI), con el modo offline como prueba final.
OUTPUT:  HyperFrames, 1920x1080, 30 fps, MP4.
TIME:    540 s x 30 = 16200 frames (9:00; el mínimo pedido era 8:00). Rejilla
         conceptual de 120 BPM = 0.5 s/beat = 15 frames/beat; cortes en
         múltiplos de 0.5 s. Voz en español con Kokoro-82M local (ef_dora):
         11 pistas, una por capítulo, 527 s de narración; el texto sigue siendo
         portador en pantalla. Sin música ni efectos; ver REVIEW.md.
LOOK:    ground #0D1117 a sangre (superficie de editor, sin rejilla decorativa);
         panel #161B22 con borde #30363D; ink #F0F6FC, ink-dim #8B949E;
         código JetBrains Mono 28 px / line-height 38 px con sintaxis Darcula
         (kw #CF8E6D, str #6A8759, fn #56A8F5, cm #7A7E85);
         display Inter 800, título 64 px (5.9% de la altura, tracking -2%),
         sub 30 px, capítulo 24 px; acento verde Android #3DDC84 reservado a
         la palabra clave de cada capítulo, estados de éxito y la claim;
         azul #38BDF8 para nombres de capa y líneas de conexión;
         único material cálido: ficha papel #F6F1E7, 420x250, radio 10 px,
         rot -2°, sombra 0 14px 34px rgba(0,0,0,.5);
         grano 0%, viñeta 0%, degradados 0, glow 0.
OBJECTS: (1) ficha “Aviso” — tab mono NoticeDto → NoticeEntity → Notice,
         campos reales id notice_1 · user_id user_123 · email user@test.com ·
         text Texto de aviso · createdAt 2025-01-01T10:00:00Z;
         (2) editor con código real de los archivos del repo, resaltado de
         línea y gutter; (3) grafo Hilt con 3 módulos y 12 proveedores;
         (4) tubería HTTP: Config → OkHttp(2 interceptores) → Retrofit →
         NoticeResponseDto; (5) tabla Room notices v1 y ondas Flow;
         (6) teléfono Compose con banner offline y LazyColumn;
         (7) interruptor de red online/offline; (8) checksum verde de 13 @Test.
MOTION:  arrivals expo.out / power4.out 0.35–0.6 s; blur-in de palabras
         6 px→0 en 0.13–0.18 s (nunca fade+slide-up); salidas power3.in
         0.35–0.5 s (40–50% más cortas que las entradas); whoosh horizontal
         en cada handoff (sale derecha, entra izquierda, misma velocidad);
         scale 0.9→1 back.out(1.4) sólo en badges y sellos; líneas de
         conexión scaleX 0→1 origin left 0.4 s power2.out; ficha viaja con
         x, rotación fija en el hijo; cámara estática; un tween por move;
         todo lo visible es función del tiempo del timeline.
SHOTS:   f0–f600     S1 hook: ficha aterriza 0–0.6, pregunta por palabra
                     1.2–2.4, línea HTTPS→DTO→Room→Flow→UI 4–5, ficha sale
                     derecha 17–19.5. Thumbnail = frame 0 con la ficha.
         f600–f2100   S2 Hilt: marker 0.5, @HiltAndroidApp 2, @AndroidEntryPoint
                     7, hiltViewModel 12, módulos 18/25/32, "12 · 3 · 1" 39,
                     ficha cruza el grafo 43–48.
         f2100–f3300  S3 dominio: Notice 2, interfaces 8/16, "sin Android" 24,
                     ficha cambia tag a Notice 30, sale 37.
         f3300–f5700  S4 red: Config 2, Endpoints 7, interceptor 13, header
                     resaltado 17, logging 21, Retrofit 27, @GET 33,
                     NoticeResponseDto 39, "paginación recibida, no usada" 47,
                     paquete recorre la tubería 54–64, ficha tag DTO 68.
         f5700–f7500  S5 mapeo: DTO 2, toEntity 12, Entity 16, orEmpty 22,
                     toDomain 28, Notice 32, "DTO ≠ Entity ≠ Notice" 39,
                     código toDomain 45, sale 55.
         f7500–f9600  S6 repositorio: LEER observeNotices 3, Flow 10,
                     ESCRIBIR refreshNotices 16, runCatching 22, saveNotices 28,
                     convergencia en Room 34, claim parcial 41, Result 47,
                     assertEquals verde 54, sale 65.
         f9600–f11400 S7 Room: Entity 2, DAO query 8, fila notice_1 16,
                     INSERT REPLACE 26, ondas Flow 30/36/42, "consumo_datos.db
                     · v1" 46, firma del DAO 51, sale 57.
         f11400–f13200 S8 UI: _uiState/uiState 2, update 8, teléfono 16,
                     collectAsStateWithLifecycle 22, LazyColumn 28,
                     ficha cae en la lista 42, sale 55.
         f13200–f14700 S9 offline: onAvailable 2, onLost 10, red se apaga 12,
                     banner 18, "if (isOnline)" se apaga 26, ficha permanece
                     32, ondas Room 36–44, "Sin red. Con datos." 45.
         f14700–f15750 S10 email + pruebas: @POST 2, sendEmail 6, DTO 11,
                     JSON 16, 13 @Test 21, BUILD SUCCESSFUL 26, 6 fakes 30.
         f15750–f16200 S11 cierre: diagrama completo 0–1.5, claim por palabra
                     2–4, hold hasta f16200 (última línea 3 s).
BANNED:  void oscuro con cosas flotando (cada escena está llena de código o de
         un objeto concreto); glow/bloom/neon/partículas; degradados; glass
         cards; cream+serif; todo centrado; todo fade+slide-up; tres cards en
         fila; KPI grids; logo en esquina; títulos que siguen moviéndose tras
         aterrizar; loops de respiración; typing como apertura; cifras
         inventadas (13 @Test, 12 proveedores, 3 módulos, 2 interceptores,
         1 entidad y v1 salen del código real; BUILD SUCCESSFUL sale de la
         guía de tests del repo, no de una ejecución nueva); exponer la ApiKey
         literal (se muestra como ********).
QA:      f0 (ficha+pregunta), f600 (seam 1), f1800 (módulos Hilt), f4200
         (interceptor + header), f6900 (DTO→Entity), f9300 (dos lanes SSOT),
         f11100 (ondas Flow), f12900 (ficha dentro del teléfono), f14300
         (banner offline + ficha viva), f15600 (13 @Test), f16150 (claim).
