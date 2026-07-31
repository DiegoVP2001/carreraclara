# Prompt — Tarea 6 / Sesión 3b: Acordeón DOM+JS + Estado vacío + Arancel dot-range

> **Requisito previo:** Sesión 3a completada. El sistema CSS ya tiene la nueva paleta (verde `#1a7f64`, navy `#0f2e45`, ámbar `#e8960a`), tipografía Figtree+Inter, cards con sombra y radio 1rem. Esta sesión restructura el DOM y el JS — no toca `:root` ni el look visual (eso ya está).

---

## Contexto del proyecto

Comparador de carreras para estudiantes chilenos de 4to medio. Dos páginas HTML estáticas autocontenidas:
- `web/index.html` — Comparar carreras
- `web/instituciones.html` — Comparar instituciones

Esta sesión hace **dos cosas separadas y bien delimitadas**:
1. Restructurar los gráficos/contenido de ambas páginas en **secciones acordeón** con JS.
2. Rediseñar el gráfico de arancel en `instituciones.html` como **hybrid dot-range chart**.

---

## Parte 1 — Acordeón por secciones

### Decisión de diseño (aprobada, 2026-06-25)
Patrón: 6 secciones acordeón de College Scorecard con scroll continuo (`Expand All` / `Close All`) — **no tabs**. Los tabs ocultan secciones; el acordeón permite ver dos secciones abiertas a la vez haciendo scroll. Confirmado por Diego tras ver el sitio real (ver `tarea_8b_exploracion/hallazgos.md`).

### Secciones para `index.html` (Comparar carreras)

| Orden | Título | Banda color | Tinte fondo abierto | Contenido actual |
|---|---|---|---|---|
| 1 | Perfil del programa | `#3b82f6` | `#eff6ff` | Checkboxes tipo inst., área, acreditación, duración — el panel "dónde se imparte" |
| 2 | Puntajes de ingreso PAES | `#6366f1` | `#f0f0ff` | Mini barras apiladas de ponderaciones |
| 3 | Empleabilidad y retención | `#1a7f64` | `#e6f4f0` | Gráficos emp. 1er año, emp. 2do año, retención 1er y 2do año |
| 4 | Ingresos | `#e8960a` | `#fffbec` | Gráfico ingreso 4° año + distribución percentiles |
| 5 | Costos y arancel | `#e05252` | `#fff3f0` | (no hay gráfico de arancel en index.html — esta sección puede estar vacía o mostrar el bloque de badges de arancel si existe) |

### Secciones para `instituciones.html` (Comparar instituciones)

| Orden | Título | Banda color | Tinte fondo abierto | Contenido actual |
|---|---|---|---|---|
| 1 | Perfil institucional | `#3b82f6` | `#eff6ff` | Panel de info general (acreditación, tipo sociedad, web, dirección) |
| 2 | Empleabilidad y retención | `#1a7f64` | `#e6f4f0` | Gráficos emp. 1er año, retención, duración real |
| 3 | Ingresos | `#e8960a` | `#fffbec` | Gráfico banda de ingreso al 4° año |
| 4 | Costos y arancel | `#e05252` | `#fff3f0` | Gráfico arancel 2026 (ver Parte 2 abajo) |

### Estructura HTML de cada sección acordeón

```html
<section class="accordion-section" data-section="empleabilidad" open>
  <button class="accordion-header" aria-expanded="true">
    <span class="accordion-band"></span>
    <span class="accordion-title">Empleabilidad y retención</span>
    <span class="accordion-chevron">▾</span>
  </button>
  <div class="accordion-body">
    <!-- contenido existente de esta sección -->
  </div>
</section>
```

**CSS para la banda de color lateral (el elemento firma):**
```css
.accordion-section[data-section="empleabilidad"] .accordion-band {
  background: #1a7f64;
}
.accordion-section[data-section="empleabilidad"][aria-expanded="true"] .accordion-body {
  background: #e6f4f0;
}
```
(Repetir para las 4-5 secciones con sus colores.)

### JS del acordeón

```js
function initAccordions() {
  document.querySelectorAll('.accordion-header').forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
    });
  });
  document.getElementById('btn-expandir-todo').addEventListener('click', () => {
    document.querySelectorAll('.accordion-header').forEach(b => b.setAttribute('aria-expanded', 'true'));
  });
  document.getElementById('btn-colapsar-todo').addEventListener('click', () => {
    document.querySelectorAll('.accordion-header').forEach(b => b.setAttribute('aria-expanded', 'false'));
  });
}
```

El acordeón usa `aria-expanded` en el `<button>` como única fuente de estado — el CSS controla visibilidad con `[aria-expanded="false"] + .accordion-body { display: none }`. Sin JS adicional para toggle.

### Botones globales

Encima de todas las secciones acordeón (antes de la primera):
```html
<div class="accordion-controls">
  <button id="btn-expandir-todo">Expandir todo</button>
  <button id="btn-colapsar-todo">Colapsar todo</button>
</div>
```

### Estado inicial

- **Sección 1 ("Perfil"):** abierta por defecto (`aria-expanded="true"`)
- **Resto:** colapsadas por defecto (`aria-expanded="false"`)
- Excepción: si hay ≥1 carrera/combo seleccionado al cargar la página (URL con query params, pendiente de Tarea 12 backlog item 10), abrir las secciones que tengan datos visibles.

---

## Parte 2 — Estado vacío rediseñado

El estado actual (sin carreras seleccionadas) es básicamente nada visible. Reemplazarlo por:

