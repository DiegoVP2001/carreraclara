# TAREA 15b — Filtros adicionales

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T15** — Select "Área" en index_v2 filtra autocomplete de carreras; select "Tipo" en instituciones_v2 filtra autocomplete de instituciones.

## Qué hace esta tarea

Agregar filtros adicionales a una o ambas páginas. **Los filtros concretos se definen en plan mode al inicio de la sesión**, revisando primero qué campos están disponibles en `web/data/core.json` y `web/data/instituciones.json`.

## Criterio de "tarea completa"

- Los filtros acordados en plan mode están implementados y funcionan.
- Se abre en el navegador y Diego confirma visualmente.
- `PLAN.md` actualizado con T15b ✅.
