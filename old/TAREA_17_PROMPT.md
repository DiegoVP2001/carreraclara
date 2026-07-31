# TAREA 17 — "Dónde se imparte" mejorado

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T15** — Select "Área" en index_v2 filtra autocomplete de carreras; select "Tipo" en instituciones_v2 filtra autocomplete.
- **T15b** — Panel lateral de filtros en instituciones_v2 (6 filtros con sliders dinámicos).
- **T16** — Compartir URL: `#c=slug1,slug2` en index_v2; `#i=id1,id2` en instituciones_v2. Share bar + toast.

## Qué hace esta tarea

Mejorar la sección "Dónde se imparte" en `index_v2.html` (sección `#seccion-detalle`).

Actualmente muestra una lista de instituciones que ofrecen cada carrera, cargada desde `web/data/detalle/<slug>.json` (lazy load). El diseño es básico.

**Los detalles concretos se definen en plan mode al inicio de la sesión**, revisando primero:
- Qué datos tiene disponibles cada archivo `detalle/<slug>.json` (institución, tipo, región, arancel, duración, acreditación).
- Cómo se está renderizando actualmente (`renderDetallePanels()` en index_v2.html).
- Qué mejoras visuales o de UX agregarían más valor (ej: ordenar por empleabilidad, filtrar por región, mostrar arancel, destacar diferencias entre instituciones).

## Archivos a tocar

- `web/index_v2.html` (principalmente)
- Posiblemente `web/data/detalle/*.json` si faltan campos — consultar primero qué tiene.

## Criterio de "tarea completa"

- La sección "Dónde se imparte" muestra información más útil y visualmente clara para cada carrera.
- Se abre en el navegador y Diego confirma visualmente.
- `PLAN.md` actualizado con T17 ✅.
