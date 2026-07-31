# TAREA 19d — "Dónde se imparte" mejorado: animaciones y contraste

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T17** — Sección "Dónde se imparte" en `index_v2.html`: stats bar (N instituciones, N regiones, rango arancel), badges por tipo de institución (Universidad/IP/CFT) con color, acreditación con color, empleabilidad 1er año, regiones compactas (`>3 → "N regiones"`). El panel se expande al hacer clic en una flecha por carrera.
- **T19, T19b, T19c** — Sistema de animaciones CSS en tarjetas, enter/exit, hover/focus.

---

## ⚠️ FLUJO OBLIGATORIO: plan → aprobación → ejecución

**Antes de escribir una sola línea de código**, hacer lo siguiente:

1. **Leer el código actual** de la sección "Dónde se imparte" en `index_v2.html`:
   - Encontrar la función que renderiza el panel (probablemente `renderDetallePanels` o similar).
   - Identificar el mecanismo de mostrar/ocultar (¿`hidden`? ¿`display:none`? ¿clase CSS? ¿`max-height`?).
   - Revisar el CSS actual del panel, la tabla de instituciones, las filas, y los badges.
   - Revisar cómo se mueve la flecha ▾/▴ hoy.
2. **Presentar a Diego un plan detallado** que incluya:
   - Estado actual de cada aspecto (apertura, flecha, tabla, contraste, hover en filas).
   - Propuesta concreta para cada uno: qué CSS/JS se agrega o modifica, y qué efecto produce.
   - Mockup textual o descripción del resultado esperado si ayuda a visualizar.
3. **Esperar confirmación explícita de Diego** antes de implementar nada.

Solo después de la aprobación, implementar en el orden propuesto.

---

## Qué hace esta tarea

Mejorar la sección "Dónde se imparte" que aparece en cada tarjeta de carrera (`index_v2.html`) en cuatro áreas:

### 1. Animación al abrir/cerrar el panel
- El panel actualmente aparece/desaparece de forma abrupta.
- Añadir apertura suave: patrón `max-height` + `opacity` con `transition` ("accordion suave").
- Cierre igualmente animado (no solo desaparece).

### 2. Rotación animada de la flecha del acordeón
- La flecha (▾ / ▴) debería rotar con `transform: rotate(180deg)` y `transition` al abrir/cerrar.
- No cambiar el carácter Unicode — solo rotar con CSS.

### 3. Contraste y legibilidad en la tabla de instituciones
- Añadir zebra-stripes alternadas (filas pares/impares con fondo levemente distinto) para facilitar la lectura en tablas largas.
- Revisar el contraste de los badges de tipo (Universidad=azul, IP=naranja, CFT=verde) sobre el fondo de la tabla: deben cumplir WCAG AA mínimo.
- Si el header de la tabla se pierde al hacer scroll, considerar `position: sticky; top: 0`.

### 4. Hover en filas de la tabla
- `:hover` sobre cada `<tr>` de institución → highlight sutil de fila (fondo más oscuro + `transition`).
- Consistente con las animaciones hover de T19c.

## Archivos a tocar

- `web/index_v2.html` (principalmente)

## Criterio de "tarea completa"

- Plan aprobado por Diego antes de implementar.
- El panel "Dónde se imparte" se abre y cierra con animación suave (sin brusquedad).
- La flecha rota con transición al abrir/cerrar.
- Las filas de la tabla tienen contraste alternado legible y `:hover` highlight.
- Diego confirma visualmente.
- `PLAN.md` actualizado con T19d ✅.
- `TAREA_20_PROMPT.md` generado (optimización móvil).