```html
<div id="empty-state" class="empty-state">
  <svg ...><!-- ícono SVG simple: lupa + documento, sin stock art --></svg>
  <h2>Compara carreras lado a lado</h2>
  <p>Busca una carrera arriba para empezar. Puedes comparar hasta las que quieras.</p>
</div>
```

**CSS:**
```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-3);
  text-align: center;
  color: var(--color-text-muted);
}
.empty-state h2 { font-family: var(--font-display); color: var(--color-text); }
```

Se muestra cuando `selected.length === 0`; se oculta (`.hidden`) cuando hay ≥1 selección. Igual patrón para `instituciones.html`.

---

## Parte 3 — Gráfico de arancel dot-range (solo `instituciones.html`)

### El problema
El gráfico actual (`chart-arancel`) usa floating bars para exactos Y para rangos — dos convenciones mezcladas, difícil leer cuál es "el precio real" vs. "un estimado".

### La solución aprobada: hybrid dot-range en Chart.js
- **Exacto (`arancel_exacto !== null`):** punto sólido. En Chart.js se logra con floating bar `[valor - delta, valor + delta]` donde `delta = 40000` (40k CLP — mínimo perceptible, no representa rango real), opacidad 100%, color `var(--color-primary)`.
- **Rango (`arancel_aproximado === true`):** floating bar real `[arancel_min, arancel_max]`, opacidad 45%, color `var(--color-text-muted)`, borde discontinuo (configurar `borderDash` en Chart.js o usar `borderWidth`).
- **Sin dato (`arancel_exacto === null && !arancel_aproximado`):** barra omitida (`null`), badge "sin dato de arancel" ya existente.
- **UF:** ya se omiten del gráfico (implementado en Tarea 7 Iteración 4).

**Leyenda debajo del gráfico (HTML estático, no Chart.js legend):**
```html
<div class="arancel-leyenda">
  <span class="leyenda-exacto">● Valor exacto</span>
  <span class="leyenda-rango">▬ Estimado (rango entre sedes/jornadas)</span>
</div>
```

**Tooltip:** para exacto mostrar el valor puntual real; para rango mostrar "De $X.XXX.XXX a $Y.YYY.YYY".

### Lo que NO cambia en el gráfico de arancel
- El dataset JSON (`arancel_exacto`, `arancel_min`, `arancel_max`, `arancel_aproximado`, `arancel_moneda`) — no regenerar `instituciones.json`.
- Los badges "arancel en UF", "sin dato de arancel", "arancel aproximado (rango)" — siguen igual.
- La función `resolver_arancel` en `export_instituciones.py` — no tocar.

---

## Verificación con subagentes

### Paso 1 — node --check + aserciones

Después de los cambios, verificar con Node.js:
```bash
node --check web/index.html  # solo si Node acepta HTML; si no, extraer el <script> primero
```

Aserciones mínimas a ejecutar sobre el JS real del archivo:
1. `initAccordions` existe como función o bloque
2. `btn-expandir-todo` y `btn-colapsar-todo` tienen listeners
3. El gráfico de arancel usa delta para exactos (buscar la constante `40000` o equivalente)
4. La función de tooltip de arancel distingue exacto vs. rango

### Paso 2 — Fork code-review

Lanzar fork agent con:
> "Revisa `web/index.html` y `web/instituciones.html`. Busca: (1) secciones acordeón cuyo `aria-expanded` inicial podría no coincidir con el estado visual CSS; (2) el gráfico de arancel en `instituciones.html` — verifica que el delta de exactos no se aplique a rangos y viceversa; (3) cualquier evento listener que se registre más de una vez si `renderSelected()` se llama múltiples veces (patrón clásico de bug en re-renders sin cleanup); (4) el estado vacío: ¿se oculta correctamente cuando `selected.length > 0`?"

### Paso 3 — skill `verify` (si disponible)

Intentar abrir la página en navegador real y confirmar visualmente:
- Header navy + tarjetas con sombra presentes (de Sesión 3a)
- Secciones acordeón colapsan/expanden al hacer click
- "Expandir todo" abre todas; "Colapsar todo" las cierra
- Estado vacío visible al cargar sin selección
- Gráfico arancel: punto compacto para exactos, barra ancha translúcida para rangos

---

## Definición de "sesión 3b completa"

1. Ambas páginas tienen acordeón funcional con las secciones especificadas arriba.
2. Botones "Expandir todo" / "Colapsar todo" operativos.
3. Estado vacío visible en ambas páginas.
4. Gráfico de arancel en `instituciones.html` usa dot para exactos y barra semitransparente para rangos, con leyenda.
5. Los 3 pasos de verificación ejecutados (node, fork, verify).
6. `python -m http.server` + `Invoke-WebRequest` confirmando 200 en ambos HTML y JSONs.

---

## Al terminar

- Actualizar `PLAN.md`: cambiar "Sesión 3b (pendiente)" → "Sesión 3b (completada, fecha)" + resumen de 2-3 líneas de qué secciones quedaron en el acordeón.
- Marcar en `PLAN.md` el ítem 4 del backlog como completado.
- Mover `TAREA_6_SESION3_PROMPT.md` (el original) a `old/` si no está ya.
- Mover este archivo a `old/TAREA_6_SESION3B_PROMPT.md`.
- Evaluar si corresponde abrir alguna de las pantallas TODO del roadmap (Explorar carreras, Buscar instituciones) como siguiente tarea — ver sección "Tarea 12" de `PLAN.md`.
