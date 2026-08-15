# TAREA 24 — "Qué NEM necesito" (pestaña nueva)

## Contexto de arranque en frío

Proyecto: `comparador_carreras` / **Carrera Clara** — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl, en producción en [carreraclara.cl](https://carreraclara.cl) (Vercel, root `web/`, sin build step).

**Estado al inicio de esta tarea:**
- MVP completo y desplegado. Todas las tareas hasta **T23c** cerradas.
- Tres páginas canónicas, cada una un HTML autocontenido (CSS y JS inline, sin bundler):

| Página | Archivo | URL en producción |
|---|---|---|
| Portada | `web/landing.html` | `/` |
| Tipos de carrera | `web/index_v2.html` | `/tipos-de-carrera` |
| Carreras por institución | `web/instituciones_v2.html` | `/carreras-por-institucion` |

- Las URLs limpias vienen de `web/vercel.json` (`rewrites`). **Cualquier ruta nueva necesita su rewrite ahí.**
- `web/sw.js` cachea el HTML con Cache First → **subir `CACHE_VERSION`** (hoy `carreraclara-v3`) al terminar, o los usuarios recurrentes no verán la pantalla nueva.
- Las dos herramientas existentes tienen header con marca clickeable (`<a href="/">`) y botón flotante de feedback con modal. La pantalla nueva debería heredar los dos.
- `landing.html` tiene `<nav class="tabs">` con los tools existentes (Inicio / Tipos de carrera / Carreras por institución) — esta tarea agrega ahí un cuarto ítem.

**Por qué existe esta tarea:** surgió de una pregunta de Diego sobre de dónde sacar el "Promedio NEM 2025 de Matrícula 2025" que se ve en la ficha de mifuturo.cl. La investigación (sesión 2026-08-14) encontró que **el dato ya está descargado y cargado en la base de datos local, solo que nunca se exportó ni se mostró** — no hace falta scrapear nada.

## Qué hace esta tarea

Una **cuarta herramienta de nivel superior**, con su propio tab en el nav: el estudiante elige una carrera y ve, para cada institución/sede/jornada donde se imparte, el **NEM promedio real de los estudiantes matriculados en 2025** (no un requisito oficial — SIES no publica "notas de corte" por NEM, publica el promedio de quienes efectivamente entraron). Esto le da una referencia concreta de "qué tan competitivo es este NEM en esta carrera/institución", cosa que hoy la página no ofrece en ningún lado.

Complementa (no reemplaza) las ponderaciones PAES que ya se exportan (Tarea 9: `ponderacion_nem`, `ponderacion_ranking`, etc. en `data/detalle/<slug>.json`) — esas dicen "cuánto pesa el NEM en tu puntaje de postulación"; el dato nuevo dice "qué NEM tuvo la gente que entró". Juntos dan el cuadro completo.

## De dónde sale el dato (ya investigado, no repetir la búsqueda)

| | |
|---|---|
| Archivo fuente | `mifuturo/Buscador_de_Carreras_2025_2026_SIES_EEE.xlsx` |
| Hoja | `Busc. Carreras 2025-2026` |
| Columnas | `Promedio NEM 2025 de Matrícula 2025` (col. 28) y `Promedio PAES 2025 de Matrícula 1er año 2025` (col. 27) |
| Grano | carrera × institución × sede × jornada — **idéntico** al de `hecho_oferta` / la tabla "Dónde se imparte" de `index_v2.html` |
| Ya cargado en | `mifuturo/processed/comparador.db`, tabla `hecho_oferta`, columnas `promedio_nem_2025` y `promedio_paes_2025` (TEXT, sin parsear a número todavía) |
| Cobertura NEM | 9.898/9.900 filas con valor; 3.142 marcadas `s/i` |
| Cobertura PAES | 8.226/9.900 marcadas `-` (sentinela **distinto** a `s/i` — mismo archivo, dos convenciones de "sin dato" conviviendo; hay que mapear ambas a `NULL` al parsear) |

**Lo que falta para exponerlo (nada de esto existe hoy):**
1. `mifuturo/queries.py` — `OfertaInstitucion` (línea ~97) y su SQL (línea ~294, dentro de `obtener_detalle_carrera_generica` o el nombre vigente de esa función) no seleccionan `promedio_nem_2025` ni `promedio_paes_2025`. Hay que sumarlos, parseando `s/i` y `-` a `None` (mismo patrón que la Decisión 6 de `mifuturo/MODELO_DATOS.md`, documentando ahí el segundo centinela).
2. `web/export_json.py` — no emite estos campos en `data/detalle/<slug>.json` (compárese con las `ponderacion_*`, que sí se emiten desde la línea ~159).
3. Ningún HTML muestra el dato hoy en ninguna parte.

**Nota de calidad de dato ya verificada:** 4.734 filas tienen `promedio_nem_2025` pero `ponderacion_nem = 0` (probablemente IP/CFT con admisión vía NEM directo o admisión especial, sin fórmula PAES) — es decir, el dato es útil incluso donde no hay ponderación PAES. Y 149 filas tienen `ponderacion_nem > 0` pero `promedio_nem_2025 = 's/i'` — casos a marcar explícitamente como "sin dato" aunque el NEM sí pese en el puntaje.

## Decisiones que hay que tomar CON Diego antes de escribir código

1. **Ruta y nombre de archivo.** ¿`web/nem.html` con ruta limpia `/que-nem-necesito` (coincide con el nombre pedido) o algo más corto tipo `/nem`? Necesita entrada nueva en `vercel.json` y `sw.js`.
2. **Flujo de selección.** La forma más barata es reusar el autocomplete de carrera que ya existe en `index_v2.html` y, en vez de construir una pantalla de selección desde cero, cargar `data/detalle/<slug>.json` (que ya trae la lista de ofertas por institución/sede/jornada) y agregar las columnas NEM/PAES a esa misma tabla en la pantalla nueva. Confirmar con Diego si se replica esa UI o se diseña algo distinto.
3. **Qué se muestra por fila.** ¿Solo NEM promedio, o también PAES promedio + las ponderaciones ya existentes (para explicar "en esta institución el NEM pesa 30%, y el promedio de quienes entraron fue 5.8")? Recomendado: mostrar ambos donde existan, porque son las dos piezas que dan sentido a la pregunta "qué NEM necesito".
4. **¿Input interactivo del propio NEM del estudiante?** Esta primera versión, ¿es solo tabla informativa (compara visualmente), o se agrega un campo "ingresa tu NEM" que resalte en verde/rojo las filas donde está sobre/bajo el promedio? Definir alcance del MVP de esta tarea — el input interactivo puede quedar para una iteración futura si se prefiere no comprometerse ahora.
5. **Estados vacíos.** 3.142 filas sin NEM (`s/i`) y 8.226 sin PAES promedio (`-`) — deben marcarse explícitamente como "sin dato", nunca ocultarse ni mostrarse como 0 (regla del proyecto, ya aplicada en el resto del sitio).

## Archivos que probablemente se tocan

- `mifuturo/queries.py` — sumar `promedio_nem_2025`/`promedio_paes_2025` a `OfertaInstitucion` y su SQL; documentar el centinela `-` en `mifuturo/MODELO_DATOS.md`.
- `web/export_json.py` — sumar los dos campos a cada oferta en `data/detalle/<slug>.json`.
- Nuevo: `web/nem.html` (o el nombre que se decida) — pantalla de la herramienta nueva, con header/footer/feedback modal iguales a las otras dos.
- `web/landing.html`, `index_v2.html`, `instituciones_v2.html` — sumar el cuarto tab al `<nav class="tabs">` y a los links cruzados de footer (patrón T20c).
- `web/vercel.json` — rewrite de la ruta nueva.
- `web/sw.js` — subir `CACHE_VERSION` (hoy `carreraclara-v3`) y sumar el archivo nuevo a `PRECACHE_URLS`.
- `PLAN.md` — marcar T24 ✅ al cierre; `TAREA_25_PROMPT.md` (Ficha de institución) queda como siguiente sesión.

## Criterio de "tarea completa"

- El estudiante puede elegir una carrera y ver, por institución/sede/jornada, el NEM promedio real de matrícula 2025 (y PAES promedio donde exista).
- Estados "sin dato" (`s/i` NEM, `-` PAES) marcados explícitamente, nunca ocultos ni en 0.
- Cuarto tab visible y funcional en el nav de las tres páginas existentes.
- URL limpia y compartible (`vercel.json` con rewrite).
- Header con marca clickeable y botón de feedback, igual que las otras páginas.
- Revisada en escritorio y a 375px.
- `sw.js` con `CACHE_VERSION` subida; `PLAN.md` marcado T24 ✅.

## Recordatorio de flujo

Este proyecto avanza por sesiones aprobadas: **plan → aprobación explícita de Diego → ejecución**. Al terminar, levantar el server local (`python dev_server.py`, nunca `python -m http.server`) y abrirle la página en el navegador antes de dar la tarea por cerrada.
