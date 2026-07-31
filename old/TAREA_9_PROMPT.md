# Prompt para iniciar la Tarea 9 — Ponderaciones PAES en datos propios

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para ejecutar la Tarea 9 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto y `PLAN.md` completo (especialmente la sección "Tarea 9 — Ponderaciones PAES en datos propios", el "Addendum 2" dentro de la sección "Tarea 8" donde se confirmaron los datos, y la tabla "Roadmap general actualizado" al final) para tener el contexto completo de las dos pestañas Comparar ya construidas:

- **Comparar carreras** (`web/index.html` + `web/export_json.py`).
- **Comparar instituciones** (`web/instituciones.html` + `web/export_instituciones.py`).

**Tu tarea (Tarea 9): exponer las ponderaciones PAES (NEM, Ranking, Lenguaje, Matemática 1, Matemática 2, Historia, Ciencias, Otros) que ya existen en los datos crudos, sin depender de ninguna fuente externa nueva.**

## Contexto de los datos (ya confirmado en la Tarea 8, no repetir la investigación)

- `oferta/Oferta_Academica_2026_SIES_05_06_2026_WEB_E.xlsx` trae 8 columnas reales de ponderación por componente (`Ponderación Notas`, `Ponderación Ranking Notas`, `Ponderación Lenguaje`, `Ponderación Matemáticas`, `Ponderación Matemáticas 2`, `Ponderación Historia`, `Ponderación Ciencias`, `Ponderación Otros`), al mismo grano que `hecho_oferta` (institución × carrera × sede × jornada) — la misma tabla que ya alimenta "dónde se imparte" (`index.html`) y el arancel cruzado (`instituciones.html`).
- `mifuturo/Buscador_de_Carreras_2025_2026_SIES_EEE.xlsx` también trae una columna `Ponderaciones`, pero con valores sueltos poco estructurados (ej. "NEM", "30") — de menor utilidad directa; no es la fuente principal de esta tarea, solo evalúala si te sirve de respaldo puntual.
- Esto es **distinto del puntaje de corte DEMRE** (que sigue diferido, requiere fuente externa no descargada — no lo intentes en esta sesión).

## Qué hacer

1. **Carga y valida las 8 columnas de ponderación desde `oferta/...xlsx`** con un script exploratorio corto (no definitivo) que confirme: rango de valores esperado (0-100, deberían sumar 100 por fila cuando hay ponderación real), cuántas filas tienen las 8 columnas en 0 (candidato a "sin ponderación PAES reportada" como estado explícito, no error — pero primero verifica si es ausencia legítima, ej. carreras con admisión especial/sin PAES, igual como se hizo con `arancel`/UF en la Tarea 7 Iteración 4) y si hay algún valor fuera de [0,100] o que no sume 100.
2. **Decide el punto de unión a `hecho_oferta`** — ya existe esa tabla cargada en `comparador.db`; estas columnas son nuevas de la misma fuente (`Buscador_de_Carreras`/`Oferta_Academica`, confirma cuál corresponde exactamente a la tabla `hecho_oferta` ya cargada en `mifuturo/loader.py` antes de asumir que es una columna que falta agregar vs. una que ya está cargada y solo no se expone en `queries.py`).
3. **Extiende `mifuturo/queries.py`** de forma aditiva (mismo patrón ya usado para el panel institucional en la Tarea 7 Iteración 4 — no rompas los call sites existentes): agrega las 8 ponderaciones al dataclass que corresponda (`OfertaInstitucion` o el que uses para `hecho_oferta`).
4. **Expón las ponderaciones en los exports** (`web/export_json.py` y/o `web/export_instituciones.py`, según dónde decidas mostrarlas — ver punto 5) con assert de cobertura, igual criterio que el resto del proyecto (nunca ocultar silenciosamente un estado, ej. "sin ponderación PAES reportada" debe ser explícito, no `null` mudo).
5. **Decide dónde mostrarlas en la UI** — candidatos: panel "dónde se imparte" de `index.html` (por sede/jornada, ya que la ponderación varía a ese grano) y/o tarjeta de combo de `instituciones.html`. Como referencia visual rápida, considera un mini gráfico de barras apiladas (las 8 ponderaciones de una fila siempre suman ~100, ideal para barra apilada) en vez de una tabla de 8 números — pero no sobre-diseñes esta sesión; una tabla simple también es válida si el tiempo no da para más, y se puede pulir en la Tarea 11 (polish de tarjetas).
6. **No toques** `comparador.db` salvo que el punto 2 revele que falta cargar una columna nueva en el loader — en ese caso, documenta la decisión igual que se hizo históricamente en este proyecto (ver `mifuturo/loader.py` y su log).

## Restricciones

- No implementes el glosario interactivo (Tarea 10) ni el polish de tarjetas (Tarea 11) en esta sesión — quedan para sesiones separadas, según `PLAN.md`.
- No es necesario esperar a la Tarea 8b (exploración con la extensión Chrome) — esta tarea es independiente de esos hallazgos.

## Verificación antes de cerrar la sesión

(no hay herramienta de navegador en este entorno — verificación de lógica por script, igual que en tareas anteriores; la prueba visual en navegador queda para Diego)

- El script de carga/validación confirma el comportamiento real de las 8 columnas (rango, suma esperada, casos en 0) y lo deja documentado.
- `queries.py` extendido no rompe los call sites existentes (export_json.py, export_instituciones.py, cualquier otro).
- El/los export(s) corren sin error con assert de cobertura nuevo.
- Comparación directa contra `comparador.db`/el Excel fuente para 1-2 casos reales (uno con ponderación normal, uno en el estado "sin ponderación" si existe).
- Si agregaste lógica JS no trivial (ej. gráfico de barras apiladas), pruébala con Node sobre la lógica real extraída del archivo, mismo método ya validado en este proyecto.
- `python -m http.server` + `curl` confirmando 200 en los archivos tocados.

Al terminar, actualiza el estado de la Tarea 9 en `PLAN.md` (estado completada, con un resumen de las decisiones de implementación — qué tabla/columnas exactas, cómo se manejó el estado "sin ponderación", dónde quedó expuesto en la UI) y deja anotado que la Tarea 10 (glosario interactivo) sigue en el roadmap.
