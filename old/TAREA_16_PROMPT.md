# TAREA 16 — Compartir comparativas (Share URL)

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T15** — Select "Área" en index_v2 filtra autocomplete de carreras; select "Tipo" en instituciones_v2 filtra autocomplete de instituciones.
- **T15b** — Panel lateral de filtros en instituciones_v2 (Tipo, Área, Acreditación mín., Empleabilidad mín., Arancel máx., Duración máx.).
- **T15c** — Favicon implementado.

## Qué hace esta tarea

Permitir compartir una comparativa vía URL. Al tener 2+ carreras o instituciones seleccionadas, el estado de la comparación se serializa en la URL (query params o hash) para que compartir el link restaure exactamente la misma comparación.

**Los detalles concretos se definen en plan mode al inicio de la sesión**, revisando primero:
- Qué identificadores usar como clave para carreras (slugs en `core.json`) e instituciones (IDs en `instituciones.json`).
- Dónde colocar el botón/icono "Compartir" en la UI.
- Si incluir también el estado de los filtros activos en la URL.

## Archivos a tocar

- `web/index_v2.html`
- `web/instituciones_v2.html`

## Criterio de "tarea completa"

- Compartir una URL restaura la comparación al cargar la página.
- El botón/icono de compartir es visible y copia la URL al portapapeles (o abre el diálogo de compartir nativo).
- Se abre en el navegador y Diego confirma visualmente.
- `PLAN.md` actualizado con T16 ✅.
