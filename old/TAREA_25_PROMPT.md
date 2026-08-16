# TAREA 25 — Auditoría de datos no considerados por error

## Contexto de arranque en frío

Proyecto: `comparador_carreras` / **Carrera Clara** — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl, en producción en [carreraclara.cl](https://carreraclara.cl) (Vercel, root `web/`, sin build step).

**Estado al inicio de esta tarea:**
- MVP completo y desplegado. Todas las tareas hasta **T24 cerradas** ("Qué NEM necesito" en producción, 4ta herramienta).
- Cuatro páginas canónicas, cada una un HTML autocontenido (CSS y JS inline, sin bundler):

| Página | Archivo | URL en producción |
|---|---|---|
| Portada | `web/landing.html` | `/` |
| Tipos de carrera | `web/index_v2.html` | `/tipos-de-carrera` |
| Carreras por institución | `web/instituciones_v2.html` | `/carreras-por-institucion` |
| Qué NEM necesito | `web/nem.html` | `/que-nem-necesito` |

## Por qué existe esta tarea

En T24 se descubrió que `web/data/instituciones.json` (construido desde `hecho_indicadores`, grano institución×carrera-**título**) **no es superset** de `hecho_oferta` (grano institución×carrera-**genérica**+sede+jornada, de donde sale el NEM/PAES real). Resultado: **1183 combinaciones institución+carrera con NEM/PAES real quedaban invisibles** en el selector de "Qué NEM necesito" porque el selector se armó reusando la fuente de datos equivocada — nadie lo notó hasta que Diego comparó un dato puntual (Ingeniería Civil PUC) contra mifuturo.cl y no calzó.

Ese hallazgo prendió una alarma más general: si esto pasó una vez sin que el pipeline avisara (nada se rompió, no hubo excepción, solo datos silenciosamente ausentes), **puede estar pasando en otras partes del sitio** sin que se haya notado. Esta tarea es una auditoría defensiva — no se espera necesariamente encontrar más bugs del mismo tamaño, pero vale la pena mirar sistemáticamente antes de seguir construyendo sobre supuestos no verificados.

## Qué hace esta tarea

Una revisión **de punta a punta** de la cadena de datos, buscando tres tipos de brecha distintos (son problemas distintos, no mezclar el diagnóstico):

1. **Cargado pero no exportado.** Columnas que existen en `mifuturo/processed/comparador.db` (vía `mifuturo/loader.py`) y son consultables desde `mifuturo/queries.py`, pero ningún script de `web/export_*.py` las emite a JSON. Dato disponible, nunca sale del backend.
2. **Exportado pero no mostrado.** Campos que sí llegan a algún `web/data/*.json`, pero ninguna de las 4 páginas los lee/renderiza en su JS. Dato que viaja al cliente y se descarta.
3. **Cobertura silenciosamente incompleta** (el patrón de T24). Casos donde dos fuentes que deberían representar "lo mismo" (misma institución, misma carrera) en realidad tienen grano o cobertura distintos, y el código asume que una es superset de la otra sin haberlo verificado. El caso ya conocido es `hecho_indicadores` (título) vs. `hecho_oferta` (genérica) — pero conviene revisar si `instituciones_v2.html` mismo (que ya cruza institución+genérica contra `hecho_oferta` vía `resolver_arancel`/`resolver_ponderaciones` en `export_instituciones.py`) tiene algún supuesto similar sin confirmar, y si `index_v2.html` (que cruza `hecho_oferta` con `dim_carrera_generica` vía `Área Carrera Genérica`, con ~23% de valores "otros"/"bachillerato" sin resolver — Decisión 7 de `mifuturo/MODELO_DATOS.md`) esconde algo parecido.

**Fuera de alcance explícito:** los tres datasets nunca integrados (`matricula/`, `titulados/`, `personal/`) — confirmar que efectivamente no hay nada a medio importar de ellos (un `import` suelto, una tabla a medio poblar) es parte de esta auditoría, pero **diseñar cómo integrarlos es trabajo de T26** (el brainstorm), no de esta tarea.

## Método sugerido (referencia, no receta obligatoria)

1. **Fuente → loader.** Para cada dataset fuente (`mifuturo/`, `oferta/`, `matricula/`, `titulados/`, `personal/`), revisar su glosario oficial (`Glosario_*`/`*_GLOSARIO_*`) y comparar la lista completa de columnas contra lo que `mifuturo/loader.py` efectivamente carga a `dim_institucion`/`dim_carrera_generica`/`hecho_indicadores`/`hecho_oferta`/`hecho_benchmark_nacional`. `mifuturo/MODELO_DATOS.md` ya documenta esto para varias tablas — usarlo como punto de partida, no repetir el trabajo, solo confirmar que sigue vigente y llenar los huecos que ese doc no cubrió.
2. **Loader → queries.** Comparar las columnas de cada tabla de `comparador.db` contra los `SELECT` de `mifuturo/queries.py` y los campos de sus dataclasses (`OfertaInstitucion`, `IndicadorTitulo`, `InstitucionInfo`, `BenchmarkNacional`, etc.).
3. **Queries → export.** Comparar los dataclasses contra lo que `web/export_json.py` y `web/export_instituciones.py` realmente escriben a JSON.
4. **Export → pantalla.** Para cada campo de cada `web/data/*.json`, `grep` en las 4 páginas HTML para confirmar que algún `el.innerHTML`/template string lo usa. Ojo con nombres reusados entre archivos (ej. `ponderacion_*` se usa en 3 de las 4 páginas con el mismo componente visual).
5. **El patrón T24 en las otras páginas.** Releer `resolver_arancel`/`resolver_ponderaciones` en `web/export_instituciones.py` (Tarea 7) con la pregunta explícita: "¿esta función asume que institución+genérica es superset de institución+título, la misma asunción que falló en T24?" — y hacer el mismo chequeo cuantitativo que se hizo en T24 (contar pares en un lado que no están en el otro) si aplica.

## Decisiones que ya están tomadas (no volver a discutir)

- **No se corrige nada en esta sesión.** Es una tarea de diagnóstico/reporte, no de implementación. Si aparece un hallazgo obviamente rápido de arreglar, proponerlo a Diego igual — pero el entregable es el informe, no el fix.
- **Distinguir "bug nuestro" de "SIES no lo reportó".** Los sentinelas `s/i` y `-` (ver Decisión 6 y 11 de `mifuturo/MODELO_DATOS.md`) son ausencia legítima de dato en la fuente, no un hallazgo de esta auditoría — se listan aparte solo si su manejo (parseo, exposición como "sin dato") tiene un error real.
- El criterio de confianza de cada hallazgo se reporta explícito: **confirmado** (verificado con una consulta/conteo real) vs. **sospecha a verificar** (se ve raro pero no se alcanzó a confirmar) vs. **descartado** (se investigó y es ausencia legítima, se documenta igual para no reabrir la pregunta después).

## Archivos que probablemente se leen (ninguno se modifica en esta tarea)

- `mifuturo/*.py` (`loader.py`, `queries.py`), `mifuturo/MODELO_DATOS.md`
- `web/export_json.py`, `web/export_instituciones.py`
- `web/landing.html`, `web/index_v2.html`, `web/instituciones_v2.html`, `web/nem.html`
- Glosarios de `mifuturo/`, `oferta/`, `matricula/`, `titulados/`, `personal/`

## Criterio de "tarea completa"

- Un informe (nuevo doc, ej. `AUDITORIA_DATOS_T25.md`) que liste, para cada uno de los tres tipos de brecha, los hallazgos concretos con su nivel de confianza y el archivo/línea donde se verificó.
- Cobertura de las 4 páginas y las 5 fuentes de datos, no solo el área donde ya se encontró el bug de T24.
- Confirmación explícita (aunque sea "nada raro encontrado") sobre `matricula/`, `titulados/`, `personal/`.
- `PLAN.md` marcado T25 ✅ con un resumen de 2 líneas del hallazgo principal (si lo hay).

## Recordatorio de flujo

Este proyecto avanza por sesiones aprobadas: **plan → aprobación explícita de Diego → ejecución**. Dado que esta tarea es de investigación, el "plan" puede ser simplemente confirmar el método antes de empezar a recorrer archivos — no hace falta un plan tan detallado como en una tarea de implementación.
