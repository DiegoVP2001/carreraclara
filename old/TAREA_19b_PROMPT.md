# TAREA 19b — Animaciones extendidas a más elementos de la página

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T19** — Fade-in/slide-in al agregar tarjetas (`is-entering` + doble rAF); fade-out+scale al quitar (`is-removing` + `transitionend`). Las clases CSS son `.is-entering` y `.is-removing` sobre `li.carrera-card` y `li.combo-card`.

---

## ⚠️ FLUJO OBLIGATORIO: plan → aprobación → ejecución

**Antes de escribir una sola línea de código**, hacer lo siguiente:

1. **Leer ambas páginas HTML completas** y hacer un audit exhaustivo: listar **todos** los elementos que aparecen, desaparecen o cambian de estado dinámicamente (no solo los candidatos listados abajo). Para cada uno anotar: ¿cómo se muestra/oculta hoy? (`hidden`, `display:none`, clase CSS, JS directo) ¿ya tiene `transition`? ¿el cambio es brusco o suave?
2. **Presentar a Diego una tabla de plan** con columnas: elemento / estado actual / propuesta / páginas afectadas / prioridad. Incluir también los elementos descartados y por qué (ya tiene animación suficiente, o el esfuerzo no justifica el efecto).
3. **Esperar confirmación explícita de Diego** antes de implementar nada.

Solo después de la aprobación, implementar en el orden propuesto.

---

## Qué hace esta tarea

Extender el sistema de animaciones ya instalado (T19) a la mayor cantidad posible de otros elementos de ambas páginas, manteniendo siempre CSS transitions/animations puras (sin librerías JS de animación).

Candidatos a analizar (no todos tienen que usarse — el plan lo determina):

**Ambas páginas:**
- **Toast "¡Enlace copiado!"** — ya tiene `.visible` con `opacity` y `transform`; revisar si la transición de salida existe o solo la de entrada.
- **Dropdown de autocomplete** (`#autocomplete-list`) — aparece/desaparece con `hidden`; considerar fade+slide corto.
- **Barra de compartir** (`#share-bar`) — aparece al tener ≥2 items; actualmente puede ser brusco (toggle `hidden`); considerar fade-in.
- **Aviso de usabilidad** (`#aviso-usabilidad`) — similar a share-bar; fade suave.
- **Estado vacío** (`#seccion-vacia`) y sección de gráficos — transición al alternar entre ellos.
- **Gráficos Chart.js** — verificar que la animación built-in esté habilitada; si no, activarla.
- **Badges que aparecen condicionalmente** — micro-fade si se muestran/ocultan dinámicamente.

**instituciones_v2.html específico:**
- **Resultados del panel de filtros** — los combos que se filtran en tiempo real podrían tener micro-fade al actualizarse.
- **Panel de detalle de institución** (si existe uno que se expande) — fade-in al abrir.

**index_v2.html específico:**
- **Panel "Dónde se imparte"** — fade-in al abrir (el panel detalle por carrera).
- **Efecto visual al activar/desactivar checkboxes de tipo** dentro de tarjetas.

## Archivos a tocar

- `web/index_v2.html`
- `web/instituciones_v2.html`

## Criterio de "tarea completa"

- Plan aprobado por Diego antes de implementar.
- Al menos 4 elementos adicionales (fuera de las tarjetas de T19) tienen transición suave.
- Diego abre en el navegador y confirma visualmente.
- `PLAN.md` actualizado con T19b ✅.
- `TAREA_19c_PROMPT.md` ya existe (fue generado junto con este).
