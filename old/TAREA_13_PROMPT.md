# Prompt — Tarea 13: Layout 3 columnas en comparación

## Contexto del proyecto

Estamos construyendo **Carrera Clara**, un comparador de carreras universitarias/IP/CFT para estudiantes chilenos de 4to medio, basado en datos públicos de MiFuturo.cl/SIES. Los archivos activos son `web/index_v2.html` (Comparar carreras) y `web/instituciones_v2.html` (Comparar instituciones). La lógica JS y los datos JSON están completos — esta tarea es exclusivamente de presentación visual.

Roadmap activo en `PLAN.md`. Historial de decisiones técnicas en `PLAN_HISTORIAL.md`.

## Situación actual

Cuando el usuario selecciona carreras o combos institución+carrera para comparar, estos se renderizan como una lista vertical:

```css
/* index_v2.html y instituciones_v2.html — mismo patrón */
ul#selected-list {
  display: flex;
  flex-direction: column;  /* tarjetas apiladas una debajo de otra */
  gap: var(--space-1);
}
```

Cada tarjeta ocupa el 100% del ancho disponible, lo que hace que con 3 o más elementos la página se vuelva muy larga de scrollear.

- En `index_v2.html`: cada tarjeta es `li.carrera-card`
- En `instituciones_v2.html`: cada tarjeta es `li.combo-card`

Los gráficos de comparación (Chart.js) están en secciones **separadas** debajo de las tarjetas — no están dentro de cada `li`. El cambio de layout no los afecta directamente.

## Qué hacer

Cambiar `ul#selected-list` de lista vertical a **grilla de 3 columnas** en ambos archivos.

**Comportamiento esperado:**
- **Desktop (≥ 1024px):** 3 columnas de igual ancho (`repeat(3, 1fr)`)
- **Tablet (≥ 640px y < 1024px):** 2 columnas
- **Móvil (< 640px):** 1 columna

**Consideraciones importantes:**
1. Cada tarjeta contiene bastante contenido (íconos, métricas titulares, checkboxes de tipo, mini barras de ponderación PAES). Asegurarse de que el contenido interno no desborde en el ancho más chico de cada columna.
2. El botón "✕ Eliminar" de cada tarjeta debe seguir siendo accesible.
3. El componente `#tooltip-popup` usa `position: fixed` — no se ve afectado por el cambio de layout del contenedor.
4. Los Chart.js que están en secciones `<figure>` fuera de `#selected-list` no deben tocarse en esta tarea (son globales, no por tarjeta).
5. Verificar que el `#aviso-usabilidad` (banner que aparece con ≥7 ítems seleccionados) sigue apareciendo correctamente sobre la grilla.

## Archivos a tocar

Solo CSS (bloque `<style>`) de:
- `web/index_v2.html` — regla de `ul#selected-list` y ajustes internos de `li.carrera-card` si es necesario
- `web/instituciones_v2.html` — ídem para `li.combo-card`

No tocar: `web/export_json.py`, `web/export_instituciones.py`, `web/data/`, `mifuturo/`.

## Criterio de tarea completa

1. Con 1–2 ítems seleccionados: se muestran en 1 o 2 columnas (no fuerza 3 vacías).
2. Con 3+ ítems: grilla de 3 columnas visible y legible.
3. En viewport < 640px: vuelve a 1 columna.
4. El contenido interno de cada tarjeta no desborda horizontalmente.

## Al terminar

1. Levantar `python -m http.server 8000` desde `web/` y abrir automáticamente `Start-Process "http://localhost:8000/index_v2.html"` para que Diego revise.
2. Cuando Diego confirme: marcar Tarea 13 como completada en `PLAN.md` (fecha + 2 líneas de resumen) y generar `TAREA_14_PROMPT.md`.
