# Prompt para iniciar la Tarea 6 / Sesión 2 — Construir el MVP funcional "Comparar"

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para arrancar la Sesión 2 de la Tarea 6 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto, `PLAN.md` (sección "Tarea 6 — Diseño UI del comparador", especialmente las partes B "Spec del MVP", C "Linaje de datos" y "Construcción del MVP") y `mifuturo/queries.py` (capa de consulta ya lista, no se toca el modelo de datos) para tener el contexto completo antes de empezar.

**Tu tarea (Tarea 6 / Sesión 2 del plan maestro): construir el MVP funcional de la pantalla "Comparar carreras"** — que **todo funcione**, sin invertir en estética todavía (eso es la Sesión 3). El criterio de éxito es correctitud y completitud funcional, con un markup limpio y re-skinneable (variables CSS, HTML semántico) para que la Sesión 3 pueda re-pintar sin reescribir lógica.

Concretamente:

1. **`web/export_json.py`** — reusa `mifuturo/queries.py` (no reimplementes las consultas). Genera:
   - `web/data/core.json`: las 190 carreras genéricas con área/familia y la lista completa de benchmarks (sin colapsar), más el resultado de `diagnostico_cobertura()`.
   - `web/data/detalle/<slug>.json`: un archivo por carrera con su oferta (`hecho_oferta`) e indicadores propios (`hecho_indicadores`), para lazy-load desde el cliente.
   - Define un slug determinista (normalización + kebab-case) y documéntalo, porque el JS del cliente necesita generarlo igual para pedir el archivo correcto.
   - Esto resuelve el TODO `seleccionar_benchmark_destacado` dejado en `queries.py`: no se colapsa nada en el build, las 3 vistas de benchmark son lógica de cliente (punto 2).

2. **`web/index.html`** — página estática self-contained (CSS y JS inline, sin build step), que:
   - Permite agregar 2–4 carreras genéricas (autocomplete sobre `core.json`) y las muestra como series/columnas.
   - Implementa los **3 toggles de vista de benchmark** (cliente, sin tocar `queries.py` ni los JSON): "todo lado a lado" (default — una barra por carrera × tipo de institución), "priorizar Universidad" (fallback Universidad → IP → CFT), y "filtro por tipo" (selector global; carreras sin ese tipo se marcan "sin dato").
   - Grafica con **Chart.js** (CDN): ingreso al 4° año, empleabilidad 1er/2do año, retención, y distribución de ingreso (percentiles 10/50/90 al 5° año).
   - Incluye un panel **"dónde se imparte"**: al seleccionar una carrera, carga su `detalle/<slug>.json` (lazy) y muestra la oferta por institución (región, jornada, sede, arancel, vacantes, nivel) más los indicadores propios.
   - Muestra los **estados explícitos sin ocultarlos**: badge "sin comparación nacional" (carreras sin benchmark) y "institución sin ficha" (FK colgante), más un pie de página con los conteos de `diagnostico_cobertura()`.
   - Usa `context7` para confirmar la API vigente de Chart.js v4 antes de escribir el código de los gráficos (evita sintaxis obsoleta).

3. **No tocar `comparador.db`.** En `queries.py`, solo si corresponde, deja un comentario corto en el TODO existente indicando que se resolvió como toggle de cliente en la UI — no se borra el dato ni se cambia la consulta.

**Verificación antes de cerrar la sesión:**
- `python web/export_json.py` corre sin error; `core.json` trae 190 carreras (las 26 sin benchmark con lista vacía, no se caen); se generan los `detalle/*.json`.
- Servir con `python -m http.server` desde `web/` (evita la restricción de `fetch()` sobre `file://`).
- Agregar 2–3 carreras y confirmar que aparecen los 4 gráficos; probar los 3 toggles (default debe ser "todo lado a lado"); elegir una carrera con varios tipos de institución y verificar varias barras; elegir una sin benchmark y verificar el badge.
- Abrir "dónde se imparte" de una carrera y confirmar que carga su `detalle/<slug>.json`; si hay una institución sin ficha, debe verse el badge correspondiente, no un error.

Al terminar, actualiza el estado de la Tarea 6 en `PLAN.md` (marca la Sesión 2 como completada, con un resumen de 2-3 líneas de las decisiones de implementación) y deja anotado que la Sesión 3 (rediseño visual, prompt en `TAREA_6_SESION3_PROMPT.md`) puede empezar.
