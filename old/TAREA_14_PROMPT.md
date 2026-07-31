# Prompt — Tarea 14: Marca prominente en header/footer

## Contexto del proyecto

Estamos construyendo **Carrera Clara**, un comparador de carreras universitarias/IP/CFT para estudiantes chilenos de 4to medio, basado en datos públicos de MiFuturo.cl/SIES. Los archivos activos son `web/index_v2.html` (Comparar carreras) y `web/instituciones_v2.html` (Comparar instituciones).

Roadmap activo en `PLAN.md`. Historial de tareas completadas (1–13) en `PLAN_HISTORIAL.md`.

## Situación actual

Ambas páginas tienen header y footer funcionales (implementados en Tarea 6/rediseño), pero la identidad visual de "Carrera Clara" no es suficientemente prominente. El objetivo de esta tarea es reforzar la presencia de marca en ambos extremos de la página.

**Header actual:**
- Logo `assets/logo_carrera_clara.png` (fondo transparente) a 70px de alto, color blanco sobre fondo navy
- Eslogan en texto debajo del logo
- Tabs de navegación entre las dos vistas

**Footer actual:**
- Fondo navy, 3 columnas
- Contiene: nombre del proyecto, fuente de datos (SIES/MiFuturo.cl), contacto o créditos

## Qué hacer

Mejorar la marca visual en header y footer de ambas páginas:

1. **Header:** verificar que el logo se vea nítido, el eslogan sea legible y el contraste sea correcto. Si hay inconsistencias entre `index_v2.html` e `instituciones_v2.html`, unificarlas.

2. **Footer:** agregar un texto de atribución visible: `"Datos: SIES / MiFuturo.cl — Ministerio de Educación de Chile"` con link a `https://www.mifuturo.cl`. El link debe abrirse en nueva pestaña.

3. **Consistencia entre páginas:** el header y footer de ambos archivos deben ser visualmente idénticos (mismos colores, tamaños, espaciados).

## Archivos a tocar

Solo CSS y HTML (bloques `<style>` y `<header>`/`<footer>`) de:
- `web/index_v2.html`
- `web/instituciones_v2.html`

No tocar: `web/data/`, `mifuturo/`, scripts de exportación.

## Criterio de tarea completa

1. El logo se ve nítido en desktop y móvil.
2. El eslogan es legible (contraste suficiente sobre el fondo navy).
3. El footer muestra la atribución de datos con link funcional a mifuturo.cl.
4. Header y footer son visualmente idénticos en ambas páginas.

## Al terminar

1. Levantar `python -m http.server 8000` desde `web/` y abrir automáticamente `Start-Process "http://localhost:8000/index_v2.html"`.
2. Cuando Diego confirme: marcar Tarea 14 como completada en `PLAN.md` y generar `TAREA_15_PROMPT.md`. Mover este archivo a `old/`.
