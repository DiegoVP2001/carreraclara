# TAREA 19 — Animaciones y microinteracciones

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T15b** — Panel lateral de filtros en instituciones_v2 (Tipo, Área, Acreditación mín., Empleabilidad mín., Arancel máx., Duración máx.).
- **T16** — Compartir URL: `#c=slug1,slug2` en index_v2; `#i=id1,id2` en instituciones_v2.
- **T17** — "Dónde se imparte" en index_v2: stats bar, badges tipo+acreditación, sort, regiones compactas.
- **T18** — Gráfico Arancel rediseñado: ordenado por valor, color por tipo (Universidad/IP/CFT), línea promedio.

## Qué hace esta tarea

Agregar animaciones y microinteracciones que mejoren la percepción de rapidez y respuesta.

Candidatos principales:
- **Transición al agregar/quitar tarjetas** — fade-in/slide-in al agregar, fade-out al quitar combo (en ambas páginas)
- **Skeleton loader** — mientras se cargan los gráficos o los datos (si aplica)
- **Hover/focus states** en botones y tarjetas — ya existen pero podrían refinarse
- **Toast de "¡Enlace copiado!"** — ya tiene visibilidad CSS; revisar si puede mejorar

Antes de implementar, revisar:
- Qué interacciones existen actualmente que ya tienen transición CSS.
- Qué nuevas animaciones aportarían valor sin sobrecargar la UX.
- Preferencia: CSS transitions/animations sobre JS animation libraries (sin dependencias nuevas).

## Archivos a tocar

- `web/index_v2.html` (principalmente)
- `web/instituciones_v2.html` (principalmente)

## Criterio de "tarea completa"

- Al agregar una combinación, la tarjeta aparece con una transición suave.
- Al quitar una combinación, la tarjeta desaparece con transición suave (sin salto de layout brusco).
- Se abre en el navegador y Diego confirma visualmente.
- `PLAN.md` actualizado con T19 ✅.
