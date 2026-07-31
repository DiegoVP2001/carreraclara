# Prompt para iniciar la Tarea 8 — Auditoría College Scorecard + backlog de mejoras

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/`.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto y `PLAN.md` completo (especialmente la sección "Tarea 8" y "Roadmap general actualizado" al final) para tener el contexto de las dos pestañas Comparar ya construidas:

- **Comparar carreras** (`web/index.html` + `web/export_json.py`) — Tarea 6, Sesión 2 + iteración UX.
- **Comparar instituciones** (`web/instituciones.html` + `web/export_instituciones.py`) — Tarea 7 + iteraciones 2, 3 y 4 (esta última agregó panel institucional y arancel cruzado escalonado por certeza).

**Tu tarea: sesión de investigación y síntesis, sin construir UI todavía.** Objetivo: evaluar con rigor (no solo con la impresión general que guio la Tarea 6) si conviene agregar más filtros, gráficos o tipos de comparación a las dos pestañas ya construidas, antes de invertir en el rediseño visual final (Tarea 6, Sesión 3 — ver `TAREA_6_SESION3_PROMPT.md`, que **ya tiene un pendiente anotado**: el gráfico de arancel anual 2026 en `instituciones.html` necesita ser repensado de raíz, no solo repintado — tenlo en mente si tu auditoría toca algo relacionado a comparación de costos).

## Qué hacer

1. **2-3 sub-agentes de exploración** (vía `WebFetch`/`WebSearch` — sin herramienta de navegador en este entorno, así que el análisis es sobre contenido/estructura de página, no interacción en vivo) con preguntas específicas y no superpuestas, por ejemplo:
   - (a) Taxonomía de filtros de `collegescorecard.ed.gov/search/` (el buscador de instituciones, equivalente a nuestro futuro "Buscar instituciones" — ítem 5 del roadmap de pantallas en `PLAN.md` Tarea 6).
   - (b) Qué métricas/gráficos muestra su función **Compare** una vez elegidos 2+ programas/escuelas — el equivalente real a nuestras pestañas Comparar, más relevante que `/search/` para esta evaluación.
   - (c) Opcionalmente, cualquier documentación/repo público sobre las decisiones de diseño de Scorecard (es open source), si aporta el "por qué" y no solo el "qué".
2. **Sintetiza los hallazgos en un backlog acotado: máximo ~8-10 recomendaciones**, cada una con:
   - Qué pestaña afecta (carreras / instituciones / ambas).
   - Esfuerzo estimado (bajo/medio/alto).
   - Si depende de pantallas TODO que aún no existen (Explorar carreras, Buscar instituciones — ítems 1 y 5 del roadmap).
3. Puedes señalar si algún hallazgo sugiere fusionar/conectar pantallas hoy planeadas como separadas (ej. que buscar y comparar deberían estar más integrados, como en Scorecard) — no cierres esa puerta de antemano aunque implementarla sea fase posterior.

## Restricciones

- **No implementes nada de la Tarea 9 todavía.** El entregable es el documento de backlog. Diego aprueba qué entra a la Tarea 9 antes de que se implemente nada.
- No toques `comparador.db`, `queries.py`, ni los exports/HTML existentes.

## Al terminar

- Actualiza `PLAN.md`: marca la Tarea 8 como completada, pega el backlog final (las recomendaciones aprobadas o pendientes de aprobación) y deja explícito qué decidió Diego para la Tarea 9.
- Si Diego aprueba el alcance de la Tarea 9 en la misma sesión, escribe `TAREA_9_PROMPT.md` con ese alcance ya cerrado (mismo patrón que los prompts anteriores).
