# TAREA 18 — Gráfico Arancel 2026 rediseñado

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T15b** — Panel lateral de filtros en instituciones_v2 (Tipo, Área, Acreditación mín., Empleabilidad mín., Arancel máx., Duración máx.).
- **T16** — Compartir URL: `#c=slug1,slug2` en index_v2; `#i=id1,id2` en instituciones_v2.
- **T17** — "Dónde se imparte" en index_v2: stats bar, badges tipo+acreditación, empleabilidad en summary, fix float duración, fix `<th>` nowrap.

## Qué hace esta tarea

Rediseñar el gráfico de **Arancel 2026** en `instituciones_v2.html`.

Actualmente hay un gráfico de barras (Chart.js) que muestra el arancel de las instituciones comparadas. Antes de implementar, revisar:
- Cómo se renderiza actualmente (`renderCharts()` o equivalente en instituciones_v2.html).
- Qué datos de arancel están disponibles en `web/data/instituciones.json`.
- Qué mejoras visuales agregarían más valor (ej: ordenar barras por valor, mostrar promedio como línea de referencia, agrupar por tipo de institución, mostrar rango en lugar de valor único si hay múltiples sedes).

## Archivos a tocar

- `web/instituciones_v2.html` (principalmente)

## Criterio de "tarea completa"

- El gráfico de arancel se ve más claro y útil para comparar entre instituciones.
- Se abre en el navegador y Diego confirma visualmente.
- `PLAN.md` actualizado con T18 ✅.
