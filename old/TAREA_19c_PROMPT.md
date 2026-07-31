# TAREA 19c — Hover/focus animations en todos los elementos interactivos de ambas páginas

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor: `python -m http.server 8000` desde `web/`.

Tareas anteriores completadas relevantes:
- **T19** — Enter/exit animations en `li.carrera-card` y `li.combo-card` (`.is-entering`, `.is-removing`).
- **T19b** — Animaciones extendidas a más elementos (toast, autocomplete, share bar, estado vacío, gráficos).

---

## ⚠️ FLUJO OBLIGATORIO: plan → aprobación → ejecución

**Antes de escribir una sola línea de código**, hacer lo siguiente:

1. **Auditar AMBAS páginas HTML completas**: leer el CSS de ambos archivos y listar todos los elementos interactivos existentes (botones, links, labels, sliders, inputs, tarjetas, badges, filas de tabla, ítems de lista, selects, etc.).
2. **Para cada elemento**, anotar:
   - ¿Tiene `:hover` hoy? ¿Tiene `transition`?
   - ¿Qué efecto se propone agregar o mejorar?
3. **Presentar a Diego una tabla de plan** con columna "elemento / estado actual / propuesta / páginas afectadas".
4. **Esperar confirmación explícita de Diego** antes de implementar nada.

Solo después de la aprobación, implementar todos los cambios aprobados.

---

## Qué hace esta tarea

Agregar o refinar animaciones sutiles al pasar el mouse (`:hover`) y al enfocar con teclado (`:focus-visible`) sobre **todos** los elementos interactivos de **ambas páginas**.

**Principio guía:** las animaciones de hover deben ser _ligeras_ — escala +1–2%, sombra más pronunciada, ligero lift (`translateY(-2px)`), o cambio de color/brillo. Nada dramático. El objetivo es que la interfaz "responda" al tacto sin distraer.

### Elementos candidatos — `index_v2.html`

- **`li.carrera-card`** — `:hover` → lift sutil (`translateY(-2px)`) + `box-shadow` más pronunciado. Asegurar que `transition` cubra `box-shadow`.
- **Botón × (quitar carrera)** — `:hover` → color más intenso + `scale(1.15)`.
- **Botón "Agregar"** (submit del selector) — `:hover` → `brightness` o `scale(1.02)` + sombra; `:active` → `scale(0.97)`.
- **Botón "Comparar"** (si existe separado) — igual que Agregar.
- **Botón "Compartir"** — igual.
- **Flecha de acordeón** (▾ que abre "Dónde se imparte") — `:hover` → color más oscuro.
- **Ítems del autocomplete** (`#autocomplete-list li`) — `:hover`/`[aria-selected]` → fondo de resaltado más visible + transición de color.
- **Labels de checkbox de tipo** (dentro de tarjetas) — `:hover` → fondo sutil + borde.
- **Links del footer** — `:hover` ya tiene `transition: color`; revisar si se puede mejorar.
- **Select de filtro de área** — `:focus` → borde más visible.
- **Input de búsqueda de carrera** — `:focus` → `box-shadow` de ring.

### Elementos candidatos — `instituciones_v2.html`

- **`li.combo-card`** — `:hover` → lift sutil + `box-shadow` más pronunciado (misma mecánica que carrera-card).
- **Botón × (quitar combo)** — `:hover` → color + `scale(1.15)`.
- **Botones Agregar / Compartir** — `:hover` + `:active` feedback.
- **Ítems del autocomplete de institución** — `:hover`/`[aria-selected]` → resaltado + transición.
- **Select de institución** (paso 1) y **Select de carrera** (paso 2) — `:focus` → ring visible.
- **Sliders del panel de filtros** (`input[type="range"]`) — thumb `:hover`/`:focus` → ring más pronunciado o cambio de color del thumb.
- **Custom select de Tipo/Área** (reemplazaron los `<select>` nativos en T19b) — `.custom-select-list li:hover` usa actualmente `--color-primary` (verde). **Diego quiere cambiar el color de hover/highlighted al azul del header** (`--color-header-bg: #0f2e45`) con fondo tipo `rgba(15,46,69,0.08)`. Incluir esto en el plan. Aplica a `.custom-select-list li:hover` y `.custom-select-list li.cs-selected` en ambas páginas.
- **Filas de la tabla de aranceles** (si hay tabla) — `:hover` → highlight de fila sutil.
- **Links del footer** — consistente con index_v2.
- **Botones de paginación o navegación** (si existen) — `:hover` + `:active`.
- **Badges/pills interactivos** (si alguno es clickeable) — `:hover` → `opacity` o `brightness`.

### Nota sobre `:focus-visible`

Cada efecto `:hover` debe tener su equivalente `:focus-visible` para accesibilidad con teclado. No usar `:focus` sola (eso activa el ring también al hacer clic con mouse, lo cual es visual ruido).

## Archivos a tocar

- `web/index_v2.html`
- `web/instituciones_v2.html`

## Criterio de "tarea completa"

- Plan aprobado por Diego antes de implementar.
- Todos los elementos aprobados en el plan tienen `:hover` y `:focus-visible` con `transition`.
- Se probó pasando el mouse por toda la interfaz de ambas páginas.
- Diego confirma visualmente que las animaciones se sienten ligeras, no invasivas.
- `PLAN.md` actualizado con T19c ✅.
- `TAREA_19d_PROMPT.md` ya existe (fue generado junto con este).
