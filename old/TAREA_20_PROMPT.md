# TAREA 20 — Optimización móvil

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T13** — Layout 3 columnas responsivo (3/2/1 col por breakpoint).
- **T17** — Sección "Dónde se imparte" con stats bar, badges, tabla de instituciones.
- **T19b** — Custom selects animados en filtros (fade + chevron rotate).
- **T19c** — Hover/focus en cards, buttons, inputs, summaries.
- **T19d** — Animaciones bidireccionales en acordeones "Dónde se imparte" e institution-cards; filtros del panel como custom selects; zebra stripes + sticky header en tabla.

---

## ⚠️ FLUJO OBLIGATORIO: plan → aprobación → ejecución

**Antes de escribir una sola línea de código**, hacer lo siguiente:

1. **Auditar ambas páginas en viewport 375px** (iPhone SE / Android típico):
   - Revisar con DevTools (o browser automation) los breakpoints existentes.
   - Identificar elementos que se rompen, se superponen, tienen touch targets < 44px, o requieren scroll horizontal.
   - Registrar: header, filtros, selector de carrera/institución, tarjetas, gráficos, sección "Dónde se imparte", panel lateral de filtros (`instituciones_v2`).
2. **Presentar a Diego un plan detallado** con lista de problemas encontrados y propuesta CSS/JS para cada uno.
3. **Esperar confirmación explícita de Diego** antes de implementar nada.

Solo después de la aprobación, implementar en el orden propuesto.

---

## Qué hace esta tarea

Asegurar que ambas páginas sean usables en celular (375–430px de ancho) sin romper desktop.

### Áreas a revisar y mejorar

1. **Touch targets** — Todos los botones, checkboxes y summary clickeables deben tener área mínima de 44×44px (WCAG 2.5.5). Especialmente: botón ×, botones del custom select, resumen de institución clickeable.
2. **Header en móvil** — Logo + nombre + nav tabs: verificar que no se desborde ni apile mal en 375px.
3. **Panel lateral de filtros (`instituciones_v2`)** — Hoy es `position: sticky` en desktop. En móvil debe colapsar a algo usable (acordeón o sección colapsable arriba de los resultados).
4. **Sección "Dónde se imparte" (`index_v2`)** — La tabla de instituciones tiene 7 columnas y se desborda en móvil. Opciones: scroll horizontal con `overflow-x: auto`, o card layout vertical para cada fila.
5. **Gráficos** — Verificar que los canvas no se corten y que el alto mínimo sea legible en 375px.
6. **Custom selects** — Verificar que el dropdown no quede cortado por el viewport.
7. **Tipografía** — Revisar que font-size no sea < 14px en ningún elemento visible.

## Archivos a tocar

- `web/index_v2.html` (principalmente)
- `web/instituciones_v2.html` (principalmente, por panel lateral)

## Criterio de "tarea completa"

- Plan aprobado por Diego antes de implementar.
- Ambas páginas funcionan sin scroll horizontal en 375px.
- Touch targets cumplen 44px mínimo en los elementos interactivos principales.
- Panel lateral de filtros usable en móvil.
- Diego confirma visualmente en viewport reducido.
- `PLAN.md` actualizado con T20 ✅.
- `TAREA_21_PROMPT.md` generado (PWA instalable).
