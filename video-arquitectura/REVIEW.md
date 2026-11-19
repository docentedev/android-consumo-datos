# REVIEW — El aviso que cruza las capas

## Decisiones creativas
- Se construyó el guion **“El aviso que cruza las capas”**, elegido por el usuario entre tres opciones
  (`STORYLINES.md`). Los otros dos («El mapa que se dibuja» y «DTO ≠ Entity ≠ Notice») quedaron
  guardados pero no se produjeron.
- Una escena por capítulo (11 escenas / 540 s). El objeto portador es la ficha **Notice**, que cruza
  todo el metraje y sobrevive al corte de red. El cierre usa la misma estación de trabajo de los
  videos anteriores del repo (fondo `#0D1117`, verde Android `#3DDC84`, azul `#38BDF8`, tipografía
  Inter + JetBrains Mono).
- Toda cifra y todo fragmento de código salen del checkout `17ba569` (rama `feature/result-01`):
  13 `@Test`, 34 archivos `.kt`, 3 módulos Hilt, 12 proveedores, 2 interceptores, 1 entidad Room v1,
  6 fakes. La ApiKey se muestra como `********`, nunca literal. El guion de voz se contrastó contra
  ese mismo commit: se corrigió la frase que reducía la capa UI a dos archivos cuando son tres
  (`NoticeViewModel`, `NoticeScreen`, `NoticeUiState`).
- **Con voz en español**, añadida a petición del usuario: Kokoro-82M en local, voz `ef_dora`, modelo
  gratuito y sin credenciales. Once pistas, una por capítulo, ajustadas a la duración de su escena
  (527 s de narración sobre 540 s de video). El texto de la narración está en `narration.json` y se
  regenera con `tools/build_narration.py`. El video sigue llevando todo el contenido en pantalla: la
  voz acompaña, no sustituye al texto. No hay música ni efectos.

## Medido
- `npx hyperframes check`: **0 errores** en las cuatro puertas (lint, runtime, layout, motion);
  contraste **81/81** en WCAG AA.
- `snapshot --review`: 22 fotogramas de beat + 10 seams + 2 hojas de teléfono (360 px) en
  `.hyperframes/artifacts/snapshots/14c1937c-…/`. El OCR de esos frames confirma que los 11 beats
  y sus títulos están presentes y en orden.
- Se partieron las líneas de código más largas (`Config.PRODUCTION`, `@GET getNotices`, `@Query`,
  `StateFlow.asStateFlow`, `SendEmailRequestDto`) para que no se cortaran dentro del panel.

- Render final `renders/architecture-9min-voz.mp4`: 540.000 s, H.264 + AAC 48 kHz estéreo, 21.7 MB;
  `volumedetect` confirma voz no silenciosa en varias muestras (5, 100, 300 y 530 s) y el OCR de
  frames del MP4 confirma los beats de esos momentos.

## No medido / no visto
- En esta sesión el agente **no pudo ver las imágenes directamente**: la revisión visual se hizo por
  OCR (Vision de macOS) sobre los snapshots y por los análisis automáticos de layout/contraste.
  La inspección visual final queda para el usuario en el Studio preview.
- La voz se generó y se midió, pero no se escuchó: la revisión fue por duración, timing y transcripción,
  no por oído. El usuario debe escuchar el render final.

## Plano más débil
- **S9 offline** (440–490 s): el cambio `online → offline` y el banner succionan toda la atención
  mientras la ficha permanece quieta. Con más tiempo se animaría también el borde de la ficha para
  que el objeto portador siga guiando la mirada. El solape se resolvió apagando `● online` a los
  10.5 s, antes de que aparezca `○ offline`.

## Warnings conservados a propósito
- Sin música ni efectos: la narración ocupa el canal de audio y el texto sigue siendo portador.
- `dead_stretch`: las pausas largas son tiempo de lectura del código en pantalla, no huecos; se
  prefirió dejarlas antes que acelerar la lectura de fragmentos reales.
- `text_below_floor` en la barra de archivos y en etiquetas pequeñas de la ficha: son rótulos de
  contexto («texture»), no texto de lectura; el contenido portador va a 28 px o más.
- `timeline_track_too_dense`: cada sub-composición es deliberadamente un capítulo completo; partirla
  más rompería la unidad de la escena que pide el guion.
- `text_box_overflow` residual (19 avisos de información): líneas de código casi al límite del panel;
  el panel recorta con `overflow:hidden` y las identificaciones clave siguen legibles.
