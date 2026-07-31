# Prompt para iniciar la Tarea 7 — Comparar instituciones entre carreras distintas

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para ejecutar la Tarea 7 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto, `PLAN.md` (sección "Tarea 7 — Comparar instituciones entre carreras distintas" y la tabla "Roadmap general actualizado"), `mifuturo/queries.py` (capa de consulta ya lista, no se toca el modelo de datos) y `web/index.html` (la pestaña "Comparar carreras" ya construida — reusa sus patrones de UI: `normalizar`/`slugify`, el combobox del selector, `badgeInstitucion`, el patrón `dibujarChart`/`destruirChart` de Chart.js v4, el acordeón por institución de "dónde se imparte") para tener el contexto completo antes de empezar.

**Tu tarea (Tarea 7): construir una pestaña nueva "Comparar instituciones" que permita comparar 2-4 combinaciones institución+carrera completamente distintas entre sí** (ej. "Ingeniería Civil en la PUC" vs. "Medicina en la Universidad de Chile"), a diferencia del panel "dónde se imparte" de la Tarea 6 que solo muestra instituciones *dentro de una misma carrera genérica ya elegida*.

Concretamente:

1. **Define el contrato de datos primero, antes de tocar la UI** (mismo orden que en la Tarea 6 Sesión 2 — evita que selector y export asuman formatos distintos):
   - Decide el grano: usa `hecho_indicadores` (`IndicadorTitulo` en `queries.py` — institución × carrera-título, ya confiable porque viene directo del ancla) en vez de `hecho_oferta` (peor cobertura de join a carrera genérica, ver Tarea 1/4 en `PLAN.md`).
   - Decide un identificador determinista para cada combinación institución+carrera-título (igual de explícito que el slug de carrera genérica de la Tarea 6) y documéntalo.
   - Decide la forma del índice de datos: ¿un `web/data/instituciones.json` plano con todas las combinaciones buscables (institución, carrera_título, área/familia si ayuda al filtro de texto), o algo indexado por institución? Debe soportar el selector del punto 2 sin tener que listar miles de combinaciones de antemano en el cliente innecesariamente — pero el dataset es chico (~1692 filas), así que un único JSON plano es probablemente suficiente; no sobre-diseñes.
   - El **ingreso** a este nivel es `ingreso_banda_texto` (banda ordinal, ej. "De $900 mil a $1 millón"), no numérico continuo — decide cómo graficarlo como categoría ordenada, no como eje numérico. Verifica la API de Chart.js v4 para una escala de categorías ordinales (vía `WebSearch` contra `chartjs.org/docs/latest`, o `context7` si está disponible en tu sesión).

2. **`web/export_instituciones.py`** (nuevo script, mismo patrón que `web/export_json.py`: reusa `queries.py`, no reimplementes consultas) — genera el índice de datos decidido en el punto 1.

3. **Nueva sección/pestaña en `web/index.html`** (o un segundo archivo HTML si decides que mezclar las dos pestañas en un solo archivo se vuelve inmanejable — decide y justifica):
   - Selector nuevo que busca por **institución y por carrera simultáneamente** (no reutiliza el selector de carrera genérica de la Tarea 6 tal cual, porque el espacio de búsqueda es distinto). Reusa `normalizar()` para que la búsqueda siga sin requerir tildes.
   - Permite agregar 2-4 combinaciones institución+carrera como series.
   - Gráficos comparables a los de "Comparar carreras" pero al grano de `IndicadorTitulo`: empleabilidad 1er/2do año, retención 1er año, continuidad de estudios, duración real, e ingreso (banda ordinal, ver punto 1).
   - Maneja el estado "institución sin ficha" (FK colgante) explícitamente en el selector: decide cómo se busca/selecciona una institución sin nombre propio — no puede buscarse por nombre si no lo tiene (ej. ¿se identifica por código + carrera, con un label como "Institución sin ficha (código 165) — Carrera X"?).
   - **No construyas filtros de región/acreditación/tipo todavía** — quedan para la Tarea 8/9 (se evaluará primero si son prioritarios contra cómo lo hace College Scorecard). No te adelantes a esa evaluación.

4. **No tocar `comparador.db`** ni `mifuturo/queries.py` (salvo, si corresponde, un comentario corto documentando una decisión, igual que se hizo en la Tarea 6 Sesión 2 — no se borra dato ni se cambia consulta).

**Verificación antes de cerrar la sesión** (no hay herramienta de navegador en este entorno — verificación de lógica por script, igual que en la Tarea 6 Sesión 2 y su iteración v2; la prueba visual en navegador queda para Diego):
- El script de export corre sin error y genera datos coherentes con `mifuturo/queries.py` (compara un caso real contra `comparador.db` directamente con `sqlite3`, igual que se hizo en la Tarea 6).
- El identificador/slug nuevo es determinista y sin colisiones sobre el dataset real completo (no una muestra).
- Si hay lógica JS nueva no trivial (selector, agregación, formateo de banda de ingreso), pruébala ejecutando las funciones reales contra fixtures sintéticas con Node (extraer el `<script>`, parchear el cierre del IIFE para exponer las funciones, como se hizo en la Tarea 6 — no hace falta reinventar el método, ya está validado en este proyecto).
- Servir con `python -m http.server` desde `web/` y confirmar con `curl` que las rutas nuevas (HTML, JSON) responden 200 y que el contenido es el esperado (igual que se hizo en la Tarea 6).
- Un caso real con institución sin ficha debe poder agregarse a la comparación sin romper nada, mostrando el estado explícito.

Al terminar, actualiza el estado de la Tarea 7 en `PLAN.md` (estado completada, con un resumen de 2-3 líneas de las decisiones de implementación — identificador elegido, forma del índice de datos, cómo se graficó la banda de ingreso ordinal) y deja anotado que la Tarea 8 (auditoría College Scorecard + backlog) puede empezar.
