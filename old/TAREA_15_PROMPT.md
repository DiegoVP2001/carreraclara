# Prompt — Tarea 15: Filtros en comparación

## Contexto del proyecto

Estamos construyendo **Carrera Clara**, un comparador de carreras universitarias/IP/CFT para estudiantes chilenos de 4to medio, basado en datos públicos de MiFuturo.cl/SIES. Los archivos activos son `web/index_v2.html` (Comparar carreras) y `web/instituciones_v2.html` (Comparar instituciones).

Roadmap activo en `PLAN.md`. Historial de tareas completadas (1–14) en `PLAN_HISTORIAL.md`.

## Situación actual

Ambas páginas tienen un comparador funcional que muestra tarjetas de carreras/instituciones con gráficos. El usuario agrega manualmente cada ítem uno a uno desde un combobox. No existe ningún mecanismo de filtrado ni exploración previa a la comparación.

**Datos disponibles:**
- `web/data/core.json`: 190 carreras genéricas con campos como `area`, `tipo` (Universitaria/IP/CFT), `nombre`.
- `web/data/instituciones.json`: 1690 combos institución × carrera-título, con campos `tipo_inst`, `region`, `nombre_inst`.

## Qué hacer

Agregar filtros de selección rápida **sobre el selector existente** en ambas páginas (sin reemplazarlo):

### `index_v2.html` (Comparar carreras)

Filtros inline sobre el input de búsqueda:
1. **Área** (select) — valores únicos del campo `area` en `core.json` (ej: Salud, Tecnología, Arte…). Al seleccionar un área, el autocomplete muestra solo carreras de esa área.
2. **Tipo de institución** (toggle-chips: Universitaria / IP / CFT) — filtra qué filas aparecen en los gráficos de barras para la carrera seleccionada (no filtra qué carreras se pueden agregar).

### `instituciones_v2.html` (Comparar instituciones)

Filtros inline sobre el selector de institución:
1. **Tipo de institución** (select: Universidad / IP / CFT) — pre-filtra el listado de instituciones en el autocomplete.
2. **Región** (select) — pre-filtra el listado de instituciones por región (`region` en `instituciones.json`).

## Archivos a tocar

Solo HTML/CSS/JS de:
- `web/index_v2.html`
- `web/instituciones_v2.html`

No tocar: `web/data/`, scripts de exportación, `mifuturo/`.

## Decisiones ya tomadas

- Los filtros son **UI sobre los datos ya cargados en memoria** — no requieren nuevas peticiones de red.
- Los filtros de institución/región en `instituciones_v2.html` afectan el autocomplete (qué instituciones aparecen), no las tarjetas ya agregadas.
- El toggle Universitaria/IP/CFT en `index_v2.html` ya existe en cada tarjeta de carrera — los nuevos filtros de área son adicionales, no reemplazan lo existente.

## Criterio de tarea completa

1. En `index_v2.html`: un select de área visible sobre el input que filtra el autocomplete.
2. En `instituciones_v2.html`: selects de tipo y región que filtran el autocomplete de instituciones.
3. Ambos filtros resetean cuando el usuario borra el input o selecciona "Todas".
4. No hay regresiones en la lógica de comparación ni en los gráficos.

## Al terminar

1. Levantar `python -m http.server 8000` desde `web/` y abrir `Start-Process "http://localhost:8000/index_v2.html"`.
2. Cuando Diego confirme: marcar Tarea 15 como completada en `PLAN.md` y generar `TAREA_16_PROMPT.md`. Mover este archivo a `old/`.
