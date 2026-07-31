# Prompt — Tarea 6 / Sesión 3a: Sistema CSS/Visual (sin JS ni DOM)

> **Requisito previo:** Tareas 6–11 completadas. Esta sesión es la primera mitad del rediseño visual final. Solo toca CSS — ningún JS, ningún cambio estructural de DOM.

---

## Contexto del proyecto

Comparador de carreras para estudiantes chilenos de 4to medio. Dos páginas HTML estáticas, autocontenidas, sin build step:
- `web/index.html` — Comparar carreras (190 genéricas SIES)
- `web/instituciones.html` — Comparar instituciones (1690 combos institución×carrera)

Ambas comparten el mismo bloque `<style>` con variables CSS en `:root`. Toda la lógica JS está inline en el mismo archivo. La Sesión 3 del rediseño está dividida en **3a (CSS, esta sesión)** y **3b (acordeón JS + arancel, siguiente sesión)**.

---

## Dirección visual aprobada (Diego, 2026-06-25)

### Paleta
| Token | Valor | Rol |
|---|---|---|
| `--color-bg` | `#f5f6f4` | Fondo página — blanco cálido |
| `--color-surface` | `#ffffff` | Superficie de tarjeta |
| `--color-header-bg` | `#0f2e45` | **Header navy invertido** (el riesgo deliberado — rompe el patrón gobierno) |
| `--color-text` | `#1c2b36` | Texto principal |
| `--color-text-muted` | `#6b7a86` | Texto secundario |
| `--color-primary` | `#1a7f64` | Verde mineral (no azul) |
| `--color-primary-light` | `#e6f4f0` | Tinte verde — estados activos |
| `--color-accent` | `#e8960a` | Ámbar — salarios y costos |
| `--color-danger` | `#c0392b` | Datos faltantes / alertas |
| `--color-border` | `#dde1e7` | Bordes suaves |
| `--color-chart-1` | `#1a7f64` | Chart — serie 1 (verde) |
| `--color-chart-2` | `#e8960a` | Chart — serie 2 (ámbar) |
| `--color-chart-3` | `#3b82f6` | Chart — serie 3 (azul cielo) |

Reemplazar los valores `--color-badge-warning-*` y `--color-badge-missing-*` también:
- `--color-badge-warning-bg: #fff8e6` / `--color-badge-warning-text: #92600a`
- `--color-badge-missing-bg: #fde8e8` / `--color-badge-missing-text: #8b1a1a`

### Tipografía
Añadir antes del `<style>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

Actualizar variables:
- `--font-family: 'Inter', system-ui, -apple-system, sans-serif;`
- `--font-display: 'Figtree', system-ui, sans-serif;` (nueva variable)
- `--font-base: 16px;` (sin cambio)

Aplicar `font-family: var(--font-display)` a: `h1`, `h2`, `h3`, `.card-header h3`, `.card-metric-value`, la pestaña activa `.activo` en `nav.tabs`.

### Header
El `header.app-header` pasa a:
- `background: var(--color-header-bg)` (navy)
- `color: #ffffff`
- El `h1` y `.subtitle` en blanco / blanco con 80% opacidad
- Los links de `nav.tabs` en blanco con 70% opacidad; `.activo` con `background: rgba(255,255,255,0.18)` y `color: #ffffff` (sin cambio de fondo azul)

### Tarjetas
- `background: var(--color-surface)` (blanco puro)
- `border: 1px solid var(--color-border)`
- `border-radius: 1rem` (subir de 0.5rem)
- `box-shadow: 0 2px 12px rgba(0,0,0,0.07)`
- Padding interno: `var(--space-3)` (sin cambio)

### Chips y métricas (.card-icon-chip, .card-metric)
- `.card-icon-chip`: `background: var(--color-bg)`, `border: 1px solid var(--color-border)`, `border-radius: 2rem`, texto en `var(--color-text-muted)`, `font-size: 0.82rem`
- `.card-metric-value`: `font-family: var(--font-display)`, `font-size: 1.5rem`, `font-weight: 700`, color `var(--color-primary)` para empleabilidad, `var(--color-accent)` para ingreso
- `.card-metric-label`: `font-size: 0.78rem`, `color: var(--color-text-muted)`, uppercase + `letter-spacing: 0.04em`

### Aviso de usabilidad (#aviso-usabilidad)
- `background: var(--color-primary-light)`, border `var(--color-primary)`, texto `var(--color-primary)` oscurecido (`color-mix` o `#0d5c47`)

### Fondo del body
- `background: var(--color-bg)` (ya tiene esta variable, solo cambiar el valor en `:root`)

---

## Lo que esta sesión NO toca

- Ninguna función JS (ni una línea)
- Ninguna estructura HTML (`<div>`, `<section>`, etc.) — solo atributos `class` si una clase cambia de nombre
- Los archivos `web/data/core.json`, `web/data/instituciones.json`, ningún `.py`
- La lógica de gráficos Chart.js (colores de datasets sí cambian vía `--color-chart-*`, pero solo en el bloque CSS, no en el JS)

---

## Definición de "sesión 3a completa"

1. Ambos HTML tienen `:root` actualizado con la nueva paleta.
2. Google Fonts link presente antes del `<style>` en ambos.
3. Header navy en ambos — contraste WCAG AA verificado (blanco sobre `#0f2e45` = ratio ~9:1, OK).
4. Tarjetas con sombra, radio 1rem, borde sutil.
5. `.card-metric-value` usando `Figtree` y colores semánticos.
6. `node --check` sobre el JS extraído pasa (sin errores de sintaxis — al tocar CSS dentro de `<style>` no debería haber JS afectado, pero verificar de todas formas).
7. Fork code-review: agente dedicado lee ambos HTML y reporta: (a) variables CSS referenciadas pero no declaradas, (b) clases CSS con reglas que se cancelen entre sí, (c) cualquier selector que ya no matchee markup existente.
8. `python -m http.server` + `Invoke-WebRequest` confirmando 200 en `index.html` e `instituciones.html`.

---

## Verificación con subagente

Al finalizar los cambios, antes de declarar la sesión completa, lanza un **fork agent** con este prompt:

> "Eres un revisor de CSS. Lee `web/index.html` y `web/instituciones.html` de este proyecto. Busca: (1) variables CSS con prefijo `--color-` o `--font-` que se usen en el CSS pero no estén declaradas en `:root`; (2) reglas CSS que se cancelen mutuamente por especificidad (ej. `.card .metric-value` vs `.metric-value`); (3) selectores `.foo` que no aparezcan en ninguna parte del HTML del archivo (clases fantasma). Reporta solo hallazgos reales, no advertencias genéricas."

---

## Al terminar

- Actualizar `PLAN.md`: cambiar "Sesión 3a (pendiente)" → "Sesión 3a (completada, fecha)".
- Mover este archivo a `old/TAREA_6_SESION3A_PROMPT.md`.
- Verificación visual en navegador real: pendiente de Diego (abrir `web/index.html` con el servidor HTTP, confirmar header navy, tarjetas con sombra, tipografía Figtree en títulos).
