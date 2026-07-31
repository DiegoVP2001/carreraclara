# Prompt para iniciar la Tarea 10 — Glosario interactivo (tooltip inline)

> Copia y pega el contenido de abajo al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para ejecutar la Tarea 10 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto y `PLAN.md` completo (especialmente la sección "Tarea 10" y el "Roadmap general actualizado" al final) para tener el contexto de las dos pestañas ya construidas:

- **Comparar carreras** (`web/index.html`)
- **Comparar instituciones** (`web/instituciones.html`)

**Tu tarea (Tarea 10): implementar el tooltip inline simple** — el patrón de ayuda contextual que Scorecard usa en los íconos ℹ de cada métrica individual dentro de `/compare/` y `/school/`.

## Alcance confirmado (Tarea 8b)

Dos patrones distintos, a implementar en sesiones separadas:

1. **Tooltip inline simple (esta tarea)** — click/hover sobre un ícono ℹ junto a cada nombre de métrica, muestra texto corto de definición. Implementación: atributo `data-tooltip` en el HTML generado por JS + componente CSS/JS mínimo reutilizable entre ambas pestañas. No usa un drawer lateral con buscador.
2. **Drawer lateral completo** (Tarea 12, diferida) — aparece en tarjetas de resultados de "Buscar instituciones"/"Explorar carreras" que aún no existen. No se construye en esta sesión.

## Métricas a cubrir (~15-20 ya expuestas en ambas pestañas)

Redactar el contenido de los tooltips a mano, basado en `mifuturo/MODELO_DATOS.md` (no hay PDF glosario para `mifuturo/`):

**`index.html` (Comparar carreras) — benchmark nacional:**
- Empleabilidad 1er/2do año
- Retención 1er/2do año
- Ingreso al 4° año (con percentiles 10/50/90)
- Tipo de institución (toggle de benchmark)
- Sin comparación nacional (badge)

**`index.html` — panel "dónde se imparte":**
- Arancel 2026 (con nota de UF)
- Ponderaciones PAES (los 8 componentes: NEM, Ranking, Lenguaje, Mat., Mat.2, Historia, Ciencias, Otros) — añadidas en Tarea 9
- Vacantes 1er semestre
- Sin ponderación PAES reportada (badge)

**`instituciones.html` (Comparar instituciones):**
- Empleabilidad 1er/2do año
- Retención 1er año
- Banda de ingreso al 4° año de titulado
- Duración real (semestres)
- Arancel exacto vs. aproximado (niveles 1/2/3)
- Ponderaciones PAES en tarjeta de combo (Tarea 9)
- Acreditación / años de acreditación
- Sin ponderación PAES reportada (badge)
- Varía por sede/jornada (badge de ponderaciones)

**Estados de datos (badges) — cubrir todos:**
- "Sin comparación nacional" (26 carreras)
- "Institución sin ficha" (16 combos)
- "Sin dato de arancel", "Arancel en UF", "Arancel aproximado (rango)"
- "Sin ponderación PAES reportada" (Tarea 9)

## Qué hacer

1. **Diseñar el componente tooltip** reutilizable: atributo `data-tooltip` en el elemento HTML + CSS (posicionamiento, flecha, z-index, transición) + JS minimal (show/hide en hover+focus, cierra con Escape/clic fuera). Accesible: `role="tooltip"`, `aria-describedby`. Mismo bloque CSS/JS copiado en ambos archivos (son standalone, sin build step).
2. **Añadir íconos ℹ** junto a cada nombre de métrica en el JS de renderizado de ambos archivos (en las funciones que generan HTML dinámico: `renderGrupoInstitucion`, `renderSelected`, `renderCharts`, etc.).
3. **Redactar el contenido de los tooltips** (15-20 textos cortos, 1-2 frases, en español de Chile, nivel 4to medio).
4. **No implementar** el drawer lateral (Tarea 12) ni el polish de tarjetas tipo Scorecard (Tarea 11).

## Restricciones

- No tocar `mifuturo/loader.py`, `queries.py`, `export_json.py`, `export_instituciones.py`.
- No tocar `comparador.db`.
- Los exports deben seguir corriendo sin error después.

## Verificación

- Aserciones Node sobre lógica del componente tooltip (show/hide, posicionamiento).
- Confirmar textos de tooltip en el HTML servido (`python -m http.server` + `Invoke-WebRequest`).
- `node --check` sobre JS extraído (nota: la regex de normalización Unicode falla siempre en Node/Windows por encoding — es pre-existente, no es de esta tarea).

Al terminar, actualiza el estado de la Tarea 10 en `PLAN.md` y anota que la Tarea 11 (polish de tarjetas) sigue en el roadmap.
